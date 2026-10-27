"""Builds one ASS subtitle file for the whole video from narration_meta.json's
per-beat word timestamps. One word on screen at a time, centered in the frame,
plain yellow, with a quick pop-in scale animation - only the word currently
being spoken is ever visible (no accumulating line, no karaoke highlight
progression across several words).

Each beat's words are already timestamped relative to that beat's own wav
(alignment.py ran faster-whisper per beat); this stage just adds each beat's
`start` offset once to land every word on the shared, final timeline.
"""

import argparse
import difflib
import json
import re

import pysubs2

import config
import evidence

WORD_FONT_SIZE = 70

TITLE_FONT_SIZE = 84
TITLE_MARGIN_V = 300  # from the top edge - positions a two-line title lower in the 560px band, closer to the square

# Quick scale-up "pop": starts at 60% size, overshoots to 115%, settles to 100% -
# all within the first 180ms of the word's own on-screen window. Runs the same
# way regardless of how long the word stays up; a very short word just gets cut
# off mid-settle, which still reads as a quick pop rather than a static word.
POP_TAG = r"\fscx60\fscy60\t(0,120,\fscx115\fscy115)\t(120,180,\fscx100\fscy100)"

_ONES = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
    "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19,
}
_TENS = {
    "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50,
    "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90,
}
_SCALES = {"hundred": 100, "thousand": 1000, "million": 1_000_000, "billion": 1_000_000_000}
_NUMBER_WORDS = {**_ONES, **_TENS, **_SCALES}

# Units/markers that, directly after a spelled-out number in the SAME hyphenated
# word (e.g. "three-hundred-year"), confirm it's a real year/date/measurement
# figure worth converting to digits - not every stray number word in natural
# speech ("the most famous one", "a single scroll").
_NUMBER_UNIT_SUFFIXES = {
    "year", "years", "yr", "yrs", "decade", "decades", "century", "centuries",
    "ce", "bce", "ad", "bc",
    "kg", "kilogram", "kilograms", "g", "gram", "grams",
    "km", "kilometer", "kilometers", "kilometre", "kilometres",
    "m", "meter", "meters", "metre", "metres",
    "cm", "centimeter", "centimeters", "centimetre", "centimetres",
    "mm", "millimeter", "millimeters",
    "lb", "lbs", "pound", "pounds", "ft", "foot", "feet",
    "in", "inch", "inches", "mi", "mile", "miles",
}

_NUMBER_TOKEN_RE = re.compile(r"^([A-Za-z]+(?:-[A-Za-z]+)*)(\W*)$")


def _words_to_int(words: list[str]) -> int | None:
    """Standard accumulate-and-scale number-word parser (e.g. ["three",
    "hundred"] -> 300). Returns None if any word isn't a recognized number word."""
    if not words or any(w not in _NUMBER_WORDS for w in words):
        return None
    result, current = 0, 0
    for w in words:
        val = _NUMBER_WORDS[w]
        if val == 100:
            current = (current or 1) * 100
        elif val >= 1000:
            current = (current or 1) * val
            result += current
            current = 0
        else:
            current += val
    return result + current


def _convert_number_token(token: str) -> str:
    """Spelled-out year/date/measurement compounds like 'three-hundred-year'
    display as '300-year' in the caption - the narration audio already said it
    naturally, this only changes what's burned into the subtitle. Only
    converts when a number-word run is immediately followed, in the SAME
    hyphenated token, by a recognized unit/year/date suffix - a bare number
    word with no such suffix (the pronoun "one" in "the most famous one", a
    plain count like "three different suspects") is left as text, since it
    isn't a year/date/figure."""
    m = _NUMBER_TOKEN_RE.match(token)
    if not m:
        return token
    core, trail = m.group(1), m.group(2)
    parts = core.split("-")
    lower_parts = [p.lower() for p in parts]

    n = 0
    for p in lower_parts:
        if p in _NUMBER_WORDS:
            n += 1
        else:
            break
    if n == 0 or n == len(parts):
        return token  # no number-word run, or no trailing suffix to check it against

    suffix = lower_parts[n]
    if suffix not in _NUMBER_UNIT_SUFFIXES:
        return token

    value = _words_to_int(lower_parts[:n])
    if value is None:
        return token
    digits = f"{value:,}" if value >= 1000 else str(value)
    suffix_parts = parts[n:]
    return digits + "-" + "-".join(suffix_parts) + trail


