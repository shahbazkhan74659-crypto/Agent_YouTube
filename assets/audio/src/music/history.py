"""
CATEGORY B - History & ancient civilizations (7 tracks, MUS_HI01-07).

Revision note (2026-10-25, post-listen fix): the original version of this
file leaned on one skeleton for nearly every track (stereo pad/drone +
H.scatter_events(H.pluck, ...) melody + a sparse noise_perc/irregular
percussion layer), varying mainly root/mode/density - closer to re-skinning
one formula than genuinely distinct compositions, and the result read as
both too similar and (for the sparse-transient tracks specifically) too
quiet. Every track below now leads with a different primitive from
audio_lib.py (inharmonic "toll" accents, bandpass-filtered hollow noise,
kick-driven build, FM-tone melody, granular/AM stutter, granular grit,
saturation-as-decline), and every render_bed() call passes target_lufs so
loudness is consistent across the folder instead of swinging ~9 LU between
tracks with sparse vs. continuous content at the "same" peak_db.
"""

import numpy as np
import audio_lib as A
import composition as C
import helpers as H

SR = A.SR


def make_hi01_echoes_of_antiquity():
    """Solemn melodic fragments, resonant drones, measured percussion,
    historical distance. A Aeolian. Lead voice: inharmonic "tolling bell"
    accents instead of plain plucks."""
    loop_dur, xfade = 28.0, 2.5
    total = loop_dur + xfade
    root = 110.0  # A2
    notes = A.modal_notes(root, "aeolian", octaves=2)
    n = int(SR * total)

    drone = H.stereo_pad_pair(total, freqs=[root, notes[4]], detune_voices=4, spread_cents=10, seed_l=1, seed_r=2)

    def toll(f, d, sr, amp):
        return A.inharmonic_hit(f, d, sr=sr, partials=[1, 2.0, 2.76, 4.0], decays=[1.6, 2.2, 3.0, 3.8],
                                 noise_transient=0.12, seed=int(f) % 97) * amp

    tolls = H.scatter_events(n, SR, toll, notes[3:6], events_per_loop=7, seed=3, amp=0.32, dur_each=3.0)
    perc_pattern = H.irregular_pattern(28, seed=4, density=0.3, min_strength=0.6)
    perc = A.rhythm_pattern(A.noise_perc, perc_pattern, step_dur=total / 28, n_steps=28, band="low", decay=8)

    env = A.envelope_from_breakpoints(total, SR, [(0, 0.6), (14, 0.9), (28, 0.6)])
    layers = [(drone, 0.55, 0.0), (tolls, 1.0, 0.0), (perc, 0.75, 0.0)]
    return C.render_bed(layers, total, loop_dur=loop_dur, xfade=xfade, envelope=env,
                         reverb=dict(decay=2.8, wet=0.3), peak_db=-3.0, target_lufs=-15.0,
                         pre_limit_drive=1.8)


def make_hi02_the_lost_civilization():
    """Archaeological mysteries, abandoned cities, forgotten societies.
    Lead voice: a bandpass-filtered "hollow" noise texture (not a pad) -
    sparse distant inharmonic hits, phrases that never quite resolve."""
    loop_dur, xfade = 26.0, 2.5
    total = loop_dur + xfade
    root = 130.81  # C3
    notes = A.modal_notes(root, "phrygian", octaves=2)
    n = int(SR * total)

    hollow = A.bandpass(A.white_noise(total, seed=10), SR, center=550, bw_oct=0.6) * 0.32
    hollow = np.stack([hollow, hollow], axis=1)
    distant_pad = H.stereo_pad_pair(total, freqs=[root], detune_voices=2, spread_cents=5, seed_l=11, seed_r=12)

    def distant_hit(f, d, sr, amp):
        return A.inharmonic_hit(f, d, sr=sr, partials=[1, 1.9, 3.1], decays=[2.0, 2.6, 3.4],
                                 noise_transient=0.2, seed=int(f) % 97) * amp

    sparse_hits = H.scatter_events(n, SR, distant_hit, notes[2:5], events_per_loop=5, seed=13, amp=0.28, dur_each=3.0)

    env = A.envelope_from_breakpoints(total, SR, [(0, 0.55), (13, 0.8), (26, 0.55)])
    layers = [(hollow, 1.0, 0.0), (distant_pad, 0.35, 0.0), (sparse_hits, 1.0, 0.1)]
    return C.render_bed(layers, total, loop_dur=loop_dur, xfade=xfade, envelope=env,
                         reverb=dict(decay=4.0, wet=0.4), peak_db=-5.0, target_lufs=-16.0)


