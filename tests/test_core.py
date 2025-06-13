import os
import pytest
from ytdl_core import core

def test_is_playlist():
    assert core.is_playlist("https://youtube.com/playlist?list=xyz")
    assert core.is_playlist("https://www.youtube.com/watch?v=xyz&list=abc")
    assert not core.is_playlist("https://youtube.com/watch?v=xyz")

def test_download_video(tmp_path):
    # Use a short, freely available video for testing (or mock in real unit testing)
    video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Example video
    output_path = tmp_path
    core.download_video(video_url, str(output_path))
    
    # Confirm at least one file was downloaded
    downloaded_files = list(output_path.glob("*"))
    assert len(downloaded_files) > 0