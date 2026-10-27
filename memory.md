# Progress log — 2026-10-24

Everything done today, in order. Full detail lives in `idea.md` (decisions) and
`voice.md` (creator profile); this is the narrative record of the day.

## 1. Tooling installed and customized

- Installed `youtube-agent-skill` (11 global Claude skills: `/yt-script`,
  `/yt-package`, `/yt-retention`, `/yt-edit`, `/yt-comment`, `/yt-plan`,
  `/yt-viral`, `/yt-shorts`, `/yt-seo`, `/yt-chapters`, `/yt-audit`) — reviewed the
  source first for prompt-injection/network-call red flags before installing.
- **`yt-script`** rewritten for a narration-only, pre-launch channel: dropped
  on-camera/"paste 3 of your videos" assumptions; now requires a `research.md`
  brief before writing any claim, with SOLID/CONTESTED/UNCERTAIN confidence
  carried into how each line is stated; `[ON SCREEN: ...]` cues now require a
  sourceable visual (Wikimedia/NASA/Pixabay/Smithsonian search term or an
  `AI-generate:` prompt); `hooks.json` examples reworded to this niche (cosmetic
  only, scoring regex untouched).
- **`yt-factcheck`** built from scratch: gather (new `sources.py`, stdlib-only,
  hits Wikipedia + Internet Archive + Semantic Scholar, all free/keyless) → draft
  claims with confidence tags → independent re-check by a *fresh* subagent with no
  memory of the draft → visual anchors → `research.md` brief.
- **`voice.md`** template reworked for narration/TTS instead of on-camera
  presence (tone, Kokoro preset, pacing, visual mix instead of camera/desk
  questions).
