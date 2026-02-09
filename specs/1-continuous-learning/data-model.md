# Data Model: Continuous Learning Refactor

**Feature**: 1-continuous-learning
**Date**: 2026-02-09

## Entities

### ConversationEntry (对话条目)

**说明**: 单条对话记录的数据结构

**字段**:

| 字段名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| timestamp | str | 时间戳 | "2026-02-09 20:49:40" |
| sender | str | 发送者 | "user", "claude", "assistant" |
| content | str | 消息内容 | "请帮我修复这个问题" |
| line_number | int | 在文件中的行号 | 42 |

**Python 定义**:
```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class ConversationEntry:
    """对话条目"""
    timestamp: str
    sender: str
    content: str
    line_number: int

    @classmethod
    def from_line(cls, line: str, line_number: int) -> Optional['ConversationEntry']:
        """从单行文本解析对话条目"""
        # 格式: 2026-02-09 20:49:40 user> 消息内容
        import re
        pattern = r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+(\w+)>\s*(.+)$'
        match = re.match(pattern, line.strip())
        if match:
            return cls(
                timestamp=match.group(1),
                sender=match.group(2),
                content=match.group(3),
                line_number=line_number
            )
        return None
```

---

### IssuePattern (问题模式)

**说明**: 检测到反复出现的问题模式

**字段**:

| 字段名 | 类型 | 说明 |
|--------|------|------|
| topic | str | 问题主题（简短描述） |
| occurrences | int | 出现次数 |
| first_line | int | 首次出现的行号 |
| last_line | int | 最后出现的行号 |
| keywords | Set[str] | 关键词集合 |
| user_messages | List[Dict] | 相关的用户消息 |

**Python 定义**:
```python
from dataclasses import dataclass, field
from typing import Set, List, Dict

@dataclass
class IssuePattern:
    """问题模式"""
    topic: str
    occurrences: int
    first_line: int
    last_line: int
    keywords: Set[str] = field(default_factory=set)
    user_messages: List[Dict] = field(default_factory=list)

    def meets_threshold(self, threshold: int = 3) -> bool:
        """检查是否达到反复问题阈值"""
        return self.occurrences >= threshold
```

---

### LearnedSkill (学习技能)

**说明**: 生成的学习技能

**字段**:

| 字段名 | 类型 | 说明 |
|--------|------|------|
| name | str | 技能名称（文件名） |
| description | str | 技能描述 |
| issue_topic | str | 问题主题 |
| retry_count | int | 检测到的反复次数 |
| generated_at | str | 生成时间（ISO 8601） |
| content | str | 技能内容（markdown 格式） |
| file_path | Path | 技能文件路径 |

**Python 定义**:
```python
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime
from typing import Optional

@dataclass
class LearnedSkill:
    """学习技能"""
    name: str
    description: str
    issue_topic: str
    retry_count: int
    generated_at: str
    content: str
    file_path: Optional[Path] = None

    @classmethod
    def create(cls, pattern: IssuePattern, content: str) -> 'LearnedSkill':
        """从问题模式创建学习技能"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        name = f"fix-{sanitize_topic(pattern.topic)}-{timestamp}"
        return cls(
            name=name,
            description=f"自动生成的修复技能 - {pattern.topic}",
            issue_topic=pattern.topic,
            retry_count=pattern.occurrences,
            generated_at=datetime.now().isoformat(),
            content=content
        )

    def save(self, directory: Path) -> Path:
        """保存技能到文件"""
        directory.mkdir(parents=True, exist_ok=True)
        self.file_path = directory / f"{self.name}.md"
        with open(self.file_path, 'w', encoding='utf-8') as f:
            f.write(self.content)
        return self.file_path

def sanitize_topic(topic: str) -> str:
    """清理主题字符串，用作文件名"""
    import re
    # 移除特殊字符，只保留字母、数字、中文和连字符
    sanitized = re.sub(r'[^\w\u4e00-\u9fff-]', '-', topic)
    # 限制长度
    return sanitized[:50]
```

---

