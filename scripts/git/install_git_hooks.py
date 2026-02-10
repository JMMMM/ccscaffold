#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Install Git Hooks Script (Python version)
安装 Git 钩子脚本 (Python 版本) - 将隐私检查脚本安装到项目的 .git/hooks/
"""

import os
import sys
import shutil
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from ccscaffold.utils import (
    find_python_command,
    make_executable,
    is_unix
)


def get_project_root():
    """获取项目根目录"""
    script_dir = Path(__file__).resolve().parent
    return script_dir.parent.parent


def install_hooks():
    """安装 Git 钩子"""
    project_root = get_project_root()
    git_dir = project_root / '.git'

    # 检查是否在 Git 仓库中
    if not git_dir.exists():
        print("错误: 当前目录不是一个 Git 仓库")
        print("请确保在项目根目录运行此脚本")
        return False

    # 检测 Python 命令
    python_cmd = find_python_command(min_version='3.9')
    if not python_cmd:
        print("警告: 未检测到 Python 3.9 或更高版本")
        print("使用 'python3' 作为默认命令")
        python_cmd = 'python3'

    print(f"使用 Python 命令: {python_cmd}")

    # 钩子目录
    hooks_dir = git_dir / 'hooks'

    # 创建钩子目录（如果不存在）
    hooks_dir.mkdir(parents=True, exist_ok=True)

    # pre-commit 钩子内容
    pre_commit_content = f"""#!/usr/bin/env bash
#
# Git Pre-commit Hook - Privacy Check
# Git 提交前隐私检查钩子
#

SCRIPT_DIR="$(cd "$(dirname "${{BASH_SOURCE[0]}}")" && pwd)"
PROJECT_ROOT="$(cd "${{SCRIPT_DIR}}/../.." && pwd)"
PRIVACY_CHECK_SCRIPT="${{PROJECT_ROOT}}/scripts/git/privacy_check.py"

# 检查隐私检查脚本是否存在
if [ -f "${{PRIVACY_CHECK_SCRIPT}}" ]; then
    {python_cmd} "${{PRIVACY_CHECK_SCRIPT}}"
    EXIT_CODE=$?

    if [ ${{EXIT_CODE}} -ne 0 ]; then
        echo ""
        echo "警告: 提交被阻止 - 检测到敏感信息"
        echo "使用 'git commit --no-verify' 跳过检查（不推荐）"
        exit 1
    fi
else
    echo "警告: 隐私检查脚本不存在: ${{PRIVACY_CHECK_SCRIPT}}"
    echo "继续提交..."
fi

exit 0
"""

    # 安装 pre-commit 钩子
    pre_commit_file = hooks_dir / 'pre-commit'
    with open(pre_commit_file, 'w', encoding='utf-8') as f:
        f.write(pre_commit_content)

    # 设置可执行权限（仅 Unix-like 系统）
    if is_unix():
        make_executable(pre_commit_file)

    return True


def main():
    """主函数"""
    print("=" * 60)
    print("安装 Git 钩子")
    print("=" * 60)
    print()

    if install_hooks():
        print("pre-commit 钩子已安装")
        print()
        print("=" * 60)
        print("安装完成！")
        print("=" * 60)
        print()
        print("已安装的 Git 钩子:")
        print("  - pre-commit: 提交前自动检查隐私安全")
        print()
        print("每次执行 'git commit' 时会自动运行隐私检查")
        print()
        print("如需跳过检查（不推荐）:")
        print("  git commit --no-verify")
        print()
        return 0
    else:
        return 1


if __name__ == '__main__':
    sys.exit(main())
