"""One-off: generates the host character's pose library (not part of render.py's
per-video pipeline - run once, reused by every video the same way Assets_audio is).

Reuses visuals/ai_generate.py's Pollinations wrapper directly rather than
duplicating it. Prompt template is v3's winning design-concept prompt (plain
background, pure black silhouette, no visible face, long coat + wide-brim fedora -
confirmed working after 3 iterations) with only the gesture clause swapped per
pose. Each generated image gets backgrounds removed via rembg (confirmed working
cleanly in a smoke test) before being saved as the final transparent pose asset.

Usage: python generate_character_poses.py [--pose neutral|pointing|questioning] [--force]
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "visuals"))
import ai_generate  # noqa: E402
import config  # noqa: E402

PROMPT_TEMPLATE = (
    "a completely black silhouette figure standing against a plain solid dark blue background, "
    "no visible face, no visible skin, pure black shadow shape, "
    "wearing a long open coat and a wide-brim fedora hat, both part of the same black silhouette, "
    "{gesture}, "
    "minimalist graphic design, bold flat shapes, high contrast, full body, centered"
)

GESTURES = {
    "neutral": "standing straight, arms relaxed at sides, full body visible including feet and shoes",
    "pointing": (
        "right arm raised horizontally to the side at shoulder height, hand open with a single "
        "finger extended pointing sideways, confident stance, full body visible including feet and shoes"
    ),
    "questioning": (
        "one hand raised near the chin, head tilted slightly to one side, "
        "full body visible including feet and shoes"
    ),
}


def generate_pose(pose: str, force: bool = False) -> Path:
    out_path = config.CHARACTER_DIR / f"{pose}.png"
    if out_path.exists() and not force:
        return out_path

    config.CHARACTER_DIR.mkdir(parents=True, exist_ok=True)
    raw_path = config.CHARACTER_DIR / f"{pose}_raw.png"
    prompt = PROMPT_TEMPLATE.format(gesture=GESTURES[pose])
    ai_generate.generate(prompt, raw_path, width=600, height=900)

    from PIL import Image
    from rembg import remove

    cutout = remove(Image.open(raw_path))
    cutout.save(out_path)
    return out_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pose", choices=list(GESTURES), default=None, help="Generate just one pose")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    poses = [args.pose] if args.pose else list(config.CHARACTER_POSES)
    for pose in poses:
        path = generate_pose(pose, force=args.force)
        print(f"{pose}: {path}")
