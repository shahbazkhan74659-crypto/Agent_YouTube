# Research Findings

Research only — nothing acted on. Covers (1) an evaluation of the source PDF's claims, and
(2) niche research for the science/history/philosophy pivot.

## 1. Evaluating `EARN-System-by-siddhantt.ai.pdf`

- It's a lead-magnet PDF that repeatedly pushes a paid "Motion Graphics Toolkit" upsell
  (pages 1, 7, 9). Treat it as marketing-with-useful-content, not a neutral guide.
- The $28K/28-days and 2M-views/2-days figures are disclosed as best-case/not-typical
  results — good that they said so, but still the hook.
- **Technically legit parts:** Wan2GP (github.com/deepbeepmeep/Wan2GP) is a real,
  free, open-source local video tool. The Claude Code motion-graphics workflow (script →
  voice → word-synced text → described animation → render) is a sound, real workflow.
  YouTube Partner Program thresholds as stated (1,000 subs + 4,000 watch hrs/12mo OR 10M
  Shorts views/90 days) were accurate at time of writing.
- **What it leaves out / undersells:**
  - YouTube's **"inauthentic content" policy** (renamed from "repetitious content" in
    July 2025, clarified further in July 2026) specifically targets mass-produced,
    repetitive AI-generated videos — exactly the autopilot cartoon-character model the
    PDF's Path 1 describes (same character, templated 8-second clips, daily posting).
    Channels doing this at scale have been demonetized/removed.
  - Shorts monetization bar is rising: reports point to the threshold increasing from
    10M to 20M views/90 days for new applicants starting Feb 2027 (unverified against
    YouTube's own announcement — only seen in secondary sources).
  - GPU rendering cost (hourly rental or local hardware) isn't priced into the "to
    start: $0" pitch.
  - ₹15,000–₹50,000 motion-graphics client pricing is anecdotal, not a guaranteed
    market rate.

## 2. Why the pivot (2 videos/day, sci/history/philosophy) is a real improvement

### RPM / monetization data favors this niche
- A 2026 dataset of 300 channels (AIR Media-Tech) found **Education & Science is the
  highest-paying YouTube niche**: median RPM **$10.22**, vs. Entertainment's **$2.43**.
  Education also runs ads on 77% of views vs. 55% for Entertainment.
- History wasn't in that dataset; a lower-confidence estimate puts it around $5–12 RPM —
  still well above general entertainment/kids content.
- No Shorts-specific RPM figures were found for these niches (only long-form data) — a
  real gap to watch for.

### This format sidesteps the "inauthentic content" risk
- The inauthentic-content policy targets *repetitive, templated* AI content — same
  character/format, churned daily. Two videos a day on distinct scientific, historical,
  and philosophical topics, each with its own script and visuals, is structurally the
  opposite pattern. Not immune to scrutiny, but not the target case.

### AI disclosure labels appear reach/monetization-neutral
- YouTube's "altered or synthetic content" disclosure (auto-detection rolling out since
  May 2026) is reported by YouTube as not affecting recommendations or monetization.
  Stylized/animated AI content (not photorealistic) typically only gets a line in the
  expanded description, not a prominent overlay.
- The real monetization risk remains the separate inauthentic-content bucket
  (repetition / manipulation / sensitive-topic synthetic personas), not AI disclosure
  itself.

### Where this niche is harder than the original cartoon-channel pitch
- Factual accuracy matters much more — history/philosophy are contested territory;
  a wrong claim or a one-sided framing draws pushback fast. Needs a
  verification/sourcing step if scripts are AI-drafted, not just "ask and post."
- Competition is entrenched (Kurzgesagt, Eons, established philosophy explainer
  channels) — differentiation in angle/voice/visual style matters more than volume.

## 3. Free/cheap tooling research (TTS, visuals, thumbnails)

Research only — nothing installed/tested on this machine yet. Goal: find free-first
alternatives per the budget decision (Claude usage + ElevenLabs are the only accepted
must-spend items; everything else free-first).

### TTS alternatives to ElevenLabs

