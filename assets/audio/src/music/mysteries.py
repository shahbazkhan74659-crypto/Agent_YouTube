"""
CATEGORY E - Mysteries & unanswered questions (7 tracks, MUS_MI01-07).
Deliberately not the same ominous-drone-plus-ticking-clock seven times:
sparse evolving motif, mechanical/archival texture, a motif that approaches
but never reaches resolution, a drifting "unknown signal", restrained
historical unease, an irregular meter, and a convergence that actually
lands (the one mystery track allowed a real resolution).
"""

import numpy as np
import audio_lib as A
import composition as C
import helpers as H

SR = A.SR


def make_mi01_the_unsolved_mystery():
    """General mysteries, missing information. Sparse pulses, restrained
    dissonance, a motif that evolves slowly across the loop rather than
    repeating identically."""
    loop_dur, xfade = 24.0, 2.0
    total = loop_dur + xfade
    root = 185.0  # F#3-ish
    notes = A.modal_notes(root, "whole_tone", octaves=2)
    n = int(SR * total)

    drone = A.lowpass(A.vibrato_sine(root / 2, total, rate_hz=0.08, depth_cents=14), SR, cutoff=350) * 0.3
    drone = np.stack([drone, drone], axis=1)
    motif = H.scatter_events(n, SR, H.pluck, notes[:5], events_per_loop=9, seed=1, amp=0.26, dur_each=2.4)
    ticks = H.sub_pulse(n, SR, interval_sec=2.2, amp=0.05, f_start=90, f_end=60, thump_dur=0.05)

    env = A.envelope_from_breakpoints(total, SR, [(0, 0.5), (12, 0.7), (24, 0.5)])
    layers = [(drone, 1.0, 0.0), (motif, 1.0, 0.0), (ticks, 1.0, 0.0)]
    return C.render_bed(layers, total, loop_dur=loop_dur, xfade=xfade, envelope=env,
                         reverb=dict(decay=2.6, wet=0.3), peak_db=-6.5)


def make_mi02_the_forbidden_archive():
    """Hidden manuscripts, secret records, forgotten knowledge. Subtle
    mechanical textures (delayed clicks), dark resonances, investigative
    movement."""
    loop_dur, xfade = 22.0, 2.0
    total = loop_dur + xfade
    root = 146.83  # D3

    dark = A.bandpass(A.white_noise(total, seed=10), SR, center=350, bw_oct=1.0) * 0.2
    dark = np.stack([dark, dark], axis=1)
    click = A.noise_perc(0.3, SR, band="high", decay=22, seed=11)
    clicks_delayed = A.delay(np.pad(click, (0, int(SR * total) - len(click))), SR, time_ms=420, feedback=0.4,
                              mix=0.5, n_repeats=8) * 0.3
    pad = A.lowpass(A.pad_voice([root], total, detune_voices=2, spread_cents=5, seed=12), SR, cutoff=500) * 0.22
    pad = np.stack([pad, pad], axis=1)

    env = A.envelope_from_breakpoints(total, SR, [(0, 0.55), (11, 0.8), (22, 0.55)])
    layers = [(dark, 1.0, 0.0), (clicks_delayed, 1.0, 0.1), (pad, 1.0, 0.0)]
    return C.render_bed(layers, total, loop_dur=loop_dur, xfade=xfade, envelope=env,
                         reverb=dict(decay=2.2, wet=0.26), peak_db=-6.5)


def make_mi03_the_missing_piece():
    """Investigations where one crucial fact is still unknown. Fragmented
    motifs that gradually approach a meaningful resolution without fully
    reaching it - the phrase always stops one note short."""
    loop_dur, xfade = 22.0, 2.0
    total = loop_dur + xfade
    root = 220.0  # A3
    notes = A.modal_notes(root, "dorian", octaves=1)
    n = int(SR * total)

    phrase_notes = notes[:4]  # deliberately omit the resolving 5th note
    motif = H.scatter_events(n, SR, H.pluck, phrase_notes, events_per_loop=16, seed=20, amp=0.28, dur_each=1.5)
    held = A.lowpass(A.pad_voice([root / 2], total, detune_voices=2, spread_cents=6, seed=21), SR, cutoff=450) * 0.2
    held = np.stack([held, held], axis=1)

    env = A.envelope_from_breakpoints(total, SR, [(0, 0.5), (11, 0.9), (22, 0.5)])
    layers = [(motif, 1.0, 0.0), (held, 1.0, 0.0)]
    return C.render_bed(layers, total, loop_dur=loop_dur, xfade=xfade, envelope=env,
                         reverb=dict(decay=1.9, wet=0.24), peak_db=-6.5)


def make_mi04_the_unexplained_signal():
    """Strange signals, unidentified sounds, unusual scientific
    observations. Electronic pulses, unstable (drifting) frequencies,
    synthetic textures suggesting an unknown source."""
    loop_dur, xfade = 20.0, 2.0
    total = loop_dur + xfade

    signal = A.vibrato_sine(880, total, rate_hz=0.6, depth_cents=60) * 0.2
    signal2 = A.fm_tone(660, total, mod_ratio=2.73, mod_index=2.5) * 0.15
    n_steps = 40
    irregular = H.irregular_pattern(n_steps, seed=30, density=0.35, min_strength=0.4)
    pulses = A.rhythm_pattern(A.noise_perc, irregular, step_dur=total / n_steps, n_steps=n_steps,
                               band="high", decay=24)

    env = A.envelope_from_breakpoints(total, SR, [(0, 0.5), (10, 0.9), (20, 0.5)])
    layers = [(signal, 1.0, -0.2), (signal2, 1.0, 0.2), (pulses, 0.7, 0.0)]
    return C.render_bed(layers, total, loop_dur=loop_dur, xfade=xfade, envelope=env,
                         reverb=dict(decay=1.2, wet=0.16), peak_db=-6.5)


