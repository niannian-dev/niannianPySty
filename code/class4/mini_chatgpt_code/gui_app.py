import threading
import tkinter as tk
from tkinter import ttk, messagebox

from core.config import load_config, BASE_DIR
from core.controller import AppController
from core.logger import setup_logger
from core.llm import LLMClient


class MiniChatGPTGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("mini ChatGPT Code")
        self.root.geometry("1000x720")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(2, weight=1)

        self.config = load_config()
        self.logger = setup_logger(self.config.get("APP_LOG_LEVEL", "INFO"))
        self.workspace_dir = BASE_DIR / self.config.get("WORKSPACE_DIR", "workspace")
        self.workspace_dir.mkdir(exist_ok=True)
        self.llm = LLMClient(self.config)
        self.controller = AppController(
            llm=self.llm,
            workspace_dir=self.workspace_dir,
            config=self.config,
            logger=self.logger,
        )

        self.status_var = tk.StringVar(value="空闲")
        self.display_mode = self._resolve_mode_label()
        self.command_options = self._dedupe_commands(self.config.get("ALLOWED_COMMANDS", []))
        self.task_templates = self._build_task_templates()
        self.task_type_var = tk.StringVar()
        self.detail_option_var = tk.StringVar()
        self.capability_var = tk.StringVar()

        self._build_root_layout()
        self._build_top_info()
        self._build_input_area()
        self._build_output_area()
        self._build_status_bar()

    def _build_root_layout(self):
        self.top_frame = ttk.Frame(self.root, padding=(10, 8))
        self.top_frame.grid(row=0, column=0, sticky="ew")
        self.top_frame.columnconfigure(0, weight=1)

        self.input_frame = ttk.Frame(self.root, padding=(10, 4))
        self.input_frame.grid(row=1, column=0, sticky="ew")
        self.input_frame.columnconfigure(0, weight=1)

        self.content_frame = ttk.Frame(self.root, padding=(10, 6))
        self.content_frame.grid(row=2, column=0, sticky="nsew")
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.columnconfigure(1, weight=1)
        self.content_frame.rowconfigure(0, weight=1)

        self.status_frame = ttk.Frame(self.root, padding=(10, 4))
        self.status_frame.grid(row=3, column=0, sticky="ew")
        self.status_frame.columnconfigure(1, weight=1)

    def _resolve_mode_label(self):
        request_mode = self.config.get("REQUEST_MODE", "chat_completions")
        friendly_names = {
            "chat_completions": "聊天解析模式",
            "gpt-4o": "多模态协作模式",
            "gpt-4o-mini": "快速多模态模式",
        }
        return friendly_names.get(request_mode, request_mode)

    def _dedupe_commands(self, commands):
        ordered_commands = []
        seen = set()
        for command in commands:
            command_text = str(command).strip()
            if not command_text:
                continue
            normalized = command_text.lower()
            if normalized in seen:
                continue
            seen.add(normalized)
            ordered_commands.append(command_text)
        return ordered_commands

    def _build_task_templates(self):
        return {
            "读取文件": [
                "读取 test.txt",
                "读取 notes/todo.txt",
            ],
            "总结文件": [
                "总结 test.txt",
                "解释 notes/todo.txt",
            ],
            "写入文件": [
                "写入 note.txt 内容是 你好",
                "写入 logs/today.txt 内容是 今天完成了测试",
            ],
            "执行命令": self.command_options or ["python"],
        }

    def _get_capability_text(self, task_type=None):
        lines = [
            "支持动作：读取文件 / 总结文件 / 写入文件 / 执行命令",
            "路径要求：请使用工作目录内的相对路径，例如 test.txt 或 notes/a.txt",
            "示例格式：读取 test.txt；总结 test.txt；写入 note.txt 内容是 你好；执行 python --version",
        ]
        if task_type == "执行命令":
            command_text = "、".join(self.command_options) if self.command_options else "当前未配置白名单命令"
            lines.append(f"当前白名单命令：{command_text}")
        return "\n".join(lines)

    def _build_top_info(self):
        title_label = ttk.Label(
            self.top_frame,
            text="mini ChatGPT Code 控制台",
            font=("Helvetica", 18, "bold"),
        )
        title_label.grid(row=0, column=0, sticky="w")

        info_frame = ttk.Frame(self.top_frame)
        info_frame.grid(row=1, column=0, sticky="ew", pady=(6, 0))
        info_frame.columnconfigure(1, weight=1)

        info_items = [
            ("当前工作目录", str(self.workspace_dir)),
            ("当前模型", self.config.get("OPENAI_MODEL", "未配置")),
            ("当前模式", self.display_mode),
        ]
        for row, (label_text, value) in enumerate(info_items):
            label = ttk.Label(info_frame, text=f"{label_text}:")
            label.grid(row=row, column=0, sticky="w", padx=(0, 5))
            value_label = ttk.Label(info_frame, text=value)
            value_label.grid(row=row, column=1, sticky="w")

    def _build_input_area(self):
        self.input_frame.columnconfigure(0, weight=1)

        capability_frame = ttk.Labelframe(self.input_frame, text="输入提示")
        capability_frame.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        capability_frame.columnconfigure(0, weight=1)
        capability_label = ttk.Label(
            capability_frame,
            textvariable=self.capability_var,
            justify="left",
        )
        capability_label.grid(row=0, column=0, sticky="w", padx=8, pady=6)

        selector_frame = ttk.Frame(self.input_frame)
        selector_frame.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        selector_frame.columnconfigure(1, weight=1)
        selector_frame.columnconfigure(3, weight=1)

        task_type_label = ttk.Label(selector_frame, text="任务类型：")
        task_type_label.grid(row=0, column=0, sticky="w", padx=(0, 5), pady=2)

        task_type_names = list(self.task_templates.keys())
        self.task_type_combo = ttk.Combobox(
            selector_frame,
            textvariable=self.task_type_var,
            values=task_type_names,
            state="readonly",
        )
        self.task_type_combo.grid(row=0, column=1, sticky="ew", pady=2)
        self.task_type_combo.bind("<<ComboboxSelected>>", self._on_task_type_change)

        detail_label = ttk.Label(selector_frame, text="模板/命令：")
        detail_label.grid(row=0, column=2, sticky="w", padx=(12, 5), pady=2)

        self.detail_option_combo = ttk.Combobox(
            selector_frame,
            textvariable=self.detail_option_var,
            state="readonly",
        )
        self.detail_option_combo.grid(row=0, column=3, sticky="ew", pady=2)
        self.detail_option_combo.bind("<<ComboboxSelected>>", self._on_detail_option_change)

        command_row_frame = ttk.Frame(self.input_frame)
        command_row_frame.grid(row=2, column=0, sticky="ew")
        command_row_frame.columnconfigure(0, weight=1)

        entry_label = ttk.Label(command_row_frame, text="请输入命令：")
        entry_label.grid(row=0, column=0, sticky="w", columnspan=2)

        self.input_entry = ttk.Entry(command_row_frame)
        self.input_entry.grid(row=1, column=0, sticky="ew", pady=(5, 0))

        button_frame = ttk.Frame(command_row_frame)
        button_frame.grid(row=1, column=1, sticky="e", padx=(10, 0), pady=(5, 0))

        self.run_button = ttk.Button(button_frame, text="执行", command=self.run_task)
        self.run_button.grid(row=0, column=0, padx=(0, 5))

        clear_button = ttk.Button(button_frame, text="清空输出", command=self.clear_output)
        clear_button.grid(row=0, column=1, padx=5)

        example_button = ttk.Button(button_frame, text="示例", command=self.fill_example)
        example_button.grid(row=0, column=2, padx=(5, 0))

        self.task_type_var.set(task_type_names[0])
        self._refresh_detail_options(task_type_names[0])
        self.capability_var.set(self._get_capability_text())

    def _build_output_area(self):
        task_frame = ttk.Labelframe(self.content_frame, text="模型返回的任务")
        task_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
        task_frame.columnconfigure(0, weight=1)
        task_frame.rowconfigure(0, weight=1)

        result_frame = ttk.Labelframe(self.content_frame, text="执行结果")
        result_frame.grid(row=0, column=1, sticky="nsew", padx=(6, 0))
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)

        self.task_output_text = tk.Text(task_frame, wrap="word")
        task_scroll = ttk.Scrollbar(task_frame, orient="vertical", command=self.task_output_text.yview)
        self.task_output_text.configure(yscrollcommand=task_scroll.set)
        self.task_output_text.grid(row=0, column=0, sticky="nsew", padx=(5, 0), pady=5)
        task_scroll.grid(row=0, column=1, sticky="ns", padx=(0, 5), pady=5)

        self.result_output_text = tk.Text(result_frame, wrap="word")
        result_scroll = ttk.Scrollbar(result_frame, orient="vertical", command=self.result_output_text.yview)
        self.result_output_text.configure(yscrollcommand=result_scroll.set)
        self.result_output_text.grid(row=0, column=0, sticky="nsew", padx=(5, 0), pady=5)
        result_scroll.grid(row=0, column=1, sticky="ns", padx=(0, 5), pady=5)

    def _build_status_bar(self):
        status_label = ttk.Label(self.status_frame, text="状态：")
        status_label.grid(row=0, column=0, sticky="w")

        current_status = ttk.Label(self.status_frame, textvariable=self.status_var)
        current_status.grid(row=0, column=1, sticky="w", padx=(6, 0))

        hint_label = ttk.Label(
            self.status_frame,
            text="(空闲 · 正在解析任务 · 正在执行命令 · 执行完成 · 执行失败)",
        )
        hint_label.grid(row=0, column=2, sticky="e")

    def _set_status(self, status_text):
        self.status_var.set(status_text)

    def _set_run_button_enabled(self, enabled):
        self.run_button.configure(state="normal" if enabled else "disabled")

    def _run_in_ui_thread(self, func):
        done = threading.Event()
        result = {"value": None, "error": None}

        def wrapper():
            try:
                result["value"] = func()
            except Exception as exc:
                result["error"] = exc
            finally:
                done.set()

        self.root.after(0, wrapper)
        done.wait()
        if result["error"] is not None:
            raise result["error"]
        return result["value"]

    def _confirm_write(self, path):
        return self._run_in_ui_thread(
            lambda: messagebox.askyesno("确认写入", f"即将写入文件：{path}\n是否继续？")
        )

    def _display_outputs(self, task_text, result_text):
        self.task_output_text.delete("1.0", "end")
        self.result_output_text.delete("1.0", "end")
        self.task_output_text.insert("end", task_text)
        self.result_output_text.insert("end", result_text)
        self.task_output_text.see("end")
        self.result_output_text.see("end")

    def clear_output(self):
        self.task_output_text.delete("1.0", "end")
        self.result_output_text.delete("1.0", "end")
        self._set_status("空闲")

    def fill_example(self):
        self._apply_detail_selection()

    def _refresh_detail_options(self, task_type):
        options = self.task_templates.get(task_type, [])
        self.detail_option_combo["values"] = options
        if options:
            self.detail_option_var.set(options[0])
        else:
            self.detail_option_var.set("")
        self.capability_var.set(self._get_capability_text(task_type))

    def _apply_input_text(self, text):
        self.input_entry.delete(0, "end")
        self.input_entry.insert(0, text)

    def _build_input_from_selection(self):
        task_type = self.task_type_var.get()
        selected_value = self.detail_option_var.get().strip()
        if not selected_value:
            return ""
        if task_type == "执行命令":
            return f"执行 {selected_value}"
        return selected_value

    def _apply_detail_selection(self):
        selected_text = self._build_input_from_selection()
        if selected_text:
            self._apply_input_text(selected_text)

    def _on_task_type_change(self, _event=None):
        task_type = self.task_type_var.get()
        self._refresh_detail_options(task_type)
        self._apply_detail_selection()

    def _on_detail_option_change(self, _event=None):
        self._apply_detail_selection()

    def _execute_task_in_background(self, user_input):
        try:
            execution = self.controller.process_input(
                user_input,
                on_status=None,
                confirm_write=self._confirm_write,
            )
            self.root.after(0, lambda execution=execution: self._handle_task_success(execution))
        except Exception as exc:
            self.root.after(0, lambda exc=exc: self._handle_task_error(exc))

    def _handle_task_success(self, execution):
        self._display_outputs(
            execution["task_text"],
            execution["result_text"],
        )
        self._set_run_button_enabled(True)
        self._set_status("执行完成")

    def _handle_task_error(self, exc):
        self.logger.exception("GUI 执行失败")
        self._set_run_button_enabled(True)
        self._set_status("执行失败")
        messagebox.showerror("错误", str(exc))

    def run_task(self):
        user_input = self.input_entry.get().strip()
        if not user_input:
            messagebox.showwarning("提示", "请输入命令")
            return

        self.task_output_text.delete("1.0", "end")
        self.result_output_text.delete("1.0", "end")
        self._set_status("处理中")
        self._set_run_button_enabled(False)

        worker = threading.Thread(
            target=self._execute_task_in_background,
            args=(user_input,),
            daemon=True,
        )
        worker.start()


def main():
    root = tk.Tk()
    app = MiniChatGPTGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
