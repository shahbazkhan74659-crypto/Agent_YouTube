"""
Orchestrator / entry point for the Bollywood-referenced emotion music library.
Mirrors generate.py's pattern exactly (same resumable-by-asset approach),
pointed at registry_bollywood.py and Assets_audio/music_bollywood/ instead of
the genre library's registry.py and Assets_audio/music/.

Usage:
    python generate_bollywood.py                     # everything in registry_bollywood.MUSIC
    python generate_bollywood.py --emotion motivational
    python generate_bollywood.py --id BOL_MOT01

Currently a no-op either way - registry_bollywood.MUSIC is empty until real
tracks are composed (see that file's comment and
Assets_audio/music_bollywood/README.md).
"""

import sys
from pathlib import Path

import numpy as np

import audio_lib as A
import registry_bollywood as registry
import metadata_gen_bollywood as metadata_gen

ROOT = Path(__file__).parent.parent
DATA_ROOT = ROOT.parent.parent / "Assets_audio" / "music_bollywood"


def parse_filter(argv):
    emotion = None
    asset_id = None
    for i, a in enumerate(argv):
        if a == "--emotion" and i + 1 < len(argv):
            emotion = argv[i + 1]
        if a == "--id" and i + 1 < len(argv):
            asset_id = argv[i + 1]
    return emotion, asset_id


def select_assets(emotion=None, asset_id=None):
    assets = registry.ALL_ASSETS
    if asset_id:
        assets = [a for a in assets if a["id"] == asset_id]
    if emotion:
        assets = [a for a in assets if a["emotion"] == emotion]
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
    emotion, asset_id = parse_filter(sys.argv[1:])
    assets = select_assets(emotion, asset_id)
    if not assets:
        print(f"No assets matched emotion={emotion!r} id={asset_id!r} "
              f"(registry_bollywood.MUSIC has {len(registry.MUSIC)} entries)")
        return 1

    results = []
    for asset in assets:
        res = generate_one(asset)
        results.append(res)
        tag = res["status"].upper()
        detail = res.get("error", "") if res["status"] == "failed" else f"{res['duration_sec']}s"
        print(f"[{tag}] {asset['id']:12s} {asset['filename']:60s} {detail}")

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
