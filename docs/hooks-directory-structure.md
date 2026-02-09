# Hooks 目录结构说明

## 概述

CC-Scaffold 使用两种目录结构来管理 hooks 脚本：

1. **开发目录**: `chat-record/hooks/` - 用于开发和维护源码
2. **安装目录**: `.claude/scripts/hooks/chat-record/` - 实际运行时使用的位置

## 目录结构对比

### 开发结构（源码维护）

```
chat-record/
├── hooks/
│   └── session_end_summary.py    # 源码文件
├── skills/
│   └── chat-recorder/
├── commands/
└── README.md
```

### 安装结构（运行时）

```
.claude/
├── scripts/
│   └── hooks/
│       └── chat-record/
│           └── session_end_summary.py    # 实际使用的脚本
├── skills/
│   └── chat-recorder/
├── commands/
└── settings.json
```

## 为什么使用 `.claude/scripts/hooks/`？

### 优点

1. **版本控制友好**: 所有脚本都在 `.claude/` 目录下，便于管理
2. **路径统一**: 与 skills、commands、agents 等保持一致的目录结构
3. **相对路径简单**: 脚本内部可以使用相对路径定位项目根目录
4. **迁移方便**: 整个 `.claude/` 目录可以直接复制到其他项目

### 与 `.claude-hooks/` 的对比

| 特性 | `.claude-hooks/` | `.claude/scripts/hooks/` |
|------|------------------|------------------------|
| 官方支持 | ✅ 旧标准 | ✅ 新标准 |
| 版本控制 | ⚠️ 需要额外配置 | ✅ 自动包含 |
| 路径管理 | ⚠️ 相对路径复杂 | ✅ 路径清晰 |
| 可移植性 | ⚠️ 需要单独复制 | ✅ 整体复制 |

## Hooks 脚本分析

### session_end_summary.py

- **钩子类型**: `Stop`
- **功能**: 会话结束时生成总结和文件修改记录
- **触发时机**: 用户关闭 Claude Code 或结束会话时
- **主要逻辑**:
  1. 读取 `conversation.txt` 获取会话内容
  2. 读取 `modify_logs.txt` 获取文件修改记录
  3. 生成总结并保存到 `session_summary.txt`
  4. 清空 `conversation.txt` 为下次会话做准备

### 路径获取逻辑

脚本使用以下逻辑获取项目根目录：

```python
def get_project_root():
    """获取项目根目录"""
    # 脚本位置: .claude/scripts/hooks/chat-record/session_end_summary.py
    # 需要向上4级到达项目根目录
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent.parent.parent.parent
    return project_root
```

路径说明：
- `session_end_summary.py` 所在目录: `.claude/scripts/hooks/chat-record/`
- 向上1级: `.claude/scripts/hooks/`
- 向上2级: `.claude/scripts/`
- 向上3级: `.claude/`
- 向上4级: `项目根目录/`

## 配置示例

### settings.json 配置

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python39 .claude/scripts/hooks/chat-record/session_end_summary.py",
            "timeout": 10
          }
        ],
        "description": "生成会话总结"
      }
    ]
  }
}
```

## 开发建议

### 添加新 Hook

1. 在 `chat-record/hooks/` 创建源码文件
2. 修改 `get_project_root()` 函数以适应新位置
3. 在安装脚本中添加复制逻辑
4. 更新 `settings.json` 配置
5. 测试 hook 功能

### 调试 Hook

```bash
# 手动测试 hook
python39 .claude/scripts/hooks/chat-record/session_end_summary.py

# 查看输出
echo '{"hook_event_name": "Stop"}' | python39 .claude/scripts/hooks/chat-record/session_end_summary.py
```

## 迁移指南

### 从 `.claude-hooks/` 迁移到 `.claude/scripts/hooks/`

1. **创建新目录**:
   ```bash
   mkdir -p .claude/scripts/hooks/chat-record
   ```

2. **移动脚本**:
   ```bash
   cp .claude-hooks/session_end_summary.py .claude/scripts/hooks/chat-record/
   ```

3. **修改路径获取逻辑**:
   - 更新 `get_project_root()` 函数
   - 确保使用 `Path(__file__).resolve()` 获取绝对路径

4. **更新配置**:
   - 修改 `.claude/settings.json`
   - 将路径从 `.claude-hooks/` 改为 `.claude/scripts/hooks/`

5. **删除旧目录**:
   ```bash
   rm -rf .claude-hooks
   ```

6. **重启 Claude Code**

## 常见问题

### Q: 为什么不使用 `.claude-hooks/`？

A: `.claude-hooks/` 是旧标准，仍然有效但不够灵活。新标准 `.claude/scripts/hooks/` 提供更好的可移植性和版本控制支持。

### Q: 已有的 `.claude-hooks/` 需要删除吗？

A: 建议迁移到新目录后删除，避免混淆和配置错误。

### Q: 如何确保脚本路径正确？

A: 使用 `Path(__file__).resolve()` 获取脚本绝对路径，然后使用 `.parent` 向上导航到项目根目录。

### Q: 多个项目的 hooks 如何管理？

A: 将源码维护在 CC-Scaffold 的功能目录中（如 `chat-record/hooks/`），通过安装脚本复制到目标项目。
