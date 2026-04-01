import json
import subprocess
import os

def read_file(path: str) -> str:
    """读取文件内容"""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
    
def write_file(path: str, content: str) -> None:
    """写入文件内容"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def run_command(cmd: list[str]) -> dict:
    """执行命令并返回结果"""
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

def parse_user_input(user_input: str) -> dict:
    """
    把用户输入转换成任务 dict
    这是一个简化版“意图识别器”
    支持:
    1. read 文件名
    2. write 文件名 内容
    3. cmd 命令
    """
    user_input = user_input.strip()
    if not user_input:
        return {"action": "error", "message": "输入不能为空"}
    parts = user_input.split(" ", 2)
    action = parts[0].lower()
    if action == "read":
        if len(parts) < 2:
            return {"action": "error", "message": "用法: read 文件名"}
        return {
            "action": "read_file",
            "path": parts[1]
        }
    if action == "write":
        if len(parts) < 3:
            return {"action": "error", "message": "用法: write 文件名 内容"}
        return {
            "action": "write_file",
            "path": parts[1],
            "content": parts[2]
        }
    if action == "cmd":
        if len(parts) < 2:
            return {"action": "error", "message": "用法: cmd 命令"}
        cmd_list = parts[1].split()
        if len(parts) == 3:
            cmd_list.append(parts[2])
        return {
            "action": "run_command",
            "cmd": cmd_list
        }
    return {"action": "error", "message": "不支持的命令。支持: read / write / cmd"}


def handle_task(task: dict) -> dict:
    """执行任务"""
    action = task["action"]
    if action == "error":
        return {
            "status": "error",
            "message": task["message"]
        }
    if action == "read_file":
        path = task["path"]
        if not os.path.exists(path):
            return {
                "status": "error",
                "message": f"文件不存在: {path}"
            }
        try:
            content = read_file(path)
            return {
                "status": "success",
                "content": content
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"读取失败: {e}"
            }
    if action == "write_file":
        path = task["path"]
        content = task["content"]
        try:
            write_file(path, content)
            return {
                "status": "success",
                "message": f"写入成功: {path}"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"写入失败: {e}"
            }
    if action == "run_command":
        cmd = task["cmd"]
        result = run_command(cmd)
        return {
            "status": "success" if result["code"] == 0 else 
"error",
            "result": result
        }
    return {
        "status": "error",
        "message": "未知任务类型"
    }


def main() -> None:
    while True:
        print("=== mini Claude Code demo ===")
        print("支持命令:")
        print("  read 文件名")
        print("  write 文件名 内容")
        print("  cmd 命令")
        print("输入 exit 退出")
        print()
        user_input = input("请输入指令> ").strip()
        if user_input.lower() == "exit":
            print("程序结束")
            break
        # 用户输入 -> task dict
        task = parse_user_input(user_input)
        # task dict -> JSON字符串（模拟 AI 输出）
        task_json = json.dumps(task, ensure_ascii=False)
        print("\n[任务 JSON]")
        print(task_json)
        # JSON字符串 -> dict
        parsed_task = json.loads(task_json)
        # 执行任务
        result = handle_task(parsed_task)
        print("\n[执行结果]")
        print(json.dumps(result, ensure_ascii=False, 
indent=2))
        print("-" * 40)            


if __name__ == "__main__":
    main()