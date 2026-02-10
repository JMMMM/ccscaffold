#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-
"""
CC-Scaffold Utilities Module
CC-Scaffold 工具模块
"""

from .privacy_utils import (
    PrivacySanitizer,
    LogSanitizer,
    get_safe_project_path,
    safe_print_path,
)

from .platform import (
    is_windows,
    is_macos,
    is_linux,
    is_unix,
    get_platform_name,
    get_default_python_candidates,
    detect_python_command,
    detect_available_python_commands,
    find_python_command,
    get_python_exe_path,
    make_executable,
    normalize_path,
    get_home_directory,
    get_config_directory
)

from .config import (
    Config,
    get_config,
    reset_config,
    interactive_python_command_selection
)

__all__ = [
    "PrivacySanitizer",
    "LogSanitizer",
    "get_safe_project_path",
    "safe_print_path",
    # 平台检测
    'is_windows',
    'is_macos',
    'is_linux',
    'is_unix',
    'get_platform_name',
    # Python 命令检测
    'get_default_python_candidates',
    'detect_python_command',
    'detect_available_python_commands',
    'find_python_command',
    'get_python_exe_path',
    # 路径和文件
    'make_executable',
    'normalize_path',
    'get_home_directory',
    'get_config_directory',
    # 配置管理
    'Config',
    'get_config',
    'reset_config',
    'interactive_python_command_selection'
]
