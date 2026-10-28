# Script: The Library of Alexandria — Gemini visuals validation test (first ~1 minute)

**Title:** The Destruction of the Library of Alexandria

**Status: VALIDATION TEST** — trimmed to the first 4 beats of
`videos/library-of-alexandria-destruction/script.md` (HOOK through BEAT 2),
now split into **18 visual segments** (up from 7 — see the 2026-10-28 cut-rate
note below). **Reverted 2026-10-27** back to pure English narration —
the Hindi/Hinglish pilot from 2026-10-26 (see `memory.md`) is superseded,
not deleted. Read with an **"Indian tone"**: Kokoro has no dedicated
Indian-English voice, so this tests one of its Hindi-trained presets
speaking English text under `--lang en-us` instead of `hi` — untested before
this. 4 candidates were generated to `voice-picker/` for a listen
(`hf_alpha`/`hf_beta`/`hm_omega`/`hm_psi`); **`hf_alpha` confirmed 2026-10-27**
after listening, superseding the `hm_omega` placeholder used in the first
revert pass. Scoped to this test video only — the channel-wide production
preset in `voice.md` stays `af_bella`, untouched by this (later superseded
channel-wide by `hf_alpha`, also untouched by this scoped slug unless re-tested).
The `build/romanized.json` positional-caption workaround from the Hindi pilot no
longer applies — moved aside (`romanized_hindi_test.json.bak`) — captions use the
normal English `reconcile_words()` text-matching path, which also restores
digit-formatted numbers in the subtitle (`40,000`, `700,000`, `three-hundred-year`
→ `300-year`) instead of the Hinglish positional zip.

**Rewritten 2026-10-28** — the `[ON SCREEN: ...]` cues below were previously bare
Wikimedia search terms (old grammar, predates the 2026-10-27 visual-sourcing flip;
`resolve.py` now raises `ValueError` on that form for the primary visual). Rewritten
to `AI-generate:` prompts per `visual-style-brief.md`'s two-mode illustrated style,
grounded in this topic's shared `research.md` (`../library-of-alexandria-destruction/research.md`)
confidence levels: HOOK = myth/legend treatment (the caliph story itself), the
"three-hundred-year death" line = claim 4 (SOLID), Demetrius's proposal = claim 2a
(CONTESTED), the scroll-count beat = claim 3 (SOLID with caveat, caveat carried in
the diagram content itself — a red-flagged outlier bar — rather than the
sketchy/desaturated CONTESTED treatment). This video's `build/` visuals were
deleted in an earlier cleanup pass (see `memory.md`, 2026-10-27 "Test folder
cleanup") — the segments below are being regenerated from scratch via a live
Gemini/Chrome session, not reusing any prior asset.

**Cut-rate pass, same day** — the first rewrite only matched the original 7
`[ON SCREEN: ...]` cue positions, but `visual-style-brief.md`'s ≤4s-per-segment
rule (`config.MAX_SEGMENT_DURATION_SEC`) wasn't checked against this slug's actual
beat durations (`build/narration_meta.json`: beat_01=16.96s, beat_02=10.94s,
beat_03=18.22s, beat_04=15.30s). At 1-2 cues per beat, several resulting segments
would have held 7-12s — several times over the cap. Recalculated precisely against
`narration.py`'s own `_segment_timing()` formula (duration split proportionally by
each segment's word count, not by narration punctuation) and re-split every beat's
cue points so every one of the 18 resulting segments lands at 2.1-4.0s, all cutting
at or near a natural clause break. Where a beat needed more cuts than it had
distinct ideas (BEAT 1's Demetrius sentence, BEAT 2's bar-chart sentence), the
extra segments are a different angle/zoom on the same scene or diagram per the
brief's section 6 guidance, not a new unrelated subject.

**Generation note, same day** — all 18 images generated live via Gemini
(`gemini.google.com/app`, Flash model, one new chat per segment). BEAT 2's
original "two-bar comparison chart" concept for the 40,000-vs-700,000 segments
didn't render reliably after 4 attempts (2 retries in one chat, a fresh chat,
then a simplified prompt — all either merged the two bars into one or dropped
the label text) — per `visual-style-brief.md`'s section 8 discipline, pivoted
to a different concept instead of continuing to force the failing one: a
single precarious, absurdly tall stack of scrolls conveys the same "is this
number real" idea without needing precise multi-bar geometry. The three
`beat_04` cues below reflect what was actually generated, not the original
bar-chart wording.

