"""
CATEGORY F - Knowledge, education & curiosity (6 tracks, MUS_KN01-06).
Bright and intelligent, never childish (no xylophone/ukulele-tutorial
cliches): light rhythmic exploration, two interlocking pluck patterns that
resolve into alignment, gradual harmonic expansion, a short distinctive
motif, minimalist electronic repetition, and a clear melodic payoff.
"""

import numpy as np
import audio_lib as A
import composition as C
import helpers as H

SR = A.SR


def make_kn01_the_curiosity_engine():
    """Fascinating facts, general knowledge, surprising observations.
    Bright but sophisticated motifs, light rhythmic movement, a sense of
    exploration - major pentatonic, forward motion."""
    loop_dur, xfade = 20.0, 2.0
    total = loop_dur + xfade
    root = 261.63  # C4
    notes = A.modal_notes(root, "major_pentatonic", octaves=2)
    n = int(SR * total)

    pad = H.stereo_pad_pair(total, freqs=[root], detune_voices=2, spread_cents=6, seed_l=1, seed_r=2)
    motif = H.scatter_events(n, SR, H.pluck, notes[2:7], events_per_loop=20, seed=3, amp=0.24, dur_each=1.0)
    n_steps = 40
    light_pattern = [0.4 if i % 2 == 0 else 0.0 for i in range(n_steps)]
    pulse = A.rhythm_pattern(A.noise_perc, light_pattern, step_dur=total / n_steps, n_steps=n_steps,
                              band="high", decay=22)

    env = A.envelope_from_breakpoints(total, SR, [(0, 0.55), (10, 0.9), (18, 1.0), (22, 0.6)])
    layers = [(pad, 0.3, 0.0), (motif, 1.0, 0.0), (pulse, 0.6, 0.15)]
    return C.render_bed(layers, total, loop_dur=loop_dur, xfade=xfade, envelope=env,
                         reverb=dict(decay=1.3, wet=0.16), peak_db=-6.0)


def make_kn02_the_hidden_connection():
    """Connecting ideas across science, history, philosophy, or culture.
    Two interlocking pluck patterns (different step counts) that only
    align fully once per loop - the structure itself is the metaphor."""
    loop_dur, xfade = 24.0, 2.0
    total = loop_dur + xfade
    root = 220.0  # A3
    notes_a = A.modal_notes(root, "major_pentatonic", octaves=1)
    notes_b = A.modal_notes(root * 1.5, "major_pentatonic", octaves=1)
    n = int(SR * total)

    n_steps = 48
    pattern_a = [1.0 if i % 3 == 0 else 0.0 for i in range(n_steps)]
    pattern_b = [1.0 if i % 4 == 0 else 0.0 for i in range(n_steps)]

    def cell_a(dur, sr, **kw):
        return H.pluck(notes_a[0], dur, sr, amp=0.26, decay=5.0)

    def cell_b(dur, sr, **kw):
        return H.pluck(notes_b[1], dur, sr, amp=0.22, decay=5.0)

    voice_a = A.rhythm_pattern(cell_a, pattern_a, step_dur=total / n_steps, n_steps=n_steps)
    voice_b = A.rhythm_pattern(cell_b, pattern_b, step_dur=total / n_steps, n_steps=n_steps)
    pad = A.lowpass(A.pad_voice([root / 2], total, detune_voices=2, spread_cents=5, seed=10), SR, cutoff=500) * 0.2
    pad = np.stack([pad, pad], axis=1)

    env = A.envelope_from_breakpoints(total, SR, [(0, 0.6), (12, 0.9), (24, 0.6)])
    layers = [(voice_a, 1.0, -0.2), (voice_b, 1.0, 0.2), (pad, 1.0, 0.0)]
    return C.render_bed(layers, total, loop_dur=loop_dur, xfade=xfade, envelope=env,
                         reverb=dict(decay=1.5, wet=0.2), peak_db=-6.0)


def make_kn03_a_mind_awakens():
    """Learning, intellectual growth, discovering a new concept. Gradual
    harmonic expansion (notes added one at a time across the loop),
    subtle rhythmic development, measured optimism - Lydian."""
    loop_dur, xfade = 24.0, 2.0
    total = loop_dur + xfade
    root = 196.0  # G3
    notes = A.modal_notes(root, "lydian", octaves=2)

    layers_sig = np.zeros((int(SR * total), 2))
    chord_notes = notes[:5]
    for i, f in enumerate(chord_notes):
        voice = H.stereo_pad_pair(total, freqs=[f], detune_voices=2, spread_cents=6, seed_l=20 + i, seed_r=30 + i)
        fade_in_t = 2.0 + i * 4.0
        gate = A.envelope_from_breakpoints(total, SR, [(0, 0.0), (fade_in_t, 0.0),
                                                         (fade_in_t + 3, 1.0), (total, 1.0)])[:, None]
        layers_sig += voice * gate * (0.3 / len(chord_notes))

    env = A.envelope_from_breakpoints(total, SR, [(0, 0.7), (24, 1.0)])
    sig = C.render_bed([(layers_sig, 1.0, 0.0)], total, loop_dur=loop_dur, xfade=xfade, envelope=env,
                        reverb=dict(decay=1.8, wet=0.2), peak_db=-6.5)
    return sig


