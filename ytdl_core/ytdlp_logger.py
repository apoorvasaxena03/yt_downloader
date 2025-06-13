from .logger import drm_logger
import re

class YTDLPLogger:
    """
    Custom logger for yt-dlp that logs known warnings (DRM, geo-block, etc.)
    and extracts the video ID to reconstruct the full YouTube URL.
    """

    def debug(self, msg): pass

    def warning(self, msg: str):
        msg_lower = msg.lower()

        warning_types = {
            "drm protected": "🔒 DRM Protection",
            "sabr streaming": "⚠️ SABR Streaming Restriction",
            "geo-restricted": "🌍 Geo-blocked",
            "not available in your country": "🌍 Country Restriction",
            "age restricted": "🔞 Age Restriction",
            "missing a url": "🚫 Format Missing URL",
            "no video formats": "🚫 No Video Formats",
        }

        for key, label in warning_types.items():
            if key in msg_lower:
                # Try to extract video ID
                video_id = self._extract_video_id(msg)
                video_url = f"https://www.youtube.com/watch?v={video_id}" if video_id else "Unknown URL"
                drm_logger.warning(f"{label} | {video_url} | {msg.strip()}")
                break

    def error(self, msg): pass

    def _extract_video_id(self, msg: str) -> str:
        """Extracts video ID from yt-dlp messages like [youtube] RgNf8LjN8CM:"""
        match = re.search(r"\[youtube\]\s+([a-zA-Z0-9_-]{11})", msg)
        return match.group(1) if match else ""
