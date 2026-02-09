#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Conversation Reader for Continuous Learning

对话文件读取器
"""

from pathlib import Path
from typing import List, Optional
from models import ConversationEntry


class ConversationReader:
    """对话文件读取器"""

    def __init__(self, file_path: Path, max_lines: int = 20):
        self.file_path = file_path
        self.max_lines = max_lines

    def read_latest(self, from_line: int = 0) -> List[ConversationEntry]:
        """读取最新的对话条目

        Args:
            from_line: 从第几行开始读取（用于增量读取）

        Returns:
            对话条目列表
        """
        if not self.file_path.exists():
            print(f"错误: 对话文件不存在: {self.file_path}")
            return []

        with open(self.file_path, 'r', encoding='utf-8') as f:
            all_lines = f.readlines()

        total_lines = len(all_lines)

        # 从上次处理的行数开始读取
        if from_line > 0:
            print(f"从第 {from_line} 行开始读取 (共 {total_lines} 行)")
            lines_to_read = all_lines[from_line:]
        else:
            print(f"读取完整对话文件 (共 {total_lines} 行)")
            lines_to_read = all_lines

        # 限制读取的条数，支持多行消息
        entries = []
        current_entry = None
        for i, line in enumerate(lines_to_read):
            # 尝试解析为新消息
            entry = ConversationEntry.from_line(line, from_line + i + 1)
            if entry:
                # 如果有当前消息，先保存
                if current_entry:
                    entries.append(current_entry)
                    # 达到最大条数限制
                    if len(entries) >= self.max_lines:
                        break
                current_entry = entry
            elif current_entry and line.strip():
                # 如果不是新消息但有内容，且当前有消息，则作为续行
                # 检查是否是续行（以空格开头）
                if line.startswith(' ') or line.startswith('\t'):
                    # 追加到当前消息内容
                    current_entry.content += ' ' + line.strip()

        # 保存最后一条消息
        if current_entry and len(entries) < self.max_lines:
            entries.append(current_entry)

        print(f"已加载 {len(entries)} 条对话条目")
        return entries

    def get_line_number_of_last_user_message(self, entries: List[ConversationEntry]) -> int:
        """获取最后一个用户消息在文件中的行号"""
        if not entries:
            return 0

        last_user_entry = None
        for entry in reversed(entries):
            if entry.sender == 'user':
                last_user_entry = entry
                break

        if last_user_entry:
            return last_user_entry.line_number

        return entries[-1].line_number if entries else 0
