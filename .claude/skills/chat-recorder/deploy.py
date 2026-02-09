#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chat Recorder 部署脚本

将 chat_recorder 部署到指定的项目目录
"""

import os
import sys
import shutil
from pathlib import Path


def get_python_command():
    """检测系统的Python命令"""
    import platform
    system = platform.system()

    if system == 'Linux' or system == 'Darwin':  # Linux或Mac
        # 优先使用python3.9，其次python3，最后python
        for cmd in ['python3.9', 'python3', 'python']:
            try:
                import subprocess
                result = subprocess.run(['which', cmd], capture_output=True, text=True)
                if result.returncode == 0:
                    return cmd
            except:
                pass
        return 'python3.9'  # 默认
    else:  # Windows
        return 'python39'


def deploy_chat_recorder(target_project_path):
    """部署 chat_recorder 到目标项目"""

    target_path = Path(target_project_path).resolve()

    if not target_path.exists():
        print(f"错误：目标路径不存在: {target_path}")
        return False

    # 创建必要的目录
    target_skills_dir = target_path / '.claude' / 'skills' / 'chat-recorder'
    target_skills_dir.mkdir(parents=True, exist_ok=True)

    # 获取当前脚本所在目录
    current_dir = Path(__file__).parent.resolve()
    source_file = current_dir / 'chat_recorder.py'

    if not source_file.exists():
        print(f"错误：找不到源文件: {source_file}")
        return False

    # 复制 chat_recorder.py
    target_file = target_skills_dir / 'chat_recorder.py'

    try:
        # 检查源文件和目标文件是否相同
        source_file_resolved = source_file.resolve()
        target_file_resolved = target_file.resolve()

        if source_file_resolved == target_file_resolved:
            print(f"源文件和目标文件相同，跳过复制")
        else:
            shutil.copy2(source_file, target_file)
            print(f"已复制: {target_file}")
    except Exception as e:
        print(f"复制文件时出错: {e}")
        return False

    # 获取合适的Python命令
    python_cmd = get_python_command()

    # 创建或更新 settings.json
    settings_file = target_path / '.claude' / 'settings.json'

    hooks_config = {
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
                        }
                    ],
                    "description": "清理空文件，记录结束时间"
                }
            ]
        }
    }

    import json

    # 如果 settings.json 已存在，读取并合并
    if settings_file.exists():
        try:
            with open(settings_file, 'r', encoding='utf-8') as f:
                existing_config = json.load(f)

            # 合并 hooks 配置
            if 'hooks' not in existing_config:
                existing_config['hooks'] = {}

            existing_config['hooks'].update(hooks_config['hooks'])

            hooks_config = existing_config
            print(f"已更新现有配置: {settings_file}")
        except Exception as e:
            print(f"警告：读取现有配置失败: {e}，将创建新配置")

    # 写入配置文件
    with open(settings_file, 'w', encoding='utf-8') as f:
        json.dump(hooks_config, f, indent=2, ensure_ascii=False)

    print(f"已创建/更新配置: {settings_file}")
    print(f"\n部署完成！chat_recorder 已安装到: {target_path}")
    print(f"\n配置信息：")
    print(f"- Python命令: {python_cmd}")
    print(f"- 记录文件位置: {target_path / '.claude' / 'conversations'}")
    print(f"\n下一步：")
    print(f"1. 确保系统已安装 {python_cmd} 或修改 .claude/settings.json 中的命令")
    print(f"2. 重启 Claude Code 使 hooks 生效")

    return True


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("Chat Recorder 部署工具")
        print("\n用法:")
        print("  python3 deploy.py <目标项目路径>")
        print("  python39 deploy.py <目标项目路径>")
        print("\n示例:")
        print("  python3 deploy.py /path/to/your/project")
        print("  python3 deploy.py ..")
        print("  python3 deploy.py ~/my-project")
        print("\n注意:")
        print("  如果在目标项目的 .claude/skills/chat-recorder 目录中运行，")
        print("  可以使用 '.' 或 '..' 作为目标路径")
        sys.exit(1)

    target_path = sys.argv[1]

    if deploy_chat_recorder(target_path):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
