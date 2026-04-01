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
    
