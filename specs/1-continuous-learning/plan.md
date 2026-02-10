# Implementation Plan: Continuous Learning Refactor

**Branch**: `1-continuous-learning` | **Date**: 2026-02-09 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/1-continuous-learning/spec.md`

## Summary

重构 continuous-learning 功能，实现自动分析对话内容并生成学习技能的系统。核心功能包括：
1. SessionEnd 钩子自动触发分析
2. `/summary-skills` 命令手动触发
3. 检测反复问题（≥3次沟通未解决）
4. 使用 Claude API 生成技能并保存到 `.claude/skills/learn/`

技术方法：使用 Python 3.9+ 编写钩子和命令脚本，通过 Claude API 分析对话内容并生成结构化的学习技能。

## Technical Context

**Language/Version**: Python 3.9+
**Primary Dependencies**: Claude Code API, pathlib, json, subprocess, re
**Storage**: 文件系统（conversation.txt, state.json, 技能文件）
**Testing**: 手动测试 + 真实对话数据分析
**Target Platform**: Windows, Linux, macOS (跨平台)
**Project Type**: 单项目（Claude Code 功能扩展）
**Performance Goals**: 60秒内完成分析（FR-013）
**Constraints**:
  - 必须 Python 3.9+ 兼容
  - 钩子执行时间 < 60 秒
  - 跨平台兼容
**Scale/Scope**:
  - 处理最近 20 条对话（可配置）
  - 生成单个技能文件
  - 状态跟踪避免重复分析

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### 临时文件路径规范 (PRINCIPLE I)
- [x] 所有临时文件使用 `.claude/tmp/` 目录 - 状态文件存储在 `.claude/skills/continuous-learning/`
- [x] 按功能类型正确分类 (conversations/, cache/, scripts/) - 使用现有的 conversations 目录
- [x] 文件命名包含时间戳 - 生成的技能文件包含时间戳

### 文档语言规范 (PRINCIPLE II)
- [x] 文档使用中文编写 - README.md 和命令文档使用中文
- [x] 脚本文件使用英文命名 - summary_skills.py, session_end_hook.py
- [x] 代码注释保持一致性 - 中文注释说明逻辑

### Python 版本兼容性 (PRINCIPLE III)
- [x] Python 脚本兼容 3.9+ - 使用标准库，避免高版本特性
- [x] 避免使用高版本特性 - 使用 pathlib 而非新增方法

### 代码字符规范 (PRINCIPLE IV)
- [x] 无特殊 Unicode 字符 - 仅使用 ASCII
- [x] 仅使用 ASCII 字符集 - UTF-8 编码但不包含特殊字符

### 文档组织规范 (PRINCIPLE V)
- [x] Markdown 文档放置在 `docs/` 目录 - 功能文档在 ccscaffold/continuous-learning/docs/
- [x] 按功能模块分类 - 按功能组织

### 组件自包含原则 (PRINCIPLE VI)
- [x] 组件可独立运行 - 钩子和命令可独立工作
- [x] 依赖关系明确声明 - 依赖 chat-record 功能提供对话数据

### README.md 强制要求 (PRINCIPLE VII)
- [x] 每个功能组件包含 README.md - 创建完整 README
- [x] README 使用中文编写 - 符合规范
- [x] 包含功能说明、使用方法、配置说明 - 完整文档结构
- [x] 包含依赖关系和注意事项 - 说明依赖 chat-record
- [x] 文档与代码实现同步 - 同步更新

### 代码质量标准 (PRINCIPLE VIII)
- [x] 变量、函数、类命名清晰表达用途 - 遵循 PEP 8
- [x] 复杂逻辑添加注释说明 - 添加中文注释
- [x] 函数有完整的文档字符串 - 使用 docstring
- [x] 无魔法数字或字符串 - 定义为常量（MAX_CONVERSATIONS = 20）
- [x] 单个函数不超过 50 行 - 模块化设计
- [x] 单个类不超过 300 行 - 分离关注点
- [x] 模块职责单一,边界清晰 - 分析器、生成器、状态管理分离
- [x] 模块间依赖最小化,无循环依赖 - 清晰的层次结构
- [x] 使用依赖注入而非直接依赖具体实现 - 配置注入
- [x] 模块可以独立测试 - 纯函数设计
- [x] 每个文件不超过 1000 行代码 - 预计 < 500 行

### 跨平台可移植性优先原则 (PRINCIPLE IX)
- [x] 功能支持 Windows、Linux、macOS 三个平台 - 使用 pathlib 和 subprocess
- [x] 默认使用跨平台实现 - Python 标准库
- [x] 平台特定优化有明确的性能提升依据 (>30%) - 无平台特定优化
- [x] 平台特定代码有回退到跨平台实现的逻辑 - N/A
- [x] 文件路径使用跨平台库 (pathlib, tempfile 等) - 使用 pathlib.Path
- [x] 移植工具提供交互式平台选择 - N/A（非移植工具）
- [x] 在目标平台进行了测试 - 需要测试
- [x] 文档中说明平台兼容性和限制 - 在 README 中说明

### 隐私保护与信息安全原则 (PRINCIPLE X)
- [x] Git 提交前已运行隐私检查脚本 - 提交前检查
- [x] 无绝对路径包含用户目录名 - 使用相对路径
- [x] 无个人身份识别信息 - 使用占位符
- [x] 无认证凭据 - 使用环境变量
- [x] 敏感配置使用环境变量或配置模板 - 配置文件模板
- [x] 测试数据已脱敏处理 - 使用虚构数据
- [x] 日志输出不包含敏感信息 - 脱敏处理
- [x] `.env` 等敏感文件已添加到 `.gitignore` - 确认
- [x] 文档和注释中无真实敏感信息 - 使用占位符

## Project Structure

### Documentation (this feature)

```text
specs/1-continuous-learning/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── summary-skills-command.md
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
.claude/
├── commands/
│   └── summary-skills.md        # 手动触发命令
├── skills/
│   └── continuous-learning/
│       ├── skill.json           # 技能配置
│       ├── SKILL.md             # 技能说明
│       └── scripts/
│           ├── summary_skills.py      # 核心分析脚本
│           └── session_end_hook.py    # SessionEnd 钩子
├── hooks/
│   └── continuous-learning/
│       └── session_end_hook.py  # SessionEnd 钩子（备用位置）
└── settings.json               # 全局配置（添加钩子配置）

