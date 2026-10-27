# Script: The Library of Alexandria — Gemini visuals validation test (first ~1 minute)

**Title:** The Destruction of the Library of Alexandria

**Status: VALIDATION TEST** — trimmed to the first 4 beats / 7 visual
segments of `videos/library-of-alexandria-destruction/script.md` (HOOK
through BEAT 2). **Reverted 2026-10-27** back to pure English narration —
the Hindi/Hinglish pilot from 2026-10-26 (see `memory.md`) is superseded,
not deleted. Read with an **"Indian tone"**: Kokoro has no dedicated
Indian-English voice, so this tests one of its Hindi-trained presets
speaking English text under `--lang en-us` instead of `hi` — untested before
this. 4 candidates were generated to `voice-picker/` for a listen
(`hf_alpha`/`hf_beta`/`hm_omega`/`hm_psi`); **`hf_alpha` confirmed 2026-10-27**
after listening, superseding the `hm_omega` placeholder used in the first
revert pass. Scoped to this test video only — the channel-wide production
preset in `voice.md` stays `af_bella`, untouched by this. The `build/romanized.json` positional-caption
workaround from the Hindi pilot no longer applies — moved aside
(`romanized_hindi_test.json.bak`) — captions now use the normal English
`reconcile_words()` text-matching path, which also restores digit-formatted
numbers in the subtitle (`40,000`, `700,000`, `three-hundred-year` →
`300-year`) instead of the Hinglish positional zip. The `[ON SCREEN: ...]`
cues below are kept verbatim from the original for reference only — this
render's actual visuals come from Gemini/Veo clips and images already
resolved into `build/manifest.json` (unchanged, since the beat/segment
structure is identical to the Hindi version it replaces).

## Script

**[ON SCREEN: Wikimedia Commons: "Library of Alexandria illustration" — the tested
public-domain O. Von Corven engraving, `alexandria_library.jpg`]**

**HOOK (0:00-0:15):** Before you believe the caliph burned the Library of Alexandria,
know the story has zero evidence from the century it happened in.

**[ON SCREEN: Wikimedia Commons: "ancient Alexandria fire illustration"]**

The real story isn't one fire — it's a three-hundred-year death with at least three
different suspects, and the most famous one probably never touched a single scroll.

**[ON SCREEN: Wikimedia Commons: "ancient Library of Alexandria depiction"]**

**THE TURN (0:15-0:30):** Today we're tracing what actually happened to the Library
of Alexandria — what's solid, what historians still argue about, and the one popular
version that's almost certainly a myth.

**[ON SCREEN: Wikimedia Commons: "Ptolemy I Soter bust" / "ancient Alexandria map"]**

**BEAT 1 — The founding (SOLID):** The Library was part of the Mouseion, a research
institution founded in the early Ptolemaic dynasty, in Egypt.

**[ON SCREEN: Wikimedia Commons: "Demetrius of Phalerum"]**

Tradition credits Demetrius of Phalerum with proposing it to Ptolemy I — though some
historians call his exact role debatable, so treat that detail as likely, not certain.

**[ON SCREEN: Wikimedia Commons: "ancient papyrus scroll"]**

**BEAT 2 — How big was it, really (SOLID, with a caveat):** Nobody knows exactly how
many scrolls it held.

**[ON SCREEN: Wikimedia Commons: "ancient library scrolls shelves"]**

Estimates range from 40,000 to as high as 700,000 — but that top figure comes from
ancient writers centuries later, and modern historians consider it almost certainly
exaggerated.
