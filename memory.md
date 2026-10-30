# Progress log

Compacted rewrite (2026-10-30) of the original day-by-day build log. Keeps every
decision, every real bug found/fixed (and its root cause), and the current state of
each component; trims blow-by-blow narration and superseded detail. `idea.md` is
still the settled-state doc; this is the "why" and "what broke" history.

# 2026-10-24 — Tooling, niche/pipeline decisions, first skill customization

Installed `youtube-agent-skill` (11 global Claude skills: `/yt-script`, `/yt-package`,
`/yt-retention`, `/yt-edit`, `/yt-comment`, `/yt-plan`, `/yt-viral`, `/yt-shorts`,
`/yt-seo`, `/yt-chapters`, `/yt-audit`) — reviewed source for injection/network risk
first. Customized `yt-script` for a narration-only, pre-launch channel: requires a
`research.md` brief before any factual claim, SOLID/CONTESTED/UNCERTAIN confidence
carried into delivery, `[ON SCREEN: ...]` cues must name a sourceable visual. Built
**`yt-factcheck`** from scratch: `sources.py` (stdlib-only, keyless — Wikipedia,
Internet Archive, Semantic Scholar) → draft claims with confidence tags →
independent re-check by a *fresh* subagent → visual anchors → `research.md`.
Reworked `voice.md` for TTS/narration instead of on-camera presence. File
convention: `videos/<slug>/` holds `research.md` + `script.md`.

Live end-to-end test on "Library of Alexandria": `yt-factcheck` correctly
downgraded the Serapeum/library link to UNCERTAIN and flagged the Caliph Omar
burning story as an unsupported legend; `yt-script` produced a grounded script.
Found `hookscore.py`'s STAKES property floors pure-curiosity hooks (calibrated for
personal-loss stakes like "lose"/"waste"/"risk") — resisted inventing false stakes
to game it; fixed two days later by adding destruction/mystery vocabulary native to
this niche (destroyed, vanished, forgotten, erased, forbidden, unsolved, etc.) —
verified against the Alexandria hook (54→57) and four synthetic curiosity hooks
(22→48 floor) with zero effect on a control self-help hook.

**Pipeline/budget decided**: images/clips + voiceover + captions, not from-scratch
motion graphics — hardware (Ryzen 3 5425U, integrated GPU, 8GB RAM) can't sustain
render-heavy animation daily. Cadence: 1 video/day. Budget: Claude + ElevenLabs are
the only accepted must-spends; **Kokoro** (free, local, CPU TTS) chosen over
ElevenLabs/voice-cloning for now; visuals free-source-first; music/SFX
self-produced; thumbnails free-tool-first; storage local.

**Differentiation angle decided**: epistemic transparency as the format itself —
confidence-tagged claims, myths corrected not repeated, sourcing shown rather than
asserted. Formalized as **Storytelling → Explanation → Questionary**: narrative
hook, then claims at real confidence level, then deliver the payoff *and* a
genuinely unresolved question back to the viewer (after the payoff, never instead
of it).

**Daily schedule decided**: content ready by 8:00 PM, 8–11 PM is the admin/Claude
collab window, upload before midnight regardless of whether the window was used.

GIMP 3.2.6 confirmed already installed (resolves thumbnail tooling). Reviewed the
other 9 generic `yt-*` skills (flagged generic, not yet customized — finished next
day).

**Tooling research** (full detail in `research-findings.md`): Kokoro tested working
locally (RTF ≈1.05 on this CPU) but `create_timed()` returns empty timings —
`faster-whisper` (`base.en`) tested as the fix (50/50 words aligned, near-real-time).
Wikimedia Commons + NASA APIs confirmed keyless/working; Pixabay + api.data.gov keys
retrieved and working; Pexels API key issuance paused site-wide (unusable); Gemini
free-tier image generation confirmed blocked via API (0-request quota) — image/video
gen only ever works through the live `gemini.google.com` web UI, never the API, for
the whole life of this project.

