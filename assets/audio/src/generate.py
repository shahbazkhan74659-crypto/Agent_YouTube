"""
Orchestrator / entry point for the library. Iterates registry.ALL_ASSETS,
renders each via its generator function, writes 48kHz/24-bit WAV, measures
real technical stats from the rendered signal, and updates the metadata
catalogs.

Usage:
    python generate.py                      # everything (100 assets)
    python generate.py --category science    # just one category
    python generate.py --id MUS_SC01         # just one asset

Deliberately a plain sys.argv filter, not a full argparse CLI - the asset
set and all per-asset metadata live in registry.py, not in config files, so
regenerating a subset after tweaking one generator function is cheap without
needing a heavier CLI surface.
"""

import sys
from pathlib import Path

import numpy as np

import audio_lib as A
import registry
import metadata_gen

ROOT = Path(__file__).parent.parent
# music/, sfx/, and metadata/ live outside assets/audio/ now, at
# C:\YouTube\Assets_audio\ (moved 2026-10-25 on request - separates the
# actual deliverable assets from this dev/source-code tree, which keeps
# src/ and reports/ where they were).
DATA_ROOT = ROOT.parent.parent / "Assets_audio"


def parse_filter(argv):
    category = None
    asset_id = None
    for i, a in enumerate(argv):
        if a == "--category" and i + 1 < len(argv):
            category = argv[i + 1]
        if a == "--id" and i + 1 < len(argv):
            asset_id = argv[i + 1]
    return category, asset_id


def select_assets(category=None, asset_id=None):
    assets = registry.ALL_ASSETS
    if asset_id:
        assets = [a for a in assets if a["id"] == asset_id]
    if category:
        assets = [a for a in assets if a["category"] == category]
    return assets


def generate_one(asset):
    try:
        sig = asset["generator"]()
    except Exception as e:
        return {"id": asset["id"], "status": "failed", "error": f"{type(e).__name__}: {e}"}

    if not np.all(np.isfinite(sig)):
        return {"id": asset["id"], "status": "failed", "error": "non-finite samples (NaN/Inf) before encoding"}

    out_path = DATA_ROOT / asset["rel_dir"] / asset["filename"]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    A.write_wav24(out_path, sig)

    peak = float(np.max(np.abs(sig)))
    peak_db = 20 * np.log10(peak + 1e-12)
    true_peak_db = 20 * np.log10(A.true_peak_estimate(sig) + 1e-12)
    loudness = A.measure_loudness(sig)
    duration = len(sig) / A.SR
    channels = sig.shape[1] if sig.ndim == 2 else 1

    return {
        "id": asset["id"], "status": "generated", "path": str(out_path),
        "duration_sec": round(duration, 3), "sample_rate": A.SR, "channels": channels,
        "bit_depth": 24, "peak_dbfs": round(peak_db, 2), "estimated_true_peak_dbfs": round(true_peak_db, 2),
        "integrated_loudness_lufs": round(loudness, 2) if loudness is not None else None,
    }


def main():
    category, asset_id = parse_filter(sys.argv[1:])
    assets = select_assets(category, asset_id)
    if not assets:
        print(f"No assets matched category={category!r} id={asset_id!r}")
        return 1

    results = []
    for asset in assets:
        res = generate_one(asset)
        results.append(res)
        tag = res["status"].upper()
        detail = res.get("error", "") if res["status"] == "failed" else f"{res['duration_sec']}s"
        print(f"[{tag}] {asset['id']:10s} {asset['filename']:55s} {detail}")

    metadata_gen.update_stats(results)
    metadata_gen.write_catalogs()

    n_ok = sum(1 for r in results if r["status"] == "generated")
    n_total = len(results)
    print(f"\nGenerated {n_ok}/{n_total} assets.")
    if n_ok < n_total:
        print("FAILURES:")
        for r in results:
            if r["status"] == "failed":
                print(f"  {r['id']}: {r['error']}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
