"""
Shared synthesis primitives for the channel's self-produced topic-based
music/SFX library (science/history/philosophy/mythology/mysteries/knowledge/
religion/storytelling). Pure numpy/scipy procedural synthesis - no samples,
no licensed material, no network calls. Every asset under music/ and sfx/ is
built from these functions by the per-category generator modules in
src/music/ and src/sfx/, via the registry in registry.py.

Supersedes the old flat assets/audio/audio_lib.py (44.1kHz/16-bit, 12 assets
tied to the Storytelling->Explanation->Questionary structure) - this library
is 48kHz/24-bit throughout.
"""

import numpy as np
import soundfile as sf
from scipy.signal import butter, lfilter, fftconvolve, resample_poly

SR = 48000

try:
    import pyloudnorm as _pyln
    _HAS_LOUDNORM = True
except ImportError:
    _HAS_LOUDNORM = False


# --------------------------------------------------------------- oscillators --

def sine(freq, dur, sr=SR, phase=0.0, detune_cents=0.0):
    n = int(sr * dur)
    t = np.arange(n) / sr
    f = freq * (2 ** (detune_cents / 1200))
    return np.sin(2 * np.pi * f * t + phase)


def triangle(freq, dur, sr=SR, detune_cents=0.0):
    n = int(sr * dur)
    t = np.arange(n) / sr
    f = freq * (2 ** (detune_cents / 1200))
    phase = (f * t) % 1.0
    return 2 * np.abs(2 * (phase - np.floor(phase + 0.5))) - 1


def square(freq, dur, sr=SR, duty=0.5, detune_cents=0.0):
    n = int(sr * dur)
    t = np.arange(n) / sr
    f = freq * (2 ** (detune_cents / 1200))
    phase = (f * t) % 1.0
    return np.where(phase < duty, 1.0, -1.0)


def white_noise(dur, sr=SR, seed=0):
    rng = np.random.default_rng(seed)
    return rng.standard_normal(int(sr * dur))


# -------------------------------------------------------------------- filters --

def lowpass(sig, sr=SR, cutoff=4000.0, order=2):
    cutoff = min(cutoff, sr * 0.49)
    b, a = butter(order, cutoff / (sr / 2), btype="low")
    return lfilter(b, a, sig)


def highpass(sig, sr=SR, cutoff=200.0, order=2):
    cutoff = max(cutoff, 10.0)
    b, a = butter(order, cutoff / (sr / 2), btype="high")
    return lfilter(b, a, sig)


def bandpass(sig, sr=SR, center=1000.0, bw_oct=1.0, order=2):
    low = max(center / (2 ** (bw_oct / 2)), 20.0)
    high = min(center * (2 ** (bw_oct / 2)), sr * 0.49)
    if high <= low:
        high = low * 1.1
    b, a = butter(order, [low / (sr / 2), high / (sr / 2)], btype="band")
    return lfilter(b, a, sig)


def time_varying_bandpass(noise, sr=SR, f_start=300.0, f_end=3000.0, bw_oct=1.3, n_blocks=48):
    """Overlap-add sweep filter: cheap, robust 'whoosh'/'riser' texture from noise."""
    n = len(noise)
    block = n // ((n_blocks + 1) // 2)
    hop = block // 2
    window = np.hanning(block)
    out = np.zeros(n + block)
    centers = np.geomspace(f_start, f_end, n_blocks)
    pos = 0
    for i in range(n_blocks):
        if pos + block > n:
            break
        seg = noise[pos:pos + block] * window
        filtered = bandpass(seg, sr, center=centers[i], bw_oct=bw_oct)
        out[pos:pos + block] += filtered
        pos += hop
    return out[:n]


# --------------------------------------------------------------- pitch/envelope --

def exp_pitch_sweep(f_start, f_end, dur, sr=SR):
    """Sine with an exponential pitch glide (for booms/dings)."""
    n = int(sr * dur)
    t = np.arange(n) / sr
    k = np.log(f_end / f_start) / dur
    inst_freq = f_start * np.exp(k * t)
    phase = 2 * np.pi * np.cumsum(inst_freq) / sr
    return np.sin(phase)


