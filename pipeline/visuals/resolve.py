"""Routes each visual segment's [ON SCREEN: ...] cue to one resolved local image
file. A beat is now typically several segments (script_parser.py splits a beat at
every inline cue) rather than one image per beat - this is the actual fix for
visuals holding static for a whole beat's duration.

Search-term cues go through sources.py (Wikimedia -> NASA -> Pixabay ->
Smithsonian, first license-clean hit wins); AI-generate cues go through
ai_generate.py (Pollinations.ai). A segment with no cue at all (e.g. "THE TURN" /
"CLOSE" in the Alexandria test script, which don't get their own ON SCREEN line)
falls back to holding the previous segment's resolved visual - cue-less segments
still need something on screen, and the alternative (erroring) would block every
real script.md that has one.

Every resolution is recorded in build/manifest.json, flat, keyed by composite
segment id (`beat_06_seg00`) - source url/license/artist, or the AI prompt used -
that's what the video description's source list is built from later.
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import config  # noqa: E402
from visuals import ai_generate, sources  # noqa: E402


def _ext_from_url(url: str, default: str = ".jpg") -> str:
    suffix = Path(url.split("?")[0]).suffix
    return suffix if suffix else default


def _resolve_cue(cue: dict | None, seg_id: str, visuals_dir: Path) -> dict | None:
    if cue is None:
        return None
    dest_stub = visuals_dir / seg_id
    for term in cue.get("search_terms", []):
        result = sources.search_and_download(term, dest_stub, _ext_from_url)
        if result:
            return {"id": seg_id, **result}
    prompt = cue.get("ai_generate_prompt")
    if prompt:
        dest = dest_stub.with_suffix(".jpg")
        ai_generate.generate(prompt, dest)
        return {
            "id": seg_id,
            "path": str(dest),
            "source": "pollinations",
            "title": prompt,
            "url": None,
            "license": "AI-generated (Pollinations.ai)",
            "artist": "AI-generated",
            "page_url": None,
        }
    return None


def resolve_all(slug: str, force: bool = False) -> tuple[list[dict], str]:
    build = config.build_dir(slug)
    meta = json.loads((build / "narration_meta.json").read_text(encoding="utf-8"))["beats"]
    visuals_dir = build / "visuals"
    visuals_dir.mkdir(exist_ok=True)
    manifest_path = build / "manifest.json"

    cached = {}
    if manifest_path.exists() and not force:
        for entry in json.loads(manifest_path.read_text(encoding="utf-8")):
            if Path(entry["path"]).exists():
                cached[entry["id"]] = entry

    manifest = []
    last_resolved = None
    for beat in meta:
        for seg_i, seg in enumerate(beat["segments"]):
            seg_id = f"{beat['id']}_seg{seg_i:02d}"
            entry = cached.get(seg_id)
            if entry is None:
                entry = _resolve_cue(seg.get("on_screen"), seg_id, visuals_dir)
                if entry is None:
                    if last_resolved is None:
                        raise RuntimeError(
                            f"{seg_id} has no ON SCREEN cue and there's no earlier segment to fall back to"
                        )
                    entry = {**last_resolved, "id": seg_id, "fallback_from": last_resolved["id"]}
            manifest.append(entry)
            last_resolved = entry

    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    return manifest, str(manifest_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("slug")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    manifest, path = resolve_all(args.slug, force=args.force)
    print(f"Resolved {len(manifest)} segments -> {path}")
    for entry in manifest:
        note = f" (fallback from {entry['fallback_from']})" if "fallback_from" in entry else ""
        print(f"  {entry['id']}: [{entry['source']}] {entry.get('title', '')[:60]}{note}")
