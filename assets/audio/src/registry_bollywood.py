"""
Single source of truth for the Bollywood-referenced emotion music library
(Assets_audio/music_bollywood/) - mirrors registry.py's pattern exactly, keyed
by `emotion` instead of `category`/`genre`/`mood`. generate_bollywood.py,
metadata_gen_bollywood.py and validate_bollywood.py all read this module
instead of hardcoding asset lists, same as the genre library's trio does.
"""

from bollywood_music import (  # noqa: F401 - imported for when entries are added below
    motivational, mysterious, cold, cheerful, epic, tense, dark, melancholic,
    romantic, reflective, hopeful, nostalgic, awe, peaceful,
)


def _slug(title):
    return title.replace(",", "").replace("'", "").replace(" ", "_")


def _mus(id_, title, emotion, generator, purpose, mood, instrumentation, tonal_center, bpm, loop_dur, notes=""):
    slug = _slug(title)
    return {
        "id": id_, "type": "music", "title": title,
        "filename": f"{id_}_{slug}.wav", "emotion": emotion, "rel_dir": emotion,
        "generator": generator, "purpose": purpose, "mood": mood,
        "instrumentation": instrumentation, "tonal_center": tonal_center, "bpm": bpm,
        "loop_compatible": "yes (seamless)" if loop_dur else "no (one-shot)",
        "voiceover_suitability": "backing bed - duck under narration",
        "nominal_duration_sec": loop_dur, "notes": notes,
    }


# No tracks yet (2026-10-26) - infrastructure-only build, deliberately waiting on
# real Bollywood background-score reference material + a composition brief per
# emotion before writing any actual music (see
# Assets_audio/music_bollywood/README.md). Add entries here the same way
# registry.py's MUSIC list does once that exists, e.g.:
#
#   _mus("BOL_MOT01", "Example Title", "motivational",
#        motivational.make_bol_mot01_example,
#        "Triumphant beats, overcoming odds", "driving, uplifting, building",
#        "dholak + tanpura drone + string swell", "D Dorian", 100, 24.0),
MUSIC: list[dict] = []

ALL_ASSETS = MUSIC
