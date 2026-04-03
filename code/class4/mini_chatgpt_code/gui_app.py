import json
import tkinter as tk
from tkinter import ttk, messagebox

from core.config import load_config, BASE_DIR
from core.logger import setup_logger
from core.llm import LLMClient
from core.task_parser import handle_task

class MiniChatGPTGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("mini ChatGPT Code")
        self.root.geometry("1000x720")
        # 加载项⽬配置
        self.config = load_config()
        self.logger = setup_logger(self.config.get("APP_LOG_LEVEL", "INFO"))
        self.workspace_dir = BASE_DIR / self.config.get("WORKSPACE_DIR", "workspace")
        self.workspace_dir.mkdir(exist_ok=True)
        self.llm = LLMClient(self.config)
        # 顶部标题
        title_label = ttk.Label(root, text="mini ChatGPT Code ⼆段式⼯程版")
        title_label.pack(pady=10)
        # 输⼊区域
        input_frame = ttk.Frame(root)
        input_frame.pack(fill="x", padx=10, pady=5)
        input_label = ttk.Label(input_frame, text="请输⼊指令：")
        input_label.pack(anchor="w")
        self.input_entry = ttk.Entry(input_frame, width=100)
        self.input_entry.pack(fill="x", pady=5)
        # 按钮区域
        button_frame = ttk.Frame(root)
        button_frame.pack(fill="x", padx=10, pady=5)
        run_button = ttk.Button(button_frame, text="执⾏", command=self.run_task)
        run_button.pack(side="left", padx=5)
        clear_button = ttk.Button(button_frame, text="清空输出", command=self.clear_output)
        clear_button.pack(side="left", padx=5)
        example_button = ttk.Button(button_frame, text="填⼊示例", command=self.fill_example)
        example_button.pack(side="left", padx=5)
        # 输出区域
        output_frame = ttk.Frame(root)
        output_frame.pack(fill="both", expand=True, padx=10, pady=10)
        output_label = ttk.Label(output_frame, text="输出结果：")
        output_label.pack(anchor="w")
        self.output_text = tk.Text(output_frame, wrap="word")
        self.output_text.pack(fill="both", expand=True)
        # 底部提示
        tip = (
            "示例：读取 test.txt | 总结 test.txt | "
            "写⼊note.txt 内容是 你好 | 执⾏ python --version"
        )
        tip_label = ttk.Label(root, text=tip)
        tip_label.pack(pady=5)
    def append_output(self, text):
        self.output_text.insert("end", text + "\n")
        self.output_text.see("end")
    def clear_output(self):
        self.output_text.delete("1.0", "end")
    def fill_example(self):
        self.input_entry.delete(0, "end")
        self.input_entry.insert(0, "总结 test.txt")
    def run_task(self):
        user_input = self.input_entry.get().strip()
        if not user_input:
            messagebox.showwarning("提示", "请输⼊内容")
            return
        self.append_output("=" * 60)
        self.append_output(f"[⽤户输⼊]\n{user_input}")
        try:
            task = self.llm.parse_task(user_input)
            self.append_output("[模型返回的任务 JSON]")
            self.append_output(json.dumps(task, ensure_ascii=False, indent=2))
            result = handle_task(task, self.workspace_dir, self.llm, self.config)
            self.append_output("[执⾏结果]")
            self.append_output(json.dumps(result, ensure_ascii=False, indent=2))
        except Exception as e:
            self.logger.exception("GUI执⾏异常")
            messagebox.showerror("错误", str(e))
def main():
    root = tk.Tk()
    app = MiniChatGPTGUI(root)
    root.mainloop()

    
if __name__ == "__main__":
    main()