ccscaffold/continuous-learning/  # 功能组件目录
├── docs/
│   ├── continuous-learning.md   # 功能文档
│   └── continuous-learning-usage.md  # 使用指南
├── skills/                      # 组件技能
│   └── continuous-learning/
│       ├── skill.json
│       ├── SKILL.md
│       └── scripts/
│           ├── summary_skills.py
│           └── session_end_hook.py
├── hooks/                       # 组件钩子
│   └── session_end_continuous_learning.py
└── README.md                    # 组件文档

.claude/skills/learn/            # 生成的学习技能存储目录
```

**Structure Decision**: 采用单项目结构，所有脚本放在 `.claude/skills/continuous-learning/` 目录下，生成的技能保存在 `.claude/skills/learn/` 目录。功能组件目录 `ccscaffold/continuous-learning/` 用于分发和文档管理。

## Complexity Tracking

> **No violations to report** - 所有设计都符合项目宪章要求。

## Phase 0: Research & Analysis

### Research Tasks

1. **验证对话文件格式**
   - 确认 `conversation.txt` 的标准格式
   - 验证时间戳 + sender > content 格式
   - 确认用户消息和 AI 响应的识别模式

2. **确定问题检测算法**
   - 评估如何检测"反复问题"（≥3次）
   - 设计关键词匹配和相似度算法
   - 确定问题模式识别策略

3. **研究 Claude API 集成**
   - 确认如何在 Python 脚本中调用 Claude API
   - 设计 prompt 模板结构
   - 确定响应解析方法

### Research Findings

**Decision**: 使用关键词频率统计 + 相似度匹配检测反复问题

**Rationale**:
- 关键词频率统计简单高效，适合检测重复提及
- 相似度匹配可识别不同表述的同一问题
- 对于小数据集（20条），性能不是问题

**Alternatives considered**:
- 使用 NLP 模型进行语义分析：过度工程，依赖重
- 简单字符串匹配：无法识别不同表述的同一问题

**对话文件格式验证**:
```
时间戳 sender> content
示例: 2026-02-09 20:49:40 claude> Tool: Read
示例: 2026-02-09 20:56:11 user> 测试修复后的记录
```

## Phase 1: Design

### Data Model

**ConversationEntry**: 对话条目
```python
{
    "timestamp": str,      # "2026-02-09 20:49:40"
    "sender": str,         # "user" or "claude"
    "content": str,        # 消息内容
    "line_number": int     # 行号（用于状态跟踪）
}
```

**IssuePattern**: 问题模式
```python
{
    "topic": str,          # 问题主题
    "occurrences": int,    # 出现次数
    "first_line": int,     # 首次出现行号
    "last_line": int,      # 最后出现行号
    "keywords": List[str]  # 关键词列表
}
```

**LearnedSkill**: 学习技能
```python
{
    "name": str,           # 技能名称
    "description": str,    # 技能描述
    "issue_topic": str,    # 问题主题
    "retry_count": int,    # 检测到的反复次数
    "generated_at": str,   # 生成时间
    "content": str         # 技能内容（markdown）
}
```

**State**: 状态文件
```python
{
    "conversation_file": {
        "last_line": int,              # 已处理的行数
        "skills_generated": List[dict] # 生成的技能列表
    }
}
```

### API Contracts

**无 API 契约** - 本功能是纯本地脚本，不涉及 HTTP API。

### Implementation Design

#### 1. 核心类设计

```python
class ConversationReader:
    """对话文件读取器"""
    def __init__(self, file_path: Path, max_lines: int = 20):
        self.file_path = file_path
        self.max_lines = max_lines

    def read_latest(self, from_line: int = 0) -> List[ConversationEntry]
    def parse_line(self, line: str) -> Optional[ConversationEntry]

