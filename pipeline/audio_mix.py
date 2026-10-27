"""Concatenates per-beat narration into one track, builds the music bed from
Assets_audio/music_bollywood by the active emotion at each beat (from a script's
[MUSIC: ...] cues - see script_parser.py), crossfading between beds wherever the
emotion changes partway through the video, and drops in SOLID/CONTESTED-CONFIDENCE
claim-reveal SFX accents at the beats where a confidence tag appears - the exact
assets README names for that role, still read from the old genre-based SFX catalog
(Assets_audio/sfx/ + sfx_catalog.csv), which is unaffected by the 2026-10-26 switch
to the Bollywood-referenced emotion music library. Mixed with ffmpeg (one
filter_complex graph: concat narration -> build+crossfade music parts -> delay each
sfx to its beat's start -> amix -> alimiter safety peak clamp, which is exactly the
"no limiter stage, re-check combined peak" gap the audio library's README flags for
this kind of multi-asset stacking).
"""

import argparse
import csv
import json

import config
import ffmpeg_tool


def _db_to_linear(db: float) -> float:
    return 10 ** (db / 20)


def _load_catalog(path) -> list[dict]:
    if not path.exists():
        return []
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def pick_music_bed(category: str, mood: str | None = None) -> dict:
    """Legacy genre-based picker (Assets_audio/music/ + music_catalog.csv). Kept for
    reference/rollback - no longer called by build_mix as of the 2026-10-26 switch
    to the Bollywood-referenced emotion library (pick_emotion_bed, below)."""
    rows = _load_catalog(config.MUSIC_CATALOG)
    candidates = [r for r in rows if r["category"] == category]
    if not candidates:
        raise ValueError(f"No music bed found for category={category!r}")
    if mood:
        filtered = [r for r in candidates if mood.lower() in r["mood"].lower()]
        if filtered:
            candidates = filtered
    row = candidates[0]
    return {**row, "path": str(config.ASSETS_AUDIO_DIR / "music" / row["category"] / row["filename"])}


def pick_emotion_bed(emotion: str) -> dict:
    """Picks a track from the Bollywood-referenced emotion library
    (Assets_audio/music_bollywood/<emotion>/ + music_catalog_bollywood.csv)."""
    rows = _load_catalog(config.MUSIC_CATALOG_BOLLYWOOD)
    candidates = [r for r in rows if r["emotion"] == emotion]
    if not candidates:
        raise ValueError(
            f"No Bollywood-referenced music bed found for emotion={emotion!r}. "
            f"The library has no tracks yet for this emotion - render one into "
            f"{config.MUSIC_BOLLYWOOD_DIR / emotion} and register it in "
            f"{config.MUSIC_CATALOG_BOLLYWOOD}."
        )
    row = candidates[0]
    return {**row, "path": str(config.MUSIC_BOLLYWOOD_DIR / row["emotion"] / row["filename"])}


def find_sfx(name_candidates: tuple[str, ...]) -> dict | None:
    rows = _load_catalog(config.SFX_CATALOG)
    by_stem = {r["filename"].rsplit(".", 1)[0]: r for r in rows}
    for name in name_candidates:
        row = by_stem.get(name)
        if row:
            return {**row, "path": str(config.ASSETS_AUDIO_DIR / "sfx" / row["category"] / row["filename"])}
    return None


def _sfx_cue_points(meta: list[dict]) -> list[tuple[float, dict]]:
    """One SFX placement per beat whose confidence_tags include SOLID or
    CONTESTED/UNCERTAIN, at that beat's start time."""
    solid_sfx = find_sfx(config.SOLID_SFX_CANDIDATES)
    uncertain_sfx = find_sfx(config.UNCERTAIN_SFX_CANDIDATES)
    cues = []
    for beat in meta:
        tags = set(beat.get("confidence_tags", []))
        if "SOLID" in tags and solid_sfx:
            cues.append((beat["start"], solid_sfx))
        elif tags & {"CONTESTED", "UNCERTAIN"} and uncertain_sfx:
            cues.append((beat["start"], uncertain_sfx))
    return cues


def music_parts(meta: list[dict], default_emotion: str | None) -> list[dict]:
    """Groups consecutive beats sharing the same active emotion into contiguous
    {start, end, emotion} parts - the mix only switches/crossfades bed at a part
    boundary, not every beat, since a [MUSIC: ...] cue usually spans several beats
    (e.g. the whole Explanation section). Raises if a beat has no emotion and no
    --default-emotion fallback was given - every beat needs one before mixing."""
    parts: list[dict] = []
    for beat in meta:
        emotion = beat.get("emotion") or default_emotion
        if emotion is None:
            raise ValueError(
                f"{beat['id']} has no [MUSIC: ...] cue in scope and no --default-emotion "
                f"was given - every beat needs an active emotion before mixing."
            )
        if emotion not in config.EMOTION_CATEGORIES:
            raise ValueError(
                f"{beat['id']}: unknown emotion {emotion!r} - must be one of "
                f"{', '.join(config.EMOTION_CATEGORIES)}"
            )
        if parts and parts[-1]["emotion"] == emotion:
            parts[-1]["end"] = beat["end"]
        else:
            parts.append({"start": beat["start"], "end": beat["end"], "emotion": emotion})
    return parts