- File convention established: `C:\YouTube\videos\<topic-slug>\` holds `research.md`
  + `script.md` per video.
- **Live end-to-end test** on "Library of Alexandria — why/how it was destroyed":
  `yt-factcheck` correctly downgraded the Serapeum/library link to UNCERTAIN and
  flagged the Caliph Omar burning story as an unsupported legend rather than
  fact; `yt-script` produced a grounded script from that brief, hook formula "The
  Warning." Honest finding logged: `hookscore.py`'s STAKES property is calibrated
  for growth-hack content and scores pure historical-curiosity hooks WEAK —
  resisted inventing false stakes to game the score; parked as a separate issue.

## 2. Production pipeline and budget decided

- Images/video clips + voiceover + captions, not from-scratch motion graphics —
  hardware (Ryzen 3 5425U, integrated graphics, 8GB RAM) can't sustain
  render-heavy animation at daily cadence.
- Cadence: 1 video/day (down from the original 2/day idea).
- Budget: Claude usage + ElevenLabs are the only accepted must-spend items;
  **Kokoro** (free, local, CPU-only TTS) chosen as the actual production voice
  over ElevenLabs/voice-cloning for now; visuals free-source-first; music/SFX
  self-produced; thumbnails free-tool-first; storage local.

## 3. Differentiation angle and content structure decided

- Discussed what actually differentiates this channel from Kurzgesagt/Eons/etc.
  now that visuals are stock-sourced like anyone else's. Landed on **epistemic
  transparency as the format itself**: claims visibly tagged by confidence,
  popular myths actively corrected (not repeated), sourcing shown rather than
  asserted — harder to copy than a visual style since it requires the
  `yt-factcheck` pipeline behind it.
- Formalized a three-beat content structure: **Storytelling → Explanation →
  Questionary** — narrative hook, then claims at their real confidence level,
  then the payoff *and* a genuinely unresolved question back to the viewer
  (question after the payoff, never instead of it). Logged in `voice.md`/
  `idea.md` only — not yet built into the `yt-script` skill itself.

## 4. Daily operating schedule set

New standing rule: content ready by **8:00 PM**, **8–11 PM** is the Admin+Claude
collab window (fixing what Admin doesn't like, finalizing edit/content), video
uploads **before midnight** regardless of whether Admin was actually active in
the window. Built into `yt-plan/SKILL.md` ("Daily production schedule" / "The
shape of a day"), replacing its old generic "three uploads a week" default, and
logged in `idea.md`.

## 5. Status check

Took stock of what's done vs. left. Confirmed open items at that point: thumbnail
tooling, `voice.md`'s unconfirmed defaults, Storytelling/Explanation/Questionary
not wired into `yt-script`, 9 of 11 skills still generic, no actual render
pipeline, `hookscore.py` STAKES weighting, music/SFX, no channel yet created.

## 6. Thumbnail tooling resolved

Verified **GIMP 3.2.6 is actually installed**
(`C:\Users\shahb\AppData\Local\Programs\GIMP 3\bin\gimp-3.exe`, Start Menu
shortcut present) — an earlier session log had shown a cancelled/failed install,
but a later successful install superseded it. Logged as decided in `idea.md`
(Budget section); removed two stale "open question" entries that were already
resolved elsewhere in the doc (thumbnail tooling, fact-check process).

## 7. Reviewed the 9 remaining generic skills

Read all 9 untouched `yt-*` skills (`yt-audit`, `yt-chapters`, `yt-comment`,
`yt-edit`, `yt-package`, `yt-retention`, `yt-seo`, `yt-shorts`, `yt-viral`) to
assess what needs customizing for this project (most still assume an on-camera
creator with an existing channel, same as `yt-script` did before it was fixed).
**Interrupted before any edits were made — this is still open.**

## 8. Resolved voice.md's three drafted defaults

User answered the three items that had been marked `[CONFIRM]`:

- **Narration tone →** Cheerful, curious, hyped, and disciplined. Reconciled with
  the existing "words I never use" vague-superlative ban by clarifying: hyped
  describes delivery energy, not permission to inflate claims — the discipline
  from `yt-factcheck` stays untouched.
- **Length →** YouTube Shorts' maximum length. Verified via web search this is
  **3 minutes** (extended from 60 seconds in October 2024), which also requires
  vertical/square framing, not just short runtime. This corrected an
  over-generalization made earlier in `yt-plan/SKILL.md` and `idea.md` ("long-form
  or Shorts, whichever") — fixed to Shorts specifically in both places.
- **Kokoro voice preset →** left genuinely undecided; user will pick later.
  Removed the earlier `af_heart`-as-default assumption from `voice.md`.
- Explicitly told **not** to copy the finished `voice.md` to
  `~/.claude/youtube/voice.md` yet (the actual path every skill reads from) —
  that copy is still pending, a one-time step for later.

## Carried-forward open items (as of end of day)

1. Copy `C:\Idea\voice.md` → `~/.claude/youtube/voice.md` (held back on purpose).
2. Finish reviewing/customizing the other 9 `yt-*` skills.
3. Build Storytelling → Explanation → Questionary into `yt-script` itself.
4. Build the actual render pipeline: TTS → visuals → assembly/captions → export.
   Nothing today produces an `.mp4` yet — this is the real blocker to shipping.
5. Revisit `hookscore.py`'s STAKES weighting for curiosity-driven hooks.
6. Produce music/SFX (decided to self-produce, none made yet).
7. Create the actual YouTube channel — doesn't exist yet.

# Progress log — 2026-10-25

Continuation of the above. The project folder was renamed `C:\Idea` → `C:\YouTube`
today — every path reference in this log and in `idea.md` now reflects that.

## 1. Finished reviewing the 9 remaining generic skills (item 2 above)

Audited all 9 against the actual pipeline (TTS-only narration via Kokoro, no raw
human recording ever, every video natively Shorts-length per `voice.md`). 7 are
channel-stage/niche-agnostic and fine as-is — `yt-audit`, `yt-chapters`,
`yt-comment`, `yt-package`, `yt-retention`, `yt-seo`, `yt-viral` — unusable only
until there's an actual channel/videos/comments to feed them, not a content
mismatch. 2 had a genuine scope mismatch with how this channel actually works and
were changed (see below): `yt-edit` assumed a human raw take (filler, retakes,
dead air from a live performance); `yt-shorts` assumed mining a clip out of a
longer video, but every video here already *is* natively a Short.

## 2. Rewrote `yt-edit` for the TTS pipeline

Reframed from "edit a human recording's transcript" to "QC the generated Kokoro
narration," reading the `faster-whisper` segment-level transcript already produced
during the existing alignment step (not the word-level timestamps used for
caption sync). DEAD now means unnatural TTS-inserted pauses; FILLER/REPEAT
documented as dormant safety nets (script-leakage, accidental duplicate renders)
rather than human-performance issues. No code changes to `deadair.py` — confirmed
its parser/gap logic already works on any `start`/`end`/`text` segment data
regardless of source, and confirmed `yt-retention/retention.py` and
`yt-chapters/chapters.py` (which import `load`/`parse_ts` from it directly) still
import cleanly.

## 3. Created `yt-shortcraft` (new skill, item 2 above)

Same craft bar as `yt-shorts` — hook via `hookscore.py`, on-screen text in the
first two seconds, loop point, vertical framing — applied to a script that
already is the whole native Short, not a clip pulled from a longer video. Drops
the "rank candidates" mining mechanic entirely. `yt-shorts` itself left
untouched and still installed, in case a compilation/repurposing need comes up
later.

## 4. Built Storytelling → Explanation → Questionary into `yt-script` (item 3 above)

"The shape" section restructured into the three named beats: **Storytelling**
(hook + the turn, mechanics unchanged), **Explanation** (the body, confidence-
tagged per `research.md`, plus a new explicit rule that a flagged myth/legend
must be named and corrected on screen rather than quietly skipped), **Questionary**
(payoff delivered explicitly, then the script closes on the actual
CONTESTED/UNCERTAIN question from `research.md` — after the payoff, never
instead of it — replacing the generic subscribe-pitch ask rather than stacking
on top of it). "What to hand back" now also requires the closing question and
which `research.md` line it's drawn from.

## 5. Found and fixed a stale `voice.md` copy

While fixing the `C:\Idea` → `C:\YouTube` path rename in `yt-factcheck` and
`yt-script`, discovered two different `voice.md` files: the master
(`C:\YouTube\voice.md`) had moved on to the finalized decisions (tone confirmed,
length confirmed, the full "Differentiation angle" section added) — but
`~/.claude/youtube/voice.md`, the path every skill actually reads from, was
still the old draft with none of that (item 1 above was only half-done: a
premature copy existed but was never refreshed after the `[CONFIRM]` items were
resolved). Every skill run since those decisions were finalized had been reading
stale guidance. Refreshed the copy from the master; the two are now
byte-identical.

## 6. Fixed `hookscore.py`'s STAKES property (item 2 above)

The `STAKE` regex only recognized personal-loss vocabulary ("lose", "waste", "risk",
"fail"), so any pure historical-curiosity hook with none of those floored at
`STAKES: 22` no matter how strong it otherwise was — and the tool's deliberate
weakest-link weighting (40% of VERDICT) then dragged the whole score down on that
one property alone. Added destruction/erasure/mystery vocabulary native to this
niche's actual stakes (destroyed, vanished, disappeared, forgotten, erased, buried,
hidden, forbidden, banned, silenced, extinct, collapsed, ruins, perished, wiped,
unsolved, mystery, burned, fell, doomed). Verified against real data: the Alexandria
test script's hook #1 moved from 54 (WEAK) to 57 (WORKABLE); four synthetic
pure-curiosity hooks with no stake words moved off the flat 22 floor to 48; a
self-help-style control hook ("You are wasting money...") was unaffected, confirming
the fix adds niche vocabulary without diluting the property elsewhere.

## 7. Built the Music/SFX library (item 2 below, same day)

Procedural synthesis via numpy/scipy (`C:\YouTube\assets\audio\audio_lib.py` +
`generate_library.py`) — self-produced per the budget decision, no stock/
licensed audio. 5 music beds tied to the Storytelling → Explanation →
Questionary structure (storytelling/curious, explanation/neutral,
tension/contested, questionary/open — all seamless loops — plus a one-shot
payoff swell) and 7 SFX, sharing one tonal family (A minor pentatonic) so
anything combined in one video stays harmonically consistent. Two SFX
specifically carry the epistemic-transparency differentiation angle into
sound: `sfx_ding_claim_solid.wav` (bright, confident) vs
`sfx_tone_uncertain.wav` (deliberately wobbly/unresolved) for SOLID vs
CONTESTED/UNCERTAIN claim reveals.

Caught and fixed a real bug before shipping: the first generation run hung
for 2+ minutes because `synth_reverb` used `np.convolve` (plain O(n·m)) on
multi-second audio — switched to `scipy.signal.fftconvolve`, dropped to
~9s for the full 12-asset run. Second bug caught by actually measuring the
loop seams (not just eyeballing): tremolo/lowpass/reverb were being applied
*after* the loop was already cropped to its final length, which silently
undid the crossfade's seam-matching — each effect re-ran from array-index 0
on the cropped copy, so the sample at the loop's end no longer matched the
sample at its start. Measured discontinuity was 20-40% of peak amplitude
before the fix. Fixed by reordering: generate the full continuous signal,
run every effect on it, and crossfade the tail into the head *last* — down
to under 3% of peak amplitude after. Catalog, mixing notes (headroom levels,
ducking guidance), and known limitations logged in
`C:\YouTube\assets\audio\README.md`. Not yet human-verified by ear — numeric
checks only (no clipping, no NaNs, loop-seam measurement).

## 8. Reworked `bed_explanation_neutral.wav` into a cinematic thriller cue (same day, user-dictated)

User dictated a full creative brief (cinematic thriller composer / sound
designer direction) to transform this one bed from a calm neutral drone into
a dark, suspenseful four-phase cue: uneasy opening → building dread →
a threat impact (after a deliberate silence dip) → an unresolved ending whose
reverse-riser climbs back into the loop point. Implemented directly in
`generate_library.py`'s `make_bed_explanation()`, adding four new reusable
primitives to `audio_lib.py`: `vibrato_sine` (slow pitch-wobble, phase-
continuous), `inharmonic_hit` (metallic/struck one-shots with optional noise
transient), `reverse_riser` (a decaying noise burst played backwards), and
`envelope_from_breakpoints` (general-purpose dynamics/automation curve).
Verified numerically: 24s/44.1kHz/stereo, peak -6dB (no clipping), loop seam
at 0.04% of peak (even tighter than the other beds), and an RMS-per-second
profile matching the intended arc (quiet open, climb through 6-12s, dip at
13s, spike at 14s, settle after). Logged the mood/filename mismatch this
creates in `idea.md` — the file is still named "neutral" but is no longer
neutral. Not yet human-verified by ear, same caveat as everything else in
this library.

## 9. Replaced the 12-asset structural audio library with a 50+50 topic-based one (2026-10-25, same day)

User pasted a large spec for a topic-categorized audio library (science,
history, philosophy, mythology, mysteries, knowledge/curiosity,
religion/cosmology, general storytelling) — 50 music tracks + 50 SFX with
CSV/JSON catalogs and a validation suite. Rather than build it alongside
the existing Storytelling → Explanation → Questionary-tied library (#7
above), the user chose to **replace** it outright, scoped to: all 100 real
assets + a working metadata catalog + real validation now, skipping a
rendered-preview system and a full `argparse` CLI for later.

Rebuilt `C:\YouTube\assets\audio\` from scratch under this structure:
`music/<8 categories>/`, `sfx/<7 categories>/`, `metadata/` (CSV + JSON
catalogs), `reports/` (generation + validation reports), `src/` (extended
`audio_lib.py` + a new `composition.py` generic multi-layer bed/one-shot
renderer + `helpers.py` + one generator module per category + `registry.py`
as the single source of truth + `generate.py`/`metadata_gen.py`/`validate.py`).
Switched format from 44.1kHz/16-bit to **48kHz/24-bit** via `soundfile`
(`scipy.io.wavfile` can't write 24-bit cleanly) — added `pyloudnorm` for
real ITU-R BS.1770 integrated-loudness measurement in the catalogs.

New synthesis primitives added to cover the spec's diversity requirements
(not every track should be a pad+pluck formula): FM/AM synthesis, a
granular-texture scatterer, a feedback delay line, tanh saturation, minimal
kick/noise percussion synths plus a `rhythm_pattern` step-sequencer, a
constant-power stereo panner, and a small table of modal scales (Dorian/
Phrygian/Lydian/whole-tone/harmonic-minor/etc., not just the old library's
one A-minor-pentatonic family).

All 50 music tracks + 50 SFX generated and passed validation on the first
full run: 100/100 valid, 0 failed, 0 flagged for review, ~21.3 minutes of
audio, ~371MB on disk (`reports/generation_report.txt`). Old flat-structure
files (`audio_lib.py`, `generate_library.py`, old `README.md`, and the 12
old `.wav` files) were deleted as part of the replace.

Deliberately preserved the one thing worth carrying forward from the old
library: the SOLID/CONTESTED claim-reveal sonic signal (epistemic
transparency differentiation angle, see "Differentiation angle" below).
No dedicated asset for it this time — documented in the new
`assets/audio/README.md` which existing SFX serve that role
(`SFX_PH04_Realization` / `SFX_KN04_Discovery_Chime` for SOLID,
`SFX_PH06_Unresolved_Thought` / `SFX_MI07_Unanswered_Question` for
CONTESTED/UNCERTAIN) instead of building near-duplicate assets.

Updated `idea.md`'s Budget §4 to describe the new library in place of the
old one.

## 10. First human listen-through found a real issue in music/history/ — fixed (2026-10-25, same day)

User started listening through the new library folder-by-folder and flagged
`music/history/` (7 tracks): too similar to each other, and too quiet to
hear clearly. Diagnosed rather than assumed — an Explore agent read
`history.py` against `mythology.py` and the catalog's measured loudness
numbers. Confirmed both as real, specific issues, not false alarms:

- **Similarity**: 5-6 of `history.py`'s 7 functions reused the identical
  skeleton (pad/drone + `scatter_events` pluck + sparse percussion),
  varying only root/mode/density — unlike `mythology.py`, where each of
  its 7 tracks leads with a genuinely different primitive.
- **Loudness**: not a category-wide deficit (history's average LUFS wasn't
  actually lower than mythology's or science's) but a real *internal*
  inconsistency — `audio_lib.normalize()` is peak-only, so tracks with one
  brief hot transient over an otherwise sparse bed (HI03, HI05) measured
  8-9 LU quieter than continuous-energy tracks (HI06) at the identical
  `peak_db` setting.

Fix: rewrote all 7 `history.py` functions so each leads with a distinct
technique (inharmonic "tolling bell" hits, bandpass-filtered hollow noise,
FM-tone melody, continuous granular/AM stutter in place of near-silent
ticks + one hit, granular grit, tanh-saturated decaying drone). Added two
new *optional* parameters to the shared `composition.render_bed()` —
`target_lufs` (gains toward a target integrated loudness instead of plain
peak-normalize, via the already-installed `pyloudnorm`) and
`pre_limit_drive` (gentle tanh soft-limiting on the full mix before that
gain step, needed because several tracks' crest factor was too high to
hit -15 LUFS without exceeding a safe peak ceiling — discovered by
measuring crest factor directly rather than guessing at parameters).
Default `None` on both — confirmed zero effect on every other category by
re-running the full validation suite and diffing other categories' catalog
rows before/after.

Result: history's internal loudness spread collapsed from 9.1 LU to 1 LU
(all 7 tracks now -15 to -16 LUFS, peaks safely under -4.3 to -6.9 dBFS),
full 100-asset validation still passes. Scoped strictly to
`music/history/` per the user's explicit instruction — no other category
touched.

## 11. Moved the deliverable asset folders out of the dev tree (2026-10-25, same day)

User asked to move `assets/audio/metadata`, `assets/audio/music`, and
`assets/audio/sfx` into a new top-level `C:\YouTube\Assets_audio\` folder
— separates the actual deliverables (audio files, CSV catalogs, JSON
manifest) from the generator/dev tree, which stays at
`C:\YouTube\assets\audio\` (`src/`, `reports/`, `README.md`,
`requirements.txt`).

Moved the 3 folders, then updated `generate.py`, `metadata_gen.py`, and
`validate.py` (the only 3 files with hardcoded path logic) to resolve
music/sfx/metadata against a new `DATA_ROOT = ROOT.parent.parent /
"Assets_audio"` instead of the old `ROOT`-relative paths; `reports/` stays
under the original `ROOT` since it wasn't part of the move. Verified with
`python validate.py` (100/100 still found and valid at the new location)
and a single-asset `python generate.py --id MUS_SC01` (confirmed the write
path also resolves correctly). Updated the README's structure diagram and
`idea.md`'s Budget §4 to point at the new location.

## Progress log — 2026-10-25 (continued): render pipeline built

Built the render pipeline that was the #1 carried-forward blocker: `C:\YouTube\pipeline\`
now takes a `script.md` straight through to a finished `final.mp4`, end to end,
verified against the real `library-of-alexandria-destruction` test video (9 beats,
159.9s, 1080x1920, clean full-file ffmpeg decode check, under the 180s Shorts cap).

Planned and approved in plan mode first (`wobbly-knitting-cocoa.md`); two things were
decided with the user before building: Kokoro voice preset stays provisional (picker
tool built, ran, 8 presets generated to `C:\YouTube\voice-picker\` for a listen - not
yet locked into `voice.md`); `AI-generate:` cues route through **Pollinations.ai**
(free, keyless) since free Gemini image generation is confirmed blocked.

**Modules** (`pipeline/`): `script_parser.py` (script.md → beats.json, handles
multi-line ON SCREEN cues and labels), `narration.py` (Kokoro per beat →
narration_meta.json with real timing), `alignment.py` (faster-whisper per beat →
word timestamps), `visuals/sources.py`+`ai_generate.py`+`resolve.py` (Wikimedia →
NASA → Pixabay → Smithsonian → Pollinations, license-filtered, → manifest.json),
`captions.py` (word timestamps → karaoke-style `.ass` kinetic captions via
`pysubs2`), `audio_mix.py` (narration + Assets_audio music bed + SOLID/CONTESTED
SFX accents → one ffmpeg filter graph → mix.wav), `assemble.py` (per-beat Ken
Burns/zoompan clips → concat → caption+audio mux → final.mp4), `render.py`
(resumable orchestrator, same `--force`/stage-skip pattern as `assets/audio`'s
`generate.py`). `ffmpeg_tool.py` wraps `imageio-ffmpeg`'s bundled binary (pip
install, confirmed full build with libx264/libx265/libass/zoompan) - avoids the
admin-elevation friction the GIMP install hit; ffmpeg was not on PATH on this
machine before this.

**Real bugs found and fixed while building (not theoretical - each one broke a
live test run):**
- Wikimedia's `upload.wikimedia.org` rate-limits (429) automated full-resolution
  downloads and explicitly tells callers to use thumbnails instead - switched to
  requesting a sized `thumburl` via `iiurlwidth`, served from a different host
  (`thumb.wikimedia.org`) that isn't rate-limited the same way. We don't need
  full-res originals for a 1080-wide frame anyway.
- Pixabay returns a generic/trending hit rather than nothing when a query has no
  real match - live example: "Serapeum Alexandria ruins" returned a hot-chocolate
  photo (its tags happened to include "Alexandria" as an incidental location tag).
  Added a relevance filter requiring at least half the query's significant words
  to actually appear in the hit's tags.
- Pollinations.ai's free tier hard-limits to 1 image per 45 seconds per IP (402
  `FREE_LIMIT`) - added a proactive rate limiter (not just retry-after-failure)
  so a multi-AI-generate-cue video doesn't burn through retries back-to-back.
- ffmpeg defaults a looped still image to 25fps input; asking for 30fps output
  frames against a 25fps-timed `-t` window silently shortened every Ken Burns
  clip to 25/30 of its intended duration (a 17.86s clip rendered as 14.90s) -
  fixed by explicitly setting `-r 30` on the looped-image input. Caught by
  comparing the assembled video's duration against the audio mix's, not by
  trusting a clean exit code.

**What's still genuinely unverified**: I checked the output technically (ffprobe
resolution/duration, a full-file decode pass with no errors) but have not watched
or listened to `final.mp4` myself - whether the Ken Burns motion looks right,
whether captions are legible, whether the music sits well under narration, and
whether the Kokoro voice actually sounds good are all still open. `render.py`
prints this caveat on every run on purpose.

## Global `video-reader` skill built (2026-10-25)

User asked for a way for Claude to actually "see" video content, independent of this
project. Built `~/.claude/skills/video-reader/` (global, not under `C:\YouTube` -
self-contained, no imports from `pipeline/`): `read_video.py` extracts evenly-spaced
frames (adaptive count, ~1 per 15s, clamped 6-40) via the same ffmpeg-stderr-parsing
trick as `ffmpeg_tool.py`, plus a full `faster-whisper` transcript (multilingual
`base` model, not `base.en` - this tool isn't English-only), to a dedicated cache
dir keyed off the input path (not next to the source file - matters for a
downloaded/untrusted video). Verified on both our own `final.mp4` and a video the
user downloaded from WhatsApp. This became the actual tool used throughout the rest
of the day to self-review renders without a real video player.

## Caption text fixed to show the real script, not Whisper's mis-hearing (2026-10-25)

Self-review via `video-reader` caught burned captions reading "In 391c, the
Sarapeum Temple" instead of "In 391 CE, the Serapeum temple" - the captions were
literally Whisper's transcription of the Kokoro audio, not the original script
text, and Whisper mis-heard "391 CE" as one token "391c". Fixed in
`captions.py`/`reconcile_words()`: realigns the real script words onto Whisper's
timestamps via `difflib.SequenceMatcher`, splitting time evenly across any block
where token counts don't match 1:1 (handles exactly this "two words merged into
one ASR token" case). Captions now show the actual script, timed by Whisper.

## Visual cut rate fixed: ~1 image per 1-2 sentences, not 1 per beat (2026-10-25)

User flagged the first cut as visually too static (up to 26s on one image per
beat). Root fix: `script_parser.py` now splits a beat into multiple visual
**segments** at every inline `[ON SCREEN: ...]` cue (previously cues only worked
*before* a beat, covering the whole thing) - traced the exact bug in the old
parser that misattributed a mid-beat cue to the *next* beat. `narration.py` times
each segment proportionally by word count (no new alignment pass needed).
`visuals/resolve.py` and `assemble.py` now operate per-segment, not per-beat.
Manually densified the Alexandria test script (9 beats -> 20 segments) and
updated `yt-script/SKILL.md` so future scripts come in dense enough on their own
("one cue per beat is not enough... roughly every 1-2 sentences").

## Reference-video research -> scoped decision: fix cut rate, not visual style (2026-10-25)

User gave a downloaded reference video and asked to match its "theme." Read it
with `video-reader` and found it differs from ours on 5 axes: cut rate (2-4s,
tied to the sentence), a consistent hand-illustrated character style (not real
photos), no Ken Burns motion, a branded title/logo overlay, and floating
per-keyword captions instead of full-sentence karaoke. **Decided: fix cut rate
only** (done above) - real photo sourcing stays (supports the epistemic-
transparency differentiation angle), full illustrated-style overhaul explicitly
deferred as a much bigger, separate undertaking.

## Branded frame template: title band + centered content square (2026-10-25/26)

Built the reusable per-video template the user sketched from a reference
screenshot: solid black 1080x1920 canvas, a white title (from a new
`**Title:**` line in `script.md`, falls back to the `# Script:` heading if
missing) in a 560px top band, and every visual (real or AI) now confined to a
centered 880x880 square (`config.SQUARE_X/Y/SIZE`) instead of the full frame -
captions moved into the resulting 480px bottom black bar. `beats.json`/
`narration_meta.json` both changed shape from a bare list to `{"title":...,
"beats": [...]}`, propagated through every stage that reads them (mechanical
one-line unwrap each in `narration.py`, `alignment.py`, `visuals/resolve.py`,
`audio_mix.py`, `assemble.py`). Caught and fixed a real miss: `render.py`'s
`--from-stage narration` skips re-parsing `script.md`, so a title text edit
needs an explicit `script_parser.py` re-run first or it silently doesn't
propagate - hit this exact bug once, fixed by re-running parse->narration-
>captions by hand rather than a full `--force` rebuild.

Title styling tuned by eye via cheap single-frame previews (reusing one already-
downloaded image + a throwaway `captions.ass`) before touching the real render -
font 64->84px, pushed down from 220->300 margin, and a real rule: **a title must
be long enough to wrap two lines** (~35-50 characters / 6-9 words) or it sits
alone on one line with awkward empty space below it. Documented in
`yt-script/SKILL.md`'s new "Title" section.

## Host character: designed, pose library built (single pose for now) (2026-10-26)

