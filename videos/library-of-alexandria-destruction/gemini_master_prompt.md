# Master prompt for Gemini — realistic 4K re-visualization

Paste everything below into Gemini (with `final.mp4` attached/uploaded). Goal:
same narration, same timing, same length — new visuals only, swapping the
current still-photo/Ken-Burns treatment for realistic 4K AI-generated video
per segment, to be composited back into the existing render pipeline.

**Read this first (not part of the prompt — context for you):** Veo (Gemini's
video model) can't lock itself to an external audio track sample-accurately,
and it generates clips in fixed durations (commonly ~8s per generation), not
arbitrary lengths like "11.51s." The realistic path is: Gemini writes one
Veo prompt per existing visual segment (below), you generate each clip near
its target length, and the clips drop into `pipeline/assemble.py`'s existing
per-segment compositing (which already trims every clip to its segment's
exact duration against the locked audio/caption timeline) — a small, separate
code change to accept a video clip instead of a still image as input, done
after you have the clips, not part of this prompt.

---

## PROMPT (copy from here down)

You are helping re-visualize an existing narrated video with new AI-generated
footage, keeping its audio, pacing, and structure completely unchanged.

**Context**: the attached `final.mp4` is a 158.8-second vertical (1080x1920)
YouTube Short titled "The Destruction of the Library of Alexandria," from an
educational channel whose format is: a recurring silhouetted host character
(long black coat, wide-brimmed fedora, fully black silhouette, no visible
face/features) stands in front of a changing background visual inside a
centered square frame, under a title band, with karaoke-style captions at the
bottom. The tone is measured, investigative, documentary-style narration —
not sensational. The channel's whole differentiation angle is **epistemic
honesty**: claims are visually/tonally distinguished by how certain they are.

**Your task**: watch `final.mp4` for overall pacing, visual rhythm, and the
existing branded-frame style (so your suggestions integrate with it, not
replace it wholesale), then write **one Veo video-generation prompt per
segment** listed below — 20 total — each describing realistic, cinematic,
photorealistic 4K footage (real-world documentary/archival-film quality, not
cartoon or illustration) that matches that segment's narration.

**Confidence-based visual treatment** — apply this consistently:
- Segments from a **SOLID**-tagged beat: straightforward photorealistic
  documentary/archival-film footage — treat it as established fact.
- Segments from a **CONTESTED** or **UNCERTAIN**-tagged beat: still
  photorealistic, but with a visible "this is reconstructed/uncertain" cue —
  slightly desaturated color, a faint grain/haze, or a soft dreamlike blur at
  the edges — so the visual itself signals lower certainty without the
  narration having to say so twice.
- Do **not** render any myth (e.g. the caliph-burns-the-library story) as if
  it visually happened — frame it as an illustrated/manuscript-style retelling
  of a legend, not a documentary reenactment of an event.

**Format for each of the 20 outputs**: segment ID, target duration, then the
Veo prompt itself (one dense paragraph: subject, setting, camera movement,
lighting, lens/film-stock feel, and the confidence-treatment cue above).

**Size/aspect ratio — read carefully:** each clip only fills the template's
centered **content square** — a 1:1 square (880x880px), *not* the full 9:16
video. The title band above it and the caption bar below it are a separate,
fixed part of the frame and are never covered by this footage. So: compose
and frame every clip for a **square (1:1)** result. If Veo doesn't offer a
1:1 aspect ratio directly, generate at its closest supported aspect ratio
instead (state which one) and frame the subject centered so the clip can be
center-cropped down to a clean 1:1 square afterward without losing the main
subject — tell me exactly how to do that crop for each clip if it isn't a
simple centered crop. Keep a consistent "look" across all 20 — same
grading/film-stock choice for every SOLID segment, same treatment for every
CONTESTED/UNCERTAIN one — so cutting between them doesn't feel like different
videos stitched together.

Here are the 20 segments, in order, each with its exact on-screen duration,
its narration text (write the Veo prompt to match this content, not the
current stock photo), its beat's confidence tag, and what's currently there
for reference only:

1. **beat_01_seg00** — 7.71s — [no tag, HOOK] — "Before you believe the
   caliph burned the Library of Alexandria, know the story has zero evidence
   from the century it happened in." — currently: Wikimedia engraving of the
   library burning.
2. **beat_01_seg01** — 9.81s — [no tag, HOOK] — "The real story isn't one
   fire — it's a three-hundred-year death with at least three different
   suspects, and the most famous one probably never touched a single scroll."
   — currently: Wikimedia public-domain illustration.
3. **beat_02_seg00** — 10.62s — [no tag, THE TURN] — "Today we're tracing
   what actually happened to the Library of Alexandria — what's solid, what
   historians still argue about, and the one popular version that's almost
   certainly a myth." — currently: mismatched stock photo (flagged separately
   as a bug, ignore it as reference).
