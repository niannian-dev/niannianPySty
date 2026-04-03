# GUI 输入提示与命令选择改造计划

## Summary
在现有 GUI 基础上，把“用户不知道该输入什么”这个问题拆成两层解决：

1. 保留当前单行输入框，但改成“可编辑输入框 + 模板辅助”，用户仍可直接输入自然语言。
2. 增加“两层选择”辅助区，先选任务类型，再按任务类型展示可用命令或示例模板，点击后自动填入输入框。
3. 在界面中明确展示当前系统真实支持的能力，而不是让用户猜。

当前通过代码确认的真实能力是：
- 动作类型：`read_file`、`summarize_file`、`write_file`、`run_command`
- 命令白名单：`python`、`dir`、`type`、`findstr`、`ipconfig`、`ping`

## Key Changes
- 在 [gui_app.py](C:/Users/shan/Desktop/python/code/class4/mini_chatgpt_code/gui_app.py) 的输入区加入“输入提示”文案：
  - 占位提示或静态说明，明确支持的自然语言格式，例如“读取 test.txt”“总结 test.txt”“写入 note.txt 内容是 你好”“执行 python --version”
  - 说明路径必须是工作目录内的相对路径，避免用户误输绝对路径
- 在 [gui_app.py](C:/Users/shan/Desktop/python/code/class4/mini_chatgpt_code/gui_app.py) 增加“两层选择”组件：
  - 第一层：任务类型选择框，固定为“读取文件 / 总结文件 / 写入文件 / 执行命令”
  - 第二层：根据第一层动态变化
    - 读取文件：填充示例模板，如“读取 test.txt”
    - 总结文件：填充示例模板，如“总结 test.txt”
    - 写入文件：填充示例模板，如“写入 note.txt 内容是 你好”
    - 执行命令：展示白名单命令选择，如 `python`、`dir`、`type`、`findstr`、`ipconfig`、`ping`
  - 用户点击“填入”或切换项时，将对应模板写入输入框，用户可继续编辑
- 在 [gui_app.py](C:/Users/shan/Desktop/python/code/class4/mini_chatgpt_code/gui_app.py) 增加“可执行能力说明”区域：
  - 简短列出当前支持的 4 类动作
  - 当选择“执行命令”时，附带展示当前白名单命令列表，来源于配置而非硬编码
- 在 [app.py](C:/Users/shan/Desktop/python/code/class4/mini_chatgpt_code/app.py) 的命令行示例基础上统一 GUI 文案，确保 CLI 和 GUI 展示的示例格式一致
- 在 [gui_app.py](C:/Users/shan/Desktop/python/code/class4/mini_chatgpt_code/gui_app.py) 中将选择框数据与配置/实际能力对齐：
  - 任务类型来自当前解析器支持的 action 集合
  - 命令列表读取 `config["ALLOWED_COMMANDS"]`
  - 去重并按稳定顺序展示，避免 `ping` 重复出现

## Public Interfaces
- GUI 会新增 2 个用户可见输入接口：
  - 任务类型选择框
  - 二级模板/命令选择框
- 不修改底层任务 JSON 结构，不修改 [core/task_parser.py](C:/Users/shan/Desktop/python/code/class4/mini_chatgpt_code/core/task_parser.py) 和 [tools/shell_tool.py](C:/Users/shan/Desktop/python/code/class4/mini_chatgpt_code/tools/shell_tool.py) 的执行协议
- 输入框仍接受自由文本，保持向后兼容

## Test Plan
- 启动 GUI 后，顶部信息区仍正常显示，新增选择框和提示区不挤压主要输出区
- 默认状态下可看到支持的输入示例，用户不需要读代码就知道可输入什么
- 选择“读取文件 / 总结文件 / 写入文件”时，二级选择显示对应自然语言模板，并能正确填入输入框
- 选择“执行命令”时，二级选择显示白名单命令，且 `ping` 不重复
- 用户在模板填入后继续手动修改内容，点击执行后仍走原有 `parse_task -> handle_task` 流程
- 手动输入旧格式命令时功能不回退
- 当配置中的 `ALLOWED_COMMANDS` 变化时，GUI 中的命令选择自动同步

## Assumptions
- 采用“下拉辅助 + 可编辑输入框”方案，不改成纯表单式交互
- 选择框按“两层选择”实现：先选任务类型，再选模板或命令
- 二级选择的目标是“帮助生成自然语言输入”，不是绕过 LLM 直接构造任务 JSON
- 当前阶段只围绕已确认的 4 类动作做提示，不扩展新的底层能力
