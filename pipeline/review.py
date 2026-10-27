"""Extracts still frames from a rendered final.mp4 so Claude can actually look at
them (via the Read tool) - a partial substitute for watching the video, since
there's no real video-playback tool available. Pulls the start and end frame of
every beat (so a Ken Burns zoom/pan is visible as a before/after pair, not just a
single static moment) plus the caption text visible at each point.

This does NOT replace an actual watch/listen - it can catch a wrong/ugly image,
a caption rendering off-screen or overlapping, or a totally static (non-zooming)
clip, but not motion smoothness, audio quality, or pacing.
"""

import argparse
import json

import config
import ffmpeg_tool


def extract_frames(slug: str, force: bool = False) -> list[str]:
    build = config.build_dir(slug)
    out_dir = build / "review_frames"
    out_dir.mkdir(exist_ok=True)
    final_path = config.output_dir(slug) / "final.mp4"
    meta = json.loads((build / "narration_meta.json").read_text(encoding="utf-8"))["beats"]

    frame_paths = []
    for beat in meta:
        for tag, t in (("start", beat["start"] + 0.1), ("end", beat["end"] - 0.1)):
            out_path = out_dir / f"{beat['id']}_{tag}.jpg"
            if not out_path.exists() or force:
                ffmpeg_tool.run(
                    ["-ss", f"{max(t, 0):.3f}", "-i", str(final_path), "-frames:v", "1", "-q:v", "2", str(out_path)]
                )
            frame_paths.append(str(out_path))
    return frame_paths


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("slug")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    paths = extract_frames(args.slug, force=args.force)
    print(f"Extracted {len(paths)} frames:")
    for p in paths:
        print(f"  {p}")
