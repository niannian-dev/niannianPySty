1.安装openai包失败
pip install openai

# 没有权限，在window PowerShell中执行运行成功

(.venv) (base) PS C:\Users\shan\Desktop\python> pip list
Fatal error in launcher: Unable to create process using '"c:\Users\shan\Desktop\work\??\.venv\Scripts\python.exe"  "C:\Users\shan\Desktop\python\.venv\Scripts\pip.exe" list': ???????????

环境中没有pip，安装
步骤1：
运行指令：python -m pip install pip
步骤2：
python -m pip install --upgrade pip
步骤3：
运行指令"pip list"检查一下

在环境变量中将Python环境配置上去

claude code 解决的，疑问