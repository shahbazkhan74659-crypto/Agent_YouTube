"""Thin subprocess wrapper around the imageio-ffmpeg-bundled ffmpeg binary (pip
install, no system/winget install needed - avoids the admin-elevation friction
the GIMP install hit earlier). Confirmed on this machine: ffmpeg 7.1 essentials
build with libx264/libx265/libass/zoompan all present. Note: imageio-ffmpeg only
bundles ffmpeg itself, not ffprobe - probe_duration() below parses ffmpeg's own
stderr "Duration:" line instead of shelling out to a binary that isn't there.
"""

import re
import subprocess

import imageio_ffmpeg

FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()
_DURATION_RE = re.compile(r"Duration:\s*(\d+):(\d\d):(\d\d)\.(\d\d)")


def run(args: list[str]) -> subprocess.CompletedProcess:
    cmd = [FFMPEG_EXE, "-y", "-hide_banner", "-loglevel", "error"] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"ffmpeg failed (exit {result.returncode}):\ncmd: {' '.join(cmd)}\nstderr:\n{result.stderr}"
        )
    return result


def probe_duration(path: str) -> float:
    """Works for any ffmpeg-readable file (audio or video) without needing ffprobe."""
    result = subprocess.run([FFMPEG_EXE, "-hide_banner", "-i", path], capture_output=True, text=True)
    match = _DURATION_RE.search(result.stderr)
    if not match:
        raise RuntimeError(f"Could not parse duration from ffmpeg output for {path}:\n{result.stderr[-500:]}")
    h, m, s, cs = (int(g) for g in match.groups())
    return h * 3600 + m * 60 + s + cs / 100


def probe_video_info(path: str) -> dict:
    """Returns {width, height, duration} parsed from ffmpeg's stderr banner."""
    result = subprocess.run([FFMPEG_EXE, "-hide_banner", "-i", path], capture_output=True, text=True)
    stream_match = re.search(r"Video:.*?(\d{2,5})x(\d{2,5})", result.stderr)
    if not stream_match:
        raise RuntimeError(f"Could not parse video stream info for {path}:\n{result.stderr[-500:]}")
    dur_match = _DURATION_RE.search(result.stderr)
    h, m, s, cs = (int(g) for g in dur_match.groups()) if dur_match else (0, 0, 0, 0)
    return {
        "width": int(stream_match.group(1)),
        "height": int(stream_match.group(2)),
        "duration": h * 3600 + m * 60 + s + cs / 100,
    }
