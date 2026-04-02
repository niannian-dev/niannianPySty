import json
from pathlib import Path

from core.config import load_config, BASE_DIR
from core.logger import setup_logger
from core.llm import LLMClient
from core.task_parser import handle_task

def main() -> None:
    config = load_config()
    logger = setup_logger(config.get("APP_LOG_LEVEL", "INFO"))
    workspace_dir = BASE_DIR / config.get("WORKSPACE_DIR", "workspace")
    workspace_dir.mkdir(exist_ok=True)
    llm = LLMClient(config)
    logger.info("应用启动成功")
    logger.info("workspace_dir=%s", workspace_dir)
    print("=== mini ChatGPT Code 工程化版本 ===")
    print("示例：")
    print("  读取 test.txt")
    print("  写入 note.txt 内容是 你好")
    print("  执行 python --version")
    print("输入 exit 退出")
    print()
    while True:
        user_input = input("请输入> ").strip()
        if user_input.lower() == "exit":
            logger.info("用户退出程序")
            print("程序结束")
            break
        logger.info("收到用户输入: %s", user_input)
        try:
            task = llm.parse_task(user_input)
            logger.info("模型返回任务: %s", json.dumps(task, ensure_ascii=False))
            print("\n[模型返回的任务 JSON]")
            print(json.dumps(task, ensure_ascii=False, indent=2))
            result = handle_task(task, workspace_dir)
            logger.info("任务执行结果: %s", json.dumps(result, ensure_ascii=False))
            print("\n[执行结果]")
            print(json.dumps(result, ensure_ascii=False, indent=2))
            print("-" * 50)
        except Exception as e:
            logger.exception("程序执行异常")
            print(f"\n程序异常: {e}")
            print("-" * 50)

if __name__ == "__main__":
    main()