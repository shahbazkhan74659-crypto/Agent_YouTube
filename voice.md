# voice.md

Filled in from the decisions already made across `idea.md` and `research-findings.md`.
**Marked [CONFIRM] where it's a drafted default, not a settled fact** - everything
else follows directly from choices already locked in. Once reviewed, copy this to
`~/.claude/youtube/voice.md` - that's the path every skill in the pack actually reads
from.

## Who I am talking to

Someone who stopped scrolling because a thumbnail promised a real answer to a
history/science/philosophy question they didn't know they wanted answered - the
Kurzgesagt/Eons audience, but mid-scroll with up to 3 minutes (the Shorts format,
see "My format" below), not someone looking for personal drama or a creator's life
update.

## How I actually talk (narration tone) [CONFIRMED, revised 2026-10-27]

**Loud, confident, sarcastic, and disciplined.** Delivery is hyped and
unapologetically blunt - dark humor and sarcastic lore land mid-fact, the way
a narrator who's a little tired of the subject's own body count would say it,
not as a bit layered on top. "Disciplined" still does the same job it always
did: the edge is in *how* a true claim is delivered, never in what it claims -
sarcasm about a fact is not license to invent, exaggerate, or round up a
number the source doesn't support. Still treats "we don't actually know" as a
genuinely interesting beat, not a letdown to rush past. This still follows the
`yt-factcheck` discipline: loud and sarcastic tone, never hyped or invented
claims.

## Words I never use

Pulled directly from `hookscore.py`'s own VAGUE list (already validated inside this
toolchain, and consistent with the "never invent a number, a result or a source"
rule every skill shares): **amazing, incredible, insane, crazy, huge, massive,
game-changer, secret, powerful, ultimate, best, revolutionary, mind-blowing,
unbelievable.** Also generic channel filler: "unlock", "dive in", "let's get into
it", "welcome back". This list stays even with a hyped tone - "hyped" describes
delivery energy, not permission to reach for vague unsubstantiated superlatives;
that's exactly what "disciplined" in the tone above rules out - sarcastic
delivery included.

## Words I do use

Not yet known - these are a creator's real tics, and none exist yet since the channel
hasn't shipped a video. **Leave this blank until 3-5 real scripts exist, then fill it
in from what actually turns out to be true**, rather than invent phrases now that
won't actually match the finished narration.

## What I will not claim

- Any claim `yt-factcheck` marks UNCERTAIN, unless explicitly decided otherwise per
  video (already the default rule).
- Personal experience, opinion, or "I tried this" framing - this is narration, not a
  creator's first-person story. No claims of the form "I researched this" beyond what
  the visible sourcing shows.
- Any number, date, or figure not traceable to a line in that video's `research.md`.

## My format

- **Length [CONFIRMED]:** target YouTube Shorts' maximum length - **3 minutes**
  (extended from 60 seconds in October 2024; recheck YouTube's own Creator Help
  docs before relying on this if it's been a while, since the platform has changed
  this limit before). This locks the format to Shorts, not long-form: vertical or
  square framing is required for a video to actually count as a Short, not just
  short runtime - that applies to every visual sourced, not just the final export.
  The Library of Alexandria test script (~2:52) already fits inside this limit.
- **Opening:** no channel intro, no subscribe pitch before the hook - already
  enforced by `yt-script`'s "no channel intro... before we get started... those are
  the single most common cause of the 0:30 cliff" rule.
- **Kokoro voice preset [CONFIRMED]: `hf_alpha`, with `--lang en-us`** - promoted
  2026-10-27 to the channel-wide default for every video, superseding `af_bella`
  (reverted-to earlier the same day, never used in any actual render). `hf_alpha` is
  one of Kokoro's Hindi-trained voices (`h`-prefixed), not an English one - Kokoro has
  no dedicated Indian-English preset, so this deliberately feeds English text through
  a Hindi-trained voice under English phonemization (`lang="en-us"`, not `"hi"`) to get
  an "Indian tone" on English narration. Chosen after listening to 4 candidates
  (`hf_alpha`/`hf_beta`/`hm_omega`/`hm_psi`) generated to `C:\YouTube\voice-picker\`,
  first confirmed on the `library-of-alexandria-destruction-gemini-test` validation
  slug, now promoted to the global default read by `config.get_voice_preset()` for
  every render that doesn't pass an explicit `--voice` override. `af_bella`/
  `am_michael`/`af_heart` were all prior English-voice choices, now superseded. If
  genuinely Hindi-language narration (`--lang hi`) is ever produced, use `hm_omega`
  instead - it tested cleanest for actual Hindi (see `memory.md`'s 2026-10-26 entries) -
  `hf_alpha` here is specifically the English-with-Indian-tone pairing, not a Hindi
  voice pick.
- **Pacing:** 150 wpm baseline, matching `yt-script`'s own runtime-estimate math.
  Punctuation is part of pacing too - see `yt-script/SKILL.md`'s Punctuation
  section for the allowed `. , ! : ?` set and how each maps onto this voice's
  delivery beats.
- **Visual style mix [CONFIRMED, flipped 2026-10-27; style replaced 2026-10-27]:**
  AI-generated is primary on every segment - Gemini (live, via the Chrome
  browser extension, in a session manually started around 10 PM) first,
  Pollinations.ai (`AI-generate:` cues, free, keyless, already automatable) as
  the always-available fallback for whatever Gemini doesn't cover that
  session. Every `AI-generate:` prompt follows `C:\YouTube\visual-style-brief.md`
  - the flat-explainer/painted-scene illustrated style, replacing the old
  photoreal-documentary default - including its SOLID/CONTESTED/UNCERTAIN/myth
  treatment and its workflow/iteration-discipline rules. Wikimedia Commons /
  NASA / Pixabay / Smithsonian, plus live-captured Chrome screenshots, are
  demoted to evidence-only: a smaller bordered inset, labeled SOURCE, over the
  primary visual, for exactly one segment at a time, never the full content
  rectangle again - see `idea.md`'s "Visual sourcing priority flipped" entry and
  `pipeline/script_parser.py`'s `[EVIDENCE: ...]` cue.
- **Content structure: Storytelling → Explanation → Questionary.** Open with the
  narrative hook (storytelling), move through the claims at their actual confidence
  level (explanation - this is just the existing SOLID/CONTESTED/UNCERTAIN beats
  named as a stage), then close by delivering the hook's payoff *and* posing the
  genuinely unresolved question back to the viewer (questionary) - the open question
  comes after the payoff, never instead of it. Content stays agnostic and rational
  across perspectives rather than arguing one side, stays open to challenge rather
  than presenting itself as the final word, and treats incomplete knowledge as the
  normal state of a topic, not something to smooth over. Immediately after the
  closing question, the script ends on one sarcastic like/subscribe line - a
  punchline tied to that episode's content, never a generic pitch - see
  `yt-script/SKILL.md`'s "Questionary" section for the exact rule.

## Differentiation angle

The actual edge isn't visual style (stock/archival footage, same raw material
anyone can use) - it's **epistemic transparency as the format itself**: claims
visibly tagged by confidence, popular myths actively corrected rather than repeated
(the Caliph Omar legend in the Alexandria test script), and sourcing shown rather
than asserted. Most pop-science/history channels state things as settled fact for
narrative smoothness; this channel's narrative *is* showing what's actually solid
versus disputed versus legend. Harder to copy than a visual style, since it requires
the `yt-factcheck` pipeline behind it, not just a tone choice.
