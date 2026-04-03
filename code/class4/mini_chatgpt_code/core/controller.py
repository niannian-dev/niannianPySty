import json
from collections.abc import Callable
from pathlib import Path

from core.task_parser import handle_task


StatusCallback = Callable[[str], None]
ConfirmWriteCallback = Callable[[str], bool]


class AppController:
    def __init__(self, llm, workspace_dir: Path, config: dict, logger=None):
        self.llm = llm
        self.workspace_dir = workspace_dir
        self.config = config
        self.logger = logger

    def process_input(
        self,
        user_input: str,
        on_status: StatusCallback | None = None,
        confirm_write: ConfirmWriteCallback | None = None,
    ) -> dict:
        self._emit_status(on_status, "正在解析任务")
        task = self.llm.parse_task(user_input)
        if self.logger:
            self.logger.info("模型返回任务: %s", json.dumps(task, ensure_ascii=False))

        self._emit_status(on_status, self._status_for_task(task))
        result = handle_task(
            task,
            self.workspace_dir,
            self.llm,
            self.config,
            confirm_write=confirm_write,
        )
        if self.logger:
            self.logger.info("任务执行结果: %s", json.dumps(result, ensure_ascii=False))

        return {
            "task": task,
            "result": result,
            "task_text": self._format_task_output(user_input, task),
            "result_text": self._format_result_output(result),
        }

    def _emit_status(self, on_status: StatusCallback | None, status_text: str):
        if on_status is not None:
            on_status(status_text)

    def _status_for_task(self, task: dict) -> str:
        action = task.get("action")
        status_map = {
            "read_file": "正在读取文件",
            "summarize_file": "正在读取文件",
            "write_file": "正在写入文件",
            "run_command": "正在执行命令",
        }
        return status_map.get(action, "正在执行任务")

    def _format_task_output(self, user_input: str, task: dict) -> str:
        return f"用户输入：\n{user_input}\n\n[模型解析]\n{json.dumps(task, ensure_ascii=False, indent=2)}\n"

    def _format_result_output(self, result: dict) -> str:
        return json.dumps(result, ensure_ascii=False, indent=2)
