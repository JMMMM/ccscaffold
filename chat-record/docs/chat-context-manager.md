# 聊天上下文管理功能

## 功能概述

聊天上下文管理功能通过 Hooks 自动记录每轮对话的内容,包括用户请求和 Claude 响应,方便后续回顾和持续学习。

## 记录格式

对话记录保存在 `.claude/conversations/` 目录下,文件名格式为 `conversation-YYYYMMDDHHMM.lib`。

记录格式:
```
2025-02-09 10:30:15 user> 请帮我创建一个新的 Python 项目
2025-02-09 10:30:16 Claude> [创建目录] mkdir -p myproject/src
2025-02-09 10:30:17 Claude> [写入文件] setup.py
```

## 安装方法

### 方法 1: 手动配置(适用于单个项目)

1. 将 `chat-context-manager` 目录复制到项目的 `.claude/skills/` 目录:

```bash
mkdir -p .claude/skills
cp -r ccscaffold/skills/chat-context-manager .claude/skills/
```

2. 在项目的 `.claude/settings.json` 中添加 hooks 配置:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python3 .claude/skills/chat-context-manager/hooks/pre_tool_use.py"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python3 .claude/skills/chat-context-manager/hooks/post_tool_use.py"
          }
        ]
      }
    ]
  }
}
```

### 方法 2: 使用迁移脚本(推荐)

运行迁移脚本并选择 `chat-context-manager` 功能:

```bash
python ccscaffold/scripts/migrate_experience.py
```

## 工作原理

### PreToolUse 钩子

- **触发时机**: 每次工具调用前
- **记录内容**: 用户请求(`user> 前缀`)
- **数据来源**: hook 数据中的 prompt 或 tool_input

### PostToolUse 钩子

- **触发时机**: 每次工具调用后
- **记录内容**: Claude 响应(`Claude> 前缀`)
- **数据来源**: tool_output,根据不同工具类型提取关键信息

## 支持的工具类型

| 工具 | 记录内容 |
|------|---------|
| Bash | 命令输出或错误信息 |
| Read | 读取的文件路径 |
| Edit/Write | 编辑的文件路径 |
| Grep/Glob | 操作完成状态 |
| AskUserQuestion | 提问内容 |
| 其他 | 通用操作完成状态 |

## 查看对话记录

对话记录保存在纯文本文件中,可以直接查看:

```bash
# 查看最新的对话记录
cat .claude/conversations/conversation-*.lib | tail -20

# 查看所有对话文件
ls -la .claude/conversations/
```

## 配置选项

在 `skill.json` 中可以配置:

- `conversations_dir`: 对话记录目录(默认: `.claude/conversations`)
- `file_prefix`: 文件名前缀(默认: `conversation-`)
- `file_extension`: 文件扩展名(默认: `.lib`)
- `timestamp_format`: 时间戳格式(默认: `%Y-%m-%d %H:%M:%S`)

## 故障排除

### 1. 对话记录未生成

检查 Python 路径是否正确:
```bash
# 确保 python3 可用
which python3
# 或者使用 python
python --version
```

### 2. 权限错误

确保 `.claude/conversations/` 目录有写权限:
```bash
chmod -R 755 .claude/
```

### 3. Windows 系统注意事项

在 Windows 上:
- 使用 `python` 而不是 `python3`
- 路径使用反斜杠或正斜杠均可
- 建议使用 Git Bash 或 WSL 运行脚本

## 与持续学习功能集成

聊天上下文管理功能为持续学习功能提供数据源。持续学习功能会读取这些对话记录,并使用 Claude 进行总结和提炼,自动生成 skills。

详见: [continuous-learning 使用文档](continuous-learning.md)

## 数据隐私

- 对话记录保存在本地项目目录中
- 不会上传到任何远程服务
- 可以随时删除 `.claude/conversations/` 目录清除记录

## 示例

完整的对话记录示例:

```
2025-02-09 10:30:15 user> 请帮我创建一个 Python 项目,包含基本的目录结构
2025-02-09 10:30:16 Claude> [创建目录] mkdir -p src tests docs
2025-02-09 10:30:17 Claude> [写入文件] src/main.py
2025-02-09 10:30:18 Claude> [写入文件] tests/test_main.py
2025-02-09 10:30:19 Claude> [写入文件] README.md
2025-02-09 10:30:20 user> 再帮我添加一个 requirements.txt
2025-02-09 10:30:21 Claude> [写入文件] requirements.txt
```

这些记录可以被持续学习功能读取,总结出"创建 Python 项目标准流程"的 skill。