**Open at end of day**: finish customizing the 9 generic skills, build
Storytelling/Explanation/Questionary into `yt-script`, build the actual render
pipeline (nothing produces an .mp4 yet — the real blocker), music/SFX, create the
YouTube channel.

# 2026-10-25 — Render pipeline built end-to-end; folder renamed `C:\Idea`→`C:\YouTube`

Finished customizing the 9 remaining skills: 7 were channel-stage-agnostic and left
as-is; **`yt-edit`** rewritten (TTS QC instead of human-take editing — DEAD now means
unnatural TTS pauses, not performance issues); **`yt-shortcraft`** created new
(same craft bar as `yt-shorts` but for scripts that already *are* a whole Short, no
clip-mining mechanic). Built Storytelling→Explanation→Questionary into
`yt-script/SKILL.md` directly. Found and fixed a stale `~/.claude/youtube/voice.md`
mirror (every skill run since the tone/length decisions were finalized had been
reading an outdated draft) — refreshed, now kept byte-identical to the master on
every future edit. Fixed `hookscore.py`'s STAKES property (see 10-24 above).

**Music/SFX library** (self-produced, numpy/scipy): built a 12-asset structural
library tied to Storytelling/Explanation/Questionary, then **same day, replaced
outright** with a 50-track/50-SFX topic-based library (8 music categories, 7 SFX
categories) per a user spec — 48kHz/24-bit via `soundfile`, `pyloudnorm` for real
LUFS measurement, new synthesis primitives (FM/AM, granular, feedback delay, modal
scales). All 100 assets passed validation first run. A caught bug:
`np.convolve`-based reverb hung 2+ min on multi-second audio — switched to
`scipy.signal.fftconvolve`. A caught bug: effects applied *after* the loop was
cropped undid the crossfade seam-matching (20–40% discontinuity) — fixed by running
effects on the full signal and crossfading last (<3%). First human listen flagged
`music/history/` as repetitive and internally inconsistent in loudness — rewrote its
7 tracks with distinct lead synthesis each and added optional `target_lufs`/
`pre_limit_drive` params to `composition.render_bed()` (history's spread: 9.1→1 LU).
Deliverable folders later moved to `C:\YouTube\Assets_audio\` (audio files/catalogs),
separate from the dev tree `assets\audio\` (generators/reports).
**(This library was later fully superseded for production — see 10-26/10-28 below;
left on disk, unused.)**

**Render pipeline built** (`C:\YouTube\pipeline\`): `script_parser.py` (script.md →
beats.json) → `narration.py` (Kokoro per beat) → `alignment.py` (faster-whisper word
timestamps) → `visuals/sources.py`+`ai_generate.py`+`resolve.py` (Wikimedia→NASA→
Pixabay→Smithsonian→Pollinations, license-filtered) → `captions.py` (word
timestamps → karaoke `.ass`) → `audio_mix.py` (narration+music+SFX→mix.wav) →
`assemble.py` (per-beat Ken Burns clips→concat→mux→final.mp4) → `render.py`
(resumable orchestrator). `ffmpeg_tool.py` wraps `imageio-ffmpeg`'s bundled binary.
Verified end-to-end against `library-of-alexandria-destruction` (9 beats, 159.9s).
Real bugs found while building: Wikimedia full-res downloads get 429-rate-limited —
switched to sized `thumburl`; Pixabay returns irrelevant trending hits on no real
match — added a tag-relevance filter; Pollinations free tier hard-limits 1
image/45s — added a proactive rate limiter; ffmpeg defaults a looped still image to
25fps, silently shortening clips timed for 30fps — fixed with explicit `-r 30`.

Built the global `video-reader` skill (`~/.claude/skills/`, outside this project) —
extracts evenly-spaced frames + full `faster-whisper` transcript from any video, so
Claude can "watch" a render. Used for the rest of the project's life as the main
self-review tool.

Found via that tool and fixed: burned captions were showing Whisper's *mis-hearing*
of the Kokoro audio instead of the real script text ("391c" for "391 CE") — fixed by
realigning real script words onto Whisper's timestamps via `difflib` in
`captions.py::reconcile_words()`. Also fixed: visual cut rate was too static (up to
26s on one image) — `script_parser.py` now splits a beat into multiple segments at
every inline `[ON SCREEN: ...]` cue, not just before a beat; densified the
Alexandria script 9 beats→20 segments.

**Branded frame template built**: black 1080x1920 canvas, white title in a top band
(falls back to the `# Script:` heading), every visual confined to a centered square
(later changed to a rectangle, see 10-27), captions in the bottom bar. A real miss:
`--from-stage narration` skips re-parsing script.md, so a title edit needs an
explicit `script_parser.py` re-run first. Title rule: must be long enough to wrap
two lines (~35–50 chars) or it sits alone with awkward empty space.

**Host character designed**: silhouette in the channel logo's hat/coat style via
Pollinations (`sana`, its only free model). Scoped to a single "neutral" pose after
gesture variety repeatedly failed — position (not gesture) cycles per segment for
movement. Real bug: compositing 20 chained per-segment overlay filters onto one
whole-video stream bloated output past 140MB (each overlay toggle reads as a scene
change to x264) — fixed by compositing character+background per segment, then
concatenating cheaply.

**A real "watch the video" pass caught two bugs frame-checks missed**: (1) captions
were silently empty — a `narration.py` re-run (to fix the title) rebuilds
`narration_meta.json` from scratch, silently wiping the `words` field only
`alignment.py` adds; `captions.py`'s `if not words: continue` then skips every beat
with no error. **This exact bug recurred at least three more times across this
project** (10-26, 10-27, 10-28) — always same root cause, always fixed by re-running
`alignment.py --force` → `captions.py` → re-assemble. (2) Kokoro spoke a markdown
character out loud ("asterisk not asterisk") from `*not*` emphasis — fixed with
`strip_markdown_emphasis()` in `script_parser.py`.

Render finished, hit and fixed a separate real bug: `assemble.py`'s resume logic
only checks clip *existence*, not validity — a corrupt truncated clip from a
previous interrupted run was silently kept and broke the concat. **`assemble.py`
also never regenerates captions on its own `--force`** — if narration/alignment
changed, `captions.py` needs its own explicit re-run or the mux silently uses a
stale caption file. Both lessons recurred repeatedly for the rest of the project.
Also found (not fixed, cosmetic only): a Pixabay fallback image for two segments was
an unrelated "castle-alexandria-egypt-aliens" photo that cleared the relevance
filter on raw tag word-count despite being irrelevant — mooted later when Pixabay
stopped being used as a primary source (10-27).

Kokoro voice preset locked in: `am_michael` (first of several — see the running
voice history at the end of this file). Whisper's transcript of Kokoro's own output
consistently garbles Greek/Ptolemaic proper nouns — flagged as unconfirmed whether
Kokoro mispronounces or Whisper mishears; **resolved 2026-10-30 (see bottom)**.

**Bollywood-referenced emotion music system scoped** (background-score style only,
never sampling real recordings — downloading/modifying real Bollywood tracks was
explicitly rejected over Content ID/copyright risk). 14 emotion categories (not
genre), music can shift mid-video by structural part via a new `[MUSIC: <emotion>]`
cue. Built: `audio_mix.py` multi-part crossfaded mixing (verified with synthetic
sine-tone test beds before trusting the length-preserving math), new synthesis
primitives (tabla/dholak/sitar/tanpura/bansuri/harmonium), parallel
registry/generate/validate scripts, 14 empty category folders. **Status then and for
the rest of the project: infrastructure only, zero tracks ever composed** — waiting
on real reference material/brief that was never supplied; **superseded entirely when
music/SFX were dropped from production on 10-28.**

Side track, logged for continuity: verified a Google One AI Student offer as
genuine (not a scam — stays on canonical Google domains), claimed on a secondary
account via a real pending-degree marksheet. Confirmed Google One AI Plus/Pro (
consumer subscription) and the Gemini Developer API are billed completely
separately — the subscription does not raise API quota or unlock free image
generation.

# 2026-10-26 — Veo test, Hindi pivot, Ken Burns motion, visual-sourcing redesign

**Veo re-visualization explored**: drafted `gemini_master_prompt.md` (per-segment
prompts honoring SOLID/CONTESTED/UNCERTAIN/myth visual treatment) and generated one
proof-of-concept Veo clip live via `gemini.google.com/videos` (720x1280, 10.01s,
correct style). Confirmed Veo bakes in its own audio (must be stripped) and doesn't
match segment duration exactly (needs trimming) — both later handled when
`assemble.py` gained a video-clip branch. **Status: never scaled past the one
clip** — the project moved to Gemini still-images-only the next day instead.

**Hindi/Hinglish pivot tried then fully reverted** (same two days): switched
narration to Hindi-dominant Hindustani via `hm_omega`/`lang="hi"` — verified Kokoro
can genuinely speak Hindi (Whisper detected `hi` at 95.6% and transcribed a near
match, albeit in Perso-Arabic script, not Devanagari). Built a positional-zip
caption mode (`_zip_positional()`) since the normal text-matching caption aligner
can't work on non-Latin script. Tried a 60:40 Hindi:English ratio, user reverted
back to the original ~90:10 mostly-Hindi version, then **the whole Hindi/Hinglish
direction was reverted to English the next day (10-27)** at the user's request,
with an "Indian tone" experiment (English narration through a Hindi-voice preset)
tried instead — this became `hf_alpha`, promoted to global default later 10-27. No
Hindi/Hinglish content exists in production.

**Pure-Gemini-visuals validation build**: new slug
`library-of-alexandria-destruction-gemini-test` (first 4 beats only) to test
`am_michael` + square-cropped Gemini/Veo visuals before committing fully. Added
`assemble.py`'s video-clip branch (scale+crop to square, loop/trim to segment
duration, Veo's own audio implicitly dropped) and `--no-music` (since the Bollywood
library had zero tracks and crashed the normal music path). **A real self-inflicted
bug**: re-rendering via `--from-stage visuals` force-re-resolved every segment
through the *old* Wikimedia/Pixabay chain using stale English cues still left in
`script.md`, silently overwriting 4 of 5 just-downloaded Gemini images with random
stock photos. Recovered from `~/Downloads/`. **Lesson**: always use the *first*
stage that actually changed, never a later stage whose cached output needs
preserving.

