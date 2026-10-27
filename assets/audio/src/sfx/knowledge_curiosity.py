"""
CATEGORY F - Knowledge & curiosity SFX (7 one-shots, SFX_KN01-07). Avoids
the familiar video-game reward-chime cliche - restrained and a little
more sophisticated.
"""

import numpy as np
import audio_lib as A


def make_kn01_curiosity_ping():
    """A subtle, sophisticated tonal accent."""
    dur = 0.4
    sig = A.sine(1040, dur) * A.adsr(dur, attack=0.004, decay=0.1, sustain_level=0.1, release=0.2)
    sig = A.normalize(sig, peak_db=-8)
    return A.stereo_haas(sig, delay_ms=6, side_mix=0.35)


def make_kn02_interesting_fact():
    """A short, memorable accent suitable for a surprising fact."""
    dur = 0.6
    sig = A.inharmonic_hit(698.46, dur, partials=[1, 2.0, 2.76], decays=[2.6, 3.2, 4.0], noise_transient=0.1, seed=1)
    sig = A.fade_edges(sig, fade_in=0.002, fade_out=0.2)
    sig = A.normalize(sig, peak_db=-7.5)
    return A.stereo_haas(sig, delay_ms=8, side_mix=0.35)


def make_kn03_idea_connection():
    """A small layered effect suggesting two concepts coming together."""
    dur = 0.6
    n = int(A.SR * dur)
    a = A.sine(440, dur) * A.adsr(dur, attack=0.01, decay=0.1, sustain_level=0.2, release=0.3)
    b = np.concatenate([np.zeros(int(A.SR * 0.08)), A.sine(554.37, dur)])[:n] * A.adsr(
        dur, attack=0.01, decay=0.1, sustain_level=0.2, release=0.3)
    sig = (a + b) * 0.5
    sig = A.normalize(sig, peak_db=-7.5)
    return A.stereo_haas(sig, delay_ms=10, side_mix=0.4)


def make_kn04_discovery_chime():
    """A distinctive but restrained chime - the SOLID-confidence claim-
    reveal alternative sound in this category."""
    dur = 1.0
    sig = A.inharmonic_hit(880, dur, partials=[1, 2.0, 2.76, 3.0], decays=[2.2, 3.0, 4.0, 4.5], seed=2)
    sig = A.fade_edges(sig, fade_in=0.002, fade_out=0.3)
    sig = A.synth_reverb(sig, decay=1.2, wet=0.26)
    sig = A.normalize(sig, peak_db=-7)
    return A.stereo_haas(sig, delay_ms=9, side_mix=0.4)


def make_kn05_concept_transition():
    """A smooth, short transition between explanatory sections."""
    dur = 0.5
    noise = A.white_noise(dur, seed=3)
    sig = A.time_varying_bandpass(noise, f_start=500, f_end=2200, bw_oct=1.0, n_blocks=24)
    sig = sig * A.adsr(dur, attack=0.02, decay=0.1, sustain_level=0.2, release=0.25)
    sig = A.normalize(sig, peak_db=-8)
    return A.stereo_haas(sig, delay_ms=8, side_mix=0.4)


def make_kn06_unexpected_detail():
    """A quick accent emphasizing an overlooked piece of information."""
    dur = 0.25
    sig = A.fm_tone(1100, dur, mod_ratio=2.0, mod_index=1.0) * A.adsr(
        dur, attack=0.003, decay=0.06, sustain_level=0.1, release=0.1)
    sig = A.normalize(sig, peak_db=-8)
    return A.stereo_haas(sig, delay_ms=5, side_mix=0.3)


def make_kn07_knowledge_unlocked():
    """A compact, satisfying sound for an explanation becoming clear."""
    dur = 0.8
    n = int(A.SR * dur)
    sig = np.zeros(n)
    for i, f in enumerate([523.25, 659.25, 783.99]):
        seg = A.sine(f, 0.2) * A.adsr(0.2, attack=0.003, decay=0.08, sustain_level=0.1, release=0.1)
        start = int(i * 0.07 * A.SR)
        sig[start:start + len(seg)] += seg * 0.4
    sig = A.normalize(sig, peak_db=-7.5)
    return A.stereo_haas(sig, delay_ms=7, side_mix=0.35)