4. **beat_03_seg00** — 7.40s — [SOLID] — "The Library was part of the
   Mouseion, a research institution founded in the early Ptolemaic dynasty,
   in Egypt." — currently: mismatched stock photo (same bug, ignore).
5. **beat_03_seg01** — 11.51s — [SOLID, with a caveat on Demetrius's role] —
   "Tradition credits Demetrius of Phalerum with proposing it to Ptolemy I —
   though some historians call his exact role debatable, so treat that detail
   as likely, not certain." — currently: unrelated Thessaloniki church photo
   (ignore).
6. **beat_04_seg00** — 3.46s — [SOLID, with a caveat] — "Nobody knows exactly
   how many scrolls it held." — currently: papyrus/hieroglyphs stock photo.
7. **beat_04_seg01** — 12.13s — [SOLID, with a caveat] — "Estimates range
   from 40,000 to as high as 700,000 — but that top figure comes from ancient
   writers centuries later, and modern historians consider it almost
   certainly exaggerated." — currently: library shelves stock photo.
8. **beat_05_seg00** — 6.22s — [CONTESTED] — "The most commonly blamed
   culprit. Caesar's own account only mentions burning ships and docks —" —
   currently: Julius Caesar bust photo.
9. **beat_05_seg01** — 6.63s — [CONTESTED] — "it's a later writer, Strabo,
   writing twenty-five years afterward, who connects the fire to the
   library." — currently: unrelated old-writing stock photo.
10. **beat_05_seg02** — 6.63s — [CONTESTED] — "Historians still dispute how
    much was actually lost, and there's evidence the library kept functioning
    afterward." — currently: Wikimedia photo of the Serapeum ruins.
11. **beat_06_seg00** — 9.59s — [SOLID temple destruction] — "In 391 CE, the
    Serapeum temple in Alexandria was destroyed under Bishop Theophilus —
    that part is well documented by near-contemporary writers." — currently:
    Wikimedia photo, Pompey's Pillar ruins.
12. **beat_06_seg01** — 8.28s — [UNCERTAIN library link] — "What's not
    documented: any ancient source actually connecting that destruction to a
    library collection still existing at the time." — currently: Machu Picchu
    photo (wrong continent, ignore — placeholder fallback).
13. **beat_06_seg02** — 6.10s — [UNCERTAIN library link] — "The two events
    get merged in popular retellings. The sources don't support that merge."
    — currently: AI-generated conceptual image.
14. **beat_07_seg00** — 7.94s — [UNCERTAIN — legend] — "The most famous
    version — a caliph ordering the library burned because its books were
    either redundant with or contrary to the Quran —" — currently:
    medieval-manuscript-style AI image.
15. **beat_07_seg01** — 4.96s — [UNCERTAIN — legend] — "traces to a single
    writer, Bar Hebraeus, writing roughly six hundred years after the fact."
    — currently: Wikimedia scribe illustration.
16. **beat_07_seg02** — 3.31s — [UNCERTAIN — legend] — "No source from the
    century it supposedly happened mentions it." — currently: Wikimedia
    archive-shelves photo.
17. **beat_07_seg03** — 9.60s — [UNCERTAIN — legend] — "And the same exact
    story gets told about a different library, under the same caliph,
    somewhere else entirely — a strong sign it's a reused legend, not a
    record." — currently: AI-generated mirrored-libraries image.
18. **beat_08_seg00** — 11.04s — [PAYOFF, synthesis] — "So the Library of
    Alexandria wasn't destroyed. It was worn down — a fire here, a purge
    there, a temple demolition that got conflated with it later, across three
    centuries —" — currently: Wikimedia ruins illustration.
19. **beat_08_seg01** — 6.77s — [PAYOFF, synthesis] — "and the single-villain
    version everyone repeats is the one part of the story with the least
    evidence behind it." — currently: Wikimedia lighthouse illustration.
20. **beat_09_seg00** — 5.95s — [CLOSE] — "Full source list and confidence
    ratings for every claim in this video are linked in the description." —
    currently: same lighthouse illustration (ending card).

Output all 20 as a numbered list in the format above, ready to paste
individually into Veo.

---

## After Gemini responds (not part of the prompt)

1. Generate each clip in Veo, closest to the target duration.
2. Save them somewhere like `videos/library-of-alexandria-destruction/build/visuals_v2/<segment_id>.mp4`.
3. Tell me and I'll adjust `pipeline/assemble.py`'s `_build_segment_clip()` to
   accept a video clip (trim/loop to the segment's exact duration, and
   scale/crop it to the 880x880 content square — `config.SQUARE_SIZE` — same
   as it already does for a still image) instead of requiring a still image,
   and re-run the assembly — audio, captions, and timing stay exactly as they
   are now.
