#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Summary Skills Command - 持续学习功能

当用户输入 /summary-skills 时:
1. 读取 .claude/conversations/current_session 对应的 conversation-xxx.txt
2. 从上次记录的行数开始读取(避免重复分析)
3. 分析聊天内容中是否出现同一个问题反复修改失败的情况(用户反复要求修复大于等于3次)
4. 根据AI_TOOL_USE的回复，总结出规律和触发点
5. 生成新的 skill 文件并保存到 skills/learns 目录
6. 更新状态文件,记录已处理的行数
"""

import sys
import os
import json
import re
from datetime import datetime
from pathlib import Path


class StateManager:
    """状态管理器 - 跟踪已处理的对话行数"""

    def __init__(self, project_dir):
        self.project_dir = Path(project_dir)
        self.state_file = self.project_dir / 'skills' / 'continuous-learning' / 'state.json'
        self.state = self._load_state()

    def _load_state(self):
        """加载状态文件"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"警告: 无法加载状态文件: {e}")
                return {}

        # 初始化状态
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        return {}

    def get_last_processed_line(self, conversation_file_name):
        """获取指定对话文件上次处理的行数"""
        return self.state.get(conversation_file_name, {}).get('last_line', 0)

    def update_last_processed_line(self, conversation_file_name, line_number, skill_name):
        """
        更新指定对话文件的处理行数

        Args:
            conversation_file_name: 对话文件名
            line_number: 已处理的行数
            skill_name: 生成的 skill 名称
        """
        if conversation_file_name not in self.state:
            self.state[conversation_file_name] = {
                'last_line': line_number,
                'skills_generated': [],
                'first_analyzed': datetime.now().isoformat(),
                'last_analyzed': datetime.now().isoformat()
            }
        else:
            self.state[conversation_file_name]['last_line'] = line_number
            self.state[conversation_file_name]['last_analyzed'] = datetime.now().isoformat()

        # 记录生成的 skill
        if skill_name:
            self.state[conversation_file_name]['skills_generated'].append({
                'name': skill_name,
                'generated_at': datetime.now().isoformat(),
                'processed_line': line_number
            })

        self._save_state()

    def _save_state(self):
        """保存状态到文件"""
        try:
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(self.state, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"警告: 无法保存状态文件: {e}")

    def get_summary(self):
        """获取状态摘要"""
        summary = {
            'total_conversations': len(self.state),
            'total_skills': sum(
                len(conv.get('skills_generated', []))
                for conv in self.state.values()
            )
        }
        return summary


