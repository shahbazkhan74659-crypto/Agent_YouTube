"""
CATEGORY D - Mythology & legendary worlds (7 tracks, MUS_MY01-07).
Treated as distinct bodies of story, not interchangeable fantasy tropes -
each track is a different structural idea (emergence from silence, awe,
hollow dread, rhythmic resolve, chaos resolving into order, enigmatic
rediscovery, controlled collapse), built from the same synthesis primitives
as everything else in this library (no claim of authentic traditional
instrument recordings - these are original procedural textures).
"""

import numpy as np
import audio_lib as A
import composition as C
import helpers as H

SR = A.SR


def make_my01_creation_of_the_cosmos():
    """Creation myths, primordial beginnings. Deep evolving drone emerging
    gradually from near-silence into a full, expansive texture - the
    emergence itself is the whole arrangement."""
    loop_dur, xfade = 30.0, 3.0
    total = loop_dur + xfade
    root = 61.74  # B1

    sub = A.lowpass(A.vibrato_sine(root, total, rate_hz=0.04, depth_cents=7), SR, cutoff=130)
    overtone = H.stereo_pad_pair(total, freqs=[root * 3, root * 5], detune_voices=3, spread_cents=10,
                                  seed_l=1, seed_r=2)
    emergence = A.envelope_from_breakpoints(total, SR, [(0, 0.0), (10, 0.3), (22, 1.0), (30, 0.8)])

    env = emergence
    layers = [(sub, 1.0, 0.0), (overtone, 0.4, 0.0)]
    return C.render_bed(layers, total, loop_dur=loop_dur, xfade=xfade, envelope=env,
                         reverb=dict(decay=3.6, wet=0.4), peak_db=-6.5)


def make_my02_the_gods_among_mortals():
    """Divine figures, supernatural encounters. Grand but restrained pad,
    resonant bell-like tones, an atmosphere of awe rather than bombast -
    Lydian, wide and bright without percussion."""
    loop_dur, xfade = 26.0, 2.5
    total = loop_dur + xfade
    root = 130.81  # C3
    notes = A.modal_notes(root, "lydian", octaves=2)
    n = int(SR * total)

    pad = H.stereo_pad_pair(total, freqs=notes[:3], detune_voices=4, spread_cents=11, seed_l=10, seed_r=11)
    resonant = H.scatter_events(n, SR,
                                 lambda f, d, sr, amp: A.inharmonic_hit(f, d, sr, partials=[1, 2.0, 2.76, 4.0],
                                                                        decays=[1.8, 2.4, 3.2, 4.0],
                                                                        noise_transient=0.1) * amp,
                                 notes[4:7], events_per_loop=6, seed=12, amp=0.3, dur_each=4.0)

    env = A.envelope_from_breakpoints(total, SR, [(0, 0.55), (13, 0.85), (26, 0.55)])
    layers = [(pad, 0.55, 0.0), (resonant, 1.0, 0.0)]
    return C.render_bed(layers, total, loop_dur=loop_dur, xfade=xfade, envelope=env,
                         reverb=dict(decay=3.2, wet=0.36), peak_db=-6.5)


def make_my03_the_underworld():
    """Journeys to the realm of the dead, afterlife narratives. Dark
    drones, hollow resonances (narrow bandpass, not a full pad), sparse
    percussion, unsettling spatial depth."""
    loop_dur, xfade = 24.0, 2.0
    total = loop_dur + xfade
    root = 55.0  # A1

    dark = A.lowpass(A.vibrato_sine(root, total, rate_hz=0.05, depth_cents=9), SR, cutoff=110)
    hollow = A.bandpass(A.white_noise(total, seed=20), SR, center=700, bw_oct=0.5) * 0.25
    n = int(SR * total)
    distant_hits = H.scatter_events(n, SR,
                                     lambda f, d, sr, amp: A.inharmonic_hit(f, d, sr, partials=[1, 1.9, 3.3],
                                                                            decays=[2.0, 2.8, 3.6],
                                                                            noise_transient=0.3) * amp,
                                     [root * 2, root * 2.2], events_per_loop=5, seed=21, amp=0.3, dur_each=3.0)

    env = A.envelope_from_breakpoints(total, SR, [(0, 0.6), (12, 0.8), (24, 0.6)])
    layers = [(dark, 1.0, 0.0), (hollow, 1.0, 0.0), (distant_hits, 1.0, 0.0)]
    return C.render_bed(layers, total, loop_dur=loop_dur, xfade=xfade, envelope=env,
                         reverb=dict(decay=3.8, wet=0.42), peak_db=-7.0)


def make_my04_the_heros_journey():
    """Legendary heroes, trials, transformation, quests. A motif that
    rhythmically develops - starts as a plain pulse, gains percussion
    layers and a countermelody as the loop progresses - determination
    without a generic superhero swell."""
    loop_dur, xfade = 26.0, 2.5
    total = loop_dur + xfade
    root = 174.61  # F3
    notes = A.modal_notes(root, "mixolydian", octaves=2)
    n = int(SR * total)

    pulse = H.sub_pulse(n, SR, interval_sec=1.0, amp=0.1, f_start=110, f_end=55, thump_dur=0.2)
    n_steps = 52
    perc_pattern = [1.0 if (i % 8 == 0) else (0.5 if i % 4 == 0 else 0.0) for i in range(n_steps)]
    perc = A.rhythm_pattern(A.noise_perc, perc_pattern, step_dur=total / n_steps, n_steps=n_steps,
                             band="mid", decay=12)
    counter = H.scatter_events(n, SR, H.pluck, notes[3:7], events_per_loop=14, seed=30, amp=0.25, dur_each=1.3)

    env = A.envelope_from_breakpoints(total, SR, [(0, 0.5), (14, 0.9), (26, 0.6)])
    layers = [(pulse, 1.0, 0.0), (perc, 0.8, 0.1), (counter, 1.0, -0.1)]
    return C.render_bed(layers, total, loop_dur=loop_dur, xfade=xfade, envelope=env,
                         reverb=dict(decay=1.8, wet=0.22), peak_db=-6.0)