**Character overlay dropped as a toggle** (`config.SHOW_CHARACTER = False`, not
deleted) and **captions redesigned**: from 6-word bottom-bar karaoke lines to one
word on screen at a time, centered full-frame, with a scale-up "pop" animation.
Added a scoped number-to-digit converter for hyphen-compounded year/measurement
tokens only ("three-hundred-year"→"300-year"), leaving bare number words alone.

# 2026-10-27 — Voice reverts, Ken Burns bug, visual-sourcing flip, content rectangle, visual-style pivot

**Voice history this day**: reverted `am_michael`→`af_bella`; then, reverting the
Hindi pivot to English with an "Indian tone" experiment, discovered Kokoro has no
dedicated Indian-English preset — tested feeding English text through the 4 Hindi
voice presets under `--lang en-us`; user picked **`hf_alpha`**, confirmed on the
gemini-test slug, then **promoted it to the channel-wide default the same day**
(superseding `af_bella`, which was never actually used in a real render).

**Randomized Ken Burns motion added, and a real pre-existing bug found**: built a
10-motion pool (zoom in/out, 4 straight pans, 4 diagonal pans), seeded per-segment
for reproducibility. Verifying by pixel-diff (not exit code) at first gave a false
negative — *input-side* `-ss` seeking snaps to the nearest keyframe (frame 0 on
these short clips), masking real motion; switched to *output-side* seeking and found
a genuine bug: `zoom_in`'s `zoompan` state wasn't reliably defaulting to 1.0 on this
ffmpeg build, so it had been rendering as a near-static clip since this pipeline was
first built on 10-25 — fixed with an explicit `if(eq(on,0),1.0,...)` start value.
**(Ken Burns motion itself was discarded entirely the next day, 10-28 — kept as a
dormant toggle.)**

