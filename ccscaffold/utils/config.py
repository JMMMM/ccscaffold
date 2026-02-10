#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CC-Scaffold 配置管理系统
提供统一的配置文件加载、保存和管理功能
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

from .platform import get_config_directory, detect_available_python_commands


class Config:
    """配置管理类"""

    # 配置文件名
    CONFIG_FILE = 'config.json'

    # 默认配置
    DEFAULT_CONFIG = {
        'python': {
            'command': None,  # Python 命令（如 'python3', 'python39'）
            'auto_detect': True,  # 是否自动检测
            'min_version': '3.9',  # 最低版本要求
            'candidates': []  # 自定义候选列表
        },
        'platform': {
            'name': None,  # 平台名称（自动检测）
            'auto_detect': True  # 是否自动检测
        },
        'paths': {
            'config_dir': None,  # 配置目录（自动设置）
            'temp_dir': None  # 临时目录（可自定义）
        }
    }

    def __init__(self, config_dir: Optional[Path] = None):
        """
        初始化配置管理器

        Args:
            config_dir: 配置目录路径，如果为 None 则使用默认目录
        """
        if config_dir is None:
            config_dir = get_config_directory()

        self.config_dir = Path(config_dir)
        self.config_file = self.config_dir / self.CONFIG_FILE
        self.config = self.DEFAULT_CONFIG.copy()

        # 加载配置
        self.load()

    def load(self) -> bool:
        """
        从配置文件加载配置

        Returns:
            是否成功加载
        """
        if not self.config_file.exists():
            # 创建默认配置文件
            return self.save()

        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                loaded_config = json.load(f)

            # 合并配置（保留默认值）
            self._merge_config(self.config, loaded_config)
            return True
        except Exception as e:
            print(f"警告: 加载配置文件失败: {e}")
            print(f"使用默认配置")
            return False

    def save(self) -> bool:
        """
        保存配置到文件

        Returns:
            是否成功保存
        """
        try:
            # 确保配置目录存在
            self.config_dir.mkdir(parents=True, exist_ok=True)

            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)

            return True
        except Exception as e:
            print(f"错误: 保存配置文件失败: {e}")
            return False

    def _merge_config(self, base: Dict, override: Dict):
        """
        递归合并配置字典

        Args:
            base: 基础配置
            override: 覆盖配置
        """
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value

    def get(self, *keys: str, default: Any = None) -> Any:
        """
        获取配置值

        Args:
            *keys: 配置键路径（如 'python', 'command'）
            default: 默认值

        Returns:
            配置值，如果不存在返回默认值
        """
        value = self.config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value

    def set(self, *keys: str, value: Any) -> bool:
        """
        设置配置值

        Args:
            *keys: 配置键路径
            value: 配置值

        Returns:
            是否成功设置
        """
        config = self.config
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]

        config[keys[-1]] = value
        return self.save()

    def get_python_command(self) -> Optional[str]:
        """
        获取配置的 Python 命令

        Returns:
            Python 命令，如果未配置返回 None
        """
        return self.get('python', 'command')

    def set_python_command(self, command: str) -> bool:
        """
        设置 Python 命令

        Args:
            command: Python 命令

        Returns:
            是否成功设置
        """
        return self.set('python', 'command', value=command)

    def get_python_candidates(self) -> list:
        """
        获取 Python 命令候选列表

        Returns:
            候选列表
        """
        candidates = self.get('python', 'candidates', default=[])
        if candidates:
            return candidates

        # 如果没有自定义候选列表，使用自动检测
        from .platform import get_default_python_candidates
        return get_default_python_candidates()

    def should_auto_detect_python(self) -> bool:
        """
        是否应该自动检测 Python 命令

        Returns:
            是否自动检测
        """
        return self.get('python', 'auto_detect', default=True)

    def get_min_python_version(self) -> str:
        """
        获取最低 Python 版本要求

        Returns:
            版本字符串
        """
        return self.get('python', 'min_version', default='3.9')

    def get_config_directory(self) -> Path:
        """
        获取配置目录路径

        Returns:
            配置目录路径
        """
        return self.config_dir

    def to_dict(self) -> Dict:
        """
        转换为字典

        Returns:
            配置字典
        """
        return self.config.copy()

    def __repr__(self) -> str:
        return f"Config(config_file='{self.config_file}')"


# 全局配置实例
_global_config: Optional[Config] = None


def get_config() -> Config:
    """
    获取全局配置实例（单例模式）

    Returns:
        配置实例
    """
    global _global_config
    if _global_config is None:
        _global_config = Config()
    return _global_config


def reset_config():
    """重置全局配置实例"""
    global _global_config
    _global_config = None


def interactive_python_command_selection(config: Optional[Config] = None) -> Optional[str]:
    """
    交互式 Python 命令选择

    Args:
        config: 配置实例，如果为 None 则使用全局配置

    Returns:
        选择的 Python 命令，如果取消返回 None
    """
    if config is None:
        config = get_config()

    print("\n检测可用的 Python 版本...")
    from .platform import detect_available_python_commands
    available = detect_available_python_commands()

    if not available:
        print("警告: 未检测到可用的 Python 命令")
        print("请手动输入 Python 命令（如: python39, python3.9, python3）")

        while True:
            cmd = input("Python 命令 (或留空取消): ").strip()
            if not cmd:
                return None

            from .platform import detect_python_command
            result = detect_python_command(cmd)
            if result:
                print(f"检测到: {result[1]}")
                if input("使用此命令？(y/n): ").lower() == 'y':
                    config.set_python_command(cmd)
                    return cmd
            else:
                print(f"命令 '{cmd}' 不可用，请重新输入")

    print("\n可用的 Python 版本:")
    for i, (cmd, version) in enumerate(available, 1):
        print(f"  {i}. {cmd} ({version})")
    print(f"  {len(available) + 1}. 自定义")

    while True:
        choice = input(f"\n请选择 [1-{len(available) + 1}]，或留空使用第一个: ").strip()

        if not choice:
            selected = available[0][0]
            config.set_python_command(selected)
            return selected

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(available):
                selected = available[idx][0]
                config.set_python_command(selected)
                return selected
            elif idx == len(available):
                # 自定义
                while True:
                    cmd = input("请输入 Python 命令: ").strip()
                    if not cmd:
                        break

                    from .platform import detect_python_command
                    result = detect_python_command(cmd)
                    if result:
                        print(f"检测到: {result[1]}")
                        if input("使用此命令？(y/n): ").lower() == 'y':
                            config.set_python_command(cmd)
                            return cmd
                    else:
                        print(f"命令 '{cmd}' 不可用，请重新输入")
                # 如果用户取消自定义，返回到主菜单
                continue
            else:
                print("无效的选择，请重新输入")
        except ValueError:
            print("请输入数字")


if __name__ == '__main__':
    # 测试代码
    print("配置管理测试")
    print("=" * 60)

    config = get_config()
    print(f"配置目录: {config.get_config_directory()}")
    print(f"配置文件: {config.config_file}")
    print()

    print("当前配置:")
    print(json.dumps(config.to_dict(), indent=2, ensure_ascii=False))
    print()

    print("Python 配置:")
    print(f"  命令: {config.get_python_command()}")
    print(f"  自动检测: {config.should_auto_detect_python()}")
    print(f"  最低版本: {config.get_min_python_version()}")
    print(f"  候选列表: {config.get_python_candidates()}")
