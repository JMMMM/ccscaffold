#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-
"""
CC-Scaffold - Claude Code Experience Management Tool
CC-Scaffold - Claude Code 经验管理工具

一个帮助你管理和迁移 Claude Code 经验的工具包,采用功能模块化组织结构。

Version: 2.2.0
宪章版本: 1.4.0
"""

__version__ = "2.2.0"
__constitution_version__ = "1.4.0"

from .utils.privacy_utils import (
    PrivacySanitizer,
    LogSanitizer,
    get_safe_project_path,
    safe_print_path,
)

__all__ = [
    "PrivacySanitizer",
    "LogSanitizer",
    "get_safe_project_path",
    "safe_print_path",
]
