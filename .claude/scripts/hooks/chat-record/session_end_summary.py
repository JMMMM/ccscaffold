#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-
"""
SessionEnd Hook - 会话结束时生成总结和文件修改记录

钩子类型: Stop
功能：
1. 读取 conversation.txt 总结会话内容
2. 读取 modify_logs.txt 获取文件修改记录
3. 生成会话总结并保存

位置: .claude/scripts/hooks/chat-record/session_end_summary.py
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path


def get_project_root():
    """获取项目根目录"""
    # 从脚本位置向上查找项目根目录
    # 脚本位置: .claude/scripts/hooks/chat-record/session_end_summary.py
    # 需要向上4级到达项目根目录
    script_dir = Path(__file__).resolve().parent
    # .claude/scripts/hooks/chat-record -> .claude -> 项目根目录
    project_root = script_dir.parent.parent.parent.parent
    return project_root


CONFIG = {
    "conversation_file": None,
    "modify_log_file": None,
    "session_summary_file": None
}


def init_config():
    """初始化配置，设置绝对路径"""
    project_root = get_project_root()
    CONFIG["conversation_file"] = str(project_root / '.claude' / 'conversations' / 'conversation.txt')
    CONFIG["modify_log_file"] = str(project_root / 'logs' / 'modify_logs.txt')
    CONFIG["session_summary_file"] = str(project_root / '.claude' / 'conversations' / 'session_summary.txt')


def read_file_content(file_path):
    """读取文件内容"""
    file_path = Path(file_path)
    if not file_path.exists():
        return None

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    if not content.strip():
        return None

    return content


def get_file_modifications():
    """获取文件修改记录"""
    modify_logs = read_file_content(CONFIG["modify_log_file"])

    if not modify_logs:
        return "本次会话没有文件修改记录。"

    return modify_logs


def generate_session_summary():
    """生成会话总结"""
    # 读取会话内容
    conversation = read_file_content(CONFIG["conversation_file"])

    if not conversation:
        return "本次会话没有记录内容。"

    # 获取文件修改记录
    modifications = get_file_modifications()

    # 生成总结标题
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    summary = f"# 会话总结\n"
    summary += f"# 生成时间: {timestamp}\n\n"
    summary += f"## 会话内容摘要\n\n"
    summary += f"{conversation}\n\n"
    summary += f"## 文件修改记录\n\n"
    summary += f"{modifications}\n\n"
    summary += f"# " + "=" * 60 + "\n"

    return summary


def save_summary(summary):
    """保存会话总结"""
    summary_file = Path(CONFIG["session_summary_file"])
    summary_file.parent.mkdir(parents=True, exist_ok=True)

    # 追加模式保存
    with open(summary_file, 'a', encoding='utf-8') as f:
        f.write(summary)


def clear_conversation():
    """清空会话记录，为下次会话做准备"""
    conversation_file = Path(CONFIG["conversation_file"])

    if conversation_file.exists():
        conversation_file.write_text('', encoding='utf-8')


def main():
    """主函数"""
    # 初始化配置
    init_config()

    # 设置 stderr 的编码为 UTF-8
    if sys.platform == 'win32':
        import io
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

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
        # 没有 hook 数据，直接退出
        sys.exit(0)

    # 检查是否是 Stop 事件（会话结束）
    hook_event_name = hook_data.get("hook_event_name", "")

    if hook_event_name != "Stop":
        sys.exit(0)

    # 生成会话总结
    summary = generate_session_summary()

    # 保存总结
    save_summary(summary)

    # 清空会话记录
    clear_conversation()

    # 输出提示信息
    sys.stderr.write("\n=== 会话已结束 ===\n")
    sys.stderr.write(f"会话总结已保存到: {CONFIG['session_summary_file']}\n")
    sys.stderr.write("下次会话开始时，你可以使用 /loadLastSession 命令加载上一次会话的内容。\n")

    sys.exit(0)


if __name__ == "__main__":
    main()
