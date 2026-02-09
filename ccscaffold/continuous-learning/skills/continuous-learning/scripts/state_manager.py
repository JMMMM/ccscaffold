#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
State Manager for Continuous Learning

持续学习功能的状态管理
"""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


@dataclass
class ConversationState:
    """单个对话文件的状态"""
    last_line: int = 0
    skills_generated: List[Dict] = field(default_factory=list)
    first_analyzed: str = ""
    last_analyzed: str = ""


@dataclass
class StateManager:
    """状态管理器"""
    state_file: Path

    def __init__(self, state_file: Path):
        self.state_file = state_file
        self.state = self._load_state()

    def _load_state(self) -> Dict[str, ConversationState]:
        """加载状态文件"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return {
                        name: ConversationState(**state)
                        for name, state in data.items()
                    }
            except Exception as e:
                print(f"警告: 无法加载状态文件: {e}")
                return {}

        return {}

    def get_last_processed_line(self, conversation_file_name: str) -> int:
        """获取指定对话文件上次处理的行数"""
        if conversation_file_name in self.state:
            return self.state[conversation_file_name].last_line
        return 0

    def update_last_processed_line(
        self,
        conversation_file_name: str,
        line_number: int,
        skill_name: str
    ):
        """
        更新指定对话文件的处理行数

        Args:
            conversation_file_name: 对话文件名
            line_number: 已处理的行数
            skill_name: 生成的技能名称
        """
        if conversation_file_name not in self.state:
            self.state[conversation_file_name] = ConversationState()

        state = self.state[conversation_file_name]
        state.last_line = line_number
        state.last_analyzed = datetime.now().isoformat()

        if not state.first_analyzed:
            state.first_analyzed = datetime.now().isoformat()

        # 记录生成的技能
        if skill_name:
            state.skills_generated.append({
                'name': skill_name,
                'generated_at': datetime.now().isoformat(),
                'processed_line': line_number
            })

        self._save_state()

    def _save_state(self):
        """保存状态到文件"""
        try:
            self.state_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.state_file, 'w', encoding='utf-8') as f:
                data = {
                    name: {
                        'last_line': state.last_line,
                        'skills_generated': state.skills_generated,
                        'first_analyzed': state.first_analyzed,
                        'last_analyzed': state.last_analyzed
                    }
                    for name, state in self.state.items()
                }
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"警告: 无法保存状态文件: {e}")

    def get_summary(self) -> Dict[str, int]:
        """获取状态摘要"""
        return {
            'total_conversations': len(self.state),
            'total_skills': sum(
                len(state.skills_generated)
                for state in self.state.values()
            )
        }
