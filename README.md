# 🎥 YouTube Downloader with CLI, GUI & Resume Support

A robust and flexible YouTube downloader using `yt-dlp`, supporting:

- ✅ Video and playlist downloads  
- ✅ Resume interrupted playlists  
- ✅ GUI via Tkinter  
- ✅ Auto-download FFmpeg on Windows  
- ✅ Detailed logging (downloads, errors, DRM)  
- ✅ Reusable as a Python module  
- ✅ CLI usage for automation  

---

## 🚀 Features

- 🔗 Supports YouTube videos & playlists  
- 💾 Resume interrupted downloads (per playlist)  
- 🎞️ Auto-selects best quality (with fallback if `ffmpeg` is missing)  
- 🧩 Downloads audio/video and merges using `ffmpeg`  
- 🔐 Logs DRM, SABR, and geo-blocking warnings separately  
- 🧪 Unit-tested core logic  
- 🖥️ Simple GUI for non-technical users  

---

## ⚙️ Installation

```bash
git clone https://github.com/<your-username>/yt-downloader.git
cd yt-downloader
pip install -e .
```
---

## 🧪 Usage

- ▶️ CLI Examples
```bash
# Download a single video
yt-downloader --url "https://youtu.be/xyz123" --output "C:/Videos"

# Download first 5 videos from a playlist
yt-downloader --url "https://youtube.com/playlist?list=PL123..." --output "C:/Videos" --limit 5

# Resume previously interrupted playlist
yt-downloader --resume --output "C:/Videos" --playlist "https://youtube.com/playlist?list=PL123..."
```

- 🖥️ GUI (Optional)
```bash
python -m ytdl_core.gui
```
A Tkinter-based GUI will open for video/playlist downloading.
