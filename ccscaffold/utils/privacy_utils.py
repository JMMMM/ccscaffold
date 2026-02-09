#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-
"""
CC-Scaffold Privacy Utilities
隐私保护工具模块 - 提供数据脱敏和敏感信息检测功能

根据 CC-Scaffold 宪章 Principle X: 隐私保护与信息安全原则
"""

import re
from typing import Optional, Dict, Any
from pathlib import Path


class PrivacySanitizer:
    """数据脱敏工具类"""

    # 敏感信息检测模式
    PATTERNS = {
        'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        'unix_path_with_username': r'/(home|Users|var|tmp)/[^/]+',
        'windows_path_with_username': r'[A-Z]:\\(Users|Program Files|Documents)[^\\]*',
        'ip_address': r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
        'url_credentials': r'://[^:@]+:[^@]+@',
    }

    # 脱敏替换模板
    MASK_TEMPLATES = {
        'email': '***@***.***',
        'unix_path_with_username': r'/\1/***',
        'windows_path_with_username': r'\1:\\***',
        'ip_address': '***.***.***.***',
        'url_credentials': '://***:***@',
    }

    @classmethod
    def sanitize_string(cls, text: str) -> str:
        """
        脱敏字符串中的敏感信息

        Args:
            text: 原始文本

        Returns:
            脱敏后的文本
        """
        if not text:
            return text

        result = text

        # 按模式进行脱敏
        for pattern_name, pattern in cls.PATTERNS.items():
            template = cls.MASK_TEMPLATES.get(pattern_name, '***')
            result = re.sub(pattern, template, result, flags=re.IGNORECASE)

        return result

    @classmethod
    def sanitize_path(cls, path: str) -> str:
        """
        脱敏文件路径中的用户名

        Args:
            path: 文件路径

        Returns:
            脱敏后的路径
        """
        if not path:
            return path

        # 脱敏 Unix-like 路径
        path = re.sub(r'/(home|Users|var|tmp)/[^/]+', r'/\1/***', path)

        # 脱敏 Windows 路径
        path = re.sub(r'[A-Z]:\\(Users|Program Files|Documents)[^\\]*',
                     r'\1:\\***', path)

        return path

    @classmethod
    def sanitize_log_message(cls, message: str) -> str:
        """
        脱敏日志消息中的敏感信息

        Args:
            message: 日志消息

        Returns:
            脱敏后的日志消息
        """
        return cls.sanitize_string(message)

    @classmethod
    def sanitize_dict(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        递归脱敏字典中的敏感信息

        Args:
            data: 原始字典

        Returns:
            脱敏后的字典
        """
        if not isinstance(data, dict):
            return data

        result = {}
        for key, value in data.items():
            # 检查键名是否为敏感字段
            if cls._is_sensitive_key(key):
                result[key] = '***'
            elif isinstance(value, str):
                result[key] = cls.sanitize_string(value)
            elif isinstance(value, dict):
                result[key] = cls.sanitize_dict(value)
            elif isinstance(value, list):
                result[key] = [cls.sanitize_dict(item) if isinstance(item, dict)
                               else cls.sanitize_string(item) if isinstance(item, str)
                               else item for item in value]
            else:
                result[key] = value

        return result

    @classmethod
    def _is_sensitive_key(cls, key: str) -> bool:
        """检查键名是否为敏感字段"""
        sensitive_keywords = [
            'password', 'passwd', 'pwd',
            'secret', 'token', 'key',
            'api_key', 'apikey', 'access_token',
            'auth', 'credential', 'private_key',
            'email', 'phone', 'address',
        ]
        key_lower = key.lower()
        return any(keyword in key_lower for keyword in sensitive_keywords)

    @classmethod
    def check_for_sensitive_info(cls, text: str) -> list:
        """
        检查文本中是否包含敏感信息

        Args:
            text: 要检查的文本

        Returns:
            发现的敏感信息列表，格式: [{'type': 类型, 'match': 匹配内容}]
        """
        issues = []

        for pattern_name, pattern in cls.PATTERNS.items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                issues.append({
                    'type': pattern_name,
                    'match': match.group(),
                })

        return issues


class LogSanitizer:
    """日志脱敏工具类"""

    @staticmethod
    def sanitize(record: Dict[str, Any]) -> Dict[str, Any]:
        """
        脱敏日志记录

        Args:
            record: 日志记录字典

        Returns:
            脱敏后的日志记录
        """
        # 使用 PrivacySanitizer 处理
        return PrivacySanitizer.sanitize_dict(record)

    @staticmethod
    def sanitize_exception(exception: Exception) -> str:
        """
        脱敏异常信息中的敏感路径

        Args:
            exception: 异常对象

        Returns:
            脱敏后的异常信息字符串
        """
        import traceback

        tb_str = ''.join(traceback.format_exception(
            type(exception), exception, exception.__traceback__
        ))

        # 脱敏文件路径
        sanitized = PrivacySanitizer.sanitize_path(tb_str)

        return sanitized


def get_safe_project_path(path: Path) -> str:
    """
    获取安全的项目路径表示（用于日志和显示）

    Args:
        path: 文件路径

    Returns:
        脱敏后的路径字符串
    """
    path_str = str(path)

    # 如果是绝对路径，脱敏用户名
    if path.is_absolute():
        path_str = PrivacySanitizer.sanitize_path(path_str)
    else:
        # 相对路径保持不变
        pass

    return path_str


def safe_print_path(path: Path, label: str = "Path") -> None:
    """
    安全地打印路径（自动脱敏）

    Args:
        path: 文件路径
        label: 标签
    """
    safe_path = get_safe_project_path(path)
    print(f"{label}: {safe_path}")


# 示例用法
if __name__ == '__main__':
    # 测试脱敏功能
    test_cases = [
        ("Email: user@example.com", "Email: ***@***.***"),
        ("Path: /Users/ming/work/project", "Path: /Users/***"),
        ("Path: C:\\Users\\ming\\Documents", "Path: C:\\Users\\***"),
        ("IP: 192.168.1.1", "IP: ***.***.***.***"),
        ("URL: ftp://user:pass@host", "URL: ftp://***:***@host"),
    ]

    print("隐私脱敏测试:")
    print("=" * 60)

    for input_text, expected in test_cases:
        result = PrivacySanitizer.sanitize_string(input_text)
        status = "OK" if result == expected else f"FAIL (got: {result})"
        print(f"{input_text:40} -> {status}")

    print()
    print("敏感信息检测测试:")
    print("=" * 60)

    test_text = "Contact user@example.com at /home/alice/work"
    issues = PrivacySanitizer.check_for_sensitive_info(test_text)

    print(f"测试文本: {test_text}")
    print(f"发现 {len(issues)} 个敏感信息:")
    for issue in issues:
        print(f"  - {issue['type']}: {issue['match']}")
