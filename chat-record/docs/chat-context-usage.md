# 会话记录功能使用指南

## ✅ 安装状态

已安装并配置完成！功能会在下次 Claude Code 执行工具时自动开始工作。

## 🎯 工作原理

### 自动触发时机

会话记录功能通过 **Hooks** 自动工作，无需手动启动：

```
你的请求
  ↓
[PreToolUse Hook] → 记录: user> 你的请求内容
  ↓
Claude 执行工具 (Read/Write/Bash/...)
  ↓
[PostToolUse Hook] → 记录: Claude> 执行结果
  ↓
保存到 .claude/conversations/conversation-YYYYMMDDHHMM.lib
```

### 记录内容示例

```
2025-02-09 11:30:15 user> 请帮我创建一个 Python 文件
2025-02-09 11:30:16 Claude> [写入文件] main.py
2025-02-09 11:30:17 user> 再添加一个测试文件
2025-02-09 11:30:18 Claude> [写入文件] test_main.py
2025-02-09 11:30:19 Claude> [读取文件] README.md
```

## 📂 文件位置

记录保存在：`.claude/conversations/conversation-YYYYMMDDHHMM.lib`

每次会话会创建一个新的记录文件，文件名包含时间戳。

## 🔍 查看记录

### 查看所有记录文件

```bash
# 列出所有对话记录
ls -lh .claude/conversations/

# 按时间排序查看
ls -lt .claude/conversations/*.lib
```

### 查看最新的记录

```bash
# 查看最新的对话记录文件
cat .claude/conversations/conversation-*.lib

# 查看最后 20 行
tail -20 .claude/conversations/conversation-*.lib

# 实时监控（新会话开始后）
tail -f .claude/conversations/conversation-*.lib
```

### 搜索特定内容

```bash
# 搜索包含某个关键词的对话
grep "关键词" .claude/conversations/conversation-*.lib

# 搜索所有用户请求
grep "user>" .claude/conversations/conversation-*.lib

# 搜索所有 Claude 响应
grep "Claude>" .claude/conversations/conversation-*.lib
```

## 🛠️ 测试功能

### 方法 1: 继续当前对话

**最简单！** 只要继续使用 Claude Code，记录会自动生成。

例如：
- 请 Claude 创建一个文件
- 请 Claude 读取文件
- 请 Claude 执行命令

每个操作都会被记录！

### 方法 2: 手动测试 Hook

如果你想立即测试，可以手动运行 Hook 脚本：

```bash
# 测试 PreToolUse Hook
echo '{"hook_type":"PreToolUse","tool_name":"Bash","tool_input":{"command":"echo test"},"prompt":"测试请求"}' | python .claude/skills/chat-context-manager/hooks/pre_tool_use.py

# 测试 PostToolUse Hook
echo '{"hook_type":"PostToolUse","tool_name":"Bash","tool_output":{"output":"test output"}}' | python .claude/skills/chat-context-manager/hooks/post_tool_use.py
```

然后查看生成的记录：

```bash
cat .claude/conversations/conversation-*.lib
```

## 📊 记录格式说明

### 时间戳

每条记录都包含精确的时间戳：

```
2025-02-09 11:30:15 user> 请求内容
^^^^^^^^ ^^^^^^^^
  日期    时间
```

### 用户请求标记

```
user> 你的请求内容
```
- 记录你发送给 Claude 的消息
- 或从工具输入中提取的关键信息

### Claude 响应标记

```
Claude> [操作类型] 详细信息
```

不同工具类型的响应格式：

| 工具 | 记录格式 |
|------|---------|
| Bash | `[命令输出] 输出内容` 或 `[命令执行错误] 错误信息` |
| Read | `[读取文件: 文件路径]` |
| Write | `[编辑文件: 文件路径]` |
| Edit | `[编辑文件: 文件路径]` |
| Grep | `[Grep 操作完成]` |
| Glob | `[Glob 操作完成]` |

## 🔧 配置选项

### 修改存储位置

编辑 `.claude/skills/chat-context-manager/skill.json`：

```json
{
  "configuration": {
    "conversations_dir": ".claude/conversations",
    "file_prefix": "conversation-",
    "file_extension": ".lib",
    "timestamp_format": "%Y-%m-%d %H:%M:%S"
  }
}
```

### 修改时间戳格式

在 Hook 脚本中修改 `timestamp_format`：

```python
# 原格式: 2025-02-09 11:30:15
# 可改为: 2025/02/09 11:30:15
timestamp = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
```

## 🎨 高级用法

### 统计对话数量

```bash
# 统计用户请求数
grep -c "user>" .claude/conversations/conversation-*.lib

# 统计 Claude 响应数
grep -c "Claude>" .claude/conversations/conversation-*.lib
```

### 提取特定时间段

```bash
# 提取今天的对话
grep "2025-02-09" .claude/conversations/conversation-*.lib

# 提取特定时间段的对话
grep "11:3[0-9]" .claude/conversations/conversation-*.lib
```

### 导出对话记录

```bash
# 导出为文本文件
cat .claude/conversations/conversation-*.lib > my-conversation.txt

# 导出为 Markdown（添加格式）
sed 's/user> /**user>**/g' .claude/conversations/conversation-*.lib > conversation.md
```

## ⚠️ 注意事项

### 1. 文件大小

- 每个会话创建一个新文件
- 文件会不断增长，建议定期清理旧记录

### 2. 隐私

- 记录保存在本地，不会上传
- 如需删除，直接删除 `.claude/conversations/` 目录

### 3. 性能

- Hooks 是异步的，不会影响响应速度
- 记录操作非常快速

## 🐛 故障排除

### 问题 1: 没有生成记录文件

**可能原因：**
- Hook 还没有被触发（需要实际使用工具）
- Python 路径不正确

**解决方法：**
```bash
# 检查 Python 是否可用
python --version

# 测试 Hook
echo '{}' | python .claude/skills/chat-context-manager/hooks/pre_tool_use.py
```

### 问题 2: Hook 报错

**查看错误信息：**
```bash
# 手动运行 Hook 查看详细错误
echo '{}' | python .claude/skills/chat-context-manager/hooks/pre_tool_use.py 2>&1
```

**常见错误：**
- 模块导入错误：安装缺失的模块
- 权限错误：确保 `.claude/` 目录可写
- 路径错误：使用绝对路径或相对路径

### 问题 3: Windows 路径问题

如果在 Windows 上遇到路径问题，修改 `.claude/settings.json`：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "command": "python .claude/skills/chat-context-manager/hooks/pre_tool_use.py"
      }
    ]
  }
}
```

使用正斜杠 `/` 或双反斜杠 `\\` 都可以。

## 📚 相关功能

### 持续学习功能

会话记录为持续学习功能提供数据。安装持续学习功能后：

1. 会话结束时自动分析对话
2. 生成 skills 文件
3. 保存可复用的经验

详见：[持续学习功能使用指南](continuous-learning.md)

## 💡 使用技巧

### 1. 定期备份

```bash
# 备份所有对话记录
cp -r .claude/conversations/ ~/.claude-conversations-backup/
```

### 2. 会话分类

```bash
# 为不同项目创建不同的记录目录
mkdir -p .claude/conversations/project-a
mkdir -p .claude/conversations/project-b
```

### 3. 记录分析

```bash
# 查看最常用的命令
grep "Bash" .claude/conversations/*.lib | awk '{print $3}' | sort | uniq -c | sort -rn
```

---

**提示：** 从现在开始，你的每次对话都会被自动记录。继续使用 Claude Code，记录会自动生成！