## Script

**[ON SCREEN: AI-generate: "Painted scene mode, illuminated-manuscript style, a
robed caliph figure approaching a grand pillared library building from a
distance, aged parchment-textured background, ornate gilded border framing, flat
cream-faced stick-limbed character with a single eyebrow line for expression,
muted earth-tone palette with warm gold-leaf accents, storybook legend framing
not a documentary reenactment, wide 16:9 letterboxed composition, no text"]**

**HOOK (0:00-0:15):** Before you believe the caliph burned the Library of Alexandria,

**[ON SCREEN: AI-generate: "Painted scene mode, illuminated-manuscript style, a
close view of a blank undecorated parchment page lying open on a wooden lectern,
aged paper texture, ornate gilded border framing fading at the edges, muted
earth-tone palette, storybook legend framing emphasizing absence rather than
record, wide 16:9 letterboxed composition, no text"]**

know the story has zero evidence

**[ON SCREEN: AI-generate: "Painted scene mode, illuminated-manuscript style, a
flat cream-faced stick-limbed scribe character writing by candlelight in a
dusty cobweb-draped study, visibly much later in time than the event being
described, aged parchment-textured background, ornate gilded border framing,
muted earth-tone palette with warm candle-gold accents, storybook legend
framing, wide 16:9 letterboxed composition, no text"]**

from the century it happened in.

**[ON SCREEN: AI-generate: "Painted scene mode, a single dramatic flame
silhouette rising against the dark outline of the Alexandrian library building
at night, flat cream-faced stick-limbed onlooker character in the foreground,
clean confident linework, full muted earth-tone color (charcoal gray, dusty
brown) with a saturated orange-red fire accent, wide 16:9 letterboxed
composition, no text"]**

The real story isn't one fire —

**[ON SCREEN: AI-generate: "Painted scene mode, the grand Alexandrian library
building shown crumbling in three gradual stages across a dusty earth-tone
landscape, three small suspect vignettes along the timeline, a soldier
silhouette, a fire silhouette, and a creeping-neglect vine silhouette, flat
cream-faced stick-limbed characters, clean confident linework, full muted
brown/gray/dusty-teal color, soft painterly lighting, wide 16:9 letterboxed
composition, no text"]**

it's a three-hundred-year death with at least three different suspects,

**[ON SCREEN: AI-generate: "Painted scene mode, the robed caliph figure standing
outside a locked scroll-room door, visibly apart from the scrolls inside, flat
cream-faced stick-limbed character, clean confident linework, full muted
earth-tone color with a dusty-teal door accent, wide 16:9 letterboxed
composition, no text"]**

and the most famous one probably never touched a single scroll.

**[ON SCREEN: AI-generate: "Painted scene mode, a wide establishing exterior view
of the ancient Library of Alexandria complex, columned facade and courtyard
under a clear Mediterranean sky, flat cream-faced stick-limbed figures small in
the distance for scale, clean confident linework, full muted earth-tone color
(tan stone, dusty teal sky), wide 16:9 letterboxed composition, no text"]**

**THE TURN (0:15-0:30):** Today we're tracing what actually happened to the Library

**[ON SCREEN: AI-generate: "Painted scene mode, the Library's columned reading
hall interior, scrolls stacked on open shelves, half the hall in warm confident
lamplight and half in cooler shadow, flat cream-faced stick-limbed scholar
characters, clean linework, full muted earth-tone color with warm amber and
dusty-teal contrast, wide 16:9 letterboxed composition, no text"]**

of Alexandria — what's solid, what historians still argue about,

**[ON SCREEN: AI-generate: "Painted scene mode, a faint translucent ghostly
silhouette of the robed caliph figure fading at the edge of frame while the
solid, clearly rendered Library of Alexandria reading hall occupies the rest of
the composition, flat cream-faced stick-limbed characters, clean confident
linework on the real scene, muted earth-tone palette, wide 16:9 letterboxed
composition, no text"]**

and the one popular version that's almost certainly a myth.

**[ON SCREEN: AI-generate: "Painted scene mode, a sunlit Ptolemaic-Egyptian
courtyard with the Mouseion's columned facade in the background, flat
cream-faced stick-limbed scholars walking toward the entrance in
Hellenistic-Egyptian dress, clean confident linework, full muted earth-tone
color (tan stone, dusty teal sky), wide 16:9 letterboxed composition, no
text"]**

**BEAT 1 — The founding (SOLID):** The Library was part of the Mouseion, a research

**[ON SCREEN: AI-generate: "Painted scene mode, the Mouseion's interior research
hall, flat cream-faced stick-limbed scholars and scribes working at reading
tables, Hellenistic columns fused with Egyptian architectural motifs, clean
confident linework, full muted earth-tone color with warm amber light, wide
16:9 letterboxed composition, no text"]**

institution founded in the early Ptolemaic dynasty, in Egypt.

**[ON SCREEN: AI-generate: "Painted scene mode, Demetrius of Phalerum walking
toward a sunlit Alexandrian royal courtroom carrying a scroll, flat cream-faced
stick-limbed character, CONTESTED treatment: sketchier looser line weight,
desaturated muted palette, a faint dashed-line border motif worked into the
scene's framing, wide 16:9 letterboxed composition, no text"]**

Tradition credits Demetrius of Phalerum with proposing it to

**[ON SCREEN: AI-generate: "Painted scene mode, Demetrius of Phalerum presenting
a scroll to Ptolemy I seated on a modest throne in the same sunlit Alexandrian
courtroom, flat cream-faced stick-limbed characters, CONTESTED treatment:
sketchier looser line weight, desaturated muted palette, a faint dashed-line
border motif worked into the scene's framing, wide 16:9 letterboxed
composition, no text"]**

Ptolemy I — though some historians call his exact role

**[ON SCREEN: AI-generate: "Painted scene mode, the same royal courtroom scene
with Demetrius and Ptolemy I, now rendered with visibly looser sketchier
linework fading into a dashed outline at the composition's edges, desaturated
muted palette, flat cream-faced stick-limbed characters, signaling historical
uncertainty, wide 16:9 letterboxed composition, no text"]**

debatable, so treat that detail as likely, not certain.

**[ON SCREEN: AI-generate: "Flat explainer mode, a stylized library-shelf diagram
with rows of scroll cubbies fading into a soft hazy question-mark silhouette at the
far end, clean confident line weight, muted dusty-teal neutral informational
backdrop, small hand-drawn-caps diagram label reading SCROLL COUNT: UNKNOWN, wide
16:9 letterboxed composition"]**

**BEAT 2 — How big was it, really (SOLID, with a caveat):** Nobody knows exactly how
many scrolls it held.

**[ON SCREEN: AI-generate: "Flat explainer mode, a single absurdly tall and
precarious stack of ancient scrolls towering off the top of the frame, leaning
slightly as if about to topple, a small flat cream-faced stick-limbed scholar
character at the base looking up at it for scale, clean confident line weight,
pale neutral background with muted dusty-teal accents, small hand-drawn-caps
diagram label near the base reading 700,000?, wide 16:9 letterboxed
composition"]**

Estimates range from 40,000 to as high as 700,000 —

**[ON SCREEN: AI-generate: "Flat explainer mode, a closer zoomed-in view on a
single old worn scroll partway up a tall precarious stack of ancient scrolls, a
small stylized ancient scribe-and-ink-pot icon beside it, a red hand-drawn
annotation arrow pointing at the worn scroll, clean confident line weight,
pale neutral background with muted dusty-teal accents, small hand-drawn-caps
diagram label reading ANCIENT SOURCE, wide 16:9 letterboxed composition"]**

but that top figure comes from ancient writers centuries

**[ON SCREEN: AI-generate: "Flat explainer mode, the same tall precarious stack
of ancient scrolls, but the top portion of the stack is now redrawn with a
sketchy wobbly dashed outline instead of a firm line, suggesting it might not
really be that tall, pale neutral background with muted dusty-teal accents,
small hand-drawn-caps diagram label near the top reading EXAGGERATED?, wide
16:9 letterboxed composition"]**

later, and modern historians consider it almost certainly exaggerated.
