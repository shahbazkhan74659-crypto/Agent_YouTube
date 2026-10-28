"""Per-segment clip from its resolved visual, padded onto the full black
1080x1920 canvas at the content square's fixed position, with the host character
composited on top (character.py picks pose/position) - all three in one ffmpeg
pass per segment, since each segment's clip is short and simple. The clips are
then concatenated (stream-copy, cheap) and a final pass burns captions.ass
(including the static title band) and muxes mix.wav -> output/final.mp4.

Still images hold fixed - fully visible (no crop) and centered within the
content rectangle - by default as of 2026-10-28 (config.ENABLE_KEN_BURNS=False).
The Ken Burns pan/zoom code path (motion_for_segment/_motion_exprs/MOTIONS)
still exists and works if that flag is flipped back on.

One clip per visual *segment* (script_parser.py splits a beat at every inline
cue; narration.py times each segment proportionally by word count), not one per
beat - that's the actual fix for images holding static for a whole beat.

**Why per-segment, not one pass over the whole video**: an earlier version padded
+ character-overlaid the *entire* concatenated video in two separate passes, the
second chaining one timed `overlay=...:enable='between(t,...)'` per segment (20
for the test video) onto a single stream. Live-tested and killed after it balloted
to 140MB+ and climbing after 15+ minutes (for content that should encode to
~20MB) - the character popping in/out at each segment's timed window reads to
x264 as a scene change, forcing a keyframe each time, and the frame was flowing
through all 20 chained overlay instances regardless of which one was actually
active. Compositing per short segment instead avoids both problems entirely:
each small clip encodes independently and normally, and concatenation is a cheap
stream copy, not a re-encode.
"""

import argparse
import json
import random
from pathlib import Path

import character
import config
import evidence
import ffmpeg_tool

TARGET_ZOOM = 1.12  # zoom_in/zoom_out motions - subtle, centered
PAN_ZOOM = 1.2  # fixed zoom level for the pan/diagonal motions - leaves room to
# traverse the frame without ever exposing padding at the edges

VIDEO_EXTS = {".mp4", ".mov", ".webm", ".mkv"}

# Every still image gets one of these Ken Burns motions, picked per-segment (see
# motion_for_segment below) instead of the old fixed "always centered zoom-in."
MOTIONS = (
    "zoom_in", "zoom_out",
    "pan_left_to_right", "pan_right_to_left",
    "pan_top_to_bottom", "pan_bottom_to_top",
    "pan_tl_to_br", "pan_br_to_tl", "pan_tr_to_bl", "pan_bl_to_tr",
)


def motion_for_segment(seg_id: str) -> str:
    """Deterministic per-segment random pick (seeded by the segment's own id, not
    a shared RNG stream) - re-running the pipeline on an unchanged segment always
    assigns it the same motion, regardless of which other segments get rebuilt
    around it, since each clip's resumability check (build_video_track, below) is
    itself per-segment."""
    return random.Random(seg_id).choice(MOTIONS)


