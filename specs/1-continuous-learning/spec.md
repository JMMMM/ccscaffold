# Feature Specification: Continuous Learning Refactor

**Feature Branch**: `1-continuous-learning`
**Created**: 2026-02-09
**Status**: Draft
**Input**: 用户需要重构 continuous-learning（持续学习）功能，全面重新定义，创建 sessionEnd 钩子和 summary-skills 命令，自动分析聊天记录生成学习技能

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 自动会话总结 (Priority: P1)

用户希望在会话结束时自动分析对话内容，检测反复出现的问题（≥3次沟通未解决），并生成学习技能保存到指定目录。

**Why this priority**: 这是持续学习的核心功能，能够在用户无感知的情况下自动积累知识，减少手动操作。

**Independent Test**: 可以通过触发 SessionEnd 钩子完全测试，验证是否正确读取对话内容、分析问题模式并生成技能文件。

**Acceptance Scenarios**:

1. **Given** 用户完成一次包含多次修改尝试的会话，**When** 会话结束触发 SessionEnd 钩子，**Then** 系统自动读取最近20条对话，检测反复问题并生成技能文件
2. **Given** 对话内容没有反复问题，**When** 触发钩子，**Then** 系统跳过生成，不创建新文件
3. **Given** 已存在相似技能文件，**When** 检测到新模式，**Then** 系统更新现有技能而非创建新文件

---

### User Story 2 - 手动触发总结 (Priority: P2)

用户希望能够在会话中手动触发总结功能，快速查看当前对话中的问题模式并生成技能。

**Why this priority**: 提供手动控制选项，让用户可以在需要时主动总结，不一定要等到会话结束。

**Independent Test**: 可以通过执行 `/summary-skills` 命令完全测试，验证是否正确读取对话并生成技能。

**Acceptance Scenarios**:

1. **Given** 用户正在进行会话，**When** 输入 `/summary-skills` 命令，**Then** 系统读取最近20条对话并生成技能预览
2. **Given** 生成的技能预览已显示，**When** 用户确认保存，**Then** 技能文件保存到 `.claude/skills/learn/` 目录

---

### User Story 3 - 配置灵活性 (Priority: P3)

用户希望可以配置对话读取数量、文件路径等参数，以适应不同使用场景。

**Why this priority**: 提高功能的灵活性和适应性，满足不同用户的需求。

**Independent Test**: 可以通过修改配置文件测试，验证参数是否正确生效。

**Acceptance Scenarios**:

1. **Given** 用户修改了配置文件中的对话数量，**When** 触发总结功能，**Then** 系统读取指定数量的对话
2. **Given** 用户修改了文件路径配置，**When** 触发总结功能，**Then** 系统从指定路径读取对话文件

---

### Edge Cases

- 当对话文件不存在或为空时，系统应优雅退出而不报错
- 当对话数量少于配置的最大值时，系统应读取所有可用内容
- 当生成的技能文件名冲突时，系统应添加时间戳或序号避免覆盖
- 当 Claude API 调用失败时，系统应记录错误并继续执行，不影响会话正常结束

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: 系统必须提供一个 SessionEnd 钩子，在会话结束时自动触发
- **FR-002**: 系统必须提供一个 `/summary-skills` 命令，支持手动触发总结功能
- **FR-003**: 系统必须从 `.claude/conversations/conversation.txt` 读取对话内容（可配置路径）
- **FR-004**: 系统必须支持配置读取对话的最大条数（默认20条）
- **FR-005**: 系统必须检测对话中反复出现的问题（沟通次数≥3次未解决）
- **FR-006**: 系统必须使用 Claude API 分析对话并生成学习技能
- **FR-007**: 系统必须将生成的技能保存到 `.claude/skills/learn/` 目录
- **FR-008**: 系统必须在已存在相似技能时进行更新而非创建新文件
- **FR-009**: 系统必须使用中文编写所有文档和提示信息
- **FR-010**: 系统必须支持 Windows、Linux、macOS 三个平台
- **FR-011**: 系统必须使用 Python 3.9+ 兼容的代码
- **FR-012**: 系统必须遵循项目宪章的所有规范（临时文件路径、代码规范等）
- **FR-013**: 钩子脚本必须在60秒内完成执行，避免阻塞会话结束
- **FR-014**: 配置文件必须使用 JSON 格式，支持修改对话数量和文件路径

### Key Entities

- **对话记录 (Conversation)**: 存储在 `.claude/conversations/conversation.txt`，包含用户和 AI 的所有交互内容
- **学习技能 (Learned Skill)**: 存储在 `.claude/skills/learn/` 目录，包含从对话中提取的问题模式和解决方案
- **配置文件 (Config)**: JSON 格式，存储对话数量、文件路径等可配置参数
- **状态文件 (State)**: 跟踪已处理的对话位置，避免重复分析

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 会话结束时自动总结功能在 95% 的情况下能在 60 秒内完成
- **SC-002**: 检测反复问题的准确率达到 80% 以上（通过人工抽验生成的技能质量）
- **SC-003**: 用户可以手动触发总结功能并获得即时反馈
- **SC-004**: 生成的技能文件格式正确，可以被 Claude Code 正确加载
- **SC-005**: 修改配置后系统行为正确变更，配置覆盖率达到 100%

## Assumptions

- 对话文件按照标准格式存储（每条消息以时间戳 + sender > content 格式）
- Claude API 可用且在合理的响应时间内返回结果
- 用户对 `.claude` 目录有读写权限
- Python 3.9+ 已安装并在系统 PATH 中可用
- 现有的会话记录功能（chat-record）已正确配置并运行

## Out of Scope

- 自动应用生成的技能（需要人工审核后手动启用）
- 技能文件的质量自动评估和过滤
- 跨会话的问题模式检测（仅分析单个会话文件）
- 技能文件的自动删除或归档功能
