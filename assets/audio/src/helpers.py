"""
Composition-level helper sounds shared across the music/ and sfx/ category
modules (generalizes the local helpers that used to live inside the old
generate_library.py - pluck, bell, scatter_plucks, sub_pulse, stereo_pad -
so all 15 category files can reuse them instead of each redefining its own).
"""

import numpy as np
import audio_lib as A


def pluck(freq, dur, sr=A.SR, amp=1.0, decay=4.5, cutoff=3500):
    n = int(sr * dur)
    t = np.arange(n) / sr
    sig = np.sin(2 * np.pi * freq * t) + 0.25 * np.sin(2 * np.pi * freq * 2 * t)
    env = np.exp(-t * decay)
    return A.lowpass(sig * env, sr, cutoff=cutoff) * amp


def bell(freq, dur, partials, decays, sr=A.SR):
    n = int(sr * dur)
    t = np.arange(n) / sr
    sig = np.zeros(n)
    for p, d in zip(partials, decays):
        sig += np.sin(2 * np.pi * freq * p * t) * np.exp(-t * d)
    return sig


def scatter_events(n_samples, sr, event_fn, notes, events_per_loop, seed, amp=0.18, dur_each=1.6):
    """Scatter one-shot events (from event_fn(freq, dur_each, sr, amp=...))
    at random times across a buffer of n_samples - used for sparse plucks,
    random ticks, or any other 'occasional accent over a bed' texture."""
    rng = np.random.default_rng(seed)
    buf = np.zeros(n_samples)
    loop_dur = n_samples / sr
    for _ in range(events_per_loop):
        t_off = rng.uniform(0, loop_dur)
        freq = rng.choice(notes)
        seg = event_fn(freq, dur_each, sr, amp=amp * rng.uniform(0.7, 1.0))
        start = int(t_off * sr)
        seg_len = len(seg)
        end = start + seg_len
        if end <= n_samples:
            buf[start:end] += seg
        else:
            first = n_samples - start
            buf[start:] += seg[:first]
            buf[: seg_len - first] += seg[first:]
    return buf


def sub_pulse(n_samples, sr, interval_sec, amp=0.1, f_start=90, f_end=45, thump_dur=0.25, offset=0.3):
    buf = np.zeros(n_samples)
    t_cur = offset
    while t_cur * sr < n_samples:
        seg = A.exp_pitch_sweep(f_start, f_end, thump_dur, sr) * np.exp(-np.linspace(0, 6, int(sr * thump_dur)))
        start = int(t_cur * sr)
        end = start + len(seg)
        if end <= n_samples:
            buf[start:end] += seg * amp
        t_cur += interval_sec
    return buf


def stereo_pad_pair(dur, sr=A.SR, freqs=None, detune_voices=3, spread_cents=9.0,
                     wave="sine", seed_l=10, seed_r=11):
    left = A.pad_voice(freqs, dur, sr=sr, detune_voices=detune_voices,
                        spread_cents=spread_cents, wave=wave, seed=seed_l)
    right = A.pad_voice(freqs, dur, sr=sr, detune_voices=detune_voices,
                         spread_cents=spread_cents, wave=wave, seed=seed_r)
    return np.stack([left, right], axis=1)


def irregular_pattern(n_steps, seed, density=0.5, min_strength=0.4):
    """A pseudo-random strength pattern (not a steady 4/4 grid) for
    'irregular pulses' / 'unpredictable ticks' textures."""
    rng = np.random.default_rng(seed)
    return [rng.uniform(min_strength, 1.0) if rng.uniform(0, 1) < density else 0.0
            for _ in range(n_steps)]
