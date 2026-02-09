# 迁移脚本使用指南

## 功能概述

`migrate_experience.py` 是一个交互式脚本,用于将 CC-Scaffold 中的 Claude Code 经验快速迁移到新项目。

## 使用方法

### 基本用法

在目标项目目录中运行:

```bash
python /path/to/ccscaffold/scripts/migrate_experience.py
```

或者,如果你已将 CC-Scaffold 克隆到固定位置:

```bash
python ~/ccscaffold/scripts/migrate_experience.py
```

### Python 版本要求

- Python 3.9+ (推荐)
- 或 Python 3.7+

## 功能菜单

### 主菜单

```
==========================================================
              CC-Scaffold 经验迁移工具
==========================================================

1. 按功能维度迁移
2. 按类型维度迁移
3. 查看可用功能
4. 迁移全部
q. 退出
```

#### 1. 按功能维度迁移

推荐方式!选择完整的功能包进行迁移。

**子菜单:**
```
1. 列出所有功能
2. 预览功能
3. 迁移功能
0. 返回主菜单
```

**示例:**
```
请选择: 2

选择要迁移的功能:

1. chat-context-manager - 聊天上下文管理
   自动记录每轮对话的上下文

2. continuous-learning - 持续学习
   自动总结对话并生成 skills

0. 返回主菜单
q. 退出

请选择 (0-2): 1

[预览功能] 聊天上下文管理
描述: 自动记录每轮对话的上下文
类型: skill
...
```

#### 2. 按类型维度迁移

按 skills/agents/hooks 等类型进行批量迁移。

**子菜单:**
```
1. 按类型浏览
2. 迁移所有 skills
3. 迁移所有 agents
4. 迁移所有 hooks
0. 返回主菜单
```

#### 3. 查看可用功能

快速浏览所有可用功能及其描述。

#### 4. 迁移全部

一键迁移所有功能到当前项目。

## 迁移过程

### 迁移时会做什么?

1. **复制文件**
   - Hooks 脚本
   - 技能配置
   - 辅助脚本

2. **创建目录**
   - `.claude/skills/`
   - `.claude/conversations/`
   - 其他必要目录

3. **更新配置**
   - 创建或更新 `.claude/settings.json`
   - 添加 hooks 配置

### 示例输出

```
[信息] 开始迁移功能: 聊天上下文管理
[信息] 目标项目: /path/to/your/project
[成功]   已复制: skills/chat-context-manager/hooks/pre_tool_use.py
[成功]   已复制: skills/chat-context-manager/hooks/post_tool_use.py
[成功]   已复制: skills/chat-context-manager/skill.json
[成功]   已更新: .claude/settings.json

[成功] 功能 '聊天上下文管理' 迁移完成!
[信息] 共迁移 3 个文件
```

## 迁移后的文件结构

迁移完成后,项目目录结构:

```
your-project/
├── .claude/
│   ├── settings.json          # Claude Code 配置
│   ├── conversations/         # 对话记录目录
│   └── skills/                # 技能目录
│       ├── chat-context-manager/
│       │   ├── hooks/
│       │   │   ├── pre_tool_use.py
│       │   │   └── post_tool_use.py
│       │   └── skill.json
│       └── continuous-learning/
│           ├── hooks/
│           │   └── session_end.py
│           ├── scripts/
│           │   └── summarize_conversation.py
│           ├── output/
│           └── skill.json
└── ...
```

## 配置清单 (manifest.json)

迁移脚本使用 `manifest.json` 来管理功能清单。

### 清单结构

```json
{
  "features": {
    "feature-key": {
      "name": "功能名称",
      "description": "功能描述",
      "type": "skill|agent|command",
      "components": {
        "hooks": ["path/to/hook1.py", ...],
        "scripts": ["path/to/script1.py", ...],
        "config": "path/to/config.json",
        "docs": "path/to/docs.md"
      }
    }
  }
}
```

### 添加新功能

1. 在 CC-Scaffold 中创建新功能目录
2. 在 `manifest.json` 中添加配置
3. 运行迁移脚本即可使用新功能

## 常见问题

### 1. 如何只迁移某个功能?

使用"按功能维度迁移" → "迁移功能",选择需要的功能。

### 2. 如何查看功能的详细信息?

使用"按功能维度迁移" → "预览功能"。

### 3. 迁移后如何修改配置?

编辑 `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [...],
    "PostToolUse": [...],
    "SessionEnd": [...]
  }
}
```

### 4. 如何禁用某个功能?

从 `.claude/settings.json` 中删除对应的 hooks 配置,或删除整个功能目录。

### 5. Windows 系统注意事项

- 使用 `python` 而不是 `python3`
- 路径使用正斜杠或反斜杠均可
- 建议使用 Git Bash 或 PowerShell

## 高级用法

### 批量迁移到多个项目

创建一个 shell 脚本:

```bash
#!/bin/bash
# migrate-all.sh

PROJECTS=(
    "/path/to/project1"
    "/path/to/project2"
    "/path/to/project3"
)

for project in "${PROJECTS[@]}"; do
    echo "迁移到: $project"
    cd "$project"
    python ~/ccscaffold/scripts/migrate_experience.py
done
```

### 自定义迁移路径

如果 CC-Scaffold 不在标准位置,设置环境变量:

```bash
export CCSCLAFFOLD_ROOT="/custom/path/to/ccscaffold"
python $CCSCLAFFOLD_ROOT/scripts/migrate_experience.py
```

### 只迁移特定组件

修改 `manifest.json`,只保留需要的组件:

```json
{
  "features": {
    "chat-context-manager": {
      "components": {
        "hooks": [
          "skills/chat-context-manager/hooks/pre_tool_use.py"
        ]
      }
    }
  }
}
```

## 故障排除

### 1. Python 命令未找到

```bash
# 检查 Python 版本
python --version
# 或
python3 --version

# 如果未安装,安装 Python 3.9+
# Windows: https://www.python.org/downloads/
# macOS: brew install python@3.9
# Linux: sudo apt install python3.9
```

### 2. 权限错误

```bash
# 确保有写权限
chmod -R 755 .claude/

# Windows: 以管理员身份运行
```

### 3. 迁移后功能未生效

检查 `.claude/settings.json` 中的路径是否正确:

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "python .claude/skills/chat-context-manager/hooks/pre_tool_use.py"
      }]
    }]
  }
}
```

### 4. 如何回滚迁移?

删除迁移的文件和目录:

```bash
# 删除迁移的功能
rm -rf .claude/skills/chat-context-manager
rm -rf .claude/skills/continuous-learning

# 或恢复 settings.json 的备份
git checkout .claude/settings.json
```

## 最佳实践

1. **版本控制**: 将 `.claude/` 目录纳入 Git 管理
2. **团队协作**: 在项目中提交 `.claude/settings.json`
3. **渐进式迁移**: 先迁移核心功能,再逐步添加其他功能
4. **定期更新**: 从 CC-Scaffold 拉取最新功能

## 下一步

- 查看 [聊天上下文管理](chat-context-manager.md)
- 查看 [持续学习功能](continuous-learning.md)
- 查看 [开发指南](development.md)
