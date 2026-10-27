"""
Builds music_catalog.csv, sfx_catalog.csv, and asset_manifest.json from
registry.py's creative-intent metadata plus the measured technical stats
collected by generate.py (duration, peak, loudness, etc. - measured from
the actual rendered signal, not assumed).

Stats persist in metadata/_generation_stats.json between runs so that
regenerating a single category/asset (generate.py --category X) doesn't
wipe out catalog rows for everything else.
"""

import csv
import json
from pathlib import Path

import registry

ROOT = Path(__file__).parent.parent
# metadata/ (along with music/ and sfx/) lives outside assets/audio/ now,
# at C:\YouTube\Assets_audio\ (moved 2026-10-25 on request).
DATA_ROOT = ROOT.parent.parent / "Assets_audio"
METADATA = DATA_ROOT / "metadata"
STATS_FILE = METADATA / "_generation_stats.json"

SEED_NOTE = "deterministic (multiple fixed internal seeds - see generator source; re-running reproduces byte-identical output)"


def load_stats():
    if STATS_FILE.exists():
        with open(STATS_FILE, "r") as f:
            return json.load(f)
    return {}


def save_stats(stats):
    METADATA.mkdir(parents=True, exist_ok=True)
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f, indent=2)


def update_stats(results):
    """Merge a list of generate.py result dicts into the persisted stats
    store, keyed by asset id, and save."""
    stats = load_stats()
    for r in results:
        stats[r["id"]] = r
    save_stats(stats)
    return stats


def _row(asset, stats):
    s = stats.get(asset["id"], {})
    status = s.get("status", "not yet generated")
    return s, status


def write_catalogs():
    stats = load_stats()
    METADATA.mkdir(parents=True, exist_ok=True)

    music_fields = ["asset_id", "filename", "category", "genre", "mood", "narrative_purpose",
                     "intended_video_subject", "duration_sec", "bpm", "tonal_center",
                     "loop_compatible", "voiceover_suitability", "sample_rate", "bit_depth",
                     "channels", "peak_dbfs", "integrated_loudness_lufs", "random_seed", "generation_status"]
    with open(METADATA / "music_catalog.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=music_fields)
        w.writeheader()
        for asset in registry.MUSIC:
            s, status = _row(asset, stats)
            w.writerow({
                "asset_id": asset["id"], "filename": asset["filename"], "category": asset["category"],
                "genre": asset["category"].replace("_", " ").title(), "mood": asset["mood"],
                "narrative_purpose": asset["purpose"], "intended_video_subject": asset["intended_subject"],
                "duration_sec": s.get("duration_sec", asset["nominal_duration_sec"]), "bpm": asset["bpm"],
                "tonal_center": asset["tonal_center"], "loop_compatible": asset["loop_compatible"],
                "voiceover_suitability": asset["voiceover_suitability"], "sample_rate": s.get("sample_rate", ""),
                "bit_depth": s.get("bit_depth", ""), "channels": s.get("channels", ""),
                "peak_dbfs": s.get("peak_dbfs", ""), "integrated_loudness_lufs": s.get("integrated_loudness_lufs", ""),
                "random_seed": SEED_NOTE, "generation_status": status,
            })

    sfx_fields = ["asset_id", "filename", "category", "effect_type", "narrative_purpose", "intended_use",
                   "duration_sec", "channels", "sample_rate", "bit_depth", "peak_dbfs",
                   "integrated_loudness_lufs", "random_seed", "generation_status"]
    with open(METADATA / "sfx_catalog.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=sfx_fields)
        w.writeheader()
        for asset in registry.SFX:
            s, status = _row(asset, stats)
            w.writerow({
                "asset_id": asset["id"], "filename": asset["filename"], "category": asset["category"],
                "effect_type": asset["effect_type"], "narrative_purpose": asset["narrative_purpose"],
                "intended_use": asset["intended_use"], "duration_sec": s.get("duration_sec", asset["nominal_duration_sec"]),
                "channels": s.get("channels", ""), "sample_rate": s.get("sample_rate", ""),
                "bit_depth": s.get("bit_depth", ""), "peak_dbfs": s.get("peak_dbfs", ""),
                "integrated_loudness_lufs": s.get("integrated_loudness_lufs", ""),
                "random_seed": SEED_NOTE, "generation_status": status,
            })

    manifest = {"music": [], "sfx": []}
    for asset in registry.MUSIC:
        s, status = _row(asset, stats)
        manifest["music"].append({**{k: v for k, v in asset.items() if k != "generator"}, "measured": s,
                                    "generation_status": status})
    for asset in registry.SFX:
        s, status = _row(asset, stats)
        manifest["sfx"].append({**{k: v for k, v in asset.items() if k != "generator"}, "measured": s,
                                  "generation_status": status})
    with open(METADATA / "asset_manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"Wrote catalogs: {len(registry.MUSIC)} music rows, {len(registry.SFX)} sfx rows.")


if __name__ == "__main__":
    write_catalogs()