def make_mi05_shadows_of_the_past():
    """Historical mysteries, disputed accounts, forgotten events. Restrained
    pad colors, distant resonances, subtle rhythmic tension - closer to
    MUS_HI02 territory but tonally distinct (Aeolian vs. Phrygian) and
    slightly more rhythmically present."""
    loop_dur, xfade = 24.0, 2.0
    total = loop_dur + xfade
    root = 164.81  # E3
    notes = A.modal_notes(root, "aeolian", octaves=1)
    n = int(SR * total)

    pad = H.stereo_pad_pair(total, freqs=[root, notes[3]], detune_voices=3, spread_cents=8, seed_l=40, seed_r=41)
    perc_pattern = H.irregular_pattern(24, seed=42, density=0.3, min_strength=0.5)
    perc = A.rhythm_pattern(A.noise_perc, perc_pattern, step_dur=total / 24, n_steps=24, band="low", decay=9)
    distant = H.scatter_events(n, SR, H.pluck, notes[2:4], events_per_loop=5, seed=43, amp=0.2, dur_each=3.0)

    env = A.envelope_from_breakpoints(total, SR, [(0, 0.55), (12, 0.75), (24, 0.5)])
    layers = [(pad, 0.5, 0.0), (perc, 0.6, 0.0), (distant, 1.0, 0.1)]
    return C.render_bed(layers, total, loop_dur=loop_dur, xfade=xfade, envelope=env,
                         reverb=dict(decay=2.8, wet=0.32), peak_db=-7.0)


def make_mi06_the_impossible_question():
    """Apparent contradictions, strange coincidences, hard-to-explain
    phenomena. An irregular 5-step grouping (not 4/4), ambiguous tonal
    center (two unrelated roots never resolved against each other)."""
    loop_dur, xfade = 25.0, 2.0  # 25s divides evenly into 5-step groupings
    total = loop_dur + xfade
    root_a, root_b = 196.0, 174.61  # G3 and F3 - unrelated centers
    n = int(SR * total)

    n_steps = 50  # groups of 5
    pattern = [1.0 if i % 5 in (0, 2) else 0.0 for i in range(n_steps)]
    perc = A.rhythm_pattern(A.noise_perc, pattern, step_dur=total / n_steps, n_steps=n_steps, band="mid", decay=14)
    voice_a = H.scatter_events(n, SR, H.pluck, [root_a], events_per_loop=10, seed=50, amp=0.26, dur_each=1.6)
    voice_b = H.scatter_events(n, SR, H.pluck, [root_b], events_per_loop=10, seed=51, amp=0.26, dur_each=1.6)

    env = A.envelope_from_breakpoints(total, SR, [(0, 0.55), (12, 0.8), (25, 0.55)])
    layers = [(perc, 0.7, 0.0), (voice_a, 1.0, -0.25), (voice_b, 1.0, 0.25)]
    return C.render_bed(layers, total, loop_dur=loop_dur, xfade=xfade, envelope=env,
                         reverb=dict(decay=2.0, wet=0.24), peak_db=-6.5)


def make_mi07_the_final_clue():
    """The moment before a mystery becomes understandable. Gradual
    rhythmic convergence (two offset percussion voices drift into phase)
    and an emerging motif - the one mystery track that's allowed to
    actually resolve, with a compact accent near the loop's end."""
    loop_dur, xfade = 20.0, 2.0
    total = loop_dur + xfade
    root = 220.0  # A3
    notes = A.modal_notes(root, "mixolydian", octaves=1)
    n = int(SR * total)

    n_steps = 40
    voice_a = [1.0 if i % 5 == 0 else 0.0 for i in range(n_steps)]
    voice_b = [1.0 if i % 4 == 0 else 0.0 for i in range(n_steps)]  # converges with voice_a near the end
    perc_a = A.rhythm_pattern(A.noise_perc, voice_a, step_dur=total / n_steps, n_steps=n_steps, band="mid", decay=16)
    perc_b = A.rhythm_pattern(A.noise_perc, voice_b, step_dur=total / n_steps, n_steps=n_steps, band="high", decay=18)
    motif = H.scatter_events(n, SR, H.pluck, notes[:4], events_per_loop=10, seed=60, amp=0.26, dur_each=1.4)

    accent = A.inharmonic_hit(root * 2, 1.5, SR, partials=[1, 2.0, 3.0], decays=[2.0, 2.6, 3.4],
                               noise_transient=0.2, seed=61)
    accent_buf = np.zeros(n)
    start = int(17.5 * SR)
    accent_buf[start:start + len(accent)] += accent[: max(0, n - start)] * 0.35

    env = A.envelope_from_breakpoints(total, SR, [(0, 0.5), (17.0, 0.75), (17.5, 1.0), (20, 0.6)])
    layers = [(perc_a, 0.7, -0.1), (perc_b, 0.7, 0.1), (motif, 1.0, 0.0), (accent_buf, 1.0, 0.0)]
    return C.render_bed(layers, total, loop_dur=loop_dur, xfade=xfade, envelope=env,
                         reverb=dict(decay=1.6, wet=0.2), peak_db=-6.0)
