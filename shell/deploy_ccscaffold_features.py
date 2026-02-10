#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CC-Scaffold 功能部署脚本

将 chat-record 和 continuous-learning 功能部署到目标项目
"""

import os
import sys
import shutil
import json
from pathlib import Path


def get_python_command():
    """检测系统的Python命令"""
    import platform
    system = platform.system()

    if system == 'Linux' or system == 'Darwin':  # Linux或Mac
        for cmd in ['python3.9', 'python3', 'python']:
            try:
                import subprocess
                result = subprocess.run(['which', cmd], capture_output=True, text=True)
                if result.returncode == 0:
                    return cmd
            except:
                pass
        return 'python3.9'
    else:  # Windows
        return 'python39'


def deploy_chat_record(target_path, python_cmd='python3.9'):
    """部署 chat-record 功能"""
    print(f"\n{'='*60}")
    print("部署 Chat Record 功能")
    print(f"{'='*60}")

    target_path = Path(target_path).resolve()

    # 创建必要的目录
    target_skills_dir = target_path / '.claude' / 'skills' / 'chat-record'
    target_skills_dir.mkdir(parents=True, exist_ok=True)

    # 复制 chat_recorder.py
    source_file = Path(__file__).parent.parent / '.claude' / 'skills' / 'chat-record' / 'chat_recorder.py'
    target_file = target_skills_dir / 'chat_recorder.py'

    if source_file.exists():
        try:
            source_resolved = source_file.resolve()
            target_resolved = target_file.resolve()
            if source_resolved != target_resolved:
                shutil.copy2(source_file, target_file)
                print(f"已复制: {target_file}")
            else:
                print(f"跳过（源文件和目标文件相同）: {target_file}")
        except Exception as e:
            print(f"警告：复制文件时出错: {e}")
    else:
        print(f"警告：找不到源文件: {source_file}")

    # 复制 debug 脚本
    debug_source = Path(__file__).parent.parent / '.claude' / 'skills' / 'chat-record' / 'chat_recorder_debug.py'
    debug_target = target_skills_dir / 'chat_recorder_debug.py'
    if debug_source.exists():
        try:
            debug_resolved = debug_source.resolve()
            debug_target_resolved = debug_target.resolve()
            if debug_resolved != debug_target_resolved:
                shutil.copy2(debug_source, debug_target)
                print(f"已复制: {debug_target}")
            else:
                print(f"跳过（源文件和目标文件相同）: {debug_target}")
        except Exception as e:
            print(f"警告：复制文件时出错: {e}")

    # 复制 session_end_summary.py
    hooks_dir = target_path / '.claude' / 'scripts' / 'hooks' / 'chat-record'
    hooks_dir.mkdir(parents=True, exist_ok=True)

    summary_source = Path(__file__).parent.parent / '.claude' / 'scripts' / 'hooks' / 'chat-record' / 'session_end_summary.py'
    summary_target = hooks_dir / 'session_end_summary.py'
    if summary_source.exists():
        try:
            summary_resolved = summary_source.resolve()
            summary_target_resolved = summary_target.resolve()
            if summary_resolved != summary_target_resolved:
                shutil.copy2(summary_source, summary_target)
                print(f"已复制: {summary_target}")
            else:
                print(f"跳过（源文件和目标文件相同）: {summary_target}")
        except Exception as e:
            print(f"警告：复制文件时出错: {e}")

    # 复制 console-cleaner 钩子
    console_cleaner_dir = target_path / '.claude' / 'scripts' / 'hooks' / 'console-cleaner'
    console_cleaner_dir.mkdir(parents=True, exist_ok=True)

    # 复制 console cleaner 脚本
    cleaner_script_source = Path(__file__).parent.parent / '.claude' / 'scripts' / 'hooks' / 'console-cleaner' / 'clean_console_log.py'
    cleaner_script_target = console_cleaner_dir / 'clean_console_log.py'
    if cleaner_script_source.exists():
        try:
            cleaner_resolved = cleaner_script_source.resolve()
            cleaner_target_resolved = cleaner_script_target.resolve()
            if cleaner_resolved != cleaner_target_resolved:
                shutil.copy2(cleaner_script_source, cleaner_script_target)
                print(f"已复制: {cleaner_script_target}")
            else:
                print(f"跳过（源文件和目标文件相同）: {cleaner_script_target}")
        except Exception as e:
            print(f"警告：复制文件时出错: {e}")

    # 复制 console cleaner 配置
    cleaner_config_source = Path(__file__).parent.parent / '.claude' / 'scripts' / 'hooks' / 'console-cleaner' / 'config.json'
    cleaner_config_target = console_cleaner_dir / 'config.json'
    if cleaner_config_source.exists():
        try:
            config_resolved = cleaner_config_source.resolve()
            config_target_resolved = cleaner_config_target.resolve()
            if config_resolved != config_target_resolved:
                shutil.copy2(cleaner_config_source, cleaner_config_target)
                print(f"已复制: {cleaner_config_target}")
            else:
                print(f"跳过（源文件和目标文件相同）: {cleaner_config_target}")
        except Exception as e:
            print(f"警告：复制文件时出错: {e}")

    # 复制命令文件
    commands_dir = target_path / '.claude' / 'commands'
    commands_dir.mkdir(parents=True, exist_ok=True)

    load_session_source = Path(__file__).parent.parent / '.claude' / 'commands' / 'loadLastSession.md'
    load_session_target = commands_dir / 'loadLastSession.md'
    if load_session_source.exists():
        try:
            load_resolved = load_session_source.resolve()
            load_target_resolved = load_session_target.resolve()
            if load_resolved != load_target_resolved:
                shutil.copy2(load_session_source, load_session_target)
                print(f"已复制: {load_session_target}")
            else:
                print(f"跳过（源文件和目标文件相同）: {load_session_target}")
        except Exception as e:
            print(f"警告：复制文件时出错: {e}")

    # 更新 settings.json
    settings_file = target_path / '.claude' / 'settings.json'

    hooks_config = {
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
                    "matcher": "^(?!Read|Grep|Glob|WebSearch|WebFetch|TaskOutput|mcp__|4_5v_mcp__|context7|web-reader|zai-mcp-server).*$",
                    "hooks": [
                        {
                            "type": "command",
                            "command": f"{python_cmd} .claude/skills/chat-record/chat_recorder.py"
                        }
                    ],
                    "description": "记录AI工具调用（过滤读命令）"
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
                            "command": f"{python_cmd} .claude/scripts/hooks/chat-record/session_end_summary.py",
                            "timeout": 10
                        },
                        {
                            "type": "command",
                            "command": f"{python_cmd} .claude/scripts/hooks/console-cleaner/clean_console_log.py",
                            "timeout": 30
                        }
                    ],
                    "description": "会话结束处理：记录、总结、清理console.log"
                }
            ]
        }
    }

    # 合并现有配置
    if settings_file.exists():
        try:
            with open(settings_file, 'r', encoding='utf-8') as f:
                existing_config = json.load(f)

            if 'hooks' not in existing_config:
                existing_config['hooks'] = {}

            existing_config['hooks'].update(hooks_config['hooks'])
            hooks_config = existing_config
            print(f"已更新现有配置: {settings_file}")
        except Exception as e:
            print(f"警告：读取现有配置失败: {e}")

    with open(settings_file, 'w', encoding='utf-8') as f:
        json.dump(hooks_config, f, indent=2, ensure_ascii=False)

    print(f"已创建/更新配置: {settings_file}")


def deploy_continuous_learning(target_path, python_cmd='python3.9'):
    """部署 continuous-learning 功能"""
    print(f"\n{'='*60}")
    print("部署 Continuous Learning 功能")
    print(f"{'='*60}")

    target_path = Path(target_path).resolve()

    # 创建必要的目录
    target_skills_dir = target_path / '.claude' / 'skills' / 'continuous-learning'
    target_skills_dir.mkdir(parents=True, exist_ok=True)

    # 复制所有脚本文件
    source_scripts_dir = Path(__file__).parent.parent / '.claude' / 'skills' / 'continuous-learning' / 'scripts'

    if source_scripts_dir.exists():
        for script_file in source_scripts_dir.glob('*.py'):
            target_file = target_skills_dir / 'scripts' / script_file.name
            target_skills_dir.joinpath('scripts').mkdir(exist_ok=True)
            try:
                source_resolved = script_file.resolve()
                target_resolved = target_file.resolve()
                if source_resolved != target_resolved:
                    shutil.copy2(script_file, target_file)
                    print(f"已复制: {target_file}")
                else:
                    print(f"跳过（源文件和目标文件相同）: {target_file}")
            except Exception as e:
                print(f"警告：复制文件时出错: {e}")

    # 复制配置文件
    config_source = Path(__file__).parent.parent / '.claude' / 'skills' / 'continuous-learning' / 'config.json'
    config_target = target_skills_dir / 'config.json'
    if config_source.exists():
        try:
            config_resolved = config_source.resolve()
            config_target_resolved = config_target.resolve()
            if config_resolved != config_target_resolved:
                shutil.copy2(config_source, config_target)
                print(f"已复制: {config_target}")
            else:
                print(f"跳过（源文件和目标文件相同）: {config_target}")
        except Exception as e:
            print(f"警告：复制文件时出错: {e}")

    # 复制命令文件
    commands_dir = target_path / '.claude' / 'commands'
    commands_dir.mkdir(parents=True, exist_ok=True)

    summary_source = Path(__file__).parent.parent / '.claude' / 'commands' / 'summary-skills.md'
    summary_target = commands_dir / 'summary-skills.md'
    if summary_source.exists():
        try:
            summary_resolved = summary_source.resolve()
            summary_target_resolved = summary_target.resolve()
            if summary_resolved != summary_target_resolved:
                shutil.copy2(summary_source, summary_target)
                print(f"已复制: {summary_target}")
            else:
                print(f"跳过（源文件和目标文件相同）: {summary_target}")
        except Exception as e:
            print(f"警告：复制文件时出错: {e}")

    # 创建输出目录
    output_dir = target_path / '.claude' / 'skills' / 'learn'
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"已创建输出目录: {output_dir}")

    print(f"\nContinuous Learning 功能部署完成！")
    print(f"使用方法：")
    print(f"  /summary-skills")
    print(f"  /summary-skills 帮我总结最近关于分时图的修改经验")


def deploy_all(target_project_path):
    """部署所有功能到目标项目"""
    target_path = Path(target_project_path).resolve()

    if not target_path.exists():
        print(f"错误：目标路径不存在: {target_path}")
        return False

    python_cmd = get_python_command()

    print(f"{'='*60}")
    print(f"部署 CC-Scaffold 功能到: {target_path}")
    print(f"Python 命令: {python_cmd}")
    print(f"{'='*60}")

    # 部署 chat-record
    deploy_chat_record(target_path, python_cmd)

    # 部署 continuous-learning
    deploy_continuous_learning(target_path, python_cmd)

    print(f"\n{'='*60}")
    print(f"部署完成！")
    print(f"{'='*60}")
    print(f"\n已部署的功能：")
    print(f"1. Chat Record - 对话记录（含读命令过滤）")
    print(f"2. Continuous Learning - 持续学习（支持主题参数）")
    print(f"3. Console Cleaner - SessionEnd 时自动清理 console.log")
    print(f"\n下一步：")
    print(f"1. 重启 Claude Code 使功能生效")
    print(f"2. 使用 /summary-skills 命令进行技能总结")
    print(f"3. SessionEnd 时会自动清理前端代码中的 console.log")

    return True


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("CC-Scaffold 功能部署工具")
        print("\n用法:")
        print("  python3.9 deploy_ccscaffold_features.py <目标项目路径>")
        print("\n示例:")
        print("  python3.9 deploy_ccscaffold_features.py /Users/ming/Work/stock_analysis")
        print("  python3.9 deploy_ccscaffold_features.py .")
        sys.exit(1)

    target_path = sys.argv[1]

    if deploy_all(target_path):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