def make_kn04_beyond_common_knowledge():
    """Rare facts, overlooked details, unexpected explanations. A short,
    distinctive 4-note motif with controlled rhythmic variation (the
    rhythm it's played in changes each repeat) and a restrained reveal
    accent at the loop's three-quarter point."""
    loop_dur, xfade = 20.0, 2.0
    total = loop_dur + xfade
    root = 246.94  # B3
    notes = A.modal_notes(root, "major_pentatonic", octaves=1)[:4]
    n = int(SR * total)

    rhythms = [[0.0, 0.4, 0.7, 1.1], [0.0, 0.3, 0.9, 1.3], [0.0, 0.5, 0.6, 1.0]]
    motif = np.zeros(n)
    t_cur = 0.5
    i = 0
    while t_cur < total - 2.0:
        rhythm = rhythms[i % len(rhythms)]
        for j, f in enumerate(notes):
            seg = H.pluck(f, 1.0, SR, amp=0.25, decay=5.0)
            start = int((t_cur + rhythm[j]) * SR)
            end = min(start + len(seg), n)
            if end > start:
                motif[start:end] += seg[: end - start]
        t_cur += 3.2
        i += 1

    reveal = A.inharmonic_hit(root * 2, 1.2, SR, partials=[1, 2.0, 2.76], decays=[2.2, 3.0, 4.0],
                               noise_transient=0.15, seed=40)
    reveal_buf = np.zeros(n)
    start = int(15.0 * SR)
    reveal_buf[start:start + len(reveal)] += reveal[: max(0, n - start)] * 0.3

    env = A.envelope_from_breakpoints(total, SR, [(0, 0.6), (14.5, 0.75), (15.0, 1.0), (20, 0.6)])
    layers = [(motif, 1.0, 0.0), (reveal_buf, 1.0, 0.0)]
    return C.render_bed(layers, total, loop_dur=loop_dur, xfade=xfade, envelope=env,
                         reverb=dict(decay=1.4, wet=0.18), peak_db=-6.0)


def make_kn05_the_thought_experiment():
    """Hypothetical scenarios, logic puzzles, conceptual exploration.
    Minimalist electronic patterns, carefully timed accents, evolving
    repetition - FM-based, no pads at all."""
    loop_dur, xfade = 22.0, 2.0
    total = loop_dur + xfade
    root = 220.0  # A3
    n = int(SR * total)

    def fm_cell(dur, sr, **kw):
        return A.fm_tone(root, dur, sr=sr, mod_ratio=1.0, mod_index=0.8) * A.adsr(
            dur, sr, attack=0.01, decay=0.1, sustain_level=0.2, release=0.1)

    n_steps = 44
    pattern = [1.0 if i % 6 in (0, 3) else (0.4 if i % 6 == 1 else 0.0) for i in range(n_steps)]
    sequence = A.rhythm_pattern(fm_cell, pattern, step_dur=total / n_steps, n_steps=n_steps)
    accent_notes = [root * 2, root * 2 * (2 ** (7 / 12))]
    accents = H.scatter_events(n, SR,
                                lambda f, d, sr, amp: A.fm_tone(f, d, sr=sr, mod_ratio=2.0, mod_index=1.2) *
                                A.adsr(d, sr, attack=0.005, decay=0.15, sustain_level=0.0, release=0.1) * amp,
                                accent_notes, events_per_loop=8, seed=50, amp=0.22, dur_each=0.5)

    env = A.envelope_from_breakpoints(total, SR, [(0, 0.6), (11, 0.9), (22, 0.6)])
    layers = [(sequence, 1.0, 0.0), (accents, 1.0, 0.15)]
    return C.render_bed(layers, total, loop_dur=loop_dur, xfade=xfade, envelope=env,
                         reverb=dict(decay=1.0, wet=0.14), peak_db=-6.0)


def make_kn06_the_joy_of_understanding():
    """Explainers that turn confusion into clarity. Clear melodic
    structure, gentle rhythmic momentum, a positive but restrained sense
    of resolution - major pentatonic, the warmest track in this category."""
    loop_dur, xfade = 20.0, 2.0
    total = loop_dur + xfade
    root = 293.66  # D4
    notes = A.modal_notes(root, "major_pentatonic", octaves=2)
    n = int(SR * total)

    pad = H.stereo_pad_pair(total, freqs=notes[:3], detune_voices=3, spread_cents=8, seed_l=60, seed_r=61)
    melody = H.scatter_events(n, SR, H.pluck, notes[2:6], events_per_loop=16, seed=62, amp=0.24, dur_each=1.3)
    n_steps = 40
    gentle_pattern = [0.5 if i % 4 == 0 else 0.0 for i in range(n_steps)]
    pulse = A.rhythm_pattern(A.noise_perc, gentle_pattern, step_dur=total / n_steps, n_steps=n_steps,
                              band="mid", decay=16)

    env = A.envelope_from_breakpoints(total, SR, [(0, 0.6), (10, 0.95), (18, 1.0), (22, 0.6)])
    layers = [(pad, 0.4, 0.0), (melody, 1.0, 0.0), (pulse, 0.5, -0.1)]
    return C.render_bed(layers, total, loop_dur=loop_dur, xfade=xfade, envelope=env,
                         reverb=dict(decay=1.6, wet=0.2), peak_db=-6.0)
