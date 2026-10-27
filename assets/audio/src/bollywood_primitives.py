"""
Synthesis primitives for the Bollywood-referenced emotion music library
(Assets_audio/music_bollywood/, see its README for the legal/style line).
Approximates the TIMBRE and TECHNIQUE of Bollywood background-score
instrumentation - tabla, dholak, sitar, bansuri, harmonium, tanpura, string
section - entirely through procedural synthesis, exactly the way every other
primitive in audio_lib.py builds its own timbres. Nothing here is sampled
from, or derived from, any actual recording; every function below composes
basic DSP techniques (pitch sweeps, inharmonic partials, filtered noise,
vibrato, detuned-oscillator chorus) already used elsewhere in this codebase,
just aimed at a different instrument palette.

Status (2026-10-26): primitives only - no finished emotion composition has
been written yet. See bollywood_music/ for the per-emotion module stubs that
will eventually call these once there's a composition brief per emotion.
"""

import numpy as np

import audio_lib as A

SR = A.SR


# --------------------------------------------------------------- percussion --

def tabla_hit(freq, dur, sr=SR, stroke="ge", seed=0):
    """Pitched hand-drum hit (tabla/dholak family). 'ge' (the bass stroke,
    played on the bayan/left drum with the heel of the hand) gets a fast
    downward pitch bend, typical of a palm pressed into the head as it rings;
    'na'/'tin' (treble strokes, the dayan/right drum) stay closer to a fixed
    pitch with a brighter, shorter decay. Built from a pitch-swept sine body
    plus a short bandpassed noise strike transient - not sampled."""
    rng = np.random.default_rng(seed)
    n = int(sr * dur)
    if stroke == "ge":
        body = A.exp_pitch_sweep(freq * 1.4, freq * 0.85, dur, sr)
        decay = 3.5
    else:
        body = A.sine(freq, dur, sr)
        decay = 9.0
    env = np.exp(-np.linspace(0, decay, n))
    strike_len = min(int(sr * 0.006), n)
    strike = np.zeros(n)
    strike[:strike_len] = rng.standard_normal(strike_len) * np.exp(-np.linspace(0, 12, strike_len))
    return body * env + A.bandpass(strike, sr, center=freq * 3, bw_oct=2.0) * 0.6


def dholak_hit(freq, dur, sr=SR, seed=0):
    """Two-headed hand drum, lower and boomier than tabla - the driving
    rhythmic pulse behind up-tempo cues (motivational/epic/cheerful)."""
    return tabla_hit(freq * 0.6, dur, sr=sr, stroke="ge", seed=seed)


# ------------------------------------------------------------------- strings --

def sitar_pluck(freq, dur, sr=SR, meend_cents=0.0, meend_time=0.12, seed=0):
    """Plucked string with the sitar's two defining features approximated: a
    bright noise pluck transient, and 'jawari' buzz - the sitar's flattened
    bridge lets overtones ring on in a characteristic buzzy sustain,
    approximated here with mild saturation on the decaying partials rather
    than a clean harmonic decay. meend_cents lets a note bend into pitch
    (pulling the string sideways, a real sitar technique) instead of
    starting at it."""
    rng = np.random.default_rng(seed)
    n = int(sr * dur)
    t = np.arange(n) / sr
    if meend_cents:
        bend = meend_cents * np.exp(-t / max(meend_time, 1e-3))
        inst_freq = freq * (2 ** (bend / 1200))
        phase = 2 * np.pi * np.cumsum(inst_freq) / sr
        fundamental = np.sin(phase)
    else:
        fundamental = A.sine(freq, dur, sr)
    partials = np.zeros(n)
    for ratio, amp, dk in [(1.0, 1.0, 2.2), (2.01, 0.5, 3.5), (3.0, 0.3, 5.0), (4.98, 0.18, 7.0)]:
        partials += np.sin(2 * np.pi * freq * ratio * t) * amp * np.exp(-t * dk)
    body = A.saturate(fundamental * np.exp(-t * 2.0) + partials, drive=1.6)
    pluck_len = min(int(sr * 0.01), n)
    click = np.zeros(n)
    click[:pluck_len] = rng.standard_normal(pluck_len)
    return body + A.highpass(click, sr, cutoff=2500) * 0.5