class ConversationAnalyzer:
    """对话分析器"""

    def __init__(self, conversation_file, state_manager):
        self.conversation_file = Path(conversation_file)
        self.state_manager = state_manager
        self.conversation_text = ""
        self.start_line = 0
        self.total_lines = 0
        self.retry_threshold = 3

    def load_conversation(self):
        """加载对话记录,从上次处理的行数开始"""
        if not self.conversation_file.exists():
            print(f"错误: 对话文件不存在: {self.conversation_file}")
            return False

        # 获取上次处理的行数
        conv_name = self.conversation_file.name
        self.start_line = self.state_manager.get_last_processed_line(conv_name)

        with open(self.conversation_file, 'r', encoding='utf-8') as f:
            all_lines = f.readlines()

        self.total_lines = len(all_lines)

        # 从上次处理的行数开始读取
        if self.start_line > 0:
            print(f"从第 {self.start_line} 行开始读取(共 {self.total_lines} 行)")
            self.conversation_text = ''.join(all_lines[self.start_line:])
        else:
            print(f"读取完整对话文件(共 {self.total_lines} 行)")
            self.conversation_text = ''.join(all_lines)

        print(f"已加载对话文件: {self.conversation_file}")

        # 检查是否有新内容
        if self.start_line >= self.total_lines:
            print("没有新的对话内容需要分析")
            return False

        new_lines = self.total_lines - self.start_line
        print(f"新增 {new_lines} 行需要分析")

        return True

    def get_line_number_of_last_user_message(self):
        """获取最后一个用户消息在文件中的行号"""
        if not self.conversation_text:
            return self.start_line

        lines = self.conversation_text.split('\n')
        last_user_line = 0

        for i, line in enumerate(lines):
            if line.strip().startswith('user>'):
                last_user_line = i

        # 返回绝对行号
        return self.start_line + last_user_line + 1

    def analyze_retry_patterns(self):
        """
        分析反复修改的模式

        检测用户反复要求修复同一个问题的情况(>=3次)
        """
        lines = self.conversation_text.split('\n')

        # 提取用户消息和AI响应
        user_messages = []
        ai_responses = []

        current_user_msg = None
        current_ai_response = []
        in_ai_response = False

        for line in lines:
            if line.strip().startswith('user>'):
                # 保存之前的AI响应
                if current_user_msg and current_ai_response:
                    ai_responses.append({
                        'user_msg': current_user_msg,
                        'ai_response': '\n'.join(current_ai_response)
                    })

                current_user_msg = line.split('user>', 1)[1].strip()
                current_ai_response = []
                in_ai_response = False
            elif line.strip().startswith('assistant>') or line.strip().startswith('ai>'):
                in_ai_response = True
                content = line.split('>', 1)[1].strip() if '>' in line else ''
                if content:
                    current_ai_response.append(content)
            elif in_ai_response:
                current_ai_response.append(line)

        # 保存最后一个AI响应
        if current_user_msg and current_ai_response:
            ai_responses.append({
                'user_msg': current_user_msg,
                'ai_response': '\n'.join(current_ai_response)
            })

        # 检测反复修复的模式
        retry_patterns = []

        # 查找包含修复关键词的用户消息
        retry_keywords = [
            r'修复', r'修正', r'解决', r'还是不行', r'还是有问题',
            r'继续', r'再试', r'再次', r'仍然', r'fix', r'error',
            r'失败', r'不正确', r'错误', r'问题'
        ]

        for i, response in enumerate(ai_responses):
            user_msg = response['user_msg']

            # 检查是否包含修复关键词
            is_retry = any(re.search(keyword, user_msg, re.IGNORECASE)
                          for keyword in retry_keywords)

            if is_retry:
                # 查找之前是否有相关的修复尝试
                retry_count = 1
                context_messages = []

                # 向前查找相关的修复尝试
                for j in range(i - 1, max(0, i - 10), -1):
                    prev_user_msg = ai_responses[j]['user_msg']
                    if any(re.search(keyword, prev_user_msg, re.IGNORECASE)
                          for keyword in retry_keywords):
                        retry_count += 1
                        context_messages.insert(0, ai_responses[j])
                    else:
                        break

                # 如果修复次数达到阈值
                if retry_count >= self.retry_threshold:
                    context_messages.append(response)
                    retry_patterns.append({
                        'retry_count': retry_count,
                        'messages': context_messages,
                        'issue_topic': self._extract_issue_topic(user_msg)
                    })

        return retry_patterns

    def _extract_issue_topic(self, message):
        """提取问题主题"""
        # 移除常见的修复关键词,提取核心问题
        clean_msg = re.sub(
            r'(修复|修正|解决|还是|仍然|继续|再次|仍有|还有|请|帮我|能不能)',
            '',
            message,
            flags=re.IGNORECASE
        )
        return clean_msg.strip()[:100]

    def analyze_ai_tool_use(self, retry_pattern):
        """
        分析 AI_TOOL_USE 的回复,总结规律和触发点
        """
        messages = retry_pattern['messages']

        # 分析所有AI响应,查找工具使用模式
        tool_patterns = []

        for msg in messages:
            ai_response = msg['ai_response']

            # 查找工具调用模式
            tool_calls = re.findall(
                r'(\w+)\s*\(.*?\)',
                ai_response,
                re.DOTALL
            )

            # 查找错误模式
            error_patterns = re.findall(
                r'(error|错误|失败|异常|warning)',
                ai_response,
                re.IGNORECASE
            )

            # 查找文件操作模式
            file_operations = re.findall(
                r'(Read|Write|Edit|Grep|Glob)\s*\([^)]+\)',
                ai_response
            )

            if tool_calls or file_operations:
                tool_patterns.append({
                    'tools': tool_calls,
                    'errors': error_patterns,
                    'file_ops': file_operations
                })

        return tool_patterns

    def generate_skill_from_pattern(self, retry_pattern, tool_patterns):
        """
        从反复修复的模式生成 skill

        总结规律和触发点,生成可复用的 skill
        """
        retry_count = retry_pattern['retry_count']
        issue_topic = retry_pattern['issue_topic']

        # 提取第一次和最后一次尝试的内容
        first_attempt = retry_pattern['messages'][0]
        last_attempt = retry_pattern['messages'][-1]

        # 分析成功/失败的规律
        common_tools = set()
        for pattern in tool_patterns:
            for tool in pattern['tools']:
                common_tools.add(tool)

        # 生成 skill 名称
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        skill_name = f"fix-{self._sanitize_topic(issue_topic)}-{timestamp}"

        # 生成 skill 内容
        skill_content = f"""---
name: {skill_name}
description: 自动生成的修复 skill - 针对: {issue_topic[:50]}
version: 1.0.0
tags: [auto-generated, fix-pattern, retry-{retry_count}]
---

# {skill_name}

## 生成时间
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 问题概述

**主题**: {issue_topic}

**检测到的反复修复次数**: {retry_count} 次

## 触发点识别

当用户出现以下情况时,应该参考此 skill:

1. 用户提到: "{issue_topic[:100]}"
2. 用户反复要求修复同一问题(>= {retry_count}次)
3. 关键词: 修复、修正、解决、还是不行、仍然、继续

## 修复规律总结

### 常见问题模式
{self._extract_problem_pattern(retry_pattern)}

### 解决方案模式
{self._extract_solution_pattern(tool_patterns)}

### 使用的工具
{', '.join(common_tools) if common_tools else '未检测到特定工具模式'}

## 修复流程建议

基于历史对话分析,建议按以下步骤处理:

1. **识别问题**: 检查是否为 "{issue_topic[:50]}" 类型问题
2. **初始尝试**: 使用 {', '.join(list(common_tools)[:3]) if common_tools else '标准工具'} 进行诊断
3. **迭代修复**: 如果第一次尝试失败,根据错误信息调整策略
4. **验证修复**: 确认修复后进行测试验证

## 对话记录片段

### 第一次尝试
```
用户: {first_attempt['user_msg'][:200]}
```

### 最后一次尝试
```
用户: {last_attempt['user_msg'][:200]}
```

## 学习建议

- 该问题类型需要多轮迭代才能解决
- 可能需要更深入地理解上下文
- 建议在第一次尝试时就进行全面分析

---

*此 skill 由 continuous-learning 功能自动生成*
*基于 {retry_count} 次修复尝试的分析*
"""

        return skill_content, skill_name

    def _sanitize_topic(self, topic):
        """清理主题字符串,用作文件名"""
        # 移除特殊字符,只保留字母、数字、中文和连字符
        sanitized = re.sub(r'[^\w\u4e00-\u9fff-]', '-', topic)
        # 限制长度
        return sanitized[:50]

    def _extract_problem_pattern(self, retry_pattern):
        """提取问题模式"""
        messages = retry_pattern['messages']

        # 分析所有用户消息,提取共同点
        all_user_msgs = [msg['user_msg'] for msg in messages]

        # 提取常见词汇
        common_words = set()
        for msg in all_user_msgs[:3]:  # 只分析前3条
            words = re.findall(r'[\w\u4e00-\u9fff]+', msg)
            common_words.update([w for w in words if len(w) > 1])

        return ', '.join(list(common_words)[:10])

    def _extract_solution_pattern(self, tool_patterns):
        """提取解决方案模式"""
        if not tool_patterns:
            return "未检测到明确的解决方案模式"

        solutions = []

        for pattern in tool_patterns:
            if pattern['file_ops']:
                solutions.append(f"文件操作: {', '.join(pattern['file_ops'][:3])}")
            if pattern['errors']:
                solutions.append(f"错误处理: {', '.join(set(pattern['errors']))}")

        return '\n'.join(solutions) if solutions else "标准修复流程"

    def save_skill(self, skill_content, skill_name):
        """保存 skill 到 skills/learns 目录"""
        learns_dir = Path('skills/learns')
        learns_dir.mkdir(parents=True, exist_ok=True)

        skill_file = learns_dir / f'{skill_name}.md'

        with open(skill_file, 'w', encoding='utf-8') as f:
            f.write(skill_content)

        return skill_file

    def run(self):
        """运行分析流程"""
        print("=" * 60)
        print("Continuous Learning - 对话分析")
        print("=" * 60)

        # 加载对话
        if not self.load_conversation():
            return 0

        # 分析反复修复模式
        retry_patterns = self.analyze_retry_patterns()

        print(f"\n检测到 {len(retry_patterns)} 个反复修复模式")

        if not retry_patterns:
            print("\n未检测到需要总结的反复修复模式")
            print("需要用户反复要求修复同一个问题 >= 3 次才会触发")
            return 0

        # 为每个模式生成 skill
        generated_skills = []

        for i, pattern in enumerate(retry_patterns, 1):
            print(f"\n{'=' * 60}")
            print(f"模式 {i}/{len(retry_patterns)}")
            print(f"{'=' * 60}")
            print(f"问题: {pattern['issue_topic'][:100]}")
            print(f"修复次数: {pattern['retry_count']}")

            # 分析AI工具使用
            tool_patterns = self.analyze_ai_tool_use(pattern)

            # 生成 skill
            skill_content, skill_name = self.generate_skill_from_pattern(
                pattern, tool_patterns
            )

            # 保存 skill
            skill_file = self.save_skill(skill_content, skill_name)
            generated_skills.append((skill_file, skill_name))

            print(f"已生成 skill: {skill_file}")

        # 更新状态记录
        last_processed_line = self.get_line_number_of_last_user_message()
        conv_name = self.conversation_file.name

        # 为每个生成的 skill 更新状态
        for skill_file, skill_name in generated_skills:
            self.state_manager.update_last_processed_line(
                conv_name,
                last_processed_line,
                skill_name
            )

        # 总结
        print(f"\n{'=' * 60}")
        print(f"分析完成! 共生成 {len(generated_skills)} 个 skill")
        print(f"已更新处理位置到第 {last_processed_line} 行")
        print(f"{'=' * 60}")

        for skill_file, _ in generated_skills:
            print(f"  - {skill_file}")

        return 0


def get_current_conversation_file():
    """获取当前会话文件"""
    project_dir = Path.cwd()

    # 读取 .current_session 文件
    current_session_file = project_dir / '.claude' / 'conversations' / '.current_session'

    if not current_session_file.exists():
        print(f"错误: 未找到当前会话文件: {current_session_file}")
        return None

    with open(current_session_file, 'r', encoding='utf-8') as f:
        current_session = f.read().strip()

    # 构建完整路径
    conversation_file = project_dir / '.claude' / 'conversations' / current_session

    return conversation_file


def main():
    """主函数"""
    project_dir = Path.cwd()

    conversation_file = get_current_conversation_file()

    if not conversation_file:
        return 1

    # 初始化状态管理器
    state_manager = StateManager(project_dir)

    # 显示状态摘要
    summary = state_manager.get_summary()
    print(f"\n状态摘要: 已分析 {summary['total_conversations']} 个对话, 生成 {summary['total_skills']} 个 skill\n")

    analyzer = ConversationAnalyzer(conversation_file, state_manager)
    return analyzer.run()


if __name__ == '__main__':
    sys.exit(main())