def _motion_exprs(motion: str, n_frames: int) -> tuple[str, str, str]:
    """Returns the zoompan (z, x, y) expressions for a named motion. zoom_in/
    zoom_out animate z (zoom level) with x/y re-centered every frame; every pan
    motion holds z fixed at PAN_ZOOM and animates x/y linearly across the frame's
    n_frames instead, in the direction the name describes."""
    if motion == "zoom_in":
        # zoompan's internal 'zoom' state does NOT reliably default to 1.0 on this
        # ffmpeg build - live-tested: without forcing on==0, 'zoom' is already >=
        # TARGET_ZOOM from frame 0, so min(zoom+step,TARGET_ZOOM) just clamps flat
        # at TARGET_ZOOM for the whole clip (measured: 30 differing bytes out of
        # 6.2M between the first and last frame - visually static, not zooming).
        # Forcing the start value explicitly, same defensive pattern zoom_out
        # already used, fixes it (measured: 2.14M/2.32M bytes differ after).
        step = (TARGET_ZOOM - 1.0) / n_frames
        return f"if(eq(on,0),1.0,min(zoom+{step:.8f},{TARGET_ZOOM}))", "(iw-iw/zoom)/2", "(ih-ih/zoom)/2"
    if motion == "zoom_out":
        step = (TARGET_ZOOM - 1.0) / n_frames
        return (
            f"if(eq(on,0),{TARGET_ZOOM},max(1.0,zoom-{step:.8f}))",
            "(iw-iw/zoom)/2", "(ih-ih/zoom)/2",
        )
    frac = f"(on/{max(n_frames - 1, 1)})"
    x_fwd, x_rev = f"(iw-iw/zoom)*{frac}", f"(iw-iw/zoom)*(1-{frac})"
    y_fwd, y_rev = f"(ih-ih/zoom)*{frac}", f"(ih-ih/zoom)*(1-{frac})"
    x_mid, y_mid = "(iw-iw/zoom)/2", "(ih-ih/zoom)/2"
    pans = {
        "pan_left_to_right": (x_fwd, y_mid),
        "pan_right_to_left": (x_rev, y_mid),
        "pan_top_to_bottom": (x_mid, y_fwd),
        "pan_bottom_to_top": (x_mid, y_rev),
        "pan_tl_to_br": (x_fwd, y_fwd),
        "pan_br_to_tl": (x_rev, y_rev),
        "pan_tr_to_bl": (x_rev, y_fwd),
        "pan_bl_to_tr": (x_fwd, y_rev),
    }
    x_expr, y_expr = pans[motion]
    return str(PAN_ZOOM), x_expr, y_expr