User wants a recurring host character (building toward matching the reference
video's format, deferred style work from above) - saved the channel's logo
(`branding/AstralParadoxDP.png`, "Astral Paradox") as the style reference and
described a stick-limbed silhouette in the logo's hat/coat with EDITH-style
glasses. **Live-tested Pollinations' free tier has exactly one model, `sana`**
(`https://image.pollinations.ai/models`) - optimized for speed, not precise
prompt-following. 3 design iterations: attempt 1 drifted realistic/painterly,
attempt 2 (over-specified) came out as an unrelated character entirely, attempt
3 (simpler prompt) nailed a clean full-black silhouette + hat + coat but
couldn't render stick-thin legs or glasses. **Decided: simplify the brief to
match what the tool can do** rather than keep fighting it - locked in attempt 3
(`branding/character_concept_v3.png`) as the design, dropping the literal
stick-legs/glasses detail.

Built `pipeline/tools/generate_character_poses.py` (one-off, same category as
`tools/pick_voice.py`) + `rembg` for background removal (confirmed clean cutouts
in testing; its default model turned out to be a 1.02GB download, not the ~176MB
assumed going in - one-time cost, cached after). Tried 2 more gesture poses
("pointing") - both failed (claw-like hands, cropped legs) - confirmed this is a
real ceiling, not bad luck: Sana renders one consistent standing silhouette
reliably but not gesture variety. **Scoped down to a single "neutral" pose**
(`config.CHARACTER_POSES = ("neutral",)`); `character.py`'s `pose_for_beat()` is
kept as a function (not a constant) specifically so expanding the pose set later
is a one-function edit. Character **position** still cycles per segment (4
anchors, alternating left/right, 2 overflowing the square's edge) via
`character.position_for_segment()` - that's the actual source of on-screen
movement now, independent of pose.

**Real bug caught and fixed**: first compositing implementation padded the whole
video once, then chained one timed `overlay=...:enable='between(t,...)'` per
segment (20 for this video) onto that single stream. Live-tested and killed
after 15+ minutes when the output ballooned past 140MB and was still climbing
for content that should encode to ~20MB - the character popping in/out at each
segment's window reads to x264 as a scene change, forcing a keyframe every time,
and the frame flowed through all 20 chained overlay instances regardless of
which one was actually active. **Fixed by restructuring to composite per
segment**: each short Ken Burns clip gets its own single zoompan+pad+overlay
pass (one `_build_segment_clip()` call does all three now), then clips
concatenate via a cheap stream copy exactly as before. Verified: 5.4s per clip,
normal file sizes, no bloat. `final.mp4` after this fix: 1080x1920, 159.9s
(matches the audio mix), 10.4MB, clean full-file decode, correct two-line title,
character visibly moving across the square in review frames.

## PushNotification tool available but not actually working yet

User asked to be notified on their phone when a background render finishes.
`PushNotification` exists and Remote Control was confirmed connected, but the
tool itself reports **mobile push is disabled in `/config`** - needs the user to
flip that setting; not something fixable from here.

## A real "watch the video" pass caught two bugs frame-checks missed (2026-10-26)

Asked directly to watch `final.mp4`. Did the closest available thing: full
`video-reader` transcript + 32 sampled frames, read closely rather than skimmed.
That depth caught two real, previously-missed bugs that a quick frame glance
hadn't surfaced:

- **Captions were silently missing entirely from the then-current `final.mp4`.**
  Root cause: fixing the title earlier involved re-running `narration.py` to
  refresh `narration_meta.json`'s title field - but `synthesize()` rebuilds that
  file from scratch, silently wiping the `words` field that only `alignment.py`
  adds. `captions.py`'s `if not words: continue` then skipped every beat with no
  error, producing a `captions.ass` with only the title event (968 bytes, should
  be ~9.5KB). The render still "succeeded" and looked right in a quick frame
  check (title + character + background all present) - only grepping the actual
  `.ass` file content caught the missing captions.
- **Kokoro spoke a markdown character out loud.** The transcript read "What's
  asterisk not asterisk documented" - traced to the script's `*not*` (markdown
  italics for emphasis) going straight into the TTS engine as literal text.
  Confirmed via the beat's own forced-alignment output ("asterisk" is a real
  recognized word in the generated audio, not a transcription glitch). Fixed at
  the source in `script_parser.py`: new `strip_markdown_emphasis()` strips
  `*word*`/`**word**` markup (keeping the inner text) before it ever becomes
  part of a `Segment` - checked the rest of the script for other instances
  (none - this was the only one).

Both fixed, and the cascade re-run correctly: `beat_06`'s audio changed length
(25.07s -> 23.98s with "asterisk not asterisk" gone), which shifted every later
beat's start/end, which meant `mix.wav` and every segment clip from `beat_06`
onward needed regenerating too - not just the one beat. Re-ran
`alignment.py`/`captions.py`/`audio_mix.py --force` by hand, then started
`assemble.py` fresh (clips dir cleared). **User stopped the render partway
through** ("mark this, we will render tomorrow") - 5 of 20 segment clips done
(`beat_01_seg00/01`, `beat_02_seg00`, `beat_03_seg00/01`), no corrupt partial
files left behind. `captions.ass` and `mix.wav` on disk are both already correct
and current (158.8s total, down from 159.9s). **Tomorrow: just re-run
`python assemble.py library-of-alexandria-destruction` (no `--force`)** - it
resumes from the 6th clip on its own, same resumability every stage in this
pipeline already has.

## Render finished, watched for real, and voice locked in (2026-10-26)

Resumed the interrupted render (`python assemble.py library-of-alexandria-destruction`)
and hit a real bug immediately: the first resume produced a `final.mp4` that was only
36.2s instead of the expected 158.8s. Root cause - `beat_03_seg01.mp4` had been
truncated mid-write when the previous session was stopped ("moov atom not found" on
ffmpeg probe), but `assemble.py`'s resume logic (`if force or not clip_path.exists()`,
line 106) only checks that a clip file *exists*, not that it's valid, so the corrupt
clip was silently kept and the concat demuxer stopped dead at exactly that file.
Deleted the corrupt clip, re-ran to regenerate it, then had to pass `--force` to
`assemble()` as well since `if final_path.exists() and not force: return` (line 131)
was short-circuiting the reassembly step too (the broken 36.2s `final.mp4` already
"existed" from the first bad run). Final result verified clean: 1080x1920, 158.8s,
zero errors on a full-file ffmpeg decode pass.

Then did an actual watch pass with the global `video-reader` skill (frames + Whisper
transcript of the real output, not just technical probes) and found a second real bug
the technical checks couldn't have caught: `beat_02_seg00` and `beat_03_seg00` (roughly
16-30s) both show a Pixabay photo literally titled "castle-alexandria-egypt-aliens" - a
UFO-abduction composite with nothing to do with the Library of Alexandria. Traced in
`manifest.json`: both beats wanted a Wikimedia illustration, Wikimedia had no match, and
the Pixabay fallback's relevance filter (`visuals/sources.py` - "at least half the
query's significant words must appear in the hit's tags") let it through because the
photo's tag list spams "alexandria" six times plus "ancient"/"egypt" once each, clearing
the threshold on raw word-count despite having nothing to do with the query semantically.
**Not yet fixed** - flagged to the user, who has not yet said whether to fix the filter
and re-render those two segments or handle it another way.

Also found (not yet confirmed, needs a real listen): Whisper's transcript of Kokoro's
own narration consistently garbles the Greek/Ptolemaic proper nouns - "Mouseion"→
"Mausian", "Phalerum"→"fallarum", "Ptolemaic/Ptolemy"→"Tolmayic/Tolmay", "Serapeum"→
"Sarah P. M.", "391 CE"→"391 C". Burned-in captions already show the correct script text
regardless of this (fixed in an earlier session), but if Kokoro is actually
*mispronouncing* these on the audio track itself rather than Whisper just mishearing a
small ASR model on rare proper nouns, that's a separate, unfixed narration-quality issue.

**Kokoro voice preset locked in**: `am_michael`, chosen by the user after listening to
all 8 options in `voice-picker/`. Updated in `voice.md` (master +
`~/.claude/youtube/voice.md` mirror, kept in sync) and `idea.md`. Explicitly a docs-only
change per the user's instruction - not wired into the pipeline's render config, and
`library-of-alexandria-destruction` was deliberately not re-rendered with it.

## Bollywood-referenced emotion music library decided and scaffolded (2026-10-26)

User proposed using Bollywood music "for all genres" via a storytelling-first lens.
Walked through this in stages: first flagged that downloading real Bollywood tracks
and modifying them would be straightforward copyright infringement regardless of how
much the audio is altered (Content ID fingerprinting is robust to pitch/tempo/EQ
changes, and labels like T-Series/Saregama/Zee/YRF enforce aggressively) - declined to
help with that specific approach and explained why. User then clarified the actual
intent: compose original music *referencing* Bollywood's style (background-score
instrumentation/scales/rhythm, not literal songs) - confirmed that's legally sound
(copyright protects a specific recording/composition, not a genre or instrumentation)
and is exactly how the existing procedural library already works for its other
categories.

User then specified two more decisions: (1) **emotion-categorized, not genre-
categorized** - motivational/mysterious/cold/cheerful + whatever else "any possible
human emotion" covers, distilled into a practical 14-category taxonomy
(`EMOTION_CATEGORIES` in `pipeline/config.py`): motivational, mysterious, cold,
cheerful, epic, tense, dark, melancholic, romantic, reflective, hopeful, nostalgic,
awe, peaceful; (2) **music should shift mid-video** by structural part (Storytelling /
Explanation / Questionary), not stay one bed per whole video. User then explicitly
said not to compose any real tracks yet (no Bollywood reference material gathered) -
build the pipeline/generation code only.

Built, in order:

- **`[MUSIC: <emotion>]` script cue** (`pipeline/script_parser.py`) - same convention
  as `[ON SCREEN: ...]`, persists across beats until the next cue changes it, validated
  against `config.EMOTION_CATEGORIES` at parse time. Adds an `emotion` field to `Beat`;
  flows through to `narration_meta.json` for free since `narration.py` already spreads
  every beat field (`{**b, ...}`) without needing its own edit.
- **`pipeline/audio_mix.py` rewritten** from "one bed looped over the whole video" to
  multi-part crossfaded mixing: `music_parts()` groups consecutive beats sharing an
  emotion into contiguous parts; `_music_filter_graph()` builds one looped+trimmed
  ffmpeg input per part and chains `acrossfade` between them. Worked out the length-
  preserving trim math by hand (every part but the last gets trimmed to its own span +
  one crossfade's worth of extra looped material; the last part gets trimmed to
  exactly its span; each cascading crossfade consumes exactly one part's worth of
  overhang) rather than letting the naive chain shorten the total runtime by
  `(N-1)*xfade`. **Verified before trusting it**: wrote a throwaway test (3 different
  sine-tone "beds," synthetic beat metadata, outside the project tree) that calls the
  real `music_parts()`/`_music_filter_graph()` functions directly - confirmed the
  grouping logic and that a 4-beat/3-emotion timeline renders to exactly the expected
  total duration (18.000s vs 18.000s expected) with no dropout at the crossfade
  boundaries (RMS dips smoothly, never to silence). The old genre-based
  `pick_music_bed()` function is kept (renamed as legacy/deprecated in a comment) but
  no longer called - nothing deleted, in case of rollback.
- **`render.py`'s CLI** changed from required `--category`/`--mood` to optional
  `--default-emotion` (fallback for any beat with no `[MUSIC: ...]` cue in scope).
- **New parallel generator system** under `assets/audio/src/`, fully separate from the
  genre library's `registry.py`/`generate.py`/`metadata_gen.py`/`validate.py` (so
  neither can break the other): `bollywood_primitives.py` (new, real, smoke-tested
  synthesis primitives - `tabla_hit`/`dholak_hit` for pitched hand-drum strokes with a
  bass-stroke pitch bend, `sitar_pluck` with a jawari-buzz approximation via mild
  saturation and optional meend pitch-bend, `tanpura_drone` built from cyclical
  sitar-plucks on a fixed Sa-Pa-Sa-Sa-style pattern, `bansuri_tone` (breathy vibrato'd
  flute), `harmonium_drone` (detuned-reed tremolo pad), `string_section_swell`
  (legato pad + dynamics envelope) - all built from existing `audio_lib.py` primitives,
  none sampled from anything), `registry_bollywood.py` (empty `MUSIC` list, ready
  pattern), `generate_bollywood.py`, `metadata_gen_bollywood.py`,
  `validate_bollywood.py` - all run end-to-end clean with zero assets (confirms the
  scaffolding itself works, not just that it imports).
- **`Assets_audio/music_bollywood/<emotion>/`** - 14 empty folders, one per emotion,
  plus `metadata/music_catalog_bollywood.csv` (header-only) and a README documenting
  the "style-referenced, never sampled" legal line and current status.
- 14 per-emotion module stubs in `assets/audio/src/bollywood_music/` (docstring only,
  no functions yet - exactly where a composition brief will land once there's
  reference material to study).

**What this replaces**: `Assets_audio/music/` (the topic-based genre library, 50
tracks) is left on disk untouched but is no longer selected by the production
pipeline - `Assets_audio/sfx/` is unaffected and stays in active use (user explicitly
said SFX is fine, only music changes). **Status: infrastructure only - zero Bollywood-
referenced tracks exist yet.** Waiting on the user to gather real Bollywood
background-score reference material and give a composition brief per emotion before
any track gets composed - same pattern as how the original genre library waited for a
full spec before the first track was rendered.

## Google One AI Student offer investigated, verified genuine, and claimed (2026-10-26)

Side track from the channel work, logged for continuity since it involves an account
that may matter later (e.g. if a paid Gemini API tier is ever needed for the
pipeline). User pasted a `one.google.com/ai-student` link with ad-tracking params
(`utm_source=gemini`, `gclid`, etc.) and asked whether it was genuine or a scam.

**Verification process**: checked via `WebFetch` first - the URL 302-redirects to
`accounts.google.com/ServiceLogin` with a `continue=` back to the same
`one.google.com/ai-student` page, i.e. the whole chain stays on canonical Google
domains, no lookalike/typosquat host anywhere. Confirmed visually once the Chrome
extension connected (it needed a restart/reconnect first - two earlier
`tabs_context_mcp` calls failed with "Browser extension is not connected" before a
third succeeded): real Google One branding, two real plans (**Google AI Plus** - free
for 12 months then ₹399/mo, 400GB - and **Google AI Pro** - ₹489/mo up to 4 years, 74%
off ₹1,950, 5TB + YouTube Premium Lite), working "Get student offer" buttons, and
standard Google legal fine print/footnotes. Verdict: genuine, not a scam - it's
Google's own self-promotion of its real student discount, not a third party
impersonating Google.