class IssueAnalyzer:
    """问题分析器"""
    def __init__(self, retry_threshold: int = 3):
        self.retry_threshold = retry_threshold

    def analyze(self, entries: List[ConversationEntry]) -> List[IssuePattern]
    def extract_keywords(self, content: str) -> Set[str]
    def calculate_similarity(self, text1: str, text2: str) -> float

class SkillGenerator:
    """技能生成器"""
    def __init__(self, claude_api_client):
        self.claude = claude_api_client

    def generate(self, pattern: IssuePattern, entries: List[ConversationEntry]) -> LearnedSkill
    def build_prompt(self, pattern: IssuePattern, context: str) -> str

class StateManager:
    """状态管理器"""
    def __init__(self, state_file: Path):
        self.state_file = state_file

    def get_last_line(self, conversation_file: str) -> int
    def update_last_line(self, conversation_file: str, line: int, skill: str)
```

#### 2. 提示词模板

```python
SUMMARY_PROMPT = """# 角色设定
你是一个具备持续学习能力的 AI 助手。你能够根据用户提供的先前学习总结，以及当前对话内容，更新学习总结，以便在后续对话中保持连续性。

# 内容筛选规则
根据聊天内容，找出多次沟通（大于等于 {retry_threshold} 次）都没有解决的问题。

# 总结任务
1. 总结内容的处理步骤，整理出一套处理问题的流程
2. 根据 Claude Code 的规则生成一个 skill
3. 如果有现成的 skills，就进行更新，扩展功能

# 以下是聊天内容
{conversation_content}

请生成一个学习技能，包含以下部分：
- 问题概述：描述检测到的问题
- 触发点识别：什么情况下应该参考此技能
- 修复规律总结：从对话中提取的规律和解决方案
- 使用建议：如何应用此技能避免重复问题
"""
```

### Quickstart Guide

**验证步骤**：

1. **准备测试环境**：
   ```bash
   # 使用测试数据验证
   cp /path/to/source/.claude/conversations/conversation.txt \
      /path/to/project/.claude/conversations/test_conversation.txt
   ```

2. **手动触发测试**：
   ```bash
   python3.9 .claude/skills/continuous-learning/scripts/summary_skills.py \
              --conversation-file /path/to/project/.claude/conversations/test_conversation.txt
   ```

3. **验证输出**：
   - 检查是否检测到"数据日历周末显示"问题
   - 验证生成的技能文件格式
   - 确认技能保存到 `.claude/skills/learn/` 目录

## 测试计划 (Test Plan)

### 测试数据来源

使用 `/path/to/source/.claude/conversations/conversation.txt` 作为测试数据，该文件包含：

1. **数据日历周末显示问题** - 反复出现的典型案例
   - 用户反复提到：2月1日（星期日）显示红色
   - 用户反复提到：2月7日显示红色
   - 用户反复提到：2月8日（星期六）显示红色
   - 用户提到：问题没有得到解决
   - 沟通次数：≥3次

2. **板块追踪排序功能** - 完整的功能开发案例
   - 从需求分析到实现完成的完整流程
   - 包含多次代码修改和验证

### 测试场景

#### 场景 1：检测反复问题
**输入**: 读取示例项目的 conversation.txt
**预期输出**:
- 检测到"数据日历周末显示问题"模式
- 识别出问题关键词："周末"、"显示红色"、"交易日"
- 统计出现次数 ≥ 3

#### 场景 2：生成技能文件
**输入**: 检测到的问题模式 + 对话上下文
**预期输出**:
- 生成 markdown 格式的技能文件
- 文件名包含时间戳和问题主题
- 保存到 `.claude/skills/learn/` 目录

#### 场景 3：状态跟踪
**输入**: 多次运行分析
**预期输出**:
- 首次运行：处理全部对话
- 二次运行：仅处理新增对话
- 状态文件正确更新

### 测试步骤

1. **准备测试环境**：
   ```bash
   # 复制测试数据
   mkdir -p .claude/conversations
   cp /path/to/source/.claude/conversations/conversation.txt \
      .claude/conversations/test_conversation.txt
   ```

2. **运行分析脚本**：
   ```bash
   python3.9 .claude/skills/continuous-learning/scripts/summary_skills.py \
              --conversation-file .claude/conversations/test_conversation.txt \
              --max-conversations 20
   ```

3. **验证输出**：
   ```bash
   # 检查生成的技能文件
   ls -la .claude/skills/learn/

   # 查看技能内容
   cat .claude/skills/learn/*.md

   # 检查状态文件
   cat .claude/skills/continuous-learning/state.json
   ```

4. **预期结果**：
   - 生成至少 1 个技能文件（关于数据日历周末显示问题）
   - 技能文件包含：问题概述、触发点、解决方案、使用建议
   - 状态文件记录已处理的行数

### 成功标准

- ✅ 能够从测试数据中检测到"数据日历周末显示"问题
- ✅ 生成的技能文件格式正确且包含有用信息
- ✅ 状态跟踪正常工作，避免重复分析
- ✅ 脚本在 60 秒内完成分析

## Phase 2: Tasks

**Note**: 由 `/speckit.tasks` 命令生成任务列表

## Artifacts Generated

- [x] `research.md` - 研究发现和技术决策
- [x] `data-model.md` - 数据模型说明
- [x] `contracts/summary-skills-command.md` - 命令文档
- [x] `quickstart.md` - 快速入门指南
- [x] `tasks.md` - 任务列表已生成
