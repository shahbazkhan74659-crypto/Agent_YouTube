# The Idea

A YouTube channel posting **2 videos/day**, explainer/motion-graphics style, covering
**Scientific, Historical, and Philosophical** topics.

- No autopilot, no mass-produced templated content (explicitly ruled out).
- Each video gets its own script/topic — not a recurring character run through the same
  template repeatedly.
- Format fit: closer to **Path 2** (Claude Code + motion graphics: script → ElevenLabs
  voiceover → word-synced kinetic text/diagrams → render) than Path 1 (Wan2GP faceless
  cartoon character channel) from the source PDF.

## Origin

Sparked by `EARN-System-by-siddhantt.ai.pdf` (in Downloads) — a lead-magnet guide pitching
two paths: (1) a faceless Wan2GP cartoon-character Shorts channel on autopilot, (2) paid
motion-graphics client/portfolio work via Claude Code. See `research-findings.md` for the
evaluation of that source and the niche research behind this pivot.

## Tooling installed

- **`youtube-agent-skill`** (github.com/Jakeschincariol/youtube-agent-skill, MIT,
  free, no API keys) — 11 Claude skills installed globally: `/yt-script`,
  `/yt-package`, `/yt-retention`, `/yt-edit`, `/yt-comment`, `/yt-plan`, `/yt-viral`,
  `/yt-shorts`, `/yt-seo`, `/yt-chapters`, `/yt-audit`. Covers script structure/hooks,
  title+thumbnail packaging, retention analysis, editing from transcript, SEO,
  chapters, comments, and niche research. Reviewed source (no network calls, no
  prompt-injection red flags) before install.
  - **Does not cover:** source-grounding/fact-checking for contested history/
    philosophy claims — `/yt-script` refuses to invent facts but doesn't verify them
    against sources either. That's still a separate, unbuilt piece.
  - **Decided:** customize these skills + add new ones before the channel actually
    launches (not using them as-is out of the box).
  - `voice.md` template copied to `C:\YouTube\voice.md` (the project folder was
    later renamed from `C:\Idea` to `C:\YouTube` — every path below reflects the
    current location), not yet filled in at the time — every script-writing skill
    reads this file, matters more than anywhere else per the toolkit's own docs.

### Customization (done)

- **`yt-script`** — rewritten for a narration-only channel (dropped on-camera/
  "paste 3 of your videos" assumptions, since the channel is pre-launch and
  TTS-narrated). Now requires a `research.md` brief (see `yt-factcheck` below)
  before writing any factual claim — SOLID/CONTESTED/UNCERTAIN confidence levels
  carry through into how the script states each claim. `[ON SCREEN: ...]` cues must
  now name a sourceable visual (Wikimedia/NASA/Pixabay/Smithsonian search term, or an
  `AI-generate:` prompt) instead of a vague description. `hooks.json` examples
  reworded from creator-economy flavor to science/history/philosophy flavor
  (cosmetic only — the functional regex patterns are untouched).
- **`yt-factcheck`** (new skill) — gather → draft claims with confidence tags →
  independent verification by a *fresh* subagent with no memory of the draft →
  visual anchors → `research.md` brief. Built on `sources.py` (stdlib-only, no
  dependencies): free keyless lookups against Wikipedia, Internet Archive, and
  Semantic Scholar. Internet Archive results are noisy (crowdsourced, not curated —
  documented as a known caveat); Semantic Scholar's free tier rate-limits
  aggressively (treated as best-effort).
- **`voice.md`** — reworked for narration/TTS instead of on-camera presence: tone
  description instead of video transcripts, Kokoro voice preset + pacing + visual
  style mix in "My format," and a line tying "what I will not claim" to
  `yt-factcheck`'s UNCERTAIN tag.
