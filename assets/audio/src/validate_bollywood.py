"""
Technical validation suite for the Bollywood-referenced emotion music library -
mirrors validate.py's checks (existence, decode, format, silence, clipping,
NaN/Inf, duplicate filenames, exact/near-duplicate audio) against
registry_bollywood.ALL_ASSETS instead of the genre library's registry.py, so
running this never touches or depends on the genre library's reports.

Writes reports/validation_report_bollywood.txt and
reports/generation_report_bollywood.txt.

Usage: python validate_bollywood.py
"""

import hashlib
from pathlib import Path

import numpy as np
import soundfile as sf

import registry_bollywood as registry

ROOT = Path(__file__).parent.parent
REPORTS = ROOT / "reports"
DATA_ROOT = ROOT.parent.parent / "Assets_audio" / "music_bollywood"

SILENCE_THRESHOLD_DBFS = -55.0
CLIP_SAMPLE_COUNT_THRESHOLD = 8
NEAR_DUP_SIMILARITY_THRESHOLD = 0.985


def spectral_fingerprint(sig, sr, n_bins=32):
    mono = sig.mean(axis=1) if sig.ndim == 2 else sig
    spec = np.abs(np.fft.rfft(mono))
    freqs = np.fft.rfftfreq(len(mono), d=1.0 / sr)
    edges = np.geomspace(20, sr / 2, n_bins + 1)
    fp = np.zeros(n_bins)
    for i in range(n_bins):
        mask = (freqs >= edges[i]) & (freqs < edges[i + 1])
        fp[i] = spec[mask].mean() if mask.any() else 0.0
    norm = np.linalg.norm(fp) + 1e-12
    return fp / norm


def cosine_sim(a, b):
    return float(np.dot(a, b) / ((np.linalg.norm(a) + 1e-12) * (np.linalg.norm(b) + 1e-12)))


def validate_asset(asset):
    path = DATA_ROOT / asset["rel_dir"] / asset["filename"]
    findings = []
    info = {"id": asset["id"], "path": str(path), "ok": False}

    if not path.exists():
        findings.append("FILE MISSING")
        info["findings"] = findings
        return info, None

    try:
        sig, sr = sf.read(str(path), always_2d=True)
    except Exception as e:
        findings.append(f"FAILED TO DECODE: {e}")
        info["findings"] = findings
        return info, None

    sfinfo = sf.info(str(path))
    duration = len(sig) / sr
    channels = sig.shape[1]

    if sr != 48000:
        findings.append(f"sample rate {sr} != expected 48000")
    if channels != 2:
        findings.append(f"channel count {channels} != expected 2 (stereo)")
    if sfinfo.subtype != "PCM_24":
        findings.append(f"bit depth subtype {sfinfo.subtype} != expected PCM_24")

    nominal = asset["nominal_duration_sec"]
    if nominal and abs(duration - nominal) > 0.5:
        findings.append(f"duration {duration:.2f}s differs from nominal {nominal}s by >0.5s")

    if not np.all(np.isfinite(sig)):
        findings.append("NON-FINITE SAMPLES (NaN/Inf)")

    peak = float(np.max(np.abs(sig))) if sig.size else 0.0
    peak_db = 20 * np.log10(peak + 1e-12)
    if peak_db < SILENCE_THRESHOLD_DBFS:
        findings.append(f"effectively silent (peak {peak_db:.1f} dBFS)")

    clip_count = int(np.sum(np.abs(sig) >= 0.9999))
    if clip_count >= CLIP_SAMPLE_COUNT_THRESHOLD:
        findings.append(f"possible clipping ({clip_count} samples at/near full scale)")

    info.update({
        "ok": len(findings) == 0, "findings": findings, "duration_sec": round(duration, 3),
        "sample_rate": sr, "channels": channels, "peak_dbfs": round(peak_db, 2),
        "bytes": path.stat().st_size,
    })
    fp = spectral_fingerprint(sig, sr)
    return info, (sig, fp)


