import os

class Config:
    LOG_DIR = "logs"
    LOG_FILE = os.path.join(LOG_DIR, "app.log")
    LOG_LEVEL = "INFO"
    LOG_MAX_BYTES = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT = 5