#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Summary Skills - Core Script for Continuous Learning

持续学习功能的核心脚本 - 分析对话并生成学习技能
"""

import sys
import os
import argparse
from pathlib import Path
from datetime import datetime

# 添加 scripts 目录到 Python 路径
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from models import LearnedSkill, sanitize_topic
from config import get_config, DEFAULT_CONFIG_PATH
from state_manager import StateManager
from conversation_reader import ConversationReader
from issue_analyzer import IssueAnalyzer
from skill_generator import SkillGenerator


def get_project_root() -> Path:
    """获取项目根目录"""
    return Path.cwd()


def get_conversation_file(args) -> Path:
    """获取对话文件路径"""
    if args.conversation_file:
        return Path(args.conversation_file)

    # 从配置文件读取
    config = get_config()
    return get_project_root() / config.conversation_file


def get_python_command() -> str:
    """获取 Python 命令"""
    import subprocess
    for cmd in ['python39', 'python3.9', 'python3', 'python']:
        try:
            result = subprocess.run(
                [cmd, '--version'],
                capture_output=True,
                timeout=5
            )
            if result.returncode == 0:
                return cmd
        except:
            continue
    return 'python3.9'


def main():
    """主函数"""
    project_root = get_project_root()
    python_cmd = get_python_command()

    # 解析命令行参数
    parser = argparse.ArgumentParser(description='持续学习 - 分析对话并生成技能')
    parser.add_argument('--conversation-file', type=str, help='对话文件路径')
    parser.add_argument('--max-conversations', type=int, help='读取的最大对话条数')
    parser.add_argument('--config', type=str, help='配置文件路径')

    args = parser.parse_args()

    # 加载配置
    config_file = Path(args.config) if args.config else DEFAULT_CONFIG_PATH
    config = get_config(config_file)
    config = config.from_args(vars(args))

    # 获取对话文件
    conversation_file = get_conversation_file(args)
    print(f"对话文件: {conversation_file}")

    # 初始化状态管理器
    state_file = project_root / config.state_file
    state_manager = StateManager(state_file)

    # 显示状态摘要
    summary = state_manager.get_summary()
    print(f"\n状态摘要: 已分析 {summary['total_conversations']} 个对话, "
          f"生成 {summary['total_skills']} 个技能\n")

    print("=" * 60)
    print("Continuous Learning - 对话分析")
    print("=" * 60)

    # 读取对话
    reader = ConversationReader(conversation_file, config.max_conversations)
    conversation_name = conversation_file.name
    from_line = state_manager.get_last_processed_line(conversation_name)

    entries = reader.read_latest(from_line)

    if not entries:
        print("\n没有新的对话内容需要分析")
        return 0

    # 构建对话上下文
    context_lines = []
    for entry in entries:
        context_lines.append(f"{entry.timestamp} {entry.sender}> {entry.content}")
    conversation_context = '\n'.join(context_lines)

    # 分析问题
    analyzer = IssueAnalyzer(config.retry_threshold, config.keywords)
    patterns = analyzer.analyze(entries)

    print(f"\n检测到 {len(patterns)} 个反复修复模式")

    if not patterns:
        print("\n未检测到需要总结的反复修复模式")
        print("需要用户反复要求修复同一个问题 >= 3 次")
        return 0

    # 生成技能
    output_dir = project_root / config.skills_output_dir
    generator = SkillGenerator(output_dir)
    generated_skills = []

    for i, pattern in enumerate(patterns, 1):
        print(f"\n{'=' * 60}")
        print(f"模式 {i}/{len(patterns)}")
        print(f"{'=' * 60}")
        print(f"问题: {pattern.topic[:100]}")
        print(f"修复次数: {pattern.occurrences}")

        # 提取对话片段
        conversation_snippets = [msg['content'] for msg in pattern.user_messages]

        # 生成技能
        skill = generator.generate(pattern, conversation_snippets)

        if skill:
            # 保存技能
            skill_path = skill.save(output_dir)
            generated_skills.append((skill_path, skill.name))
            print(f"已生成技能: {skill_path}")

    # 更新状态
    if generated_skills:
        last_line = reader.get_line_number_of_last_user_message(entries)
        for skill_path, skill_name in generated_skills:
            state_manager.update_last_processed_line(
                conversation_name,
                last_line,
                skill_name
            )

        # 总结
        print(f"\n{'=' * 60}")
        print(f"分析完成! 共生成 {len(generated_skills)} 个技能")
        print(f"已更新处理位置到第 {last_line} 行")
        print(f"{'=' * 60}")

        for skill_path, _ in generated_skills:
            print(f"  - {skill_path}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
