"""Evidence-inset placement. Pure logic, no I/O - same role as character.py. Shared
by assemble.py (composites the bordered image) and captions.py (places the "SOURCE"
label) so the two ffmpeg passes can never land the image and its label in different
spots - both call this same function with the same segment id.
"""

import random

import config


def position_for_segment(seg_id: str) -> tuple[int, int]:
    """Deterministic per-segment random pick from config.EVIDENCE_POSITIONS - same
    seeded-by-id pattern as assemble.motion_for_segment / character.position_for_segment.
    The "_evidence" suffix on the seed keeps this independent of motion_for_segment's
    own seed for the same seg_id (no correlation between a segment's motion and its
    evidence placement)."""
    return random.Random(seg_id + "_evidence").choice(config.EVIDENCE_POSITIONS)
