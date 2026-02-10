#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-
"""
SessionEnd Hook - 会话结束时生成总结和文件修改记录
功能：
1. 读取 conversation.txt 总结会话内容
2. 读取 modify_logs.txt 获取文件修改记录
3. 生成会话总结并保存
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path


def get_project_root():
    """获取项目根目录"""
    # 获取脚本所在目录的父目录（项目根目录）
    # 脚本位置: .claude/scripts/hooks/chat-record/session_end_summary.py
    # 需要向上 4 层到达项目根目录
    script_dir = Path(__file__).resolve().parent
    return script_dir.parent.parent.parent.parent


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


def call_claude_for_summary(conversation, modifications):
    """调用 Claude 进行会话总结"""

    # 准备提示词
    prompt = f"""请分析以下会话内容并生成总结。

会话内容：
{conversation}

文件修改记录：
{modifications}

请生成一份结构化的总结，包括：
1. 会话主题
2. 主要讨论内容
3. 完成的任务
4. 文件修改情况
5. 遗留问题或后续计划

请使用中文回答。"""

    # 保存到临时文件
    temp_file = Path(get_project_root()) / '.claude' / 'tmp' / 'summary_prompt.txt'
    temp_file.parent.mkdir(parents=True, exist_ok=True)

    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write(prompt)

    # 注意：这里我们保存提示词，实际总结需要用户手动触发或在下次会话中处理
    # 因为在 sessionEnd 钩子中无法直接调用 Claude API
    return temp_file


def extract_file_modifications(conversation_text):
    """从 conversation.txt 中提取文件修改记录，生成 git log 格式
    仅读取 Output 部分获取实际修改的文件
    """
    import re

    # 按行分割
    lines = conversation_text.split('\n')

    modifications = []  # [(reason, [files])]

    current_reason = None
    current_files = []

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # 检测用户输入行（可能是修改原因）
        if line.endswith('user>'):
            # 如果之前有待处理的修改，先保存
            if current_reason and current_files:
                modifications.append((current_reason, list(set(current_files))))

            # 提取新的用户输入
            user_input = line.split('user>', 1)[1].strip()
            current_reason = user_input if user_input else None
            current_files = []

        # 检测 Output 行（工具执行结果）
        elif line.startswith('Output:'):
            # 查找 filePath 字段（Edit/Write 工具的返回值包含实际修改的文件路径）
            # 可能跨越多行，读取接下来的几行
            j = i + 1
            output_lines = [line]
            while j < len(lines) and not lines[j].strip().startswith(('2026-', 'Output:', 'user>', 'claude>')):
                output_lines.append(lines[j])
                j += 1
            output_text = ''.join(output_lines)

            # 提取 filePath (Edit/Write 工具返回值)
            match = re.search(r'"filePath":\s*"([^"]+)"', output_text)
            if match:
                file_path = match.group(1)
                # 转换为相对路径
                project_root = get_project_root()
                try:
                    rel_path = Path(file_path).relative_to(project_root)
                    file_display = str(rel_path)
                except:
                    file_display = file_path

                current_files.append(file_display)

        i += 1

    # 保存最后一次修改
    if current_reason and current_files:
        modifications.append((current_reason, list(set(current_files))))

    # 构建结果
    result = []
    for reason, files in modifications:
        if files:
            result.append(f"[change] {reason}, 修改以下文件：")
            for f in sorted(set(files)):
                result.append(f"- {f}")
            result.append("")  # 空行分隔

    return '\n'.join(result) if result else "本次会话没有文件修改记录。"


def generate_session_summary():
    """生成会话总结"""
    # 读取会话内容
    conversation = read_file_content(CONFIG["conversation_file"])

    if not conversation:
        return None

    # 从 conversation.txt 中提取文件修改记录
    modifications = extract_file_modifications(conversation)

    # 生成总结
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    summary = f"# {timestamp}\n"
    summary += f"{modifications}\n"
    summary += f"# " + "-" * 60 + "\n"

    return summary


def save_summary(summary):
    """保存会话总结"""
    summary_file = Path(CONFIG["session_summary_file"])

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
