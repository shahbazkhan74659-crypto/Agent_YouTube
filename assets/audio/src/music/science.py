"""
CATEGORY A - Science & scientific discovery (6 tracks, MUS_SC01-06).
Curious electronic motifs, microscopic precision, cosmic scale, organic
evolutionary change, cognitive/mechanical pulse, and unresolved paradox -
six different synthesis approaches, not one formula re-skinned six times.

Each make_* function returns the rendered stereo signal (float array,
shape [n, 2]) at audio_lib.SR. Writing to disk and naming is the
orchestrator's job (see registry.py / generate.py).
"""

import numpy as np
import audio_lib as A
import composition as C
import helpers as H

SR = A.SR


def make_sc01_the_discovery():
    """Curious electronic motifs, delicate pulses, evolving harmonies,
    controlled excitement. D Lydian, bright plucks over a slowly
    brightening pad."""
    loop_dur, xfade = 20.0, 2.0
    total = loop_dur + xfade
    root = 293.66  # D4
    notes = A.modal_notes(root, "lydian", octaves=2)
    n = int(SR * total)

    pad = H.stereo_pad_pair(total, freqs=[root, notes[2]], detune_voices=2, spread_cents=7, seed_l=1, seed_r=2)
    plucks = H.scatter_events(n, SR, H.pluck, notes[2:], events_per_loop=22, seed=3, amp=0.22, dur_each=1.1)
    pulse = H.sub_pulse(n, SR, interval_sec=1.25, amp=0.06, f_start=120, f_end=70)

    env = A.envelope_from_breakpoints(total, SR, [(0, 0.55), (10, 0.85), (18, 1.0), (22, 0.6)])
    layers = [(pad, 0.5, 0.0), (plucks, 1.0, 0.1), (pulse, 1.0, -0.1)]
    return C.render_bed(layers, total, loop_dur=loop_dur, xfade=xfade, envelope=env,
                         reverb=dict(decay=1.4, wet=0.18), peak_db=-6.5)


def make_sc02_the_universe_within():
    """Physics/atoms/molecular structures. Microscopic rhythmic detail via
    FM/AM tones and granular scatter - a precise, synthetic, non-pad-driven
    texture."""
    loop_dur, xfade = 22.0, 2.0
    total = loop_dur + xfade

    fm_bed = A.fm_tone(220, total, mod_ratio=3.01, mod_index=1.5) * 0.25
    am_bed = A.am_tone(440, total, mod_freq=7.0, depth=0.6) * 0.18
    micro_noise = A.granular_texture(A.white_noise(total, seed=5), grain_ms=25,
                                      density=0.5, jitter_ms=10, seed=6)
    micro_noise = A.bandpass(micro_noise, SR, center=2800, bw_oct=2.0) * 0.3

    pattern = H.irregular_pattern(88, seed=7, density=0.4, min_strength=0.3)
    ticks = A.rhythm_pattern(A.noise_perc, pattern, step_dur=total / 88, n_steps=88, band="high", decay=18)

    env = A.envelope_from_breakpoints(total, SR, [(0, 0.6), (11, 1.0), (22, 0.6), (24, 0.3)])
    layers = [(fm_bed, 1.0, -0.2), (am_bed, 1.0, 0.2), (micro_noise, 1.0, 0.0), (ticks, 0.7, 0.0)]
    return C.render_bed(layers, total, loop_dur=loop_dur, xfade=xfade, envelope=env,
                         reverb=dict(decay=0.9, wet=0.12), peak_db=-6.5)


def make_sc03_cosmic_perspective():
    """Astronomy, galaxies, scale of the universe. Spacious deep drone plus
    a slow ghostly high layer, long reverb, one slow controlled crescendo
    across the whole loop - no percussion."""
    loop_dur, xfade = 30.0, 3.0
    total = loop_dur + xfade
    root = 55.0  # A1

    sub = A.lowpass(A.vibrato_sine(root, total, rate_hz=0.05, depth_cents=8), SR, cutoff=140)
    drone = H.stereo_pad_pair(total, freqs=[root * 2, root * 2 * (2 ** (7 / 12))],
                               detune_voices=4, spread_cents=11, seed_l=10, seed_r=11)
    ghost_l = A.vibrato_sine(root * 16, total, rate_hz=0.09, depth_cents=20)
    ghost_r = A.vibrato_sine(root * 16, total, rate_hz=0.07, depth_cents=18, phase=0.8)
    ghost = np.stack([ghost_l, ghost_r], axis=1) * 0.15

    env = A.envelope_from_breakpoints(total, SR, [(0, 0.35), (15, 0.7), (26, 1.0), (30, 0.6)])
    layers = [(sub, 1.0, 0.0), (drone, 0.5, 0.0), (ghost, 1.0, 0.0)]
    return C.render_bed(layers, total, loop_dur=loop_dur, xfade=xfade, envelope=env,
                         reverb=dict(decay=3.4, wet=0.4), peak_db=-7.0)


