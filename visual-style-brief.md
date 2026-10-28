# visual-style-brief.md

What every `AI-generate:` cue in every script is written against. Read this before
writing a single Gemini or Pollinations prompt - it replaces the old photoreal-
documentary default (2026-10-27, see `idea.md`'s decision-log entry) with a
flat-vector/painted-scene illustrated style, modeled on a reference video. For
narration tone, see `voice.md` - this file is narration's visual counterpart, not a
tone document.

## 1. The two-mode system

Every primary visual is one of two modes - pick per prompt, not once per video:

- **Flat explainer mode.** Pure vector line art, flat color fills, a white or solid-
  color background. Use for diagrams, comparisons, object close-ups, and any beat
  that's explaining a mechanism or fact rather than telling a scene (e.g. "the
  surgical tool," a bar-chart lifespan comparison, a before/after split panel). Can
  carry a short all-caps hand-drawn-style diagram label and a red hand-drawn
  annotation arrow pointing at the relevant detail.
- **Painted scene mode.** The same flat character style placed into a fully shaded,
  painterly environment - soft gradient lighting, real depth and texture in the
  background (a cave wall, a jungle hut, a courtyard). Use for narrative/storytelling
  beats - anywhere the script is putting the viewer *in* a moment, not explaining a
  concept at them.

Rule of thumb: Explanation-beat diagram/mechanism content -> flat. Storytelling/
Questionary-beat narrative moments -> painted.

## 2. Character guidance

Style reference for any human figure: round cream/white head, simple black dot eyes,
a single thin eyebrow line carrying all the expression (furrowed = pain/confusion,
soft curve = content/caring), no nose, minimal mouth. Thin black-outline limbs, no
visible joints. Messy brown scribble hair. Clothing rendered with a jagged,
scribbled fur/hide texture where period-appropriate.

**Do not chase cross-prompt character consistency.** Gemini and Pollinations cannot
reliably reproduce an exact recurring character across separate generations - this
is a confirmed, documented limitation of this pipeline (it's the same reason the
project's own host-overlay character is currently off, `config.SHOW_CHARACTER =
False` in `pipeline/config.py` - repeated attempts at consistent gesture variety
failed). Don't write a prompt that says "the same character as the previous image."
Instead, aim for *prompt-internal* consistency: within one image, the character,
palette, line weight, and mode should all clearly belong to the same style
described in this brief, even if the exact character doesn't carry over to the next
segment pixel-for-pixel.

## 3. Color palette

Muted earth tones as the default base: grays, browns, tans, dusty teal/blue.
Saturated color is reserved for semantic meaning only, never decoration:

- **Red** - danger, pain, annotation arrows/callouts.
- **Green** - parasites, mold, jungle/nature elements.
- **Blue** - neutral informational backdrops (a flat-explainer card with no danger/
  nature content).

Optional flourish: small corner ornament motifs that vary by the section's subject
(leaves/twigs for a nature or jungle beat, bones for a mortality/stakes beat) - not
fixed per-video branding, pick what fits the specific beat.

## 4. Baked-in text constraint (read this before writing any prompt)

`pipeline/captions.py` already burns full-frame, word-pop captions over every
segment, and `pipeline/assemble.py` burns the video's title into a fixed band. **A
generated image must never bake in a full sentence of text** - it would duplicate
the caption track and clutter the frame.

What's allowed: a short diagram label that's part of the diagram itself (e.g. "THE
SURGICAL TOOL," "NOT ON DISPLAY," "CAN'T WALK -> CAN'T EAT") - two to five words,
describing what's drawn, not restating the narration sentence-for-sentence.

The test: if the text would restate what's being spoken at that moment, it doesn't
belong in the image. If it's labeling a part of the diagram the way an annotation
arrow does, it's fine.

## 5. Confidence-based treatment

Same four-way split as the narration's own confidence tags (SOLID / CONTESTED /
UNCERTAIN / myth, from `research.md`), adapted from the old photoreal cues to this
illustrated style:

- **SOLID** beats: clean, confident rendering in whichever mode fits (flat or
  painted) - firm line weight, full color, no visual hedge.
- **CONTESTED / UNCERTAIN** beats: same mode, but with a visible uncertainty cue
  appropriate to illustration rather than photography - sketchier/looser line
  weight, a desaturated or muted palette variant, or a dashed-line/question-mark
  motif worked into the composition. The point is the same as before: the visual
  signals lower certainty without the narration having to say so twice.
- **Myth/legend**: lean fully into painted-manuscript/storybook treatment - aged
  paper texture, illuminated-manuscript framing, something that reads as "this is
  how the story goes," never a documentary reenactment of an event that may not
  have happened as described.

## 6. Cut rate - how long each image stays on screen

**No single image should hold for more than ~4 seconds.** This was measured, not
guessed: running scene-cut detection on the reference video (`ffmpeg`'s scene filter
against the full 345s runtime) found 98 shots, median 3.03s, mean 3.52s, and 78% of
all shots at 4 seconds or under. Cuts track the audio - most shots run 2-4s, tied to
a sentence or clause boundary, not a fixed uniform interval. The few outliers that
ran longer (7-15s) were all a single flat-explainer diagram card held static through
one extended explanation (a timeline comparison, a map, a survival-rate chart) - not
a narrative/painted-scene beat. Default to the 4s ceiling everywhere; if an
explanation genuinely needs one diagram on screen longer than that, place additional
`AI-generate:` cues for the same subject (a different angle/zoom on the same
diagram) rather than holding one static image past 4s.

In practice: this is the same discipline as `yt-script/SKILL.md`'s cue-density rule
("place a new cue at every natural break in the narration") - a script with cues
placed correctly will naturally produce segments under this cap, since
`narration.py` times each segment proportionally by its word count. `narration.py`
also prints a warning (not a hard failure) when a resolved segment's computed
duration exceeds `config.MAX_SEGMENT_DURATION_SEC` (4.0s), as a build-time signal
that a beat needs its cues split further - don't ignore that warning.

## 7. Per-prompt field template

Write each `AI-generate:` prompt with these in mind (not necessarily as literal
labeled fields in the final prompt text, but as a checklist):

- **Mode** - flat explainer or painted scene.
- **Subject/setting** - what's actually in frame.
- **Palette note** - which of the base earth tones + which semantic accent, if any.
- **Confidence cue** - SOLID / CONTESTED-UNCERTAIN / myth treatment, per section 5.
- **Diagram label text** - only if flat mode and only if short (section 4).
- **Aspect/crop** - the image fills the branded frame's content rectangle
  (1080x608, full width, letterboxed - `pipeline/config.py`'s `SQUARE_WIDTH`/
  `SQUARE_HEIGHT`), not the old square. Compose for a wide, short frame, not a
  square one.
- **Bottom headroom for the watermark crop** - Gemini bakes a small gray
  sparkle watermark into the bottom-right corner of every image it generates.
  `assemble.py` crops off the bottom 15% of every Gemini-sourced image before
  fitting it into the content rectangle (`config.GEMINI_WATERMARK_CROP_FRAC`),
  which removes the watermark along with that strip - so the prompt should
  compose the actual subject within the top ~85% of the frame and treat the
  bottom ~15% as disposable margin (ground, empty space, nothing essential),
  not critical composition. An inpainting-based removal was tried first and
  rejected - see `memory.md` - it left a visible patch on anything but a flat
  background, so the crop-with-headroom approach is the standing rule now,
  not a one-off fix.

## 8. Workflow discipline for the live Gemini session

Script first, always: a live Gemini session or an `AI-generate:` prompt only ever
starts against a script.md that has already cleared `yt-script/SKILL.md`'s gate -
generating against a script still being revised means generating against text
that's about to change, not the one the video will actually ship with.

Gemini generation in this project is always manual and live - a Chrome browser
session the user starts, never API-automated (free-tier image generation is
confirmed blocked via the API). When a generated image doesn't match the prompt:

- **At most 2 retries in the same chat** for a minor accuracy fix (wrong detail,
  slightly off composition).
- **At most 4 total attempts.** If it's still wrong after that, stop iterating on
  that prompt in that chat.
- **Switch to a new Gemini conversation/chat tab** for that prompt instead of
  continuing to hammer the stale one. This isn't just discipline for its own sake -
  a stale chat already caused a real near-miss wrong-clip download once (an older,
  similar-looking chat from an earlier session nearly got downloaded as if it were
  the fresh retry's output; caught before it shipped). One new chat per segment is
  already this project's adopted norm for exactly this reason - this extends the
  same discipline to when a single prompt is failing repeatedly, not just to
  starting each new segment.

### 8a. Download-failure recovery (decided 2026-10-28)

This is a different failure from a wrong-looking image above - here the image is
fine but clicking "Download full size" doesn't actually produce a new file in
Downloads (confirmed by checking, not assumed). Don't loop on this indefinitely:

1. Close the full Gemini tab, reopen Gemini back onto that **same** conversation
   (not a new chat), and retry the download once.
2. If that still fails, discard that image and generate a fresh one in a **new**
   conversation, then try downloading that one.
3. If the new conversation's download also fails, **stop retrying downloads for
   that segment entirely.**
4. From that point on, generate every remaining segment's image as normal (one
   new conversation each), but don't attempt to download any of them - leave each
   one sitting in its own conversation for the user to download manually later
   (e.g. "I'll download the rest at 7am").

### 8b. Render/assemble gate (decided 2026-10-28)

`render.py --from-stage visuals` (or any later stage) must only run once **every**
segment of that video has an actual image file resolved on disk - either a
successfully downloaded Gemini asset in `build/visuals_gemini/`, or a
Pollinations-generated file per 8c below. If even one segment was left pending
manual download under 8a, don't resolve/caption/mix/assemble yet - wait until
every image is actually on disk first.

### 8c. Gemini-quota fallback to Pollinations (decided 2026-10-28)

Gemini is always the first choice for every segment - never start a segment on
Pollinations by default. But if Gemini's own generation limit is hit (an actual
"come back later"/quota message, not a download-mechanics failure) during a
late-night session where waiting for the reset isn't practical, switch the
remaining ungenerated segments to Pollinations.ai (`ai_generate.py` - already
wired into `resolve.py` as the automatic fallback whenever no pre-placed Gemini
asset exists for a segment) and keep going rather than stopping the whole video.
This path only applies to a genuine generation-quota wall; a download-mechanics
failure always follows 8a instead (deferred to manual download, never silently
switched to Pollinations).

## 9. Relationship to evidence insets

This brief governs the **primary** `AI-generate:` visual only. The optional
`[EVIDENCE: ...]` inset (a real photo/document/screenshot shown as proof, bordered
and labeled SOURCE) is unaffected by this style pivot - it stays real-photo-sourced
via Wikimedia/NASA/Pixabay/Smithsonian or a live Chrome screenshot, per the existing
rule in `yt-script/SKILL.md`.
