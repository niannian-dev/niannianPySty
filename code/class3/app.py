import json
import subprocess
import os
from openai import OpenAI

def load_config():
    with open("code\class3\config.json", "r", encoding="utf-8") as f:
        return json.load(f)

config = load_config()

client = OpenAI(
    api_key=config["OPENAI_API_KEY"],
    base_url=config["OPENAI_BASE_URL"]
)    

def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path: str, content: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def run_command(cmd: list[str]) -> dict:
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=15
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "code": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            "stdout": "",
            "stderr": "命令执行超时",
            "code": -1
        }
    except Exception as e:
        return {
            "stdout": "",
            "stderr": f"命令执行异常: {e}",
            "code": -1
        }


# def call_chatgpt(user_input: str) -> dict:
#     """
#     让 ChatGPT 把自然语言转换成 JSON 任务
#     """
#     system_prompt = """
# 你是一个代码助手。你必须把用户输入转换成 JSON。
# 只允许输出一个 JSON 对象，不要输出解释，不要输出 markdown。

# 你只能返回以下三种 action：
# 1. read_file
# 2. write_file
# 3. run_command

# JSON 格式示例：
# {"action":"read_file","path":"app.py"}
# {"action":"write_file","path":"note.txt","content":"hello"}
# {"action":"run_command","cmd":["python","--version"]}

# 规则：
# - 如果用户想看某个文件内容，用 read_file
# - 如果用户想写文件，用 write_file
# - 如果用户想执行命令，用 run_command
# - cmd 必须是字符串数组
# - 如果无法理解，就返回：
#   {"action":"error","message":"无法理解用户意图"}
# """

#     response = client.responses.create(
#         model="deepseek-chat",
#         input=[
#             {
#                 "role": "system",
#                 "content": system_prompt,
#             },
#             {
#                 "role": "user",
#                 "content": user_input,
#             },
#         ],
#         reasoning={"effort": "low"},
#     )

#     text = response.output_text.strip()

#     try:
#         return json.loads(text)
#     except Exception:
#         return {
#             "action": "error",
#             "message": f"模型没有返回合法 JSON: {text}"
#         }

def call_chatgpt(user_input: str) -> dict:
    system_prompt = """
你是一个代码助手。你必须把用户输入转换成 JSON。
只允许输出一个 JSON 对象，不要输出解释，不要输出 markdown。

你只能返回以下三种 action：
1. read_file
2. write_file
3. run_command

JSON 格式示例：
{"action":"read_file","path":"app.py"}
{"action":"write_file","path":"note.txt","content":"hello"}
{"action":"run_command","cmd":["python","--version"]}

规则：
- 如果用户想看某个文件内容，用 read_file
- 如果用户想写文件，用 write_file
- 如果用户想执行命令，用 run_command
- cmd 必须是字符串数组
- 如果无法理解，就返回：
  {"action":"error","message":"无法理解用户意图"}
"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
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


def handle_task(task: dict) -> dict:
    action = task.get("action")

    if action == "error":
        return {
            "status": "error",
            "message": task.get("message", "未知错误")
        }

    if action == "read_file":
        path = task.get("path", "")
        if not path:
            return {"status": "error", "message": "缺少 path"}

        if not os.path.exists(path):
            return {"status": "error", "message": f"文件不存在: {path}"}

        try:
            content = read_file(path)
            return {"status": "success", "content": content}
        except Exception as e:
            return {"status": "error", "message": f"读取失败: {e}"}

    if action == "write_file":
        path = task.get("path", "")
        content = task.get("content", "")
        if not path:
            return {"status": "error", "message": "缺少 path"}

        try:
            write_file(path, content)
            return {"status": "success", "message": f"写入成功: {path}"}
        except Exception as e:
            return {"status": "error", "message": f"写入失败: {e}"}

    if action == "run_command":
        cmd = task.get("cmd", [])
        if not isinstance(cmd, list) or not cmd:
            return {"status": "error", "message": "cmd 必须是非空列表"}

        result = run_command(cmd)
        return {
            "status": "success" if result["code"] == 0 else "error",
            "result": result
        }

    return {"status": "error", "message": f"未知 action: {action}"}


def main() -> None:
    print("=== mini ChatGPT Code demo ===")
    print("你可以直接输入自然语言，比如：")
    print("  读取 app.py")
    print("  写入 hello.txt 内容是 你好")
    print("  执行 python --version")
    print("输入 exit 退出")
    print()

    while True:
        user_input = input("请输入> ").strip()

        if user_input.lower() == "exit":
            print("程序结束")
            break

        task = call_chatgpt(user_input)

        print("\n[ChatGPT 返回的任务 JSON]")
        print(json.dumps(task, ensure_ascii=False, indent=2))

        result = handle_task(task)

        print("\n[执行结果]")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        print("-" * 50)


if __name__ == "__main__":
    main()