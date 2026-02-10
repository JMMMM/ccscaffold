#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Claude Code 对话记录系统（优化版）

记录所有对话内容：
- 仅维护一份 conversation.txt 文件
- 持续追加写入，不重置
- 支持会话总结和文件修改记录
- 过滤读命令，减少存储压力
- 保留最近 50 条记录，自动清理旧记录
"""


# 需要过滤的读命令列表（不记录到 conversation.txt）
READ_ONLY_TOOLS = {
    'Read',           # 读取文件
    'Grep',           # 搜索文件内容
    'Glob',           # 文件模式匹配
    'WebSearch',      # 网页搜索
    'WebFetch',       # 网页获取
    'mcp__context7__resolve-library-id',  # Context7 查询
    'mcp__context7__query-docs',          # Context7 文档查询
    'mcp__web-reader__webReader',         # Web Reader
    'TaskOutput',     # 获取任务输出
}

import json
import sys
import os
import re
from datetime import datetime
from pathlib import Path


# 配置
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB，超过则清空重新开始
MAX_MESSAGES = 50  # 最多保留的消息条数


def get_project_root():
    """获取项目根目录"""
    # 获取脚本所在目录的父目录的父目录的父目录（项目根目录）
    # 脚本位置: .claude/skills/chat-record/chat_recorder.py
    # 需要返回: 项目根目录
    script_dir = Path(__file__).resolve().parent
    # script/chat-record -> skills -> .claude -> project_root
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


def count_messages(content):
    """计算消息条数（以时间戳开头的行）"""
    import re
    pattern = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} (user|claude)>'
    return len(re.findall(pattern, content, re.MULTILINE))


def write_message(role, content):
    """写入消息到会话文件，只保留最近 MAX_MESSAGES 条消息"""
    try:
        check_and_reset()

        conv_file = get_conversation_file()

        # 读取现有内容
        existing_content = ""
        if conv_file.exists():
            existing_content = conv_file.read_text(encoding='utf-8')

        # 生成新消息
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        clean_content = sanitize_text(content)
        clean_role = sanitize_text(role)
        new_message = f"{timestamp} {clean_role}> {clean_content}\n"

        # 合并新消息
        all_content = existing_content + new_message

        # 如果超过最大消息数，只保留最近 MAX_MESSAGES 条
        message_count = count_messages(all_content)
        if message_count > MAX_MESSAGES:
            # 按消息分割，保留最近 MAX_MESSAGES 条
            messages = []
            current_msg = []

            for line in all_content.split('\n'):
                # 检测是否是新消息的开始（时间戳行）
                if line and line[0].isdigit():
                    if current_msg:
                        messages.append('\n'.join(current_msg))
                    current_msg = [line]
                else:
                    if current_msg or line.strip():
                        current_msg.append(line)

            if current_msg:
                messages.append('\n'.join(current_msg))

            # 只保留最近 MAX_MESSAGES 条
            messages = messages[-MAX_MESSAGES:]
            all_content = '\n'.join(messages) + '\n'

        # 写入文件
        conv_file.write_text(all_content, encoding='utf-8')

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


def truncate_output(obj, max_length=500):
    """安全截断输出，避免截断导致 JSON 无效"""
    output_str = json.dumps(obj, ensure_ascii=False)

    if len(output_str) <= max_length:
        return output_str

    # 尝试解析为字典或数组，进行智能截断
    try:
        parsed = json.loads(output_str)
        return json.dumps(safe_truncate(parsed, max_length), ensure_ascii=False)
    except:
        # 如果无法解析，直接截断
        return output_str[:max_length] + "...(truncated)"


def safe_truncate(obj, max_length):
    """递归截断对象，保持 JSON 结构有效"""
    if isinstance(obj, dict):
        result = {}
        for key, value in list(obj.items())[:5]:  # 最多保留 5 个键
            if len(json.dumps(value, ensure_ascii=False)) > 100:
                result[key] = str(type(value).__name__) + "(...truncated)"
            else:
                result[key] = value
        return result
    elif isinstance(obj, list):
        if len(obj) > 3:
            return obj[:3] + ["...(" + str(len(obj) - 3) + " more items truncated)"]
        return obj
    elif isinstance(obj, str) and len(obj) > 100:
        return obj[:100] + "...(truncated)"
    return obj


def handle_post_tool_use(data):
    """处理AI工具调用"""
    tool_name = data.get('tool_name', 'unknown')

    # 过滤读命令，不记录到 conversation.txt
    if tool_name in READ_ONLY_TOOLS:
        return

    tool_input = data.get('tool_input', {})
    tool_response = data.get('tool_response', {})

    # 格式化工具调用信息
    tool_info = f"Tool: {tool_name}"
    if tool_input:
        tool_info += f"\n  Input: {json.dumps(tool_input, ensure_ascii=False)}"

    # 安全截断输出
    if tool_response:
        output_str = truncate_output(tool_response, 500)
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
