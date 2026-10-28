"""Shared paths, constants, and settings for the render pipeline."""

import os
import re
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
VIDEOS_DIR = PROJECT_ROOT / "videos"
BRANDING_DIR = PROJECT_ROOT / "branding"
CHARACTER_DIR = BRANDING_DIR / "character"
ASSETS_AUDIO_DIR = PROJECT_ROOT / "Assets_audio"
MUSIC_CATALOG = ASSETS_AUDIO_DIR / "metadata" / "music_catalog.csv"
SFX_CATALOG = ASSETS_AUDIO_DIR / "metadata" / "sfx_catalog.csv"
VOICE_MD = PROJECT_ROOT / "voice.md"

KOKORO_MODEL_PATH = PROJECT_ROOT / "kokoro-test" / "kokoro-v1.0.int8.onnx"
KOKORO_VOICES_PATH = PROJECT_ROOT / "kokoro-test" / "voices-v1.0.bin"

load_dotenv(PROJECT_ROOT / ".env")
PIXABAY_API_KEY = os.environ.get("PIXABAY_API_KEY", "")
API_DATA_GOV_KEY = os.environ.get("API_DATA_GOV_KEY", "")

# Video output
WIDTH = 1080
HEIGHT = 1920
FPS = 30
MAX_DURATION_SEC = 180  # YouTube Shorts ceiling

# Branded frame template (same on every video): black canvas, title band near the
# top, segment visuals confined to a full-width letterboxed rectangle, captions in
# the bottom band. Layout derived from a reference image showing a full-width
# 16:9 content band (738x416, aspect 1.774 ≈ 16:9) with symmetric black margins
# top/bottom. Scaled onto our 1080-wide canvas at the band's own 16:9 aspect (not
# by literally copying the reference's margin fractions, which belong to a
# differently-shaped 738x1600 source image): 1080 wide x 608 tall (1080*9/16=607.5,
# rounded to the even 608 so the vertical split below is exactly symmetric).
# Centered vertically: 656 (title band) + 608 (content) + 656 (bottom bar) = 1920.
SQUARE_WIDTH = 1080
SQUARE_HEIGHT = 608
SQUARE_X = (WIDTH - SQUARE_WIDTH) // 2  # 0 - box now spans the full canvas width
SQUARE_Y = (HEIGHT - SQUARE_HEIGHT) // 2  # 656 - vertically centered, symmetric bands

# Host character (branding/character/<pose>.png, generated once by
# tools/generate_character_poses.py, reused across every video like Assets_audio).
# Single pose only for now - Sana (Pollinations' only free model) couldn't reliably
# render distinct arm/hand gestures after 2 tries (live-tested: "pointing" came out
# as a vague blob both times), only the one consistent standing silhouette. Position
# still cycles per segment, which is the actual source of on-screen movement.
SHOW_CHARACTER = False  # off for now - user asked to drop the overlay; flip back to re-enable
CHARACTER_POSES = ("neutral",)
CHARACTER_HEIGHT = 365  # ~60% of SQUARE_HEIGHT (608) - same ratio the old 520/880 used, rebased to the new height axis
CHARACTER_EST_WIDTH = 243  # nominal estimate for positioning math; derived from the character render's fixed 600x900 aspect at CHARACTER_HEIGHT (365 * 600/900)
CHARACTER_Y = SQUARE_Y + SQUARE_HEIGHT - CHARACTER_HEIGHT  # feet rest on the box's bottom edge

# 4 position anchors to cycle through per segment - alternating left/right. The box
# now spans the full canvas width (SQUARE_X=0), so there's no outer margin left to
# overflow into like the old centered-square layout had; these anchors stay fully
# on-canvas instead (two well inside, two near the edge).
CHARACTER_POSITIONS = (
    SQUARE_X + 40,  # left, well inside
    SQUARE_X + 10,  # left, near the edge
    SQUARE_X + SQUARE_WIDTH - CHARACTER_EST_WIDTH - 40,  # right, well inside
    SQUARE_X + SQUARE_WIDTH - CHARACTER_EST_WIDTH - 10,  # right, near the edge
)

# Evidence inset (2026-10-27 visual-sourcing flip) - a smaller bordered image shown
# over the primary AI-generated visual, labeled SOURCE, for exactly one segment at a
# time. Carries the real Wikimedia/NASA/Pixabay/Smithsonian/screenshot proof now that
# those sources no longer fill the full content square - see idea.md.
EVIDENCE_INSET_SIZE = 280  # ~46% of SQUARE_HEIGHT / ~26% of SQUARE_WIDTH - readable as proof, clearly secondary
EVIDENCE_BORDER_PX = 6
EVIDENCE_BORDER_COLOR = "white"
EVIDENCE_LABEL_TEXT = "SOURCE"

