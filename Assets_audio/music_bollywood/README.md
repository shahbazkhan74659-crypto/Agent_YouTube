# Bollywood-referenced emotion music library

Replaces `Assets_audio/music/` (the genre-categorized library) for actual
production use, decided 2026-10-26. That older library is left on disk,
untouched - just no longer selected by `pipeline/audio_mix.py`.
`Assets_audio/sfx/` is unaffected by this change and stays in use as-is.

## What "Bollywood-referenced" means here

Every track in this library is an **original composition**, self-produced
with the same procedural-synthesis pipeline as the rest of `assets/audio/`
(see `assets/audio/src/bollywood/`). "Bollywood-referenced" means the
composer studies Bollywood **background-score** (instrumental underscore,
not picturized songs) conventions as a style guide - instrumentation
(tabla, dholak, sitar, bansuri, harmonium, string sections), scales, and
rhythmic feel - and writes new music in that tradition.

**What this is not**: no track here is sampled, looped, pitched, or
otherwise derived from an actual copyrighted Bollywood recording. Nothing
in this library is downloaded. Copyright protects a specific recording and
composition, not a genre or instrumentation - the line this library stays
on the right side of is "inspired by the style," never "built from the
song." See the project's `idea.md` / `memory.md` for the fuller discussion
of why (Content ID risk, channel-risk, and the fact that it would have
undercut the reason the procedural pipeline exists at all).

## Structure

One folder per emotion category (`EMOTION_CATEGORIES` in `pipeline/config.py`):

```
music_bollywood/
  motivational/   mysterious/   cold/        cheerful/
  epic/           tense/        dark/        melancholic/
  romantic/       reflective/   hopeful/     nostalgic/
  awe/            peaceful/
```

Catalog: `Assets_audio/metadata/music_catalog_bollywood.csv` (same role as
the old `music_catalog.csv`, keyed by `emotion` instead of `category`).

## Status (2026-10-26)

**Infrastructure only - zero tracks exist yet.** Every folder above is
empty. The pipeline (cue syntax in `script.md`, per-part crossfade mixing
in `audio_mix.py`, the catalog loader, the Bollywood-style synthesis
primitives in `assets/audio/src/bollywood/bollywood_primitives.py`) is
built and ready, but no actual composition has been written - that's
waiting on gathering real Bollywood background-score reference material
and a composition brief per emotion, the same way the original genre
library started from a full user-provided spec before any track was
rendered. See `assets/audio/src/bollywood/music/` for the per-emotion
module stubs this will fill in.

## How a video selects emotions

A `script.md` marks which emotion is active from a given beat onward with
an inline cue, same convention as `[ON SCREEN: ...]`:

```
**[MUSIC: mysterious]**

**HOOK (0:00-0:15):** ...
```

The cue persists across beats until the next `[MUSIC: ...]` cue changes it,
so one cue per structural part (Storytelling / Explanation / Questionary,
or finer) is normally enough. `pipeline/audio_mix.py` groups consecutive
beats sharing an emotion into one continuous music "part," picks one track
per part, and crossfades between parts at the boundary
(`config.MUSIC_CROSSFADE_SEC`, default 1.5s) so the mood shifts with the
video instead of looping one bed over the whole runtime.
