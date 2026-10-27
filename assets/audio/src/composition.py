"""
Generic multi-layer track/SFX shell. Generalizes the crossfade-tail-into-
head loop technique (generate the full continuous signal, run every effect
on it, and ONLY THEN crossfade - cropping first and filtering after destroys
the seam match) into a reusable builder so each of the 50 music tracks picks
genuinely different layers/instrumentation/arrangement instead of re-skinning
one formula.
"""

import numpy as np
import audio_lib as A


def render_bed(layers, total_dur, sr=A.SR, loop_dur=None, xfade=2.0,
                envelope=None, reverb=None, peak_db=-6.0, target_lufs=None,
                pre_limit_drive=None):
    """Mix a list of mono or stereo layers into one stereo bed.

    layers: list of (signal, mix_level, pan_pos) where signal is 1D (mono,
        will be panned via A.pan) or already 2D stereo (pan_pos ignored).
    total_dur: length of `signal` buffers passed in, in seconds.
    loop_dur: if given, the output is cropped to loop_dur seconds with the
        tail crossfaded into the head for a seamless loop (xfade = total_dur
        - loop_dur must be > 0). If None, the output is a one-shot of
        total_dur seconds (envelope/fades applied, no crossfade).
    envelope: optional 1D gain curve (length total_dur*sr) applied to the
        full mix before any loop crop - e.g. from A.envelope_from_breakpoints.
    reverb: optional dict of kwargs for A.synth_reverb, applied per-channel
        to the full mix before cropping.
    target_lufs: if given, final gain targets this integrated loudness
        (via A.normalize_lufs, peak capped at peak_db) instead of plain
        peak normalization - use for tracks where sparse transients would
        otherwise undershoot perceived loudness relative to denser ones at
        the same peak_db. Default (None) preserves the original plain
        peak-normalize behavior for every existing caller.
    pre_limit_drive: if given, applies gentle tanh soft-limiting
        (A.saturate) to the full mix before the final normalize step - this
        compresses a track's hottest transients (e.g. a sparse accent hit)
        relative to its sustained body, lowering crest factor so
        target_lufs can actually be reached without blowing past peak_db.
        Default (None) applies no limiting - unchanged for every existing
        caller.
    """
    n = int(sr * total_dur)
    mix = np.zeros((n, 2))
    for sig, level, pos in layers:
        if sig.ndim == 1:
            stereo = A.pan(sig, pos)
        else:
            stereo = sig
        length = min(len(stereo), n)
        mix[:length] += stereo[:length] * level

    if envelope is not None:
        mix *= envelope[:n, None]

    if reverb is not None:
        left = A.synth_reverb(mix[:, 0], sr, seed=1, **reverb)
        right = A.synth_reverb(mix[:, 1], sr, seed=2, **reverb)
        mix = np.stack([left, right], axis=1)

    if loop_dur is not None:
        xf = int(sr * xfade)
        L = int(sr * loop_dur)
        fade_in = np.linspace(0, 1, xf)[:, None]
        fade_out = 1 - fade_in
        out = mix[:L].copy()
        out[:xf] = mix[:L][:xf] * fade_in + mix[L:L + xf] * fade_out
    else:
        out = mix
        fi, fo = int(sr * 0.01), int(sr * 0.3)
        if fi > 0:
            out[:fi] *= np.linspace(0, 1, fi)[:, None]
        if fo > 0:
            out[-fo:] *= np.linspace(1, 0, fo)[:, None]

    if pre_limit_drive is not None:
        # saturate() maps its own peak (after this pre-normalize to unit
        # scale) to the saturating region of tanh, so quiet body content
        # (well below the peak) stays near-linear while the hot transient
        # gets compressed toward it - that's what actually lowers crest
        # factor; applying saturate() directly to an arbitrary-scale mix
        # would do nothing since tanh is ~linear far from its peak.
        out = A.saturate(A.normalize(out, peak_db=0.0), drive=pre_limit_drive)

    if target_lufs is not None:
        return A.normalize_lufs(out, sr=sr, target_lufs=target_lufs, peak_ceiling_db=peak_db)
    return A.normalize(out, peak_db=peak_db)
