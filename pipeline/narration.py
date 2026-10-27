"""Kokoro TTS per beat. Reads build/beats.json, writes build/beats/<id>.wav plus
build/narration_meta.json - the timed contract (start/end/duration per beat,
cumulative across beats with config.BEAT_GAP_SEC silence between them) that every
later stage (alignment, visuals, captions, audio_mix, assemble) reads instead of
re-deriving timing itself.

Also gives every beat's visual segments (from script_parser.py) a start/end on
the same global timeline, by splitting the beat's span proportionally by each
segment's word count - not a new alignment pass. Visual-cut placement tolerates
a few hundred ms of drift fine, unlike captions, so this doesn't need to be
word-exact or depend on Whisper's transcription matching the segment text.
"""

import argparse
import json
from pathlib import Path

import soundfile as sf

import config


def load_beats(slug: str) -> dict:
    path = config.build_dir(slug) / "beats.json"
    return json.loads(path.read_text(encoding="utf-8"))


def _segment_timing(segments: list[dict], start: float, end: float, beat_id: str = "?") -> list[dict]:
    word_counts = [max(1, len(seg["text"].split())) for seg in segments]
    total_words = sum(word_counts)
    duration = end - start
    cursor = start
    timed = []
    for seg, wc in zip(segments, word_counts):
        seg_end = cursor + duration * wc / total_words
        timed.append({**seg, "start": round(cursor, 3), "end": round(seg_end, 3)})
        cursor = seg_end
    if timed:
        timed[-1]["end"] = round(end, 3)  # avoid float drift leaving a gap at the beat boundary
    for i, seg in enumerate(timed):
        seg_dur = seg["end"] - seg["start"]
        if seg_dur > config.MAX_SEGMENT_DURATION_SEC:
            preview = seg["text"][:40] + ("..." if len(seg["text"]) > 40 else "")
            print(
                f"  [cut-rate] WARNING: {beat_id} seg{i:02d} would hold for {seg_dur:.1f}s "
                f"(cap {config.MAX_SEGMENT_DURATION_SEC:.1f}s) - \"{preview}\" - place "
                f"another [ON SCREEN: ...]/AI-generate: cue in this stretch of script.md"
            )
    return timed


def synthesize(slug: str, voice: str | None = None, force: bool = False, lang: str = "en-us") -> tuple[list[dict], str]:
    voice = voice or config.get_voice_preset()
    data = load_beats(slug)
    title, beats = data["title"], data["beats"]
    build = config.build_dir(slug)
    beats_dir = build / "beats"
    beats_dir.mkdir(exist_ok=True)

    kokoro = None
    cursor = 0.0
    timed = []
    for b in beats:
        wav_path = beats_dir / f"{b['id']}.wav"
        if wav_path.exists() and not force:
            data, sr = sf.read(str(wav_path))
            duration = len(data) / sr
        else:
            if kokoro is None:
                from kokoro_onnx import Kokoro

                kokoro = Kokoro(str(config.KOKORO_MODEL_PATH), str(config.KOKORO_VOICES_PATH))
            samples, sr = kokoro.create(b["narration"], voice=voice, speed=config.KOKORO_SPEED, lang=lang)
            duration = len(samples) / sr
            sf.write(str(wav_path), samples, sr)

        start = cursor
        end = start + duration
        cursor = end + config.BEAT_GAP_SEC
        timed.append(
            {
                **b,
                "segments": _segment_timing(b["segments"], start, end, b["id"]),
                "wav_path": str(wav_path),
                "duration": round(duration, 3),
                "start": round(start, 3),
                "end": round(end, 3),
                "voice": voice,
            }
        )

    out_path = build / "narration_meta.json"
    out_data = {"title": title, "beats": timed}
    out_path.write_text(json.dumps(out_data, indent=2, ensure_ascii=False), encoding="utf-8")
    return timed, str(out_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("slug")
    parser.add_argument("--voice", default=None)
    parser.add_argument("--lang", default="en-us", help="espeak-ng language code for Kokoro, e.g. 'hi' for Hindi")
    parser.add_argument("--force", action="store_true", help="Re-synthesize even if a beat's wav already exists")
    args = parser.parse_args()

    timed, out_path = synthesize(args.slug, voice=args.voice, force=args.force, lang=args.lang)
    total = timed[-1]["end"] if timed else 0.0
    print(f"Synthesized {len(timed)} beats, voice={timed[0]['voice'] if timed else '-'}, "
          f"total timeline {total:.1f}s -> {out_path}")
    for t in timed:
        print(f"  [{t['start']:6.2f}-{t['end']:6.2f}] {t['id']} ({t['duration']:.2f}s)")
