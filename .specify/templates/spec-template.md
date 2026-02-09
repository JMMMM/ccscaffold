# Feature Specification: [FEATURE NAME]

**Feature Branch**: `[###-feature-name]`  
**Created**: [DATE]  
**Status**: Draft  
**Input**: User description: "$ARGUMENTS"

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - [Brief Title] (Priority: P1)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently - e.g., "Can be fully tested by [specific action] and delivers [specific value]"]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]
2. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### User Story 2 - [Brief Title] (Priority: P2)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### User Story 3 - [Brief Title] (Priority: P3)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

[Add more user stories as needed, each with an assigned priority]

### Edge Cases

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right edge cases.
-->

- What happens when [boundary condition]?
- How does system handle [error scenario]?

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
  IMPORTANT: All requirements must comply with the project constitution:
  - Temporary files must use .claude/tmp/ directory structure
  - Documentation must be in Chinese and placed in docs/ folder
  - Script files must use English naming
  - Python code must be compatible with 3.9+
  - No special Unicode characters in code
  - All features MUST support Windows, Linux, and macOS platforms
  - Portability takes priority over performance
  - Platform-specific optimizations must have >30% performance gain
  - Migration tools must provide interactive platform selection
-->

### Functional Requirements

- **FR-001**: System MUST [specific capability, e.g., "allow users to create accounts"]
- **FR-002**: System MUST [specific capability, e.g., "validate email addresses"]
- **FR-003**: Users MUST be able to [key interaction, e.g., "reset their password"]
- **FR-004**: System MUST [data requirement, e.g., "persist user preferences"]
- **FR-005**: System MUST [behavior, e.g., "log all security events"]
- **FR-006**: 系统必须在 `.claude/tmp/conversations/` 目录中存储临时对话记录
- **FR-007**: 文档必须使用中文编写并放置在 `docs/` 目录中
- **FR-008**: 每个功能组件必须包含 README.md 文件,说明功能作用、使用方法和配置说明
- **FR-009**: 代码必须遵循可读性优化要求,命名清晰,注释充分
- **FR-010**: 代码必须遵循高内聚低耦合原则,模块职责单一
- **FR-011**: 每个文件代码行数不得超过 1000 行(不含注释和空行)
- **FR-012**: 功能必须支持 Windows、Linux、macOS 三个平台
- **FR-013**: 默认实现必须使用跨平台解决方案
- **FR-014**: 文件路径操作必须使用跨平台库 (pathlib, tempfile 等)
- **FR-015**: 平台特定优化必须有明确的性能提升依据 (>30%)
- **FR-016**: 平台特定代码必须包含回退到跨平台实现的逻辑
- **FR-017**: 移植工具必须提供交互式平台选择功能
- **FR-018**: 系统不得在 Git 提交中包含敏感信息 (绝对路径、电子邮件、密码等)
- **FR-019**: 敏感配置必须使用环境变量或配置模板,不得硬编码
- **FR-020**: 测试数据和示例数据必须脱敏处理
- **FR-021**: 日志输出不得包含敏感信息,必须进行脱敏处理
- **FR-022**: `.env` 等敏感配置文件必须添加到 `.gitignore`

*Example of marking unclear requirements:*

- **FR-009**: System MUST authenticate users via [NEEDS CLARIFICATION: auth method not specified - email/password, SSO, OAuth?]
- **FR-010**: System MUST retain user data for [NEEDS CLARIFICATION: retention period not specified]

### Key Entities *(include if feature involves data)*

- **[Entity 1]**: [What it represents, key attributes without implementation]
- **[Entity 2]**: [What it represents, relationships to other entities]

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: [Measurable metric, e.g., "Users can complete account creation in under 2 minutes"]
- **SC-002**: [Measurable metric, e.g., "System handles 1000 concurrent users without degradation"]
- **SC-003**: [User satisfaction metric, e.g., "90% of users successfully complete primary task on first attempt"]
- **SC-004**: [Business metric, e.g., "Reduce support tickets related to [X] by 50%"]
