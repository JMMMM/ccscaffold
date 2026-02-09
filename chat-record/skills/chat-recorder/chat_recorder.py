#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Claude Code 对话记录系统（优化版）

记录所有对话内容：
- 仅维护一份 conversation.txt 文件
- 每次新会话时清空并重新开始
- 支持会话总结和文件修改记录
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path


# 配置
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB，超过则清空重新开始


def get_project_root():
    """获取项目根目录"""
    # 获取脚本所在目录的父目录的父目录的父目录（项目根目录）
    # 脚本位置: .claude/skills/chat-recorder/chat_recorder.py
    # 需要返回: 项目根目录
    script_dir = Path(__file__).resolve().parent
    # script/chat-recorder -> skills -> .claude -> project_root
    return script_dir.parent.parent.parent


def get_conversation_file():
    """获取会话文件路径（固定为 conversation.txt）"""
    project_root = get_project_root()
    conv_dir = project_root / '.claude' / 'conversations'
    conv_dir.mkdir(parents=True, exist_ok=True)
    return conv_dir / 'conversation.txt'


def get_modify_log_file():
    """获取文件修改记录文件路径"""
    project_root = get_project_root()
    logs_dir = project_root / 'logs'
    logs_dir.mkdir(parents=True, exist_ok=True)
    return logs_dir / 'modify_logs.txt'


def get_session_summary_file():
    """获取会话总结文件路径"""
    project_root = get_project_root()
    conv_dir = project_root / '.claude' / 'conversations'
    conv_dir.mkdir(parents=True, exist_ok=True)
    return conv_dir / 'session_summary.txt'


def sanitize_text(text):
    """清理文本，移除或替换无法编码的字符"""
    if isinstance(text, str):
        try:
            # 尝试编码为UTF-8，如果失败则清理surrogate字符
            text.encode('utf-8')
            return text
        except UnicodeEncodeError:
            # 移除surrogate字符
            return text.encode('utf-8', errors='surrogateescape').decode('utf-8', errors='replace')
    return text


def check_and_reset():
    """检查文件大小，超过限制则清空重新开始"""
    conv_file = get_conversation_file()

    if conv_file.exists():
        file_size = conv_file.stat().st_size
        if file_size >= MAX_FILE_SIZE:
            # 文件太大，清空重新开始
            conv_file.write_text('', encoding='utf-8')


def write_message(role, content):
    """写入消息到会话文件"""
    try:
        check_and_reset()

        conv_file = get_conversation_file()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # 清理内容中的特殊字符
        clean_content = sanitize_text(content)
        clean_role = sanitize_text(role)
        message = f"\n{timestamp} {clean_role}> {clean_content}\n"

        with open(conv_file, 'a', encoding='utf-8', errors='replace') as f:
            f.write(message)

    except Exception as e:
        sys.stderr.write(f"[Chat Recorder Error] {str(e)}\n")


def handle_session_start(data):
    """处理会话开始 - 不做任何操作，等待用户手动加载"""
    # 新会话开始时，不清空文件，由用户决定
    pass


def handle_user_prompt(data):
    """处理用户输入"""
    prompt = data.get('prompt', '')
    if prompt:
        write_message('user', prompt)


def handle_post_tool_use(data):
    """处理AI工具调用"""
    tool_name = data.get('tool_name', 'unknown')
    tool_input = data.get('tool_input', {})
    tool_response = data.get('tool_response', {})

    # 格式化工具调用信息
    tool_info = f"Tool: {tool_name}"
    if tool_input:
        tool_info += f"\n  Input: {json.dumps(tool_input, ensure_ascii=False)}"

    # 只记录部分输出（避免太长）
    if tool_response:
        output_str = json.dumps(tool_response, ensure_ascii=False)
        if len(output_str) > 500:
            output_str = output_str[:500] + "...(truncated)"
        tool_info += f"\n  Output: {output_str}"

    write_message('claude', tool_info)


def handle_stop(data):
    """处理会话结束"""
    # 会话结束时不做任何操作
    # 由 sessionEnd 钩子处理总结
    pass


def main():
    """主函数"""
    try:
        # 从标准输入读取 hook 数据，处理编码问题
        import io
        if hasattr(sys.stdin, 'buffer'):
            # 在Windows上使用二进制模式读取，然后解码
            input_data = sys.stdin.buffer.read().decode('utf-8', errors='replace')
        else:
            input_data = sys.stdin.read()

        if not input_data:
            return

        # 解析 JSON 数据
        data = json.loads(input_data)

        # 根据 hook 类型处理
        hook_event_name = data.get('hook_event_name', '')

        if hook_event_name == 'SessionStart':
            handle_session_start(data)
        elif hook_event_name == 'UserPromptSubmit':
            handle_user_prompt(data)
        elif hook_event_name == 'PostToolUse':
            handle_post_tool_use(data)
        elif hook_event_name == 'Stop':
            handle_stop(data)

        # 输出原始数据(Claude Code 要求)
        # 在Windows上需要处理编码问题
        try:
            print(input_data, flush=True)
        except UnicodeEncodeError:
            # 如果直接输出失败，使用sys.stdout.buffer写入
            if hasattr(sys.stdout, 'buffer'):
                sys.stdout.buffer.write(input_data.encode('utf-8', errors='replace'))
                sys.stdout.buffer.flush()

    except Exception as e:
        # 出错时不影响 Claude Code 正常运行
        sys.stderr.write(f"[Chat Recorder Error] {str(e)}\n")
        try:
            print(input_data if 'input_data' in locals() else '', flush=True)
        except:
            if 'input_data' in locals() and hasattr(sys.stdout, 'buffer'):
                sys.stdout.buffer.write(input_data.encode('utf-8', errors='replace'))


if __name__ == '__main__':
    main()
