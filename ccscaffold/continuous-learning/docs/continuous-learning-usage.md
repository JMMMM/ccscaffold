# Continuous Learning - 使用指南

## 快速开始

### 安装

使用 CC-Scaffold 的迁移脚本或手动复制文件：

```bash
# 复制技能
cp -r ccscaffold/continuous-learning/skills/continuous-learning .claude/skills/

# 复制命令
cp ccscaffold/continuous-learning/commands/summary-skills.md .claude/commands/

# 配置钩子（如果尚未配置）
# 编辑 .claude/settings.json，添加 SessionEnd 钩子配置
```

### 验证安装

```bash
# 检查命令是否可用
python3.9 .claude/skills/continuous-learning/scripts/summary_skills.py --help

# 查看配置
cat .claude/skills/continuous-learning/config.json
```

## 基本使用

### 手动触发

在 Claude Code 对话中输入：

```
/summary-skills
```

系统会：
1. 读取最近 20 条对话
2. 检测反复问题（≥3次）
3. 生成学习技能
4. 保存到 `.claude/skills/learn/` 目录

### 自动触发

会话结束时自动触发，无需手动操作。

### 查看结果

```bash
# 查看生成的技能
ls -la .claude/skills/learn/

# 查看技能内容
cat .claude/skills/learn/*.md
```

## 高级用法

### 自定义对话数量

编辑 `.claude/skills/continuous-learning/config.json`:

```json
{
  "max_conversations": 50
}
```

### 指定对话文件

```bash
python3.9 .claude/skills/continuous-learning/scripts/summary_skills.py --conversation-file /path/to/conversation.txt
```

### 清除状态重新分析

```bash
rm .claude/skills/continuous-learning/state.json
```

## 输出说明

### 生成的技能格式

```markdown
---
name: fix-{issue}-{timestamp}
description: 自动生成的修复技能 - {issue}
version: 1.0.0
tags: [auto-generated, fix-pattern, retry-{count}]
---

# {skill-name}

## 生成时间
{timestamp}

## 问题概述
**主题**: {issue}

## 触发点识别
1. 用户提到: "{topic}"
2. 用户反复要求修复 (≥ {count} 次)
3. 关键词: {keywords}

## 修复规律总结
{patterns}

## 修复流程建议
{suggestions}

## 对话记录片段
{conversation_snippets}
```

### 状态文件

`.claude/skills/continuous-learning/state.json`:

```json
{
  "conversation.txt": {
    "last_line": 150,
    "skills_generated": [
      {
        "name": "fix-weekend-display-issue",
        "generated_at": "2026-02-09T21:30:00",
        "processed_line": 150
      }
    ],
    "first_analyzed": "2026-02-09T21:00:00",
    "last_analyzed": "2026-02-09T21:30:00"
  }
}
```

## 测试指南

### 准备测试数据

```bash
# 使用测试数据验证
cp /path/to/source/.claude/conversations/conversation.txt \
   .claude/conversations/test_conversation.txt
```

### 运行测试

```bash
# 分析测试数据
python3.9 .claude/skills/continuous-learning/scripts/summary_skills.py \
            --conversation-file .claude/conversations/test_conversation.txt \
            --max-conversations 20
```

### 验证结果

```bash
# 检查生成的技能
ls -la .claude/skills/learn/

# 查看技能内容
cat .claude/skills/learn/*.md
```

### 预期结果

使用示例项目的测试数据，应该检测到：
- **问题**: 数据日历周末显示问题
- **原因**: 交易日判断默认值错误
- **解决方案**: 修改默认值从 True 改为 False

## 常见问题

### Q: 如何禁用自动触发？

编辑 `.claude/settings.json`，移除 SessionEnd 钩子配置。

### Q: 如何只分析特定会话？

使用 `--conversation-file` 参数指定对话文件路径。

### Q: 生成的技能如何使用？

技能保存在 `.claude/skills/learn/` 目录，可以手动查看和应用。

### Q: 如何删除生成的技能？

直接删除 `.claude/skills/learn/` 目录下的对应文件。

## 技巧

1. **调整阈值**: 根据项目特点调整 `retry_threshold` 值
2. **定期清理**: 定期检查和删除低质量技能
3. **手动优化**: 人工编辑生成的技能以提高质量
4. **版本控制**: 将生成的技能纳入版本控制

## 相关文档

- [功能文档](continuous-learning.md)
- [实现计划](../../specs/1-continuous-learning/plan.md)
