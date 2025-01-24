import logging
from config import Config

def setup_logging():
    """Setup logging configuration."""
    config = Config()
    logging.basicConfig(
        filename=config.LOG_FILE,
        level=config.LOG_LEVEL,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )