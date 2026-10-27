import time
from kokoro_onnx import Kokoro
import soundfile as sf
from faster_whisper import WhisperModel

text = (
    "The ancient Library of Alexandria was one of the largest and most significant "
    "libraries of the ancient world. Scholars believe it may have held hundreds of "
    "thousands of scrolls, covering mathematics, astronomy, medicine, and philosophy. "
    "Its eventual destruction remains one of history's great unsolved mysteries, "
    "debated by historians for centuries."
)

print("=== Step 1: Generate audio with Kokoro ===")
kokoro = Kokoro("kokoro-v1.0.int8.onnx", "voices-v1.0.bin")
t0 = time.time()
samples, sample_rate = kokoro.create(text, voice="af_heart", speed=1.0, lang="en-us")
gen_time = time.time() - t0
audio_duration = len(samples) / sample_rate
sf.write("alignment_test.wav", samples, sample_rate)
print(f"TTS generation: {gen_time:.2f}s for {audio_duration:.2f}s of audio (RTF={gen_time/audio_duration:.2f})")

print("\n=== Step 2: Forced alignment with faster-whisper ===")
t0 = time.time()
model = WhisperModel("base.en", device="cpu", compute_type="int8")
load_time = time.time() - t0
print(f"Whisper model load: {load_time:.2f}s")

t0 = time.time()
segments, info = model.transcribe("alignment_test.wav", word_timestamps=True)
segments = list(segments)
align_time = time.time() - t0
print(f"Alignment time: {align_time:.2f}s (RTF={align_time/audio_duration:.2f})")

print("\n=== Word-level timestamps ===")
word_count = 0
for seg in segments:
    for w in seg.words:
        print(f"  [{w.start:6.2f}s - {w.end:6.2f}s]  {w.word}")
        word_count += 1

print(f"\nTotal words aligned: {word_count}")
print(f"Expected words (approx): {len(text.split())}")
print(f"\nTotal pipeline time: {gen_time + load_time + align_time:.2f}s for {audio_duration:.2f}s of audio")
