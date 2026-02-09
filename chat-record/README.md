# 会话记录功能 (Chat Record)

## 功能说明

自动记录 Claude Code 的所有对话上下文,包括用户请求和 Claude 响应,方便后续回顾和持续学习。

### 主要特点

- **单一文件**: 仅维护一份 `conversation.txt` 文件
- **自动记录**: 通过 Hooks 自动捕获所有对话
- **会话总结**: SessionEnd 时自动生成会话总结
- **文件修改记录**: 自动记录文件修改历史
- **手动加载**: 通过命令手动加载上一次会话

### 工作流程

1. **会话进行中**: 所有对话记录到 `conversation.txt`
2. **会话结束时**: 自动生成总结到 `session_summary.txt`
3. **下次会话开始**: 使用 `/loadLastSession` 命令加载上一次会话

## 使用方法

### 前置条件

1. 确保已安装 Claude Code
2. 确保已启用 Hooks 功能
3. 确保有对 `.claude` 目录的写权限

### 基本使用

#### 方法 1: 自动安装(推荐)

使用 CC-Scaffold 的迁移脚本:

```bash
# 在目标项目中运行
python /path/to/ccscaffold/scripts/migrate_experience.py
# 选择 chat-record 功能
```

#### 方法 2: 手动安装

1. **复制文件到项目**:
   ```bash
   # 复制 skills
   cp -r chat-record/skills/chat-recorder .claude/skills/

   # 复制 hooks（推荐使用 .claude/scripts/hooks 目录）
   mkdir -p .claude/scripts/hooks/chat-record
   cp chat-record/hooks/*.py .claude/scripts/hooks/chat-record/

   # 复制 commands
   cp chat-record/commands/*.md .claude/commands/
   ```

2. **配置 settings.json**:

   在项目的 `.claude/settings.json` 中添加:

   ```json
   {
     "hooks": {
       "UserPromptSubmit": [
         {
           "type": "command",
           "command": "python39 .claude/skills/chat-recorder/chat_recorder.py"
         }
       ],
       "PostToolUse": [
         {
           "type": "command",
           "command": "python39 .claude/skills/chat-recorder/chat_recorder.py"
         }
       ],
       "Stop": [
         {
           "type": "command",
           "command": "python39 .claude/skills/chat-recorder/chat_recorder.py"
         },
         {
           "type": "command",
           "command": "python39 .claude/scripts/hooks/chat-record/session_end_summary.py",
           "timeout": 10
         }
       ]
     }
   }
   ```

3. **重启 Claude Code**

### 高级用法

#### 加载上一次会话

使用 `/loadLastSession` 命令加载上一次会话的内容:

```
/loadLastSession
```

该命令会读取并展示:
- 会话总结 (session_summary.txt)
- 会话内容 (conversation.txt)
- 文件修改记录 (modify_logs.txt)

#### 自定义存储位置

修改 hook 脚本中的存储路径:

```python
# 在 chat_recorder.py 中
def get_conversation_file():
    # 修改为自定义路径
    return custom_path / 'conversation.txt'
```

#### 清空会话记录

如果需要清空当前会话记录，删除以下文件:
```bash
rm .claude/conversations/conversation.txt
```

## 配置说明

### 必需配置

无。该功能不需要额外的配置。

### 可选配置

#### 存储目录

默认: `.claude/conversations/`

可通过修改 hook 脚本中的路径函数来自定义。

#### 文件大小限制

默认: 5MB

可通过修改 `chat_recorder.py` 中的 `MAX_FILE_SIZE` 变量来自定义。

#### 记录格式

默认:
- 用户请求: `user> 请求内容`
- Claude 响应: `claude> 响应内容`

可通过修改 hook 脚本中的格式化逻辑来自定义。

### 环境变量

无。

## 依赖关系

- **Claude Code**: 必需,版本 1.0+
- **Python**: 3.9+ (用于 hook 脚本)

## 注意事项

1. **性能影响**: Hooks 会轻微影响性能,但通常可以忽略
2. **存储空间**: 会话记录会占用磁盘空间,达到 5MB 后自动清空
3. **隐私**: 记录包含完整对话内容,注意隐私保护
4. **文件权限**: 确保 `.claude-hooks/` 目录下的脚本有执行权限
5. **路径问题**: Windows 路径使用 `\\` 或原始字符串 `r"path"`

## 目录结构

```
chat-record/
├── skills/
│   └── chat-recorder/          # 会话记录技能
│       ├── chat_recorder.py    # 主脚本
│       ├── chat_recorder_debug.py  # 调试脚本
│       └── deploy.py           # 部署脚本
├── hooks/                      # Hooks 脚本源码（开发维护）
│   └── session_end_summary.py  # SessionEnd 钩子源码
├── commands/
│   └── loadLastSession.md      # 加载上一次会话命令
├── docs/
│   ├── chat-context-manager.md    # 上下文管理文档
│   ├── chat-context-usage.md      # 使用说明
│   ├── chat-recorder-deployment.md# 部署文档
│   └── chat-recorder-fixes.md     # 修复记录
└── README.md                    # 本文件
```

**注意**: Hooks 脚本在安装时会被复制到项目的 `.claude/scripts/hooks/chat-record/` 目录。

## 文件说明

### conversation.txt

存储当前会话的所有对话内容。每次新会话时保留上次内容，用户可手动清空或使用 `/loadLastSession` 命令加载。

### session_summary.txt

存储所有历史会话的总结。每次会话结束时追加新的总结。

### modify_logs.txt

存储文件修改记录。最多保留 20 条记录。

## 故障排除

### 问题 1: Hook 脚本没有执行

**症状**: 对话没有被记录

**解决方案**:
1. 检查 `.claude/settings.json` 配置是否正确
2. 确认脚本路径是否正确(相对路径)
3. 查看 Claude Code 日志是否有错误信息
4. 确认脚本文件有执行权限

### 问题 2: 记录文件没有生成

**症状**: Hook 执行了但没有文件

**解决方案**:
1. 检查 `.claude/conversations/` 目录是否存在
2. 确认有写权限
3. 运行调试脚本查看错误

### 问题 3: 会话总结没有生成

**症状**: 会话结束时没有生成总结

**解决方案**:
1. 检查 session_end_summary.py 是否在 hooks 配置中
2. 确认 Stop 事件已正确配置
3. 查看错误日志

### 问题 4: /loadLastSession 命令不工作

**症状**: 命令没有响应或报错

**解决方案**:
1. 确认命令文件已复制到 `.claude/commands/`
2. 检查文件格式是否正确
3. 重启 Claude Code

## 相关文档

- [聊天上下文管理详细文档](docs/chat-context-manager.md)
- [使用说明](docs/chat-context-usage.md)
- [部署文档](docs/chat-recorder-deployment.md)
- [修复记录](docs/chat-recorder-fixes.md)

## 更新日志

- v2.0.0 (2025-02-09): 优化版本
  - 仅维护一份 conversation.txt 文件
  - 新增 SessionEnd 钩子自动生成会话总结
  - 整合文件修改记录功能
  - 新增 /loadLastSession 命令
  - 移除时间命名方式
- v1.0.0 (2025-02-09): 初始版本
