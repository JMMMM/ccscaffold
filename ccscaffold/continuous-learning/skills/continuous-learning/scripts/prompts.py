#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prompt Templates for Continuous Learning

持续学习功能的提示词模板
"""

# Summary prompt template for analyzing conversation and generating skills
SUMMARY_PROMPT_TEMPLATE = """# 角色设定
你是一个具备持续学习能力的 AI 助手。你能够根据用户提供的先前学习总结，以及当前对话内容，更新学习总结，以便在后续对话中保持连续性。

# 内容筛选规则
根据聊天内容，找出多次沟通（大于等于 {retry_threshold} 次）都没有解决的问题。

# 总结任务
1. 总结内容的处理步骤，整理出一套处理问题的流程
2. 根据 Claude Code 的规则生成一个 skill
3. 如果有现成的 skills，就进行更新，扩展功能

# 以下是聊天内容
{conversation_content}

请生成一个学习技能，包含以下部分：
- 问题概述：描述检测到的问题
- 触发点识别：什么情况下应该参考此技能
- 修复规律总结：从对话中提取的规律和解决方案
- 使用建议：如何应用此技能避免重复问题
"""


# Skill file template for generated learned skills
SKILL_TEMPLATE = """---
name: {skill_name}
description: 自动生成的修复技能 - {issue_topic}
version: 1.0.0
tags: [auto-generated, fix-pattern, retry-{retry_count}]
---

# {skill_name}

## 生成时间
{generated_time}

## 问题概述

**主题**: {issue_topic}

**检测到的反复修复次数**: {retry_count} 次

## 触发点识别

当用户出现以下情况时，应该参考此技能：

1. 用户提到: "{issue_topic[:100]}"
2. 用户反复要求修复同一问题 (>= {retry_threshold} 次)
3. 关键词: {keywords}

## 修复规律总结

### 常见问题模式
{problem_pattern}

### 解决方案模式
{solution_pattern}

### 使用的工具
{tools_used}

## 修复流程建议

基于历史对话分析，建议按以下步骤处理：

1. **识别问题**: 检查是否为 "{issue_topic[:50]}" 类型问题
2. **初始尝试**: 使用标准工具进行诊断
3. **迭代修复**: 如果第一次尝试失败，根据错误信息调整策略
4. **验证修复**: 确认修复后进行测试验证

## 对话记录片段

### 第一次尝试
```
{first_attempt}
```

### 最后一次尝试
```
{last_attempt}
```

## 学习建议

- 该问题类型需要多轮迭代才能解决
- 可能需要更深入地理解上下文
- 建议在第一次尝试时就进行全面分析

---

*此技能由 continuous-learning 功能自动生成*
*基于 {retry_count} 次修复尝试的分析*
"""


def build_summary_prompt(conversation_content: str, retry_threshold: int = 3) -> str:
    """构建总结提示词"""
    return SUMMARY_PROMPT_TEMPLATE.format(
        conversation_content=conversation_content,
        retry_threshold=retry_threshold
    )


def build_skill_content(
    skill_name: str,
    issue_topic: str,
    retry_count: int,
    generated_time: str,
    problem_pattern: str,
    solution_pattern: str,
    tools_used: str,
    first_attempt: str,
    last_attempt: str,
    retry_threshold: int = 3,
    keywords: str = "修复, 修正, 解决, 问题"
) -> str:
    """构建技能文件内容"""
    return SKILL_TEMPLATE.format(
        skill_name=skill_name,
        issue_topic=issue_topic,
        retry_count=retry_count,
        generated_time=generated_time,
        problem_pattern=problem_pattern,
        solution_pattern=solution_pattern,
        tools_used=tools_used,
        first_attempt=first_attempt[:500],
        last_attempt=last_attempt[:500],
        retry_threshold=retry_threshold,
        keywords=keywords
    )