- **Edge-TTS** (`pip install edge-tts`) — wraps Microsoft Edge's online "Read Aloud"
  voice service. Free, no API key. Community wrappers (e.g. `easy-edge-tts`) add
  word-level timestamps, which is exactly what's needed for word-synced captions.
  Caveat: requires internet, no official usage quota stated (it's a reverse-engineered
  endpoint, so it could throttle/break without notice) — not something to build a
  daily-upload pipeline on without a fallback.
- **Kokoro** (82M params, Apache 2.0, open weights) — runs fully **locally on CPU**,
  no GPU needed. Reported RAM floor: 4GB min / 8GB recommended — right at the edge of
  this machine's 8GB, workable but tight. Deployment via Kokoro-FastAPI container is
  ~5GB, worth checking against the 161GB free disk space. Quality is reported as strong
  for its size, but no benchmark found for a CPU this weak (Ryzen 3 5425U) — needs a
  hands-on test, not just a spec-sheet read.
- **Piper** (open source, used by apps like SUZA Voice Studio) — another CPU-local
  option, lighter-weight than Kokoro, less discussed for quality.
- **Chatterbox** (Resemble AI, MIT license) — vendor claims it's competitive with
  ElevenLabs in blind tests; unverified independently.
- Note: ElevenLabs itself reportedly cut self-serve API pricing up to 55% around
  May 2026 — worth re-checking current ElevenLabs pricing before assuming it's
  expensive, in case "cheaper tier" beats "switch tools."

**Recommendation to test first:** Kokoro (fully offline, no quota risk) as primary,
Edge-TTS as a free cloud backup — both free, so no cost decision is actually needed
here, just a quality/speed test on this specific laptop.

**Tested on this machine (2026-10-24), `kokoro-onnx` 0.6.1, int8 model (92MB) + voices
(28MB), CPU-only, no GPU:**
- Model load: ~2.7s.
- A 38-word test sentence (14.4s of audio) generated in 15.1s → **real-time factor
  ≈1.05 (0.95x real-time)**. Workable for 1 video/day — a 5-minute voiceover takes
  roughly 5 minutes to synthesize, no GPU needed.
