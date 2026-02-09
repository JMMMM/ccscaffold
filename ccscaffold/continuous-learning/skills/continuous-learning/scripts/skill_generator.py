#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skill Generator for Continuous Learning

技能生成器 - 使用 Claude -p 生成学习技能
"""

import subprocess
import json
import tempfile
from pathlib import Path
from typing import Optional, List
from datetime import datetime

from models import IssuePattern, LearnedSkill


class SkillGenerator:
    """技能生成器"""

    def __init__(self, skills_output_dir: Path):
        self.skills_output_dir = Path(skills_output_dir)

    def generate(self, pattern: IssuePattern, conversation_snippets: List[str]) -> Optional[LearnedSkill]:
        """使用 claude -p 生成学习技能

        Args:
            pattern: 检测到的问题模式
            conversation_snippets: 对话片段列表

        Returns:
            生成的学习技能，如果生成失败则返回 None
        """
        print(f"\n正在使用 Claude AI 生成技能: {pattern.topic}")

        # 构建提示词
        prompt = self._build_claude_prompt(pattern, conversation_snippets)

        # 检查现有技能
        existing_skills = self._find_existing_skills(pattern)

        # 调用 claude -p
        skill_content = self._call_claude_api(prompt)

        if not skill_content:
            print("Claude API 返回空内容，生成失败")
            return None

        # 从生成的内容中提取技能名称（从 YAML frontmatter）
        skill_name = self._extract_skill_name_from_content(skill_content)

        # 创建技能对象
        skill = LearnedSkill(
            name=skill_name,
            description=f"自动生成的修复技能 - {pattern.topic}",
            issue_topic=pattern.topic,
            retry_count=pattern.occurrences,
            generated_at=datetime.now().isoformat(),
            content=skill_content
        )

        print(f"技能生成成功: {skill.name}")
        return skill

    def _build_claude_prompt(self, pattern: IssuePattern, conversation_snippets: List[str]) -> str:
        """构建 Claude 提示词"""
        # 构建对话内容
        if conversation_snippets:
            conversation_text = "\n\n".join([f"### 对话片段 {i+1}\n{snippet}" for i, snippet in enumerate(conversation_snippets)])
        else:
            conversation_text = "（无对话片段）"

        prompt = f"""# 角色设定
你是一个具备持续学习能力的 AI 助手，专门分析 Claude Code 对话记录，从反复出现的错误中学习并生成修复技能。

# 任务目标
分析提供的对话片段，识别反复出现的问题（用户反复要求修复 ≥{pattern.occurrences} 次），生成一个结构化的技能文件。

# 输入信息

## 问题主题
{pattern.topic}

## 反复次数
{pattern.occurrences} 次

## 关键词
{', '.join(list(pattern.keywords)[:10]) if pattern.keywords else '无'}

## 对话片段（按时间顺序）
{conversation_text}

# 输出要求

## 1. 直接输出 Markdown 内容
**重要**: 直接输出 Markdown 格式的技能文件内容，**不要使用任何代码块包裹**（不要用 ```markdown ... ```）

## 2. 技能文件结构（必须严格遵守）

**第一部分：YAML Frontmatter（必须，放在最开始）**
```yaml
---
name: fix-简洁英文名
description: 自动生成的修复技能 - {pattern.topic}
version: 1.0.0
tags: [auto-generated, fix-pattern, retry-{pattern.occurrences}]
generated_at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
---
```

