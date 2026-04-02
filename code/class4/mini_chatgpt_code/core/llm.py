import json
from openai import OpenAI

TASK_SYSTEM_PROMPT = """
你是一个代码助手。你必须把用户输入转换成 JSON。
只允许输出一个 JSON 对象，不要输出解释，不要输出 markdown。
你只能返回以下四种 action：
1. read_file
2. write_file
3. run_command
4. summarize_file
JSON 格式示例：
{"action":"read_file","path":"test.txt"}
{"action":"write_file","path":"note.txt","content":"hello"}
{"action":"run_command","cmd":["python","--version"]}
{"action":"summarize_file","path":"test.txt"}
规则：
规则：
- path 必须是相对路径，例如 test.txt 或 notes/a.txt
- 如果用户想看某个文件内容，用 read_file
- 如果用户想写文件，用 write_file
- 如果用户想执行命令，用 run_command
- 如果用户想“总结、概括、解释、分析”某个文件，用 summarize_file
- cmd 必须是字符串数组
- 如果无法理解，就返回：
  {"action":"error","message":"无法理c解用户意图"
"""

SUMMARY_SYSTEM_PROMPT = """
你是一个文件分析助手。
用户会给你文件路径和文件内容。
请你用中文完成：
1. 文件在讲什么
2. 关键信息是什么
3. 如果这是代码/配置/文档，有什么值得注意的地方
回答要清晰、简洁。
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



    # def parse_task(self, user_input: str) -> dict:
    #     if self.request_mode == "responses":
    #         response = self.client.responses.create(
    #             model=self.model,
    #             input=[
    #                 {"role": "system", "content": SYSTEM_PROMPT},
    #                 {"role": "user", "content": user_input},
    #             ],
    #         )
    #         text = response.output_text.strip()
    #     else:
    #         response = self.client.chat.completions.create(
    #             model=self.model,
    #             messages=[
    #                 {"role": "system", "content": SYSTEM_PROMPT},
    #                 {"role": "user", "content": user_input},
    #             ],
    #             temperature=0
    #         )
    #         text = response.choices[0].message.content.strip()
    #     try:
    #         return json.loads(text)
    #     except Exception:
    #         return {
    #             "action": "error",
    #             "message": f"模型没有返回合法 JSON: {text}"
    #         }

    def _chat(self, system_prompt: str, user_input: str) -> str:
        if self.request_mode == "responses":
            response = self.client.responses.create(
                model=self.model,
                input=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input},
                ],
            )
            return response.output_text.strip()
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input},
            ],
            temperature=0
        )
        return response.choices[0].message.content.strip()
        
    def parse_task(self, user_input: str) -> dict:
        text = self._chat(TASK_SYSTEM_PROMPT, user_input)
        try:
            return json.loads(text)
        except Exception:
            return {"action": "error","message": f"模型没有返回合法 JSON: {text}"}
             
        
    def summarize_file(self, path: str, content: str) -> str:
        prompt = f"""文件路径：{path}文件内容如下：{content}"""
        return self._chat(SUMMARY_SYSTEM_PROMPT, prompt)