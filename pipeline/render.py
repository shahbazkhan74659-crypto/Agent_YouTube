"""Orchestrator: python render.py <topic-slug> [--default-emotion <emotion>]
[--voice ...] [--from-stage STAGE] [--force]

Runs every stage in order, each stage deciding for itself whether its cached
build artifact is still valid (narration.py/alignment.py/visuals/resolve.py/
audio_mix.py/assemble.py all check before redoing work) - the same resumable-
by-stage pattern already proven in assets/audio/src/generate.py.

--from-stage skips everything before that stage (trusting whatever's already on
disk) and forces that stage and everything after to redo their work.
--force forces every stage to redo its work regardless of what's cached.
"""

import argparse

import alignment
import assemble
import audio_mix
import captions
import config
import ffmpeg_tool
import narration
import script_parser
from visuals import resolve as visuals_resolve

STAGES = ["parse", "narration", "alignment", "visuals", "captions", "audio", "assemble"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("slug")
    parser.add_argument(
        "--default-emotion", default=None,
        help="Fallback emotion (e.g. mysterious) for any beat with no [MUSIC: ...] cue in its script.md",
    )
    parser.add_argument("--voice", default=None, help="Kokoro preset; defaults to voice.md's locked-in choice")
    parser.add_argument("--lang", default="en-us", help="espeak-ng language code for Kokoro, e.g. 'hi' for Hindi")
    parser.add_argument("--no-music", action="store_true", help="Skip the music bed entirely (narration + SFX only)")
    parser.add_argument("--from-stage", choices=STAGES, default=None)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    start_idx = STAGES.index(args.from_stage) if args.from_stage else 0
    force = args.force or args.from_stage is not None

    print(f"=== render: {args.slug} ===")

    if start_idx <= STAGES.index("parse"):
        title, beats = script_parser.parse_script(args.slug)
        script_parser.save_beats_json(args.slug, title, beats)
        print(f'[parse]      "{title}" - {len(beats)} beats')

    if start_idx <= STAGES.index("narration"):
        timed, _ = narration.synthesize(args.slug, voice=args.voice, force=force, lang=args.lang)
        print(f"[narration]  {len(timed)} beats, voice={timed[0]['voice']}, "
              f"{timed[-1]['end']:.1f}s narration")

    if start_idx <= STAGES.index("alignment"):
        meta = alignment.align(args.slug, force=force)
        print(f"[alignment]  {sum(len(b['words']) for b in meta)} words aligned")

    if start_idx <= STAGES.index("visuals"):
        manifest, manifest_path = visuals_resolve.resolve_all(args.slug, force=force)
        fallbacks = sum(1 for e in manifest if "fallback_from" in e)
        print(f"[visuals]    {len(manifest)} segments resolved ({fallbacks} fallback) -> {manifest_path}")

    if start_idx <= STAGES.index("captions"):
        captions_path = captions.build_captions(args.slug)
        print(f"[captions]   -> {captions_path}")

    if start_idx <= STAGES.index("audio"):
        mix_path = audio_mix.build_mix(
            args.slug, default_emotion=args.default_emotion, force=force, no_music=args.no_music
        )
        print(f"[audio]      -> {mix_path}")

    if start_idx <= STAGES.index("assemble"):
        final_path = assemble.assemble(args.slug, force=force)
    else:
        final_path = str(config.output_dir(args.slug) / "final.mp4")

    info = ffmpeg_tool.probe_video_info(final_path)
    over_limit = info["duration"] > config.MAX_DURATION_SEC
    print()
    print(f"=== done: {final_path} ===")
    print(f"  {info['width']}x{info['height']}, {info['duration']:.1f}s"
          f"{'  *** OVER the 180s Shorts limit ***' if over_limit else ''}")
    print(f"  sources: {config.build_dir(args.slug) / 'manifest.json'}")
    print()
    print("Technical checks only - watch/listen to the actual file before calling it done:")
    print("  Ken Burns pan looking right, captions legible, music sitting under narration,")
    print("  the Kokoro voice actually sounding good.")


if __name__ == "__main__":
    main()