def _build_segment_clip(
    visual_path: str,
    duration: float,
    char_path: Path,
    char_x: int,
    motion: str,
    out_path: Path,
    evidence_path: Path | None = None,
    evidence_xy: tuple[int, int] | None = None,
    source: str | None = None,
) -> None:
    n_frames = max(1, round(duration * config.FPS))
    is_video = Path(visual_path).suffix.lower() in VIDEO_EXTS
    # Crops off the bottom strip (and Gemini's baked-in watermark with it) before
    # any scaling/fitting happens - see config.GEMINI_WATERMARK_CROP_FRAC. Only for
    # gemini-sourced stills, and only when config.ENABLE_GEMINI_WATERMARK_CROP is
    # on (disabled 2026-10-28 - watermark is shown now; see config.py's comment).
    wm_crop = (
        f"crop=iw:ih*{1 - config.GEMINI_WATERMARK_CROP_FRAC:.4f}:0:0,"
        if source == "gemini" and not is_video and config.ENABLE_GEMINI_WATERMARK_CROP
        else ""
    )

    if is_video:
        # Gemini/Veo-generated clip, not a still image - no Ken Burns zoom (it's
        # already moving footage). Scale-to-fill then center-crop to the square
        # (ffmpeg's crop centers by default when x/y are omitted) instead of
        # zoompan; -stream_loop/-t loop+trim it to the segment's exact duration
        # the same way -loop 1/-t does for a still image below. Only [out] (the
        # composited video stream) is ever mapped, so a Veo clip's own baked-in
        # audio track is implicitly dropped - no separate -an/mute step needed.
        visual_input = ["-stream_loop", "-1", "-t", f"{duration:.3f}", "-i", str(visual_path)]
        bg_chain = (
            f"[0:v]scale={config.SQUARE_WIDTH}:{config.SQUARE_HEIGHT}:force_original_aspect_ratio=increase,"
            f"crop={config.SQUARE_WIDTH}:{config.SQUARE_HEIGHT},"
            f"fps={config.FPS},"
            f"pad={config.WIDTH}:{config.HEIGHT}:{config.SQUARE_X}:{config.SQUARE_Y}:color=black,"
            "format=yuv420p[bg];"
        )
    else:
        # -r here sets the looped-image INPUT's framerate - without it ffmpeg
        # defaults a still image to 25fps, so asking for 30fps output frames
        # against a 25fps-timed -t window silently shortens every clip by 25/30
        # (live-tested: a 17.86s clip came out 14.90s before this fix).
        visual_input = ["-loop", "1", "-r", str(config.FPS), "-t", f"{duration:.3f}", "-i", str(visual_path)]
        if config.ENABLE_KEN_BURNS:
            z_expr, x_expr, y_expr = _motion_exprs(motion, n_frames)
            bg_chain = (
                f"[0:v]{wm_crop}scale=2000:-2,"  # oversample before zoompan - avoids zoompan's known jitter at low input res
                f"zoompan=z='{z_expr}':d=1:"
                f"x='{x_expr}':y='{y_expr}':"
                f"s={config.SQUARE_WIDTH}x{config.SQUARE_HEIGHT}:fps={config.FPS},"
                f"pad={config.WIDTH}:{config.HEIGHT}:{config.SQUARE_X}:{config.SQUARE_Y}:color=black,"
                "format=yuv420p[bg];"
            )
        else:
            # Fixed, no motion - 2026-10-28 default. "force_original_aspect_ratio=
            # decrease" scales to fit *within* the content rectangle without
            # cropping (unlike the video-clip branch above, which deliberately
            # fills+crops); the first pad letterboxes/pillarboxes the image to
            # exactly fill that rectangle so it's always fully visible and
            # centered, the second places that rectangle on the full canvas at
            # its fixed position - same two-stage pad already used elsewhere.
            # No separate fps= filter here - the looped input is already locked to
            # exactly config.FPS via -r above (live-tested: adding a redundant
            # downstream fps filter introduced a consistent ~1-frame rounding loss
            # per clip, 0.6s total over 18 segments, silently triggering assemble()'s
            # -shortest to trim the last ~0.6s of audio).
            bg_chain = (
                f"[0:v]{wm_crop}scale={config.SQUARE_WIDTH}:{config.SQUARE_HEIGHT}:force_original_aspect_ratio=decrease,"
                f"pad={config.SQUARE_WIDTH}:{config.SQUARE_HEIGHT}:(ow-iw)/2:(oh-ih)/2:color=black,"
                f"pad={config.WIDTH}:{config.HEIGHT}:{config.SQUARE_X}:{config.SQUARE_Y}:color=black,"
                "format=yuv420p[bg];"
            )

    # Two independent optional overlay layers (character, evidence inset) chained
    # onto the background - each appends its own filter stage and its own extra
    # input, advancing a running `label`/`next_idx` rather than special-casing every
    # on/off combination. No enable='between(t,...)' time-gating anywhere: each call
    # to this function is already scoped to exactly one segment's duration (that's
    # the whole reason this pipeline composites per-segment, not over the whole
    # video - see the module docstring), so a present layer is simply there for the
    # clip's entire length, same as the background always has been.
    parts = [bg_chain]
    label = "bg"
    next_idx = 1
    extra_inputs: list[str] = []

    if config.SHOW_CHARACTER:
        parts.append(f"[{next_idx}:v]scale=-2:{config.CHARACTER_HEIGHT}[char];")
        parts.append(f"[{label}][char]overlay=x={char_x}:y={config.CHARACTER_Y}[char_out];")
        extra_inputs += ["-loop", "1", "-i", str(char_path)]
        label, next_idx = "char_out", next_idx + 1

    if evidence_path is not None:
        ex, ey = evidence_xy
        inner = config.EVIDENCE_INSET_SIZE - 2 * config.EVIDENCE_BORDER_PX
        parts.append(
            f"[{next_idx}:v]scale={inner}:{inner}:force_original_aspect_ratio=increase,"
            f"crop={inner}:{inner},"
            f"pad={config.EVIDENCE_INSET_SIZE}:{config.EVIDENCE_INSET_SIZE}:"
            f"{config.EVIDENCE_BORDER_PX}:{config.EVIDENCE_BORDER_PX}:color={config.EVIDENCE_BORDER_COLOR}[ev];"
        )
        parts.append(f"[{label}][ev]overlay=x={ex}:y={ey}[ev_out];")
        extra_inputs += ["-loop", "1", "-i", str(evidence_path)]
        label, next_idx = "ev_out", next_idx + 1

    filter_complex = "".join(parts)
    if label == "bg":
        filter_complex = filter_complex.rstrip(";")  # neither layer present - today's exact no-overlay behavior
    map_label = f"[{label}]"

    ffmpeg_tool.run(
        visual_input
        + extra_inputs
        + [
            "-filter_complex", filter_complex,
            "-map", map_label,
            "-frames:v", str(n_frames),
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "20",
            str(out_path),
        ]
    )


