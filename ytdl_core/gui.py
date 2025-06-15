import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from .core import is_playlist, download_video, download_playlist, clean_video_url, clean_playlist_url

def launch_gui():
    root = tk.Tk()
    root.withdraw()

    url = simpledialog.askstring("YouTube Downloader", "Enter YouTube video or playlist URL:")
    if not url:
        messagebox.showerror("Error", "URL is required.")
        return

    path = filedialog.askdirectory(title="Select folder to save videos")
    if not path:
        return

    limit = None
    if is_playlist(url):
        # Clean only if it's a true playlist
        cleaned_url = clean_playlist_url(url)
        limit = simpledialog.askinteger("Playlist", "How many videos to download now?")
        download_playlist(cleaned_url, path, limit)
    else:
        cleaned_url = clean_video_url(url)
        download_video(cleaned_url, path)
