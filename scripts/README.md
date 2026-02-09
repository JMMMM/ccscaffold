# 组件安装说明

本目录包含 CC-Scaffold 开发的所有组件的安装脚本。

## 快速使用

### 部署功能到目标项目

使用 `/functionUse <目录>` 命令快速部署：

```bash
# 在 Claude Code 中执行
/functionUse /path/to/target/project
```

或者直接运行脚本：

```bash
python scripts/deploy_functions.py /path/to/target/project
```

### 从目标项目移除功能

使用 `/functionRemove <目录>` 命令快速移除：

```bash
# 在 Claude Code 中执行
/functionRemove /path/to/target/project
```

或者直接运行脚本：

```bash
python scripts/remove_functions.py /path/to/target/project
```

## 脚本说明

### deploy_functions.py

将 CC-Scaffold 的所有功能部署到目标项目：

- ✅ 会话记录功能 (chat-record)
- ✅ 会话总结钩子 (session_end_summary)
- ✅ 加载上一次会话命令 (loadLastSession)
- ✅ SpecKit Agent (speckitAgent)
- ✅ 自动配置 settings.json

**用法**:
```bash
python scripts/deploy_functions.py <目标目录>
```

**示例**:
```bash
# 部署到当前目录
python scripts/deploy_functions.py .

# 部署到指定目录
python scripts/deploy_functions.py /path/to/target/project
```

### remove_functions.py

从目标项目中移除 CC-Scaffold 的所有功能：

- 🗑️ 删除所有相关文件和目录
- 🧹 清理 settings.json 配置
- ✨ 保留其他功能配置

**用法**:
```bash
python scripts/remove_functions.py <目标目录>
```

**示例**:
```bash
# 从当前目录移除
python scripts/remove_functions.py .

# 从指定目录移除
python scripts/remove_functions.py /path/to/target/project
```

### install_components.py (旧版)

保留用于向后兼容，建议使用 `deploy_functions.py`。

## 已安装的组件

执行安装脚本后，以下组件将被安装到目标项目：

### 1. 会话记录 (chat-record)

- **位置**: `.claude/skills/chat-recorder/`
- **功能**: 自动记录所有对话内容到 `conversation.txt`
- **特性**:
  - 仅维护一份会话文件
  - 会话结束时自动生成总结
  - 自动记录文件修改历史

### 2. SessionEnd 钩子 (session_end_summary.py)

- **位置**: `.claude/scripts/hooks/chat-record/session_end_summary.py`
- **功能**: 会话结束时生成总结和文件修改记录
- **触发**: Stop 事件

### 3. 加载上一次会话命令 (loadLastSession)

- **位置**: `.claude/commands/loadLastSession.md`
- **功能**: 加载上一次会话的内容和总结
- **使用**: 在 Claude Code 中输入 `/loadLastSession`

### 4. SpecKit Agent (speckitAgent)

- **位置**: `.claude/agents/speckitAgent.md`
- **功能**: 执行 spec-kit 方法论进行系统化功能开发
- **触发**: 当用户明确提到使用 spec-kit 时

## 目录结构说明

CC-Scaffold 采用以下目录结构组织组件：

```
.claude/
├── skills/           # 技能脚本
│   └── chat-recorder/
├── scripts/          # Hooks 和其他脚本（推荐位置）
│   └── hooks/
│       └── chat-record/
│           └── session_end_summary.py
├── commands/         # 斜杠命令
├── agents/           # AI 代理
└── settings.json     # 配置文件
```

**注意**:
- `.claude-hooks/` 是 Claude Code 的**旧标准**，仍被支持但不推荐
- 推荐使用 `.claude/scripts/hooks/` 来维护 hooks 脚本，便于版本控制

## 配置文件

安装脚本会自动更新 `.claude/settings.json`，配置以下 hooks：

- **UserPromptSubmit**: 记录用户输入
- **PostToolUse**: 记录 AI 工具调用
- **Stop**: 生成会话总结

## 注意事项

1. **Python 版本**: 需要 Python 3.9 或更高版本
2. **备份**: 安装前建议备份项目
3. **重启**: 安装完成后需要重启 Claude Code
4. **覆盖**: 安装会覆盖现有的同名文件

## 手动安装

如果需要手动安装，请参考各功能的 README.md：

- [会话记录功能](../chat-record/README.md)
- [SpecKit Agent 功能](../speckitAgent/README.md)

## 卸载

要卸载这些组件，请使用移除脚本：

```bash
python scripts/remove_functions.py /path/to/target/project
```

或手动删除以下文件和目录：

```bash
# 删除 skills
rm -rf .claude/skills/chat-recorder

# 删除 scripts/hooks
rm -rf .claude/scripts/hooks/chat-record

# 删除 commands
rm .claude/commands/loadLastSession.md

# 删除 agent
rm .claude/agents/speckitAgent.md

# 恢复 settings.json（手动编辑）
```

## 故障排除

### 问题 1: Hooks 没有执行

**解决方案**:
1. 检查 `.claude/settings.json` 配置
2. 确认 Python 版本正确
3. 重启 Claude Code

### 问题 2: 命令不工作

**解决方案**:
1. 确认命令文件在 `.claude/commands/` 目录
2. 检查文件格式是否正确
3. 重启 Claude Code

### 问题 3: 旧配置导致错误

**解决方案**:
1. 删除 `.claude-hooks/` 目录（如果存在）
2. 使用新的 `.claude/scripts/hooks/` 路径
3. 更新 settings.json 配置

### 问题 4: 部署/移除失败

**解决方案**:
1. 确认目标目录有写权限
2. 检查路径是否正确
3. 查看错误输出信息

## 更新日志

- v2.1.0 (2025-02-09): 新增功能部署命令
  - 新增 `/functionUse` 命令快速部署
  - 新增 `/functionRemove` 命令快速移除
  - 新增 `deploy_functions.py` 脚本
  - 新增 `remove_functions.py` 脚本
  - 更新 `.gitignore` 排除运行时文件
- v2.0.0 (2025-02-09): 优化版本
  - 整合文件修改记录功能
  - 新增会话总结功能
  - 新增加载上一次会话命令
  - Hooks 迁移到 `.claude/scripts/hooks/` 目录