**Eligibility question**: user disclosed their actual status progressively - first
"college completed in June, one year drop, technically not a student," then corrected
to "diploma still pending from college, only last sem's marksheet submitted." Declined
to help fabricate or game the verification, but once the user clarified the document
was genuine and accurately reflected their real (pending-degree) status, treated that
as legitimate rather than coached on how to deceive the checker. Read the actual
submitted PDF (`Marksheet.pdf`) at the user's request and flagged two real problems
before Google's own review caught the same two: (1) the document names "GTU" (Gujarat
Technological University, the affiliating body) rather than the user's actual college,
likely mismatching whatever they typed into the verification form; (2) the document is
a **Semester III** grade card (exam Dec 2024, joined 2023 on a 3-year/6-semester
program) - roughly 20 months stale relative to now, not the final-semester document
its "last sem's result" framing implied. First verification attempt was rejected for
exactly these two reasons (screenshot confirmed). **User then completed verification
successfully on a different Google account** (not `shahbazkhan74659@gmail.com`).

**Gemini API vs. Google One AI Plus/Pro clarified** (user's next question, after
wanting to create a Gemini API key that had failed on the free tier, hoping the new
Plus subscription would raise its limits): these are two separate products sharing the
same underlying Gemini models but entirely separate billing - Google One AI Plus/Pro
is a consumer subscription (raises limits in the Gemini chat app/website only);
the Gemini Developer API (Google AI Studio/Vertex AI) is billed through a separate
Google Cloud Billing Account per project, regardless of any Google One subscription on
the account. Creating an API key on the Plus-subscribed account would land on the same
free tier as any other account - the subscription doesn't carry over. Confirmed
separately that Plus/Pro benefits in the **Gemini chat app** do follow the verified
Google account itself (not a specific installed app) - signing into `gemini.google.com`
or the mobile app with that account is enough, no separate Google One app install
needed.

**Net result**: Google One AI Plus (or Pro) is now active on a secondary Google
account, verified via a real diploma marksheet. It does **not** unlock or discount the
Gemini Developer API - that would need a separate Google Cloud Billing Account if ever
needed for this project's pipeline.

## Veo re-visualization prompt drafted and run through Gemini (2026-10-26)

User asked for a "master prompt for Gemini" to turn `library-of-alexandria-destruction`
into a realistic-4K-visuals version with the same audio/length. Flagged the real
constraint first: Veo can't lock to external audio sample-accurately and generates
fixed-ish clip lengths, so the actual plan is per-segment regeneration (one Veo prompt
per existing visual segment, each with its already-known exact duration) to be dropped
into `assemble.py`'s existing per-segment compositing - not a single "regenerate the
whole video" instruction. Built `gemini_master_prompt.md` with all 20 segments' exact
durations/text/confidence tags pulled straight from `narration_meta.json`, plus a rule
extending the channel's epistemic-transparency angle into the new visuals: SOLID beats
get straightforward photorealistic treatment, CONTESTED/UNCERTAIN beats get a visible
"reconstructed/uncertain" visual cue (desaturation/grain/blur), and the caliph myth
(BEAT 5/UNCERTAIN) gets illustrated-manuscript treatment rather than being rendered as
if it documentarily happened.

