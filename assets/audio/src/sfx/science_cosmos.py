"""
CATEGORY A - Science & cosmic SFX (8 one-shots, SFX_SC01-08). All original
procedural synthesis - none of these are claimed as literal recordings of
atoms, quantum events, or outer space.
"""

import numpy as np
import audio_lib as A


def make_sc01_atomic_pulse():
    """A compact, precise electronic pulse suggesting a microscopic
    process."""
    dur = 0.18
    sig = A.fm_tone(1400, dur, mod_ratio=4.0, mod_index=1.0) * A.adsr(
        dur, attack=0.002, decay=0.04, sustain_level=0.0, release=0.1)
    sig = A.normalize(sig, peak_db=-7)
    return A.stereo_haas(sig, delay_ms=5, side_mix=0.3)


def make_sc02_cosmic_sweep():
    """A spacious, evolving sweep for space imagery or scientific
    transitions."""
    dur = 2.5
    noise = A.white_noise(dur, seed=1)
    sig = A.time_varying_bandpass(noise, f_start=150, f_end=5200, bw_oct=1.6, n_blocks=70)
    sig = sig * A.adsr(dur, attack=0.3, decay=0.5, sustain_level=0.4, release=1.2)
    sig = A.synth_reverb(sig, decay=2.0, wet=0.3)
    sig = A.fade_edges(sig, fade_in=0.05, fade_out=0.3)
    sig = A.normalize(sig, peak_db=-6.5)
    return A.stereo_haas(sig, delay_ms=18, side_mix=0.55)


def make_sc03_quantum_glitch():
    """A brief, fragmented electronic effect with controlled digital
    irregularity."""
    dur = 0.4
    tone = A.fm_tone(900, dur, mod_ratio=2.73, mod_index=3.0)
    sig = A.granular_texture(tone, grain_ms=12, density=0.7, jitter_ms=20, seed=2)
    sig = A.fade_edges(sig, fade_in=0.002, fade_out=0.05)
    sig = A.normalize(sig, peak_db=-7)
    return A.stereo_haas(sig, delay_ms=7, side_mix=0.6)


def make_sc04_scientific_discovery_accent():
    """A sophisticated reveal accent for a new fact or breakthrough."""
    dur = 1.1
    sig = A.inharmonic_hit(988.0, dur, partials=[1, 2.0, 3.0, 4.0], decays=[2.2, 2.8, 3.6, 4.4],
                            noise_transient=0.15, seed=3)
    sig = A.synth_reverb(sig, decay=1.1, wet=0.26)
    sig = A.fade_edges(sig, fade_in=0.003, fade_out=0.25)
    sig = A.normalize(sig, peak_db=-7)
    return A.stereo_haas(sig, delay_ms=9, side_mix=0.4)


def make_sc05_energy_field():
    """An evolving synthetic tone suggesting an invisible field or force."""
    dur = 2.2
    sig = A.am_tone(220, dur, mod_freq=4.0, depth=0.6) + A.vibrato_sine(221.5, dur, rate_hz=0.3, depth_cents=40) * 0.5
    sig = sig * A.adsr(dur, attack=0.3, decay=0.3, sustain_level=0.7, release=0.6)
    sig = A.normalize(sig, peak_db=-7)
    return A.stereo_haas(sig, delay_ms=16, side_mix=0.5)


def make_sc06_signal_detected():
    """A distinctive electronic signal for the discovery of an unusual
    observation."""
    dur = 0.9
    n = int(A.SR * dur)
    sig = np.zeros(n)
    for i, f in enumerate([660, 880, 1320]):
        beep = A.fm_tone(f, 0.12, mod_ratio=1.5, mod_index=0.5) * A.adsr(
            0.12, attack=0.004, decay=0.03, sustain_level=0.3, release=0.06)
        start = int(i * 0.2 * A.SR)
        sig[start:start + len(beep)] += beep * 0.6
    sig = A.normalize(sig, peak_db=-7)
    return A.stereo_haas(sig, delay_ms=10, side_mix=0.4)


def make_sc07_deep_space_rumble():
    """A designed low-frequency atmospheric effect for cosmic imagery."""
    dur = 5.0
    sig = A.lowpass(A.vibrato_sine(42, dur, rate_hz=0.08, depth_cents=12), cutoff=90)
    sig = sig * A.adsr(dur, attack=1.0, decay=1.0, sustain_level=0.7, release=2.0)
    sig = A.synth_reverb(sig, decay=2.5, wet=0.3)
    sig = A.normalize(sig, peak_db=-7)
    return A.stereo_haas(sig, delay_ms=20, side_mix=0.4)


def make_sc08_particle_cascade():
    """A layered sequence of tiny, rapidly evolving synthetic transients."""
    dur = 1.3
    n = int(A.SR * dur)
    rng = np.random.default_rng(4)
    sig = np.zeros(n)
    for i in range(22):
        t_off = i * 0.055 + rng.uniform(-0.01, 0.01)
        freq = rng.uniform(900, 2600)
        click = A.fm_tone(freq, 0.04, mod_ratio=3.0, mod_index=0.6) * np.exp(-np.linspace(0, 12, int(A.SR * 0.04)))
        start = int(t_off * A.SR)
        end = min(start + len(click), n)
        if end > start:
            sig[start:end] += click[: end - start] * 0.3
    sig = A.normalize(sig, peak_db=-7)
    return A.stereo_haas(sig, delay_ms=6, side_mix=0.45)
