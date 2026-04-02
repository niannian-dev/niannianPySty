# Python Project

## 项目简介

这是一个 Python 学习项目，从基础到ai应用。


## 代码文件说明

### code/class1/gpt_python_basics.py

- 变量
- if 条件判断
- for 循环
- 函数定义
- list 列表
- dict 字典
- json 数据处理
- 文件读写
- subprocess 执行外部命令
- pip + 虚拟环境

交互式命令行工具，支持以下命令：
- `read 文件名` - 读取文件内容
- `write 文件名 内容` - 写入文件内容
- `cmd 命令` - 执行外部命令
- 输入 `exit` 退出程序

### code/class2/gpt_python_basics.py
自动化任务执行脚本，演示如何：
- 使用 list 存储一组任务
- 使用 for 循环遍历任务
- dict 与 JSON 字符串互转
- 自动生成带日期的新闻文件
- 执行系统命令并保存结果

### code/class2/app.py
功能与 gpt_python_basics.py 相同，是 class2 的练习代码。

### code/class3/app.py
API 调用示例，从 keyConfig.json 读取配置，使用 OpenAI SDK 调用 DeepSeek API 进行对话。

### code/class3/test.py
完整的 AI 编程助手 demo，功能包括：
- 从 keyConfig.json 加载 API 配置
- 调用 DeepSeek API 将自然语言转换为 JSON 任务
- 支持三种任务类型：
  - `read_file` - 读取文件
  - `write_file` - 写入文件
  - `run_command` - 执行命令
- 交互式命令行界面，用户输入自然语言后自动解析并执行

使用前需要配置 keyConfig.json 文件，格式如下：
```json
{
    "OPENAI_API_KEY": "your-api-key",
    "OPENAI_BASE_URL": "https://api.deepseek.com/v1"
}
```

### code/class4/mini_chatgpt_code
工程化的 AI 编程助手，采用模块化架构：

**目录结构：**
- `core/` - 核心模块
  - `config.py` - 配置加载（从 keyConfig.json 读取 API 配置）
  - `llm.py` - LLM 客户端，支持 chat.completions 和 responses 两种模式
  - `task_parser.py` - 任务解析与执行调度
  - `logger.py` - 日志模块
- `tools/` - 工具模块
  - `file_tool.py` - 文件读写工具（带安全检查，限制 workspace 目录）
  - `shell_tool.py` - 命令执行工具（带危险命令黑名单）
- `workspace/` - 工作目录，存放用户操作的文件
- `logs/` - 日志目录

**主要特性：**
- 支持配置化（API key、base_url、model、request_mode 等）
- 安全的文件操作（限制在 workspace 内）
- 危险命令过滤（禁止 rm、del、shutdown 等）
- 日志记录
- 统一的错误处理

**运行方式：**
```bash
.venv\Scripts\python.exe code\class4\mini_chatgpt_code\app.py
```

**keyConfig.json 配置项：**
```json
{
    "OPENAI_API_KEY": "your-key",
    "OPENAI_BASE_URL": "https://api.deepseek.com/v1",
    "OPENAI_MODEL": "deepseek-chat",
    "REQUEST_MODE": "chat_completions",
    "APP_LOG_LEVEL": "INFO",
    "WORKSPACE_DIR": "workspace"
}
```

## 环境配置

1. 创建虚拟环境：
```bash
python -m venv .venv
```

2. 激活虚拟环境：
```bash
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

## 运行项目

```bash
python main.py
```

###
    
