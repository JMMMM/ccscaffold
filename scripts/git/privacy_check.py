#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-
"""
Git Pre-commit Privacy Check Script
Git 提交前隐私检查脚本 - 防止敏感信息泄露

根据 CC-Scaffold 宪章 Principle X: 隐私保护与信息安全原则
检查 Git 暂存区中是否包含敏感信息
"""

import sys
import subprocess
import re
from pathlib import Path


# 敏感信息检测模式
SENSITIVE_PATTERNS = {
    'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    'unix_path_with_username': r'/(home|Users|var|tmp)/[^/]+',
    'windows_path_with_username': r'[A-Z]:\\(Users|Program Files|Documents)[^\\]*',
    'api_key': r'(api[_-]?key|apikey|access[_-]?token|secret)[\s:=]+["\']?[A-Za-z0-9_\-]{16,}',
    'password': r'(password|passwd|pwd)[\s:=]+["\']?[^\s"\']+',
    'ip_address': r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
    'url_credentials': r'://[^:@]+:[^@]+@',
    'private_key': r'-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----',
}


def get_staged_diff():
    """获取 Git 暂存区的 diff 内容"""
    try:
        result = subprocess.run(
            ['git', 'diff', '--cached', '--unified=0'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"错误: 无法获取 Git diff: {e}")
        return None


def check_for_sensitive_info(diff_content):
    """
    检查 diff 内容中是否包含敏感信息

    Returns:
        list: 发现的问题列表，每个问题包含 (类型, 匹配行, 匹配内容)
    """
    issues = []

    if not diff_content:
        return issues

    lines = diff_content.split('\n')

    for line_num, line in enumerate(lines, 1):
        # 只检查新增的行（以 + 开头但不是 +++）
        if not line.startswith('+') or line.startswith('+++'):
            continue

        # 移除开头的 + 号
        content = line[1:]

        # 检查每种敏感信息模式
        for pattern_name, pattern in SENSITIVE_PATTERNS.items():
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                issues.append({
                    'line': line_num,
                    'pattern': pattern_name,
                    'content': match.group(),
                    'context': line.strip()
                })

    return issues


def print_issues(issues):
    """打印发现的问题"""
    if not issues:
        return

    print("=" * 70)
    print("隐私安全检查失败 - 发现敏感信息")
    print("=" * 70)
    print()
    print("以下内容可能包含敏感信息，请在提交前移除或脱敏：")
    print()

    for i, issue in enumerate(issues, 1):
        print(f"[{i}] {issue['pattern'].upper()}")
        print(f"    行号: {issue['line']}")
        print(f"    内容: {issue['context']}")
        print(f"    匹配: {issue['content']}")
        print()

    print("=" * 70)
    print("建议的解决方案：")
    print("=" * 70)
    print()
    print("1. 绝对路径: 使用相对路径或环境变量")
    print("2. 电子邮件: 使用 test@example.com 或占位符")
    print("3. API 密钥/密码: 使用环境变量，不要提交到代码库")
    print("4. IP 地址: 使用占位符如 192.168.1.1")
    print()
    print("如果确认这些内容安全，可以使用 --no-verify 跳过检查:")
    print("  git commit --no-verify")
    print()


def main():
    """主函数"""
    # 获取暂存区的 diff
    diff_content = get_staged_diff()

    if diff_content is None:
        sys.exit(1)

    # 检查敏感信息
    issues = check_for_sensitive_info(diff_content)

    if issues:
        print_issues(issues)
        sys.exit(1)

    print("隐私安全检查通过")
    sys.exit(0)


if __name__ == '__main__':
    main()
