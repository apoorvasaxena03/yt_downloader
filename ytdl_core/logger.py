import logging
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logger = logging.getLogger("yt_downloader")
logger.setLevel(logging.INFO)
log_handler = logging.FileHandler(LOG_DIR / "downloaded.log")
log_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
logger.addHandler(log_handler)

error_logger = logging.getLogger("yt_errors")
error_handler = logging.FileHandler(LOG_DIR / "errors.log")
error_handler.setFormatter(logging.Formatter("%(asctime)s - ERROR - %(message)s"))
error_logger.addHandler(error_handler)

# DRM/SABR warning logger
drm_logger = logging.getLogger("yt_drm_sabr")
drm_handler = logging.FileHandler(LOG_DIR / "skipped_due_to_drm_sabr.log")
drm_handler.setFormatter(logging.Formatter("%(asctime)s - WARNING - %(message)s"))
drm_logger.setLevel(logging.WARNING)
drm_logger.addHandler(drm_handler)