_EV_MARGIN = 24  # with SQUARE_X=0 this is now the only padding against the true canvas
# edge (was SQUARE_X(100)+24=124px before) - bump if it reads as too tight by eye.
# 4 corners + center, same cycling-anchor style as CHARACTER_POSITIONS above -
# evidence.position_for_segment() picks one of these per segment (seeded, not truly
# random, so re-renders stay reproducible).
EVIDENCE_POSITIONS = (
    (SQUARE_X + _EV_MARGIN, SQUARE_Y + _EV_MARGIN),  # top-left
    (SQUARE_X + SQUARE_WIDTH - EVIDENCE_INSET_SIZE - _EV_MARGIN, SQUARE_Y + _EV_MARGIN),  # top-right
    (SQUARE_X + _EV_MARGIN, SQUARE_Y + SQUARE_HEIGHT - EVIDENCE_INSET_SIZE - _EV_MARGIN),  # bottom-left
    (
        SQUARE_X + SQUARE_WIDTH - EVIDENCE_INSET_SIZE - _EV_MARGIN,
        SQUARE_Y + SQUARE_HEIGHT - EVIDENCE_INSET_SIZE - _EV_MARGIN,
    ),  # bottom-right
    (
        SQUARE_X + (SQUARE_WIDTH - EVIDENCE_INSET_SIZE) // 2,
        SQUARE_Y + (SQUARE_HEIGHT - EVIDENCE_INSET_SIZE) // 2,
    ),  # center
)

# Live-session asset drop locations - populated manually by Claude during a session
# where the user has Chrome connected (Gemini generation, URL screenshots), never
# written by code. visuals/resolve.py checks these before falling back to Pollinations
# (primary) or skipping evidence entirely for that segment (evidence, fail-soft).
GEMINI_VISUALS_DIRNAME = "visuals_gemini"  # build/visuals_gemini/<seg_id>.*
EVIDENCE_DIRNAME = "evidence"  # build/evidence/<seg_id>.*

# Narration
PACING_WPM = 150
BEAT_GAP_SEC = 0.35  # silence between beats
KOKORO_SPEED = 1.0
DEFAULT_VOICE_PRESET = "af_heart"  # used only if voice.md hasn't locked one in yet

# Gemini watermark crop (2026-10-28, disabled 2026-10-28 same day) - Gemini's
# "Download full size" button bakes a small gray sparkle watermark into the
# bottom-right corner of every generated image (measured directly off real
# exports at 2752x1536: a ~95x95px mark sitting roughly 88-96% of the way
# down, fixed position regardless of content/background). Tried inpainting it
# out first - basic OpenCV inpainting (Telea/NS) leaves a visible blurry patch
# on anything but a flat background, often more noticeable than the mark
# itself on detailed/ornate images (see memory.md). Fixed upstream with a
# bottom-15% crop instead - worked, but cost real composition (the
# beat_04_seg01 "700,000?" diagram label landed in the cropped strip and had
# to be regenerated, see memory.md's 2026-10-28 entries). **Decided to stop
# cropping and show the watermark instead** - toggle, not delete, same
# pattern as SHOW_CHARACTER/ENABLE_MUSIC/ENABLE_SFX/ENABLE_KEN_BURNS.
# assemble.py's wm_crop filter stage still exists and still works if this is
# ever flipped back on. Tested asking Gemini to keep its own watermark small
# and cornered (a prompt instruction, not post-processing) - didn't work:
# the sparkle came back at its usual size/position, plus a new unwanted
# second mark (the model painted an actual signature monogram into the scene
# in response to the word "signature"). Standing rule per
# visual-style-brief.md: don't mention the watermark in prompts at all.
ENABLE_GEMINI_WATERMARK_CROP = False
GEMINI_WATERMARK_CROP_FRAC = 0.15  # crop the bottom 15%, keep the top 85% - only used if the flag above is re-enabled

# Ken Burns pan/zoom on still images - off by default as of 2026-10-28 (user asked
# to discard the moving-image effect; every still now holds fixed and fully visible,
# centered, no crop). Toggle, not delete - same pattern as SHOW_CHARACTER/
# ENABLE_MUSIC/ENABLE_SFX: assemble.py's zoompan code path still works if flipped
# back on, it's just unused by default.
ENABLE_KEN_BURNS = False