def tanpura_drone(root_freq, dur, sr=SR, tuning=(1.0, 1.5, 1.0, 0.5), cycle_sec=3.2, seed=0):
    """Continuous drone built from repeated sitar-style plucks on a fixed
    cycle (the tanpura's characteristic Sa-Pa-Sa-Sa / Sa-Ma-Sa-Sa pattern,
    `tuning` given as ratios on the root) - the sustained harmonic bed
    almost every Bollywood cue, of any emotion, sits on top of."""
    n = int(sr * dur)
    out = np.zeros(n)
    step = int(sr * cycle_sec / len(tuning))
    pos, i = 0, 0
    while pos < n:
        ratio = tuning[i % len(tuning)]
        note_dur = min(cycle_sec / len(tuning) * 1.8, (n - pos) / sr)
        if note_dur <= 0:
            break
        note = sitar_pluck(root_freq * ratio, note_dur, sr=sr, seed=seed + i)
        end = min(pos + len(note), n)
        out[pos:end] += note[: end - pos] * 0.5
        pos += step
        i += 1
    return out


def string_section_swell(freqs, dur, sr=SR, voices=6, swell_points=None, seed=0):
    """Lush legato string-section pad with a slow dynamic swell - the
    orchestral drama behind epic/romantic/motivational payoff moments. Built
    on audio_lib.pad_voice (detuned-oscillator chorus) rather than a single
    clean tone, since a real section is many slightly-detuned players."""
    pad = A.pad_voice(freqs, dur, sr=sr, detune_voices=voices, spread_cents=7.0, wave="sine", seed=seed)
    if swell_points is None:
        swell_points = [(0, 0.0), (dur * 0.4, 1.0), (dur * 0.85, 1.0), (dur, 0.0)]
    env = A.envelope_from_breakpoints(dur, sr, swell_points)
    return pad * env


# -------------------------------------------------------------------- winds --

def bansuri_tone(freq, dur, sr=SR, breathiness=0.15, vibrato_rate_hz=5.0, vibrato_depth_cents=18.0, seed=0):
    """Breathy bamboo flute: a vibrato'd sine body layered with filtered
    breath noise and a soft attack - the lead voice for reflective/romantic/
    peaceful cues."""
    rng = np.random.default_rng(seed)
    n = int(sr * dur)
    body = A.vibrato_sine(freq, dur, sr=sr, rate_hz=vibrato_rate_hz, depth_cents=vibrato_depth_cents)
    breath = A.bandpass(rng.standard_normal(n), sr, center=freq * 2.5, bw_oct=2.5) * breathiness
    attack = min(int(sr * 0.08), n)
    env = np.ones(n)
    env[:attack] = np.linspace(0, 1, attack)
    return (body + breath) * env


# ------------------------------------------------------------------- drones --

def harmonium_drone(freq, dur, sr=SR, reed_voices=4, tremolo_rate_hz=0.6, seed=0):
    """Sustained reed-organ drone: detuned triangle-wave voices (bellows-
    driven reeds beating slightly against each other) with a slow tremolo
    from the hand-pumped bellows. Foundation layer for cold/epic/awe/dark
    cues."""
    n = int(sr * dur)
    sig = np.zeros(n)
    rng = np.random.default_rng(seed)
    for v in range(reed_voices):
        detune = rng.uniform(-6, 6)
        sig += A.triangle(freq, dur, sr, detune_cents=detune) * 0.6
        sig += A.triangle(freq * 2, dur, sr, detune_cents=detune * 1.3) * 0.25
    sig /= reed_voices
    return A.tremolo(sig, sr=sr, rate_hz=tremolo_rate_hz, depth=0.12)
