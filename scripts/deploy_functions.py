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
from pathlib import Path


def get_ccscaffold_root():
    """获取 CC-Scaffold 根目录"""
    script_dir = Path(__file__).resolve().parent
    return script_dir.parent


def deploy_to_target(target_dir):
    """部署功能到目标目录"""
    ccscaffold_root = get_ccscaffold_root()
    target_root = Path(target_dir).resolve()

    if not target_root.exists():
        print(f"错误: 目标目录不存在: {target_root}")
        return False

    print(f"部署 CC-Scaffold 功能到: {target_root}")
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

    # 2. 部署 hooks
    print("2. 部署 hooks...")
    hooks_src = ccscaffold_root / '.claude' / 'scripts' / 'hooks' / 'chat-record'
    hooks_dst = target_scripts_hooks / 'chat-record'

    if hooks_dst.exists():
        shutil.rmtree(hooks_dst)
    shutil.copytree(hooks_src, hooks_dst)
    print(f"   ✓ hooks 已部署")

    # 3. 部署命令
    print("3. 部署命令...")
    command_src = ccscaffold_root / '.claude' / 'commands' / 'loadLastSession.md'
    command_dst = target_commands / 'loadLastSession.md'

    if command_dst.exists():
        command_dst.unlink()
    shutil.copy2(command_src, command_dst)
    print(f"   ✓ loadLastSession 命令已部署")

    # 4. 部署 agent
    print("4. 部署 agent...")
    agent_src = ccscaffold_root / '.claude' / 'agents' / 'speckitAgent.md'
    agent_dst = target_agents / 'speckitAgent.md'

    if agent_dst.exists():
        agent_dst.unlink()
    shutil.copy2(agent_src, agent_dst)
    print(f"   ✓ speckitAgent 已部署")

    # 5. 更新或创建 settings.json
    print("5. 配置 settings.json...")
    settings_file = target_root / '.claude' / 'settings.json'

    # 新的配置
    new_config = {
        "hooks": {
            "UserPromptSubmit": [
                {
                    "matcher": "*",
                    "hooks": [
                        {
                            "type": "command",
                            "command": "python39 .claude/skills/chat-recorder/chat_recorder.py"
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
                            "command": "python39 .claude/skills/chat-recorder/chat_recorder.py"
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
                            "command": "python39 .claude/skills/chat-recorder/chat_recorder.py"
                        },
                        {
                            "type": "command",
                            "command": "python39 .claude/scripts/hooks/chat-record/session_end_summary.py",
                            "timeout": 10
                        }
                    ],
                    "description": "生成会话总结"
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
    print("  - session_end_summary: 会话总结钩子")
    print("  - loadLastSession: 加载上一次会话命令")
    print("  - speckitAgent: SpecKit Agent")
    print()
    print("请重启目标项目的 Claude Code 以使更改生效。")
    print()

    return True


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python deploy_functions.py <目标目录>")
        print()
        print("示例:")
        print("  python deploy_functions.py /path/to/target/project")
        print("  python deploy_functions.py .")
        sys.exit(1)

    target_dir = sys.argv[1]

    print("=" * 60)
    print("CC-Scaffold 功能部署")
    print("=" * 60)
    print()

    success = deploy_to_target(target_dir)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
