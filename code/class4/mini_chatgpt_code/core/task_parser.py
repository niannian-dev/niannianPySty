from pathlib import Path
from tools.file_tool import read_file, write_file
from tools.shell_tool import run_command
def handle_task(task: dict, workspace_dir: Path) -> dict:
    action = task.get("action")
    if action == "error":
        return {"status": "error", "message": task.get("message", "未知错误")}
    
    if action == "read_file":
        path = task.get("path", "")
        if not path:
            return {"status": "error", "message": "缺少 path"}
        try:
            content = read_file(workspace_dir, path)
            return {"status": "success", "content": content}
        except Exception as e:
            return {"status": "error", "message": f"读取失败: {e}"}
        
    if action == "write_file":
        path = task.get("path", "")
        content = task.get("content", "")
        if not path:
            return {"status": "error", "message": "缺少 path"}
        try:
            write_file(workspace_dir, path, content)
            return {"status": "success", "message": f"写入成功: {path}"}
        except Exception as e:
            return {"status": "error", "message": f"写入失败: {e}"}
    if action == "run_command":
        cmd = task.get("cmd", [])
        if not isinstance(cmd, list) or not cmd:
            return {"status": "error", "message": "cmd 必须是非空列表"}
        result = run_command(workspace_dir, cmd)
        return {"status": "success" if result["code"] == 0 else "error","result": result}
    return {"status": "error", "message": f"未知 action: {action}"}