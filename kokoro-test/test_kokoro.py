import time
from kokoro_onnx import Kokoro
import soundfile as sf

print("Loading model...")
t0 = time.time()
kokoro = Kokoro("kokoro-v1.0.int8.onnx", "voices-v1.0.bin")
print(f"Model load time: {time.time() - t0:.2f}s")

text = (
    "The ancient Library of Alexandria was one of the largest and most significant "
    "libraries of the ancient world. Scholars believe it may have held hundreds of "
    "thousands of scrolls, covering mathematics, astronomy, medicine, and philosophy."
)

print("Generating speech...")
t0 = time.time()
samples, sample_rate = kokoro.create(text, voice="af_heart", speed=1.0, lang="en-us")
gen_time = time.time() - t0

audio_duration = len(samples) / sample_rate
rtf = gen_time / audio_duration

sf.write("test_output.wav", samples, sample_rate)

print(f"Generation time: {gen_time:.2f}s")
print(f"Audio duration: {audio_duration:.2f}s")
print(f"Real-time factor (lower=faster-than-realtime): {rtf:.3f}")
print(f"Speed multiple: {1/rtf:.2f}x real-time" if rtf > 0 else "")
print("Saved to test_output.wav")
