"""Search + license-filter + resolve-to-URL for the four free visual sources
decided in idea.md/voice.md: Wikimedia Commons, NASA, Pixabay, Smithsonian.

Wikimedia and NASA extend the exact calls already proven working in
visuals-test/ (see research-findings.md). Pixabay is confirmed working here too
(live-tested while building this module). Smithsonian's Open Access search API
was live-tested here and found NOT to reliably return image URLs in its
`descriptiveNonRepeating.online_media` field even for queries that should have
image results (0/30 across three test queries) - kept as a last-priority,
best-effort source rather than dropped, in case a future query shape does
return media, but don't rely on it.

Wikimedia note (found live): downloading the full-resolution `url` from
upload.wikimedia.org gets rate-limited fast (429 "please contact noc@wikimedia.org
... or instead use thumbnail images") - Commons explicitly asks bulk/automated
callers to use sized thumbnails instead. We don't need full-res originals for a
1080-wide vertical frame anyway, so this fetches `thumburl` (via `iiurlwidth`,
served from thumb.wikimedia.org) rather than the original.
"""

import html
import re
import sys
import time
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import config  # noqa: E402

HEADERS = {"User-Agent": "YouTubeChannelPipeline/1.0 (personal educational project)"}
TIMEOUT = 15


def _strip_html(text: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", "", text or "")).strip()


def _license_ok(license_short: str, usage_terms: str) -> bool:
    combined = f"{license_short} {usage_terms}".lower()
    return any(k in combined for k in config.ALLOWED_LICENSE_KEYWORDS)


def wikimedia_search(term: str, limit: int = 5) -> list[dict]:
    url = "https://commons.wikimedia.org/w/api.php"
    try:
        r = requests.get(
            url,
            params={"action": "query", "format": "json", "list": "search", "srnamespace": 6, "srsearch": term, "srlimit": limit},
            headers=HEADERS,
            timeout=TIMEOUT,
        )
        r.raise_for_status()
        titles = [item["title"] for item in r.json().get("query", {}).get("search", [])]
    except requests.RequestException:
        return []

    candidates = []
    for i, title in enumerate(titles):
        if i > 0:
            time.sleep(0.4)  # avoid tripping Commons' API rate limit across rapid calls
        try:
            r = requests.get(
                url,
                params={
                    "action": "query",
                    "format": "json",
                    "titles": title,
                    "prop": "imageinfo",
                    "iiprop": "url|extmetadata|size",
                    "iiurlwidth": 1200,
                },
                headers=HEADERS,
                timeout=TIMEOUT,
            )
            r.raise_for_status()
            pages = r.json().get("query", {}).get("pages", {})
        except requests.RequestException:
            continue
        for page in pages.values():
            infos = page.get("imageinfo")
            if not infos:
                continue
            info = infos[0]
            meta = info.get("extmetadata", {})
            license_short = meta.get("LicenseShortName", {}).get("value", "")
            usage_terms = meta.get("UsageTerms", {}).get("value", "")
            if not _license_ok(license_short, usage_terms):
                continue
            candidates.append(
                {
                    "source": "wikimedia",
                    "title": title,
                    "url": info.get("thumburl") or info.get("url"),
                    "width": info.get("thumbwidth", info.get("width")),
                    "height": info.get("thumbheight", info.get("height")),
                    "license": license_short or usage_terms or "unknown",
                    "artist": _strip_html(meta.get("Artist", {}).get("value", "")),
                    "page_url": info.get("descriptionurl"),
                }
            )
    return candidates


def _nasa_orig_asset(nasa_id: str) -> str | None:
    try:
        r = requests.get(f"https://images-api.nasa.gov/asset/{nasa_id}", headers=HEADERS, timeout=TIMEOUT)
        r.raise_for_status()
        items = r.json().get("collection", {}).get("items", [])
    except requests.RequestException:
        return None
    orig = [i["href"] for i in items if "~orig" in i["href"]]
    if orig:
        return orig[0]
    return items[-1]["href"] if items else None


def nasa_search(term: str, limit: int = 5) -> list[dict]:
    try:
        r = requests.get(
            "https://images-api.nasa.gov/search",
            params={"q": term, "media_type": "image"},
            headers=HEADERS,
            timeout=TIMEOUT,
        )
        r.raise_for_status()
        items = r.json().get("collection", {}).get("items", [])[:limit]
    except requests.RequestException:
        return []

    candidates = []
    for item in items:
        data = item["data"][0]
        nasa_id = data.get("nasa_id")
        asset_url = _nasa_orig_asset(nasa_id) if nasa_id else None
        if not asset_url:
            continue
        candidates.append(
            {
                "source": "nasa",
                "title": data.get("title", term),
                "url": asset_url,
                "license": "Public Domain (NASA) - verify per-image, see research-findings.md",
                "artist": data.get("center", "NASA"),
                "page_url": item.get("href"),
            }
        )
    return candidates


def _pixabay_relevant(term: str, tags: str) -> bool:
    """Pixabay returns generic/trending hits rather than nothing when a query has no
    good match (live-tested: "Serapeum Alexandria ruins" returned a hot-chocolate
    photo whose tags happened to include "Alexandria" as an incidental location tag)
    - a single incidental word match isn't enough; require at least half of the
    query's non-trivial words to actually appear in the hit's tags."""
    words = [w for w in re.findall(r"[a-z]+", term.lower()) if len(w) >= 4]
    if not words:
        return True
    tags_lower = tags.lower()
    matches = sum(1 for w in words if w in tags_lower)
    return matches >= max(1, (len(words) + 1) // 2)


def pixabay_search(term: str, limit: int = 5) -> list[dict]:
    if not config.PIXABAY_API_KEY:
        return []
    try:
        r = requests.get(
            "https://pixabay.com/api/",
            params={
                "key": config.PIXABAY_API_KEY,
                "q": term,
                "image_type": "photo",
                "per_page": max(limit, 3),  # Pixabay's API minimum is 3
                "safesearch": "true",
            },
            headers=HEADERS,
            timeout=TIMEOUT,
        )
        r.raise_for_status()
        hits = r.json().get("hits", [])[:limit]
    except requests.RequestException:
        return []

    return [
        {
            "source": "pixabay",
            "title": h.get("tags", term),
            "url": h.get("largeImageURL"),
            "width": h.get("imageWidth"),
            "height": h.get("imageHeight"),
            "license": "Pixabay Content License (free for commercial use, no attribution required)",
            "artist": h.get("user", "pixabay"),
            "page_url": h.get("pageURL"),
        }
        for h in hits
        if h.get("largeImageURL") and _pixabay_relevant(term, h.get("tags", ""))
    ]


def smithsonian_search(term: str, limit: int = 5) -> list[dict]:
    """Best-effort only - see module docstring. Returns [] far more often than not."""
    if not config.API_DATA_GOV_KEY:
        return []
    try:
        r = requests.get(
            "https://api.si.edu/openaccess/api/v1.0/search",
            params={"q": term, "api_key": config.API_DATA_GOV_KEY, "rows": limit},
            headers=HEADERS,
            timeout=TIMEOUT,
        )
        r.raise_for_status()
        rows = r.json().get("response", {}).get("rows", [])
    except requests.RequestException:
        return []

    candidates = []
    for row in rows:
        media = row.get("content", {}).get("descriptiveNonRepeating", {}).get("online_media")
        if not media:
            continue
        for m in media.get("media", []):
            if m.get("type") != "Images":
                continue
            resources = m.get("resources", [])
            if not resources:
                continue
            best = resources[-1]
            candidates.append(
                {
                    "source": "smithsonian",
                    "title": row.get("title", term),
                    "url": best.get("url"),
                    "license": "Smithsonian Open Access (CC0) - verify per-collection",
                    "artist": "Smithsonian",
                    "page_url": row.get("content", {}).get("descriptiveNonRepeating", {}).get("record_link"),
                }
            )
    return candidates


SOURCE_PRIORITY = (wikimedia_search, nasa_search, pixabay_search, smithsonian_search)


def search_image(term: str) -> dict | None:
    """Tries each source in priority order, returns the first license-clean candidate found."""
    for search_fn in SOURCE_PRIORITY:
        candidates = search_fn(term)
        if candidates:
            return candidates[0]
    return None


def search_and_download(term: str, dest_stub: Path, ext_fn) -> dict | None:
    """Tries every candidate from every source (in priority order) until one actually
    downloads - a search hit whose file 404s/429s doesn't kill the whole run, it just
    moves on to the next candidate."""
    for search_fn in SOURCE_PRIORITY:
        for candidate in search_fn(term):
            dest = dest_stub.with_suffix(ext_fn(candidate["url"]))
            try:
                download(candidate, dest)
            except requests.RequestException:
                continue
            return {"path": str(dest), **candidate}
    return None


def download(candidate: dict, dest_path: Path, attempts: int = 3, backoff_sec: float = 5.0) -> Path:
    last_error = None
    for attempt in range(1, attempts + 1):
        try:
            r = requests.get(candidate["url"], headers=HEADERS, timeout=30)
            r.raise_for_status()
            dest_path.write_bytes(r.content)
            return dest_path
        except requests.RequestException as exc:
            last_error = exc
            if attempt < attempts:
                time.sleep(backoff_sec)
    raise last_error
