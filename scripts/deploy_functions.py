#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-
"""
CC-Scaffold 功能部署脚本
将 CC-Scaffold 的所有功能部署到目标项目
"""

import os
import sys
import shutil
import json
import subprocess
from pathlib import Path


def get_ccscaffold_root():
    """获取 CC-Scaffold 根目录"""
    script_dir = Path(__file__).resolve().parent
    return script_dir.parent


def detect_python_command():
    """检测可用的 Python 命令"""
    candidates = ['python3.9', 'python39', 'python3', 'python']
    available = []

    for cmd in candidates:
        try:
            result = subprocess.run(
                [cmd, '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                version = result.stdout.strip().replace('Python ', '')
                available.append((cmd, version))
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue

    return available


def select_python_command():
    """让用户选择 Python 命令"""
    print("\n检测可用的 Python 版本...")
    available = detect_python_command()

    if not available:
        print("警告: 未检测到可用的 Python 命令")
        print("请手动输入 Python 命令（如: python39, python3.9, python3）")
        return input("Python 命令: ").strip() or "python39"

    print("\n可用的 Python 版本:")
    for i, (cmd, version) in enumerate(available, 1):
        print(f"  {i}. {cmd} ({version})")
    print(f"  {len(available) + 1}. 自定义")

    while True:
        choice = input(f"\n请选择 [1-{len(available) + 1}]，默认使用 python39: ").strip()

        if not choice:
            return "python39"

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(available):
                return available[idx][0]
            elif idx == len(available):
                return input("请输入 Python 命令: ").strip() or "python39"
            else:
                print("无效的选择，请重新输入")
        except ValueError:
            print("请输入数字")


def deploy_to_target(target_dir, python_cmd=None):
    """部署功能到目标目录"""
    ccscaffold_root = get_ccscaffold_root()
    target_root = Path(target_dir).resolve()

    if not target_root.exists():
        print(f"错误: 目标目录不存在: {target_root}")
        return False

    print(f"部署 CC-Scaffold 功能到: {target_root}")
    print()

    # 如果没有指定 Python 命令，让用户选择
    if python_cmd is None:
        python_cmd = select_python_command()

    print(f"\n使用 Python 命令: {python_cmd}")
    print()

    # 创建目标目录
    target_skills = target_root / '.claude' / 'skills'
    target_scripts_hooks = target_root / '.claude' / 'scripts' / 'hooks'
    target_commands = target_root / '.claude' / 'commands'
    target_agents = target_root / '.claude' / 'agents'

    target_skills.mkdir(parents=True, exist_ok=True)
    target_scripts_hooks.mkdir(parents=True, exist_ok=True)
    target_commands.mkdir(parents=True, exist_ok=True)
    target_agents.mkdir(parents=True, exist_ok=True)

    # 1. 部署 chat-record skill
    print("1. 部署会话记录功能...")
    chat_recorder_src = ccscaffold_root / '.claude' / 'skills' / 'chat-recorder'
    chat_recorder_dst = target_skills / 'chat-recorder'

    if chat_recorder_dst.exists():
        shutil.rmtree(chat_recorder_dst)
    shutil.copytree(chat_recorder_src, chat_recorder_dst)
    print(f"   ✓ chat-recorder skill 已部署")

    # 2. 部署 continuous-learning skill
    print("2. 部署持续学习功能...")
    continuous_learning_src = ccscaffold_root / '.claude' / 'skills' / 'continuous-learning'
    continuous_learning_dst = target_skills / 'continuous-learning'

    if continuous_learning_dst.exists():
        shutil.rmtree(continuous_learning_dst)
    shutil.copytree(continuous_learning_src, continuous_learning_dst)

    # 修复 skill.json 中的 handler 路径
    skill_json = continuous_learning_dst / 'skill.json'
    if skill_json.exists():
        with open(skill_json, 'r', encoding='utf-8') as f:
            skill_config = json.load(f)
        # 修复 handler 路径
        if 'commands' in skill_config:
            for cmd in skill_config['commands']:
                if 'handler' in cmd:
                    # 将 ${PROJECT_DIR}/skills 替换为实际路径
                    cmd['handler'] = cmd['handler'].replace(
                        'python3 ${PROJECT_DIR}/skills/',
                        f'{python_cmd} .claude/skills/'
                    )
        with open(skill_json, 'w', encoding='utf-8') as f:
            json.dump(skill_config, f, ensure_ascii=False, indent=2)
    print(f"   ✓ continuous-learning skill 已部署")

    # 3. 部署 hooks
    print("3. 部署 hooks...")
    # 部署 chat-record hooks
    hooks_src = ccscaffold_root / '.claude' / 'scripts' / 'hooks' / 'chat-record'
    hooks_dst = target_scripts_hooks / 'chat-record'

    if hooks_dst.exists():
        shutil.rmtree(hooks_dst)
    shutil.copytree(hooks_src, hooks_dst)
    print(f"   ✓ chat-record hooks 已部署")

    # 部署 continuous-learning hooks
    cl_hooks_src = ccscaffold_root / '.claude' / 'scripts' / 'hooks' / 'continuous-learning'
    cl_hooks_dst = target_scripts_hooks / 'continuous-learning'

    if cl_hooks_dst.exists():
        shutil.rmtree(cl_hooks_dst)
    shutil.copytree(cl_hooks_src, cl_hooks_dst)
    print(f"   ✓ continuous-learning hooks 已部署")

    # 部署 console-cleaner hooks
    console_hooks_src = ccscaffold_root / '.claude' / 'scripts' / 'hooks' / 'console-cleaner'
    console_hooks_dst = target_scripts_hooks / 'console-cleaner'

    if console_hooks_src.exists():
        if console_hooks_dst.exists():
            shutil.rmtree(console_hooks_dst)
        shutil.copytree(console_hooks_src, console_hooks_dst)
        print(f"   ✓ console-cleaner hooks 已部署")

    # 4. 部署命令
    print("4. 部署命令...")
    # 部署 loadLastSession 命令
    command_src = ccscaffold_root / '.claude' / 'commands' / 'loadLastSession.md'
    command_dst = target_commands / 'loadLastSession.md'

    if command_dst.exists():
        command_dst.unlink()
    shutil.copy2(command_src, command_dst)
    print(f"   ✓ loadLastSession 命令已部署")

    # 部署 summary-skills 命令
    summary_cmd_src = ccscaffold_root / '.claude' / 'commands' / 'summary-skills.md'
    summary_cmd_dst = target_commands / 'summary-skills.md'

    if summary_cmd_src.exists():
        if summary_cmd_dst.exists():
            summary_cmd_dst.unlink()
        shutil.copy2(summary_cmd_src, summary_cmd_dst)
        print(f"   ✓ summary-skills 命令已部署")

    # 5. 部署 agent
    print("5. 部署 agent...")
    agent_src = ccscaffold_root / '.claude' / 'agents' / 'speckitAgent.md'
    agent_dst = target_agents / 'speckitAgent.md'

    if agent_dst.exists():
        agent_dst.unlink()
    shutil.copy2(agent_src, agent_dst)
    print(f"   ✓ speckitAgent 已部署")

    # 6. 更新或创建 settings.json
    print("6. 配置 settings.json...")
    settings_file = target_root / '.claude' / 'settings.json'

    # 新的配置（使用用户选择的 Python 命令）
    new_config = {
        "hooks": {
            "SessionStart": [
                {
                    "matcher": "*",
                    "hooks": [
                        {
                            "type": "command",
                            "command": f"{python_cmd} .claude/skills/chat-recorder/chat_recorder.py"
                        }
                    ],
                    "description": "创建新对话记录文件"
                }
            ],
            "UserPromptSubmit": [
                {
                    "matcher": "*",
                    "hooks": [
                        {
                            "type": "command",
                            "command": f"{python_cmd} .claude/skills/chat-recorder/chat_recorder.py"
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
                            "command": f"{python_cmd} .claude/skills/chat-recorder/chat_recorder.py"
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
                            "command": f"{python_cmd} .claude/skills/chat-recorder/chat_recorder.py"
                        },
                        {
                            "type": "command",
                            "command": f"{python_cmd} .claude/scripts/hooks/chat-record/session_end_summary.py",
                            "timeout": 10
                        },
                        {
                            "type": "command",
                            "command": f"{python_cmd} .claude/scripts/hooks/continuous-learning/session_end_continuous_learning.py",
                            "timeout": 60
                        },
                        {
                            "type": "command",
                            "command": f"{python_cmd} .claude/scripts/hooks/console-cleaner/clean_console_log.py",
                            "timeout": 30
                        }
                    ],
                    "description": "会话结束处理：总结、持续学习、清理console.log"
                }
            ]
        }
    }

    # 如果已有配置，需要合并
    if settings_file.exists():
        try:
            with open(settings_file, 'r', encoding='utf-8') as f:
                existing_config = json.load(f)

            # 合并 hooks
            if 'hooks' in existing_config:
                for event, hooks_list in new_config['hooks'].items():
                    if event not in existing_config['hooks']:
                        existing_config['hooks'][event] = []
                    existing_config['hooks'][event] = hooks_list

            with open(settings_file, 'w', encoding='utf-8') as f:
                json.dump(existing_config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"   ! 合并配置失败，使用新配置: {e}")
            with open(settings_file, 'w', encoding='utf-8') as f:
                json.dump(new_config, f, indent=2, ensure_ascii=False)
    else:
        with open(settings_file, 'w', encoding='utf-8') as f:
            json.dump(new_config, f, indent=2, ensure_ascii=False)

    print(f"   ✓ settings.json 已更新")

    print()
    print("=" * 60)
    print("部署完成！")
    print("=" * 60)
    print()
    print("已部署的功能:")
    print("  - chat-record: 会话记录功能")
    print("  - continuous-learning: 持续学习功能 (/summary-skills)")
    print("  - session_end_summary: 会话总结钩子")
    print("  - session_end_continuous_learning: 会话结束自动触发持续学习")
    print("  - console-cleaner: 自动扫描并清理前端代码中的 console.log")
    print("  - loadLastSession: 加载上一次会话命令")
    print("  - speckitAgent: SpecKit Agent")
    print()
    print(f"配置的 Python 命令: {python_cmd}")
    print()
    print("请重启目标项目的 Claude Code 以使更改生效。")
    print()

    return True


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python deploy_functions.py <目标目录> [Python命令]")
        print()
        print("参数:")
        print("  目标目录   - 要部署到的项目目录")
        print("  Python命令 - 可选，指定 Python 命令（如: python3.9, python39, python3）")
        print("              如果不指定，会自动检测并提示选择")
        print()
        print("示例:")
        print("  python deploy_functions.py /path/to/target/project")
        print("  python deploy_functions.py /path/to/target/project python3.9")
        print("  python deploy_functions.py . python3")
        sys.exit(1)

    target_dir = sys.argv[1]
    python_cmd = sys.argv[2] if len(sys.argv) > 2 else None

    print("=" * 60)
    print("CC-Scaffold 功能部署")
    print("=" * 60)

    success = deploy_to_target(target_dir, python_cmd)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