### State (状态文件)

**说明**: 跟踪已处理的对话位置

**文件路径**: `.claude/skills/continuous-learning/state.json`

**结构**:
```json
{
  "conversation.txt": {
    "last_line": 150,
    "skills_generated": [
      {
        "name": "fix-weekend-display-issue-20260209213000",
        "generated_at": "2026-02-09T21:30:00",
        "processed_line": 150
      }
    ],
    "first_analyzed": "2026-02-09T21:00:00",
    "last_analyzed": "2026-02-09T21:30:00"
  }
}
```

**Python 定义**:
```python
from dataclasses import dataclass, field
from typing import Dict, List
from pathlib import Path
import json

@dataclass
class ConversationState:
    """单个对话文件的状态"""
    last_line: int = 0
    skills_generated: List[Dict] = field(default_factory=list)
    first_analyzed: str = ""
    last_analyzed: str = ""

@dataclass
class State:
    """全局状态"""
    conversations: Dict[str, ConversationState] = field(default_factory=dict)

    def load(self, state_file: Path) -> 'State':
        """从文件加载状态"""
        if state_file.exists():
            with open(state_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # 转换为 State 对象
                for conv_name, conv_state in data.items():
                    self.conversations[conv_name] = ConversationState(**conv_state)
        return self

    def save(self, state_file: Path):
        """保存状态到文件"""
        state_file.parent.mkdir(parents=True, exist_ok=True)
        data = {
            name: {
                'last_line': state.last_line,
                'skills_generated': state.skills_generated,
                'first_analyzed': state.first_analyzed,
                'last_analyzed': state.last_analyzed
            }
            for name, state in self.conversations.items()
        }
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_last_line(self, conversation_file: str) -> int:
        """获取对话文件上次处理的行数"""
        if conversation_file in self.conversations:
            return self.conversations[conversation_file].last_line
        return 0

    def update_last_line(self, conversation_file: str, line: int, skill_name: str):
        """更新已处理的行数"""
        if conversation_file not in self.conversations:
            self.conversations[conversation_file] = ConversationState()

        state = self.conversations[conversation_file]
        state.last_line = line
        state.last_analyzed = datetime.now().isoformat()

        if not state.first_analyzed:
            state.first_analyzed = state.last_analyzed

        state.skills_generated.append({
            'name': skill_name,
            'generated_at': datetime.now().isoformat(),
            'processed_line': line
        })
```

---

## 关系图

```
ConversationEntry
    ↓ (分析)
IssuePattern
    ↓ (生成)
LearnedSkill
    ↓ (保存到)
.claude/skills/learn/{name}.md

State
    ↓ (跟踪)
ConversationEntry (避免重复分析)
```

---

## 配置模型

### Config (配置文件)

**文件路径**: `.claude/skills/continuous-learning/config.json`

**结构**:
```json
{
  "max_conversations": 20,
  "retry_threshold": 3,
  "conversation_file": ".claude/conversations/conversation.txt",
  "skills_output_dir": ".claude/skills/learn",
  "state_file": ".claude/skills/continuous-learning/state.json",
  "keywords": {
    "retry": ["修复", "修正", "解决", "还是不行", "还是有问题", "继续", "再试", "失败", "错误"],
    "issues": ["问题", "bug", "错误", "失败", "不正确"]
  }
}
```

**Python 定义**:
```python
from dataclasses import dataclass
from pathlib import Path
import json

@dataclass
class Config:
    """配置"""
    max_conversations: int = 20
    retry_threshold: int = 3
    conversation_file: str = ".claude/conversations/conversation.txt"
    skills_output_dir: str = ".claude/skills/learn"
    state_file: str = ".claude/skills/continuous-learning/state.json"
    keywords: Dict[str, List[str]] = None

    @classmethod
    def load(cls, config_file: Path) -> 'Config':
        """从文件加载配置"""
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return cls(**data)
        return cls()

    def save(self, config_file: Path):
        """保存配置到文件"""
        config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(self.__dict__, f, ensure_ascii=False, indent=2)
```
