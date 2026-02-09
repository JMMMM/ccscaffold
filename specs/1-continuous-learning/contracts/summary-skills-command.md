# Command Contract: summary-skills

**Feature**: 1-continuous-learning
**Date**: 2026-02-09

## Command Overview

**命令名称**: `/summary-skills`

**描述**: 手动触发持续学习分析，读取对话内容并生成学习技能

**触发方式**: 用户在 Claude Code 对话中输入 `/summary-skills`

---

## Command Definition

**文件路径**: `.claude/commands/summary-skills.md`

```markdown
---
description: 分析当前对话内容,检测反复修改失败的情况并生成修复 skill
---

# 持续学习 - 总结 Skills

## 执行方式

运行以下脚本分析当前对话并生成修复技能：

```bash
python3.9 .claude/skills/continuous-learning/scripts/summary_skills.py
```

## 功能说明

该命令会：

1. **读取对话内容**: 从 `.claude/conversations/conversation.txt` 读取最近 20 条对话
2. **检测反复问题**: 识别沟通次数 ≥ 3 次的未解决问题
3. **生成学习技能**: 使用 Claude API 分析并生成结构化的技能文件
4. **保存技能**: 将生成的技能保存到 `.claude/skills/learn/` 目录
5. **更新状态**: 记录已处理的对话位置，避免重复分析

## 配置选项

### 修改对话数量

编辑配置文件或传递参数：
```bash
python3.9 .claude/skills/continuous-learning/scripts/summary_skills.py --max-conversations 30
```

### 指定对话文件
```bash
python3.9 .claude/skills/continuous-learning/scripts/summary_skills.py --conversation-file /path/to/conversation.txt
```

### 查看帮助
```bash
python3.9 .claude/skills/continuous-learning/scripts/summary_skills.py --help
```

## 输出示例

```
==============================================================
Continuous Learning - 对话分析
==============================================================

读取完整对话文件(共 300 行)
已加载对话文件: .claude/conversations/conversation.txt
新增 20 行需要分析

检测到 1 个反复修复模式

==============================================================
模式 1/1
==============================================================
问题: 数据日历周末显示问题
修复次数: 3

已生成技能: .claude/skills/learn/fix-weekend-display-issue-20260209213000.md

==============================================================
分析完成! 共生成 1 个技能
已更新处理位置到第 300 行
==============================================================
  - .claude/skills/learn/fix-weekend-display-issue-20260209213000.md
```

## 生成的技能格式

生成的技能文件包含以下部分：

```markdown
---
name: fix-weekend-display-issue-20260209213000
description: 自动生成的修复技能 - 数据日历周末显示问题
version: 1.0.0
tags: [auto-generated, fix-pattern, retry-3]
---

# fix-weekend-display-issue

## 生成时间
2026-02-09 21:30:00

## 问题概述

**主题**: 数据日历周末显示问题

**检测到的反复修复次数**: 3 次

## 触发点识别

当用户出现以下情况时，应该参考此技能：

1. 用户提到: "数据日历"、"周末显示"、"交易日"
2. 用户反复要求修复同一问题 (≥ 3 次)
3. 关键词: 周末、星期日、星期六、显示红色、交易日

## 修复规律总结

### 常见问题模式
- 非交易日（周末）错误地显示任务状态
- 交易日判断逻辑的默认值设置不当
- 数据日历组件未正确过滤非交易日

### 解决方案模式
- 修改交易日判断的默认值: 从 `True` 改为 `False`
- 只在明确标记为交易日时才检查任务完成情况
- 在数据日历 API 层面进行交易日过滤

### 使用的工具
- Read, Edit, Grep, Bash

## 修复流程建议

基于历史对话分析，建议按以下步骤处理：

1. **识别问题**: 检查是否为"非交易日显示任务状态"类型问题
2. **初始尝试**: 检查 `dataCalendarBatchApi.py` 中的交易日判断逻辑
3. **根本原因**: 查找 `is_trading = trading_days_map.get(date_str, True)` 中的默认值
4. **修复方案**: 将默认值从 `True` 改为 `False`
5. **验证修复**: 检查周末日期是否正确显示为非交易日

## 对话记录片段

### 第一次尝试
```
用户: 数据日历中，应该仅判断交易日任务是否完成，
但我发现2月1日（星期日），2月7日，2月8日（星期六）都显示了红色
```

### 最后一次尝试
```
用户: 2月1日（星期日）显示红色
  - 2月7日显示红色
  - 2月8日（星期六）显示红色 问题没有得到解决
```

## 学习建议

- 该问题类型需要仔细检查默认值设置
- 使用明确的默认值（False 而非 True）可以避免模糊逻辑
- 在涉及条件判断的地方，默认值应该是"更安全"的选项

---

*此技能由 continuous-learning 功能自动生成*
*基于 3 次修复尝试的分析*
```

## 注意事项

1. **API 调用**: 生成技能需要调用 Claude API，可能需要几秒钟
2. **质量审核**: 生成的技能需要人工审核后才能使用
3. **重复检测**: 系统会跳过已分析的内容，避免重复生成
4. **状态文件**: 首次运行后会创建状态文件，记录分析进度

## 相关文档

- [功能文档](../docs/continuous-learning.md)
- [使用指南](../docs/continuous-learning-usage.md)
- [实现计划](../specs/1-continuous-learning/plan.md)
