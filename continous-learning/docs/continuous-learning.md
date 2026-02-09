# 持续学习功能

## 功能概述

持续学习功能在每次会话结束时自动分析对话内容,并生成相应的 skill 文件。这样可以从日常使用中不断积累经验,形成可复用的知识库。

## 工作流程

```
会话结束
  ↓
SessionEnd Hook 触发
  ↓
检查对话记录文件
  ↓
统计对话数量(需要 >= 10条)
  ↓
调用对话总结脚本
  ↓
生成新的 skill 文件
  ↓
保存到 output 目录
```

## 安装方法

### 方法 1: 手动配置

1. 将 `continuous-learning` 目录复制到项目的 `.claude/skills/` 目录:

```bash
mkdir -p .claude/skills
cp -r ccscaffold/skills/continuous-learning .claude/skills/
```

2. 在项目的 `.claude/settings.json` 中添加 hooks 配置:

```json
{
  "hooks": {
    "SessionEnd": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python3 .claude/skills/continuous-learning/hooks/session_end.py"
          }
        ]
      }
    ]
  }
}
```

### 方法 2: 使用迁移脚本(推荐)

```bash
python ccscaffold/scripts/migrate_experience.py
```

## 配置选项

在 `skill.json` 中可以配置:

- `min_conversations`: 最小对话数量(默认: 10)
- `output_dir`: skill 输出目录
- `skill_prefix`: 生成的 skill 文件名前缀

## 使用要求

### 依赖条件

1. **聊天上下文管理功能**
   - 必须先安装 `chat-context-manager` 功能
   - 持续学习依赖其生成的对话记录

2. **Python 环境**
   - Python 3.9+
   - 或 Python 3.7+ (需要测试)

3. **对话数量**
   - 至少 10 条用户请求才会触发总结
   - 可通过配置调整

## 生成的 Skill 格式

生成的 skill 文件包含以下部分:

```markdown
---
name: learned-skill-20250209103015
description: 从对话中学习的技能 - 关键词: python, project, setup
version: 1.0.0
---

# learned-skill-20250209103015

## 学习时间
2025-02-09 10:30:15

## 对话摘要
本次对话包含 15 条用户请求。

### 主要主题
1. 请帮我创建一个新的 Python 项目
2. 需要包含基本的目录结构
3. 添加测试框架
...

## 学习到的模式
(此处应该由 Claude API 分析生成)

## 建议的应用场景
根据对话内容,这个 skill 可能适用于:
1. 创建 Python 项目的场景
2. 相关的代码编写任务
...
```

## 查看生成的 Skills

```bash
# 列出所有生成的 skills
ls -la skills/continuous-learning/output/

# 查看最新的 skill
cat skills/continuous-learning/output/learned-skill-*.md | tail -1

# 统计生成的 skill 数量
ls -1 skills/continuous-learning/output/*.md | wc -l
```

## 应用生成的 Skills

生成的 skill 文件可以:

1. **直接使用**: 复制到 `.claude/skills/` 目录
2. **手动编辑**: 根据需要调整内容
3. **作为参考**: 查看历史模式

```bash
# 应用一个生成的 skill
cp skills/continuous-learning/output/learned-skill-20250209103015.md .claude/skills/
```

## 增强功能(可选)

当前的实现是基础版本,可以通过以下方式增强:

### 1. 集成 Claude API

修改 `summarize_conversation.py`,调用 Claude API 进行智能总结:

```python
import anthropic

client = anthropic.Anthropic(api_key="your-api-key")

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": f"请总结以下对话内容并生成一个 skill:\n\n{conversation}"
    }]
)
```

### 2. 自动应用生成的 Skills

在 `session_end.py` 中添加自动复制逻辑:

```python
# 自动复制到 skills 目录
if skill_file:
    skills_dir = Path('.claude/skills')
    shutil.copy(skill_file, skills_dir / skill_file.name)
```

### 3. Skill 去重

避免生成重复的 skills:

```python
# 检查是否已存在相似 skill
existing_skills = get_existing_skills()
if is_similar(new_skill, existing_skills):
    update_existing_skill(new_skill)
```

## 故障排除

### 1. Hook 未触发

检查 `.claude/settings.json` 中的路径是否正确:

```json
{
  "hooks": {
    "SessionEnd": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "python3 /absolute/path/to/skills/continuous-learning/hooks/session_end.py"
      }]
    }]
  }
}
```

### 2. 对话数量不足

确保有足够的对话记录:

```bash
# 查看对话数量
grep -c "user>" .claude/conversations/conversation-*.lib
```

### 3. 权限问题

确保输出目录有写权限:

```bash
chmod -R 755 skills/continuous-learning/output/
```

## 与聊天上下文管理功能的配合

持续学习功能依赖聊天上下文管理功能:

1. `chat-context-manager` 记录对话
2. `continuous-learning` 读取并总结这些记录
3. 生成新的 skills

建议同时安装这两个功能以获得最佳效果。

## 示例

### 完整工作流程示例

```
# 1. 用户开始一个新的 Claude Code 会话
# 2. 进行多轮对话(超过10条)
user> 帮我创建一个 Flask 项目
Claude> [创建目录] mkdir -p flask-project/src
user> 添加数据库支持
Claude> [编辑文件] flask-project/src/database.py
... (更多对话)

# 3. 用户结束会话(exit)
# 4. SessionEnd Hook 自动触发
# 5. 系统检测到有 15 条对话
# 6. 调用总结脚本分析对话
# 7. 生成 skill 文件: learned-skill-20250209103015.md
# 8. 输出: [SessionEnd] 对话总结完成
```

## 数据流向

```
.claude/conversations/conversation-202502091030.lib
  ↓
continuous-learning/hooks/session_end.py
  ↓
continuous-learning/scripts/summarize_conversation.py
  ↓
continuous-learning/output/learned-skill-20250209103015.md
  ↓
(可选) .claude/skills/
```

## 下一步

- 查看 [migrate-script 使用文档](migrate-script.md) 了解如何安装此功能
- 查看 [chat-context-manager 文档](chat-context-manager.md) 了解数据来源
