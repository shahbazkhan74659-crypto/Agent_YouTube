"""faster-whisper word-level forced alignment, per beat wav (same base.en/cpu/int8
config already proven in kokoro-test/test_alignment.py). Augments
build/narration_meta.json in place with each beat's word timestamps, so
captions.py has one file to read instead of stitching per-beat files itself.
"""

import argparse
import json
from pathlib import Path

import config


def align(slug: str, force: bool = False) -> list[dict]:
    build = config.build_dir(slug)
    meta_path = build / "narration_meta.json"
    data = json.loads(meta_path.read_text(encoding="utf-8"))
    meta = data["beats"]

    model = None
    for b in meta:
        wav_path = Path(b["wav_path"])
        words_path = wav_path.with_name(f"{b['id']}_words.json")

        if words_path.exists() and not force:
            words = json.loads(words_path.read_text(encoding="utf-8"))
        else:
            if model is None:
                from faster_whisper import WhisperModel

                model = WhisperModel(
                    config.WHISPER_MODEL_SIZE,
                    device=config.WHISPER_DEVICE,
                    compute_type=config.WHISPER_COMPUTE_TYPE,
                )
            segments, _info = model.transcribe(str(wav_path), word_timestamps=True)
            words = [
                {"word": w.word.strip(), "start": round(w.start, 3), "end": round(w.end, 3)}
                for seg in segments
                for w in seg.words
            ]
            words_path.write_text(json.dumps(words, indent=2, ensure_ascii=False), encoding="utf-8")

        b["words"] = words
        b["words_path"] = str(words_path)

    data["beats"] = meta
    meta_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return meta


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("slug")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    meta = align(args.slug, force=args.force)
    total_words = sum(len(b["words"]) for b in meta)
    expected = sum(len(b["narration"].split()) for b in meta)
    print(f"Aligned {len(meta)} beats, {total_words} words (expected ~{expected})")
    for b in meta:
        print(f"  {b['id']}: {len(b['words'])} words, {b['duration']:.2f}s")