def make_my05_primordial_chaos():
    """Creation from chaos, cosmic conflict, primordial forces. Begins as
    unstable filtered noise with irregular pulses; a pitched layer fades in
    only in the second half, so structure visibly emerges from chaos."""
    loop_dur, xfade = 24.0, 2.0
    total = loop_dur + xfade
    root = 98.0  # G2

    chaos = A.time_varying_bandpass(A.white_noise(total, seed=40), f_start=120, f_end=3800,
                                     bw_oct=1.8, n_blocks=64) * 0.35
    n_steps = 48
    irregular = H.irregular_pattern(n_steps, seed=41, density=0.5, min_strength=0.3)
    pulses = A.rhythm_pattern(A.noise_perc, irregular, step_dur=total / n_steps, n_steps=n_steps,
                               band="mid", decay=10)
    order = H.stereo_pad_pair(total, freqs=A.modal_notes(root, "whole_tone", octaves=1)[:3],
                               detune_voices=3, spread_cents=9, seed_l=42, seed_r=43)
    order_env = A.envelope_from_breakpoints(total, SR, [(0, 0.0), (12, 0.0), (22, 1.0), (26, 0.9)])[:, None]

    env = A.envelope_from_breakpoints(total, SR, [(0, 0.7), (12, 0.55), (24, 0.8)])
    layers = [(chaos, 1.0, 0.0), (pulses, 0.8, 0.0), (order * order_env, 0.4, 0.0)]
    return C.render_bed(layers, total, loop_dur=loop_dur, xfade=xfade, envelope=env,
                         reverb=dict(decay=2.4, wet=0.3), peak_db=-6.5)


def make_my06_forgotten_pantheons():
    """Lesser-known gods, forgotten traditions. Enigmatic modal melody with
    a distinctive FM-colored timbre (not a plain pad/pluck) - Phrygian,
    deliberately a little alien."""
    loop_dur, xfade = 24.0, 2.0
    total = loop_dur + xfade
    root = 146.83  # D3
    notes = A.modal_notes(root, "phrygian", octaves=2)
    n = int(SR * total)

    def fm_note(f, d, sr, amp):
        sig = A.fm_tone(f, d, sr=sr, mod_ratio=1.5, mod_index=1.8) * A.adsr(
            d, sr, attack=0.02, decay=0.3, sustain_level=0.4, release=d * 0.5)
        return sig * amp

    melody = H.scatter_events(n, SR, fm_note, notes[1:6], events_per_loop=13, seed=50, amp=0.26, dur_each=1.6)
    base = A.lowpass(A.pad_voice([root / 2], total, detune_voices=2, spread_cents=6, seed=51), SR, cutoff=500) * 0.25
    base = np.stack([base, base], axis=1)

    env = A.envelope_from_breakpoints(total, SR, [(0, 0.55), (12, 0.85), (24, 0.55)])
    layers = [(melody, 1.0, 0.0), (base, 1.0, 0.0)]
    return C.render_bed(layers, total, loop_dur=loop_dur, xfade=xfade, envelope=env,
                         reverb=dict(decay=2.6, wet=0.3), peak_db=-6.5)


def make_my07_the_fall_of_the_gods():
    """Divine conflict, collapse of mythological orders, the end of
    legendary ages. Building harmonic tension and percussion toward a
    controlled climax within the loop, then settling unresolved - dark
    cinematic movement."""
    loop_dur, xfade = 28.0, 2.5
    total = loop_dur + xfade
    root = 82.41  # E2
    clash = root * (2 ** (1 / 12))

    drone = H.stereo_pad_pair(total, freqs=[root, clash], detune_voices=4, spread_cents=12, seed_l=60, seed_r=61)
    n_steps = 56
    build_pattern = [min(1.0, 0.15 + i / n_steps) if i % 4 == 0 else 0.0 for i in range(n_steps)]
    build_perc = A.rhythm_pattern(A.kick, build_pattern, step_dur=total / n_steps, n_steps=n_steps,
                                   f_start=120, f_end=35)
    n = int(SR * total)
    climax = A.inharmonic_hit(root, 2.5, SR, partials=[1, 1.9, 3.2, 4.5], decays=[1.5, 2.0, 2.8, 3.5],
                               noise_transient=0.5, seed=62)
    climax_buf = np.zeros(n)
    start = int(22.0 * SR)
    climax_buf[start:start + len(climax)] += climax[: max(0, n - start)] * 0.5

    env = A.envelope_from_breakpoints(total, SR, [(0, 0.5), (21.5, 0.9), (22.0, 1.3), (28, 0.55)])
    layers = [(drone, 0.5, 0.0), (build_perc, 0.9, 0.0), (climax_buf, 1.0, 0.0)]
    return C.render_bed(layers, total, loop_dur=loop_dur, xfade=xfade, envelope=env,
                         reverb=dict(decay=3.0, wet=0.34), peak_db=-6.0)