def make_hi03_rise_and_fall_of_empires():
    """Imperial expansion, conquest, collapse. A real building arc: pad
    density and kick-driven percussion both grow across the loop, then
    pull back - already the most structurally distinct history track;
    kept, just re-leveled so it's no longer a loudness outlier."""
    loop_dur, xfade = 30.0, 3.0
    total = loop_dur + xfade
    root = 146.83  # D3
    notes = A.modal_notes(root, "dorian", octaves=2)

    pad = H.stereo_pad_pair(total, freqs=notes[:3], detune_voices=3, spread_cents=9, seed_l=20, seed_r=21)
    pad_high = H.stereo_pad_pair(total, freqs=notes[4:7], detune_voices=3, spread_cents=9, seed_l=22, seed_r=23)

    n_steps = 60
    step = total / n_steps
    density_pattern = [1.0 if (i % max(1, 12 - i // 6) == 0) else 0.0 for i in range(n_steps)]
    kicks = A.rhythm_pattern(A.kick, density_pattern, step_dur=step, n_steps=n_steps, f_start=130, f_end=38)

    env = A.envelope_from_breakpoints(total, SR, [(0, 0.4), (18, 1.0), (24, 0.95), (30, 0.5)])
    pad_high_mix = A.envelope_from_breakpoints(total, SR, [(0, 0.0), (18, 1.0), (30, 0.6)])[:, None]
    layers = [(pad, 0.5, 0.0), (pad_high * pad_high_mix, 0.3, 0.1), (kicks, 1.0, 0.0)]
    return C.render_bed(layers, total, loop_dur=loop_dur, xfade=xfade, envelope=env,
                         reverb=dict(decay=2.2, wet=0.26), peak_db=-3.0, target_lufs=-15.0,
                         pre_limit_drive=2.2)


def make_hi04_ancient_knowledge():
    """Ancient manuscripts, mathematics, astronomy, architecture. Lead
    voice: an FM-tone-colored melody (precise/intellectual timbre) instead
    of a plain pluck - Lydian, still reflective."""
    loop_dur, xfade = 22.0, 2.0
    total = loop_dur + xfade
    root = 220.0  # A3
    notes = A.modal_notes(root, "lydian", octaves=2)
    n = int(SR * total)

    def fm_note(f, d, sr, amp):
        sig = A.fm_tone(f, d, sr=sr, mod_ratio=2.0, mod_index=1.2) * A.adsr(
            d, sr, attack=0.02, decay=0.25, sustain_level=0.35, release=d * 0.4)
        return sig * amp

    melody = H.scatter_events(n, SR, fm_note, notes[1:6], events_per_loop=18, seed=30, amp=0.28, dur_each=1.3)
    shimmer = H.stereo_pad_pair(total, freqs=[notes[6]], detune_voices=2, spread_cents=5, seed_l=31, seed_r=32)
    perc_pattern = H.irregular_pattern(44, seed=33, density=0.25, min_strength=0.4)
    perc = A.rhythm_pattern(A.noise_perc, perc_pattern, step_dur=total / 44, n_steps=44, band="mid", decay=16)

    env = A.envelope_from_breakpoints(total, SR, [(0, 0.6), (11, 0.9), (22, 0.6)])
    layers = [(melody, 1.0, 0.0), (shimmer, 0.2, 0.0), (perc, 0.6, 0.15)]
    return C.render_bed(layers, total, loop_dur=loop_dur, xfade=xfade, envelope=env,
                         reverb=dict(decay=1.6, wet=0.22), peak_db=-3.0, target_lufs=-15.0,
                         pre_limit_drive=1.6)


def make_hi05_the_historical_revelation():
    """Historical facts that challenge familiar narratives. Lead voice: a
    continuously-present granular/AM stutter carrying the tension (not
    near-silent ticks plus one isolated hit - that was this track's
    quietest-outlier problem) building into a concise accent each cycle."""
    loop_dur, xfade = 20.0, 2.0
    total = loop_dur + xfade
    root = 196.0  # G3
    clash = root * (2 ** (1 / 12))
    n = int(SR * total)

    tense = H.stereo_pad_pair(total, freqs=[root, clash], detune_voices=3, spread_cents=8, seed_l=40, seed_r=41)
    stutter_source = A.am_tone(root * 2, total, mod_freq=5.0, depth=0.7)
    stutter = A.granular_texture(stutter_source, grain_ms=35, density=0.4, jitter_ms=20, seed=42) * 0.32

    accent = A.inharmonic_hit(root * 2, 2.0, SR, partials=[1, 2.0, 3.0], decays=[1.5, 2.2, 3.0],
                               noise_transient=0.2, seed=43)
    accent_buf = np.zeros(n)
    start = int(16.5 * SR)
    accent_buf[start:start + len(accent)] += accent[: max(0, n - start)] * 0.4

    env = A.envelope_from_breakpoints(total, SR, [(0, 0.6), (16.0, 0.8), (16.5, 1.0), (20, 0.65)])
    layers = [(tense, 0.45, 0.0), (stutter, 1.0, 0.1), (accent_buf, 1.0, 0.0)]
    return C.render_bed(layers, total, loop_dur=loop_dur, xfade=xfade, envelope=env,
                         reverb=dict(decay=1.5, wet=0.2), peak_db=-3.0, target_lufs=-15.0,
                         pre_limit_drive=2.2)


def make_hi06_before_recorded_time():
    """Prehistory, human origins, early migration, the deep past. Lead
    voice unchanged (single vibrato drone, no pad - already distinct from
    the rest of the folder); added bandpass-filtered granular grit in
    place of plain plucks for a rougher, more "primal" texture."""
    loop_dur, xfade = 28.0, 2.5
    total = loop_dur + xfade
    root = 73.42  # D2
    n = int(SR * total)

    drone = A.lowpass(A.vibrato_sine(root, total, rate_hz=0.06, depth_cents=10), SR, cutoff=150)
    perc_pattern = H.irregular_pattern(28, seed=50, density=0.4, min_strength=0.7)
    perc = A.rhythm_pattern(A.noise_perc, perc_pattern, step_dur=total / 28, n_steps=28, band="low", decay=6)
    grit = A.granular_texture(A.white_noise(total, seed=51), grain_ms=80, density=0.25, jitter_ms=120, seed=52)
    grit = A.bandpass(grit, SR, center=500, bw_oct=1.2) * 0.24

    env = A.envelope_from_breakpoints(total, SR, [(0, 0.55), (14, 0.85), (28, 0.55)])
    layers = [(drone, 1.0, 0.0), (perc, 0.9, 0.0), (grit, 1.0, 0.1)]
    return C.render_bed(layers, total, loop_dur=loop_dur, xfade=xfade, envelope=env,
                         reverb=dict(decay=3.2, wet=0.35), peak_db=-5.0, target_lufs=-15.0)


def make_hi07_the_last_days_of_an_empire():
    """Civilizational collapse, historical tragedy, the end of an era.
    Lead voice: controlled saturation/distortion applied to the drone (a
    decline/decay metaphor) plus mournful inharmonic tolls instead of
    plain plucks - harmonic minor, still a slow, unlifting arc."""
    loop_dur, xfade = 30.0, 3.0
    total = loop_dur + xfade
    root = 97.999  # G2
    notes = A.modal_notes(root, "harmonic_minor", octaves=2)
    n = int(SR * total)

    raw_pad = A.pad_voice(notes[:3], total, detune_voices=4, spread_cents=12, seed=60)
    decayed = A.saturate(raw_pad, drive=2.2) * 0.5
    decayed = np.stack([decayed, decayed], axis=1)
    slow_pulse = H.sub_pulse(n, SR, interval_sec=5.0, amp=0.09, f_start=85, f_end=40, thump_dur=0.4)

    def mournful_toll(f, d, sr, amp):
        return A.inharmonic_hit(f, d, sr=sr, partials=[1, 1.98, 2.76], decays=[2.0, 2.6, 3.4],
                                 noise_transient=0.1, seed=int(f) % 97) * amp

    lament = H.scatter_events(n, SR, mournful_toll, notes[3:5], events_per_loop=4, seed=62, amp=0.28, dur_each=4.0)

    env = A.envelope_from_breakpoints(total, SR, [(0, 0.6), (15, 0.78), (30, 0.6)])
    layers = [(decayed, 0.6, 0.0), (slow_pulse, 1.0, 0.0), (lament, 1.0, 0.0)]
    return C.render_bed(layers, total, loop_dur=loop_dur, xfade=xfade, envelope=env,
                         reverb=dict(decay=3.0, wet=0.32), peak_db=-3.0, target_lufs=-15.0,
                         pre_limit_drive=1.8)