def main():
    REPORTS.mkdir(parents=True, exist_ok=True)
    all_results = []
    fingerprints = {}
    hashes = {}
    filenames_seen = {}

    for asset in registry.ALL_ASSETS:
        info, extra = validate_asset(asset)
        all_results.append(info)

        fname = asset["filename"]
        filenames_seen.setdefault(fname, []).append(asset["id"])

        if extra is not None:
            sig, fp = extra
            fingerprints[asset["id"]] = fp
            h = hashlib.sha256(sig.tobytes()).hexdigest()
            hashes.setdefault(h, []).append(asset["id"])

    duplicate_filenames = {k: v for k, v in filenames_seen.items() if len(v) > 1}
    exact_duplicates = {k: v for k, v in hashes.items() if len(v) > 1}

    near_duplicates = []
    ids = list(fingerprints.keys())
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            sim = cosine_sim(fingerprints[ids[i]], fingerprints[ids[j]])
            if sim >= NEAR_DUP_SIMILARITY_THRESHOLD:
                near_duplicates.append((ids[i], ids[j], round(sim, 4)))

    n_music = len(registry.MUSIC)
    valid_music = sum(1 for r in all_results if r["ok"])
    total_duration = sum(r.get("duration_sec", 0.0) for r in all_results if r["ok"])
    total_bytes = sum(r.get("bytes", 0) for r in all_results if r["ok"])
    failed = [r for r in all_results if not r["ok"]]
    review = [r for r in all_results if r["ok"] and any("possible clipping" in f for f in r["findings"])]

    with open(REPORTS / "validation_report_bollywood.txt", "w") as f:
        f.write("BOLLYWOOD-REFERENCED MUSIC LIBRARY VALIDATION REPORT\n" + "=" * 54 + "\n\n")
        for r in all_results:
            status = "OK" if r["ok"] else "ISSUES"
            f.write(f"{r['id']:14s} [{status}]\n")
            for finding in r["findings"]:
                f.write(f"    - {finding}\n")
        f.write("\nDUPLICATE FILENAMES\n" + "-" * 20 + "\n")
        f.write("none\n" if not duplicate_filenames else "".join(f"  {k}: {v}\n" for k, v in duplicate_filenames.items()))
        f.write("\nEXACT-DUPLICATE AUDIO (identical hash)\n" + "-" * 20 + "\n")
        f.write("none\n" if not exact_duplicates else "".join(f"  {v}\n" for v in exact_duplicates.values()))
        f.write(f"\nNEAR-DUPLICATE AUDIO (spectral similarity >= {NEAR_DUP_SIMILARITY_THRESHOLD}, flagged for review, not rejected)\n" + "-" * 20 + "\n")
        f.write("none\n" if not near_duplicates else "".join(f"  {a} <-> {b}: {s}\n" for a, b, s in near_duplicates))

    with open(REPORTS / "generation_report_bollywood.txt", "w") as f:
        f.write("BOLLYWOOD-REFERENCED MUSIC LIBRARY GENERATION REPORT\n" + "=" * 54 + "\n\n")
        f.write(f"Tracks generated: {n_music}, valid: {valid_music}\n")
        f.write(f"Total audio duration (valid assets): {total_duration:.1f}s ({total_duration / 60:.1f} min)\n")
        f.write(f"Total disk usage (valid assets): {total_bytes / (1024 * 1024):.1f} MB\n")
        f.write(f"Failed assets: {len(failed)}\n")
        for r in failed:
            f.write(f"  {r['id']}: {r['findings']}\n")
        f.write(f"Assets flagged for review (non-fatal): {len(review)}\n")
        for r in review:
            f.write(f"  {r['id']}: {r['findings']}\n")
        f.write("\nKNOWN LIMITATIONS\n" + "-" * 20 + "\n")
        f.write(
            "- Not yet human-verified by ear - numeric validation only.\n"
            "- 'Measured loudness' is pyloudnorm's ITU-R BS.1770 integrated loudness where the\n"
            "  package is installed; true peak is a 4x-oversampling estimate, not a certified\n"
            "  BS.1770-4 true-peak meter.\n"
            "- Near-duplicate detection is a cheap 32-band spectral fingerprint, not a\n"
            "  perceptual audio-matching algorithm.\n"
            "- No limiter/compressor stage on an individual track - if an edit stacks\n"
            "  multiple beds/SFX together, re-check the combined peak before export.\n"
        )

    print(f"Validated {len(all_results)} assets: {sum(1 for r in all_results if r['ok'])} OK, "
          f"{len(failed)} failed, {len(review)} flagged for review.")
    print(f"Reports written to {REPORTS}")
    return 1 if failed else 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
