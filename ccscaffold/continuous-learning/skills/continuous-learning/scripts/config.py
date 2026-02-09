#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration Management for Continuous Learning

持续学习功能的配置管理
"""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class Config:
    """配置类"""
    max_conversations: int = 20
    retry_threshold: int = 3
    conversation_file: str = ".claude/conversations/conversation.txt"
    skills_output_dir: str = ".claude/skills/learn"
    state_file: str = ".claude/skills/continuous-learning/state.json"
    keywords: Dict[str, List[str]] = None

    def __post_init__(self):
        if self.keywords is None:
            self.keywords = {
                "retry": ["修复", "修正", "解决", "还是不行", "还是有问题", "继续", "再试", "失败", "错误"],
                "issues": ["问题", "bug", "错误", "失败", "不正确"]
            }

    @classmethod
    def load(cls, config_file: Path) -> 'Config':
        """从文件加载配置"""
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return cls(**data)
        return cls()

    def save(self, config_file: Path):
        """保存配置到文件"""
        config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(self.__dict__, f, ensure_ascii=False, indent=2)

    @classmethod
    def from_args(cls, args: Optional[dict] = None) -> 'Config':
        """从命令行参数创建配置"""
        if args is None:
            return cls()

        config = cls()

        if 'max_conversations' in args and args['max_conversations'] is not None:
            config.max_conversations = int(args['max_conversations'])

        if 'conversation_file' in args and args['conversation_file'] is not None:
            config.conversation_file = args['conversation_file']

        return config


# Default configuration file path
DEFAULT_CONFIG_PATH = Path(".claude/skills/continuous-learning/config.json")


def get_config(config_file: Optional[Path] = None) -> Config:
    """获取配置对象"""
    if config_file is None:
        config_file = DEFAULT_CONFIG_PATH

    if config_file.exists():
        return Config.load(config_file)

    return Config()
