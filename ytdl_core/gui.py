import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from .core import is_playlist, download_video, download_playlist

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
        limit = simpledialog.askinteger("Playlist", "How many videos to download now?")

    if is_playlist(url):
        download_playlist(url, path, limit)
    else:
        download_video(url, path)
