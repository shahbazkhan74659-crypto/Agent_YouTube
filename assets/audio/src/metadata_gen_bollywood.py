"""
Builds music_catalog_bollywood.csv from registry_bollywood.py's creative-intent
metadata plus the measured technical stats collected by generate_bollywood.py
(duration, peak, loudness, etc. - measured from the actual rendered signal, not
assumed). Mirrors metadata_gen.py's pattern; kept as a separate module/stats
file so regenerating the genre library never touches this catalog or vice versa.
"""

import json
from pathlib import Path
import csv

import registry_bollywood as registry

ROOT = Path(__file__).parent.parent
DATA_ROOT = ROOT.parent.parent / "Assets_audio"
METADATA = DATA_ROOT / "metadata"
STATS_FILE = METADATA / "_generation_stats_bollywood.json"

SEED_NOTE = "deterministic (multiple fixed internal seeds - see generator source; re-running reproduces byte-identical output)"

FIELDS = [
    "asset_id", "filename", "emotion", "title", "mood_descriptors", "narrative_purpose",
    "instrumentation", "tonal_center", "bpm", "duration_sec", "loop_compatible",
    "voiceover_suitability", "sample_rate", "bit_depth", "channels", "peak_dbfs",
    "integrated_loudness_lufs", "random_seed", "generation_status", "composition_notes",
]


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
    stats = load_stats()
    for r in results:
        stats[r["id"]] = r
    save_stats(stats)
    return stats


def write_catalogs():
    stats = load_stats()
    METADATA.mkdir(parents=True, exist_ok=True)

    with open(METADATA / "music_catalog_bollywood.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for asset in registry.MUSIC:
            s = stats.get(asset["id"], {})
            status = s.get("status", "not yet generated")
            w.writerow({
                "asset_id": asset["id"], "filename": asset["filename"], "emotion": asset["emotion"],
                "title": asset["title"], "mood_descriptors": asset["mood"],
                "narrative_purpose": asset["purpose"], "instrumentation": asset["instrumentation"],
                "tonal_center": asset["tonal_center"], "bpm": asset["bpm"],
                "duration_sec": s.get("duration_sec", asset["nominal_duration_sec"]),
                "loop_compatible": asset["loop_compatible"],
                "voiceover_suitability": asset["voiceover_suitability"],
                "sample_rate": s.get("sample_rate", ""), "bit_depth": s.get("bit_depth", ""),
                "channels": s.get("channels", ""), "peak_dbfs": s.get("peak_dbfs", ""),
                "integrated_loudness_lufs": s.get("integrated_loudness_lufs", ""),
                "random_seed": SEED_NOTE, "generation_status": status,
                "composition_notes": asset.get("notes", ""),
            })

    print(f"Wrote music_catalog_bollywood.csv: {len(registry.MUSIC)} rows.")


if __name__ == "__main__":
    write_catalogs()