- **File convention** — `C:\YouTube\videos\<topic-slug>\` holds `research.md` +
  `script.md` per video.
- **Platform-agnostic confirmed** — `yt-factcheck` has nothing YouTube-specific in
  it (no YouTube API calls, no video-length assumptions); it just researches a topic
  and writes `research.md`. Reusable as-is for fact-checking Instagram Reels or any
  other short-form content via `/yt-factcheck <topic>`, independent of `yt-script`.
  A separate Reels-specific script-writing skill (tuned for Reels pacing/format, the
  way `yt-script` is tuned for YouTube retention beats) is a possible future item,
  not yet decided.
- **Live-tested end to end** on "Library of Alexandria — why/how it was destroyed"
  (`C:\YouTube\videos\library-of-alexandria-destruction\`): `yt-factcheck` caught and
  downgraded a real claim (the Serapeum's 391 CE destruction is solid; its link to
  "the library" specifically is not, per independent verification) and correctly
  flagged the Caliph Omar story as an unsupported legend rather than stating it as
  fact. `yt-script` then produced a grounded script from that brief. One honest
  finding: `hookscore.py` is calibrated for growth-hack/personal-stakes content, so
  pure historical-curiosity hooks score WEAK on its STAKES property — resisted the
  urge to invent false stakes to game the score, since that would undercut the
  fact-checking discipline just built. Worth revisiting the tool's weighting for
  this niche separately.
- **`hookscore.py`'s STAKES property fixed (2026-10-25)** — the regex only recognized
  personal-loss words ("lose", "waste", "risk", "fail"), so a pure historical-curiosity
  hook with none of those floored at `STAKES: 22` regardless of how strong it actually
  was, and the tool's deliberate weakest-link weighting (40% of VERDICT) then dragged
  the whole score down on that one property alone. Fixed by adding
  destruction/erasure/mystery vocabulary genuinely native to this niche's stakes
  ("destroyed", "vanished", "disappeared", "forgotten", "erased", "buried", "hidden",
  "forbidden", "banned", "silenced", "extinct", "collapsed", "ruins", "perished",
  "wiped", "unsolved", "mystery", "burned", "fell", "doomed") to the `STAKE` regex in
  `yt-script/hookscore.py`. Verified against the Alexandria test script: hook #1 moved
  from 54 (WEAK) to 57 (WORKABLE); four synthetic pure-curiosity hooks with no stake
  words moved from a flat `STAKES: 22` floor to 48, and a self-help-style control hook
  ("You are wasting money...") was unaffected — confirming the fix adds niche-relevant
  vocabulary without diluting the property's signal elsewhere.
- **Skill audit (2026-10-25)** — reviewed the 9 remaining generic `yt-*` skills
  against the actual pipeline (TTS-only narration, no raw human recording, every
  video natively Shorts-length). 7 are channel-stage/niche-agnostic and fine
  as-is (`yt-audit`, `yt-chapters`, `yt-comment`, `yt-package`, `yt-retention`,
  `yt-seo`, `yt-viral` — unusable only until there's an actual channel/videos/
  comments to feed them, not a content mismatch). 2 had a genuine scope
  mismatch and were changed:
  - **`yt-edit`** rewritten — it was built for a human raw take (dead air from
    pauses, filler from rambling, repeats from retakes), which doesn't exist in
    a clean Kokoro TTS render. Reframed as a QC pass on the generated narration
    using the `faster-whisper` segment-level transcript already produced during
    the existing alignment step: DEAD now means unnatural TTS-inserted pauses;
    FILLER/REPEAT are documented as dormant safety nets (script-leakage,
    accidental duplicate renders) rather than human-performance issues. No code
    changes to `deadair.py` — its parser/gap logic already worked on any
    `start`/`end`/`text` segment data regardless of source, and it's still
    imported directly by `yt-retention/retention.py` and
    `yt-chapters/chapters.py`.
  - **`yt-shortcraft`** (new skill, added alongside the untouched `yt-shorts`) —
    `yt-shorts` was built to mine a clip out of a longer video, but every video
    here is already natively a Short. `yt-shortcraft` keeps the same craft bar
    (hook via `hookscore.py`, on-screen text in the first two seconds, loop
    point, vertical framing) applied to a script that already *is* the whole
    video, with the clip-ranking/picking mechanic dropped entirely.
- **`yt-script` updated (2026-10-25)** — the Storytelling → Explanation →
  Questionary structure (see "Differentiation angle" below) is now built into
  `yt-script/SKILL.md`'s "The shape" section directly, not just logged in
  `voice.md`. Also added: an explicit rule that a myth/legend `research.md`
  flags as unsupported must be named and corrected on screen, not just quietly
  skipped; and the closing beat now requires the genuinely unresolved
  CONTESTED/UNCERTAIN question from `research.md`, delivered after the payoff,
  replacing the generic subscribe-pitch ask rather than stacking on top of it.
- **Stale `voice.md` copy found and fixed (2026-10-25)** — discovered two
  different `voice.md` files: the master at `C:\YouTube\voice.md` had moved on
  to the finalized decisions (tone confirmed, length confirmed, the full
  "Differentiation angle" section added), but `~/.claude/youtube/voice.md` —
  the path every skill actually reads from — was still the old draft with
  none of that. Every skill run since those decisions were finalized had been
  reading stale guidance. Refreshed the copy from the master; the two are now
  byte-identical.

## Daily schedule (decided)

- **8:00 PM** — that day's content (1 or more pieces, each within YouTube Shorts'
  maximum length — 3 minutes, vertical/square framing) must be fully produced and
  ready.
- **8:00 PM – 11:00 PM** — collab window: Admin + Claude review together, fix
  whatever Admin doesn't like/wants changed/wants added, finalize edit and content.
- **Before 12:00 AM** — upload, regardless of whether Admin was active in the
  collab window; what's ready at 8 PM ships as-is if no changes land by 11 PM.
- Encoded in `yt-plan/SKILL.md` ("Daily production schedule" / "The shape of a
  day") since that's the cadence/scheduling skill — not duplicated into the other
  `yt-*` skills, which operate at the single-video level, not the daily clock.

## Production pipeline (decided)

- **Images/video clips + voiceover + captions**, not from-scratch motion graphics.
  Dropped Blender/3D animation route — hardware (Ryzen 3 5425U, integrated graphics,
  8GB RAM) can't sustain render-heavy motion graphics at a daily cadence; stock/AI
  visuals + FFmpeg-style assembly is light enough to run locally.
- Cadence: starting at **1 video/day** (not 2) to stay within hardware/usage limits.

## Budget decisions

1. **Claude usage** — accepted cost, core to the workflow.
2. **ElevenLabs** — accepted for now; actively look for a cheaper/free TTS
   alternative before committing to a paid tier.
   - **Decided:** use **Kokoro's built-in presets** (free, local, CPU-only, tested
     working — see `research-findings.md`) as the production voice until a dedicated
     Nvidia GPU is bought. Voice cloning (e.g. Coqui XTTS-v2, for narrating in the
     user's own voice) is shelved until then — too slow on CPU-only hardware to be
     worth running now.
3. **Visuals** — mostly free sources + free AI generators; paid stock/AI-image
   subscriptions are optional, not required.
4. **Music/SFX** — self-produced before launch, not licensed/subscribed.
   **Superseded (2026-10-25, same day):** the original 5-bed/7-SFX library
   tied to the Storytelling → Explanation → Questionary structure (described
   in the previous version of this note) was replaced with a much larger
   **topic-based** library: 50 music tracks + 50 SFX across 8 music
   categories (science, history, philosophy, mythology, mysteries,
   knowledge/curiosity, religion/cosmology, general storytelling) and 7 SFX
   categories, procedural synthesis via numpy/scipy/soundfile
   (`C:\YouTube\assets\audio\`), now 48kHz/24-bit (was 44.1kHz/16-bit).
   Full generation source and the validation suite (100/100 assets pass)
   live under `C:\YouTube\assets\audio\src\`/`reports\` — see
   `C:\YouTube\assets\audio\README.md`. **The actual deliverables** (the
   `.wav` files, CSV catalogs, and JSON manifest — `music/`, `sfx/`,
   `metadata/`) were moved out to `C:\YouTube\Assets_audio\` the same day,
   separate from the dev/source-code tree. The old SOLID/CONTESTED
   claim-reveal SFX pairing (epistemic-transparency angle) isn't a dedicated
   asset anymore — the README documents which new SFX (`SFX_PH04_Realization`
   / `SFX_KN04_Discovery_Chime` for SOLID, `SFX_PH06_Unresolved_Thought` /
   `SFX_MI07_Unanswered_Question` for CONTESTED/UNCERTAIN) serve that role
   instead. **Human listen-through started (2026-10-25, same day):** user is
   reviewing category by category; `music/history/` was reviewed first and
   found too repetitive (5-6 of 7 tracks reused one pad+pluck+percussion
   skeleton) and inconsistently/too quiet (peak-only normalization let
   sparse-transient tracks undershoot by up to 9 LU) — all 7 tracks rewritten
   with genuinely distinct lead synthesis per track, plus a new optional
   LUFS-targeting step in `composition.render_bed()` (now -15 to -16 LUFS
   consistently). Other 7 music categories and all 50 SFX still pending
   review — don't treat them as upload-ready yet.
   **Music superseded again, SFX unaffected (2026-10-26):** decided to stop
   using the topic-based `Assets_audio/music/` library for actual production
   (left on disk, untouched, just no longer selected) in favor of a new
   **Bollywood-referenced, emotion-categorized** library — original
   compositions that study Bollywood background-score instrumentation/scales/
   rhythm as a style reference (never sampled or derived from an actual
   copyrighted recording — see legal discussion this was decided against:
   downloading and modifying real Bollywood tracks was explicitly considered
   and rejected over Content ID/copyright risk). `Assets_audio/sfx/` keeps
   being used as-is, unaffected.

   Categorized by **emotion** instead of topic/genre — motivational,
   mysterious, cold, hopeful, cheerful, epic, tense, dark, melancholic,
   romantic, reflective, nostalgic, awe, peaceful (`EMOTION_CATEGORIES` in
   `pipeline/config.py`) — and the emotion can now **shift partway through a
   single video**, tracking its Storytelling → Explanation → Questionary
   structure (or finer), via a new `[MUSIC: <emotion>]` cue in `script.md`
   (same convention as `[ON SCREEN: ...]`). `pipeline/audio_mix.py` was
   rewritten to group consecutive beats sharing an emotion into one
   continuous "part," pick one track per part, and crossfade between parts
   at the boundary instead of looping one bed over the whole video —
   verified end-to-end with synthetic test tones (not real music) before
   trusting it, since the length-preserving crossfade math needed checking.

   **Status: infrastructure only, zero tracks composed yet.** Scaffolding
   built: `Assets_audio/music_bollywood/<emotion>/` (14 empty folders) +
   `metadata/music_catalog_bollywood.csv` (header only) +
   `assets/audio/src/bollywood_primitives.py` (new synthesis primitives —
   tabla/dholak hits, sitar pluck with meend/jawari-buzz approximation,
   tanpura drone, bansuri tone, harmonium drone, string-section swell) +
   a parallel `registry_bollywood.py`/`generate_bollywood.py`/
   `metadata_gen_bollywood.py`/`validate_bollywood.py` trio (mirrors the
   genre library's pattern exactly, fully separate so neither system can
   break the other) + 14 per-emotion module stubs in
   `assets/audio/src/bollywood_music/`. Deliberately not composing any real
   track yet — waiting on actual Bollywood background-score reference
   material and a composition brief per emotion, the same way the original
   genre library waited for a full user-provided spec before any track was
   rendered. See `Assets_audio/music_bollywood/README.md`.
5. **Thumbnails** — **Decided:** GIMP 3.2.6 installed and confirmed working
   (`C:\Users\shahb\AppData\Local\Programs\GIMP 3\bin\gimp-3.exe`) — free, local,
   no subscription. Canva Free stays as fallback only if GIMP genuinely can't cover
   a need (not expected).
6. **Storage** — managed locally by the user, no cloud storage subscription.

Net effect: the only "must-spend, no workaround sought" items are Claude usage and
(for now) ElevenLabs. Everything else is free-first with a paid fallback only if a
free option genuinely doesn't work.

## Render pipeline and visual identity (decided, 2026-10-25/26)

The render pipeline (`script.md` → `final.mp4`, the long-standing #1 blocker) is
**built** — `C:\YouTube\pipeline\`, full detail and the real bugs found/fixed along
the way logged in `memory.md`. **Every video now renders inside a reusable branded
frame, project-wide — not scoped to any one test video**: a black 9:16 canvas, the
video's own title in a top band (white text, long enough to wrap two lines — a real
authoring rule, not just a style choice), and every visual (real sourced photo or
AI-generated) confined to a centered square, with captions in the bottom bar below
it. This is implemented once in `pipeline/config.py`'s shared layout constants
(`SQUARE_SIZE`/`SQUARE_X`/`SQUARE_Y`/`WIDTH`/`HEIGHT`) and applied automatically by
`assemble.py`/`captions.py` to any slug — there is no per-video opt-in.

**Image motion, global (2026-10-27):** every still-image segment gets one of 10
randomized Ken Burns motions (zoom in, zoom out, 4 straight pans, 4 diagonal pans —
`assemble.py`'s `MOTIONS`), assigned per-segment via a seeded random pick so it's
varied but reproducible across re-renders. Applies to every video's still images by
construction (shared pipeline code, not a per-slug setting) — superseded the old
single fixed "always centered zoom-in," which a pixel-diff check that same day found
had been silently non-functional (clamped flat, no visible motion) since it was
first built. Full detail and the bug fix in `memory.md`.

**Visual sourcing priority flipped, global (2026-10-27):** AI-generated visuals
(Pollinations.ai, code-automatable; Gemini, live via the Chrome browser extension
during a session the user manually starts around 10 PM — not headless, not API, not
scheduled) are now the primary full-square visual on every segment, carrying the
confidence-based visual treatment (SOLID = documentary-real, CONTESTED/UNCERTAIN =
same but visibly softened/grained/blurred, myths = illustrated retelling) as a
standing rule. Wikimedia/NASA/Pixabay/Smithsonian and live Chrome screenshots are
demoted to a smaller bordered evidence inset — randomized corner/center position,
labeled SOURCE, one at a time, shown for exactly one segment — never the full square
again. The render pipeline now rejects (`ValueError`) a bare search-term `ON SCREEN`
cue outright rather than silently resolving it against those sources, so an old-style
script must be rewritten, not reinterpreted. New `[EVIDENCE: "term"]` /
`[EVIDENCE: screenshot: "<url>"]` cue in `script.md`; see `pipeline/script_parser.py`,
`visuals/resolve.py`, `assemble.py`, and the new `pipeline/evidence.py`. Verified
first against a throwaway smoke-test slug (stub assets, not committed), then for
real: both already-rendered test videos were initially left untouched, but
**`library-of-alexandria-destruction` was then actually regenerated the same day**
(the "not retroactively applied" caveat above was about not being forced — once the
user had Chrome connected and wanted to see the real result, it was) — 17 of its 20
segments got real Gemini-generated images (the other 3 were already
Pollinations-compliant), confirmed via the manifest (`{"gemini": 17, "pollinations":
3}`, zero Wikimedia/NASA/Pixabay remaining as primary) and by eye across several
frames spanning the full runtime. `library-of-alexandria-destruction-gemini-test`
remains untouched (it was already 100% Gemini-sourced from its original 2026-10-26
build, confirmed compliant without needing any change).

**Two real bugs found and fixed while re-rendering `library-of-alexandria-destruction`
with the new visuals (2026-10-27, same day)**: (1) its `captions.ass` was over a day
stale, still using the pre-redesign bottom-bar karaoke style, because re-running
`resolve.py`/`assemble.py` alone never re-triggers `captions.py` — the mux step just
keeps muxing whatever caption file is already on disk, silently. (2) Regenerating
captions then exposed that `narration_meta.json` had lost its `words` field entirely
(the same silent-wipe failure mode logged on 2026-10-26: a `narration.py` run
rebuilds that file from scratch and wipes alignment data unless `alignment.py` runs
again afterward) — `captions.py`'s `if not words: continue` had been skipping every
beat with no error, so the muxed captions.ass held only the title event. Fixed by
re-running `alignment.py --force` then `captions.py` then a final `assemble.py
--force`; verified by sampling a frame at the exact timestamp of a real word event
pulled from the `.ass` file (not a guessed timestamp) and confirming it renders
dead-center. Full narrative, exact commands, and every verification step in
`memory.md`.

**Host character decided**: a recurring silhouette figure — wide-brim fedora and
long coat matching the channel's own logo (`branding/AstralParadoxDP.png`, "Astral
Paradox") — appears over the background visuals, moving across the square between
cuts. Free AI image generation (Pollinations' only free model) couldn't reliably
render gesture variety after repeated attempts, so it ships as a single consistent
pose for now, with on-screen *position* (not gesture) carrying the movement —
expanding to more poses later is a scoped, known next step, not a dead end.

**Still explicitly deferred, not rejected**: matching the reference video's full
illustrated-art-style backgrounds (vs. today's real-photo-first sourcing) and its
floating-keyword caption style — real sourced photos stay for now since they
support the epistemic-transparency differentiation angle below.

## Open questions / not yet decided

Both prior items here are resolved: TTS was settled early (Kokoro, see Budget §2
above) and the visual-sourcing workflow is now the Gemini+Pollinations-primary /
real-sources-evidence-only setup described in "Visual sourcing priority flipped"
above. Nothing currently open at the project-decision level — see `memory.md`'s
latest "Carried-forward open items" for in-progress/pending work instead (e.g. the
Bollywood music library still has zero composed tracks, character pose variety is
still single-pose, and the actual YouTube channel doesn't exist yet).

## Kokoro voice preset (decided, 2026-10-26; reverted 2026-10-27; promoted to global default, same day)

**`hf_alpha`, with `--lang en-us`** — promoted to the **channel-wide default for every
video**, superseding the same-day `af_bella` revert (never used in any actual render)
and `am_michael`/`af_heart` before it. `hf_alpha` is one of Kokoro's Hindi-trained
voices, deliberately paired with English phonemization (`lang="en-us"`, not `"hi"`) to
get an "Indian tone" on English narration — Kokoro has no dedicated Indian-English
preset, so this combination is the actual mechanism, not a labeled voice choice. Chosen
after listening to 4 candidates (`hf_alpha`/`hf_beta`/`hm_omega`/`hm_psi`) generated to
`C:\YouTube\voice-picker\`; first confirmed on the `library-of-alexandria-destruction-
gemini-test` validation slug, then promoted to global. Logged in `voice.md`'s "My
format" section (both the master and the `~/.claude/youtube/voice.md` mirror, kept in
sync) — that's what `config.get_voice_preset()` reads, so every future render that
doesn't pass an explicit `--voice` override now uses `hf_alpha`/`en-us` automatically.
If genuinely Hindi-language narration is ever produced, use `hm_omega` under
`--lang hi` instead — tested cleanest for actual Hindi, see `memory.md`'s 2026-10-26
entries. **Not retroactively applied**: the existing `library-of-alexandria-destruction`
render still uses its original test voice — this decision governs videos made going
forward, not a forced re-render of what already exists.

## Differentiation angle (decided)

Not visual style (stock/AI-sourced, same raw material any channel can use) —
**epistemic transparency as the format itself**: claims tagged by confidence
(SOLID/CONTESTED/UNCERTAIN), popular myths actively corrected rather than repeated
(e.g. the Caliph Omar legend in the Alexandria test script), sourcing shown rather
than asserted. Harder to copy than a visual style since it requires the
`yt-factcheck` pipeline behind it, not just a tone choice.

Formalized as a three-beat content structure — **Storytelling → Explanation →
Questionary**: narrative hook, then the claims at their actual confidence level,
then deliver the hook's payoff *and* close on the genuinely unresolved question
back to the viewer (question comes after the payoff, never instead of it). Content
stays agnostic/rational across perspectives, open to challenge, treats incomplete
knowledge as the normal state of a topic. Logged in `voice.md` under "My format" /
"Differentiation angle", and built into `yt-script/SKILL.md`'s "The shape" section
as of 2026-10-25 — see "Customization (done)" above.