def make_sc04_evolutionary_time():
    """Evolution, prehistoric life, change across immense periods. Organic
    low percussion pulse plus a pad whose chord drifts between two scale
    degrees over the loop (a slow mode shift)."""
    loop_dur, xfade = 26.0, 2.0
    total = loop_dur + xfade
    root = 110.0  # A2
    notes_a = A.modal_notes(root, "dorian", octaves=1)[:3]
    notes_b = A.modal_notes(root * (2 ** (2 / 12)), "dorian", octaves=1)[:3]

    pad_a = H.stereo_pad_pair(total, freqs=notes_a, detune_voices=3, spread_cents=10, seed_l=20, seed_r=21)
    pad_b = H.stereo_pad_pair(total, freqs=notes_b, detune_voices=3, spread_cents=10, seed_l=22, seed_r=23)
    morph = A.envelope_from_breakpoints(total, SR, [(0, 1.0), (13, 0.0), (26, 1.0), (28, 1.0)])[:, None]
    pad = pad_a * morph + pad_b * (1 - morph)

    n = int(SR * total)
    perc_pattern = H.irregular_pattern(52, seed=24, density=0.35, min_strength=0.5)
    perc = A.rhythm_pattern(A.noise_perc, perc_pattern, step_dur=total / 52, n_steps=52, band="low", decay=10)
    low_pulse = H.sub_pulse(n, SR, interval_sec=2.6, amp=0.1, f_start=95, f_end=48)

    env = A.envelope_from_breakpoints(total, SR, [(0, 0.5), (13, 0.95), (26, 0.5)])
    layers = [(pad, 0.5, 0.0), (perc, 0.8, 0.0), (low_pulse, 1.0, 0.0)]
    return C.render_bed(layers, total, loop_dur=loop_dur, xfade=xfade, envelope=env,
                         reverb=dict(decay=2.0, wet=0.25), peak_db=-6.5)


def make_sc05_the_human_machine():
    """Neuroscience, biology, cognition. A real rhythmic pulse (kick + hat
    pattern) under AM-bass and FM-stab accents - the one science track
    built around a steady groove."""
    loop_dur, xfade = 20.0, 2.0
    total = loop_dur + xfade
    n_steps = 40
    step = total / n_steps

    kick_pattern = [1.0 if i % 8 in (0, 4) else 0.0 for i in range(n_steps)]
    hat_pattern = [0.5 if i % 2 == 1 else 0.0 for i in range(n_steps)]
    kicks = A.rhythm_pattern(A.kick, kick_pattern, step_dur=step, n_steps=n_steps, f_start=140, f_end=42)
    hats = A.rhythm_pattern(A.noise_perc, hat_pattern, step_dur=step, n_steps=n_steps, band="high", decay=20)

    bass = A.am_tone(130.81, total, mod_freq=0.5, depth=0.3) * 0.22  # C3
    stab_notes = A.modal_notes(261.63, "mixolydian", octaves=1)
    n = int(SR * total)

    def stab_cell(f, d, sr, amp):
        return A.fm_tone(f, d, sr=sr, mod_ratio=2.0, mod_index=2.2) * \
            A.adsr(d, sr, attack=0.005, decay=0.1, sustain_level=0.0, release=0.05) * amp

    stabs = H.scatter_events(n, SR, stab_cell, stab_notes, events_per_loop=14, seed=30, amp=0.3, dur_each=0.3)

    env = A.envelope_from_breakpoints(total, SR, [(0, 0.8), (18, 1.0), (22, 0.6)])
    layers = [(kicks, 1.0, 0.0), (hats, 0.8, 0.2), (bass, 1.0, 0.0), (stabs, 1.0, -0.15)]
    return C.render_bed(layers, total, loop_dur=loop_dur, xfade=xfade, envelope=env,
                         reverb=dict(decay=0.8, wet=0.1), peak_db=-6.0)


def make_sc06_scientific_paradox():
    """Counterintuitive/unresolved. Unstable harmonic movement via a
    tritone clash, fragmented granular motifs, irregular pulses - tension
    that stays intellectually intriguing, not horror-dark."""
    loop_dur, xfade = 24.0, 2.0
    total = loop_dur + xfade
    root = 196.0  # G3
    clash = root * (2 ** (6 / 12))  # tritone

    drone = H.stereo_pad_pair(total, freqs=[root, clash], detune_voices=3, spread_cents=9, seed_l=40, seed_r=41)
    frag_source = A.fm_tone(root * 2, total, mod_ratio=1.41, mod_index=2.0)
    fragments = A.granular_texture(frag_source, grain_ms=60, density=0.3, jitter_ms=40, seed=42) * 0.3

    pattern = H.irregular_pattern(48, seed=43, density=0.45, min_strength=0.4)
    pulses = A.rhythm_pattern(A.noise_perc, pattern, step_dur=total / 48, n_steps=48, band="mid", decay=14)

    env = A.envelope_from_breakpoints(total, SR, [(0, 0.6), (9, 0.4), (16, 0.9), (24, 0.55)])
    layers = [(drone, 0.45, 0.0), (fragments, 1.0, 0.1), (pulses, 0.8, -0.1)]
    return C.render_bed(layers, total, loop_dur=loop_dur, xfade=xfade, envelope=env,
                         reverb=dict(decay=1.8, wet=0.22), peak_db=-7.0)
