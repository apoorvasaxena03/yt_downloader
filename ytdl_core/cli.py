import argparse
from .core import is_playlist, download_video, download_playlist, resume_download
from pathlib import Path

def get_download_path(path: str) -> str:
    download_path = Path(path).expanduser().resolve()
    download_path.mkdir(parents=True, exist_ok=True)
    return str(download_path)

def run_cli():
    parser = argparse.ArgumentParser(description="Download YouTube videos or playlists.")
    parser.add_argument("--url", type=str, help="YouTube video or playlist URL")
    parser.add_argument("--path", type=str, help="Download destination folder", default="downloads")
    parser.add_argument("--limit", type=int, help="Number of videos to download (playlist only)")
    parser.add_argument("--resume", action="store_true", help="Resume last playlist download")
    args = parser.parse_args()

    output_path = get_download_path(args.path)

    if args.resume:
        resume_download(output_path)
    elif args.url:
        if is_playlist(args.url):
            download_playlist(args.url, output_path, args.limit)
        else:
            download_video(args.url, output_path)
    else:
        print("Error: Provide either --url or --resume.")