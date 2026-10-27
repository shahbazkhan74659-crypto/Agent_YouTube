"""
CATEGORY B - History & archaeology SFX (7 one-shots, SFX_HI01-07). Designed
procedural approximations, not claimed as literal recordings of stone,
wood, or physical mechanisms.
"""

import numpy as np
import audio_lib as A


def make_hi01_ancient_stone_impact():
    """A heavy, resonant impact with a rough, stone-like texture."""
    dur = 1.0
    boom = A.exp_pitch_sweep(140, 48, dur) * A.adsr(dur, attack=0.004, decay=0.25, sustain_level=0.15, release=0.5)
    grit = A.bandpass(A.white_noise(dur, seed=1), center=350, bw_oct=1.2) * 0.5
    grit = grit * np.exp(-np.linspace(0, 9, len(grit)))
    sig = boom + grit
    sig = A.lowpass(sig, cutoff=1400)
    sig = A.fade_edges(sig, fade_in=0.002, fade_out=0.2)
    sig = A.normalize(sig, peak_db=-5.5)
    return A.stereo_haas(sig, delay_ms=8, side_mix=0.3)


def make_hi02_temple_door():
    """A slow, weighty, stylized door movement suitable for ancient
    architectural reveals."""
    dur = 1.8
    rng = np.random.default_rng(2)
    creak = A.bandpass(A.white_noise(dur, seed=2), center=900, bw_oct=1.0)
    creak = A.tremolo(creak, rate_hz=3.0, depth=0.6) * A.adsr(
        dur, attack=0.3, decay=0.4, sustain_level=0.4, release=0.6)
    thud = A.exp_pitch_sweep(110, 50, 0.3) * np.exp(-np.linspace(0, 8, int(A.SR * 0.3)))
    sig = creak * 0.5
    sig[-len(thud):] += thud * 0.4
    sig = A.normalize(sig, peak_db=-6.5)
    return A.stereo_haas(sig, delay_ms=14, side_mix=0.45)


def make_hi03_artifact_discovery():
    """A restrained reveal accent for uncovering an ancient object."""
    dur = 1.0
    sig = A.inharmonic_hit(440, dur, partials=[1, 1.98, 3.0], decays=[2.0, 2.6, 3.4], noise_transient=0.15, seed=3)
    sig = A.synth_reverb(sig, decay=1.2, wet=0.26)
    sig = A.fade_edges(sig, fade_in=0.003, fade_out=0.25)
    sig = A.normalize(sig, peak_db=-7)
    return A.stereo_haas(sig, delay_ms=9, side_mix=0.4)


def make_hi04_buried_chamber():
    """A low atmospheric transition suggesting the discovery of a
    concealed space."""
    dur = 2.0
    sig = A.lowpass(A.white_noise(dur, seed=4), cutoff=220) * A.adsr(
        dur, attack=0.5, decay=0.4, sustain_level=0.5, release=0.7)
    hollow = A.bandpass(A.white_noise(dur, seed=5), center=500, bw_oct=0.5) * 0.3
    sig = sig + hollow
    sig = A.synth_reverb(sig, decay=2.2, wet=0.35)
    sig = A.normalize(sig, peak_db=-7)
    return A.stereo_haas(sig, delay_ms=20, side_mix=0.5)


def make_hi05_ancient_mechanism():
    """A layered mechanical effect with grinding, clicks, and resonant
    movement."""
    dur = 1.5
    n = int(A.SR * dur)
    grind = A.bandpass(A.white_noise(dur, seed=6), center=600, bw_oct=1.3)
    grind = A.tremolo(grind, rate_hz=8.0, depth=0.5) * 0.4
    sig = grind.copy()
    rng = np.random.default_rng(7)
    for i in range(6):
        t_off = i * 0.22 + rng.uniform(-0.02, 0.02)
        click = A.noise_perc(0.05, band="high", decay=20, seed=int(t_off * 100))
        start = int(t_off * A.SR)
        end = min(start + len(click), n)
        if end > start:
            sig[start:end] += click[: end - start] * 0.4
    sig = A.fade_edges(sig, fade_in=0.01, fade_out=0.2)
    sig = A.normalize(sig, peak_db=-6.5)
    return A.stereo_haas(sig, delay_ms=11, side_mix=0.4)


def make_hi06_dust_and_debris():
    """A short textured movement suitable for an archaeological reveal."""
    dur = 0.6
    sig = A.highpass(A.white_noise(dur, seed=8), cutoff=800) * A.adsr(
        dur, attack=0.02, decay=0.2, sustain_level=0.1, release=0.3)
    sig = A.lowpass(sig, cutoff=5000)
    sig = A.normalize(sig, peak_db=-8)
    return A.stereo_haas(sig, delay_ms=12, side_mix=0.5)


def make_hi07_historical_transition():
    """A cinematic transition between different eras or historical
    scenes."""
    dur = 1.6
    noise = A.white_noise(dur, seed=9)
    sweep = A.time_varying_bandpass(noise, f_start=250, f_end=2800, bw_oct=1.3, n_blocks=44)
    tone = A.exp_pitch_sweep(180, 70, dur) * 0.3
    sig = sweep * 0.6 + tone
    sig = A.synth_reverb(sig, decay=1.8, wet=0.28)
    sig = A.fade_edges(sig, fade_in=0.02, fade_out=0.3)
    sig = A.normalize(sig, peak_db=-6.5)
    return A.stereo_haas(sig, delay_ms=15, side_mix=0.5)
