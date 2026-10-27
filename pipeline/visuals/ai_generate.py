"""Pollinations.ai handler for 'AI-generate:' cues - free, keyless image generation,
used because free Gemini image generation is confirmed blocked (0 free-tier quota,
see research-findings.md).

Live-tested while building this module: the free "classic" tier enforces a hard
**1 image per 45 seconds per IP** limit (returns HTTP 402 FREE_LIMIT otherwise) and
also returned 503 "at its limit" transiently; the delivered image was 576x1024
rather than the requested 1080x1920 (same 9:16 aspect, smaller size - the service
appears to cap resolution on this tier). A module-level rate limiter enforces the
45s spacing proactively (instead of just retrying after a 402), since a
multi-AI-generate-cue video will otherwise burn through retries back-to-back.
resolve.py upscales the result during the Ken Burns pass in assemble.py regardless,
so the smaller size isn't a problem on its own.
"""

import sys
import threading
import time
import urllib.parse
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import config  # noqa: E402

HEADERS = {"User-Agent": "YouTubeChannelPipeline/1.0 (personal educational project)"}
MAX_ATTEMPTS = 5
RETRY_DELAY_SEC = 20
MIN_INTERVAL_SEC = 46  # free tier: 1 image / 45s per IP - pad by 1s

_rate_lock = threading.Lock()
_last_call_time = 0.0


def _wait_for_slot() -> None:
    global _last_call_time
    with _rate_lock:
        elapsed = time.time() - _last_call_time
        if elapsed < MIN_INTERVAL_SEC:
            time.sleep(MIN_INTERVAL_SEC - elapsed)
        _last_call_time = time.time()


def generate(prompt: str, dest_path: Path, width: int = config.SQUARE_WIDTH, height: int = config.SQUARE_HEIGHT) -> Path:
    url = config.POLLINATIONS_URL.format(prompt=urllib.parse.quote(prompt))
    last_error = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        _wait_for_slot()
        try:
            r = requests.get(url, params={"width": width, "height": height, "nologo": "true"}, timeout=60)
        except requests.RequestException as exc:
            last_error = str(exc)
        else:
            if r.status_code == 200 and r.headers.get("content-type", "").startswith("image/"):
                dest_path.write_bytes(r.content)
                return dest_path
            last_error = f"HTTP {r.status_code}: {r.text[:200]}"
        if attempt < MAX_ATTEMPTS:
            time.sleep(RETRY_DELAY_SEC)
    raise RuntimeError(f"Pollinations.ai failed after {MAX_ATTEMPTS} attempts for prompt '{prompt[:60]}...': {last_error}")
