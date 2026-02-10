#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CC-Scaffold 用户级别安装脚本
将组件安装到用户级别的 ~/.claude/ 目录
"""

import os
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime


def get_user_claude_dir():
    """获取用户级别的 .claude 目录"""
    home = Path.home()
    return home / '.claude'


def get_source_root():
    """获取 ccscaffold 项目根目录"""
    return Path(__file__).resolve().parent.parent


def backup_settings(user_claude_dir):
    """备份现有的 settings.json"""
    settings_file = user_claude_dir / 'settings.json'
    if settings_file.exists():
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = user_claude_dir / f'settings.json.bak.{timestamp}'
        shutil.copy2(settings_file, backup_file)
        print(f"  [OK] 已备份 settings.json -> {backup_file.name}")
        return True
    return False


def copy_dir(src, dst, label=""):
    """复制目录, 如果目标存在则先删除"""
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    print(f"  [OK] {label}: {dst.relative_to(get_user_claude_dir())}")


def copy_file(src, dst, label=""):
    """复制文件"""
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    print(f"  [OK] {label}: {dst.relative_to(get_user_claude_dir())}")


def install_chat_record(source_root, user_claude_dir):
    """安装 chat-record 组件"""
    print("\n[1/3] 安装 chat-record (会话记录)...")

    # 1. 复制 skills/chat-record
    src = source_root / '.claude' / 'skills' / 'chat-record'
    dst = user_claude_dir / 'skills' / 'chat-record'
    copy_dir(src, dst, "skill")

    # 2. 复制 scripts/hooks/chat-record
    src = source_root / '.claude' / 'scripts' / 'hooks' / 'chat-record'
    dst = user_claude_dir / 'scripts' / 'hooks' / 'chat-record'
    copy_dir(src, dst, "hook")

    # 3. 复制 commands/loadLastSession.md
    src = source_root / 'chat-record' / 'commands' / 'loadLastSession.md'
    dst = user_claude_dir / 'commands' / 'loadLastSession.md'
    copy_file(src, dst, "command")

    print("  chat-record 安装完成!")


def install_continuous_learning(source_root, user_claude_dir):
    """安装 continuous-learning 组件"""
    print("\n[2/3] 安装 continuous-learning (持续学习)...")

    # 1. 复制 skills/continuous-learning (包含 scripts 子目录)
    src = source_root / '.claude' / 'skills' / 'continuous-learning'
    dst = user_claude_dir / 'skills' / 'continuous-learning'
    # 复制时排除 __pycache__ 和 state.json
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(
        src, dst,
        ignore=shutil.ignore_patterns('__pycache__', '*.pyc', 'state.json')
    )
    print(f"  [OK] skill: skills/continuous-learning")

    # 2. 复制 scripts/hooks/continuous-learning
    src = source_root / '.claude' / 'scripts' / 'hooks' / 'continuous-learning'
    dst = user_claude_dir / 'scripts' / 'hooks' / 'continuous-learning'
    copy_dir(src, dst, "hook")

    # 3. 复制 skills/learn 目录 (已学习的技能)
    src = source_root / '.claude' / 'skills' / 'learn'
    dst = user_claude_dir / 'skills' / 'learn'
    if src.exists():
        if dst.exists():
            # 合并而不是覆盖
            for item in src.iterdir():
                dst_item = dst / item.name
                if not dst_item.exists():
                    shutil.copy2(item, dst_item)
                    print(f"  [OK] learned skill: skills/learn/{item.name}")
        else:
            copy_dir(src, dst, "learned skills")

    print("  continuous-learning 安装完成!")


def install_console_cleaner(source_root, user_claude_dir):
    """安装 console-cleaner 组件"""
    print("\n[3/3] 安装 console-cleaner (控制台清理)...")

    src = source_root / '.claude' / 'scripts' / 'hooks' / 'console-cleaner'
    dst = user_claude_dir / 'scripts' / 'hooks' / 'console-cleaner'
    copy_dir(src, dst, "hook")

    print("  console-cleaner 安装完成!")


def create_directories(user_claude_dir):
    """创建必要的目录结构"""
    print("\n创建目录结构...")

    dirs = [
        user_claude_dir / 'conversations',
        user_claude_dir / 'logs',
        user_claude_dir / 'tmp',
        user_claude_dir / 'commands',
        user_claude_dir / 'skills' / 'learn',
        user_claude_dir / 'scripts' / 'hooks',
    ]

    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
        print(f"  [OK] {d.relative_to(user_claude_dir)}/")


def merge_settings(user_claude_dir, python_cmd):
    """合并 settings.json 配置"""
    print("\n合并 settings.json...")

    settings_file = user_claude_dir / 'settings.json'

    # 读取现有配置 (优先读取 .bak 文件, 因为其中可能有更完整的配置)
    existing = {}
    bak_file = user_claude_dir / 'settings.json.bak'
    if bak_file.exists():
        with open(bak_file, 'r', encoding='utf-8') as f:
            existing = json.load(f)
    if settings_file.exists():
        with open(settings_file, 'r', encoding='utf-8') as f:
            current = json.load(f)
        # 用 bak 作为基础, 再用当前配置覆盖非 hooks 字段
        for key in current:
            if key != 'hooks':
                existing.setdefault(key, current[key])

    # 保留现有的关键配置
    env = existing.get('env', {})
    permissions = existing.get('permissions', {})
    plugins = existing.get('enabledPlugins', {})
    always_thinking = existing.get('alwaysThinkingEnabled', True)

    # 获取现有的 hooks
    existing_hooks = existing.get('hooks', {})

    # --- 构建新的 hooks 配置 ---

    # UserPromptSubmit: chat-record 记录用户输入
    user_prompt_hooks = [
        {
            "matcher": "*",
            "hooks": [
                {
                    "type": "command",
                    "command": (
                        f"{python_cmd} "
                        '"%USERPROFILE%\\.claude\\skills\\chat-record\\chat_recorder.py"'
                    )
                }
            ],
            "description": "chat-record: 记录用户输入"
        }
    ]

    # PostToolUse: chat-record + post_tool_use_logger(现有)
    post_tool_hooks = [
        {
            "matcher": "*",
            "hooks": [
                {
                    "type": "command",
                    "command": (
                        f"{python_cmd} "
                        '"%USERPROFILE%\\.claude\\skills\\chat-record\\chat_recorder.py"'
                    )
                },
                {
                    "type": "command",
                    "command": (
                        f"{python_cmd} "
                        '"%USERPROFILE%\\.claude\\hooks\\post_tool_use_logger.py"'
                    )
                }
            ],
            "description": "chat-record + modify-log: 记录AI工具调用和文件修改"
        }
    ]

    # Stop: chat-record + session_end_summary + continuous-learning + windows-notification(现有)
    stop_hooks = [
        {
            "matcher": "*",
            "hooks": [
                {
                    "type": "command",
                    "command": (
                        f"{python_cmd} "
                        '"%USERPROFILE%\\.claude\\skills\\chat-record\\chat_recorder.py"'
                    )
                },
                {
                    "type": "command",
                    "command": (
                        f"{python_cmd} "
                        '"%USERPROFILE%\\.claude\\scripts\\hooks\\chat-record\\session_end_summary.py"'
                    ),
                    "timeout": 15
                },
                {
                    "type": "command",
                    "command": (
                        f"{python_cmd} "
                        '"%USERPROFILE%\\.claude\\scripts\\hooks\\continuous-learning\\session_end_continuous_learning.py"'
                    ),
                    "timeout": 60
                },
                {
                    "type": "command",
                    "command": (
                        'C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe '
                        '-ExecutionPolicy Bypass -File '
                        '"%USERPROFILE%\\.claude\\hooks\\windows-notification.ps1" '
                        '-Title "Claude Code" -Message "任务已完成"'
                    ),
                    "timeout": 10
                }
            ],
            "description": "会话结束: 记录+总结+持续学习+通知"
        }
    ]

    # SessionStart: session_start_reader(现有)
    session_start_hooks = [
        {
            "matcher": "*",
            "hooks": [
                {
                    "type": "command",
                    "command": (
                        f"{python_cmd} "
                        '"%USERPROFILE%\\.claude\\hooks\\session_start_reader.py"'
                    )
                }
            ],
            "description": "会话开始: 读取修改历史"
        }
    ]

    # Notification: 保留现有的通知 hooks
    notification_hooks = existing_hooks.get('Notification', [])
    if not notification_hooks:
        notification_hooks = [
            {
                "matcher": "permission_prompt",
                "hooks": [
                    {
                        "type": "command",
                        "command": (
                            'C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe '
                            '-ExecutionPolicy Bypass -File '
                            '"%USERPROFILE%\\.claude\\hooks\\windows-notification.ps1" '
                            '-Title "Claude Code" -Message "需要权限审批"'
                        ),
                        "timeout": 10
                    }
                ]
            },
            {
                "matcher": "idle_prompt",
                "hooks": [
                    {
                        "type": "command",
                        "command": (
                            'C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe '
                            '-ExecutionPolicy Bypass -File '
                            '"%USERPROFILE%\\.claude\\hooks\\windows-notification.ps1" '
                            '-Title "Claude Code" -Message "等待你的输入"'
                        ),
                        "timeout": 10
                    }
                ]
            }
        ]

    # 组装完整配置
    new_settings = {
        "env": env,
        "permissions": permissions,
        "hooks": {
            "SessionStart": session_start_hooks,
            "UserPromptSubmit": user_prompt_hooks,
            "PostToolUse": post_tool_hooks,
            "Stop": stop_hooks,
            "Notification": notification_hooks
        },
        "enabledPlugins": plugins,
        "alwaysThinkingEnabled": always_thinking
    }

    # 写入
    with open(settings_file, 'w', encoding='utf-8') as f:
        json.dump(new_settings, f, indent=2, ensure_ascii=False)

    print(f"  [OK] settings.json 已更新")


def update_config_paths(user_claude_dir):
    """更新 continuous-learning 的 config.json 路径为用户级别"""
    print("\n更新配置文件路径...")

    config_file = user_claude_dir / 'skills' / 'continuous-learning' / 'config.json'
    if config_file.exists():
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)

        # 路径已经是相对于 .claude 的, 不需要修改
        # 但确保 skills_output_dir 指向用户级别
        config['conversation_file'] = '.claude/conversations/conversation.txt'
        config['skills_output_dir'] = '.claude/skills/learn'
        config['state_file'] = '.claude/skills/continuous-learning/state.json'

        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

        print(f"  [OK] continuous-learning/config.json")


def print_summary(user_claude_dir):
    """打印安装总结"""
    print("\n" + "=" * 60)
    print("安装完成!")
    print("=" * 60)
    print()
    print(f"安装目录: {user_claude_dir}")
    print()
    print("已安装的组件:")
    print("  1. chat-record       - 会话记录 (记录每轮对话)")
    print("  2. continuous-learning - 持续学习 (自动总结生成skill)")
    print("  3. console-cleaner   - 控制台清理 (清理console.log)")
    print()
    print("已配置的 Hooks:")
    print("  - SessionStart      : 读取修改历史")
    print("  - UserPromptSubmit  : 记录用户输入")
    print("  - PostToolUse       : 记录工具调用 + 文件修改")
    print("  - Stop              : 会话总结 + 持续学习 + 通知")
    print("  - Notification      : 权限审批/空闲提醒通知")
    print()
    print("已安装的命令:")
    print("  - /loadLastSession  : 加载上一次会话内容")
    print()
    print("请重启 Claude Code 以使更改生效。")
    print()


def main():
    """主函数"""
    print("=" * 60)
    print("CC-Scaffold 用户级别安装脚本")
    print("=" * 60)

    source_root = get_source_root()
    user_claude_dir = get_user_claude_dir()
    python_cmd = 'python39'

    print(f"\n源目录:   {source_root}")
    print(f"目标目录: {user_claude_dir}")
    print(f"Python:   {python_cmd}")

    # 1. 备份
    print("\n备份现有配置...")
    backup_settings(user_claude_dir)

    # 2. 创建目录
    create_directories(user_claude_dir)

    # 3. 安装组件
    install_chat_record(source_root, user_claude_dir)
    install_continuous_learning(source_root, user_claude_dir)
    install_console_cleaner(source_root, user_claude_dir)

    # 4. 合并 settings.json
    merge_settings(user_claude_dir, python_cmd)

    # 5. 更新配置路径
    update_config_paths(user_claude_dir)

    # 6. 打印总结
    print_summary(user_claude_dir)


if __name__ == '__main__':
    main()
