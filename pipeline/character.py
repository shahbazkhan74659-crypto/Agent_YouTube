"""Host character pose/position selection. Pure logic, no I/O - pose is picked per
beat (reusing confidence_tags script_parser.py already parses, no new script.md
convention needed); position cycles per segment, independent of pose, which is
what actually creates the "character moves" effect.
"""

import config


def pose_for_beat(beat: dict) -> str:
    """Single pose only for now (see config.CHARACTER_POSES) - kept as a function,
    not a constant, so expanding the pose set later only means editing this
    mapping, not every call site."""
    return "neutral"


def position_for_segment(global_segment_index: int) -> int:
    """Returns an x-offset (pixels from the canvas's left edge) by cycling through
    config.CHARACTER_POSITIONS."""
    return config.CHARACTER_POSITIONS[global_segment_index % len(config.CHARACTER_POSITIONS)]
