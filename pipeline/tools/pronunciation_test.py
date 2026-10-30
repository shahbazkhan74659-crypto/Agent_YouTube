"""One-off: checks whether Kokoro (current default voice) actually mispronounces
the Greek/Ptolemaic proper nouns this channel's scripts use, or whether it's just
faster-whisper's `base` model mishearing them (open item logged in memory.md since
2026-10-26, never actually confirmed). Synthesizes the real lines containing each
proper noun, straight from the production `library-of-alexandria-destruction`
script - not invented test sentences - then runs the same faster-whisper alignment
used in the real pipeline over each one as a cross-check.

This does NOT replace a human listen - Whisper mishearing a word is exactly the
failure mode in question, so its transcript here is a secondary signal, not proof
either way. Listen to the .wav files yourself and compare against what Whisper
heard.

Usage:
    python pronunciation_test.py [--voice am_adam] [--lang en-us]
"""

import argparse
import sys
from pathlib import Path

import soundfile as sf

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import config  # noqa: E402

OUT_DIR = config.PROJECT_ROOT / "pronunciation-test"

# Real lines from videos/library-of-alexandria-destruction/script.md, one per
# proper noun (or cluster of them), not synthetic test sentences.
LINES = {
    "mouseion_ptolemaic": (
        "The Library was part of the Mouseion, a research institution founded "
        "in the early Ptolemaic dynasty, in Egypt."
    ),
    "demetrius_phalerum_ptolemy": (
        "Tradition credits Demetrius of Phalerum with proposing it to Ptolemy I, "
        "though some historians call his exact role debatable, so treat that "
        "detail as likely, not certain."
    ),
    "caesar_strabo": (
        "Caesar's own account only mentions burning ships and docks, it's a "
        "later writer, Strabo, writing twenty-five years afterward, who "
        "connects the fire to the library."
    ),
    "serapeum_theophilus": (
        "In 391 CE, the Serapeum temple in Alexandria was destroyed under "
        "Bishop Theophilus, that part is well documented by near-contemporary "
        "writers."
    ),
    "caliph_bar_hebraeus": (
        "The most famous version, a caliph ordering the library burned because "
        "its books were either redundant with or contrary to the Quran, traces "
        "to a single writer, Bar Hebraeus, writing roughly six hundred years "
        "after the fact."
    ),
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--voice", default=None, help="Defaults to voice.md's confirmed preset (am_adam)")
    parser.add_argument("--lang", default="en-us")
    args = parser.parse_args()

    voice = args.voice or config.get_voice_preset()

    from kokoro_onnx import Kokoro

    OUT_DIR.mkdir(exist_ok=True)
    print(f"Voice: {voice} (lang={args.lang})")
    print("Loading Kokoro model...")
    kokoro = Kokoro(str(config.KOKORO_MODEL_PATH), str(config.KOKORO_VOICES_PATH))

    wav_paths = {}
    for key, text in LINES.items():
        samples, sr = kokoro.create(text, voice=voice, speed=config.KOKORO_SPEED, lang=args.lang)
        out_path = OUT_DIR / f"{key}.wav"
        sf.write(str(out_path), samples, sr)
        wav_paths[key] = out_path
        print(f'  [{key}] "{text}" -> {out_path}')

    print("\nRunning faster-whisper over each line as a cross-check (same model/settings as alignment.py)...")
    from faster_whisper import WhisperModel

    model = WhisperModel(
        config.WHISPER_MODEL_SIZE,
        device=config.WHISPER_DEVICE,
        compute_type=config.WHISPER_COMPUTE_TYPE,
    )

    print(f"\n{'KEY':<28} {'SAID (script)':<60}")
    for key, text in LINES.items():
        segments, _info = model.transcribe(str(wav_paths[key]), word_timestamps=False)
        heard = " ".join(seg.text.strip() for seg in segments)
        print(f"\n[{key}]")
        print(f"  script: {text}")
        print(f"  heard : {heard}")

    print(f"\nAll {len(LINES)} lines written to {OUT_DIR}\\ - listen to each one yourself.")
    print("Whisper's transcript above is only a secondary signal (it's the same model that")
    print("mis-heard these proper nouns before) - the real answer is your own ear.")


if __name__ == "__main__":
    main()