def _build_word_style() -> pysubs2.SSAStyle:
    style = pysubs2.SSAStyle()
    style.fontname = "Arial"
    style.fontsize = WORD_FONT_SIZE
    style.bold = True
    style.primarycolor = pysubs2.Color(255, 209, 0)  # every word, plain yellow/gold
    style.outlinecolor = pysubs2.Color(0, 0, 0)
    style.borderstyle = 1
    style.outline = 5
    style.shadow = 1
    style.alignment = 5  # middle-center - center of the full frame
    return style


def _build_title_style() -> pysubs2.SSAStyle:
    style = pysubs2.SSAStyle()
    style.fontname = "Arial"
    style.fontsize = TITLE_FONT_SIZE
    style.bold = True
    style.primarycolor = pysubs2.Color(255, 255, 255)  # white only, per the branded frame spec
    style.outlinecolor = pysubs2.Color(0, 0, 0)
    style.borderstyle = 1
    style.outline = 3
    style.shadow = 1
    style.alignment = 8  # top-center
    style.marginv = TITLE_MARGIN_V
    style.marginl = 60
    style.marginr = 60
    return style


def _build_evidence_label_style() -> pysubs2.SSAStyle:
    """The small "SOURCE" label burned over an evidence inset (see assemble.py's
    EVIDENCE_* compositing). Positioned per-event via \\pos() below, not a fixed
    alignment/margin - a label needs to land at whichever of the 5
    config.EVIDENCE_POSITIONS anchors evidence.position_for_segment() picked for
    that specific segment, which a single static alignment can't express."""
    style = pysubs2.SSAStyle()
    style.fontname = "Arial"
    style.fontsize = 28
    style.bold = True
    style.primarycolor = pysubs2.Color(255, 255, 255)
    style.outlinecolor = pysubs2.Color(0, 0, 0)
    style.borderstyle = 1
    style.outline = 2
    style.alignment = 7  # top-left anchor - \pos() below places it exactly, this just sets the anchor corner
    return style


def _normalize(token: str) -> str:
    return re.sub(r"[^a-z0-9]", "", token.lower())


def reconcile_words(original_text: str, whisper_words: list[dict]) -> list[dict]:
    """Burned captions should show the real script text, not whatever faster-whisper
    heard - live example: the script's "391 CE" came back from Whisper as "391c"
    (two words merged into one mis-transcribed token). Realigns the original
    script's words onto Whisper's timestamps via sequence matching; any block
    where the token counts don't match 1:1 has its time span divided evenly
    across the real words instead.
    """
    if not whisper_words:
        return []
    original_tokens = original_text.split()
    norm_orig = [_normalize(t) for t in original_tokens]
    norm_whisper = [_normalize(w["word"]) for w in whisper_words]

    matcher = difflib.SequenceMatcher(None, norm_whisper, norm_orig, autojunk=False)
    result = []
    last_end = whisper_words[0]["start"]

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        orig_slice = original_tokens[j1:j2]
        whisper_slice = whisper_words[i1:i2]
        if tag == "equal":
            for tok, w in zip(orig_slice, whisper_slice):
                result.append({"word": tok, "start": w["start"], "end": w["end"]})
                last_end = w["end"]
        elif not orig_slice:
            if whisper_slice:
                last_end = whisper_slice[-1]["end"]
        elif not whisper_slice:
            for tok in orig_slice:
                result.append({"word": tok, "start": last_end, "end": last_end})
        else:
            block_start, block_end = whisper_slice[0]["start"], whisper_slice[-1]["end"]
            step = (block_end - block_start) / len(orig_slice)
            for k, tok in enumerate(orig_slice):
                result.append({"word": tok, "start": block_start + step * k, "end": block_start + step * (k + 1)})
            last_end = block_end
    return result