def _music_filter_graph(parts: list[dict], input_idx: int, xfade: float) -> tuple[list[str], list[str], int]:
    """Builds the ffmpeg inputs + filter_complex lines for a (possibly multi-part,
    possibly multi-emotion) music bed and returns (inputs, filter_parts, next_input_idx).
    The final combined stream is left on the label '[music_raw]' (gain is applied by
    the caller, same as before, so there's exactly one volume filter regardless of
    how many parts were crossfaded).

    Crossfade length bookkeeping: every part except the last is trimmed to its own
    span *plus* one xfade's worth of extra looped material; the last part is trimmed
    to exactly its own span. Each acrossfade in the cascade consumes exactly one
    xfade of that overhang, so after all N-1 crossfades the combined stream's total
    length equals the sum of the parts' own spans - not sum(spans) - (N-1)*xfade,
    which is what a naive trim-then-crossfade chain would otherwise lose."""
    inputs: list[str] = []
    filter_parts: list[str] = []
    part_labels: list[str] = []

    single = len(parts) == 1
    for k, part in enumerate(parts):
        bed = pick_emotion_bed(part["emotion"])
        span = part["end"] - part["start"]
        is_last = k == len(parts) - 1
        trim = span if is_last else span + xfade
        inputs += ["-stream_loop", "-1", "-i", bed["path"]]
        label = "[music_raw]" if single else f"[pm{k}]"
        filter_parts.append(f"[{input_idx}:a]atrim=0:{trim}{label}")
        part_labels.append(label)
        input_idx += 1

    if single:
        return inputs, filter_parts, input_idx

    acc = part_labels[0]
    for k in range(1, len(parts)):
        out_label = "[music_raw]" if k == len(parts) - 1 else f"[mx{k}]"
        filter_parts.append(f"{acc}{part_labels[k]}acrossfade=d={xfade}:c1=tri:c2=tri{out_label}")
        acc = out_label
    return inputs, filter_parts, input_idx


def build_mix(slug: str, default_emotion: str | None = None, force: bool = False, no_music: bool = False) -> str:
    build = config.build_dir(slug)
    meta = json.loads((build / "narration_meta.json").read_text(encoding="utf-8"))["beats"]
    out_path = build / "mix.wav"
    if out_path.exists() and not force:
        return str(out_path)

    total_duration = meta[-1]["end"]
    cues = _sfx_cue_points(meta)

    inputs: list[str] = []
    input_idx = 0
    for beat in meta:
        inputs += ["-i", beat["wav_path"]]
        input_idx += 1
    n_beats = len(meta)

    filter_parts = []
    labels = []
    for i in range(n_beats):
        filter_parts.append(f"[{i}:a]apad=pad_dur={config.BEAT_GAP_SEC}[b{i}]")
        labels.append(f"[b{i}]")
    filter_parts.append(f"{''.join(labels)}concat=n={n_beats}:v=0:a=1[narr]")

    mix_labels = ["[narr]"]
    # --no-music: skip the Bollywood-emotion music bed entirely (useful while that
    # library has no tracks composed yet for any emotion - music_parts()/
    # pick_emotion_bed() would otherwise raise). default_emotion is unused here.
    if not no_music:
        parts = music_parts(meta, default_emotion)
        music_inputs, music_filter_parts, input_idx = _music_filter_graph(
            parts, input_idx, config.MUSIC_CROSSFADE_SEC
        )
        inputs += music_inputs
        filter_parts += music_filter_parts
        music_gain = _db_to_linear(config.MUSIC_BED_GAIN_DB)
        filter_parts.append(f"[music_raw]atrim=0:{total_duration},volume={music_gain}[music]")
        mix_labels.append("[music]")

    sfx_indices = []
    for _, sfx in cues:
        sfx_indices.append(input_idx)
        inputs += ["-i", sfx["path"]]
        input_idx += 1

    sfx_gain = _db_to_linear(config.SFX_GAIN_DB)
    for sfx_i, (start_time, _sfx) in zip(sfx_indices, cues):
        delay_ms = max(0, round(start_time * 1000))
        label = f"[sfx{sfx_i}]"
        filter_parts.append(f"[{sfx_i}:a]adelay={delay_ms}:all=1,volume={sfx_gain}{label}")
        mix_labels.append(label)

    filter_parts.append(
        f"{''.join(mix_labels)}amix=inputs={len(mix_labels)}:duration=first:dropout_transition=0:normalize=0[mixed]"
    )
    filter_parts.append("[mixed]alimiter=limit=0.95[out]")

    ffmpeg_tool.run(inputs + ["-filter_complex", ";".join(filter_parts), "-map", "[out]", str(out_path)])
    return str(out_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("slug")
    parser.add_argument(
        "--default-emotion", default=None,
        help="Fallback emotion for any beat with no [MUSIC: ...] cue in scope, e.g. mysterious",
    )
    parser.add_argument("--no-music", action="store_true", help="Skip the music bed entirely (narration + SFX only)")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    out_path = build_mix(args.slug, default_emotion=args.default_emotion, force=args.force, no_music=args.no_music)
    duration = ffmpeg_tool.probe_duration(out_path)
    print(f"Mixed -> {out_path} ({duration:.1f}s)")
