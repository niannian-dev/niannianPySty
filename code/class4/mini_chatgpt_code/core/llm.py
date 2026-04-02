import json
from openai import OpenAI

SYSTEM_PROMPT = """
你是一个代码助手。你必须把用户输入转换成 JSON。
只允许输出一个 JSON 对象，不要输出解释，不要输出 markdown。
你只能返回以下三种 action：
1. read_file
2. write_file
3. run_command
JSON 格式示例：
{"action":"read_file","path":"test.txt"}
{"action":"write_file","path":"note.txt","content":"hello"}
{"action":"run_command","cmd":["python","--version"]}
规则：
- path 必须是相对路径，例如 test.txt 或 notes/a.txt
- 如果用户想看某个文件内容，用 read_file
- 如果用户想写文件，用 write_file
- 如果用户想执行命令，用 run_command
- cmd 必须是字符串数组
- 如果无法理解，就返回：
  {"action":"error","message":"无法理解用户意图"}
"""
class LLMClient:
    def __init__(self, config: dict):
        kwargs = {"api_key": config["OPENAI_API_KEY"]}
        base_url = config.get("OPENAI_BASE_URL")
        if base_url:
            kwargs["base_url"] = base_url
        self.client = OpenAI(**kwargs)
        # self.model = config.get("OPENAI_MODEL", "deepseek-chat")
        self.model = config.get("OPENAI_MODEL")
        # self.request_mode = config.get("REQUEST_MODE", "chat_completions")
        self.request_mode = config.get("REQUEST_MODE")
    def parse_task(self, user_input: str) -> dict:
        if self.request_mode == "responses":
            response = self.client.responses.create(
                model=self.model,
                input=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_input},
                ],
            )
            text = response.output_text.strip()
        else:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_input},
                ],
                temperature=0
            )
            text = response.choices[0].message.content.strip()
        try:
            return json.loads(text)
        except Exception:
            return {
                "action": "error",
                "message": f"模型没有返回合法 JSON: {text}"
            }