def adsr(dur, sr=SR, attack=0.05, decay=0.15, sustain_level=0.7, release=0.3):
    n = int(sr * dur)
    a = int(sr * attack)
    d = int(sr * decay)
    r = int(sr * release)
    s = max(n - a - d - r, 0)
    env = np.concatenate([
        np.linspace(0, 1, max(a, 1)),
        np.linspace(1, sustain_level, max(d, 1)),
        np.full(s, sustain_level),
        np.linspace(sustain_level, 0, max(r, 1)),
    ])
    if len(env) > n:
        env = env[:n]
    elif len(env) < n:
        env = np.pad(env, (0, n - len(env)))
    return env


def envelope_from_breakpoints(total_dur, sr, points):
    """points: [(time_sec, level), ...] sorted by time, linear-interpolated
    across the whole buffer. General-purpose automation curve for dynamics
    swells, fades, and deliberate silence dips."""
    n = int(sr * total_dur)
    times = np.array([p[0] for p in points])
    levels = np.array([p[1] for p in points])
    t = np.arange(n) / sr
    return np.interp(t, times, levels)


def vibrato_sine(freq, dur, sr=SR, rate_hz=0.3, depth_cents=15.0, phase=0.0):
    """Sine with a slow frequency wobble - continuous phase accumulation
    (not a per-sample recompute) so there's no discontinuity. Used for
    unstable/ghostly tonal layers."""
    n = int(sr * dur)
    t = np.arange(n) / sr
    cents = depth_cents * np.sin(2 * np.pi * rate_hz * t)
    inst_freq = freq * (2 ** (cents / 1200))
    ph = 2 * np.pi * np.cumsum(inst_freq) / sr + phase
    return np.sin(ph)


# --------------------------------------------------------------------- voices --

def pad_voice(freqs, dur, sr=SR, detune_voices=3, spread_cents=9.0, wave="sine", seed=0):
    """Chorus-style pad: several detuned oscillators per note, summed and averaged."""
    rng = np.random.default_rng(seed)
    n = int(sr * dur)
    out = np.zeros(n)
    osc = sine if wave == "sine" else triangle
    for f in freqs:
        for v in range(detune_voices):
            jitter = rng.uniform(-1.5, 1.5)
            spread = (v - (detune_voices - 1) / 2) * spread_cents + jitter
            out += osc(f, dur, sr, detune_cents=spread)
    out /= (len(freqs) * detune_voices)
    return out


def fm_tone(carrier, dur, sr=SR, mod_ratio=2.0, mod_index=3.0, phase=0.0):
    """Classic FM synthesis: carrier phase-modulated by a ratio-locked
    modulator. Non-integer mod_ratio values give inharmonic, metallic/
    digital timbres - used for science/mystery/signal textures."""
    n = int(sr * dur)
    t = np.arange(n) / sr
    mod = np.sin(2 * np.pi * carrier * mod_ratio * t)
    return np.sin(2 * np.pi * carrier * t + mod_index * mod + phase)


def am_tone(carrier, dur, sr=SR, mod_freq=5.0, depth=0.8, phase=0.0):
    """Amplitude modulation: carrier tone with a tremolo-like modulator,
    useful for pulsing/energy-field textures distinct from FM's timbral
    change."""
    n = int(sr * dur)
    t = np.arange(n) / sr
    carrier_sig = np.sin(2 * np.pi * carrier * t + phase)
    mod = 1 - depth + depth * (0.5 + 0.5 * np.sin(2 * np.pi * mod_freq * t))
    return carrier_sig * mod


def inharmonic_hit(freq, dur, sr=SR, partials=(1.0,), decays=(2.0,), noise_transient=0.0, seed=0):
    """Struck/metallic one-shot: a sum of decaying partials at the given
    frequency ratios, optionally with a short noise click at the onset
    (the 'strike' transient). Non-integer partial ratios give a metallic/
    dissonant color; integer-ish ratios give something closer to a bell."""
    n = int(sr * dur)
    t = np.arange(n) / sr
    sig = np.zeros(n)
    for p, d in zip(partials, decays):
        sig += np.sin(2 * np.pi * freq * p * t) * np.exp(-t * d)
    if noise_transient > 0:
        rng = np.random.default_rng(seed)
        click_len = min(int(sr * 0.008), n)
        sig[:click_len] += (rng.standard_normal(click_len) * noise_transient
                             * np.exp(-np.linspace(0, 8, click_len)))
    return sig


