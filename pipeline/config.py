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
# top, segment visuals confined to a centered square. Layout measured from a
# reference screenshot (495x703): title ~14-22% down, content square ~57% of
# height at ~82% of width, centered. Converted to clean numbers on our 1080x1920
# canvas: 560 (title band) + 880 (square) + 480 (bottom bar, also where captions
# now live) = 1920 exactly.
SQUARE_SIZE = 880
SQUARE_X = (WIDTH - SQUARE_SIZE) // 2  # 100
SQUARE_Y = 560

# Host character (branding/character/<pose>.png, generated once by
# tools/generate_character_poses.py, reused across every video like Assets_audio).
# Single pose only for now - Sana (Pollinations' only free model) couldn't reliably
# render distinct arm/hand gestures after 2 tries (live-tested: "pointing" came out
# as a vague blob both times), only the one consistent standing silhouette. Position
# still cycles per segment, which is the actual source of on-screen movement.
SHOW_CHARACTER = False  # off for now - user asked to drop the overlay; flip back to re-enable
CHARACTER_POSES = ("neutral",)
CHARACTER_HEIGHT = 520  # ~60% of SQUARE_SIZE - reads clearly without dominating the background
CHARACTER_EST_WIDTH = 350  # nominal estimate for positioning math; actual width varies slightly per pose
CHARACTER_Y = SQUARE_Y + SQUARE_SIZE - CHARACTER_HEIGHT  # feet rest on the square's bottom edge

# 4 position anchors to cycle through per segment - alternating left/right, two of
# them overflowing the square's horizontal edge slightly (the "moves across the
# square, can poke outside it a little" effect the user asked for).
CHARACTER_POSITIONS = (
    SQUARE_X + 40,  # left, inside the square
    SQUARE_X - 60,  # left, overflowing the square's left edge
    SQUARE_X + SQUARE_SIZE - CHARACTER_EST_WIDTH - 40,  # right, inside the square
    SQUARE_X + SQUARE_SIZE - CHARACTER_EST_WIDTH + 60,  # right, overflowing the square's right edge
)

# Narration
PACING_WPM = 150
BEAT_GAP_SEC = 0.35  # silence between beats
KOKORO_SPEED = 1.0
DEFAULT_VOICE_PRESET = "af_heart"  # used only if voice.md hasn't locked one in yet

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