Ran it for real in Chrome: navigated to gemini.google.com/app (already signed into the
Plus-verified account), hit the 10MB file-attachment limit on `final.mp4` (13.2MB) so
sent the prompt as self-contained text instead of with the video attached (adjusted the
wording accordingly - no false "attached" claim). Typing the prompt via the normal
`computer` tool's keystroke simulation risked premature submission on every embedded
newline (Gemini's input submits on Enter), so used `javascript_tool` +
`document.execCommand('insertText', ...)` on the focused contenteditable instead -
inserts text without firing real Enter keypresses, verified by checking the box's
text length before sending. Switched the model from the default Flash to 3.1 Pro
(unlocked by the Plus plan; "4 Argon" was visible but locked, presumably Pro/Ultra-only)
before sending, since this is a detailed creative-writing task worth the stronger model.

Gemini's response (saved to `veo_prompts.md`): all 20 prompts, correctly honoring the
confidence-treatment rule without being told to re-state it, and correctly leaving the
host-character silhouette out of the generated-footage descriptions (it stays a
separate compositing layer, not baked into Veo's output) - confirms the prompt
communicated the pipeline's actual architecture correctly. **Status: prompts only,
nothing generated in Veo yet.** Next step when the user wants it: generate each clip,
save to `build/visuals_v2/<segment_id>.mp4`, then `assemble.py`'s
`_build_segment_clip()` needs a small change to accept a video clip (trim/loop to the
segment's exact duration, same as it already does for a still image) instead of
requiring one.

## First Veo clip generated as a proof of concept - `beat_01_seg00` (2026-10-26)

User asked to actually generate the first clip. Done live in Chrome via Gemini's
dedicated **Videos** tool (`gemini.google.com/videos`, not the regular chat box) -
set aspect ratio to Portrait (9:16) before submitting, pasted prompt #1 from
`veo_prompts.md` (the caliph-myth illuminated-manuscript prompt), ran on the Pro
model. Generation took under a minute. Downloaded the result (`Download video`
button in the player controls - had to re-locate it after an initial `find`-based
click landed near the right spot but needed a direct coordinate click to actually
trigger the save; a same-named-looking `GeminiSetup.exe` already sitting in
Downloads from earlier in the session was unrelated, not something this action
caused) and moved it into
`videos/library-of-alexandria-destruction/build/visuals_v2/beat_01_seg00.mp4`.

**Result matches the brief well**: illuminated-manuscript style, cracked parchment,
gold leaf, Arabic calligraphy border, the caliph figure with a book pile - reads
clearly as "illustrated legend," not a staged documentary reenactment, which was
the whole point of that confidence-treatment rule.

**Measured specs**: 720x1280 (9:16, correct), 10.01s, 24fps, H.264 + its own
Veo-generated AAC audio track. Two gaps vs. what the final pipeline needs, both
already expected and both exactly what the planned `assemble.py` change will cover
automatically: (1) target duration for this segment is 7.71s, not 10.01s - needs
trimming; (2) Veo bakes in its own ambient audio, which must be stripped/muted
before compositing so it doesn't clash with the real narration+music mix.

**Status**: 1 of 20 segments generated, as a proof of concept only - the other 19
and the actual `assemble.py` integration are still pending, waiting on whether the
user wants the full batch generated now or wants to review a few more first.

## Carried-forward open items (as of end of day, 2026-10-26)

0. **Veo re-visualization**: 1 of 20 segment clips generated (`beat_01_seg00`,
   proof of concept, in `build/visuals_v2/`). Waiting on the user's call on whether
   to generate the other 19 now. Either way, `assemble.py`'s `_build_segment_clip()`
   still needs the small change to accept a video clip (trim to exact duration,
   strip Veo's baked-in audio) instead of requiring a still image - not started.
1. **Fix the Pixabay relevance-filter bug** (above) and re-render `beat_02_seg00`/
   `beat_03_seg00` - still open, waiting on the user's call on approach.
2. **Confirm by ear** whether Kokoro is actually mispronouncing the Greek/Ptolemaic
   proper nouns (above) or Whisper's `base` model is just mishearing them.
3. **Wire `am_michael` into the actual pipeline render config** (now decided, not yet
   implemented - see above) and re-render the test video with it once ready.
4. Character pose variety: only "neutral" exists. Options already discussed if
   wanted later - keep trying Pollinations prompts (likely same ceiling), hand-
   edit poses in GIMP/Photopea (confirmed working, free), or accept single-pose
   permanently since position-cycling already carries the movement.
5. The deferred full illustrated-visual-style match (consistent AI art style for
   every background, not just the character) and the reference video's floating-
   keyword caption style are still open, explicitly scoped out of today's work.
6. Enable mobile push notifications in `/config` if still wanted (see above).
7. **Bollywood-referenced emotion music library**: gather real Bollywood background-
   score reference material and write a composition brief per emotion (14 categories -
   see above), then compose/register/generate actual tracks via
   `assets/audio/src/bollywood_music/<emotion>.py` + `registry_bollywood.py` +
   `generate_bollywood.py`. Nothing composed yet - infrastructure only.
7b. Old genre-based `Assets_audio/music/`: now superseded for production, so its
   pending human listen-through (7 of 8 categories, only `history/` reviewed) is no
   longer blocking a real upload - SFX's listen-through (all 50, none reviewed) is
   still relevant since SFX stays in use.
8. Create the actual YouTube channel — doesn't exist yet.
9. Audio library possible future additions (not started, not blocking):
   a rendered-preview/audition system with a timestamped index, and a
   proper `argparse`-style CLI (`generate music --category X`) if the
   simple `--category`/`--id` filter in `generate.py` stops being enough.
10. If another music category turns out to have the same "too similar /
   inconsistent loudness" problem `history.py` had, the fix pattern is
   already built and reusable: `composition.render_bed`'s optional
   `target_lufs`/`pre_limit_drive` params - no need to reinvent it.
11. Render pipeline possible future work (not started, not blocking): the
    Smithsonian source in `visuals/sources.py` was live-tested and found to
    rarely return usable image URLs (0/30 across test queries) - kept as a
    last-priority fallback, not worth more engineering time unless it becomes a
    real gap; video-clip visuals (vs. still images) and a true word-by-word
    "TikTok style" caption mode (vs. the current karaoke-highlight line groups)
   are both easy future additions if wanted, not required for v1.

## Progress log — 2026-10-26 (continued): pure-Gemini visuals test, caption redesign, Hindi/Hinglish pivot

### 1. `am_michael` voice wiring bug found and fixed

`pipeline/config.py`'s `get_voice_preset()` was silently falling back to the
`af_heart` default on every render - its regex expected
`` `voice`...[CONFIRMED] `` but `voice.md`'s real line format is
`[CONFIRMED]: `voice``, so it never matched. Fixed the regex
(`r"Kokoro voice preset.*?\[CONFIRMED\].*?`([a-z]{2}_[a-z]+)`"`); confirmed
`config.get_voice_preset()` now correctly returns `am_michael`.

### 2. Gemini/Veo square-framing bug found and fixed

`gemini_master_prompt.md` was instructing Gemini to generate every Veo clip
in a full 9:16 vertical frame, but a clip only ever fills the branded
template's centered content square (880x880, `config.SQUARE_SIZE`) - the
title band and caption bar around it are fixed and separate. Fixed the
per-clip format instructions to ask for a 1:1 square composition (or
Veo's closest supported ratio, framed so a center-crop doesn't cut off the
subject), and updated the note on `assemble.py`'s still-pending video-clip
support to say it should scale/crop to the square. The one already-generated
Veo clip (`beat_01_seg00`, 720x1280) predates this fix.

### 3. Pure-Gemini-visuals validation render built: `library-of-alexandria-destruction-gemini-test`

New slug (`videos/library-of-alexandria-destruction-gemini-test/`, separate
from the production `library-of-alexandria-destruction` render) built to
validate `am_michael` + square-cropped Gemini/Veo visuals before committing
to the full 20-segment video. Scoped to the first 4 beats / 7 segments
(HOOK through BEAT 2, matching `veo_prompts.md` entries #1-7, ~62-70s).

**Code changes** (all still live in the pipeline):
- `pipeline/assemble.py`'s `_build_segment_clip()` - added a video-clip
  branch (`VIDEO_EXTS`): scale-to-fill + center-crop to the square
  (`force_original_aspect_ratio=increase` + `crop`, no x/y needed since
  `crop` centers by default) and `-stream_loop`/`-t` to loop/trim a clip to
  the segment's exact duration, instead of the still-image zoompan path.
  Only `[out]`/`[bg]` (video-only) is ever mapped, so a Veo clip's own
  baked-in audio is implicitly dropped.
- `pipeline/audio_mix.py` + `render.py` - added `--no-music` (skips
  `music_parts()`/`pick_emotion_bed()` entirely). Needed because the
  Bollywood-referenced emotion music library (see 2026-10-26 entry above)
  has zero tracks composed for any emotion yet, so the normal music path
  hard-crashes (`ValueError`) on every render right now. Purely additive,
  zero effect without the flag.
- `pipeline/review.py` - fixed a real pre-existing bug: `extract_frames()`
  read `narration_meta.json` without unwrapping the `{"title":...,
  "beats":[...]}` wrapper (every other stage got this fix when the format
  changed; this one was missed), crashing with `TypeError: string indices
  must be integers`. One-line fix.

**Generation**: 7 segments, pure Gemini-sourced (no Wikimedia/Pixabay/
Pollinations) - `beat_01_seg00`/`beat_01_seg01` as Veo video clips
(`gemini.google.com/videos`), `beat_02_seg00` through `beat_04_seg01` as
Gemini-generated still images (`gemini.google.com/app`, plain chat image
gen) once the Veo daily generation quota ran out mid-batch. Real friction
hit along the way:
- Gemini's `/videos` page UI was flaky under Chrome automation - the aspect
  ratio dropdown and prompt textbox intermittently didn't respond to normal
  clicks (`computer` tool), traced to the page using a hidden off-screen
  mirror `contenteditable` for the "real" input; worked around with
  `javascript_tool` dispatching a full synthetic pointer-event sequence
  (pointerdown/mousedown/pointerup/mouseup/click) instead of a single click.
- Nearly downloaded the wrong clip once: a stale pre-existing "Medieval
  Arabic Manuscript Animation" chat (from an earlier session) looked like
  the fresh retry's output in the Library view. User caught it before
  download. Lesson: verify a generation by its own chat URL/session, not by
  a Library thumbnail that happens to look similar.
- `beat_01_seg00` ended up reusing the earlier-session proof-of-concept clip
  (same prompt, already verified 720x1280/10.01s) rather than regenerating,
  since Veo's quota ran out before it could be redone.
- Gemini's image-gen "Download image" (the `...` menu) is a real local
  download; the on-image circular download icon is a *public share-link*
  flow instead - closed that dialog without creating a link once by mistake,
  caught before anything was shared.
- All 5 Gemini images came back natively 2048x2048 (exact square), no
  cropping/distortion needed.

**A real self-inflicted bug mid-session**: re-rendering later with
`--from-stage visuals` (instead of `--from-stage captions`) force-re-resolved
every segment through the normal Wikimedia/NASA/Pixabay/Pollinations chain
using the OLD English `[ON SCREEN: ...]` cues still kept in script.md for
reference - silently overwriting 4 of the 5 Gemini image files on disk
(same destination filename) with random stock photos (the exact
"castle-alexandria-egypt-aliens" mismatch bug from the production slug's
known open item recurred here too). Recovered because the original
downloaded PNGs were still sitting in `~/Downloads/` untouched; restored
and rebuilt `manifest.json` by hand. **Lesson reinforced**: `--from-stage`
forces every stage from that point on including the named one - use the
*first stage that actually changed*, never a stage whose cached output
(like a hand-seeded `manifest.json`) needs to be preserved.

Verified via frame reads + the `video-reader` skill (transcript): branded
frame, square-crop, and SOLID-vs-UNCERTAIN visual treatment (crisp
photorealistic vs. desaturated/hazy) all read correctly on both the video
clips and the stills; captions show the real script text even where Whisper
mis-hears proper nouns (pre-existing, unrelated behavior, confirmed still
working).

### 4. Character overlay removed (toggle, not deleted) + captions redesigned

Per request: dropped the host-character silhouette "for now" -
`config.SHOW_CHARACTER = False` (new flag) with `assemble.py`'s
`_build_segment_clip()` branching to skip the character input/overlay
entirely when off - one flip to bring it back later.

Captions rebuilt from the 6-word karaoke-line style to one word on screen
at a time: centered in the full frame (`\an5`, was bottom-bar), plain
yellow/gold (no more two-tone karaoke progression), with a quick scale-up
"pop" (`\fscx60\fscy60\t(0,120,\fscx115\fscy115)\t(120,180,\fscx100\fscy100)`)
on every word - each word's ASS event spans only its own spoken timing, no
accumulated line. Font size tuned down after a look (110 -> 70).

Added a scoped number-word-to-digit converter (`_convert_number_token` in
`captions.py`): a spelled-out number is only converted to digits when
directly hyphen-compounded, in the SAME script token, with a recognized
year/date/measurement-unit suffix (`three-hundred-year` -> `300-year`,
`forty-two-kg` -> `42-kg`) - deliberately leaves a bare number word alone
(the pronoun "one" in "the most famous one", a plain count like "three
different suspects") since those aren't years/dates/figures and converting
them would misfire on normal English. Narration audio is unaffected - this
only changes what's burned into the subtitle.

### 5. Hindi/Hinglish narration pivot (in progress)

Request: switch narration to Hindi-dominant Hindustani (Hindi + Urdu +
English mixed), captions to stay Latin-script but show the Hinglish
transliteration of what's actually spoken (not an English translation).

**Verified Kokoro can actually do this**: `hm_omega` voice + `lang="hi"`
(passed through to `phonemizer`/espeak-ng, not documented in
`kokoro_onnx`'s own docstring but works) produced genuinely correct Hindi
speech - independently confirmed by transcribing the output with a
multilingual Whisper model, which detected `hi` at 95.6% confidence and
transcribed back essentially the same sentence (in Perso-Arabic/Urdu
script, not Devanagari - Whisper's Hindi model doesn't reliably stay in one
script, a finding that shaped the approach below).

**Real technical snag found**: the existing caption-timing approach
(`reconcile_words()`, text-matching original script words onto Whisper's
transcript via `difflib`) cannot work for Hindi - `_normalize()` strips
everything outside `a-z0-9`, so Devanagari/Urdu script collapses to empty
strings before matching even starts, and Whisper's script-switching makes
a same-script match impossible to rely on anyway. Solution: a new
positional-zip mode (`_zip_positional()` in `captions.py`) - when an
optional `build/romanized.json` (`{"<beat_id>": "roman hinglish text..."}`)
exists for a slug, captions pair Whisper's own word-level *timestamps*
directly against our own Romanized word list by position/index, ignoring
Whisper's transcribed text entirely. Approximate (word counts between our
Hinglish text and Whisper's segmentation won't match exactly - observed
~5-7 word drift per beat, meaning the last few words of a beat may go
uncaptioned), but workable for a validation pass. Zero effect on the
English production slug (no `romanized.json` there).

**Other code changes**: `config.WHISPER_MODEL_SIZE` switched from
`base.en` to multilingual `base` (English-only can't transcribe Hindi at
all; multilingual still handles English fine - same reasoning the global
`video-reader` skill already uses). `narration.py`/`render.py` gained a
`--lang` flag (default `en-us`, threaded into `kokoro.create(..., lang=)`,
previously hardcoded).

**Content**: rewrote `script.md`'s narration into Hindi-dominant
Hindustani (Devanagari), keeping Urdu-origin words natural to spoken
Hindi (यकीन/yakeen, सबूत/saboot, मुजरिम/mujrim, रिवायत/rivayat,
मुमकिन/mumkin) and English technical/proper nouns as-is (library,
Mouseion, Ptolemaic, Ptolemy, Demetrius, Phalerum, myth, idea, role) -
matches how real Hindi YouTube documentary narration actually code-switches.
Preserved the exact beat/segment/cue structure (same 4 beats, 7 segments,
same `[ON SCREEN: ...]` cue positions) so the existing pure-Gemini
`manifest.json` entries from §3 stay valid without touching visuals again.
Hand-wrote the matching `build/romanized.json`. On-screen Title band left
in English (channel branding, not narration-driven) - not asked to change,
flagged as a judgment call.

**Status**: narration synthesized (`hm_omega`, `lang=hi`, 75.7s) and aligned
(multilingual Whisper, 222 words across 4 beats) successfully. Manifest
recovery from the `--from-stage visuals` mistake (§3) done. Re-rendered from
`--from-stage captions --no-music` and verified: frame reads confirmed
visuals/captions render correctly (Hinglish words like "Isse", "Aaj",
"library" showing in sync, including right at the last word of a beat -
`_zip_positional()`'s approximate word-count drift didn't cause visible
desync here), and `video-reader`'s transcript independently detected the
whole 76s track as `hi` (Hindi) and came back a near word-for-word phonetic
match to the Devanagari script (again in Perso-Arabic script, not
Devanagari - same Whisper quirk). Confirmed good.

### 6. Hindi:English ratio tried at 60:40, reverted back to mostly-Hindi

Follow-up request: shift the code-switching ratio to roughly 60% Hindi /
40% English by word count (noticeably more than §5's handful of English
proper nouns, which was closer to 90:10). Rewrote all 4 beats' narration
and `romanized.json` with much heavier English content-word substitution
(verbs/nouns/adjectives switched to English, Hindi kept for grammar/
connectors - "Before you believe कि खलीफा ne...", "Tradition के मुताबिक,
Demetrius of Phalerum ne yeh idea..."), hand-counted at build time to
~59.5:40.5 Hindi:English across the 4 beats. Re-synthesized
(`hm_omega`/`hi`, now 97.0s - longer, more words overall) and re-rendered.

Verified the code-switch actually came through in the audio (not just on
paper): `video-reader`'s transcript of the new render clearly surfaced
plain English phrases throughout ("before you believe", "let me tell you",
"real story", "historians argue", "almost certainly exaggerated") alongside
the Hindi portions, confirming Kokoro's `hi` voice did pronounce the
English-heavy mix as intended. Caveat given honestly: this only confirms
the ratio/intelligibility, not whether the Hindi<->English switch points
sound smooth or choppy by ear.

**User reviewed and reverted** - "previous one is ok" - back to the §5
mostly-Hindi version. Restored `script.md` and `build/romanized.json` to
the §5 text, re-ran narration/alignment/render. Hit one self-caused bug
doing the revert: ran `narration.py --force` straight after restoring
`script.md` without re-running `script_parser.py` first, so it
re-synthesized from the *stale* `beats.json` (still holding the 60:40
text) - durations came back identical to the 60:40 run (97.0s), which is
what caught it. **Lesson**: restoring `script.md` alone doesn't revert
anything downstream - `beats.json` is a separate cached artifact and needs
its own re-parse (`script_parser.parse_script()` +
`save_beats_json()`) before narration/alignment/render will see the
reverted text. Re-parsed, re-synthesized, re-rendered - durations matched
the known-good §5 run exactly (75.7s narration, 76.0s final), manifest
confirmed still pointing at all 7 original pure-Gemini assets.

Current state: `videos/library-of-alexandria-destruction-gemini-test/output/final.mp4`
is the §5 mostly-Hindi version (76.0s), user-confirmed good.

# Progress log — 2026-10-27

## Kokoro voice preset reverted: `am_michael` → `af_bella`

User reverted the locked-in voice choice back to `af_bella` (one of the original 8
options in `C:\YouTube\voice-picker\`), superseding `am_michael` (the 2026-10-26
decision). Updated the three places that recorded the old choice, consistent with
how the `am_michael` decision itself was logged: `voice.md` (master) and its
`~/.claude/youtube/voice.md` mirror (kept byte-identical, same as every prior sync),
and `idea.md`'s "Kokoro voice preset" section.

Same caveat as before applies unchanged: not wired into the pipeline's actual render
config and not used in any actual render yet — `config.get_voice_preset()` reads the
`[CONFIRMED]` backtick value straight out of `voice.md`, so the next render that
doesn't pass an explicit `--voice` override will pick up `af_bella` automatically,
but `library-of-alexandria-destruction`'s existing render was not re-rendered for
this change, same as last time.

## Hindi/Hinglish pilot reverted to English with an "Indian tone" experiment (2026-10-27)

User asked to revert `library-of-alexandria-destruction-gemini-test`'s narration and
captions back to pure English (undoing the 2026-10-26 Hindi/Hinglish pivot), spoken
with an "Indian tone," with numbers showing as digits in the subtitle.

**Checked what Kokoro actually ships first**: listed all 54 bundled voices via
`Kokoro.get_voices()` (previously only the 8-voice shortlist in
`tools/pick_voice.py` had been seen) — confirmed there is no dedicated Indian-English
preset. Voices are grouped by language prefix: `a`=American English, `b`=British
English, `h`=Hindi (`hf_alpha`, `hf_beta`, `hm_omega`, `hm_psi`), plus Spanish/
French/Italian/Japanese/Portuguese/Mandarin groups. So "Indian tone" for *English*
narration isn't a preset switch — it's an untested combination: feed English text
through a Hindi-trained voice under `--lang en-us` instead of `hi`. Generated all 4
Hindi-voice candidates speaking the standard English test line (via the existing
`pick_voice.py` tool, unmodified) to `voice-picker/hf_alpha.wav`/`hf_beta.wav`/
`hm_omega.wav`/`hm_psi.wav` for the user to actually listen to and pick from — same
test-before-locking pattern as every other voice decision in this project. Not yet
picked; `hm_omega` used as a provisional, unlocked choice for the render below (it
had already proven cleanest in the 2026-10-26 Hindi testing).

**Reverted the content**: `script.md` rewritten back to the original English HOOK/
THE TURN/BEAT 1/BEAT 2 text (byte-for-byte the same beats as the production
`library-of-alexandria-destruction/script.md`), keeping the identical 4-beat/
7-segment structure and `[ON SCREEN: ...]` cue positions the Hindi version used -
confirmed `manifest.json` (the Gemini/Veo visual resolutions) stays valid untouched,
no re-resolution needed. `build/romanized.json` (the Hinglish positional-caption
workaround) moved aside to `romanized_hindi_test.json.bak` rather than deleted, so
`captions.py` falls back to its normal English `reconcile_words()` text-matching
path automatically.

**Re-ran only the affected stages** (not `render.py`'s blanket `--force`, which would
also force the visuals stage and re-trigger the exact "overwrites Gemini images with
stock fallbacks" bug logged on 2026-10-26): `script_parser.py` (re-parse - always
reruns) → `narration.py --voice hm_omega --lang en-us --force` (65.2s, 4 beats) →
`alignment.py --force` (160/161 words aligned) → `captions.py` (no force flag
needed, always rewrites) → `audio_mix.py --no-music --force` (Bollywood emotion
library still has zero tracks, same as 2026-10-26) → `assemble.py --force` (ran
long enough to background; finished clean, 7 segment clips rebuilt against the new
English timing).

**Verified**: captions grepped directly for the number-conversion rule - confirmed
`300-year`, `40,000`, `700,000` all render as digits (the hyphen-compound rule in
`captions.py::_convert_number_token` plus the script's own already-numeric text),
restoring the behavior the Hindi captions had bypassed. Final output: 1080x1920,
65.5s (matches the audio mix exactly), clean full-file ffmpeg decode.

**`hf_alpha` confirmed (2026-10-27, same day)**: user listened to the 4 candidates
and picked `hf_alpha`, superseding the `hm_omega` placeholder. Re-ran the same
affected stages with it (`narration.py --voice hf_alpha --lang en-us --force` →
62.5s, 4 beats → `alignment.py --force` → 158/161 words aligned → `captions.py` →
`audio_mix.py --no-music --force` → 62.8s → `assemble.py --force`, backgrounded,
finished clean). Final output: 1080x1920, 62.8s (matches the audio mix exactly),
clean full-file ffmpeg decode. Documented directly in this video's `script.md` as
confirmed. **Scoped to this test video only** - the channel-wide production preset
in `voice.md`/`idea.md` stays `af_bella`; `hf_alpha` is not an "Indian tone" option
recorded anywhere as a channel-wide default, since the user hasn't said whether
they want it to replace `af_bella` for actual production or whether this stays a
scoped experiment on the gemini-test slug only.

## Randomized Ken Burns motion added - and a real pre-existing zoom-in bug found and fixed (2026-10-27)

User asked for every still image to move on screen - left-to-right, right-to-left,
zoom in, zoom out, random directions - instead of the one fixed "always centered
zoom-in" `assemble.py` had shipped with since the render pipeline was first built
(its own old docstring literally said "panning is deliberately skipped in v1").

**Built** a 10-motion pool in `assemble.py`: `zoom_in`, `zoom_out`, 4 straight pans
(left<->right, top<->bottom), 4 diagonal pans (all 4 corner-to-corner directions) -
covers the literal ask (L-R/R-L/zoom in/zoom out) plus genuine direction variety for
"random directions." `motion_for_segment(seg_id)` assigns one per segment via
`random.Random(seg_id).choice(...)` - randomized across segments, but deterministic
per segment id (seeded by the id itself, not a shared RNG stream) so a partial
rebuild doesn't reshuffle unrelated segments' motions. `_motion_exprs()` generates
the corresponding zoompan `z`/`x`/`y` expressions - zoom motions animate `z` with
`x`/`y` re-centered every frame; pan motions hold `z` fixed at a new `PAN_ZOOM=1.2`
(vs. the zoom motions' `TARGET_ZOOM=1.12`) and animate `x`/`y` linearly across the
clip's frame count instead, which needed more headroom than the old subtle
zoom-only margin to pan across without ever exposing the padded edges.

**Verified by pixel-diffing, not just a clean ffmpeg exit code** - a clip can
"succeed" while being visually static (exactly what turned out to be happening
here). First attempt at verification used *input-side* `-ss` seeking
(`ffmpeg -ss T -i file`), which snaps to the nearest keyframe - these clips have
essentially one keyframe at frame 0 (60-frame clips, far under any normal GOP
size), so every "end frame" sample was silently reading frame 0 again, masking
any real motion. Caught by comparing against a known-working motion (the pans) and
finding the SAME near-zero result for frame 0 vs frame 0 regardless of motion type -
switched to *output-side* seeking (`ffmpeg -i file -ss T`, forces accurate decode)
and got the expected large per-motion pixel differences.

**Real bug found this way**: with accurate seeking, 9 of the 10 motions showed
2.2-2.3M differing bytes out of 6.2M between first/last frame - `zoom_in` showed
only 30. Root cause: `zoompan`'s internal `zoom` state does not reliably default to
`1.0` on this machine's ffmpeg build, so the original `min(zoom+step,TARGET_ZOOM)`
expression (unchanged from the pipeline's original 2026-10-25 Ken Burns
implementation) was starting already at-or-above `TARGET_ZOOM` and the `min()` just
clamped it flat for the entire clip - a silent, purely cosmetic failure (ffmpeg
exits 0, correct resolution/duration, just no visible zoom). `zoom_out` had
accidentally avoided this same bug because it already forced its start value
explicitly via `if(eq(on,0),...)` for an unrelated reason (needing to start at
`TARGET_ZOOM` rather than `1.0`). Fixed `zoom_in` the same defensive way:
`if(eq(on,0),1.0,min(zoom+step,TARGET_ZOOM))` - confirmed fixed (2.18M/6.2M
differing bytes after, in line with every other motion). **This means the
production `library-of-alexandria-destruction` render's "centered Ken Burns
zoom-in" has been effectively near-static this whole time**, since before today's
change - not a regression introduced by this work, a pre-existing bug this work
happened to surface by actually measuring motion instead of trusting a clean exit
code.

**Re-rendered both existing test videos** to apply this - `assemble.py --force`
only (narration/alignment/visuals/audio untouched, same "force only the stage that
actually changed" lesson from the 2026-10-26 entries above): `library-of-
alexandria-destruction` (20 clips, 1080x1920, 158.8s - unchanged duration, as
expected since only motion changed, not timing) and `library-of-alexandria-
destruction-gemini-test` (7 clips - 2 of them Veo video clips, unaffected by this
change since motion only applies to the still-image branch; 1080x1920, 62.8s,
also unchanged duration). Both passed a clean full-file ffmpeg decode.

**Not yet done**: an actual watch of either re-rendered video - this was verified
by pixel-diffing sampled frames (confirms motion exists and roughly how much), not
by eye for whether any specific motion choice looks good on a specific image (e.g.
whether a diagonal pan ever crops out something important in a photo with an
off-center subject).

## `hf_alpha` promoted from scoped test to channel-wide global default; branded frame + random motion confirmed global too (2026-10-27, same day)

User closed the open scoping question from earlier today: `hf_alpha` (the
English-with-Indian-tone voice confirmed on the `library-of-alexandria-destruction-
gemini-test` slug) is now the **global production voice preset** for every video
made going forward, not a scoped experiment. Also explicitly confirmed the branded
frame template and today's randomized image-motion work are project-wide standards,
not per-test-video behavior - both already were, by construction (shared code in
`pipeline/config.py`/`assemble.py`, no per-slug setting exists for either), so this
was mainly about formalizing the decision record rather than a code change.

Updated `voice.md` (master + `~/.claude/youtube/voice.md` mirror, kept in sync) and
`idea.md`'s "Kokoro voice preset" section to record `hf_alpha` + `--lang en-us` as
the global default, superseding `af_bella` (reverted to earlier the same day, never
used in any render). Verified `config.get_voice_preset()` now resolves to
`hf_alpha` directly from `voice.md`. Also expanded `idea.md`'s "Render pipeline and
visual identity" section to state explicitly that the branded frame (shared
`SQUARE_SIZE`/`SQUARE_X`/`SQUARE_Y`/`WIDTH`/`HEIGHT` constants) and the new 10-motion
randomized Ken Burns system both apply to every video unconditionally.

**Not retroactively applied to existing renders** - same pattern as every prior
voice decision (`af_heart`→`am_michael`→`af_bella`→`hf_alpha`): this governs videos
made from here on; `library-of-alexandria-destruction`'s existing render still uses
its original test voice unless/until the user asks for an actual re-render with the
new global default.

## Visual sourcing priority flipped: AI-generated primary, real sources → evidence inset (2026-10-27, same day)

Biggest design conversation of the day. Started from a scheduling question ("run this
without my laptop on") that led nowhere useful (Gemini has no API - confirmed again
that free-tier image/video generation returns 0 quota and the user's Google One
subscription doesn't unlock API billing, so Gemini only works via a live, logged-in
Chrome session) - but the user's actual resolution was simpler than any scheduling
fix: **no deployment at all**. They'll manually start a fresh Claude Code conversation
around 10 PM with Chrome connected and logged into Gemini, laptop staying on/connected
through the night, and drive Gemini generation live from inside that session; Pollinations
("already settled") stays the code-automatable fallback. That resolved the entire
automation tension without building anything - the actual ask that followed was a
content/architecture redesign, not infrastructure: **flip which sources are "primary"
visuals vs. which are reduced to "evidence."**

Went through full plan-mode: an Explore agent confirmed the exact pre-existing cue
grammar in the global `yt-script`/`yt-factcheck` skills (`~/.claude/skills/`) - flat,
one cue = one image, no primary/evidence distinction anywhere, no validator for the
grammar at all. Two `AskUserQuestion` rounds resolved the open design points: (1)
Gemini's role - live via Chrome during the 10PM session, Pollinations as the automatable
fallback; (2) "screenshots" as an evidence source - captured live via Chrome in the same
session, not a new API; (3) evidence layout - a small corner/center inset over the
primary visual, randomized position, one at a time, labeled SOURCE (the user's own
wording and ASCII mockup). A Plan agent then produced the concrete file-by-file design,
read against the exact current code (not guessed) - confirmed the existing per-segment
(not whole-video) compositing architecture means the evidence overlay needs zero
time-gating, since each `_build_segment_clip()` call is already scoped to one segment's
duration.

**Implementation** (plan file: `ok-then-redesign-the-zany-waffle.md`):

- **New `[EVIDENCE: ...]` cue** in `script_parser.py` - `[EVIDENCE: "term"]` (real
  source) or `[EVIDENCE: screenshot: "<url>"]` (live Chrome capture), parsed the same
  way `MUSIC_CUE_RE` already was (a second independent cue type in the same loop).
  Unlike `ON SCREEN`, it does NOT flush the current segment - it attaches to whatever
  segment is already accumulating, consumed exactly once on the next real flush (same
  consumption rule `pending_cue` already had). Verified with a throwaway test script
  exercising every path (plain AI-generate, pre-placed Gemini stub, search-term
  evidence, screenshot evidence, and a no-cue segment immediately after an
  evidence-bearing one) - `beats.json` showed evidence attached only where intended,
  never leaking onto the neighbor with no cue.
- **`visuals/resolve.py` rewritten**: `_resolve_cue` → `_resolve_primary` - checks
  `build/visuals_gemini/<seg_id>.*` first (a file dropped manually during the live
  session, never written by code), else Pollinations via the unchanged
  `ai_generate.py`. The `sources.py` (Wikimedia/NASA/Pixabay/Smithsonian) call was
  **removed entirely** from this path, not just reordered - a bare search-term
  `ON SCREEN` cue now raises `ValueError` instead of silently resolving against those
  sources, forcing old-style scripts to be rewritten rather than reinterpreted (verified
  directly: constructed a bare-search-term cue and confirmed the exact error fires).
  New `_resolve_evidence` (fail-soft, never raises - a missing/empty result just means
  no inset for that one segment) handles the two evidence cue types, the screenshot
  path checking `build/evidence/<seg_id>.*` the same way. **Real bug caught and fixed
  before it shipped**: the existing no-cue fallback (`entry = {**last_resolved, "id":
  seg_id, ...}`) would have silently copied a neighbor's `evidence` key onto a segment
  that never asked for one - fixed by stripping `"evidence"` from the inherited entry
  and resolving each segment's own evidence cue independently (skipped only when this
  exact segment already has a valid cached evidence entry of its own, same
  skip-if-already-resolved discipline every other pipeline stage already follows - not
  unconditionally re-fetching on every plain re-run, which would otherwise re-hit
  Wikimedia/Pixabay for nothing). Verified end-to-end against the real `manifest.json`:
  the fallback segment had no `"evidence"` key at all, confirmed via direct JSON
  inspection, not just eyeballing.
- **New `pipeline/evidence.py`** - pure placement logic, same role as `character.py`:
  `position_for_segment(seg_id)` picks one of 5 anchors (`config.EVIDENCE_POSITIONS` -
  4 corners + center) via `random.Random(seg_id + "_evidence").choice(...)`, same
  seeded-random pattern as today's Ken Burns `motion_for_segment`. Shared by
  `assemble.py` (places the bordered image) and `captions.py` (places the SOURCE
  label) so the two separate ffmpeg passes can never land them in different spots -
  confirmed by direct coordinate check (captions' `\pos()` values were exactly the
  image position + 8px).
- **`assemble.py`**: `_build_segment_clip()` gained `evidence_path`/`evidence_xy`
  params; the old two-branch `if config.SHOW_CHARACTER: ... else: ...` structure was
  generalized into a small chain of optional layers (character, then evidence), each
  advancing a running output label - correctly collapses back to today's exact
  behavior when neither is present (maps `[bg]` directly, same trailing-`;` strip).
  Border composited with only `scale`/`crop`/`pad` (already-proven filters, no new
  ffmpeg dependency) - no `drawtext`, since `ffmpeg_tool.py`'s own docstring only
  confirms `libx264/libx265/libass/zoompan` on this build, not freetype/drawtext.
  `_flatten_segments()` now also takes `manifest` (new param) to look up each
  segment's resolved evidence and compute its position.
- **`captions.py`**: the "SOURCE" label goes through the existing `pysubs2`/libass
  pipeline instead of a new ffmpeg filter - a new `EvidenceLabel` style, positioned
  per-event via `\pos()` (needed since the label has 5 possible anchor points, not one
  fixed spot `alignment`/`marginv` could express). New per-segment loop (separate from
  the existing per-beat word loop) reads `manifest.json` and emits one event per
  evidence-bearing segment, scoped to exactly that segment's own `start`/`end` (already
  absolute/global timeline values from `narration.py`'s `_segment_timing()`, no offset
  math needed).
- **`config.py`**: `EVIDENCE_INSET_SIZE=280` (~32% of the square), 6px white border,
  "SOURCE" label text, `EVIDENCE_POSITIONS` (4 corners + center, same style as
  `CHARACTER_POSITIONS`), and the two new manual-drop directory names
  (`visuals_gemini/`, `evidence/`).
- **Skill files updated**: `~/.claude/skills/yt-script/SKILL.md`'s "Explanation"
  section now documents `AI-generate:` as the only valid primary cue and folds in the
  confidence-based visual-treatment language (lifted verbatim from
  `gemini_master_prompt.md`'s already-proven SOLID/CONTESTED/UNCERTAIN/myth rules,
  previously only applied to a one-off Veo re-visualization exercise, now a standing
  rule for every script going forward) plus the new optional `[EVIDENCE: ...]` cue.
  `~/.claude/skills/yt-factcheck/SKILL.md`'s "visual anchors" step split into (a) a
  mood/scene prompt for the primary visual (every section needs one) and (b) an
  optional real sourceable term/URL for an evidence inset (only where a real source
  actually exists).
- **Docs**: `voice.md` (master + `~/.claude/youtube/voice.md` mirror, confirmed
  byte-identical after the edit) and `idea.md` both updated with the new priority,
  matching this project's existing decision-log conventions.

**End-to-end verification** (a throwaway `videos/__evidence_smoketest__/` slug, deleted
after - not committed, not left in the repo): ran every real stage (`script_parser.py`
→ `narration.py` → `resolve.py` with a stub Gemini asset and a stub screenshot dropped
in place of a live Chrome session → `alignment.py` → `captions.py` → `audio_mix.py
--no-music` → `assemble.py`) and actually looked at the rendered frames, not just
exit codes - confirmed by eye: the Gemini-stub segment showed its evidence inset
(a real Wikimedia Julius Caesar bust, found live through `sources.py`) bottom-right
with a white border and "SOURCE" label inside it; the screenshot-evidence segment
showed its stub bottom-left; the plain segment and the no-evidence fallback segment
showed neither border nor label at all. This is the same "pixel-diff/frame-check the
real output, don't trust a clean exit code" discipline the Ken Burns motion fix used
earlier today.

**Not yet done**: nothing has actually been generated via a live Gemini/Chrome session
under this new convention - the whole live-10PM-session workflow is still only
exercised by the smoke test's stub files. The two existing rendered test videos were
deliberately left untouched (their `script.md`s predate this grammar and would raise
`ValueError` on a bare search-term cue if ever force-re-resolved without being
rewritten first - documented in `resolve.py`'s module docstring, not just here).

## Production video regenerated with real Gemini visuals - first live use of the new pipeline (2026-10-27, same day)

User connected Chrome live (not waiting for the planned 10PM window - "Chrome is
connected", then logged into the Google One Plus account mid-session: "wait! Plus
account is logged out, let me log in"/"ok logged in!") and asked to actually generate
the production `library-of-alexandria-destruction` video's 17 non-compliant segments
(everything still on Wikimedia/Pixabay/NASA as primary - the other 3 were already
`pollinations`, confirmed compliant already) via Gemini, confirming afterward:
"generate images only from gemini" (not Veo video - images only, simpler/faster/no
separate video quota).

**Reused existing work rather than re-deriving prompts**: `veo_prompts.md` (from the
2026-10-26 Veo retrofit exercise) already had all 20 segments' prompts written with
the confidence-based visual treatment correctly applied (SOLID=photorealistic
documentary, CONTESTED/UNCERTAIN=desaturated/grained/blurred, myth=illustrated
manuscript) - adapted each one for still-image generation (dropped camera-movement
language like "slow push-in," added "square 1:1 composition" framing) instead of
re-inventing them.

**Generation workflow** (`gemini.google.com/app`, Flash model, Plus account): one new
chat per segment (avoids the exact "stale similar-looking chat" mixup bug logged
2026-10-26), type prompt, wait for generation, click the image's own download icon
(top-right overlay on hover - NOT the circular icon in the image's center, which is a
share-link flow per the 2026-10-26 note; this is a cleaner, more reliable control than
the "..." menu's "Download image" used last time), verify via `PowerShell
Get-ChildItem ... Sort-Object LastWriteTime` which exact file just landed (never
assumed the filename), then moved+renamed into
`build/visuals_gemini/<seg_id>.png`. **Real tooling snag found and fixed**: the Bash
tool's `~` resolved to a stale/different path than the actual Windows Downloads folder
for file-listing purposes (a plain `ls ~/Downloads` kept showing yesterday's files
even after a confirmed-fresh download) - switched to PowerShell
`$env:USERPROFILE\Downloads` for every download-detection check, and used the
explicit `/c/Users/shahb/Downloads/...` path (not `~`) for the actual `mv` into place,
which worked correctly throughout. One real mid-session Gemini error ("Something went
wrong (1076)") on segment 12/17 - the prompt text survived in the input box unsent;
re-clicking send recovered it without re-typing, confirmed by the chat title changing
and a real image landing right after.

All 17 generated, verified by file listing (`beat_01_seg00.png` through
`beat_09_seg00.png`, 8-12MB each - full-resolution downloads, not thumbnails) before
touching the pipeline.

**Re-resolving without wasting the 3 already-compliant segments**: running
`resolve.py --force` on the whole slug would have been wrong - the 3 segments already
on `pollinations` (`beat_06_seg02`/`beat_07_seg00`/`beat_07_seg03`) have empty
`search_terms` (confirmed by reading their actual cue structure in `beats.json` before
assuming), so they wouldn't have tripped the new `ValueError`, but `--force` would
still have thrown away their already-good Pollinations images and regenerated new
(different, pointless) ones. Instead: surgically removed just the 17 target segments'
entries from `manifest.json` (kept the 3 compliant ones cached), then ran `resolve.py`
with no `--force` flag at all - the 17 missing-from-cache entries resolved fresh
(found their new `visuals_gemini/` assets immediately, zero fallback to Pollinations
needed), the 3 cached ones were left untouched. Confirmed via `Counter` over
`manifest.json`: `{'gemini': 17, 'pollinations': 3}`, zero `wikimedia`/`nasa`/
`pixabay`/`smithsonian` remaining anywhere as a primary source.

**Re-rendered and verified**: `assemble.py --force` (20 segment clips + final mux,
backgrounded, ~a few minutes given the Gemini images are 8-12MB full-res vs. the old
stock photos' smaller sizes) → `output/final.mp4`, 1080x1920, **158.8s - exactly
matching the known-good duration** (only the visuals changed, narration/captions/audio
untouched), clean full-file ffmpeg decode. Spot-checked 4 frames spread across the
whole runtime (not just the first one) by eye: the caliph/manuscript illustration at
the hook, Demetrius proposing to Ptolemy I (photorealistic, SOLID-with-caveat
treatment correctly applied), the ruined Serapeum interior (UNCERTAIN library link,
correctly desaturated/moody), and the crumbling-papyrus payoff shot - all
thematically on-point and dramatically better composed than the old mismatched stock
photos (e.g. the previously-flagged "castle-alexandria-egypt-aliens" Pixabay mismatch
is gone, replaced entirely).

**This is the first real, non-synthetic test of the whole 2026-10-27 visual-sourcing
redesign** - confirms the `visuals_gemini/` pre-placed-asset convention, the
cache-preserving partial-re-resolve pattern, and the branded-frame compositing all
work correctly against real Gemini output, not just the smoke test's stub PNGs.

## Found and fixed: production video's captions were stale AND silently empty (2026-10-27, same day)

User reported the production video's subtitles weren't centered. Investigated rather
than guessing - this turned out to be two stacked bugs, not one:

1. **`captions.ass` was stale**, dated Oct 26 01:45 - from *before* the 2026-10-26
   word-pop caption redesign ever happened. It still had the old `Karaoke` style
   (bottom-bar, alignment=2, 6-word lines), not the current `Word` style
   (full-frame-centered, alignment=5, one word at a time). Root cause: today's
   re-renders of this slug only touched `resolve.py` and `assemble.py` - `captions.py`
   was never re-run for this slug today, so `assemble()` just kept muxing whatever
   `captions.ass` was already sitting on disk from over a day ago. Fixed by actually
   running `captions.py` again.
2. **That re-run then exposed a second, worse bug**: the regenerated `captions.ass`
   had exactly **one** `Dialogue` event - the title - and zero word captions. Checked
   `narration_meta.json` directly rather than assuming: every beat's `words` field was
   completely absent. This is the *exact* silent-failure bug already logged on
   2026-10-26 ("Captions were silently missing entirely... `synthesize()` rebuilds
   `narration_meta.json` from scratch, silently wiping the `words` field that only
   `alignment.py` adds") - `captions.py`'s `if not words: continue` skipped every
   single beat with no error. Confirmed `narration_meta.json`'s mtime (Oct 26 14:07)
   matches a `narration.py` run that postdates whatever earlier `alignment.py` run had
   populated `words` - the exact wipe sequence the 2026-10-26 entry describes, just
   never re-aligned afterward for this slug specifically.

Fixed by re-running `alignment.py --force` (403/408 words aligned), then `captions.py`
again (399 Dialogue events this time, not 1), then a final `assemble.py --force`.
**Verified properly this time** - the first attempt's visual check sampled two
arbitrary timestamps that happened to land in the gaps between words (word-pop
captions are only visible ~0.1-0.3s each) and showed nothing, which could have been
misread as "still broken." Pulled the exact first word event's timing straight from
`captions.ass` ("Before", 0.00-0.20s) and sampled a frame inside that exact window
instead of guessing - confirmed the word renders dead-center of the full 1080x1920
frame, matching the `Word` style's `alignment=5`.

Final: 1080x1920, 158.8s (unchanged - only captions changed, not timing), clean
full-file decode. **Lesson reinforced for future re-renders of any slug**: `--force`
on `assemble.py` alone does NOT regenerate captions - if a slug's narration or
alignment has been touched since its `captions.ass` was last built, `captions.py`
needs its own explicit re-run, or the mux step silently keeps using a stale file with
no warning.

## Carried-forward open items (as of end of day, 2026-10-27)

Resolved today, superseding items on the 2026-10-26 list: #0 (Veo re-visualization) -
superseded by the "images only from Gemini" decision, not video clips; the
`build/visuals_v2/` video-clip compositing path built on 2026-10-26 still exists and
works (used by the gemini-test slug), just isn't the chosen path for the production
slug going forward. #1 (Pixabay relevance-filter mismatch) - moot, the two affected
segments are Gemini-sourced now, Pixabay isn't used as a primary source for anything
anymore (see below for where it still matters). #3 (wire a voice preset into the
pipeline) - done, superseded twice over by `af_bella` then `hf_alpha`, both actually
wired via `voice.md`'s `[CONFIRMED]` line read by `config.get_voice_preset()`. The
back half of #11 (word-by-word caption mode "vs. the current karaoke-highlight line
groups") was already stale by the time it was written - the same-day 2026-10-26
caption redesign (word-pop, one at a time) had already superseded the karaoke style
it was comparing against.

Still open, unchanged: #2 (confirm by ear whether Kokoro mispronounces Greek/
Ptolemaic proper nouns - now a question about `hf_alpha`, not `am_michael`, never
actually checked), #4 (character pose variety, single-pose only, character overlay
currently off anyway), #6 (mobile push notifications), #7/#7b (Bollywood music
library still zero tracks; old genre library's SFX listen-through still pending),
#8 (actual YouTube channel still doesn't exist), #9/#10 (audio library CLI/LUFS
notes, not blocking), #11's front half (Smithsonian rarely returns usable results -
unchanged, now actually relevant again since Smithsonian is part of the *evidence*
search chain, not retired).

New from today:

1. **`script.md` itself was never rewritten to the new cue grammar for
   `library-of-alexandria-destruction`** - the render now uses real Gemini images
   (via the `visuals_gemini/` pre-placed-asset path), but the script's `[ON SCREEN:
   ...]` cues are still the old bare-search-term form. This works fine as long as
   those Gemini assets stay on disk, but a future `--force` re-resolve of this slug
   *without* the assets present (or without first rewriting the cues to
   `AI-generate:` prompts) will hit the new `ValueError` - this is flagged in
   `resolve.py`'s own docstring as intentional, but the script itself is still
   technically inconsistent with what it actually renders. Worth rewriting
   `script.md`'s cues to match, for long-term maintainability, next time this video
   is touched.
2. **`[EVIDENCE: ...]` has never been used in a real script** - built and verified
   against a throwaway smoke-test slug only (stub Gemini/screenshot files, deleted
   after). No actual video has a real evidence inset yet; the production
   regeneration today had zero evidence cues in its (old-grammar) script.
3. **Live Chrome screenshot evidence has never actually been captured** - same
   status, smoke-tested with a stub file only.
4. **3 of `library-of-alexandria-destruction`'s 20 segments are still Pollinations,
   not Gemini** (`beat_06_seg02`/`beat_07_seg00`/`beat_07_seg03` - already compliant
   with the new rules, just not upgraded to Gemini quality). Left as-is since the
   user didn't ask for a full-Gemini pass, only a compliant one - could be revisited.
5. **The planned "connect Chrome around 10 PM, work through the night" cadence
   hasn't actually been exercised as its own cadence yet** - today's Gemini
   generation happened ad hoc, mid-afternoon, once the user had Chrome/the Plus
   account ready, not during a dedicated overnight session. The mechanism is now
   proven (17 real images generated, resolved, and rendered correctly end to end),
   just not yet under the specific nightly timing originally discussed.
6. **Lesson to carry into every future re-render, not just this one**: `assemble.py
   --force` does not regenerate captions - if narration or alignment changed since a
   slug's `captions.ass` was last built, run `captions.py` explicitly too, or risk
   silently muxing a stale or (per today's second bug) completely empty caption
   file.

## Progress log — 2026-10-27 (continued): content-rectangle template, visual-style pivot, cut-rate/punctuation/script-first rules, captions back to the bottom bar

Long session covering a full redesign pass on the branded frame template, a
reference-video-driven visual/tone pivot, two new measured production rules, and a
caption-position revert - each verified against real renders, not just written down.
User handled the content-rectangle template code (item 1 below) and the test-folder
cleanup (item 2) via their own manual commit (`650bbea "Template update"`) partway
through; everything from item 3 onward was committed separately, in 7 logical
commits, at the end of the session (see item 11).

### 1. Content box: square -> full-width letterboxed rectangle

User wanted the content square's height decreased ("make it a full rectangle") and
width increased to span the full mobile screen, "same this size" as a reference
WhatsApp image. Measured the reference precisely with PIL (`numpy` row/column
brightness scan, not eyeballing): content band spans rows 592-1007 of a 738x1600
image - 416px tall, full 738px width, symmetric 592px black bars top and bottom.
That band's own aspect ratio (738/416 = 1.774) is essentially 16:9. Scaled onto the
project's 1080-wide canvas at that aspect (not by copying the reference's raw margin
fractions, which belong to a differently-shaped source canvas): **1080x608**,
vertically centered (`SQUARE_Y = (1920-608)//2 = 656`), growing both the title band
and bottom bar from 560/480px to 656/656px symmetrically.

Ran this through full plan mode (two Explore agents mapping every `SQUARE_SIZE`/
`SQUARE_X`/`SQUARE_Y` usage across `config.py`/`assemble.py`/`character.py`/
`evidence.py`/`visuals/ai_generate.py`, then a Plan agent for the concrete diffs).
Key findings from that research: `SQUARE_SIZE` had been used as *both* a width and a
height term everywhere, only correct because it used to be a true square - splitting
it into `SQUARE_WIDTH`/`SQUARE_HEIGHT` required auditing every dependent line, not a
blind rename. The host-character "overflow past the square's edge" anchors
(dormant, `SHOW_CHARACTER=False`) were redesigned to stay on-canvas now that there's
no outer margin to overflow into. `assemble.py`'s three hardcoded `SQUARE_SIZE:
SQUARE_SIZE` ffmpeg filter calls (video crop, video scale, zoompan output size) were
the real functional fix - left as-is they'd have stretched every future visual to a
false 1:1.

Verified by re-rendering `library-of-alexandria-destruction-gemini-test`
(`assemble.py --force` + `review.py --force`, visuals/narration/captions untouched)
and reading frames from both a Veo video segment and a still-image segment: full-width
band, correct ~16:9 proportions, symmetric letterboxing, no stretch.

### 2. Test folder cleanup: `library-of-alexandria-destruction-gemini-test`

User asked to delete all visuals from this slug, keeping only the script, template,
and audio. Deleted `build/visuals`, `visuals_gemini`, `visuals_v2`, `evidence`,
`clips`, `review_frames`, `manifest.json`, `video_silent.mp4`, `output/final.mp4`
(recreated the now-empty directories so the pipeline doesn't need to). Kept
`script.md`, `build/beats.json`, `build/captions.ass`, `build/beats/` (per-beat
narration wav + word timings), `build/narration_meta.json`, `build/mix.wav` -
`manifest.json` had to go too, since keeping it without the actual image files would
make the pipeline think stale visuals were still cached. Everything deleted was
already committed to git, so fully recoverable if ever needed.

### 3. Reference-video style analysis -> new `visual-style-brief.md`

User sent a second reference video (5:45, stone-age medicine topic) and asked for
its styling/tone analyzed, then turned into a reusable brief for every future
`AI-generate:` prompt. Read 16 frames + the full Whisper transcript via the global
`video-reader` skill. Found a genuinely different, reusable visual system from the
project's prior photoreal-documentary direction:

- **Two-mode illustration system**: flat vector-line explainer cards (diagrams,
  comparisons, bar charts, short hand-drawn-caps diagram labels, red annotation
  arrows) alternating with fully painted/shaded narrative scenes using the same flat
  stick-figure character (round cream head, black dot eyes, single eyebrow line for
  expression, thin black-outline limbs, scribble hair/fur).
- Muted earth palette (gray/brown/tan/dusty teal) with saturated color reserved for
  semantic meaning only (red=danger/annotation, green=parasite/nature, blue=neutral).
- Narration tone: conversational, dryly sarcastic, dark humor landing mid-fact,
  named/dated sourcing delivered as casually as the jokes, uncertainty stated flatly
  ("we don't know exactly why") rather than hedged apologetically - noted this
  overlaps closely with the channel's own existing SOLID/CONTESTED/UNCERTAIN
  epistemic-transparency angle, just with a more sarcastic register than `voice.md`
  had locked in before today.
- A content-specific CTA pattern (*"Still have all your limbs? Hit like and
  subscribe"*) - a punchline tied to the episode's own content, not boilerplate.

User then asked for this turned into a visual-style brief plus a tone pivot
(sarcastic lore/dark humor, loud/confident delivery) plus a sarcastic Like &
Subscribe line added to the actual audio/script. Full plan mode: two Explore agents
(one mapping `yt-script`/`yt-factcheck`'s exact current wording for the confidence-
treatment rule and the Questionary beat's existing "replaces a generic like/
subscribe pitch, not stacks on top of one" rule - the real conflict point; one
mapping Kokoro's actual audio-gain levers and the existing `gemini_master_prompt.md`
structural precedent), then a Plan agent. Three real design decisions surfaced and
resolved via `AskUserQuestion` rather than assumed: the sarcastic CTA line placement
(end-of-script, alongside the closing question - not mid-script, not a per-video
judgment call), whether "loud and confident" means an audio-engineering change
(no - Kokoro's TTS call has no volume/pitch parameter at all, confirmed by reading
the installed `kokoro_onnx` library directly; it's writing/tone only), and whether
the new illustrated style fully replaces photoreal as the default (yes, full
replacement, matching every prior style decision's pattern in this project).

Built `C:\YouTube\visual-style-brief.md` (new, channel-wide reusable doc, same tier
as `voice.md`): the two-mode system, character guidance (explicitly NOT chasing
cross-prompt character consistency - tied directly to why `config.SHOW_CHARACTER`
is dormant), palette, a baked-in-text constraint (short diagram labels fine, full
caption-length sentences not, since `captions.py` already burns its own captions -
this is the kind of collision-with-existing-system flag this project's docs always
call out explicitly), confidence treatment adapted from photoreal to illustrated
(SOLID=clean confident rendering, CONTESTED/UNCERTAIN=sketchier line weight/muted
palette/dashed motif instead of grain-and-blur, myth=painted-manuscript/storybook),
a per-prompt field checklist, and workflow discipline for the live Gemini session
(max 2 retries for a minor fix, max 4 total attempts before switching to a new
Gemini chat tab - citing the real stale-chat near-miss wrong-clip download logged
2026-10-26 as the reason this matters, not just discipline for its own sake).

Updated `yt-script/SKILL.md` (confidence-treatment block now points at the brief,
same pattern as its existing `voice.md` pointer; Questionary beat rewritten to add
the mandatory sarcastic closing CTA right after the existing closing question,
explicitly reconciling rather than silently contradicting the old "replaces, not
stacks" sentence; "What to hand back" gained a bullet), `yt-factcheck/SKILL.md`
(one-line pointer in the visual-anchors step), and `voice.md` (master + the
`~/.claude/youtube/voice.md` mirror, kept byte-identical as always): tone rewritten
to "loud, confident, sarcastic, and disciplined" without loosening the no-invented-
claims rule or the banned-vague-superlative list, visual-style-mix bullet repointed
at the brief (also fixed a stale "content square" reference left from item 1),
content-structure bullet documents the new closing CTA. Also fixed one more stale
"content square" reference in `yt-script/SKILL.md`'s Title section while in there.

Generated one real test image live through Chrome/Gemini using the new brief - a
painted-scene, SOLID-confidence prompt (Demetrius of Phalerum presenting the library
idea to Ptolemy I). Result matched the brief well on every axis (character style,
palette, confident clean linework, no baked-in text, 2752x1536 = 1.79:1, close to
the target 16:9). Saved to `visuals-test/style_brief_test_01_demetrius_ptolemy.png`.

### 4. Cut-rate rule: no image holds longer than ~4 seconds

User asked for a hard-ish ceiling (images shouldn't all mechanically be 4s, but none
should exceed it, timed to the audio like the reference) and to re-analyze the
reference video properly rather than relying on the earlier eyeballed frame sample.
Ran real ffmpeg scene-cut detection (`select='gt(scene,0.25)'`,`showinfo`) across the
full 345s runtime: 98 shots, median 3.03s, mean 3.52s, **78% of all shots at 4s or
under**. Pulled frames from the handful of outliers (7-15s) and confirmed they were
all a single flat-explainer diagram card held through one extended explanation (a
timeline comparison, a map+skull graphic, a survival-rate chart), not narrative beats
- informed the rule's exception language without softening the default cap.

Added `config.MAX_SEGMENT_DURATION_SEC = 4.0` and a matching (non-fatal) warning in
`narration.py`'s `_segment_timing()` - prints the exact beat/segment id and a text
preview whenever a resolved segment would hold past the cap, so an under-densified
script gets caught at build time instead of relying on the writer's eye. Smoke-tested
with synthetic segments before trusting it (fires exactly on the oversized one, silent
on well-split ones) - same "verify before trusting new text/timing logic" discipline
this project has used all along. Tightened `yt-script/SKILL.md`'s cue-density rule
(was "~5-8s of narration" per cue, now targets under 4s, cut points at natural
narration breaks) and added a "Cut rate" section to `visual-style-brief.md` with the
full measurement. Logged in `idea.md`.

### 5. Punctuation rule: narration only pauses on `. , ! : ?`

User wanted narration to only pause on period/comma/exclamation/colon/question mark,
with the script using them "excessively but not too much" and "perfect grammar."
Full plan mode again: two Explore agents (one tracing `render.py`'s actual stage
order - confirmed `parse` always runs before `visuals` in a normal run, but
`--from-stage visuals` jumps straight to `resolve_all()` reading
`narration_meta.json` with zero staleness check; and a punctuation audit of the real
production `script.md` - em-dash is the dominant real offender, ~8 uses, no
semicolons/ellipses/parentheses exist in it today, and it has no `!`/`?` at all yet;
one reading `kokoro_onnx`'s and `phonemizer`'s actual installed source directly -
found `kokoro_onnx/chunker.py` only actively manages pauses for its own
`SENTENCE_MARKS=".!?…"` and `CLAUSE_MARKS=",;:"`, so a plain/spaced hyphen is
silently dropped with zero pause today and an em-dash/parenthesis gets an
uncontrolled, purely model-learned pause), then a Plan agent for the exact regex
design.

Built `script_parser.normalize_pause_punctuation()`, composed with the existing
`strip_markdown_emphasis()` at the exact point raw script text becomes `Segment.text`
(`flush_segment()`): em-dash/en-dash/spaced-hyphen/double-hyphen -> comma;
semicolon/ellipsis -> period, capitalizing the following word; parentheticals ->
comma-wrapped inline asides; several cleanup passes for the punctuation collisions
those substitutions can produce (doubled commas, a comma stacked right before a
terminator, stray spacing). **Smoke-tested and found a real bug before trusting it**:
a leading/unspaced ellipsis produced a glued `.word` with no space - fixed by making
the ellipsis/semicolon substitutions insert their own trailing space
(`". "`/`". "` instead of bare `"."`), then re-verified the full synthetic case list
plus the real production script (all ~8 em-dashes converted to commas cleanly, the
one pre-existing colon untouched, word-internal hyphens like "three-hundred-year"
correctly left alone).

Also added `visuals/resolve.py`'s `_warn_if_narration_stale()` - the staleness gap
the stage-order research surfaced - a non-fatal mtime comparison (`script.md` vs.
`narration_meta.json`) at the top of `resolve_all()`, the one function reachable from
both a normal full run and `--from-stage visuals`. Verified directly: fires when
`script.md`'s mtime is bumped past `narration_meta.json`'s, goes silent again once
`narration_meta.json` is regenerated, silent when either file is simply missing -
same "warn, don't silently proceed" pattern as the cut-rate warning, and the same
staleness-bug class this file already logs real incidents for (stale `captions.ass`,
silently-wiped alignment data).

Documented as two paired rules - punctuation in `yt-script/SKILL.md`'s new
"Punctuation" section (maps each of the five marks to a beat the skill already
defines: period=declarative, colon=reveal, comma=breath, exclamation=loud delivery
sparingly, question mark=Questionary close) plus a `voice.md` Pacing cross-reference;
script-first in `yt-script/SKILL.md`'s "The gate" (visual generation starts only
after the gate, never alongside it) and a precondition sentence in
`visual-style-brief.md`'s workflow-discipline section. Both logged in `idea.md`.

### 6. Wan2GP: where it's used (nowhere) and whether it's legally usable (yes, but hardware blocks it)

User asked where Wan2GP is used in the pipeline - answer: nowhere, it's only
mentioned in `idea.md`/`research-findings.md` as "Path 1" of the original
lead-magnet PDF (a faceless autopilot cartoon-character channel), explicitly
rejected early on in favor of the current Kokoro+Gemini/Pollinations+ffmpeg pipeline.
Confirmed via a repo-wide grep - zero code usage.

Follow-up: is there any legal way to use it. Fetched the actual current
`LICENSE.txt` directly from `github.com/deepbeepmeep/WanGP` (the project renamed
from Wan2GP to WanGP) rather than trusting a third-party mirror copy found first via
search. The **WanGP Community License 2.0** explicitly permits free use "including
inside a company" (SS1.8/1.9(ii)/3.3 - internal/business use regardless of revenue is
Free Use, not Restricted Commercialization), and SS6.5(b) exempts free/ad-monetized
publication of outputs from even the attribution requirement (attribution is only
owed on a "Direct Output Sale" - selling the output itself as the product, which an
ad-monetized YouTube upload isn't under their own definition). The underlying Wan 2.2
model weights (Alibaba) are separately Apache 2.0. Net: legally clear, free, no
attribution needed for this channel's actual use case - a paid commercial license
would only be needed to resell/white-label the software itself or sell outputs as
direct paid deliverables, neither of which applies here.

The real blocker is hardware, not law: Wan2GP's video diffusion models need a real
discrete GPU; this machine has integrated graphics only - the same wall that already
made this project pivot away from local video generation in the first place
(`idea.md`'s "Production pipeline" decision). Offered to look into minimal cloud-GPU
rental costs if the user wants to revisit that budget stance - not pursued yet.

### 7. Captions moved back to the bottom bar

User asked to move the word-pop captions back below the content rectangle, same
nature (one word visible at a time, pop animation), just repositioned - the
2026-10-26 redesign had made them full-frame-centered (`alignment=5`). Changed
`captions.py`'s `_build_word_style()` to `alignment=2` (bottom-center), with
`marginv` computed from `config.HEIGHT - SQUARE_Y - SQUARE_HEIGHT` (the bottom bar's
actual current height, 656px, divided in half) instead of a hardcoded number, so it
stays correct automatically if the content rectangle's size ever changes again.
Nothing else about the caption style touched - color, pop animation, one-word-only
behavior all unchanged.

Verified by regenerating `captions.ass`, re-running `assemble.py --force` on the
production `library-of-alexandria-destruction` slug, pulling the first word event's
exact timing straight from the regenerated `captions.ass` ("Before", 0.00-0.20s,
same discipline as the 2026-10-27 caption-centering bug verification), and sampling
an accurate (output-side-seeked) frame at that timestamp - confirmed the word renders
centered in the bottom bar below the image. Logged in `idea.md`.

### 8. Committed and pushed - 7 logical commits

User asked for everything committed and pushed, specifically as 7 commits. Checked
`git status`/`git fetch` first and found the user had already manually committed and
pushed the content-rectangle template change plus the test-folder cleanup themselves
(`650bbea "Template update"`, confirmed local matched `origin/main` exactly before
starting) - avoided re-committing that work. Split everything from `visual-style-
brief.md` onward into 7 coherent commits (new brief; `voice.md` tone/CTA/pointer
rewrite; cut-rate `config.py`+`narration.py`; punctuation `script_parser.py`+
`visuals/resolve.py`; captions `captions.py` + the full re-rendered production-slug
build artifacts; `idea.md`'s decision-log entries; the style-brief test image),
verified a clean working tree between each, and pushed
(`650bbea..f22f48f` on `origin/main`).

## Carried-forward open items (as of end of this session)

Everything from the 2026-10-27 list above is either resolved by this session's work
or unaffected. New/updated:

1. **The new visual-style-brief.md format has been used for exactly one real
   generation** (the Demetrius/Ptolemy test image) - a full real script hasn't been
   written and illustrated under the new style/tone/punctuation/cut-rate rules
   together yet. That's the real end-to-end test still pending.
2. **Nothing has actually been heard** under the new "loud, confident, sarcastic"
   tone or the new punctuation-normalized narration - same standing caveat this
   project always carries for anything judged by eye/transcript rather than by ear.
3. **The sarcastic Like & Subscribe closing line has never been written into a real
   script yet** - the rule exists in `yt-script/SKILL.md` and `voice.md`, untested
   against an actual beat.
4. **Wan2GP/WanGP remains legally usable but practically blocked by hardware** - no
   action taken, flagged as a possible future budget conversation (cloud GPU rental)
   if ever revisited.
5. Everything else carried from before (Bollywood music library still zero tracks,
   character pose variety still single-pose, actual YouTube channel still doesn't
   exist, mobile push notifications still disabled, Kokoro's Greek/Ptolemaic
   pronunciation still unconfirmed by ear) is unchanged by this session.