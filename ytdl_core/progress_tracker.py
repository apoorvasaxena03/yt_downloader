import json
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from typing import List, Dict, Any


PROGRESS_DIR = Path("progress")
PROGRESS_DIR.mkdir(exist_ok=True)


def extract_playlist_id(url: str) -> str:
    """Extract playlist ID from a YouTube playlist URL."""
    query = parse_qs(urlparse(url).query)
    return query.get("list", ["unknown"])[0]


def get_progress_file_path(playlist_url: str) -> Path:
    playlist_id = extract_playlist_id(playlist_url)
    return PROGRESS_DIR / f"{playlist_id}.json"


def save_progress(playlist_url: str, remaining_urls: List[str]) -> None:
    """Save remaining video URLs for a playlist."""
    file_path = get_progress_file_path(playlist_url)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump({
            "playlist_url": playlist_url,
            "remaining_urls": remaining_urls
        }, f, indent=2)


def load_progress(playlist_url_or_id: str) -> Dict[str, Any]:
    """Load progress using full playlist URL or playlist ID."""
    if "list=" in playlist_url_or_id:
        file_path = get_progress_file_path(playlist_url_or_id)
    else:
        file_path = PROGRESS_DIR / f"{playlist_url_or_id}.json"

    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"playlist_url": "", "remaining_urls": []}
