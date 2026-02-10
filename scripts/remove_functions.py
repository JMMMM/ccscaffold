#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-
"""
CC-Scaffold 功能移除脚本
从目标项目中移除 CC-Scaffold 的所有功能
"""

import os
import sys
import json
import shutil
from pathlib import Path


def remove_from_target(target_dir):
    """从目标目录移除功能"""
    target_root = Path(target_dir).resolve()

    if not target_root.exists():
        print(f"错误: 目标目录不存在: {target_root}")
        return False

    print(f"从 {target_root} 移除 CC-Scaffold 功能")
    print()

    removed_items = []
    errors = []

    # 1. 移除 chat-record skill
    print("1. 移除会话记录功能...")
    chat_recorder_dir = target_root / '.claude' / 'skills' / 'chat-record'

    if chat_recorder_dir.exists():
        shutil.rmtree(chat_recorder_dir)
        print(f"   ✓ chat-record skill 已移除")
        removed_items.append(str(chat_recorder_dir))
    else:
        print(f"   - chat-record skill 不存在，跳过")

    # 2. 移除 hooks
    print("2. 移除 hooks...")
    hooks_dir = target_root / '.claude' / 'scripts' / 'hooks' / 'chat-record'

    if hooks_dir.exists():
        shutil.rmtree(hooks_dir)
        print(f"   ✓ hooks 已移除")
        removed_items.append(str(hooks_dir))

        # 尝试删除空的父目录
        try:
            parent = hooks_dir.parent.parent
            if parent.exists() and not list(parent.iterdir()):
                parent.rmdir()
                parent = parent.parent
                if parent.exists() and not list(parent.iterdir()):
                    parent.rmdir()
        except:
            pass
    else:
        print(f"   - hooks 不存在，跳过")

    # 3. 移除命令
    print("3. 移除命令...")
    command_file = target_root / '.claude' / 'commands' / 'loadLastSession.md'

    if command_file.exists():
        command_file.unlink()
        print(f"   ✓ loadLastSession 命令已移除")
        removed_items.append(str(command_file))
    else:
        print(f"   - loadLastSession 命令不存在，跳过")

    # 4. 移除 agent
    print("4. 移除 agent...")
    agent_file = target_root / '.claude' / 'agents' / 'speckitAgent.md'

    if agent_file.exists():
        agent_file.unlink()
        print(f"   ✓ speckitAgent 已移除")
        removed_items.append(str(agent_file))
    else:
        print(f"   - speckitAgent 不存在，跳过")

    # 5. 清理 settings.json 中的相关配置
    print("5. 清理 settings.json...")
    settings_file = target_root / '.claude' / 'settings.json'

    if settings_file.exists():
        try:
            with open(settings_file, 'r', encoding='utf-8') as f:
                config = json.load(f)

            modified = False
            hooks_to_remove = ['UserPromptSubmit', 'PostToolUse', 'Stop']

            for hook_name in hooks_to_remove:
                if 'hooks' in config and hook_name in config['hooks']:
                    # 检查是否包含我们的 hooks
                    hooks_list = config['hooks'][hook_name]
                    new_hooks_list = []

                    for matcher_config in hooks_list:
                        hooks = matcher_config.get('hooks', [])
                        new_hooks = []

                        for hook in hooks:
                            command = hook.get('command', '')
                            # 如果不是我们的 hook，保留它
                            if 'chat-record' not in command and 'session_end_summary' not in command:
                                new_hooks.append(hook)
                            else:
                                modified = True

                        if new_hooks:
                            matcher_config['hooks'] = new_hooks
                            new_hooks_list.append(matcher_config)

                    if new_hooks_list:
                        config['hooks'][hook_name] = new_hooks_list
                    else:
                        del config['hooks'][hook_name]
                        modified = True

            # 如果没有 hooks 了，删除整个 hooks 配置
            if 'hooks' in config and not config['hooks']:
                del config['hooks']
                modified = True

            if modified:
                with open(settings_file, 'w', encoding='utf-8') as f:
                    json.dump(config, f, indent=2, ensure_ascii=False)
                print(f"   ✓ settings.json 已清理")
            else:
                print(f"   - settings.json 无需修改")

        except Exception as e:
            print(f"   ! 清理 settings.json 时出错: {e}")
            errors.append(str(e))
    else:
        print(f"   - settings.json 不存在，跳过")

    # 6. 移除空的 .claude-scripts/hooks 目录（如果存在）
    print("6. 清理空目录...")
    scripts_hooks_dir = target_root / '.claude' / 'scripts' / 'hooks'

    if scripts_hooks_dir.exists() and not list(scripts_hooks_dir.iterdir()):
        try:
            scripts_hooks_dir.rmdir()
            scripts_dir = scripts_hooks_dir.parent
            if scripts_dir.exists() and not list(scripts_dir.iterdir()):
                scripts_dir.rmdir()
            print(f"   ✓ 空目录已清理")
        except:
            pass

    print()
    print("=" * 60)
    print("移除完成！")
    print("=" * 60)
    print()

    if removed_items:
        print("已移除的组件:")
        for item in removed_items:
            print(f"  - {item}")
        print()

    if errors:
        print("遇到的错误:")
        for error in errors:
            print(f"  - {error}")
        print()

    print("请重启目标项目的 Claude Code 以使更改生效。")
    print()

    return True


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python remove_functions.py <目标目录>")
        print()
        print("示例:")
        print("  python remove_functions.py /path/to/target/project")
        print("  python remove_functions.py .")
        sys.exit(1)

    target_dir = sys.argv[1]

    print("=" * 60)
    print("CC-Scaffold 功能移除")
    print("=" * 60)
    print()

    success = remove_from_target(target_dir)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
