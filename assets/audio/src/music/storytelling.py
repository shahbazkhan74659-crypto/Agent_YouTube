"""
CATEGORY H - General intellectual storytelling (6 tracks, MUS_ST01-06).
Versatile backing beds not tied to one subject - a quick punchy hook, a
deliberately thin narration-friendly bed, a track with a real turn, a
restrained dark-ethics cue, an open-ended ambient closer, and a track whose
opening motif expands into something bigger.
"""

import numpy as np
import audio_lib as A
import composition as C
import helpers as H

SR = A.SR


def make_st01_the_unbelievable_fact():
    """A startling fact that demands immediate attention. Rapid atmospheric
    hook, compact development, one memorable accent - the shortest loop in
    the library, built to grab attention fast."""
    loop_dur, xfade = 16.0, 1.5
    total = loop_dur + xfade
    root = 293.66  # D4
    notes = A.modal_notes(root, "major_pentatonic", octaves=2)
    n = int(SR * total)

    hit = A.inharmonic_hit(root * 2, 1.0, SR, partials=[1, 2.0, 2.76], decays=[2.0, 2.6, 3.4],
                            noise_transient=0.3, seed=1)
    hit_buf = np.zeros(n)
    hit_buf[: len(hit)] += hit * 0.4
    motif = H.scatter_events(n, SR, H.pluck, notes[2:6], events_per_loop=14, seed=2, amp=0.28, dur_each=0.9)
    riser = A.reverse_riser(1.5, SR, seed=3, decay=4.0, cutoff=4000) * 0.2
    riser_buf = np.zeros(n)
    riser_buf[-len(riser):] += riser

    env = A.envelope_from_breakpoints(total, SR, [(0, 1.0), (6, 0.8), (14, 0.9), (16, 0.6)])
    layers = [(hit_buf, 1.0, 0.0), (motif, 1.0, 0.0), (riser_buf, 1.0, 0.0)]
    return C.render_bed(layers, total, loop_dur=loop_dur, xfade=xfade, envelope=env,
                         reverb=dict(decay=1.2, wet=0.16), peak_db=-6.0)


def make_st02_the_deep_dive():
    """A more detailed explanation of a complex topic. Stable, unobtrusive
    rhythmic movement, controlled harmonic development, excellent narration
    space - deliberately the thinnest/quietest mix in the library."""
    loop_dur, xfade = 28.0, 2.5
    total = loop_dur + xfade
    root = 220.0  # A3
    notes = A.modal_notes(root, "dorian", octaves=1)
    n = int(SR * total)

    pad = H.stereo_pad_pair(total, freqs=[root], detune_voices=2, spread_cents=5, seed_l=10, seed_r=11)
    n_steps = 56
    thin_pattern = [0.3 if i % 4 == 0 else 0.0 for i in range(n_steps)]
    pulse = A.rhythm_pattern(A.noise_perc, thin_pattern, step_dur=total / n_steps, n_steps=n_steps,
                              band="mid", decay=20)
    sparse_notes = H.scatter_events(n, SR, H.pluck, notes[2:4], events_per_loop=5, seed=12, amp=0.14, dur_each=2.5)

    env = A.envelope_from_breakpoints(total, SR, [(0, 0.5), (14, 0.6), (28, 0.5)])
    layers = [(pad, 0.3, 0.0), (pulse, 0.4, 0.0), (sparse_notes, 1.0, 0.0)]
    return C.render_bed(layers, total, loop_dur=loop_dur, xfade=xfade, envelope=env,
                         reverb=dict(decay=1.6, wet=0.18), peak_db=-8.0)


def make_st03_the_unexpected_truth():
    """Revealing a fact that overturns an assumption. Understated opening,
    gradual tension, a clear musical turn at a fixed point each loop -
    minor-to-major pivot."""
    loop_dur, xfade = 22.0, 2.0
    total = loop_dur + xfade
    root = 196.0  # G3
    minor_notes = A.modal_notes(root, "aeolian", octaves=1)
    major_notes = A.modal_notes(root, "mixolydian", octaves=1)
    n = int(SR * total)

    minor_pad = H.stereo_pad_pair(total, freqs=minor_notes[:3], detune_voices=3, spread_cents=8,
                                   seed_l=20, seed_r=21)
    major_pad = H.stereo_pad_pair(total, freqs=major_notes[:3], detune_voices=3, spread_cents=8,
                                   seed_l=22, seed_r=23)
    turn = A.envelope_from_breakpoints(total, SR, [(0, 1.0), (14.5, 1.0), (15.0, 0.0), (22, 0.0)])[:, None]
    pad = minor_pad * turn + major_pad * (1 - turn)
    turn_accent = A.inharmonic_hit(root * 2, 1.2, SR, partials=[1, 2.0, 3.0], decays=[1.8, 2.4, 3.2],
                                    noise_transient=0.2, seed=24)
    accent_buf = np.zeros(n)
    start = int(15.0 * SR)
    accent_buf[start:start + len(turn_accent)] += turn_accent[: max(0, n - start)] * 0.35

    env = A.envelope_from_breakpoints(total, SR, [(0, 0.45), (14.5, 0.55), (15.0, 1.0), (22, 0.65)])
    layers = [(pad, 0.5, 0.0), (accent_buf, 1.0, 0.0)]
    return C.render_bed(layers, total, loop_dur=loop_dur, xfade=xfade, envelope=env,
                         reverb=dict(decay=2.0, wet=0.24), peak_db=-6.5)