# Visual cut rate (2026-10-27) - no single resolved segment should display for
# longer than this. Measured from a reference video's actual scene cuts (ffmpeg
# scene-cut detection over its full runtime): median shot 3.03s, 78% of shots at
# 4s or under. narration.py warns (doesn't fail) when a segment exceeds this, as a
# build-time signal that a beat's [ON SCREEN: ...]/AI-generate: cues need to be
# placed more densely - see visual-style-brief.md's "Cut rate" section and
# yt-script/SKILL.md's cue-density rule.
MAX_SEGMENT_DURATION_SEC = 4.0

# Alignment
# Multilingual (not base.en) - this pipeline now also renders Hindi/Hinglish
# narration (lang="hi" below), same reasoning the global video-reader skill
# already uses: a multilingual model still handles English fine, an
# English-only one can't handle Hindi at all.
WHISPER_MODEL_SIZE = "base"
WHISPER_DEVICE = "cpu"
WHISPER_COMPUTE_TYPE = "int8"

# Visuals
POLLINATIONS_URL = "https://image.pollinations.ai/prompt/{prompt}"
ALLOWED_LICENSE_KEYWORDS = (
    "public domain",
    "cc0",
    "pd-old",
    "pdm",
    "cc-by",
    "cc by",
    "attribution",
)

# Audio mix
# Music + SFX dropped from production for now (2026-10-28 decision) - narration-only
# mix is the default. Toggle, not delete: Assets_audio/ (music_bollywood, sfx,
# metadata) and the genre-based music/ library stay on disk untouched, and
# audio_mix.py's music/SFX code paths still work if flipped back on later - same
# pattern as config.SHOW_CHARACTER.
ENABLE_MUSIC = False
ENABLE_SFX = False
MUSIC_BED_GAIN_DB = -20.0  # README mixing notes: -18 to -24 dB under narration
SFX_GAIN_DB = -6.0
SOLID_SFX_CANDIDATES = ("SFX_PH04_Realization", "SFX_KN04_Discovery_Chime")
UNCERTAIN_SFX_CANDIDATES = ("SFX_PH06_Unresolved_Thought", "SFX_MI07_Unanswered_Question")

# Bollywood-referenced emotion music library (2026-10-26 decision - replaces the
# genre-categorized Assets_audio/music/ library for actual production use; that
# older library is left on disk, untouched, just no longer selected by audio_mix.py.
# SFX stay on the old genre-based Assets_audio/sfx/ catalog - unaffected by this.
#
# "Bollywood-referenced" means original compositions that study Bollywood
# background-score conventions (instrumentation, scales, rhythmic feel) as a
# style reference - never sampled/derived from an actual copyrighted recording.
# See Assets_audio/music_bollywood/README.md.
MUSIC_BOLLYWOOD_DIR = ASSETS_AUDIO_DIR / "music_bollywood"
MUSIC_CATALOG_BOLLYWOOD = ASSETS_AUDIO_DIR / "metadata" / "music_catalog_bollywood.csv"

# Practical distillation of "any human emotion music can trigger" into a workable,
# extensible set (grounded in film-scoring mood-board practice and the GEMS-9
# music-emotion model) - not meant to be literally exhaustive. Adding a new one
# later is a one-folder + one-registry-entry change, not a redesign.
EMOTION_CATEGORIES = (
    "motivational", "mysterious", "cold", "cheerful", "epic", "tense", "dark",
    "melancholic", "romantic", "reflective", "hopeful", "nostalgic", "awe", "peaceful",
)
MUSIC_CROSSFADE_SEC = 1.5  # how long adjacent emotion beds overlap at a part boundary

_VOICE_LINE_RE = re.compile(
    r"Kokoro voice preset.*?\[CONFIRMED\].*?`([a-z]{2}_[a-z]+)`", re.IGNORECASE
)


def video_dir(slug: str) -> Path:
    return VIDEOS_DIR / slug


def build_dir(slug: str) -> Path:
    d = video_dir(slug) / "build"
    d.mkdir(parents=True, exist_ok=True)
    return d


def output_dir(slug: str) -> Path:
    d = video_dir(slug) / "output"
    d.mkdir(parents=True, exist_ok=True)
    return d


def get_voice_preset() -> str:
    """Read the locked-in Kokoro preset from voice.md, else fall back to the default."""
    if VOICE_MD.exists():
        match = _VOICE_LINE_RE.search(VOICE_MD.read_text(encoding="utf-8"))
        if match:
            return match.group(1)
    return DEFAULT_VOICE_PRESET
