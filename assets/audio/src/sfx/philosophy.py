"""
CATEGORY C - Philosophy & intellectual revelations SFX (6 one-shots,
SFX_PH01-06). No cartoon lightbulb / cash-register cliches.

SFX_PH04 (Realization) and SFX_PH06 (Unresolved Thought) are the pair that
carries forward this channel's old epistemic-transparency signal (see the
old library's sfx_ding_claim_solid.wav / sfx_tone_uncertain.wav) - use PH04
for a SOLID-confidence claim reveal and PH06 for a CONTESTED/UNCERTAIN one.
"""

import numpy as np
import audio_lib as A


def make_ph01_the_question():
    """A subtle, memorable tonal accent introducing a profound question."""
    dur = 1.0
    sig = (A.sine(392, dur) + A.sine(587.33, dur) * 0.6) * A.adsr(
        dur, attack=0.1, decay=0.3, sustain_level=0.4, release=0.5)
    sig = A.synth_reverb(sig, decay=1.6, wet=0.3)
    sig = A.normalize(sig, peak_db=-7.5)
    return A.stereo_haas(sig, delay_ms=18, side_mix=0.5)


def make_ph02_thought_shift():
    """A short transition suggesting a change in perspective."""
    dur = 0.7
    sig = A.exp_pitch_sweep(440, 330, dur) * A.adsr(dur, attack=0.02, decay=0.2, sustain_level=0.2, release=0.35)
    sig = A.lowpass(sig, cutoff=2500)
    sig = A.normalize(sig, peak_db=-7.5)
    return A.stereo_haas(sig, delay_ms=12, side_mix=0.4)


def make_ph03_paradox_accent():
    """An unusual, unresolved tonal gesture for a philosophical
    contradiction."""
    dur = 1.1
    sig = (A.sine(330, dur) + A.sine(349.23, dur)) * 0.5 * A.adsr(
        dur, attack=0.05, decay=0.3, sustain_level=0.3, release=0.5)
    sig = A.lowpass(sig, cutoff=2800)
    sig = A.normalize(sig, peak_db=-8)
    return A.stereo_haas(sig, delay_ms=22, side_mix=0.55)


def make_ph04_realization():
    """A restrained harmonic accent indicating a conceptual breakthrough -
    the SOLID-confidence claim-reveal sound."""
    dur = 1.2
    sig = A.inharmonic_hit(523.25, dur, partials=[1, 2.0, 3.0], decays=[2.4, 3.0, 3.8],
                            noise_transient=0.1, seed=1)
    sig = A.synth_reverb(sig, decay=1.1, wet=0.24)
    sig = A.fade_edges(sig, fade_in=0.002, fade_out=0.3)
    sig = A.normalize(sig, peak_db=-7)
    return A.stereo_haas(sig, delay_ms=9, side_mix=0.4)


def make_ph05_existential_void():
    """A short, spacious, low-intensity atmospheric effect."""
    dur = 1.8
    sig = A.lowpass(A.vibrato_sine(80, dur, rate_hz=0.1, depth_cents=10), cutoff=160) * A.adsr(
        dur, attack=0.4, decay=0.3, sustain_level=0.5, release=0.9)
    sig = A.synth_reverb(sig, decay=2.0, wet=0.35)
    sig = A.normalize(sig, peak_db=-8.5)
    return A.stereo_haas(sig, delay_ms=20, side_mix=0.5)


def make_ph06_unresolved_thought():
    """A brief dissonant tail that ends without full harmonic resolution -
    the CONTESTED/UNCERTAIN claim-reveal sound."""
    dur = 1.0
    sig = (A.sine(440, dur) + A.sine(452, dur)) * 0.5
    env = A.adsr(dur, attack=0.05, decay=0.2, sustain_level=0.5, release=0.5)
    sig = A.lowpass(sig * env, cutoff=3000)
    sig = A.fade_edges(sig, fade_in=0.02, fade_out=0.3)
    sig = A.normalize(sig, peak_db=-8)
    return A.stereo_haas(sig, delay_ms=20, side_mix=0.6)
