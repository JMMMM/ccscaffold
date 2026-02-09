#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Issue Analyzer for Continuous Learning

问题分析器 - 检测反复出现的问题
"""

import re
from typing import List, Set, Dict
from models import ConversationEntry, IssuePattern


class IssueAnalyzer:
    """问题分析器"""

    def __init__(self, retry_threshold: int = 3, keywords: Dict[str, List[str]] = None):
        self.retry_threshold = retry_threshold
        self.keywords = keywords or {
            "retry": ["修复", "修正", "解决", "还是不行", "还是有问题", "继续", "再试", "失败", "错误"],
            "issues": ["问题", "bug", "错误", "失败", "不正确"]
        }

    def analyze(self, entries: List[ConversationEntry]) -> List[IssuePattern]:
        """分析对话条目，检测反复问题

        Args:
            entries: 对话条目列表

        Returns:
            检测到的问题模式列表
        """
        # 提取用户消息
        user_messages = []
        for entry in entries:
            if entry.sender == 'user':
                user_messages.append(entry)

        if not user_messages:
            print("没有找到用户消息")
            return []

        # 检测反复问题的模式
        issue_patterns = []

        # 构建问题关键词匹配
        retry_keywords = set(self.keywords.get("retry", []))
        issue_keywords = set(self.keywords.get("issues", []))

        # 分析每个用户消息，查找反复提及的问题
        for i, msg in enumerate(user_messages):
            content = msg.content

            # 检查是否包含重试关键词
            has_retry = any(keyword in content for keyword in retry_keywords)
            has_issue = any(keyword in content for keyword in issue_keywords)

            if has_retry and has_issue:
                # 提取问题主题（移除重试关键词后的内容）
                topic = self._extract_topic(content, retry_keywords)

                # 查找之前是否有相关的问题
                related_count = 1
                first_line = msg.line_number
                last_line = msg.line_number

                for j in range(i - 1, max(0, i - 10), -1):
                    prev_msg = user_messages[j]
                    if self._is_similar_issue(content, prev_msg.content):
                        related_count += 1
                        first_line = min(first_line, prev_msg.line_number)
                    else:
                        break

                # 如果达到阈值，创建问题模式
                if related_count >= self.retry_threshold:
                    # 收集所有相关的用户消息
                    related_messages = []
                    for j in range(i, max(0, i - related_count), -1):
                        related_messages.insert(0, {
                            'line': user_messages[j].line_number,
                            'content': user_messages[j].content
                        })

                    # 检查是否已存在相似的模式
                    is_duplicate = False
                    for pattern in issue_patterns:
                        if self._is_similar_topic(topic, pattern.topic):
                            # 更新模式而不是创建新的
                            pattern.occurrences = max(pattern.occurrences, related_count)
                            pattern.last_line = max(pattern.last_line, last_line)
                            # 添加新的消息（如果还没有）
                            for new_msg in related_messages:
                                if not any(m['line'] == new_msg['line'] for m in pattern.user_messages):
                                    pattern.user_messages.append(new_msg)
                            is_duplicate = True
                            break

                    if not is_duplicate:
                        pattern = IssuePattern(
                            topic=topic,
                            occurrences=related_count,
                            first_line=first_line,
                            last_line=last_line,
                            keywords=self._extract_keywords(content),
                            user_messages=related_messages
                        )
                        issue_patterns.append(pattern)

        return issue_patterns

    def _extract_topic(self, content: str, retry_keywords: Set[str]) -> str:
        """提取问题主题（移除重试关键词）"""
        topic = content
        for keyword in retry_keywords:
            topic = topic.replace(keyword, '')
        # 清理多余空格和标点
        topic = ' '.join(topic.split())
        return topic[:100]  # 限制长度

    def _is_similar_issue(self, content1: str, content2: str) -> bool:
        """判断两个消息是否描述相似的问题"""
        # 方法0: 检查是否是"继续修复"类型的消息
        # 如果消息包含"继续"、"再试"、"还是不行"等关键词，认为是对之前问题的跟进
        followup_keywords = ['继续', '再试', '还是', '仍然', '没有解决', '仍未']
        is_followup1 = any(kw in content1 for kw in followup_keywords)
        is_followup2 = any(kw in content2 for kw in followup_keywords)

        # 如果其中一个是跟进消息，另一个包含问题关键词，认为相关
        if (is_followup1 or is_followup2):
            has_issue1 = any(kw in content1 for kw in self.keywords.get("issues", []))
            has_issue2 = any(kw in content2 for kw in self.keywords.get("issues", []))
            if has_issue1 or has_issue2:
                return True

        # 方法1: 基于关键词的相似度
        words1 = set(self._extract_words(content1))
        words2 = set(self._extract_words(content2))

        if not words1 or not words2:
            return False

        intersection = words1 & words2
        union = words1 | words2

        # 相似度 = 交集 / 并集
        similarity = len(intersection) / len(union) if union else 0

        # 方法2: 检查是否有共同的关键问题词（如"日历"、"红色"、"数据"等）
        # 这些词通常表示问题的核心主题
        topic_keywords1 = self._extract_topic_keywords(content1)
        topic_keywords2 = self._extract_topic_keywords(content2)
        topic_intersection = topic_keywords1 & topic_keywords2

        # 如果有共同的主题关键词（至少1个），认为相似
        if len(topic_intersection) >= 1:
            return True

        # 方法3: 检查是否都包含"问题"关键词
        has_issue1 = any(kw in content1 for kw in self.keywords.get("issues", []))
        has_issue2 = any(kw in content2 for kw in self.keywords.get("issues", []))
        if has_issue1 and has_issue2:
            # 如果都有问题关键词，使用更低的相似度阈值
            return similarity > 0.15

        # 否则使用标准词汇相似度判断
        return similarity > 0.2  # 降低阈值到20%

    def _is_similar_topic(self, topic1: str, topic2: str) -> bool:
        """判断两个主题是否相似"""
        return topic1 == topic2 or topic1 in topic2 or topic2 in topic1

    def _extract_keywords(self, content: str) -> Set[str]:
        """从内容中提取关键词"""
        words = self._extract_words(content)
        # 过滤掉常见词和短词
        stop_words = {'的', '是', '我', '我', '了', '有', '和', '在', '这', '那'}
        return {w for w in words if len(w) > 1 and w not in stop_words}

    def _extract_words(self, content: str) -> Set[str]:
        """提取词汇"""
        # 匹配中文词汇和英文单词
        chinese_pattern = re.findall(r'[\u4e00-\u9fff]+', content)
        english_pattern = re.findall(r'[a-zA-Z]+', content)
        return set(chinese_pattern + english_pattern)

    def _extract_topic_keywords(self, content: str) -> Set[str]:
        """提取主题关键词（通常是问题相关的核心词汇）"""
        # 定义常见的主题关键词模式
        topic_patterns = [
            r'[数据日历]+',
            r'[红色]+',
            r'[周末]+',
            r'[星期]+',
            r'[交易日]+',
            r'[月份]+',
            r'[日期]+',
            r'[显示]+',
            r'[API]+',
            r'[数据库]+',
            r'[函数]+',
        ]

        keywords = set()
        for pattern in topic_patterns:
            matches = re.findall(pattern, content)
            keywords.update(matches)

        return keywords