def reverse_riser(dur, sr=SR, seed=0, decay=5.0, cutoff=5000.0):
    """A decaying filtered-noise burst played backwards: rises from near-
    silence to a peak at the very end, instead of the usual attack-then-decay
    shape. Used to build energy into a cut/impact, or - for a loop - to
    connect the end of a loop back into its own opening."""
    n = int(sr * dur)
    rng = np.random.default_rng(seed)
    noise = rng.standard_normal(n)
    env = np.exp(-np.linspace(0, decay, n))
    sig = lowpass(noise * env, sr, cutoff=cutoff)
    return sig[::-1]


# ------------------------------------------------------------------ percussion --

def kick(dur, sr=SR, f_start=150.0, f_end=40.0, click=0.3, seed=0):
    """Minimal synthetic kick/low thump: pitch-dropping sine + an optional
    transient click, for tracks that need a real rhythmic pulse rather than
    a pad-only texture."""
    body = exp_pitch_sweep(f_start, f_end, dur, sr) * adsr(
        dur, sr, attack=0.002, decay=dur * 0.3, sustain_level=0.0, release=dur * 0.6)
    if click > 0:
        rng = np.random.default_rng(seed)
        click_len = min(int(sr * 0.006), len(body))
        body[:click_len] += rng.standard_normal(click_len) * click * np.exp(-np.linspace(0, 10, click_len))
    return body


def noise_perc(dur, sr=SR, band="high", decay=12.0, seed=0):
    """Short filtered-noise percussive hit - a hat/shaker/tick-style
    transient. band: 'high' (hat-like), 'mid' (shaker-like), 'low' (brush)."""
    rng = np.random.default_rng(seed)
    n = int(sr * dur)
    noise = rng.standard_normal(n)
    if band == "high":
        noise = highpass(noise, sr, cutoff=6000)
    elif band == "mid":
        noise = bandpass(noise, sr, center=2500, bw_oct=1.5)
    else:
        noise = lowpass(highpass(noise, sr, cutoff=400), sr, cutoff=1800)
    env = np.exp(-np.linspace(0, decay, n))
    return noise * env


def rhythm_pattern(cell_fn, pattern, step_dur, n_steps, sr=SR, **kwargs):
    """Lay out a boolean/weight pattern (list of 0..1 hit strengths) of
    length n_steps, each step_dur seconds apart, using cell_fn(dur, sr=sr,
    **kwargs) as the one-shot sound for each hit. Returns a buffer exactly
    n_steps * step_dur long."""
    total_dur = n_steps * step_dur
    n = int(sr * total_dur)
    buf = np.zeros(n)
    cell = cell_fn(min(step_dur * 1.8, 0.4), sr=sr, **kwargs)
    for i, strength in enumerate(pattern):
        if strength <= 0:
            continue
        start = int(i * step_dur * sr)
        end = min(start + len(cell), n)
        buf[start:end] += cell[: end - start] * strength
    return buf


# ------------------------------------------------------------------------ fx --

def tremolo(sig, sr=SR, rate_hz=0.15, depth=0.2):
    n = len(sig)
    t = np.arange(n) / sr
    lfo = 1 - depth + depth * np.sin(2 * np.pi * rate_hz * t)
    return sig * lfo


def synth_reverb(sig, sr=SR, decay=2.2, wet=0.28, seed=1):
    ir_len = int(sr * decay)
    rng = np.random.default_rng(seed)
    noise = rng.standard_normal(ir_len)
    env = np.exp(-np.linspace(0, 6.5, ir_len))
    ir = lowpass(noise * env, sr, cutoff=3500)
    ir = ir / (np.max(np.abs(ir)) + 1e-9)
    wet_sig = fftconvolve(sig, ir, mode="full")[:len(sig)]
    wet_sig = wet_sig / (np.max(np.abs(wet_sig)) + 1e-9) * (np.max(np.abs(sig)) + 1e-9)
    return (1 - wet) * sig + wet * wet_sig


