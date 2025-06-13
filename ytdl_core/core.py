from typing import Optional, Callable
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError
from .logger import logger, error_logger
from .ytdlp_logger import YTDLPLogger
from .progress_tracker import save_progress, load_progress, get_progress_file_path
import shutil
import requests
import zipfile
import platform




def clean_video_url(url: str) -> str:
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    if 'v' in query:
        return f"https://www.youtube.com/watch?v={query['v'][0]}"
    elif 'youtu.be' in parsed.netloc:
        return parsed.scheme + "://" + parsed.netloc + parsed.path
    return url


def clean_playlist_url(url: str) -> str:
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    if 'list' in query:
        return f"https://www.youtube.com/playlist?list={query['list'][0]}"
    return url


def ensure_ffmpeg() -> Optional[str]:
    """
    Ensures ffmpeg is available. If not found, downloads and extracts it to a local path (Windows only).
    Returns the ffmpeg path or None.
    """
    if shutil.which("ffmpeg"):
        return "ffmpeg"  # Use system ffmpeg

    if platform.system() != "Windows":
        print("❌ FFmpeg not found and auto-download is only supported on Windows.")
        return None

    ffmpeg_dir = Path("ffmpeg_bin")
    ffmpeg_exe = ffmpeg_dir / "ffmpeg.exe"

    if ffmpeg_exe.exists():
        return str(ffmpeg_exe)

    print("⬇️  Downloading FFmpeg...")

    url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    zip_path = "ffmpeg.zip"

    try:
        # Download zip
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(zip_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        # Extract ffmpeg.exe only
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            for file in zip_ref.namelist():
                if file.endswith("ffmpeg.exe") and "/bin/" in file:
                    zip_ref.extract(file, ffmpeg_dir)
                    ffmpeg_path = ffmpeg_dir / Path(file).name
                    (ffmpeg_dir / file).rename(ffmpeg_path)
                    break

        Path(zip_path).unlink(missing_ok=True)
        print(f"✅ FFmpeg ready at {ffmpeg_exe}")
        return str(ffmpeg_exe)

    except Exception as e:
        print(f"❌ Failed to download FFmpeg: {e}")
        return None


def get_ydl_opts(output_path: str, on_progress: Optional[Callable] = None) -> dict:
    ffmpeg_path = ensure_ffmpeg()
    ffmpeg_installed = ffmpeg_path is not None

    if ffmpeg_installed:
        # ✅ High compatibility: MP4 container, H.264 video, AAC audio
        format_selector = (
            "bestvideo[ext=mp4][vcodec^=avc1]+bestaudio[ext=m4a]/"
            "best[ext=mp4][vcodec^=avc1][acodec^=mp4a]/best"
        )
        merge_format = "mp4"
    else:
        # 🛑 No ffmpeg: fallback to progressive stream
        print("⚠️ FFmpeg unavailable. Falling back to progressive-only (lower quality).")
        format_selector = "best[ext=mp4][vcodec^=avc1][acodec^=mp4a]/best"
        merge_format = None

    return {
        "outtmpl": str(Path(output_path) / "%(title).200s.%(ext)s"),
        "format": format_selector,
        "merge_output_format": merge_format,
        "progress_hooks": [on_progress] if on_progress else [],
        "noplaylist": True,
        "quiet": True,
        **({"ffmpeg_location": ffmpeg_path} if ffmpeg_installed and ffmpeg_path != "ffmpeg" else {})
    }


def download_video(
    url: str,
    output_path: str,
    on_progress: Optional[Callable] = None,
    on_complete: Optional[Callable] = None
) -> None:
    try:
        if "list=" in url:
            print("⚠️  Detected playlist parameters in video URL — cleaning...")

        cleaned_url = clean_video_url(url)

        def hook(d):
            if d["status"] == "finished" and on_complete:
                on_complete(d.get("info_dict", {}), d.get("_default_template", ""))
            elif d["status"] == "downloading" and on_progress:
                on_progress(d)

        ydl_opts = get_ydl_opts(output_path, on_progress=hook)
        ydl_opts["logger"] = YTDLPLogger()

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([cleaned_url])
            logger.info(f"Downloaded: {cleaned_url}")

    except DownloadError as e:
        print(f"❌ Failed: {url} | {e}")
        error_logger.error(f"Failed: {url} | Reason: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {url} | {e}")
        error_logger.error(f"Unexpected error: {url} | Reason: {e}")


def download_playlist(
    url: str,
    output_path: str,
    limit: Optional[int] = None
) -> None:
    try:
        cleaned_url = clean_playlist_url(url)
        with YoutubeDL({"extract_flat": "in_playlist", "quiet": True}) as ydl:
            info_dict = ydl.extract_info(cleaned_url, download=False)
            entries = info_dict.get("entries", [])

        total = len(entries)
        print(f"\n📁 Playlist: {info_dict.get('title', 'Unknown')}")
        print(f"🔢 Total videos: {total}")

        if limit is None:
            limit = int(input(f"How many videos to download now? (max {total}): "))

        to_download = [entry['url'] for entry in entries[:limit]]
        for video_url in to_download:
            download_video(video_url, output_path)

        remaining = [entry['url'] for entry in entries[limit:]]
        if remaining:
            save_progress(cleaned_url, remaining)
            print(f"💾 {len(remaining)} videos saved for later.")
        else:
            progress_file = get_progress_file_path(cleaned_url)
            progress_file.unlink(missing_ok=True)
            print("✅ All videos downloaded.")
    except Exception as e:
        print(f"❌ Playlist download failed: {e}")
        error_logger.error(f"Playlist failed: {url} | Reason: {e}")


def resume_download(output_path: str, playlist_url_or_id: str) -> None:
    progress = load_progress(playlist_url_or_id)
    remaining = progress.get("remaining_urls", [])
    if not remaining:
        print("📭 No videos left to resume.")
        return

    print(f"🔁 Resuming playlist: {progress['playlist_url']}")
    print(f"{len(remaining)} videos remaining.")

    limit = int(input(f"How many to download now? (max {len(remaining)}): "))
    selected = remaining[:limit]

    for url in selected:
        download_video(url, output_path)

    new_remaining = remaining[limit:]
    if new_remaining:
        save_progress(progress["playlist_url"], new_remaining)
        print(f"💾 {len(new_remaining)} videos still remaining.")
    else:
        progress_file = get_progress_file_path(progress["playlist_url"])
        progress_file.unlink(missing_ok=True)