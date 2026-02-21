import os
import logging
from logging.handlers import RotatingFileHandler
from app.config import Config

def setup_logger(name: str = "app_logger"):
    # Garante que a pasta existe
    os.makedirs(Config.LOG_DIR, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(Config.LOG_LEVEL)

    if not logger.handlers:
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        # Handler de Arquivo
        file_handler = RotatingFileHandler(
            Config.LOG_FILE,
            maxBytes=Config.LOG_MAX_BYTES,
            backupCount=Config.LOG_BACKUP_COUNT
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Handler de Console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger