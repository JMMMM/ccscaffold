# Quickstart Guide: Continuous Learning Refactor

**Feature**: 1-continuous-learning
**Date**: 2026-02-09

## Overview

本功能实现了自动分析 Claude Code 对话内容并生成学习技能的系统。它能够检测反复出现的问题（≥3次沟通未解决），并生成结构化的修复技能。

**核心功能**:
- SessionEnd 钩子自动触发分析
- `/summary-skills` 命令手动触发
- 检测反复问题并生成技能
- 状态跟踪避免重复分析

---

## Installation

### 方法 1: 自动安装（推荐）

```bash
# 使用功能部署命令
/functionUse

# 选择 continuous-learning 功能
```

### 方法 2: 手动安装

```bash
# 1. 复制脚本到 .claude/skills/
cp -r ccscaffold/continuous-learning/skills/continuous-learning .claude/skills/

# 2. 复制命令文件
cp ccscaffold/continuous-learning/commands/summary-skills.md .claude/commands/

# 3. 配置 settings.json 添加钩子
# 编辑 .claude/settings.json，添加：
{
  "hooks": {
    "SessionEnd": [
      {
        "script": ".claude/skills/continuous-learning/scripts/session_end_hook.py",
        "description": "持续学习: 自动分析对话并生成技能"
      }
    ]
  }
}
```

---

## Usage

### 手动触发

在 Claude Code 对话中输入：

```
/summary-skills
```

系统会自动：
1. 读取当前对话文件
2. 检测反复问题
3. 生成学习技能
4. 保存到 `.claude/skills/learn/` 目录

### 自动触发

会话结束时自动触发，无需手动操作。

---

## Testing

### 使用真实数据测试

```bash
# 1. 准备测试数据
mkdir -p .claude/conversations
cp /path/to/source/.claude/conversations/conversation.txt \
   .claude/conversations/test_conversation.txt

# 2. 运行分析脚本
python3.9 .claude/skills/continuous-learning/scripts/summary_skills.py \
            --conversation-file .claude/conversations/test_conversation.txt \
            --max-conversations 20

# 3. 查看生成的技能
ls -la .claude/skills/learn/
cat .claude/skills/learn/*.md
```

### 预期结果

使用示例项目的测试数据，应该检测到：

**问题**: 数据日历周末显示问题
- 用户反复提到周末显示红色的问题
- 具体日期: 2月1日（星期日）、2月7日、2月8日（星期六）
- 沟通次数: ≥3次

**生成的技能应包含**:
- 问题概述: 数据日历在非交易日错误显示任务状态
- 根本原因: 交易日判断默认值错误
- 解决方案: 修改默认值为 False
- 预防措施: 使用明确的默认值

---

## Configuration

### 配置文件位置

`.claude/skills/continuous-learning/config.json`

### 可配置参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `max_conversations` | 20 | 读取的最大对话条数 |
| `retry_threshold` | 3 | 触发技能生成的反复次数阈值 |
| `conversation_file` | `.claude/conversations/conversation.txt` | 对话文件路径 |
| `skills_output_dir` | `.claude/skills/learn` | 技能输出目录 |
| `state_file` | `.claude/skills/continuous-learning/state.json` | 状态文件路径 |

### 配置示例

```json
{
  "max_conversations": 30,
  "retry_threshold": 3,
  "conversation_file": ".claude/conversations/conversation.txt",
  "skills_output_dir": ".claude/skills/learn",
  "state_file": ".claude/skills/continuous-learning/state.json",
  "keywords": {
    "retry": ["修复", "修正", "解决", "还是不行", "还是有问题"],
    "issues": ["问题", "bug", "错误", "失败"]
  }
}
```

---

## Verification

### 检查点

- [ ] 脚本可以正常运行（无错误）
- [ ] 能够从测试数据中检测到"数据日历周末显示"问题
- [ ] 生成的技能文件格式正确
- [ ] 技能文件包含有用信息（问题、原因、解决方案）
- [ ] 状态跟踪正常工作（避免重复分析）
- [ ] 脚本在 60 秒内完成分析

### 调试技巧

```bash
# 查看详细日志
python3.9 .claude/skills/continuous-learning/scripts/summary_skills.py --verbose

# 清除状态重新分析
rm .claude/skills/continuous-learning/state.json
python3.9 .claude/skills/continuous-learning/scripts/summary_skills.py

# 检查对话文件格式
head -20 .claude/conversations/conversation.txt
```

---

## Troubleshooting

### 问题 1: 没有检测到任何问题

**可能原因**:
- 对话内容没有达到反复阈值（< 3次）
- 关键词配置不匹配

**解决方案**:
- 增加 `max_conversations` 值
- 调整 `retry_threshold` 值
- 检查对话内容是否真的有反复问题

### 问题 2: Claude API 调用失败

**可能原因**:
- API 密钥未配置
- 网络连接问题

**解决方案**:
- 检查 Claude Code 配置
- 确认网络连接正常

### 问题 3: 生成的技能质量不好

**可能原因**:
- 对话上下文不足
- 问题模式不够清晰

**解决方案**:
- 增加 `max_conversations` 值
- 人工编辑生成的技能

---

## Next Steps

1. **审核生成的技能**: 查看生成的技能内容，人工审核
2. **调整配置**: 根据实际需求调整配置参数
3. **监控性能**: 观察自动触发的性能影响
4. **持续改进**: 根据使用反馈优化提示词模板

---

## Related Documentation

- [功能文档](../../ccscaffold/continuous-learning/docs/continuous-learning.md)
- [使用指南](../../ccscaffold/continuous-learning/docs/continuous-learning-usage.md)
- [实现计划](./plan.md)
- [数据模型](./data-model.md)
