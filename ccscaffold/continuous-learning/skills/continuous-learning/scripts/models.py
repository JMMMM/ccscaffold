#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data Models for Continuous Learning

持续学习功能的数据模型定义
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Set
from pathlib import Path


@dataclass
class ConversationEntry:
    """对话条目"""
    timestamp: str
    sender: str
    content: str
    line_number: int

    @classmethod
    def from_line(cls, line: str, line_number: int) -> Optional['ConversationEntry']:
        """从单行文本解析对话条目"""
        import re
        pattern = r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+(\w+)>\s*(.+)$'
        match = re.match(pattern, line.strip())
        if match:
            return cls(
                timestamp=match.group(1),
                sender=match.group(2),
                content=match.group(3),
                line_number=line_number
            )
        return None


@dataclass
class IssuePattern:
    """问题模式"""
    topic: str
    occurrences: int
    first_line: int
    last_line: int
    keywords: Set[str] = field(default_factory=set)
    user_messages: List[Dict] = field(default_factory=list)

    def meets_threshold(self, threshold: int = 3) -> bool:
        """检查是否达到反复问题阈值"""
        return self.occurrences >= threshold


@dataclass
class LearnedSkill:
    """学习技能"""
    name: str
    description: str
    issue_topic: str
    retry_count: int
    generated_at: str
    content: str
    file_path: Optional[Path] = None

    @classmethod
    def create(cls, pattern: IssuePattern, content: str) -> 'LearnedSkill':
        """从问题模式创建学习技能"""
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        name = f"fix-{sanitize_topic(pattern.topic)}-{timestamp}"
        return cls(
            name=name,
            description=f"自动生成的修复技能 - {pattern.topic}",
            issue_topic=pattern.topic,
            retry_count=pattern.occurrences,
            generated_at=datetime.now().isoformat(),
            content=content
        )

    def save(self, directory: Path) -> Path:
        """保存技能到文件"""
        directory.mkdir(parents=True, exist_ok=True)
        self.file_path = directory / f"{self.name}.md"
        with open(self.file_path, 'w', encoding='utf-8') as f:
            f.write(self.content)
        return self.file_path


def sanitize_topic(topic: str) -> str:
    """清理主题字符串，用作文件名"""
    import re
    sanitized = re.sub(r'[^\w\u4e00-\u9fff-]', '-', topic)
    return sanitized[:50]


@dataclass
class ConversationState:
    """单个对话文件的状态"""
    last_line: int = 0
    skills_generated: List[Dict] = field(default_factory=list)
    first_analyzed: str = ""
    last_analyzed: str = ""


@dataclass
class State:
    """全局状态"""
    conversations: Dict[str, ConversationState] = field(default_factory=dict)

    def load(self, state_file: Path) -> 'State':
        """从文件加载状态"""
        if state_file.exists():
            import json
            with open(state_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for conv_name, conv_state in data.items():
                    self.conversations[conv_name] = ConversationState(**conv_state)
        return self

    def save(self, state_file: Path):
        """保存状态到文件"""
        import json
        from datetime import datetime
        state_file.parent.mkdir(parents=True, exist_ok=True)
        data = {
            name: {
                'last_line': state.last_line,
                'skills_generated': state.skills_generated,
                'first_analyzed': state.first_analyzed,
                'last_analyzed': state.last_analyzed
            }
            for name, state in self.conversations.items()
        }
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_last_line(self, conversation_file: str) -> int:
        """获取对话文件上次处理的行数"""
        if conversation_file in self.conversations:
            return self.conversations[conversation_file].last_line
        return 0

    def update_last_line(self, conversation_file: str, line: int, skill_name: str):
        """更新已处理的行数"""
        from datetime import datetime
        if conversation_file not in self.conversations:
            self.conversations[conversation_file] = ConversationState()

        state = self.conversations[conversation_file]
        state.last_line = line
        state.last_analyzed = datetime.now().isoformat()

        if not state.first_analyzed:
            state.first_analyzed = state.last_analyzed

        state.skills_generated.append({
            'name': skill_name,
            'generated_at': datetime.now().isoformat(),
            'processed_line': line
        })
