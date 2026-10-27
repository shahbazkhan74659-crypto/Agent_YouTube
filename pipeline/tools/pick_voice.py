"""One-off: renders the same line in a handful of Kokoro presets so the user can
listen and pick one. Run once; the result gets written into voice.md by hand
afterward (not by this script - that's a one-line markdown edit, not worth
scripting). Usage:

    python pick_voice.py [--voices af_heart,af_bella,...] [--text "..."] [--slug <topic-slug>]
"""

import argparse
import sys
import time
from pathlib import Path

import soundfile as sf

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import config  # noqa: E402

DEFAULT_SHORTLIST = [
    "af_heart",
    "af_bella",
    "af_nova",
    "af_sky",
    "am_adam",
    "am_michael",
    "bm_george",
    "bf_emma",
]

DEFAULT_TEXT = (
    "Before you believe the caliph burned the Library of Alexandria, know the "
    "story has zero evidence from the century it happened in."
)

OUT_DIR = config.PROJECT_ROOT / "voice-picker"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--voices", default=",".join(DEFAULT_SHORTLIST))
    parser.add_argument("--text", default=None)
    parser.add_argument(
        "--slug",
        default=None,
        help="Pull beat_01's narration from this video's script as the test line instead of the default.",
    )
    args = parser.parse_args()

    text = args.text
    if text is None and args.slug:
        import script_parser

        beats = script_parser.parse_script(args.slug)
        text = beats[0].narration

    text = text or DEFAULT_TEXT
    voices = [v.strip() for v in args.voices.split(",") if v.strip()]

    from kokoro_onnx import Kokoro

    OUT_DIR.mkdir(exist_ok=True)
    print(f"Loading Kokoro model...")
    kokoro = Kokoro(str(config.KOKORO_MODEL_PATH), str(config.KOKORO_VOICES_PATH))
    print(f'Test line: "{text}"\n')

    for voice in voices:
        t0 = time.time()
        samples, sample_rate = kokoro.create(text, voice=voice, speed=config.KOKORO_SPEED, lang="en-us")
        gen_time = time.time() - t0
        duration = len(samples) / sample_rate
        out_path = OUT_DIR / f"{voice}.wav"
        sf.write(str(out_path), samples, sample_rate)
        rtf = gen_time / duration if duration else 0
        print(f"  {voice:<14} {duration:5.2f}s audio, RTF={rtf:.2f} -> {out_path}")

    print(f"\nListen to the files in {OUT_DIR}\\, then tell Claude which preset you picked")
    print("so it can be locked into voice.md.")


if __name__ == "__main__":
    main()
