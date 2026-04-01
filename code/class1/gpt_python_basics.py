'''
这是一个demo用来串联python的基本用法
包含内容
1. 变量
2. if
3. for
4. 函数
5. list
6. dict
7. json
8. 文件读写
9. subprocess
10. pip+env
'''

import json # 导入json模块
import subprocess # 导入subprocess模块,用于执行外部命令
import os # 导入os模块,用于操作操作系统
from datetime import datetime # 导入datetime模块,用于操作日期时间

# 函数：读取文件
def read_file(path):
    with open(path,"r",encoding="utf-8") as f:
        return f.read()
    
# 函数：写入文件
def write_file(path,content):
    with open(path,"w",encoding="utf-8") as f:
        f.write(content)

# 函数：执行外部命令
def run_command(cmd):
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
    )
    return{
        "stdout": result.stdout,
        "stderr": result.stderr,
        "code": result.returncode,
    }
# subprocess.run()函数用于执行外部命令,返回一个CompletedProcess对象
# 函数参数说明：cmd命令字符串,capture_output是否捕获标准输出和错误输出,text是否将输出转换为字符串
# 函数返回值：一个字典,包含标准输出、错误输出和返回码


def get_commend_result(cmd):
        try:
            result = run_command(cmd)["stdout"]
        except subprocess.CalledProcessError as e:
            result = "command failed: " + e.stderr
        return result

# 函数：处理任务
def handle_task(task):
    action = task["action"]

    if action == "write_file":
        path = task["path"]
        content = task["content"]
        write_file(path,content)
        return {"status": "success", "message": f"{path} 写⼊成功"}
   
    elif action == "read_file":
        path = task["path"]
        if not os.path.exists(path):
            return {"status": "error", "message": f"{path} 不存在"}
        content = read_file(path)
        return {"status": "success", "content": content}
    
    elif action == "run_command":
        cmd = task["cmd"]
        result = run_command(cmd)
        return {"status": "success", "result": result}

    else:
        return {"status": "error", "message": "未知操作"}
    

def generate_news(date):
    return f"这是{date}的新闻"

def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")


# 主流程
def main():
    # list: 一组任务
    task_list = [
         {
            "action": "write_file",
            "path": "hello.txt",
            "content": "Hello, mini Claude Code!"
        },
        {
            "action": "read_file",
            "path": "hello.txt"
        },
        {
            "action": "run_command",
            "cmd": ["python", "--version"]
        },{
            "action": "write_file",
            "path": "news"+get_current_date()+".txt",
            "content": generate_news(get_current_date())
        },{
            "action": "read_file",
            "path": "news"+get_current_date()+".txt",
            "content": "成功读取" + get_current_date() + "的新闻"
        },{
            "action": "run_command",
            "cmd": ["ipconfig", "/all"]
        }
        ,{
            "action": "write_file",
            "path": "ipconfig.txt",
            "content": get_commend_result(["ipconfig", "/all"])
        }
    ]

    # for: 遍历任务
    for task in task_list:
        print("\n当前任务:",task)

        # dict -> JSON字符串
        task_json = json.dumps(task,ensure_ascii=False)
        print("JSON字符串:",task_json)

        # JSON字符串 -> dict
        parsed_task = json.loads(task_json)

        try:
            result = handle_task(parsed_task)
            print("处理结果:",result)
        except Exception as e:
            print("处理错误:",e)

if __name__ == "__main__":
    main()