def _zip_positional(whisper_words: list[dict], roman_words: list[str]) -> list[dict]:
    """For non-Latin-script narration (Hindi/Urdu/etc.), reconcile_words()'s
    text matching doesn't work: _normalize() strips everything outside
    a-z0-9, so Devanagari/Urdu script collapses to empty strings and
    SequenceMatcher has nothing real to match on - and live-tested, Whisper's
    Hindi model doesn't even reliably transcribe back in the same script we
    fed in (Devanagari narration came back transcribed in Perso-Arabic).
    Instead, pair Whisper's own word-level timestamps directly with our own
    Romanized/Hinglish word list by position - both are transcribing/reading
    the same underlying words, so index-for-index is a reasonable
    approximation. Extra/missing words at the end (count mismatch) are
    dropped rather than guessed at.
    """
    n = min(len(whisper_words), len(roman_words))
    return [
        {"word": roman_words[i], "start": whisper_words[i]["start"], "end": whisper_words[i]["end"]}
        for i in range(n)
    ]


def build_captions(slug: str) -> str:
    build = config.build_dir(slug)
    data = json.loads((build / "narration_meta.json").read_text(encoding="utf-8"))
    title, meta = data["title"], data["beats"]

    # Optional: build/romanized.json = {"<beat_id>": "roman hinglish text..."} -
    # when present for a beat, captions show this Romanized text (positionally
    # zipped to Whisper's own word timestamps) instead of the original script
    # text. Absent entirely for every English-narrated slug today - zero
    # behavior change there.
    romanized_path = build / "romanized.json"
    romanized = json.loads(romanized_path.read_text(encoding="utf-8")) if romanized_path.exists() else {}

    # manifest.json - read here only to know which segments carry an evidence inset
    # (visuals/resolve.py's "evidence" key), so the matching "SOURCE" label can be
    # burned at the same absolute coordinates assemble.py composited the bordered
    # image at (both call evidence.position_for_segment(seg_id) with the same seed).
    manifest_path = build / "manifest.json"
    manifest = {e["id"]: e for e in json.loads(manifest_path.read_text(encoding="utf-8"))} if manifest_path.exists() else {}

    subs = pysubs2.SSAFile()
    subs.info["PlayResX"] = str(config.WIDTH)
    subs.info["PlayResY"] = str(config.HEIGHT)
    subs.styles["Word"] = _build_word_style()
    subs.styles["Title"] = _build_title_style()
    subs.styles["EvidenceLabel"] = _build_evidence_label_style()

    total_duration = meta[-1]["end"] + config.BEAT_GAP_SEC  # matches audio_mix.py's trailing apad
    subs.append(
        pysubs2.SSAEvent(start=0, end=round(total_duration * 1000), style="Title", text=title)
    )

    for beat in meta:
        words = beat.get("words")
        if not words:
            continue
        if beat["id"] in romanized:
            words = _zip_positional(words, romanized[beat["id"]].split())
        else:
            words = reconcile_words(beat["narration"], words)
        for w in words:
            if not w["word"]:
                continue
            start = beat["start"] + w["start"]
            end = beat["start"] + w["end"]
            if end <= start:
                continue
            display_word = _convert_number_token(w["word"])
            event = pysubs2.SSAEvent(
                start=round(start * 1000),
                end=round(end * 1000),
                style="Word",
                text="{" + POP_TAG + "}" + display_word,
            )
            subs.append(event)

    # Evidence "SOURCE" labels - one event per segment that has a resolved evidence
    # inset, spanning exactly that segment's own start/end (already absolute/global
    # timeline values from narration.py's _segment_timing(), no beat-start offset
    # needed here, unlike the per-word loop above). \pos() places it at the same
    # (ex, ey) assemble.py composited the bordered image at, 8px inside its border.
    for beat in meta:
        for seg_i, seg in enumerate(beat["segments"]):
            seg_id = f"{beat['id']}_seg{seg_i:02d}"
            ev = manifest.get(seg_id, {}).get("evidence")
            if not ev:
                continue
            ex, ey = evidence.position_for_segment(seg_id)
            label_x, label_y = ex + 8, ey + 8
            subs.append(
                pysubs2.SSAEvent(
                    start=round(seg["start"] * 1000),
                    end=round(seg["end"] * 1000),
                    style="EvidenceLabel",
                    text=f"{{\\pos({label_x},{label_y})}}{config.EVIDENCE_LABEL_TEXT}",
                )
            )

    out_path = build / "captions.ass"
    subs.save(str(out_path))
    return str(out_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("slug")
    args = parser.parse_args()

    path = build_captions(args.slug)
    print(f"Wrote {path}")
