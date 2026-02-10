# 会话记录功能 (Chat Record)

## 功能说明

自动记录 Claude Code 的所有对话上下文,包括用户请求和 Claude 响应,方便后续回顾和持续学习。

### 主要特点

- **单一文件**: 仅维护一份 `conversation.txt` 文件
- **追加记录**: 持续追加写入，不重置
- **自动记录**: 通过 Hooks 自动捕获所有对话
- **会话总结**: SessionEnd 时自动生成会话总结
- **文件修改记录**: 自动记录文件修改历史
- **手动加载**: 通过命令手动加载上一次会话
- **过滤读命令**: 在 matcher 配置层面过滤 Read、Grep、Glob 等读命令，减少存储压力
- **数量限制**: 保留最近 50 条记录

### 工作流程

1. **会话进行中**: 所有对话持续追加到 `conversation.txt`
2. **自动限制**: 保持最近 50 条记录，超出自动删除旧记录
3. **会话结束时**: 自动生成总结到 `session_summary.txt`
4. **下次使用**: 直接继续使用，历史记录自动保留

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
   cp -r chat-record/skills/chat-record .claude/skills/

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
           "matcher": "*",
           "hooks": [
             {
               "type": "command",
               "command": "python3.9 .claude/skills/chat-record/chat_recorder.py"
             }
           ],
           "description": "记录用户输入"
         }
       ],
       "PostToolUse": [
         {
           "matcher": "^(?!Read|Grep|Glob|WebSearch|WebFetch|TaskOutput|mcp__|4_5v_mcp__|context7|web-reader|zai-mcp-server).*$",
           "hooks": [
             {
               "type": "command",
               "command": "python3.9 .claude/skills/chat-record/chat_recorder.py"
             }
           ],
           "description": "记录AI工具调用（过滤读命令）"
         }
       ],
       "Stop": [
         {
           "matcher": "*",
           "hooks": [
             {
               "type": "command",
               "command": "python3.9 .claude/skills/chat-record/chat_recorder.py"
             },
             {
               "type": "command",
               "command": "python3.9 .claude/scripts/hooks/chat-record/session_end_summary.py",
               "timeout": 10
             },
             {
               "type": "command",
               "command": "python3.9 .claude/scripts/hooks/console-cleaner/clean_console_log.py",
               "timeout": 30
             }
           ],
           "description": "会话结束处理"
         }
       ]
     }
   }
   ```

   **最佳实践**: 在 `PostToolUse` 中使用 `matcher` 正则表达式过滤读命令，而不是在 Python 脚本内部实现过滤。这样可以：
   - 避免不必要的脚本执行
   - 提升系统性能
   - 更符合 Claude Code 的设计理念

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

#### 自定义过滤器（最佳实践）

**推荐方式**: 在 `settings.json` 的 `matcher` 中过滤

使用正则表达式的负向预查来排除不需要记录的工具：

```json
{
  "PostToolUse": [
    {
      "matcher": "^(?!Read|Grep|Glob).*$",
      "hooks": [...]
    }
  ]
}
```

**优势**:
- 配置层面过滤，避免脚本执行
- 更好的性能
- 符合 Claude Code 设计理念

**过滤的常见读命令**:
- `Read` - 读取文件
- `Grep` - 搜索文件内容
- `Glob` - 文件模式匹配
- `WebSearch` - 网页搜索
- `WebFetch` - 网页获取
- `TaskOutput` - 获取任务输出
- `mcp__*` - MCP 服务器工具

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
│   └── chat-record/            # 会话记录技能
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
│   ├── chat-record-deployment.md # 部署文档
│   └── chat-record-fixes.md      # 修复记录
└── README.md                    # 本文件
```

**注意**: Hooks 脚本在安装时会被复制到项目的 `.claude/scripts/hooks/chat-record/` 目录。

## 文件说明

### conversation.txt

持续存储所有对话内容。保留最近 50 条记录，超出自动删除旧记录。无需手动清空，系统自动维护。

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
- [部署文档](docs/chat-record-deployment.md)
- [修复记录](docs/chat-record-fixes.md)

## 更新日志

- v2.2.0 (2025-02-10): 追加记录版本
  - 移除 SessionStart 钩子，不再重置会话文件
  - 改为持续追加写入模式
  - 记录数量限制提升至 50 条
  - 保留最近 50 条对话记录，自动清理旧记录
- v2.1.0 (2025-02-10): 读命令过滤版本
  - 新增读命令过滤功能，自动过滤 Read、Grep、Glob、WebSearch 等读命令
  - 减少 conversation.txt 存储压力
  - **最佳实践**: 在 settings.json 的 matcher 中实现过滤，而非 Python 脚本内部
  - 支持过滤的命令列表：Read、Grep、Glob、WebSearch、WebFetch、Context7 相关工具、TaskOutput 等
- v2.0.0 (2025-02-09): 优化版本
  - 仅维护一份 conversation.txt 文件
  - 新增 SessionEnd 钩子自动生成会话总结
  - 整合文件修改记录功能
  - 新增 /loadLastSession 命令
  - 移除时间命名方式
- v1.0.0 (2025-02-09): 初始版本