def delay(sig, sr=SR, time_ms=250.0, feedback=0.35, mix=0.3, n_repeats=6):
    """Simple feedback delay line (not a true IIR comb - summed discrete
    taps, cheap and stable for short SFX/accent use)."""
    n_delay = int(sr * time_ms / 1000)
    out = sig.copy()
    tap = sig.copy()
    for i in range(1, n_repeats + 1):
        tap = np.concatenate([np.zeros(n_delay), tap])[: len(sig)] * feedback
        out = out + tap
    return (1 - mix) * sig + mix * out / (1 + mix)


def saturate(sig, drive=2.0):
    """Soft-clip (tanh) saturation for controlled distortion/grit."""
    return np.tanh(sig * drive) / np.tanh(drive)


def granular_texture(source, sr=SR, grain_ms=40.0, density=0.6, jitter_ms=15.0, seed=0):
    """Granular-style texture: chop `source` into short grains, scatter them
    with timing jitter and random gain, and overlay. Produces a stuttering/
    fragmented quality distinct from continuous synthesis - used for
    mystery/revelation/quantum-glitch textures."""
    rng = np.random.default_rng(seed)
    n = len(source)
    grain_n = max(int(sr * grain_ms / 1000), 8)
    window = np.hanning(grain_n)
    out = np.zeros(n)
    pos = 0
    hop = max(int(grain_n * 0.5), 1)
    while pos + grain_n < n:
        if rng.uniform(0, 1) < density:
            jitter = int(rng.uniform(-jitter_ms, jitter_ms) / 1000 * sr)
            src_start = min(max(pos + jitter, 0), n - grain_n)
            grain = source[src_start:src_start + grain_n] * window * rng.uniform(0.5, 1.0)
            out[pos:pos + grain_n] += grain
        pos += hop
    return out


def pan(stereo_or_mono, pos=0.0):
    """Constant-power pan a mono signal to a stereo pair. pos in [-1, 1]."""
    if stereo_or_mono.ndim == 2:
        mono = stereo_or_mono.mean(axis=1)
    else:
        mono = stereo_or_mono
    theta = (pos + 1) * np.pi / 4
    left = mono * np.cos(theta)
    right = mono * np.sin(theta)
    return np.stack([left, right], axis=1)


def normalize(sig, peak_db=-6.0):
    peak = np.max(np.abs(sig)) + 1e-9
    target = 10 ** (peak_db / 20)
    return sig * (target / peak)


def normalize_lufs(sig, sr=SR, target_lufs=-15.0, peak_ceiling_db=-5.0):
    """Gain the signal toward a target integrated loudness (LUFS) rather
    than just the loudest sample - fixes the case where plain peak
    normalize() under-represents perceived loudness for a signal with one
    brief hot transient over an otherwise sparse/ambient bed (same peak,
    much lower RMS/LUFS than a denser track). The result's peak is then
    capped at peak_ceiling_db so this never introduces clipping. Falls back
    to plain peak normalization at peak_ceiling_db if pyloudnorm isn't
    installed or loudness can't be measured (e.g. buffer too short)."""
    loudness = measure_loudness(sig, sr)
    if loudness is None or not np.isfinite(loudness):
        return normalize(sig, peak_db=peak_ceiling_db)
    gain = 10 ** ((target_lufs - loudness) / 20)
    out = sig * gain
    peak = np.max(np.abs(out)) + 1e-9
    ceiling = 10 ** (peak_ceiling_db / 20)
    if peak > ceiling:
        out = out * (ceiling / peak)
    return out


def fade_edges(sig, sr=SR, fade_in=0.01, fade_out=0.05):
    n = len(sig)
    fi = int(sr * fade_in)
    fo = int(sr * fade_out)
    out = sig.copy()
    if fi > 0:
        out[:fi] *= np.linspace(0, 1, fi)
    if fo > 0:
        out[-fo:] *= np.linspace(1, 0, fo)
    return out


