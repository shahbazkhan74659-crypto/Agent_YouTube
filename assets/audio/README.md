# Audio library — topic-based music & SFX

Self-produced per the budget decision in `idea.md` ("Music/SFX — self-produced
before launch, not licensed/subscribed"). Everything here is **procedural
synthesis** (numpy/scipy, `soundfile` for 24-bit I/O — no samples, no stock
sources, no network calls), organized by **subject category**
(science/history/philosophy/mythology/mysteries/knowledge/religion/
storytelling) rather than by the channel's narration structure.

This replaces the earlier, smaller library that was tied one-to-one to the
Storytelling → Explanation → Questionary beat structure (5 beds + 7 SFX,
44.1kHz/16-bit) — that system is gone; this one is the channel's audio
library going forward.

## Format

**48kHz / 24-bit PCM, stereo**, via `soundfile` (`scipy.io.wavfile` can't
write 24-bit cleanly — that's why the old library was 16-bit).

**Human listen-through in progress** — generated and numerically validated
(see `reports/validation_report.txt`: 100/100 assets pass — correct sample
rate/channels/bit depth, no clipping, no NaN/Inf, no silence, no duplicate
filenames, no exact-duplicate or near-duplicate audio flagged), and the user
has started listening category by category. `music/history/` was the first
folder reviewed (2026-10-25) — it was too repetitive and had an inconsistent/
too-quiet mix, so all 7 tracks were rewritten and re-mastered (see "Known
limitations" and `music/history.py`'s own revision note). The other 7 music
categories and all 50 SFX haven't been listened to yet — don't treat them as
upload-ready until they have been.

## Structure

The actual deliverable assets (the audio files, catalogs, and manifest) live
in a separate top-level folder from the dev/source-code tree — moved there
2026-10-25 on request, so the folders someone just wants to grab `.wav`
files or the catalog from aren't mixed in with `src/`:

```
C:\YouTube\Assets_audio\                  # the deliverables
├── music/<category>/MUS_XXnn_Title.wav   (50 tracks across 8 categories)
├── sfx/<category>/SFX_XXnn_Title.wav     (50 one-shots across 7 categories)
└── metadata/
    ├── music_catalog.csv       # one row per track
    ├── sfx_catalog.csv         # one row per SFX
    └── asset_manifest.json     # same data, for software integration

C:\YouTube\assets\audio\                  # the generator (this folder)
├── reports/
│   ├── generation_report.txt   # counts, total duration/disk usage, limitations
│   └── validation_report.txt   # per-asset technical findings
├── src/
│   ├── audio_lib.py            # synthesis primitives (oscillators, filters,
│   │                            # FM/AM, percussion, delay/saturation/
│   │                            # granular, modal scales, 24-bit writer,
│   │                            # loudness/true-peak estimation,
│   │                            # LUFS-target normalization)
│   ├── composition.py          # generic multi-layer bed/one-shot renderer
│   │                            # (optional target_lufs/pre_limit_drive -
│   │                            # see Mixing notes)
│   ├── helpers.py              # shared composition helpers (pluck, bell,
│   │                            # scatter_events, sub_pulse, ...)
│   ├── music/<category>.py     # one function per track (8 files)
│   ├── sfx/<category>.py       # one function per SFX (7 files)
│   ├── registry.py             # the single source of truth: every asset's
│   │                            # id/path/category/generator/metadata
│   ├── generate.py             # orchestrator / entry point
│   ├── metadata_gen.py         # builds the CSV/JSON catalogs
│   └── validate.py             # technical validation suite
└── requirements.txt
```

## Regenerating / extending

```
cd src
python generate.py                        # everything (100 assets, ~1-2 min on CPU)
python generate.py --category science      # just one category (music or sfx)
python generate.py --id MUS_SC01           # just one asset
python validate.py                         # re-validate what's on disk
```

It's deterministic (fixed RNG seeds inside each generator function) —
re-running reproduces byte-identical output, so it's safe to tweak a
parameter and re-run rather than hand-edit a `.wav`. There's no full
`argparse` CLI or a rendered audio-preview system yet (deliberately deferred
— see "Known limitations"); `registry.py` is where a new track/SFX gets
added if the library grows further.

## Categories

**Music** (`music/`, 50 tracks):

| Category | Count | Covers |
|---|---|---|
| `science` | 6 | Scientific discoveries, physics, cosmology-adjacent, biology, paradoxes |
| `history` | 7 | Ancient civilizations, empires, archaeology, deep prehistory |
| `philosophy` | 6 | Existence, free will, consciousness, paradox, mortality |
| `mythology` | 7 | Creation myths, gods, the underworld, heroic quests, collapse |
| `mysteries` | 7 | Unsolved questions, investigations, unexplained signals |
| `knowledge_curiosity` | 6 | General fascinating facts, learning, explainers |
| `religion_cosmology` | 5 | Comparative religion, cosmic order, afterlife beliefs |
| `storytelling` | 6 | General-purpose hooks, deep-dive narration beds, dark-ethics cues, open endings |

**SFX** (`sfx/`, 50 one-shots): `science_cosmos` (8), `history_archaeology` (7),
`philosophy` (6), `mystery_investigation` (8), `mythology_fantasy` (7),
`knowledge_curiosity` (7), `cinematic_editing` (7, generic cut/impact/riser
tools usable regardless of subject).

Full per-asset detail (purpose, mood, tonal center, loop compatibility,
measured duration/peak/loudness) is in `metadata/music_catalog.csv` and
`metadata/sfx_catalog.csv` — those are the actual searchable catalog, this
README is just the map.

### Example catalog lookups

The CSV/JSON catalogs are built to answer queries like:

- *Curious music for a science fact* → `music_catalog.csv`, category=`science`,
  mood contains "curious" → `MUS_SC01_The_Discovery.wav`.
- *Mysterious music for ancient history* → category=`history`, mood contains
  "sparse"/"unresolved" → `MUS_HI02_The_Lost_Civilization.wav`.
- *Philosophical music without sadness* → category=`philosophy`, mood NOT
  containing "sad"/"mournful" → most of this category qualifies by design
  (`MUS_PH03_Free_Will`, `MUS_PH04_Consciousness`).
- *A subtle sound for a surprising fact* → `sfx_catalog.csv`,
  `SFX_KN02_Interesting_Fact.wav` or `SFX_SC04_Scientific_Discovery_Accent.wav`.
- *An ambient loop for a philosophical monologue* → `music_catalog.csv`,
  loop_compatible=yes, category=`philosophy` → `MUS_PH01_The_Question_of_Existence.wav`.

## Carrying forward the epistemic-transparency signal

The old library had a dedicated SOLID/CONTESTED claim-reveal SFX pair
(`sfx_ding_claim_solid.wav` / `sfx_tone_uncertain.wav`) that carried the
channel's differentiation angle (confidence is something the viewer *hears*,
not just reads) — see `idea.md`. That pairing isn't a separate asset here;
use these existing SFX for the same purpose:

- **SOLID-confidence claim reveal** → `SFX_PH04_Realization.wav` or
  `SFX_KN04_Discovery_Chime.wav`.
- **CONTESTED/UNCERTAIN claim reveal** → `SFX_PH06_Unresolved_Thought.wav` or
  `SFX_MI07_Unanswered_Question.wav`.

## Mixing notes

- Peaks sit around -4.3 to -9 dBFS depending on asset (see `peak_dbfs` in the
  catalogs) — nothing clipped, but still duck music beds well under narration
  (roughly -18 to -24 dB relative to voice) in the assembly step; these are
  backing beds, not mix-ready masters.
- `music/history/`'s 7 tracks additionally target a consistent **-15 to -16
  LUFS** integrated loudness (via `composition.render_bed`'s `target_lufs`
  parameter) rather than relying on peak level alone — fixes a real
  inconsistency the first listen-through caught (see below). Other
  categories still rely on plain peak normalization; revisit the same way if
  the same complaint comes up elsewhere.
- Stereo: music beds mostly use true stereo chorus (independently seeded
  left/right oscillator detuning) or constant-power panning of layered mono
  voices; SFX use a cheap Haas-delay stereo widen. Both collapse fine to mono.
- Most music tracks (all but a few deliberately short/one-shot storytelling
  cues) are seamless loops — built with the crossfade-the-tail-into-the-head
  technique, not a hard cut — so they repeat under narration of any length
  without a click at the loop point.
- A handful of tracks (e.g. `MUS_HI03_Rise_and_Fall_of_Empires`,
  `MUS_MY07_The_Fall_of_the_Gods`, `MUS_ST03_The_Unexpected_Truth`) have a
  real dynamic arc inside each loop cycle (a build, a dip, an accent) — check
  `metadata/music_catalog.csv`'s purpose/mood text before assuming a flat
  background level.

## Known limitations

- **Only `music/history/` has been human-verified by ear so far** (see
  above) — the other 7 music categories and all 50 SFX haven't been
  listened to yet. Same honest caveat the old library had, now partially
  resolved rather than fully open.
- **Preview-audio system not built** — no single "audition reel" with
  timestamped index yet. Scoped out of this build on purpose; the catalogs
  are the way to find an asset for now. Worth adding later if the library
  grows further.
- **No full CLI** — `generate.py` takes a simple `--category`/`--id` filter,
  not a polished `argparse` subcommand surface (`generate music --category X`
  as literally specified). The registry-driven filter covers the same
  resumability need without the extra surface.
- **Loudness/true-peak are estimates**, not certified broadcast-standard
  measurements — see `reports/generation_report.txt`'s "Known limitations"
  for the exact caveat. `integrated_loudness_lufs` is `pyloudnorm`'s
  ITU-R BS.1770 calculation; true peak is a 4x-oversampling estimate.
- **Near-duplicate detection** (`validate.py`) is a cheap 32-band spectral
  fingerprint comparison, not a perceptual audio-matching algorithm — good
  enough to flag for review, not a rigorous duplicate detector. Nothing was
  flagged in this run.
- **No limiter/compressor stage** — if a future edit stacks multiple
  beds/SFX together, re-check the combined peak before export.
- **BPM is "N/A"** for every track in the catalog — this library is built
  from loop/envelope durations and event-scatter timing, not a fixed metric
  grid, so a literal BPM number would be fabricated for most tracks (a few,
  like `MUS_SC05_The_Human_Machine`, do have an internal step grid, but it's
  not exposed as a single tempo value either).
