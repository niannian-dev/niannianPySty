import subprocess
from pathlib import Path


BLOCKED_COMMANDS = {"rm", "del", "shutdown", "reboot", "format"}

def run_command(workspace_dir: Path, cmd: list[str]) -> dict:
    if not cmd:
        return {"stdout": "", "stderr": "命令不能为空", "code": -1}
    
    if cmd[0].lower() in BLOCKED_COMMANDS:
        return {
            "stdout": "",
            "stderr": f"危险命令已禁止: {cmd[0]}",
            "code": -1
        }
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=15,
            cwd=str(workspace_dir)
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "code": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {"stdout": "", "stderr": "命令执行超时", "code": -1}
    except Exception as e:
        return {"stdout": "", "stderr": f"命令执行异常: {e}", "code": -1}