def make_st04_the_dark_side_of_knowledge():
    """Dangerous discoveries, ethical dilemmas, unintended consequences.
    Restrained tension, darker harmonic movement, measured cinematic
    accents - minor-2nd clash, low and controlled, never bombastic."""
    loop_dur, xfade = 24.0, 2.0
    total = loop_dur + xfade
    root = 87.31  # F2
    clash = root * (2 ** (1 / 12))

    drone = H.stereo_pad_pair(total, freqs=[root, clash], detune_voices=3, spread_cents=9, seed_l=30, seed_r=31)
    n = int(SR * total)
    low_pulse = H.sub_pulse(n, SR, interval_sec=3.0, amp=0.1, f_start=95, f_end=42, thump_dur=0.3)
    grit = A.bandpass(A.white_noise(total, seed=32), SR, center=1800, bw_oct=1.5) * 0.04
    grit = np.stack([grit, grit], axis=1)

    env = A.envelope_from_breakpoints(total, SR, [(0, 0.55), (12, 0.75), (24, 0.55)])
    layers = [(drone, 0.5, 0.0), (low_pulse, 1.0, 0.0), (grit, 1.0, 0.0)]
    return C.render_bed(layers, total, loop_dur=loop_dur, xfade=xfade, envelope=env,
                         reverb=dict(decay=2.4, wet=0.28), peak_db=-6.5)


def make_st05_the_great_unknown():
    """Questions science, philosophy, and history haven't fully resolved.
    Spacious ambient textures, evolving motifs, a deliberately open
    ending - suspended chord, no percussion, the most spacious track in
    this category."""
    loop_dur, xfade = 30.0, 3.0
    total = loop_dur + xfade
    root = 73.42  # D2

    suspended = H.stereo_pad_pair(total, freqs=[root * 2, root * 2 * (2 ** (5 / 12)), root * 2 * (2 ** (7 / 12))],
                                   detune_voices=3, spread_cents=9, seed_l=40, seed_r=41)
    shimmer = A.vibrato_sine(root * 8, total, rate_hz=0.06, depth_cents=18) * 0.12

    env = A.envelope_from_breakpoints(total, SR, [(0, 0.4), (16, 0.7), (30, 0.4)])
    layers = [(suspended, 0.45, 0.0), (shimmer, 1.0, 0.0)]
    return C.render_bed(layers, total, loop_dur=loop_dur, xfade=xfade, envelope=env,
                         reverb=dict(decay=3.4, wet=0.38), peak_db=-7.5)


def make_st06_the_world_reimagined():
    """A fresh perspective on a familiar subject. A distinctive 3-note
    opening motif that, across the loop, expands into a fuller
    arrangement - the opposite arc of ST02's deliberate restraint."""
    loop_dur, xfade = 24.0, 2.0
    total = loop_dur + xfade
    root = 261.63  # C4
    notes = A.modal_notes(root, "lydian", octaves=2)
    n = int(SR * total)

    motif = H.scatter_events(n, SR, H.pluck, notes[:3], events_per_loop=10, seed=50, amp=0.28, dur_each=1.4)
    pad = H.stereo_pad_pair(total, freqs=notes[2:5], detune_voices=3, spread_cents=8, seed_l=51, seed_r=52)
    pad_gate = A.envelope_from_breakpoints(total, SR, [(0, 0.0), (10, 0.0), (18, 1.0), (24, 1.0)])[:, None]
    n_steps = 48
    perc_pattern = [1.0 if i % 6 == 0 else 0.0 for i in range(n_steps)]
    perc = A.rhythm_pattern(A.noise_perc, perc_pattern, step_dur=total / n_steps, n_steps=n_steps,
                             band="mid", decay=14)
    perc_gate = A.envelope_from_breakpoints(total, SR, [(0, 0.0), (10, 0.0), (18, 1.0), (24, 1.0)])

    env = A.envelope_from_breakpoints(total, SR, [(0, 0.55), (10, 0.65), (20, 1.0), (24, 0.7)])
    layers = [(motif, 1.0, 0.0), (pad * pad_gate, 0.4, 0.0), (perc * perc_gate, 0.7, 0.1)]
    return C.render_bed(layers, total, loop_dur=loop_dur, xfade=xfade, envelope=env,
                         reverb=dict(decay=1.8, wet=0.22), peak_db=-6.0)
