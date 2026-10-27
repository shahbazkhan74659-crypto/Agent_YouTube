"""Parses a yt-script-produced script.md into beats.json.

Downstream stages (narration, alignment, visuals, captions, assembly) all read
beats.json, never the raw markdown, so formatting drift in script.md can't break
them. See pipeline/README or the plan for the full stage list.

Each beat is split into one or more visual `segments` at every `[ON SCREEN: ...]`
cue - a cue appearing before a beat's text starts (or right after its label, with
no narration yet) opens segment 0; a cue appearing mid-beat (after some narration
has already accumulated) closes the current segment and opens a new one, so a
single beat can carry several distinct visuals. A cue immediately followed by the
*next* beat's label (no narration in between) is not a dangling empty segment of
the current beat - it carries forward untouched as the next beat's segment 0.
"""

import json
import re
import sys
from dataclasses import asdict, dataclass, field

import config

ON_SCREEN_START_RE = re.compile(r"^\*{0,2}\[ON SCREEN:", re.IGNORECASE)
ON_SCREEN_INNER_RE = re.compile(r"ON SCREEN:\s*(.*?)\]", re.IGNORECASE | re.DOTALL)
MUSIC_CUE_RE = re.compile(r"^\*{0,2}\[MUSIC:\s*([a-z_\- ]+?)\]\*{0,2}\s*$", re.IGNORECASE)
LABEL_LINE_RE = re.compile(r"^\*\*(.+?):\*\*\s*(.*)$")
HEADING_RE = re.compile(r"^#{1,6}\s")
QUOTED_RE = re.compile(r'"([^"]+)"')
AI_GENERATE_BEFORE_RE = re.compile(r"ai-generate\s*:?\s*$", re.IGNORECASE)
CONFIDENCE_RE = re.compile(r"\b(SOLID|CONTESTED|UNCERTAIN)\b", re.IGNORECASE)
MARKDOWN_EMPHASIS_RE = re.compile(r"\*{1,2}([^*]+?)\*{1,2}")


def strip_markdown_emphasis(text: str) -> str:
    """Narration text goes straight to a TTS engine, which reads literal '*'
    characters aloud - live-tested: "What's *not* documented" came out as "What's
    asterisk not asterisk documented". Strips markdown emphasis markup, keeping
    the inner text, before it ever reaches a Segment."""
    return MARKDOWN_EMPHASIS_RE.sub(r"\1", text)


@dataclass
class Cue:
    raw: str
    search_terms: list = field(default_factory=list)
    ai_generate_prompt: str | None = None


@dataclass
class Segment:
    on_screen: Cue | None
    text: str


@dataclass
class Beat:
    id: str
    index: int
    label: str
    tag: str | None
    confidence_tags: list
    narration: str
    segments: list
    emotion: str | None = None  # music mood for this beat onward - see MUSIC_CUE_RE;
    # carries forward from the last [MUSIC: ...] cue seen, same persistence rule as
    # pending_cue for ON SCREEN, except it's not consumed - it keeps applying to every
    # beat after it until the next cue changes it.


def parse_cue(inner_text: str) -> Cue:
    """Splits an ON SCREEN cue's quoted strings into search terms vs. an AI-generate prompt."""
    search_terms = []
    ai_prompt = None
    for m in QUOTED_RE.finditer(inner_text):
        preceding = inner_text[max(0, m.start() - 30) : m.start()]
        if AI_GENERATE_BEFORE_RE.search(preceding):
            ai_prompt = m.group(1)
        else:
            search_terms.append(m.group(1))
    return Cue(raw=inner_text.strip(), search_terms=search_terms, ai_generate_prompt=ai_prompt)


def read_cue_block(lines: list[str], i: int) -> tuple[Cue, int]:
    """Reads a (possibly multi-line) ON SCREEN block starting at line i. Returns
    (Cue, index of the line after the block)."""
    buf = [lines[i].strip()]
    n = len(lines)
    while not re.search(r"\]\*{0,2}\s*$", buf[-1]) and i + 1 < n:
        i += 1
        buf.append(lines[i].strip())
    cue_block = " ".join(buf)
    inner = ON_SCREEN_INNER_RE.search(cue_block)
    return parse_cue(inner.group(1) if inner else cue_block), i + 1


def split_label(header: str):
    """'BEAT 4 — ... (SOLID ... / UNCERTAIN ...)' -> ('BEAT 4 — ...', 'SOLID ... / UNCERTAIN ...')."""
    m = re.match(r"^(.*?)\s*\(([^)]*)\)\s*$", header.strip())
    if m:
        return m.group(1).strip(), m.group(2).strip()
    return header.strip(), None


TITLE_LINE_RE = re.compile(r"^\*\*Title:\*\*\s*(.+)$", re.IGNORECASE | re.MULTILINE)
H1_SCRIPT_RE = re.compile(r"^#\s+Script:\s*(.+)$", re.IGNORECASE | re.MULTILINE)


def extract_title(text: str) -> str:
    """The short on-screen title (yt-script writes a '**Title:** ...' line near the
    top of script.md). Falls back to the descriptive '# Script: <topic>' H1 heading
    if that line is missing, so an older/hand-edited script doesn't just break."""
    m = TITLE_LINE_RE.search(text)
    if m:
        return m.group(1).strip()
    m = H1_SCRIPT_RE.search(text)
    if m:
        return m.group(1).strip()
    raise ValueError("No '**Title:**' line or '# Script: ...' heading to derive a title from")