- `Kokoro.create_timed()` (the library's built-in word/phoneme-timing API) **returned
  empty timings on both the int8 and full fp32 (325MB) models** — this is a limitation
  of `kokoro-onnx` 0.6.1 itself, not the quantization. **Kokoro cannot be relied on for
  word-synced caption timing out of the box.**
- Workaround needed: generate audio with Kokoro, then run a separate forced-alignment
  pass (e.g. free/local `faster-whisper` transcribing the generated WAV back to get
  word timestamps) to recover word-sync data. This approach works regardless of which
  TTS engine is used, so it's worth building once and reusing. Not yet tested on this
  machine.
- Output written to `C:\Idea\kokoro-test\test_output.wav` for a manual listen —
  quality not yet human-verified.

**Forced-alignment workaround tested (2026-10-24), `faster-whisper` 1.2.1,
`base.en` model, CPU-only, int8 compute:**
- Full pipeline on a 50-word/21.8s test clip: Kokoro TTS generation 17.24s (RTF 0.79)
  + Whisper word-alignment 4.05s (RTF 0.19) = **~21s of compute for ~22s of audio,
  essentially real-time**, excluding one-time setup.
- Whisper model load: 37.5s on first run (one-time download+cache), **1.67s on every
  run after** since it's cached locally — negligible per-video overhead going forward.
- **Accuracy: 50/50 words aligned**, timestamps looked clean and plausible against the
  source text (spot-checked by eye, not by ear yet).
- **Verdict: the free pipeline works.** Kokoro (TTS) → `faster-whisper` `base.en`
  (word-level forced alignment) → word timestamps for kinetic-text sync, all local,
  all CPU-only, no paid service required. This resolves the open "Kokoro has no
  reliable built-in timestamps" gap found above.
- Test files: `C:\Idea\kokoro-test\test_alignment.py`,
  `C:\Idea\kokoro-test\alignment_test.wav`.
- Not yet verified: audio actually listened to for voice-quality judgment; behavior
  on longer (multi-minute) scripts with varied punctuation/numbers; whether `base.en`
  is the right size/accuracy tradeoff vs. `small.en`/`tiny.en`.

**Hindi TTS test (2026-10-24):** Kokoro ships 4 generic Hindi voices (`hf_alpha`,
`hf_beta` female; `hm_omega`, `hm_psi` male — not modeled on any real person). A short
Hindi sentence generated in 3.78s for 3.84s of audio (near real-time, same CPU-only
setup). Output: `C:\Idea\kokoro-test\hindi_test.wav`, quality not yet human-verified.
**Declined:** cloning a specific real public figure's voice (was asked to attempt
Sanjay Dutt's voice) — not attempted, on personality-rights/synthetic-persona
grounds, and Kokoro has no voice-cloning-from-reference capability regardless (fixed
preset voices only).

### Free image/video sourcing

- **Pexels, Pixabay, Mixkit** — consistently the top-recommended free stock
  video/image sites, HD/4K, no attribution required on Pexels/Pixabay. Generic
  B-roll only (people, nature, city) — won't cover science/history/philosophy-specific
  visuals (artifacts, diagrams, historical figures).
- **Wikimedia Commons, NASA (on Commons/Flickr), Smithsonian Open Access** — the
  actually-relevant sources for this niche. NASA's own material is public domain
  unless noted (NASA logos, and Hubble/SOHO/APOD imagery specifically, can carry
  separate copyright — check per image). Smithsonian Open Access license terms
  weren't confirmed in this pass — verify per-collection before use. These are the
  best fit for historical portraits, scientific diagrams, and artifacts that generic
  stock sites won't have.
- **Caveat found across sources:** "free" stock sites sometimes watermark the actual
  download while showing a clean preview, and some clips require attribution even on
  otherwise-free sites — check each asset's specific license, not just the site's
  general policy.

### Free AI image generation (for gaps stock/archives don't cover)

- **Google Gemini / "Nano Banana 2"** — top pick found: ~100 images/day free via the
  Gemini app, or ~500/day via Google AI Studio, no watermark, no card required, native
  4K. Best free ceiling found, but daily-capped, not unlimited — fine for 1 video/day.
- **Getimg.ai** — 40 free credits/day, no card required.
- No source confirmed a truly free *and* unlimited *and* watermark-free generator —
  all free tiers found are credit/daily-capped. For 1 video/day this is almost
  certainly enough; would need to re-check if cadence later increases.

### Free thumbnail tools

- **Photopea** — free, browser-based, Photoshop-equivalent feature set. No install.
- **GIMP** — free, open source, offline desktop editor — fits the "no cloud
  dependency" storage preference better than a browser tool.
- **Canva Free** (not Pro) — confirmed as fallback per the budget decision; freemium,
  template-driven, fastest for simple thumbnail layouts if Photopea/GIMP prove too
  slow for daily use.
- Dedicated "AI thumbnail maker" tools (Pikzels, ThumbGenix, etc.) found in search were
  mostly vendor listings with unclear/no free tier details — not verified enough to
  recommend over Photopea/GIMP/Canva Free.

**Recommendation:** GIMP or Photopea as the default (both genuinely free, no caps);
Canva Free only if daily thumbnail turnaround with GIMP/Photopea proves too slow.

### Hands-on test (2026-10-24)

- **Photopea — confirmed working end to end.** No signup, loads a full
  Photoshop-equivalent editor directly in-browser. Claims to be fully client-side
  ("no uploads... never leave your device"), which fits the no-cloud-storage
  preference. Built a real 1280x720 YouTube-thumbnail-preset canvas, added an
  editable text layer ("MYTH BUSTED," auto-named from its content, matching
  `yt-package`'s "3 words maximum" rule), exported as PNG via File > Export As, and
  the file landed in `Downloads\New Project.png` (4,527 bytes, matching the export
  dialog's live preview exactly). One caveat: the free version shows rotating ad
  banners (GoDaddy, crypto trading, etc.) in the side panel — not a functional
  limitation, just a visual nuisance during editing.
- **GIMP — installed successfully.** The unattended `winget install` failed because
  GIMP's installer requires Windows admin elevation (UAC), which runs on a secure
  desktop nothing can automate past. The user re-ran it from an elevated
  (administrator) terminal and approved it manually — a one-time, ~2-minute step.
  Confirmed installed: GIMP 3.2.6 at
  `C:\Users\shahb\AppData\Local\Programs\GIMP 3\bin\gimp.exe`, with its own bundled
  Python interpreter (`bin\python.exe`) — useful later for scripting batch
  thumbnail generation via GIMP's Script-Fu/Python-Fu instead of manual clicking,
  if daily thumbnail volume ever makes that worth building.
- **Verdict:** both options are now live. Photopea (no install, works in-browser,
  ads in the free tier) and GIMP (fully offline, no ads, scriptable) are both
  genuinely free and confirmed working — pick per-video based on whether
  browser-based or fully-offline editing is preferred that day.

### Visuals pipeline — hands-on test (2026-10-24)

Tested the two sources that need **no account/API key at all** — both confirmed
working end to end (search → license check → full-res download), from
`C:\Idea\visuals-test\`:

- **Wikimedia Commons API** — `action=query&list=search` finds files, then
  `prop=imageinfo&iiprop=url|extmetadata` returns the download URL *and* license
  metadata (`LicenseShortName`, `Artist`, `UsageTerms`) in the same call. This means
  a script can auto-filter to only public-domain/CC results before downloading
  anything — no manual license-checking needed. Test: searched "Library of
  Alexandria," confirmed a result as "Public domain," downloaded it
  (`alexandria_library.jpg`, 1072×1090).
- **NASA Images API** (`images-api.nasa.gov`) — no key needed. Search returns
  thumbnail/medium links; the `/asset/<nasa_id>` endpoint gives the original
  full-resolution URL (`~orig.jpg`). NASA's own imagery is public domain by default
  (exceptions: NASA logos, non-US-agency imagery, some Hubble/SOHO/APOD items — check
  per image). Test: searched "Hubble nebula," downloaded
  `nebula_orig.jpg` at 1280×1231.
- **Not yet tested — all require the user to create a free account first (can't be
  done on their behalf):**
  - **Pexels / Pixabay** — free API key via account signup; generic B-roll, not
    niche-specific.
  - **Google Gemini ("Nano Banana 2")** — free API key via Google AI Studio; needed
    for custom AI-generated visuals stock/archives don't cover.
  - **Smithsonian Open Access** — free API key via api.data.gov.

**Verdict so far:** Wikimedia Commons + NASA alone already cover a meaningful chunk
of the science/history niche (diagrams, historical figures/art, space imagery) with
zero signup and zero cost. Pexels/Pixabay/Gemini would add generic B-roll and custom
AI generation on top, but need the user to grab free keys first.

### Key signup follow-up (2026-10-24) — corrects the free-tier assumptions above

- **Pexels: API key issuance is currently paused site-wide.** Account exists, but
  the API page itself says "New API key issuance is currently paused and cannot be
  requested." Not fixable on our end — this source is unavailable for now,
  independent of account status.
- **Pixabay: working.** Key retrieved from the account's API docs page (shown inline
  once logged in — not emailed). Validated live: searched "nebula," got 500 results
  with usable image URLs.
- **api.data.gov: working.** Key arrives by email (can take a few minutes, check
  spam). Validated against NASA's APOD endpoint.
- **Gemini (Google AI Studio): key valid, but free image generation is NOT actually
  reachable via the API right now — corrects the earlier research.** Tested both
  `gemini-3.1-flash-image` (Nano Banana 2) and `gemini-2.5-flash-image` (Nano Banana):
  both return `429 quota exceeded`, with the free-tier limit explicitly listed as
  **0** requests for image generation specifically. Isolated the cause: plain text
  generation (`gemini-3.8-flash`) on the *same key* works fine on the free tier, so
  this isn't an account-wide billing block — it's specific to image-generation
  models. The "~100–500 free images/day" figure from the earlier web search appears
  to be outdated or app-only (e.g. gemini.google.com consumer UI), not available
  through the API as tested. **Gemini AI image generation is off the table for this
  project unless billing is enabled on the Google Cloud project**, which reopens the
  cost-item conversation for custom AI visuals.

**Updated net picture:** Of the four sources chased, **2 of 4 are usable for free
right now (Pixabay, api.data.gov/Smithsonian+NASA)**, 1 is blocked at the platform
level (Pexels, paused issuance), and 1 requires paid billing despite being marketed
as free (Gemini image gen). Combined with Wikimedia Commons + NASA's own keyless
API, the actually-free visual pipeline today is: **Wikimedia Commons, NASA, Pixabay,
Smithsonian** — all license-checkable, all free, all tested working. Custom AI-
generated visuals (for gaps those four don't cover) remains unresolved — either find
another free zero-shot image generator, or accept it as a small paid line item.

## Sources

- [YouTube RPM by niche 2026 — AIR Media-Tech](https://air.io/en/air-data-findings/which-youtube-niche-makes-the-most-money-in-2026-ranked-by-real-rpm-and-cpm)
- [YouTube Shorts RPM niche-by-niche — AIR Media-Tech](https://air.io/air-data-findings/what-is-youtube-shorts-rpm-in-your-niche-in-2026)
- [YouTube AI content disclosure policy — AIR Media-Tech](https://air.io/en/youtube-glossary/what-is-youtubes-ai-content-disclosure-policy)
- [YouTube will try to automatically flag AI videos — The Decoder](https://the-decoder.com/youtube-will-try-to-automatically-flag-ai-videos-starting-this-month/)
- [What Qualifies as Inauthentic Content on YouTube — gofaceless.ai](https://www.gofaceless.ai/blog/what-qualifies-as-inauthentic-content-on-youtube)
- [YouTube Partner Program Requirements 2026 — AIR Media-Tech](https://air.io/en/monetization/youtube-partner-program-requirements-2026-the-complete-guide)
- [YouTube Shorts Monetization in 2026 — vidIQ](https://vidiq.com/blog/post/youtube-shorts-monetization/)
- [YouTube raises monetisation bar, tightens Shorts eligibility — DropMedia](https://www.dropmedia.co.uk/?p=8396)
- [YouTube clarifies policies around AI slop — TechCrunch](https://techcrunch.com/2026/07/20/youtube-clarifies-policies-around-ai-slop-and-upsetting-videos/)
- [YouTube monetization rules on AI slop / inauthentic content — Android Headlines](https://www.androidheadlines.com/2026/07/youtube-monetization-rules-ai-slop-inauthentic-content.html)
- [YouTube AI slop crackdown 2026 — logie.ai](https://logie.ai/news/youtube-ai-slop-crackdown-2026-monetization/)
- [Kokoro vs ElevenLabs — PromptQuorum](https://www.promptquorum.com/power-local-llm/kokoro-vs-elevenlabs)
- [Local, CPU-Friendly, High-Quality TTS with Kokoro — ariya.io](https://ariya.io/2026/03/local-cpu-friendly-high-quality-tts-text-to-speech-with-kokoro)
- [Kokoro TTS Requirements — aquarion-libtts docs](https://aquarion-libtts.readthedocs.io/en/stable/requirements/kokoro.html)
- [edge-tts — PyPI](https://pypi.org/project/edge-tts)
- [Best free stock video sites — TechRadar](https://www.techradar.com/news/the-best-free-stock-video-sites)
- [The 12 Best Stock Video Websites in 2026 — PhotoWorkout](https://www.photoworkout.com/selling-videos/)
- [AI Image Generator for Free: Best Tools 2026 — aitoolmapper](https://aitoolmapper.substack.com/p/ai-image-generator-for-best)
- [Free AI YouTube Thumbnail Generator — Piktochart](https://piktochart.com/ai-youtube-thumbnail-generator)
- [getimg.ai YouTube Thumbnail Maker](https://getimg.ai/use-cases/youtube-thumbnail-maker)
- [Canva alternatives — 1of10](https://1of10.com/compare/canva-alternatives)
- [Images, Video, and Audio Resources on the Web — UVM Libraries](https://www.uvm.edu/ctl/images-on-the-web/)
