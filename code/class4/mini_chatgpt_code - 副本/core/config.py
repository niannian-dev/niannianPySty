import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "keyConfig.json"

def load_config() -> dict:
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"配置文件不存在:{CONFIG_PATH}")
    
    with open(CONFIG_PATH, "r" , encoding="utf-8") as f:
        config = json.load(f)

    if not config.get("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY 未配置")
    
    return config

# def main():
#     strr = load_config()
#     print(strr)
#     print(strr.get("APP_LOG_LEVEL"))

# if __name__ == "__main__":
#     main()