**第二部分：技能内容（Markdown 格式）**
```markdown
# {self._generate_skill_title(pattern.topic)}

## 生成时间
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 问题概述
**主题**: {pattern.topic}
**反复次数**: {pattern.occurrences} 次修复尝试

## 触发点识别
当用户提到以下情况时参考此技能：
[列出 3-5 个触发关键词或场景]

## 问题分析
[深入分析问题的根本原因，基于对话内容]

## 修复规律总结
[从对话中提取的修复模式和方法]

## 修复流程建议
[分步骤的修复流程]

## 最佳实践
[列出关键实践要点]

## 避免陷阱
[常见的错误做法和如何避免]

## 对话记录参考
### 首次报告
[从对话片段1中提取]

### 中间尝试
[从中间对话片段中提取]

### 最终状态
[从最后对话片段中提取]

---
*此技能由 Continuous Learning 自动生成*

## 3. 内容要求
- **基于实际对话**: 所有分析必须基于提供的对话片段，不编造信息
- **可操作性**: 提供具体的步骤和方法
- **通用性**: 提炼可复用的规律，而非针对单一案例
- **结构化**: 使用清晰的标题和列表

## 4. 分析重点
1. **根因分析**: 为什么这个问题反复出现？
2. **模式识别**: 哪些修复方法有效？哪些无效？
3. **知识提炼**: 可以总结出什么通用原则？
4. **预防措施**: 如何避免类似问题？

## 5. 输出要求（重要）
- **必须从 YAML frontmatter 开始**，格式如下：
  ```yaml
  ---
  name: fix-简洁英文名
  description: ...
  version: 1.0.0
  tags: [...]
  generated_at: ...
  ---
  ```
- **英文名称示例**：`fix-session-summary`、`fix-weekend-display`、`fix-api-error`
- **不要使用代码块包裹整个输出**
- **直接输出完整的技能文件内容**

请开始生成技能文件（必须包含 YAML frontmatter）：
"""

        return prompt

    def _find_existing_skills(self, pattern: IssuePattern) -> List[Path]:
        """查找现有的相关技能"""
        if not self.skills_output_dir.exists():
            return []

        existing = []
        topic_keywords = self._extract_topic_keywords(pattern.topic)

        for skill_file in self.skills_output_dir.glob("*.md"):
            try:
                content = skill_file.read_text(encoding='utf-8')
                # 检查是否包含相关关键词
                if any(kw in content for kw in topic_keywords):
                    existing.append(skill_file)
            except Exception:
                continue

        return existing

    def _extract_topic_keywords(self, topic: str) -> List[str]:
        """从主题中提取关键词"""
        import re
        # 提取中文词汇
        chinese_words = re.findall(r'[\u4e00-\u9fff]{2,}', topic)
        return chinese_words[:5] if chinese_words else [topic[:10]]

    def _call_claude_api(self, prompt: str) -> Optional[str]:
        """调用 claude -p API"""
        try:
            # 使用管道直接传递提示词
            result = subprocess.run(
                ['claude', '-p', '-'],
                input=prompt,
                capture_output=True,
                text=True,
                timeout=120  # 2 分钟超时
            )

            if result.returncode == 0:
                output = result.stdout.strip()
                if output:
                    print(f"Claude API 返回 {len(output)} 字符")

                    # 去除可能的 markdown 代码块包装
                    output = self._unwrap_markdown_code_block(output)

                    return output
                else:
                    print("Claude API 返回空内容")
                    if result.stderr:
                        print(f"stderr: {result.stderr}")
                    return None
            else:
                print(f"Claude API 调用失败 (返回码 {result.returncode})")
                if result.stderr:
                    print(f"stderr: {result.stderr}")
                return None

        except subprocess.TimeoutExpired:
            print("错误: Claude API 调用超时")
            return None
        except FileNotFoundError:
            print("错误: 未找到 claude 命令，请确保 Claude Code CLI 已安装")
            return None
        except Exception as e:
            print(f"错误: Claude API 调用失败: {e}")
            return None

    def _unwrap_markdown_code_block(self, content: str) -> str:
        """去除 markdown 代码块包装"""
        import re

        # 匹配 ```markdown ... ``` 或 ``` ... ```
        pattern = r'^```(?:markdown)?\s*\n(.*?)\n```$'
        match = re.match(pattern, content, re.DOTALL)

        if match:
            return match.group(1).strip()

        return content

    def _extract_skill_name_from_content(self, content: str) -> str:
        """从生成的技能内容中提取 name 字段"""
        import re

        # 从 YAML frontmatter 中提取 name
        match = re.search(r'^name:\s*(.+?)\s*$', content, re.MULTILINE)
        if match:
            name = match.group(1).strip()
            # 移除可能的 .md 后缀（统一处理）
            if name.endswith('.md'):
                name = name[:-3]
            # 确保没有 .md 后缀
            return name

        # 如果没有找到 name，使用默认名称
        return f"fix-issue-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    def _generate_skill_title(self, topic: str) -> str:
        """生成技能标题"""
        # 提取核心问题作为标题
        if len(topic) > 50:
            return topic[:50] + "..."
        return topic

    def _sanitize_topic(self, topic: str) -> str:
        """清理主题字符串，用作文件名"""
        import re
        # 只保留字母、数字、中文和连字符
        sanitized = re.sub(r'[^\w\u4e00-\u9fff-]', '-', topic)
        # 移除连续的连字符
        sanitized = re.sub(r'-+', '-', sanitized)
        # 移除首尾连字符
        sanitized = sanitized.strip('-')
        return sanitized[:50]
        """生成技能内容（简化版本）"""
        generated_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 提取问题模式
        problem_pattern = self._extract_problem_pattern(pattern)
        solution_pattern = self._extract_solution_pattern(pattern)
        tools_used = self._extract_tools_used(context)

        # 提取对话片段
        first_attempt = self._get_first_attempt(pattern, context)
        last_attempt = self._get_last_attempt(pattern, context)

        # 提取关键词
        keywords = ', '.join(list(pattern.keywords)[:10]) if pattern.keywords else "问题, 修复"

        return build_skill_content(
            skill_name="fix-" + self._sanitize_topic(pattern.topic),
            issue_topic=pattern.topic,
            retry_count=pattern.occurrences,
            generated_time=generated_time,
            problem_pattern=problem_pattern,
            solution_pattern=solution_pattern,
            tools_used=tools_used,
            first_attempt=first_attempt,
            last_attempt=last_attempt,
            retry_threshold=self.retry_threshold,
            keywords=keywords
        )

    def _extract_problem_pattern(self, pattern: IssuePattern) -> str:
        """提取问题模式"""
        if pattern.user_messages:
            return pattern.user_messages[0]['content'][:200]
        return pattern.topic

    def _extract_solution_pattern(self, pattern: IssuePattern) -> str:
        """提取解决方案模式"""
        # 基于问题主题提供通用建议
        solutions = {
            "默认": "1. 仔细分析问题根因\n2. 检查相关配置和代码\n3. 采用系统化方法进行修复\n4. 验证修复效果",
            "数据": "1. 检查数据源和数据格式\n2. 验证数据转换逻辑\n3. 确保数据一致性",
            "代码": "1. 阅读相关代码\n2. 理解现有实现\n3. 进行有针对性的修改",
            "配置": "1. 检查配置文件\n2. 验证配置项\n3. 确认配置生效"
        }

        for key, value in solutions.items():
            if key in pattern.topic.lower():
                return value

        return solutions["默认"]

    def _extract_tools_used(self, context: str) -> str:
        """提取使用的工具"""
        tools = []
        if 'Read' in context:
            tools.append('Read')
        if 'Edit' in context:
            tools.append('Edit')
        if 'Write' in context:
            tools.append('Write')
        if 'Bash' in context:
            tools.append('Bash')

        return ', '.join(tools) if tools else '标准工具'

    def _get_first_attempt(self, pattern: IssuePattern, context: str) -> str:
        """获取第一次尝试"""
        if pattern.user_messages:
            return pattern.user_messages[0]['content']
        return "未找到首次尝试记录"

    def _get_last_attempt(self, pattern: IssuePattern, context: str) -> str:
        """获取最后一次尝试"""
        if pattern.user_messages:
            return pattern.user_messages[-1]['content']
        return "未找到最后尝试记录"

    def _sanitize_topic(self, topic: str) -> str:
        """清理主题字符串"""
        import re
        sanitized = re.sub(r'[^\w\u4e00-\u9fff-]', '-', topic)
        return sanitized[:50]
