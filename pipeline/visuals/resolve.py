"""Routes each visual segment's [ON SCREEN: ...] cue to one resolved PRIMARY image
(full content square) and, optionally, its [EVIDENCE: ...] cue to a smaller proof
inset composited over it later in assemble.py/captions.py. A beat is now typically
several segments (script_parser.py splits a beat at every inline cue) rather than one
image per beat - this is the actual fix for visuals holding static for a whole beat's
duration.

**Visual-sourcing priority flip (2026-10-27, see idea.md)**: the PRIMARY visual is now
always AI-generated - a pre-placed Gemini asset (config.GEMINI_VISUALS_DIRNAME,
dropped manually by Claude during a live Chrome session, never written by code) wins
if present, else Pollinations.ai (ai_generate.py) generates one from the cue's
`AI-generate:` prompt. Wikimedia/NASA/Pixabay/Smithsonian (sources.py) are REMOVED
from the primary path entirely - a bare search-term ON SCREEN cue now raises, rather
than silently resolving against those sources, since a script written under the old
convention needs rewriting, not reinterpreting. Those same sources (plus live Chrome
screenshots) are now evidence-only: `_resolve_evidence` below, fail-soft since a
missing/empty evidence result should just mean no inset for that one segment, never
block the render.

A segment with no cue at all (e.g. "THE TURN" / "CLOSE" in the Alexandria test script,
which don't get their own ON SCREEN line) falls back to holding the previous
segment's resolved PRIMARY visual only - its evidence (if any) is deliberately NOT
inherited; each segment's evidence is resolved independently every time, see
resolve_all() below.

Every resolution is recorded in build/manifest.json, flat, keyed by composite
segment id (`beat_06_seg00`) - source url/license/artist, or the AI prompt used -
plus an optional nested "evidence" key with the same shape - that's what the video
description's source list is built from later.
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


def _find_pre_placed(dirpath: Path, seg_id: str) -> Path | None:
    """A file manually dropped at <dirpath>/<seg_id>.<any ext> - used for both the
    live-Gemini primary-visual path and the live-screenshot evidence path. Never
    written by this pipeline's own code, only read."""
    for p in sorted(dirpath.glob(f"{seg_id}.*")):
        return p
    return None


def _resolve_primary(cue: dict | None, seg_id: str, visuals_gemini_dir: Path, visuals_dir: Path) -> dict | None:
    gemini_asset = _find_pre_placed(visuals_gemini_dir, seg_id)
    if gemini_asset is not None:
        return {
            "id": seg_id,
            "path": str(gemini_asset),
            "source": "gemini",
            "title": (cue or {}).get("ai_generate_prompt") or (cue or {}).get("raw", ""),
            "url": None,
            "license": "AI-generated (Gemini, live via Chrome)",
            "artist": "Gemini",
            "page_url": None,
        }
    if cue is None:
        return None
    if cue.get("search_terms"):
        raise ValueError(
            f"{seg_id}: ON SCREEN cue has a bare search term "
            f"({cue['search_terms']!r}) - real-photo sources are evidence-only now "
            f"(2026-10-27 visual-sourcing flip, see idea.md). Rewrite this cue as "
            f"AI-generate: for the primary visual, or move the term to a separate "
            f"[EVIDENCE: ...] cue if it's meant to be proof, not the main visual."
        )
    prompt = cue.get("ai_generate_prompt")
    if prompt:
        dest = (visuals_dir / seg_id).with_suffix(".jpg")
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


def _resolve_evidence(cue: dict | None, seg_id: str, evidence_dir: Path) -> dict | None:
    """Fail-soft by design - unlike the primary visual, a missing or empty evidence
    result just means this one segment gets no inset, never blocks the render."""
    if cue is None:
        return None
    screenshot_url = cue.get("screenshot_url")
    if screenshot_url:
        shot = _find_pre_placed(evidence_dir, seg_id)
        if shot is None:
            print(
                f"  [warn] {seg_id}: EVIDENCE screenshot cue for {screenshot_url!r} has no "
                f"captured file yet at {evidence_dir / seg_id}.* - skipping evidence for this segment"
            )
            return None
        return {
            "source": "screenshot",
            "path": str(shot),
            "title": cue.get("raw", screenshot_url),
            "url": screenshot_url,
            "license": "Live screenshot (Chrome, captured during session)",
            "artist": None,
            "page_url": screenshot_url,
        }
    for term in cue.get("search_terms", []):
        result = sources.search_and_download(term, evidence_dir / seg_id, _ext_from_url)
        if result:
            return {"id": seg_id, **result}
    if cue.get("search_terms"):
        print(f"  [warn] {seg_id}: EVIDENCE cue found nothing sourceable for {cue['search_terms']!r} - skipping")
    return None


def resolve_all(slug: str, force: bool = False) -> tuple[list[dict], str]:
    build = config.build_dir(slug)
    meta = json.loads((build / "narration_meta.json").read_text(encoding="utf-8"))["beats"]
    visuals_dir = build / "visuals"
    visuals_dir.mkdir(exist_ok=True)
    visuals_gemini_dir = build / config.GEMINI_VISUALS_DIRNAME
    visuals_gemini_dir.mkdir(exist_ok=True)
    evidence_dir = build / config.EVIDENCE_DIRNAME
    evidence_dir.mkdir(exist_ok=True)
    manifest_path = build / "manifest.json"

    cached = {}
    if manifest_path.exists() and not force:
        for entry in json.loads(manifest_path.read_text(encoding="utf-8")):
            if Path(entry["path"]).exists():
                if "evidence" in entry and not Path(entry["evidence"]["path"]).exists():
                    del entry["evidence"]  # stale - drop so it's retried below, not left dangling
                cached[entry["id"]] = entry

    manifest = []
    last_resolved = None
    for beat in meta:
        for seg_i, seg in enumerate(beat["segments"]):
            seg_id = f"{beat['id']}_seg{seg_i:02d}"
            entry = cached.get(seg_id)
            if entry is None:
                entry = _resolve_primary(seg.get("on_screen"), seg_id, visuals_gemini_dir, visuals_dir)
                if entry is None:
                    if last_resolved is None:
                        raise RuntimeError(
                            f"{seg_id} has no ON SCREEN cue and there's no earlier segment to fall back to"
                        )
                    # Fallback only ever carries the PRIMARY visual forward - never a
                    # neighbor's evidence. Stripping it here (rather than letting it
                    # ride along) forces this segment's own evidence cue, if any, to
                    # be resolved independently below instead of silently inheriting
                    # proof that belongs to a different claim.
                    entry = {k: v for k, v in last_resolved.items() if k != "evidence"}
                    entry.update(id=seg_id, fallback_from=last_resolved["id"])
            if "evidence" not in entry:
                # Only resolve when this segment doesn't already have a valid cached
                # evidence entry of its OWN (checked just above the loop) - same
                # skip-if-already-resolved discipline every other stage in this
                # pipeline already follows, so a plain re-run doesn't re-hit
                # Wikimedia/Pixabay for evidence that was already found last time.
                evidence_entry = _resolve_evidence(seg.get("evidence"), seg_id, evidence_dir)
                if evidence_entry:
                    entry["evidence"] = evidence_entry
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
        ev = entry.get("evidence")
        ev_note = f" | evidence: [{ev['source']}] {ev.get('title', '')[:40]}" if ev else ""
        print(f"  {entry['id']}: [{entry['source']}] {entry.get('title', '')[:60]}{note}{ev_note}")
