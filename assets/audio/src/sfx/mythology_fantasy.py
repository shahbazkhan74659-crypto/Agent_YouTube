"""
CATEGORY E - Mythology & fantasy worlds SFX (7 one-shots, SFX_MY01-07).
Original procedural sound design, not a claim about the sounds of actual
gods, rituals, or supernatural events. Each effect uses a different
technique on purpose - not the same magical shimmer seven times.
"""

import numpy as np
import audio_lib as A


def make_my01_primordial_awakening():
    """A deep, evolving sound suggesting the beginning of a legendary
    world."""
    dur = 3.0
    sig = A.lowpass(A.vibrato_sine(50, dur, rate_hz=0.1, depth_cents=15), cutoff=110)
    sig = sig * A.adsr(dur, attack=1.2, decay=0.5, sustain_level=0.7, release=1.0)
    sig = A.synth_reverb(sig, decay=2.6, wet=0.34)
    sig = A.normalize(sig, peak_db=-6.5)
    return A.stereo_haas(sig, delay_ms=22, side_mix=0.5)


def make_my02_divine_presence():
    """A resonant, expansive tonal effect suggesting an extraordinary
    presence."""
    dur = 2.2
    sig = A.inharmonic_hit(220, dur, partials=[1, 2.0, 2.76, 4.0, 5.0], decays=[1.5, 2.0, 2.6, 3.2, 3.8],
                            noise_transient=0.1, seed=1)
    sig = A.synth_reverb(sig, decay=2.4, wet=0.36)
    sig = A.fade_edges(sig, fade_in=0.01, fade_out=0.5)
    sig = A.normalize(sig, peak_db=-6)
    return A.stereo_haas(sig, delay_ms=18, side_mix=0.5)


def make_my03_mythic_energy():
    """A layered synthetic effect for supernatural or legendary events."""
    dur = 1.4
    fm = A.fm_tone(330, dur, mod_ratio=1.5, mod_index=2.5) * 0.4
    am = A.am_tone(330, dur, mod_freq=6.0, depth=0.7) * 0.3
    sig = (fm + am) * A.adsr(dur, attack=0.1, decay=0.3, sustain_level=0.5, release=0.6)
    sig = A.normalize(sig, peak_db=-7)
    return A.stereo_haas(sig, delay_ms=15, side_mix=0.5)


def make_my04_underworld_gate():
    """A heavy, dark transition with resonant movement."""
    dur = 1.6
    boom = A.exp_pitch_sweep(120, 30, dur) * A.adsr(dur, attack=0.01, decay=0.3, sustain_level=0.3, release=0.9)
    hollow = A.bandpass(A.white_noise(dur, seed=2), center=500, bw_oct=0.6) * 0.3
    sig = boom + hollow
    sig = A.lowpass(sig, cutoff=1200)
    sig = A.synth_reverb(sig, decay=2.2, wet=0.32)
    sig = A.normalize(sig, peak_db=-5.5)
    return A.stereo_haas(sig, delay_ms=12, side_mix=0.4)


def make_my05_ancient_power():
    """A low, evolving tonal texture that grows in intensity."""
    dur = 2.4
    sig = A.lowpass(A.pad_voice([73.42, 87.31], dur, detune_voices=3, spread_cents=10, seed=3), cutoff=300)
    sig = sig * A.adsr(dur, attack=0.8, decay=0.3, sustain_level=0.8, release=0.8)
    sig = A.normalize(sig, peak_db=-7)
    return A.stereo_haas(sig, delay_ms=17, side_mix=0.45)


def make_my06_mythic_transformation():
    """A complex transition combining rising tonal movement and changing
    timbre."""
    dur = 1.8
    rise = A.exp_pitch_sweep(110, 660, dur) * 0.3
    timbre_shift = A.fm_tone(220, dur, mod_ratio=1.0, mod_index=0.5) * np.linspace(0, 1, int(A.SR * dur)) * 0.3
    sig = rise + timbre_shift
    sig = A.fade_edges(sig, fade_in=0.05, fade_out=0.3)
    sig = A.synth_reverb(sig, decay=1.4, wet=0.24)
    sig = A.normalize(sig, peak_db=-6.5)
    return A.stereo_haas(sig, delay_ms=14, side_mix=0.5)


def make_my07_legendary_revelation():
    """A distinctive accent for revealing a mythological figure, location,
    or event."""
    dur = 1.5
    sig = A.inharmonic_hit(293.66, dur, partials=[1, 2.0, 3.0, 4.0], decays=[1.8, 2.4, 3.0, 3.8],
                            noise_transient=0.2, seed=4)
    sig = A.synth_reverb(sig, decay=1.8, wet=0.3)
    sig = A.fade_edges(sig, fade_in=0.004, fade_out=0.4)
    sig = A.normalize(sig, peak_db=-6)
    return A.stereo_haas(sig, delay_ms=16, side_mix=0.5)
