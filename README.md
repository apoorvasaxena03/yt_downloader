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
A Tkinter-based GUI will open for video/playlist downloading.
```bash
python -m ytdl_core.main
```

- 🐍 Python Module
You can use this tool programmatically as a module:
```python
from ytdl_core.core import download_video, download_playlist, resume_download

# Download a single video
download_video("https://youtu.be/xyz123", "C:/Videos")

# Download a playlist (with user input for how many to download)
download_playlist("https://youtube.com/playlist?list=PL123...", "C:/Videos")

# Resume from a previously saved playlist session
resume_download("C:/Videos", "https://youtube.com/playlist?list=PL123...")
```

---

## 📂 Folder Structure

```bash
yt_downloader/
├── ytdl_core/
│   ├── core.py               # Main download logic
│   ├── gui.py                # GUI via Tkinter
│   ├── logger.py             # Log handlers
│   ├── ytdlp_logger.py       # Custom yt-dlp logger for warnings
│   ├── progress_tracker.py  # Playlist resume support
│   └── __init__.py
│
├── tests/
│   └── test_core.py          # Unit tests
│
├── logs/
│   ├── downloaded.log
│   ├── errors.log
│   └── drm.log
│
├── ffmpeg_bin/              # Auto-downloaded FFmpeg (if needed)
├── setup.py
├── requirements.txt
└── README.md
```

---

## 📝 Logging
- logs/downloaded.log — all successful downloads
- logs/errors.log — download failures
- logs/drm.log — warnings like DRM, SABR, geo-blocks

---

## 🔧 Dependencies
- yt-dlp – YouTube downloading backend
- requests – for FFmpeg auto-download
- tkinter – for the GUI
- ffmpeg – merges audio/video streams (auto-downloaded on Windows)

---

## 📄 License
MIT License © [Your Name or GitHub Handle]
