#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SessionEnd Hook - Continuous Learning Auto Trigger

持续学习功能的 SessionEnd 钩子 - 在会话结束时自动触发分析
"""

import os
import sys
import json
import subprocess
from pathlib import Path


def get_project_root() -> Path:
    """获取项目根目录"""
    return Path.cwd().absolute()


def get_python_command() -> str:
    """获取 Python 命令"""
    for cmd in ['python39', 'python3.9', 'python3', 'python']:
        try:
            result = subprocess.run(
                [cmd, '--version'],
                capture_output=True,
                timeout=5
            )
            if result.returncode == 0:
                return cmd
        except:
            continue
    return 'python3.9'


def main():
    """主函数"""
    # 从环境变量或 stdin 读取 hook 数据
    hook_data = None

    # 尝试从环境变量读取
    if "CLAUDE_HOOK_DATA" in os.environ:
        try:
            hook_data = json.loads(os.environ["CLAUDE_HOOK_DATA"])
        except:
            pass

    # 如果环境变量没有，尝试从 stdin 读取
    if not hook_data:
        try:
            data = sys.stdin.read()
            if data:
                hook_data = json.loads(data)
        except:
            pass

    if not hook_data:
        sys.exit(0)

    # 检查是否是 Stop 事件（会话结束）
    hook_event_name = hook_data.get("hook_event_name", "")

    if hook_event_name != "Stop":
        sys.exit(0)

    project_root = get_project_root()
    python_cmd = get_python_command()

    # 持续学习脚本路径
    script_path = project_root / '.claude' / 'skills' / 'continuous-learning' / 'scripts' / 'summary_skills.py'

    if not script_path.exists():
        sys.exit(0)

    # 运行持续学习分析
    try:
        result = subprocess.run(
            [python_cmd, str(script_path)],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=project_root
        )

        # 输出结果到 stderr（不影响正常输出）
        if result.stdout:
            sys.stderr.write("\n" + "=" * 60 + "\n")
            sys.stderr.write("持续学习分析结果:\n")
            sys.stderr.write("=" * 60 + "\n")
            sys.stderr.write(result.stdout)

        if result.returncode != 0 and result.stderr:
            sys.stderr.write(f"\n持续学习执行错误: {result.stderr}\n")

    except subprocess.TimeoutExpired:
        sys.stderr.write("\n持续学习分析超时，已跳过\n")
    except Exception as e:
        sys.stderr.write(f"\n持续学习执行失败: {e}\n")

    sys.exit(0)


if __name__ == "__main__":
    main()