**Visual sourcing priority flipped — the biggest architecture change of the
project**: AI-generated visuals (Gemini live via Chrome, Pollinations as the
automatable fallback) became the *primary* full-frame visual on every segment,
carrying the SOLID/CONTESTED/UNCERTAIN/myth confidence treatment; Wikimedia/NASA/
Pixabay/Smithsonian and live Chrome screenshots were demoted to a small bordered
"evidence" inset (randomized corner/center position, labeled SOURCE, one at a
time). New `[EVIDENCE: "term"]` / `[EVIDENCE: screenshot: "<url>"]` cue in
`script_parser.py`; `visuals/resolve.py` rewritten so a bare search-term
`[ON SCREEN: ...]` cue now raises `ValueError` instead of silently resolving against
the old sources — forces old scripts to be rewritten, not reinterpreted. New
`pipeline/evidence.py` for seeded inset placement, shared by `assemble.py` (image)
and `captions.py` (SOURCE label) so they can't land in different spots. Verified
first on a throwaway smoke-test slug, then for real: regenerated 17 of
`library-of-alexandria-destruction`'s 20 segments via live Gemini (one new chat per
segment to avoid a stale-chat mixup), surgically removing only those 17 entries from
`manifest.json` first so the 3 already-Pollinations-compliant segments weren't
wastefully re-generated. Re-rendering this also **re-triggered the captions-wipe bug
from 10-25** (`captions.ass` was a day stale, then regenerating it exposed
`narration_meta.json`'s wiped `words` field) — fixed the same documented way.

**Content rectangle redesign**: user wanted the content area shortened and widened
to span the full mobile screen. Measured a reference image precisely (PIL
brightness-scan, not eyeballing): a 1080x608 rectangle (16:9-ish), vertically
centered, replaced the old 880x880 square — required splitting
`SQUARE_SIZE`→`SQUARE_WIDTH`/`SQUARE_HEIGHT` everywhere it was used as both a width
and height term. (User's own commit; logged here for continuity.)

**Visual-style pivot — biggest content-direction change of the project**: analyzed
a second reference video (16 frames + full transcript) and found a genuinely
different, reusable system: flat-vector/painted-scene two-mode illustration (not
photoreal), a consistent flat stick-figure character style, a muted earth palette
with saturated color reserved for semantic meaning, and a sarcastic/dark-humor tone
overlapping the channel's own SOLID/CONTESTED angle. Built **`visual-style-brief.md`**
(new channel-wide doc): two-mode system (flat explainer for diagrams, painted scene
for narrative), character guidance explicitly *not* chasing cross-prompt
consistency (same limitation that keeps the host-character toggle off), palette
rules, a baked-in-text constraint (short diagram labels only — full sentences
duplicate the caption track), confidence treatment adapted to illustration (line
weight/desaturation instead of grain/blur), and workflow discipline for live-Gemini
sessions (max 2 retries per chat, max 4 attempts before switching chats — citing
the 10-26 stale-chat near-miss). Updated `voice.md`'s tone to "loud, confident,
sarcastic, and disciplined" without loosening the no-invented-claims rule, and added
a mandatory sarcastic episode-specific CTA line after the closing question.

**Cut-rate rule adopted**: measured, not guessed — ffmpeg scene-cut detection on the
full reference video found 98 shots, median 3.03s, 78% at ≤4s. Added
`config.MAX_SEGMENT_DURATION_SEC = 4.0` with a non-fatal warning in `narration.py`
when a resolved segment exceeds it.

**Punctuation rule adopted**: reading `kokoro_onnx`'s source directly found it only
manages pauses on its own `SENTENCE_MARKS`/`CLAUSE_MARKS` — this channel's allowed
set is narrower: `. , ! : ?` only. Built
`script_parser.normalize_pause_punctuation()` (em/en-dash/hyphen→comma;
semicolon/ellipsis→period; parentheticals→comma-wrapped asides), composed with
`strip_markdown_emphasis()`. Also added `_warn_if_narration_stale()` — a non-fatal
mtime check (script.md vs. narration_meta.json) since `--from-stage visuals` skips
re-parsing and would otherwise silently resolve against stale data.

**Captions moved back to the bottom bar** (`alignment=2`, was full-frame-centered
from 10-26) — same word-pop style, `marginv` now derived from the content
rectangle's actual height instead of hardcoded.

Side research: Wan2GP/WanGP's license (`WanGP Community License 2.0`, fetched
directly from GitHub, not a mirror) genuinely permits this channel's free/
ad-monetized use with no attribution owed — legally clear, but **blocked
practically**: its video-diffusion models need a real discrete GPU, which this
machine doesn't have. Not pursued.

# 2026-10-28 — Music/SFX dropped, gemini-test fully rebuilt, Ken Burns discarded, watermark handling settled

**Music/SFX dropped from production as a toggle, not a deletion**:
`config.ENABLE_MUSIC`/`ENABLE_SFX = False`; `audio_mix.py` gained its own `no_sfx`
switch (previously missing — SFX had always run regardless of `--no-music`);
`render.py`'s CLI flipped from opt-out to opt-in (`--music`/`--sfx`). `Assets_audio/`
and the generator/dev tree left fully on disk, unused.

**`library-of-alexandria-destruction-gemini-test` fully rebuilt**: recalculated the
script's 7 cues against the real segment-timing formula and split into 18
(2.08–3.93s each) before generating anything. Rewrote all 18 `[ON SCREEN: ...]`
cues to the current `AI-generate:` grammar. Generated all 18 live via Gemini — real
friction: a download-verification race grabbed a stale file twice (fixed by
cross-checking timestamp against the last known-good download before trusting a
grab); a literal two-bar-chart concept failed 4 attempts and was abandoned for an
achievable scroll-stack visual instead (per the brief's own "stop iterating, switch
concepts" discipline) — script's cues rewritten to match what was actually
generated. **Hit the captions-wipe bug a third time** (narration re-run for timing
math wiped `words`) — fixed the same documented way, this time verified by pulling
the real first word event's exact timestamp from the regenerated `.ass` file rather
than a guessed one.

**Ken Burns motion discarded entirely** (`config.ENABLE_KEN_BURNS = False`, zoompan
code path left intact but unused): every still image now holds fixed, fully
visible, centered (fit within the rectangle, pad to center — never crop). A real
bug caught before shipping: a redundant `fps=` filter after the pad caused a
systematic ~1-frame-per-clip rounding loss (18 clips → 0.6s of audio silently
trimmed by `assemble()`'s `-shortest` flag) — caught by comparing the silent
video's duration against the audio mix's, not the final output alone; fixed by
removing the redundant filter.

**Gemini watermark — inpainting tried and rejected, several approaches honestly
evaluated and all left visible artifacts on detailed illustrated content** (plain
Telea inpaint left a dark pyramid smudge at hard tone boundaries; masking/feathering
variants reduced but didn't eliminate it). Asked the user rather than guessing; user
chose **crop with headroom**: generate with the subject composed in the top ~85%,
crop the bottom 15% (`config.GEMINI_WATERMARK_CROP_FRAC = 0.15`, gated on
`manifest[...]["source"] == "gemini"` only). **Then, later the same day, reverted
again**: user asked to stop cropping and instead ask Gemini via the prompt to keep
the watermark small/cornered — tested this honestly before trusting it, and the
result was worse, not better (the usual sparkle unchanged, plus an unrelated new
monogram painted into the scene, since the model read "signature mark" as license
to add one). **Final standing rule: crop disabled
(`config.ENABLE_GEMINI_WATERMARK_CROP = False`), watermark shows, never mention it
in a prompt.**

Mid-regeneration of the production Alexandria slug's deleted images (a separate
earlier request), hit a real **stuck download** that the user caught live before
the agent did — new standing rules added to `visual-style-brief.md` §8a–8c: (a)
retry once same-chat, once in a new chat, then stop and leave it for manual
download; (b) never render/assemble until every segment has an actual file on disk;
(c) only a genuine Gemini quota wall (not a download failure) may fall through to
Pollinations.

# 2026-10-29 — `Human Evolution Part 1` built and published; channel created

First real (non-test) video, under the new `videos/Production Videos/<slug>/`
convention (gitignored). Topic: Human Evolution Part 1 (dinosaur extinction through
first hominin candidates). `research.md`/`script.md` built by hand following the
skills' own process (10 claims, hook 71/WORKABLE). Added a real fact mid-session
(India still an isolated landmass at 66 Mya, not yet collided with Eurasia) after
verifying it via `WebSearch`.

Two real `script_parser.py` bugs found parsing this script for the first time: bold
subheadings (originally `###` headings) truncated parsing to zero beats (any
heading level stops section extraction) — fixed by converting to plain bold labels;
two multi-line beat labels broke the single-line-only label regex — fixed by
joining them.

25 Gemini image prompts generated live. Real bug: a prompt saying "letterboxed"
composition got taken literally — Gemini painted real black bars into the image
content — fixed by rewording to "full-bleed, no borders" across all later prompts,
zero recurrence. Watermark handled via the user's own idea: crop both left/right
edges symmetrically (not top/bottom) — measured the real watermark bounding box and
the content rectangle's target aspect precisely before cropping, landing within
0.03% of the target aspect with a 30px safety margin on the mark.

Title font switched to Papyrus for the title band only — an initial look appeared
to be a plain-serif fallback and was briefly (wrongly) reported as a font-resolution
failure; investigating properly (verbose ffmpeg logging) showed it was actually
rendering correctly all along (this build's libass prefers Windows DirectWrite over
fontconfig) — corrected the earlier wrong claim to the user rather than leaving it
standing.

First full pipeline run for this video: `am_adam` voice (per-video choice, faster
real pace than assumed — 109.6s vs. the ~2:10 estimate), 12 cut-rate warnings
printed (not yet fixed at this point). Both `[EVIDENCE: ...]` cues auto-resolved to
real Wikimedia photos with no manual sourcing.

**YouTube channel created: MindParadox** (`@MindParadox-n1p`) — resolves the
long-open "doesn't exist yet" item. Profile picture/banner generated via Gemini
prompts built from the old logo's *content* (not the image itself, per instruction).
A real bug: the first banner generation put the character/text band in the middle
of a visually separate starfield, flanked by a mismatched plain background — fixed
by stating explicitly that the entire canvas is one continuous scene before giving
the safe-zone placement rule. Verified live on the channel page; zero videos
uploaded yet at this point.

`am_adam` **promoted from per-video exception to global default voice**, superseding
`hf_alpha` (which had never actually been used in a real production render).

**12 cut-rate warnings resolved by splitting segments, not trimming**: subdivided
the 12 over-cap segments into 13 new cues at word-balanced points (38 segments
total, up from 25); 9 of the new images reused existing art by rename, 13 were
newly generated. A real bug: 8 of the new images landed at filenames that collided
with a stale cached `manifest.json` entry — the cache check only verifies the file
*exists*, not that its content is current, so stale *metadata* (not the actual
rendered visual) survived a non-force `resolve.py` run — fixed with one `--force`
pass. Final: 109.5s, verified against 4 newly-split segments' real timestamps.

**Human watch/listen pass done — video confirmed final.** Packaging drafted via
`yt-package`/`yt-seo`: title "Could a 7-Million-Year-Old Fossil Even Walk?"
(100/100), thumbnail paired text "NOT YOUR ANCESTOR" (zero word-overlap, 100/100),
description with 6 real-timestamp chapters, 15 disambiguation tags. Thumbnail built
via a one-off Pillow script (not AI-generated — confirmed explicitly to the user),
compositing the already-sourced Sahelanthropus evidence photo.

**Published**: live, public, at `youtube.com/shorts/cGz7bPl295I`. Uploaded via
Chrome automation (`file_upload` tool — native OS pickers can't be driven);
Publish and the Made-for-Kids designation were both left for the user to click/
confirm per this project's publishing-requires-explicit-permission rule. A real
duplicate-draft bug: force-navigating past a "Leave site?" warning silently
discarded an in-progress draft's edits, leaving a stray duplicate Short in Content >
Shorts — caught by checking Content > Shorts directly, deleted only after explicit
user confirmation. **Cross-posted to Instagram** (`instagram.com/mindparadoxx06`)
the same day with adapted packaging (shorter caption, no clickable timestamps,
Instagram-tuned hashtags) — researched first that cross-posting doesn't affect
YouTube monetization. One near-miss: pressing Escape to dismiss an autocomplete
dropdown nearly triggered Instagram's "Discard post?" dialog — caught before
confirming, Cancel pressed instead.

# 2026-10-30 — Kokoro's Greek/Ptolemaic pronunciation confirmed good by ear

Resolved the item open since 10-26: whether Kokoro (now `am_adam`) actually
mispronounces the Alexandria script's Greek/Ptolemaic proper nouns, or whether
Whisper's `base` model was just mishearing them. Built
`pipeline/tools/pronunciation_test.py` (same convention as `tools/pick_voice.py`) —
synthesizes the real production-script lines containing each name (Mouseion,
Ptolemaic, Demetrius of Phalerum, Ptolemy I, Caesar, Strabo, Serapeum, Theophilus,
caliph, Bar Hebraeus) with the current default voice, writes each to
`pronunciation-test/`, and runs the same `faster-whisper` config used in the real
pipeline as a cross-check. Whisper's transcript garbled several names anyway
(Mouseion→"Mausian", Ptolemaic→"Tolmeic", etc.) — expected, and exactly why this
needed a real human ear rather than trusting Whisper's own output. **User listened
to all 5 and confirmed: all good.** Test script and `.wav` files left on disk for
reuse if a future voice change needs the same check redone.

---

# Current state (as of 2026-10-30)

- **Channel**: MindParadox, live on YouTube Shorts + Instagram Reels, 1 video
  published on both (`Human Evolution Part 1`).
- **Voice**: `am_adam`, `--lang en-us` — channel-wide default
  (history: `af_heart`→`am_michael`→`af_bella`→`hf_alpha`→**`am_adam`**). Greek/
  Ptolemaic pronunciation confirmed good by ear (10-30). `hm_omega`/`--lang hi` is
  the tested choice if genuine Hindi narration is ever produced again.
- **Audio**: narration-only; `ENABLE_MUSIC`/`ENABLE_SFX = False` (toggles — both
  music libraries and the SFX catalog still on disk, unused). Bollywood-emotion
  library: zero tracks ever composed, now moot.
- **Visuals**: Gemini (live Chrome) primary, Pollinations the automatable fallback;
  Wikimedia/NASA/Pixabay/Smithsonian/screenshots demoted to a bordered `[EVIDENCE:
  ...]` inset only. Flat-explainer/painted-scene illustrated style
  (`visual-style-brief.md`), not photoreal. `ENABLE_KEN_BURNS = False` (images hold
  fixed/centered). `ENABLE_GEMINI_WATERMARK_CROP = False` (watermark shows; never
  mention it in a prompt — tested and made things worse once). Host character
  overlay off (`SHOW_CHARACTER = False`, single pose only, dormant).
- **Frame**: black 1080x1920 canvas, title band, 1080x608 full-width letterboxed
  content rect, bottom caption bar (word-pop style, one word at a time).
- **Known recurring pipeline bugs** (see also the `pipeline_gotchas` memory file):
  any `narration.py` run wipes `alignment.py`'s word data — always re-run
  `alignment.py --force` → `captions.py` after; `assemble.py`'s resume only checks
  file existence, not staleness, for both clips and `final.mp4`; `--force` on
  `assemble.py` alone never regenerates captions; `--from-stage visuals` skips
  re-parsing `script.md`; force only the stage that actually changed, never a
  blanket `--force`.
- **Open / not yet done**: character pose variety still single-pose (dormant, not
  blocking since the overlay is off); mobile push notifications still disabled in
  `/config`; `ClaudeAnimationBase` (code-rendered consistent host character) parked
  as a possible future fix if the character overlay is ever revisited — untested on
  this hardware; Wan2GP/WanGP legally usable but blocked by lack of a discrete GPU.