def extract_script_section(text: str) -> str:
    """Isolates the '## Script' section from script.md (stops at the next '## ' heading)."""
    lines = text.split("\n")
    start = None
    end = len(lines)
    for i, line in enumerate(lines):
        if start is None and re.match(r"^#{1,6}\s*Script\s*$", line.strip(), re.IGNORECASE):
            start = i + 1
            continue
        if start is not None and i > start and HEADING_RE.match(line.strip()):
            end = i
            break
    if start is None:
        raise ValueError("No '## Script' section found in script.md")
    return "\n".join(lines[start:end])


def parse_script(slug: str) -> tuple[str, list[Beat]]:
    path = config.video_dir(slug) / "script.md"
    if not path.exists():
        raise FileNotFoundError(f"No script.md for '{slug}' at {path}")
    full_text = path.read_text(encoding="utf-8")
    title = extract_title(full_text)
    section = extract_script_section(full_text)
    lines = section.split("\n")
    n = len(lines)

    beats: list[Beat] = []
    current_beat: Beat | None = None
    current_segment_buf: list[str] = []
    pending_cue: Cue | None = None
    current_emotion: str | None = None

    def flush_segment():
        nonlocal pending_cue, current_segment_buf
        if current_beat is None:
            return
        text = strip_markdown_emphasis(" ".join(current_segment_buf).strip())
        if text:
            current_beat.segments.append(Segment(on_screen=pending_cue, text=text))
            pending_cue = None  # consumed - an empty-text flush (nothing accumulated
            # yet) leaves pending_cue untouched so it carries forward to whatever
            # segment/beat comes next, instead of being dropped or misattributed.
        current_segment_buf = []

    i = 0
    while i < n:
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        if ON_SCREEN_START_RE.match(line):
            cue, i = read_cue_block(lines, i)
            flush_segment()
            pending_cue = cue
            continue

        music_m = MUSIC_CUE_RE.match(line)
        if music_m:
            # Beat-level granularity only (music shifts "per part of the video", not
            # mid-beat) - a cue stamps itself onto whichever beat is created *next*,
            # same as the current beat if this cue sits before its label line. A cue
            # landing mid-beat (after that beat's own label) has no effect until the
            # following beat, since there's no narrower unit to attach it to.
            name = music_m.group(1).strip().lower().replace(" ", "_").replace("-", "_")
            if name not in config.EMOTION_CATEGORIES:
                raise ValueError(
                    f"Unknown [MUSIC: {music_m.group(1)}] cue - must be one of "
                    f"{', '.join(config.EMOTION_CATEGORIES)}"
                )
            current_emotion = name
            i += 1
            continue

        m = LABEL_LINE_RE.match(line)
        if m:
            flush_segment()
            if current_beat is not None:
                beats.append(current_beat)
            header, first_text = m.group(1), m.group(2)
            label, tag = split_label(header)
            confidence_tags = [t.upper() for t in CONFIDENCE_RE.findall(tag or "")]
            current_beat = Beat(
                id=f"beat_{len(beats) + 1:02d}",
                index=len(beats) + 1,
                label=label,
                tag=tag,
                confidence_tags=confidence_tags,
                narration="",
                segments=[],
                emotion=current_emotion,
            )
            current_segment_buf = [first_text] if first_text else []
            i += 1
            continue

        if HEADING_RE.match(line):
            i += 1
            continue

        if current_beat is not None:
            current_segment_buf.append(line)
        i += 1

    flush_segment()
    if current_beat is not None:
        beats.append(current_beat)

    if not beats:
        raise ValueError(f"Parsed zero beats from {path} — check the script's markdown shape")

    for b in beats:
        if not b.segments:
            raise ValueError(f"{b.id} ({b.label}) has no narration text")
        b.narration = " ".join(seg.text for seg in b.segments).strip()

    return title, beats


def save_beats_json(slug: str, title: str, beats: list[Beat]) -> str:
    out_path = config.build_dir(slug) / "beats.json"
    data = {"title": title, "beats": [asdict(b) for b in beats]}
    out_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return str(out_path)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_parser.py <topic-slug>")
        sys.exit(1)
    slug = sys.argv[1]
    title, beats = parse_script(slug)
    path = save_beats_json(slug, title, beats)
    total_segments = sum(len(b.segments) for b in beats)
    print(f'Title: "{title}"')
    print(f"Parsed {len(beats)} beats, {total_segments} visual segments -> {path}\n")
    for b in beats:
        print(f"[{b.id}] {b.label} ({b.tag or '-'}) | emotion={b.emotion or 'NONE'} | {len(b.segments)} segment(s)")
        for s_i, seg in enumerate(b.segments):
            if seg.on_screen is None:
                cue_desc = "(none - falls back to previous visual)"
            elif seg.on_screen.ai_generate_prompt and not seg.on_screen.search_terms:
                cue_desc = f"AI-generate: {seg.on_screen.ai_generate_prompt[:40]}..."
            else:
                cue_desc = ", ".join(seg.on_screen.search_terms) or seg.on_screen.raw[:40]
            snippet = seg.text[:70] + ("..." if len(seg.text) > 70 else "")
            print(f"    seg{s_i}: [{cue_desc}] {snippet}")
