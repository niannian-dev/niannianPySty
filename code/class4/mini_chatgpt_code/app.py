import json

from core.config import load_config, BASE_DIR
from core.controller import AppController
from core.logger import setup_logger
from core.llm import LLMClient


def confirm_write_in_cli(path: str) -> bool:
    answer = input(f"即将写入文件 {path}，是否继续？(y/n): ").strip().lower()
    return answer == "y"

def main() -> None:
    config = load_config()
    logger = setup_logger(config.get("APP_LOG_LEVEL", "INFO"))
    workspace_dir = BASE_DIR / config.get("WORKSPACE_DIR", "workspace")
    workspace_dir.mkdir(exist_ok=True)
    llm = LLMClient(config)
    controller = AppController(llm=llm, workspace_dir=workspace_dir, config=config, logger=logger)
    logger.info("应用启动成功")
    logger.info("workspace_dir=%s", workspace_dir)
    print("=== mini ChatGPT Code 二段式工程版 ===")
    print("示例：")
    print("  读取 test.txt")
    print("  总结 test.txt")
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
            execution = controller.process_input(
                user_input,
                confirm_write=confirm_write_in_cli,
            )
            print("\n[模型返回的任务 JSON]")
            print(json.dumps(execution["task"], ensure_ascii=False, indent=2))
            print("\n[执行结果]")
            print(execution["result_text"])
            print("-" * 50)
        except Exception as e:
            logger.exception("程序执行异常")
            print(f"\n程序异常: {e}")
            print("-" * 50)

if __name__ == "__main__":
    main()