def _flatten_segments(meta: list[dict], manifest: dict) -> list[dict]:
    """One entry per visual segment, carrying its resolved pose (per-beat, from
    character.pose_for_beat) and cycling position (per-segment, from
    character.position_for_segment - this is what actually creates the
    "character moves across the square" effect, independent of pose variety), plus
    an optional evidence image/position pulled from the segment's own manifest entry
    (resolve.py already guarantees a cue-less fallback segment never inherits a
    neighbor's evidence - see visuals/resolve.py's resolve_all())."""
    flat = []
    global_idx = 0
    for beat in meta:
        pose = character.pose_for_beat(beat)
        for seg_i, seg in enumerate(beat["segments"]):
            seg_id = f"{beat['id']}_seg{seg_i:02d}"
            ev = manifest.get(seg_id, {}).get("evidence")
            flat.append(
                {
                    "id": seg_id,
                    "start": seg["start"],
                    "end": seg["end"],
                    "pose": pose,
                    "x": character.position_for_segment(global_idx),
                    "motion": motion_for_segment(seg_id),
                    "evidence_path": Path(ev["path"]) if ev else None,
                    "evidence_xy": evidence.position_for_segment(seg_id) if ev else None,
                }
            )
            global_idx += 1
    return flat


def build_video_track(slug: str, force: bool = False) -> str:
    build = config.build_dir(slug)
    meta = json.loads((build / "narration_meta.json").read_text(encoding="utf-8"))["beats"]
    manifest = {e["id"]: e for e in json.loads((build / "manifest.json").read_text(encoding="utf-8"))}
    clips_dir = build / "clips"
    clips_dir.mkdir(exist_ok=True)

    total_duration = meta[-1]["end"] + config.BEAT_GAP_SEC  # matches audio_mix.py's trailing apad
    segments = _flatten_segments(meta, manifest)

    clip_paths = []
    for i, seg in enumerate(segments):
        clip_start = seg["start"]
        clip_end = segments[i + 1]["start"] if i + 1 < len(segments) else total_duration
        duration = clip_end - clip_start
        clip_path = clips_dir / f"{seg['id']}.mp4"
        if force or not clip_path.exists():
            char_path = config.CHARACTER_DIR / f"{seg['pose']}.png"
            _build_segment_clip(
                manifest[seg["id"]]["path"],
                duration,
                char_path,
                seg["x"],
                seg["motion"],
                clip_path,
                evidence_path=seg["evidence_path"],
                evidence_xy=seg["evidence_xy"],
                source=manifest[seg["id"]].get("source"),
            )
        clip_paths.append(clip_path)

    concat_list = clips_dir / "concat.txt"
    concat_list.write_text(
        "\n".join(f"file '{p.resolve().as_posix()}'" for p in clip_paths), encoding="utf-8"
    )
    silent_path = build / "video_silent.mp4"
    ffmpeg_tool.run(["-f", "concat", "-safe", "0", "-i", str(concat_list), "-c", "copy", str(silent_path)])
    return str(silent_path)


def _escape_filter_path(path: str) -> str:
    return path.replace("\\", "/").replace(":", "\\:")


def assemble(slug: str, force: bool = False) -> str:
    build = config.build_dir(slug)
    out_dir = config.output_dir(slug)
    captions_path = build / "captions.ass"
    mix_path = build / "mix.wav"
    final_path = out_dir / "final.mp4"

    if final_path.exists() and not force:
        return str(final_path)

    silent_path = build_video_track(slug, force=force)
    vf = f"ass='{_escape_filter_path(str(captions_path))}'"
    ffmpeg_tool.run(
        [
            "-i", silent_path, "-i", str(mix_path),
            "-vf", vf,
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "20",
            "-c:a", "aac", "-b:a", "192k",
            "-shortest",
            str(final_path),
        ]
    )
    return str(final_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("slug")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    final_path = assemble(args.slug, force=args.force)
    info = ffmpeg_tool.probe_video_info(final_path)
    print(f"Assembled -> {final_path}")
    print(f"  {info['width']}x{info['height']}, {info['duration']:.1f}s")
