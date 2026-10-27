"""
CATEGORY C - Philosophy & existential questions (6 tracks, MUS_PH01-06).
Not reduced to sad piano: restrained piano-like hits, a motif that
transposes as it repeats, a literal structure-vs-freedom duality, intimate
electronic stillness, reflective decay, and deliberate unresolved dissonance.
"""

import numpy as np
import audio_lib as A
import composition as C
import helpers as H

SR = A.SR


def _piano_hit(freq, dur, sr=SR, amp=1.0):
    sig = A.inharmonic_hit(freq, dur, sr, partials=[1, 2.0, 3.0, 4.0], decays=[1.2, 1.8, 2.6, 3.4],
                            noise_transient=0.1, seed=int(freq) % 97)
    return sig * amp


def make_ph01_the_question_of_existence():
    """Existence, being, reality. Minimal piano-like hits, spacious
    textures, slow harmonic movement, deliberate pauses between phrases -
    Aeolian, very sparse."""
    loop_dur, xfade = 24.0, 2.0
    total = loop_dur + xfade
    root = 220.0  # A3
    notes = A.modal_notes(root, "aeolian", octaves=2)
    n = int(SR * total)

    space = H.stereo_pad_pair(total, freqs=[root / 2], detune_voices=2, spread_cents=4, seed_l=1, seed_r=2)
    phrase = H.scatter_events(n, SR, _piano_hit, notes[:5], events_per_loop=7, seed=3, amp=0.3, dur_each=3.5)

    env = A.envelope_from_breakpoints(total, SR, [(0, 0.6), (12, 0.7), (24, 0.6)])
    layers = [(space, 0.3, 0.0), (phrase, 1.0, 0.0)]
    return C.render_bed(layers, total, loop_dur=loop_dur, xfade=xfade, envelope=env,
                         reverb=dict(decay=3.0, wet=0.35), peak_db=-7.5)


def make_ph02_the_infinite_regress():
    """Infinite questions, paradoxes, causality, limits of explanation. A
    short motif that repeats but transposes up a step each cycle within the
    loop - shifting tonal centers, subtly destabilizing."""
    loop_dur, xfade = 24.0, 2.0
    total = loop_dur + xfade
    root = 174.61  # F3
    n = int(SR * total)

    motif_buf = np.zeros(n)
    cycle_dur = total / 4
    for i in range(4):
        step_root = root * (2 ** (i / 12))
        motif_notes = A.modal_notes(step_root, "dorian", octaves=1)[:4]
        t0 = i * cycle_dur
        for j, f in enumerate(motif_notes):
            seg = H.pluck(f, 1.1, SR, amp=0.26, decay=3.5)
            start = int((t0 + j * 0.55) * SR)
            end = min(start + len(seg), n)
            motif_buf[start:end] += seg[: end - start]

    drone = A.lowpass(A.vibrato_sine(root / 2, total, rate_hz=0.1, depth_cents=12), SR, cutoff=400) * 0.15

    env = A.envelope_from_breakpoints(total, SR, [(0, 0.7), (24, 0.7)])
    layers = [(motif_buf, 1.0, 0.0), (drone, 1.0, 0.0)]
    return C.render_bed(layers, total, loop_dur=loop_dur, xfade=xfade, envelope=env,
                         reverb=dict(decay=1.8, wet=0.24), peak_db=-6.5)


def make_ph03_free_will():
    """Choice, determinism, responsibility, human agency. A literal
    dialogue: a steady structured percussion grid against a freer, loosely
    timed melodic line that doesn't line up with it."""
    loop_dur, xfade = 22.0, 2.0
    total = loop_dur + xfade
    root = 196.0  # G3
    notes = A.modal_notes(root, "mixolydian", octaves=2)
    n = int(SR * total)

    n_steps = 44
    grid_pattern = [1.0 if i % 4 == 0 else 0.0 for i in range(n_steps)]
    grid = A.rhythm_pattern(A.noise_perc, grid_pattern, step_dur=total / n_steps, n_steps=n_steps,
                             band="mid", decay=16)
    free_line = H.scatter_events(n, SR, H.pluck, notes[2:6], events_per_loop=12, seed=10, amp=0.28, dur_each=1.8)

    env = A.envelope_from_breakpoints(total, SR, [(0, 0.6), (11, 0.9), (22, 0.6)])
    layers = [(grid, 0.6, -0.15), (free_line, 1.0, 0.15)]
    return C.render_bed(layers, total, loop_dur=loop_dur, xfade=xfade, envelope=env,
                         reverb=dict(decay=1.4, wet=0.2), peak_db=-6.5)


def make_ph04_consciousness():
    """Subjective experience, awareness, identity. Intimate electronic
    textures, delicate harmonic layers, slowly evolving atmosphere - no
    percussion, kept deliberately close/quiet."""
    loop_dur, xfade = 26.0, 2.5
    total = loop_dur + xfade
    root = 164.81  # E3

    inner = A.am_tone(root, total, mod_freq=0.2, depth=0.4) * 0.3
    shimmer = H.stereo_pad_pair(total, freqs=[root * 2, root * 2 * (2 ** (3 / 12))],
                                 detune_voices=3, spread_cents=6, seed_l=20, seed_r=21)
    breath = A.granular_texture(A.white_noise(total, seed=22), grain_ms=200, density=0.1,
                                 jitter_ms=80, seed=23) * 0.08

    env = A.envelope_from_breakpoints(total, SR, [(0, 0.5), (13, 0.75), (26, 0.5)])
    layers = [(inner, 1.0, 0.0), (shimmer, 0.3, 0.0), (breath, 1.0, 0.0)]
    return C.render_bed(layers, total, loop_dur=loop_dur, xfade=xfade, envelope=env,
                         reverb=dict(decay=2.4, wet=0.3), peak_db=-8.0)


def make_ph05_the_weight_of_time():
    """Mortality, impermanence, memory, the passage of time. Reflective
    plucked motifs with long decay, spacious, restrained emotional depth -
    harmonic minor, very few notes."""
    loop_dur, xfade = 26.0, 2.5
    total = loop_dur + xfade
    root = 174.61  # F3
    notes = A.modal_notes(root, "harmonic_minor", octaves=2)
    n = int(SR * total)

    phrase = H.scatter_events(n, SR, lambda f, d, sr, amp: H.pluck(f, d, sr, amp=amp, decay=1.2, cutoff=2600),
                               notes[1:5], events_per_loop=6, seed=30, amp=0.3, dur_each=4.5)
    low_hold = A.lowpass(A.vibrato_sine(root / 2, total, rate_hz=0.04, depth_cents=6), SR, cutoff=300) * 0.18

    env = A.envelope_from_breakpoints(total, SR, [(0, 0.55), (13, 0.7), (26, 0.5)])
    layers = [(phrase, 1.0, 0.0), (low_hold, 1.0, 0.0)]
    return C.render_bed(layers, total, loop_dur=loop_dur, xfade=xfade, envelope=env,
                         reverb=dict(decay=3.4, wet=0.38), peak_db=-7.5)


def make_ph06_the_paradox():
    """Philosophical thought experiments, contradictions. Minimalist
    motifs, unexpected harmonic changes, controlled dissonance, endings
    that never resolve - chromatic fragment against a sustained drone."""
    loop_dur, xfade = 22.0, 2.0
    total = loop_dur + xfade
    root = 207.65  # Ab3
    notes = A.modal_notes(root, "chromatic_fragment", octaves=1)
    n = int(SR * total)

    drone = A.lowpass(A.pad_voice([root], total, detune_voices=2, spread_cents=5, seed=40), SR, cutoff=600) * 0.3
    stereo_drone = np.stack([drone, drone], axis=1)
    motif = H.scatter_events(n, SR, _piano_hit, notes, events_per_loop=10, seed=41, amp=0.26, dur_each=2.0)

    env = A.envelope_from_breakpoints(total, SR, [(0, 0.55), (11, 0.8), (22, 0.55)])
    layers = [(stereo_drone, 1.0, 0.0), (motif, 1.0, 0.0)]
    return C.render_bed(layers, total, loop_dur=loop_dur, xfade=xfade, envelope=env,
                         reverb=dict(decay=2.0, wet=0.26), peak_db=-7.0)
