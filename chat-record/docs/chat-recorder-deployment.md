# Chat Recorder 部署指南

## 快速部署

### 方法一：使用部署脚本（推荐）

#### 在目标项目中部署

**方式A：从其他目录部署**

```bash
# 在目标项目中创建临时目录
mkdir -p /path/to/target-project/.claude/skills

# 复制 chat-recorder 目录
cp -r .claude/skills/chat-recorder /path/to/target-project/.claude/skills/

# 进入目标项目目录运行部署
cd /path/to/target-project
python3 .claude/skills/chat-recorder/deploy.py /path/to/target-project
```

**方式B：在chat-recorder目录中部署**（已修复相同文件错误）

```bash
# 如果已经在目标项目的 chat-recorder 目录中
cd /path/to/target-project/.claude/skills/chat-recorder
python3.9 deploy.py /path/to/target-project

# 或者使用相对路径
python3.9 deploy.py ..      # 部署到父目录
python3.9 deploy.py .        # 部署到当前目录所在的项目
```

**部署脚本会自动**：
- 检测源文件和目标文件是否相同（避免复制错误）
- 自动检测系统类型并选择合适的Python命令：
  - Linux/Mac: 优先 `python3.9`，其次 `python3`，最后 `python`
  - Windows: 使用 `python39`
- 复制 `chat_recorder.py` 到目标位置
- 创建或更新 `.claude/settings.json` 配置
- 保留现有的其他 hooks 配置

### 方法二：手动部署

#### 步骤 1：复制文件

将以下文件复制到目标项目：

```
目标项目/
└── .claude/
    ├── skills/
    │   └── chat-recorder/
    │       └── chat_recorder.py
    └── settings.json
```

#### 步骤 2：配置 settings.json

在目标项目的 `.claude/settings.json` 中添加以下配置：

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python39 .claude/skills/chat-recorder/chat_recorder.py"
          }
        ],
        "description": "创建新对话记录文件"
      }
    ],
    "UserPromptSubmit": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python39 .claude/skills/chat-recorder/chat_recorder.py"
          }
        ],
        "description": "记录用户输入"
      }
    ],
    "PostToolUse": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python39 .claude/skills/chat-recorder/chat_recorder.py"
          }
        ],
        "description": "记录AI工具调用"
      }
    ],
    "Stop": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python39 .claude/skills/chat-recorder/chat_recorder.py"
          }
        ],
        "description": "清理空文件，记录结束时间"
      }
    ]
  }
}
```

**注意**：如果目标项目已有 `settings.json`，只需将 `hooks` 部分合并到现有配置中。

## Python 版本配置

部署脚本会自动检测系统类型并选择合适的Python命令：

### 自动检测规则

- **Linux/Mac**：
  1. 优先使用 `python3.9`
  2. 如果不存在，使用 `python3`
  3. 最后尝试 `python`

- **Windows**：
  - 使用 `python39`

### 手动修改

如果需要修改Python命令，编辑 `.claude/settings.json`：

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3.9 .claude/skills/chat-recorder/chat_recorder.py"
          }
        ]
      }
    ]
  }
}
```

常用命令示例：
- Linux/Mac: `python3.9`, `python3`, `python`
- Windows: `python39`, `python`

## 验证部署

1. **检查文件结构**
```bash
ls -la /path/to/target-project/.claude/skills/chat-recorder/
# 应该看到：chat_recorder.py
```

2. **检查配置文件**
```bash
cat /path/to/target-project/.claude/settings.json
# 应该看到 hooks 配置
```

3. **重启 Claude Code**

4. **查看记录文件**
```bash
ls -la /path/to/target-project/.claude/conversations/
# 应该看到 conversation-*.txt 文件
```

## 常见问题

### 1. Python 命令不正确

**症状**：hooks 不执行，出现 "command not found" 错误

**解决**：
- 检查系统 Python 版本：`python --version` 或 `python39 --version`
- 修改 settings.json 中的 command 为正确的 Python 命令

### 2. 权限问题（Linux/Mac）

**症状**：hooks 不执行，出现 "Permission denied" 错误

**解决**：
```bash
chmod +x .claude/skills/chat-recorder/chat_recorder.py
```

### 3. 中文显示乱码

**症状**：记录文件中中文显示为乱码或问号

**解决**：确保使用最新版本的 chat_recorder.py，已内置编码处理

### 4. Hooks 不生效

**检查清单**：
- [ ] settings.json 配置正确
- [ ] Python 命令正确
- [ ] 文件路径正确
- [ ] 已重启 Claude Code
- [ ] 查看 Claude Code 控制台是否有错误信息

## 配置选项

可以在 `chat_recorder.py` 开头修改以下配置：

```python
# 文件大小限制（默认 5MB）
MAX_FILE_SIZE = 5 * 1024 * 1024

# 最多保留的历史文件数量（默认 10 个）
MAX_FILES = 10
```

## 卸载

要从项目中移除 chat_recorder：

1. 删除文件：
```bash
rm -rf .claude/skills/chat-recorder
```

2. 从 `.claude/settings.json` 中移除相关 hooks 配置

3. （可选）删除记录文件：
```bash
rm -rf .claude/conversations
```

## 多项目管理

如果要在多个项目中使用，可以考虑：

### 方案 A：符号链接（Linux/Mac）

```bash
# 将 chat-recorder 放在一个中心位置
mkdir -p ~/.claude-shared/skills
cp -r /path/to/ccscaffold/.claude/skills/chat-recorder ~/.claude-shared/skills/

# 在每个项目中创建符号链接
ln -s ~/.claude-shared/skills/chat-recorder /path/to/project/.claude/skills/chat-recorder
```

### 方案 B：Git Submodule

```bash
# 在每个项目中添加为 submodule
cd /path/to/project
git submodule add https://your-repo/chat-recorder.git .claude/skills/chat-recorder
```

## 更新

当有新版本时：

1. 备份当前配置
2. 替换 `chat_recorder.py`
3. 更新 settings.json（如果需要）
4. 重启 Claude Code

## 技术支持

如遇到问题，请检查：
1. `.claude/conversations/` 目录是否创建
2. Claude Code 控制台的错误信息
3. Python 脚本是否能独立运行
