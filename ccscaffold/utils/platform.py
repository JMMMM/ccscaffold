#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CC-Scaffold 跨平台工具模块
提供跨平台的 Python 命令检测、平台检测等实用功能
"""

import sys
import subprocess
import shutil
from pathlib import Path
from typing import List, Tuple, Optional


def is_windows() -> bool:
    """检测是否为 Windows 系统"""
    return sys.platform == 'win32'


def is_macos() -> bool:
    """检测是否为 macOS 系统"""
    return sys.platform == 'darwin'


def is_linux() -> bool:
    """检测是否为 Linux 系统"""
    return sys.platform.startswith('linux')


def is_unix() -> bool:
    """检测是否为 Unix-like 系统（包括 macOS 和 Linux）"""
    return sys.platform in ('darwin', 'linux') or sys.platform.startswith('linux')


def get_platform_name() -> str:
    """获取平台名称"""
    if is_windows():
        return 'windows'
    elif is_macos():
        return 'macos'
    elif is_linux():
        return 'linux'
    else:
        return 'unknown'


def get_default_python_candidates() -> List[str]:
    """
    获取默认的 Python 命令候选列表
    根据平台返回不同的候选列表
    """
    if is_windows():
        # Windows 平台优先使用 python, python39
        return ['python', 'python39', 'py', 'python3']
    elif is_macos() or is_linux():
        # Unix-like 系统优先使用 python3, python3.9
        return ['python3', 'python3.9', 'python39', 'python']
    else:
        # 其他平台使用通用列表
        return ['python3', 'python', 'python3.9', 'python39']


def detect_python_command(candidate: Optional[str] = None) -> Optional[Tuple[str, str]]:
    """
    检测单个 Python 命令是否可用

    Args:
        candidate: Python 命令（如 'python3', 'python39'）

    Returns:
        如果可用，返回 (command, version) 元组；否则返回 None
    """
    if not candidate:
        return None

    try:
        result = subprocess.run(
            [candidate, '--version'],
            capture_output=True,
            text=True,
            timeout=5,
            shell=is_windows()  # Windows 下需要 shell=True
        )
        if result.returncode == 0:
            version = result.stdout.strip().replace('Python ', '')
            return (candidate, version)
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        pass

    return None


def detect_available_python_commands() -> List[Tuple[str, str]]:
    """
    检测所有可用的 Python 命令

    Returns:
        可用的 Python 命令列表，每个元素是 (command, version) 元组
        按优先级排序
    """
    candidates = get_default_python_candidates()
    available = []

    for cmd in candidates:
        result = detect_python_command(cmd)
        if result:
            available.append(result)

    return available


def find_python_command(min_version: Optional[str] = None) -> Optional[str]:
    """
    查找满足最低版本要求的 Python 命令

    Args:
        min_version: 最低版本要求（如 '3.9'）

    Returns:
        找到的 Python 命令，如果未找到返回 None
    """
    available = detect_available_python_commands()

    if not available:
        return None

    if min_version is None:
        # 返回第一个可用的
        return available[0][0] if available else None

    # 检查版本
    for cmd, version in available:
        try:
            if version >= min_version:
                return cmd
        except (ValueError, TypeError):
            # 版本比较失败，跳过
            continue

    return None


def get_python_exe_path() -> Optional[Path]:
    """
    获取当前 Python 解释器的完整路径

    Returns:
        Python 解释器路径，如果获取失败返回 None
    """
    try:
        python_path = Path(sys.executable).resolve()
        if python_path.exists():
            return python_path
    except Exception:
        pass

    return None


def make_executable(path: Path):
    """
    设置文件可执行权限（仅 Unix-like 系统）

    Args:
        path: 文件路径
    """
    if is_unix():
        try:
            import stat
            current_mode = path.stat().st_mode
            path.chmod(current_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        except Exception:
            pass


def normalize_path(path: str) -> Path:
    """
    标准化路径（处理跨平台路径分隔符）

    Args:
        path: 路径字符串

    Returns:
        标准化后的 Path 对象
    """
    return Path(path).resolve()


def get_home_directory() -> Path:
    """
    获取用户主目录（跨平台）

    Returns:
        用户主目录路径
    """
    return Path.home()


def get_config_directory() -> Path:
    """
    获取 CC-Scaffold 配置目录（跨平台）

    Returns:
        配置目录路径
    """
    if is_windows():
        # Windows: %APPDATA%\ccscaffold
        config_dir = Path(os.environ.get('APPDATA', Path.home() / 'AppData' / 'Roaming')) / 'ccscaffold'
    elif is_macos():
        # macOS: ~/Library/Application Support/ccscaffold
        config_dir = get_home_directory() / 'Library' / 'Application Support' / 'ccscaffold'
    else:
        # Linux: ~/.config/ccscaffold
        config_dir = get_home_directory() / '.config' / 'ccscaffold'

    return config_dir


# 兼容性：导入时自动添加 os 模块
import os


if __name__ == '__main__':
    # 测试代码
    print("平台信息:")
    print(f"  平台: {get_platform_name()}")
    print(f"  Windows: {is_windows()}")
    print(f"  macOS: {is_macos()}")
    print(f"  Linux: {is_linux()}")
    print(f"  Unix: {is_unix()}")
    print()

    print("Python 命令候选列表:")
    candidates = get_default_python_candidates()
    for cmd in candidates:
        print(f"  - {cmd}")
    print()

    print("可用的 Python 命令:")
    available = detect_available_python_commands()
    if available:
        for cmd, version in available:
            print(f"  - {cmd} ({version})")
    else:
        print("  未找到可用的 Python 命令")
    print()

    print("当前 Python 解释器:")
    exe_path = get_python_exe_path()
    if exe_path:
        print(f"  {exe_path}")
    else:
        print("  未获取到路径")
