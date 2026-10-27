"""
CATEGORY G - Universal cinematic editing SFX (7 one-shots, SFX_ED01-07).
Generic cut/transition/impact tools, each serving a distinct editing
purpose rather than overlapping.
"""

import numpy as np
import audio_lib as A


def make_ed01_short_whoosh():
    """A concise transition for a fast edit."""
    dur = 0.5
    noise = A.white_noise(dur, seed=1)
    sig = A.time_varying_bandpass(noise, f_start=300, f_end=3200, bw_oct=1.2, n_blocks=28)
    sig = sig * A.adsr(dur, attack=0.015, decay=0.08, sustain_level=0.25, release=0.25)
    sig = A.fade_edges(sig, fade_in=0.004, fade_out=0.05)
    sig = A.normalize(sig, peak_db=-7)
    return A.stereo_haas(sig, delay_ms=9, side_mix=0.5)


def make_ed02_deep_cinematic_impact():
    """A powerful, controlled impact."""
    dur = 1.2
    boom = A.exp_pitch_sweep(140, 35, dur) * A.adsr(dur, attack=0.004, decay=0.3, sustain_level=0.25, release=0.7)
    click = A.white_noise(0.02, seed=2) * 0.7
    sig = boom.copy()
    sig[: len(click)] += click
    sig = A.lowpass(sig, cutoff=1200)
    sig = A.synth_reverb(sig, decay=1.6, wet=0.26)
    sig = A.normalize(sig, peak_db=-5)
    return A.stereo_haas(sig, delay_ms=8, side_mix=0.3)


def make_ed03_reverse_impact():
    """A reverse swell leading into a reveal."""
    dur = 1.4
    sig = A.reverse_riser(dur, seed=3, decay=4.0, cutoff=3400) * 0.5
    sig = A.normalize(sig, peak_db=-6)
    return A.stereo_haas(sig, delay_ms=15, side_mix=0.5)


def make_ed04_subtle_low_hit():
    """A restrained low-frequency accent for emphasis."""
    dur = 0.5
    sig = A.exp_pitch_sweep(90, 45, dur) * A.adsr(dur, attack=0.003, decay=0.15, sustain_level=0.1, release=0.3)
    sig = A.lowpass(sig, cutoff=700)
    sig = A.normalize(sig, peak_db=-7)
    return A.stereo_haas(sig, delay_ms=6, side_mix=0.25)


def make_ed05_silence_drop():
    """A carefully designed transition into near-silence."""
    dur = 0.6
    sig = A.lowpass(A.white_noise(dur, seed=4), cutoff=1800)
    env = A.envelope_from_breakpoints(dur, A.SR, [(0, 0.6), (0.08, 0.6), (0.15, 0.02), (0.6, 0.0)])
    sig = sig * env
    sig = A.normalize(sig, peak_db=-9)
    return A.stereo_haas(sig, delay_ms=5, side_mix=0.3)


def make_ed06_atmospheric_riser():
    """A gradual build suitable for a short reveal."""
    dur = 2.0
    noise = A.white_noise(dur, seed=5)
    sweep = A.time_varying_bandpass(noise, f_start=200, f_end=3800, bw_oct=1.3, n_blocks=48)
    tone = A.exp_pitch_sweep(90, 500, dur) * 0.4
    sig = sweep * 0.6 + tone
    crescendo = np.linspace(0.05, 1.0, len(sig)) ** 1.4
    sig = sig * crescendo
    sig = A.fade_edges(sig, fade_in=0.04, fade_out=0.06)
    sig = A.normalize(sig, peak_db=-6)
    return A.stereo_haas(sig, delay_ms=16, side_mix=0.55)


def make_ed07_seamless_ambient_tail():
    """A useful atmospheric ending designed to blend naturally into an
    existing soundscape."""
    dur = 2.5
    sig = A.lowpass(A.pad_voice([110.0, 164.81], dur, detune_voices=3, spread_cents=8, seed=6), cutoff=900)
    sig = sig * A.envelope_from_breakpoints(dur, A.SR, [(0, 0.8), (1.5, 0.6), (2.5, 0.0)])
    sig = A.synth_reverb(sig, decay=2.0, wet=0.3)
    sig = A.normalize(sig, peak_db=-8)
    return A.stereo_haas(sig, delay_ms=18, side_mix=0.45)
