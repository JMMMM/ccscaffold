# CC-Scaffold 用户级别安装说明

## 安装概述

本文档记录了将 CC-Scaffold 组件安装到用户级别 (`~/.claude/`) 的过程和结果。

## 安装目录

```
C:\Users\Xpeng\.claude\
```

## 已安装组件

### 1. chat-record (会话记录)

自动记录每轮对话内容，支持会话总结和历史回顾。

| 类型 | 文件路径 | 说明 |
|------|----------|------|
| skill | `skills/chat-record/chat_recorder.py` | 对话记录核心脚本 |
| hook | `scripts/hooks/chat-record/session_end_summary.py` | 会话结束时生成总结 |
| command | `commands/loadLastSession.md` | `/loadLastSession` 命令 |

### 2. continuous-learning (持续学习)

自动分析对话中反复出现的问题，生成修复 skill。

| 类型 | 文件路径 | 说明 |
|------|----------|------|
| skill | `skills/continuous-learning/` | 持续学习完整模块 (含 9 个脚本) |
| hook | `scripts/hooks/continuous-learning/session_end_continuous_learning.py` | 会话结束自动触发分析 |
| learned | `skills/learn/*.md` | 已学习的经验技能 |

### 3. console-cleaner (控制台清理)

扫描前端代码中的 console.log 并生成清理报告。

| 类型 | 文件路径 | 说明 |
|------|----------|------|
| hook | `scripts/hooks/console-cleaner/clean_console_log.py` | 控制台日志清理脚本 |
| config | `scripts/hooks/console-cleaner/config.json` | 清理配置 |

## Hooks 配置

| Hook 事件 | 触发时机 | 执行内容 |
|-----------|----------|----------|
| SessionStart | 会话开始 | 读取修改历史 (`session_start_reader.py`) |
| UserPromptSubmit | 用户输入 | 记录用户输入 (`chat_recorder.py`) |
| PostToolUse | 工具调用后 | 记录工具调用 + 文件修改 (`chat_recorder.py` + `post_tool_use_logger.py`) |
| Stop | 会话结束 | 记录 + 总结 + 持续学习 + Windows 通知 |
| Notification | 权限/空闲 | Windows 桌面通知 |

## 保留的原有配置

- `env`: API 代理配置 (ANTHROPIC_BASE_URL, API_TIMEOUT_MS 等)
- `permissions`: 危险命令拒绝规则 (git push --force, rm -rf)
- `enabledPlugins`: 5 个已启用插件
- `alwaysThinkingEnabled`: 始终思考模式
- `hooks/windows-notification.ps1`: Windows 桌面通知
- `hooks/post_tool_use_logger.py`: 文件修改记录
- `hooks/session_start_reader.py`: 会话开始读取历史

## 目录结构

```
~/.claude/
  settings.json              # 主配置文件 (已合并)
  settings.json.bak          # 原始备份
  CLAUDE.md                  # 用户全局指令
  skills/
    chat-record/             # 会话记录 skill
    continuous-learning/     # 持续学习 skill (含 scripts/)
    learn/                   # 已学习的经验
    cicd-builder/            # (原有)
  scripts/
    hooks/
      chat-record/           # 会话总结 hook
      continuous-learning/   # 持续学习 hook
      console-cleaner/       # 控制台清理 hook
  hooks/                     # (原有) 独立 hooks
    post_tool_use_logger.py
    session_start_reader.py
    windows-notification.ps1
  commands/
    loadLastSession.md       # 加载上次会话命令
  conversations/             # 对话记录存储
  logs/                      # 修改日志存储
  tmp/                       # 临时文件
```

## 安装脚本

安装脚本位于: `F:\ccscaffold\scripts\install_to_user.py`

重新安装:
```bash
python39 F:\ccscaffold\scripts\install_to_user.py
```

## 使用方法

### 自动功能 (无需操作)

- 每次对话自动记录到 `conversations/conversation.txt`
- 会话结束自动生成总结到 `conversations/session_summary.txt`
- 会话结束自动运行持续学习分析
- 文件修改自动记录到 `logs/modify_logs.txt`

### 手动命令

- `/loadLastSession` - 加载上一次会话的内容和总结

## 注意事项

1. Python 命令使用 `python39`
2. 重启 Claude Code 后生效
3. 原始配置已备份为 `settings.json.bak`
