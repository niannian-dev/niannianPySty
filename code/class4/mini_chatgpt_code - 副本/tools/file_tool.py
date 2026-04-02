from pathlib import Path


def safe_resolve_path(workspace_dir: Path, relative_path: 
str) -> Path:
    """
    只允许访问 workspace_dir 内部的文件
    """
    target = (workspace_dir / relative_path).resolve()
    if workspace_dir.resolve() not in target.parents and target != workspace_dir.resolve():
        raise ValueError(f"禁止访问工作目录之外的路径: {relative_path}")
    return target


def read_file(workspace_dir: Path, relative_path: str) -> str:
    path = safe_resolve_path(workspace_dir, relative_path)
    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {relative_path}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
    

def write_file(workspace_dir: Path, relative_path: str, 
content: str) -> None:
    path = safe_resolve_path(workspace_dir, relative_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)