def stereo_from_mono_chorus(pad_fn, *args, seed_l=10, seed_r=11, **kwargs):
    """Build left/right independently with different detune jitter -> natural width."""
    left = pad_fn(*args, seed=seed_l, **kwargs)
    right = pad_fn(*args, seed=seed_r, **kwargs)
    return np.stack([left, right], axis=1)


def stereo_haas(mono, sr=SR, delay_ms=14.0, side_mix=0.55):
    """Cheap stereo widening for one-shot SFX via a short delay on one channel."""
    delay_n = int(sr * delay_ms / 1000)
    left = mono
    right = np.concatenate([np.zeros(delay_n), mono])[: len(mono)]
    right = mono * (1 - side_mix) + right * side_mix
    return np.stack([left, right], axis=1)


def make_loopable(gen_fn, loop_dur, xfade=1.5, sr=SR, **kwargs):
    """Generate loop_dur + xfade of audio, then crossfade the tail into the
    head so the result loops seamlessly at exactly loop_dur seconds."""
    total = loop_dur + xfade
    sig = gen_fn(total, sr=sr, **kwargs)
    xf = int(sr * xfade)
    L = int(sr * loop_dur)
    fade_in = np.linspace(0, 1, xf)
    fade_out = 1 - fade_in
    if sig.ndim == 1:
        blended = sig[:xf] * fade_in + sig[L:L + xf] * fade_out
        out = sig[:L].copy()
        out[:xf] = blended
    else:
        blended = sig[:xf] * fade_in[:, None] + sig[L:L + xf] * fade_out[:, None]
        out = sig[:L].copy()
        out[:xf] = blended
    return out


# -------------------------------------------------------------- modal scales --

# Semitone offsets from the root, by mode name. Covers the spec's call for
# varied tonal/modal character across categories (not one scale family).
MODES = {
    "minor_pentatonic": [0, 3, 5, 7, 10],
    "major_pentatonic": [0, 2, 4, 7, 9],
    "dorian": [0, 2, 3, 5, 7, 9, 10],
    "phrygian": [0, 1, 3, 5, 7, 8, 10],
    "lydian": [0, 2, 4, 6, 7, 9, 11],
    "mixolydian": [0, 2, 4, 5, 7, 9, 10],
    "aeolian": [0, 2, 3, 5, 7, 8, 10],
    "whole_tone": [0, 2, 4, 6, 8, 10],
    "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
    "chromatic_fragment": [0, 1, 2, 3],
}


def modal_notes(root_hz, mode, octaves=2):
    """Return the frequencies of `mode`'s scale degrees built on root_hz,
    spanning `octaves` octaves."""
    steps = MODES[mode]
    out = []
    for o in range(octaves):
        for s in steps:
            out.append(root_hz * (2 ** (o + s / 12)))
    return out


# ------------------------------------------------------------------ measurement --

def true_peak_estimate(sig, sr=SR, oversample=4):
    """Estimate true peak via polyphase oversampling (not a certified ITU-R
    BS.1770-4 true-peak meter - a practical estimate, labeled as such in the
    catalog rather than claimed as standard-compliant)."""
    up = resample_poly(sig, oversample, 1, axis=0)
    return float(np.max(np.abs(up)))


def measure_loudness(sig, sr=SR):
    """Integrated loudness via pyloudnorm (ITU-R BS.1770 algorithm) if
    installed; returns None if the package isn't available rather than
    fabricating a number."""
    if not _HAS_LOUDNORM:
        return None
    try:
        meter = _pyln.Meter(sr)
        data = sig if sig.ndim == 2 else np.stack([sig, sig], axis=1)
        return float(meter.integrated_loudness(data))
    except Exception:
        return None


# ----------------------------------------------------------------------- io --

def write_wav24(path, sig, sr=SR):
    """Write 48kHz/24-bit PCM stereo via soundfile (scipy.io.wavfile can't
    write 24-bit cleanly, which is why the old library was 16-bit)."""
    if sig.ndim == 1:
        sig = np.stack([sig, sig], axis=1)
    sig = np.clip(sig, -1.0, 1.0)
    sf.write(str(path), sig, sr, subtype="PCM_24")
