import logging
from pathlib import Path
from .config import load_config
 
logger_level = load_config().get("APP_LOG_LEVEL")

def setup_logger(log_level: str = logger_level) -> logging.Logger:
    base_dir = Path(__file__).resolve().parent.parent
    log_dir = base_dir / "logs"
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "app.log"
    logging.basicConfig(
        level=getattr(logging, log_level.upper(), logging.INFO),format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger("mini_chatgpt_code")

