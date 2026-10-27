"""
CATEGORY G - Religion, cosmology & comparative beliefs (5 tracks,
MUS_RC01-05). Analytical and reflective, not devotional or triumphant -
a reflective drone, a cyclic structure, ethereal ambiguity, a documentary-
paced ritual pulse, and three independent voices that coexist without
forcing one resolution.
"""

import numpy as np
import audio_lib as A
import composition as C
import helpers as H

SR = A.SR


def make_rc01_the_sacred_question():
    """Comparative religion, humanity and the cosmos. Reflective drones,
    spacious textures, restrained melodic movement - Dorian, unhurried."""
    loop_dur, xfade = 28.0, 2.5
    total = loop_dur + xfade
    root = 110.0  # A2
    notes = A.modal_notes(root, "dorian", octaves=2)
    n = int(SR * total)

    drone = H.stereo_pad_pair(total, freqs=[root, notes[4]], detune_voices=4, spread_cents=10, seed_l=1, seed_r=2)
    phrase = H.scatter_events(n, SR, H.pluck, notes[3:6], events_per_loop=7, seed=3, amp=0.24, dur_each=3.2)

    env = A.envelope_from_breakpoints(total, SR, [(0, 0.5), (14, 0.75), (28, 0.5)])
    layers = [(drone, 0.5, 0.0), (phrase, 1.0, 0.0)]
    return C.render_bed(layers, total, loop_dur=loop_dur, xfade=xfade, envelope=env,
                         reverb=dict(decay=3.2, wet=0.36), peak_db=-7.0)


def make_rc02_the_cosmic_order():
    """Creation, destruction, cosmic cycles across traditions. A literal
    cyclic rhythm (a steady, slow pattern that repeats exactly, mirroring a
    cosmological cycle) under expansive, slowly evolving harmony."""
    loop_dur, xfade = 24.0, 2.0
    total = loop_dur + xfade
    root = 130.81  # C3
    notes = A.modal_notes(root, "mixolydian", octaves=2)
    n = int(SR * total)

    n_steps = 48
    cycle_pattern = [1.0 if i % 12 == 0 else (0.5 if i % 6 == 0 else 0.0) for i in range(n_steps)]
    cycle = A.rhythm_pattern(A.kick, cycle_pattern, step_dur=total / n_steps, n_steps=n_steps,
                              f_start=110, f_end=50)
    pad = H.stereo_pad_pair(total, freqs=notes[:3], detune_voices=3, spread_cents=9, seed_l=10, seed_r=11)
    shimmer = A.vibrato_sine(notes[6], total, rate_hz=0.1, depth_cents=15) * 0.1

    env = A.envelope_from_breakpoints(total, SR, [(0, 0.5), (12, 0.9), (24, 0.5)])
    layers = [(cycle, 1.0, 0.0), (pad, 0.45, 0.0), (shimmer, 1.0, 0.1)]
    return C.render_bed(layers, total, loop_dur=loop_dur, xfade=xfade, envelope=env,
                         reverb=dict(decay=2.4, wet=0.3), peak_db=-6.5)


def make_rc03_visions_of_the_afterlife():
    """Comparative beliefs about death, rebirth, judgment, what may follow.
    Ethereal textures, slow development, thoughtful ambiguity - no
    percussion, unresolved suspended harmony (no third)."""
    loop_dur, xfade = 28.0, 2.5
    total = loop_dur + xfade
    root = 174.61  # F3

    suspended = H.stereo_pad_pair(total, freqs=[root, root * (2 ** (5 / 12)), root * (2 ** (7 / 12))],
                                   detune_voices=3, spread_cents=8, seed_l=20, seed_r=21)
    ghost = A.vibrato_sine(root * 4, total, rate_hz=0.07, depth_cents=22) * 0.12

    env = A.envelope_from_breakpoints(total, SR, [(0, 0.4), (14, 0.7), (28, 0.4)])
    layers = [(suspended, 0.5, 0.0), (ghost, 1.0, 0.0)]
    return C.render_bed(layers, total, loop_dur=loop_dur, xfade=xfade, envelope=env,
                         reverb=dict(decay=3.6, wet=0.4), peak_db=-7.5)


def make_rc04_the_origins_of_belief():
    """Ancient rituals, religious history, symbolic systems. Restrained
    ritual percussion, evolving drones, a documentary-paced atmosphere -
    steadier and more grounded than RC01's reflective stillness."""
    loop_dur, xfade = 26.0, 2.5
    total = loop_dur + xfade
    root = 98.0  # G2
    notes = A.modal_notes(root, "aeolian", octaves=2)
    n = int(SR * total)

    drone = A.lowpass(A.vibrato_sine(root, total, rate_hz=0.05, depth_cents=8), SR, cutoff=180)
    drone = np.stack([drone, drone], axis=1)
    n_steps = 52
    ritual_pattern = [1.0 if i % 8 in (0, 3) else 0.0 for i in range(n_steps)]
    ritual = A.rhythm_pattern(A.noise_perc, ritual_pattern, step_dur=total / n_steps, n_steps=n_steps,
                               band="low", decay=8)
    overlay = H.scatter_events(n, SR, H.pluck, notes[3:6], events_per_loop=6, seed=30, amp=0.22, dur_each=2.6)

    env = A.envelope_from_breakpoints(total, SR, [(0, 0.55), (13, 0.8), (26, 0.55)])
    layers = [(drone, 1.0, 0.0), (ritual, 0.85, 0.0), (overlay, 1.0, 0.0)]
    return C.render_bed(layers, total, loop_dur=loop_dur, xfade=xfade, envelope=env,
                         reverb=dict(decay=2.8, wet=0.32), peak_db=-6.5)


def make_rc05_many_paths_one_question():
    """Comparing different traditions' answers to the same enduring
    question. Three independent melodic voices, in three different modes
    built on three unrelated roots, coexisting in the mix without ever
    forcing a single shared resolution."""
    loop_dur, xfade = 26.0, 2.5
    total = loop_dur + xfade
    n = int(SR * total)

    voice1 = H.scatter_events(n, SR, H.pluck, A.modal_notes(146.83, "aeolian", octaves=1)[:3],
                               events_per_loop=7, seed=40, amp=0.22, dur_each=2.4)
    voice2 = H.scatter_events(n, SR, H.pluck, A.modal_notes(174.61, "mixolydian", octaves=1)[:3],
                               events_per_loop=7, seed=41, amp=0.22, dur_each=2.4)
    voice3 = H.scatter_events(n, SR, H.pluck, A.modal_notes(220.0, "phrygian", octaves=1)[:3],
                               events_per_loop=7, seed=42, amp=0.22, dur_each=2.4)
    bed = A.lowpass(A.white_noise(total, seed=43), SR, cutoff=200) * 0.05
    bed = np.stack([bed, bed], axis=1)

    env = A.envelope_from_breakpoints(total, SR, [(0, 0.55), (13, 0.8), (26, 0.55)])
    layers = [(voice1, 1.0, -0.3), (voice2, 1.0, 0.0), (voice3, 1.0, 0.3), (bed, 1.0, 0.0)]
    return C.render_bed(layers, total, loop_dur=loop_dur, xfade=xfade, envelope=env,
                         reverb=dict(decay=3.0, wet=0.34), peak_db=-7.0)
