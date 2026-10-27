"""
CATEGORY D - Mystery & investigation SFX (8 one-shots, SFX_MI01-08).
Built to support curiosity, not loud jump scares.
"""

import numpy as np
import audio_lib as A


def make_mi01_suspense_tick():
    """A subtle, precise pulse suitable for a developing mystery."""
    dur = 0.1
    sig = A.noise_perc(dur, band="high", decay=28, seed=1) * 0.5
    sig = A.normalize(sig, peak_db=-9)
    return A.stereo_haas(sig, delay_ms=4, side_mix=0.3)


def make_mi02_hidden_clue():
    """A small, distinctive accent for revealing an overlooked detail."""
    dur = 0.35
    sig = A.fm_tone(740, dur, mod_ratio=1.5, mod_index=0.9) * A.adsr(
        dur, attack=0.004, decay=0.1, sustain_level=0.1, release=0.15)
    sig = A.normalize(sig, peak_db=-7.5)
    return A.stereo_haas(sig, delay_ms=8, side_mix=0.4)


def make_mi03_mystery_stinger():
    """A short, dark tonal gesture."""
    dur = 0.8
    sig = (A.sine(220, dur) + A.sine(233.08, dur) * 0.7) * A.adsr(
        dur, attack=0.01, decay=0.2, sustain_level=0.3, release=0.4)
    sig = A.lowpass(sig, cutoff=1800)
    sig = A.normalize(sig, peak_db=-7)
    return A.stereo_haas(sig, delay_ms=14, side_mix=0.45)


def make_mi04_evidence_reveal():
    """A controlled transition accent for introducing an important
    discovery."""
    dur = 1.0
    sig = A.inharmonic_hit(330, dur, partials=[1, 1.9, 3.1], decays=[1.8, 2.4, 3.2], noise_transient=0.2, seed=2)
    sig = A.synth_reverb(sig, decay=1.3, wet=0.25)
    sig = A.fade_edges(sig, fade_in=0.003, fade_out=0.25)
    sig = A.normalize(sig, peak_db=-6.5)
    return A.stereo_haas(sig, delay_ms=10, side_mix=0.4)


def make_mi05_ominous_reverse():
    """A reverse-engineered atmospheric swell leading into a scene
    change."""
    dur = 1.8
    sig = A.reverse_riser(dur, seed=3, decay=4.2, cutoff=2600) * 0.4
    sig = A.normalize(sig, peak_db=-6.5)
    return A.stereo_haas(sig, delay_ms=16, side_mix=0.5)


def make_mi06_cryptic_signal():
    """A fragmented, unusual tonal pattern."""
    dur = 0.7
    tone = A.fm_tone(560, dur, mod_ratio=2.41, mod_index=2.2)
    sig = A.granular_texture(tone, grain_ms=30, density=0.45, jitter_ms=25, seed=4)
    sig = A.fade_edges(sig, fade_in=0.01, fade_out=0.1)
    sig = A.normalize(sig, peak_db=-7.5)
    return A.stereo_haas(sig, delay_ms=12, side_mix=0.5)


def make_mi07_unanswered_question():
    """A short effect ending in a suspended or unresolved texture."""
    dur = 1.1
    sig = (A.sine(261.63, dur) + A.sine(392.0, dur) * 0.7) * A.adsr(
        dur, attack=0.03, decay=0.2, sustain_level=0.45, release=0.6)
    sig = A.lowpass(sig, cutoff=3200)
    sig = A.fade_edges(sig, fade_in=0.01, fade_out=0.4)
    sig = A.normalize(sig, peak_db=-7.5)
    return A.stereo_haas(sig, delay_ms=20, side_mix=0.55)


def make_mi08_final_revelation():
    """A memorable but controlled accent for the conclusion of a
    mystery."""
    dur = 1.6
    sig = A.inharmonic_hit(293.66, dur, partials=[1, 2.0, 2.76, 4.0], decays=[2.0, 2.6, 3.4, 4.2],
                            noise_transient=0.25, seed=5)
    sig = A.synth_reverb(sig, decay=1.6, wet=0.3)
    sig = A.fade_edges(sig, fade_in=0.004, fade_out=0.35)
    sig = A.normalize(sig, peak_db=-6)
    return A.stereo_haas(sig, delay_ms=13, side_mix=0.45)
