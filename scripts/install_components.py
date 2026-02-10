#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CC-Scaffold 组件安装脚本
用于将 CC-Scaffold 开发的组件安装到目标项目
"""

import os
import sys
import shutil
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from ccscaffold.utils import (
    detect_available_python_commands,
    interactive_python_command_selection
)


def get_ccscaffold_root():
    """获取 CC-Scaffold 根目录"""
    script_dir = Path(__file__).parent.absolute()
    return script_dir


def install_chat_record(target_project_root):
    """安装会话记录功能"""
    ccscaffold_root = get_ccscaffold_root()
    target_root = Path(target_project_root)

    print("安装会话记录功能...")

    # 创建目标目录
    target_skills = target_root / '.claude' / 'skills'
    target_hooks = target_root / '.claude-hooks'
    target_commands = target_root / '.claude' / 'commands'
    target_skills.mkdir(parents=True, exist_ok=True)
    target_hooks.mkdir(parents=True, exist_ok=True)
    target_commands.mkdir(parents=True, exist_ok=True)

    # 复制 skill
    chat_recorder_src = ccscaffold_root / 'chat-record' / 'skills' / 'chat-record'
    chat_recorder_dst = target_skills / 'chat-record'
    if chat_recorder_dst.exists():
        shutil.rmtree(chat_recorder_dst)
    shutil.copytree(chat_recorder_src, chat_recorder_dst)
    print(f"  ✓ 已复制 chat-record skill")

    # 复制 hooks
    hooks = ['session_end_summary.py']
    for hook in hooks:
        src = ccscaffold_root / 'chat-record' / 'hooks' / hook
        dst = target_hooks / hook
        shutil.copy2(src, dst)
        print(f"  ✓ 已复制 {hook}")

    # 复制命令
    commands = ['loadLastSession.md']
    for cmd in commands:
        src = ccscaffold_root / 'chat-record' / 'commands' / cmd
        dst = target_commands / cmd
        shutil.copy2(src, dst)
        print(f"  ✓ 已复制 {cmd}")

    print("会话记录功能安装完成！")


def install_speckit_agent(target_project_root):
    """安装 SpecKit Agent"""
    ccscaffold_root = get_ccscaffold_root()
    target_root = Path(target_project_root)

    print("安装 SpecKit Agent...")

    # 创建目标目录
    target_agents = target_root / '.claude' / 'agents'
    target_agents.mkdir(parents=True, exist_ok=True)

    # 复制 agent
    src = ccscaffold_root / 'speckitAgent' / 'agents' / 'speckitAgent.md'
    dst = target_agents / 'speckitAgent.md'
    shutil.copy2(src, dst)
    print(f"  ✓ 已复制 speckitAgent")

    print("SpecKit Agent 安装完成！")


def update_settings_json(target_project_root, python_cmd):
    """更新 settings.json 配置"""
    target_root = Path(target_project_root)
    settings_file = target_root / '.claude' / 'settings.json'

    print("更新 settings.json...")

    # 新的配置
    new_config = {
        "hooks": {
            "UserPromptSubmit": [
                {
                    "matcher": "*",
                    "hooks": [
                        {
                            "type": "command",
                            "command": f"{python_cmd} .claude/skills/chat-record/chat_recorder.py"
                        }
                    ],
                    "description": "记录用户输入"
                }
            ],
            "PostToolUse": [
                {
                    "matcher": "*",
                    "hooks": [
                        {
                            "type": "command",
                            "command": f"{python_cmd} .claude/skills/chat-record/chat_recorder.py"
                        }
                    ],
                    "description": "记录AI工具调用"
                }
            ],
            "Stop": [
                {
                    "matcher": "*",
                    "hooks": [
                        {
                            "type": "command",
                            "command": f"{python_cmd} .claude/skills/chat-record/chat_recorder.py"
                        },
                        {
                            "type": "command",
                            "command": f"{python_cmd} .claude-hooks/session_end_summary.py",
                            "timeout": 10
                        }
                    ],
                    "description": "生成会话总结"
                }
            ]
        }
    }

    import json
    with open(settings_file, 'w', encoding='utf-8') as f:
        json.dump(new_config, f, indent=2, ensure_ascii=False)

    print(f"  ✓ 已更新 {settings_file}")
    print("settings.json 更新完成！")


def main():
    """主函数"""
    print("=" * 60)
    print("CC-Scaffold 组件安装脚本")
    print("=" * 60)
    print()

    # 获取目标项目路径
    if len(sys.argv) > 1:
        target_project = sys.argv[1]
    else:
        target_project = os.getcwd()

    target_root = Path(target_project)
    print(f"目标项目路径: {target_root}")
    print()

    # Python 命令选择
    python_cmd = interactive_python_command_selection()
    if python_cmd is None:
        print("未选择 Python 命令，安装已取消")
        return

    print(f"\n使用 Python 命令: {python_cmd}")
    print()

    # 确认安装
    response = input("是否继续安装？(y/n): ")
    if response.lower() != 'y':
        print("安装已取消")
        return

    print()
    print("开始安装...")
    print()

    # 安装组件
    install_chat_record(target_root)
    print()
    install_speckit_agent(target_root)
    print()
    update_settings_json(target_root, python_cmd)
    print()

    print("=" * 60)
    print("安装完成！")
    print("=" * 60)
    print()
    print("请重启 Claude Code 以使更改生效。")
    print()
    print("已安装的组件:")
    print("  - chat-record: 会话记录功能")
    print("  - speckitAgent: SpecKit Agent")
    print("  - loadLastSession: 加载上一次会话命令")
    print()
    print(f"配置的 Python 命令: {python_cmd}")
    print()


if __name__ == '__main__':
    main()
