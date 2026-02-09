# Tasks: Continuous Learning Refactor

**Feature**: 1-continuous-learning
**Date**: 2026-02-09
**Spec**: [spec.md](./spec.md)
**Plan**: [plan.md](./plan.md)

## Overview

本功能实现自动分析 Claude Code 对话内容并生成学习技能的系统。包含三个核心用户故事：自动会话总结（P1）、手动触发总结（P2）、配置灵活性（P3）。

**修改范围**:
- 新增: `.claude/commands/summary-skills.md`
- 新增: `.claude/skills/continuous-learning/` 目录及脚本
- 新增: `ccscaffold/continuous-learning/` 组件目录
- 修改: `.claude/settings.json` 添加钩子配置

## Task Summary

| Phase | Tasks | Description |
|-------|-------|-------------|
| Phase 1 | 4 | Setup & Foundational |
| Phase 2 | 5 | User Story 1: 自动会话总结 (P1) |
| Phase 3 | 4 | User Story 2: 手动触发总结 (P2) |
| Phase 4 | 3 | User Story 3: 配置灵活性 (P3) |
| Phase 5 | 5 | Polish & Cross-Cutting |
| **Total** | **21** | |

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: 项目初始化和基础结构

- [x] T001 创建目录结构: `.claude/skills/continuous-learning/`, `.claude/skills/learn/`, `ccscaffold/continuous-learning/`
- [x] T002 [P] 创建 `.claude/skills/continuous-learning/config.json` 配置文件模板
- [x] T003 [P] 创建 `ccscaffold/continuous-learning/README.md` 组件文档（中文）
- [x] T004 验证 Python 3.9+ 可用性和跨平台兼容性

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: 核心基础设施，必须在任何用户故事实现之前完成

**⚠️ CRITICAL**: 在此阶段完成之前，不能开始任何用户故事工作

- [x] T005 [P] 创建数据模型类: `ccscaffold/continuous-learning/skills/continuous-learning/scripts/models.py` (ConversationEntry, IssuePattern, LearnedSkill)
- [x] T006 [P] 创建配置管理: `ccscaffold/continuous-learning/skills/continuous-learning/scripts/config.py` (Config 类)
- [x] T007 创建状态管理: `ccscaffold/continuous-learning/skills/continuous-learning/scripts/state_manager.py` (State, StateManager 类)
- [x] T008 创建提示词模板: `ccscaffold/continuous-learning/skills/continuous-learning/scripts/prompts.py` (SUMMARY_PROMPT 常量)

**Checkpoint**: 基础设施就绪 - 用户故事实现现在可以并行开始

---

## Phase 3: User Story 1 - 自动会话总结 (Priority: P1) 🎯 MVP

**Goal**: 实现会话结束时自动分析对话并生成技能的核心功能

**Independent Test**: 触发 SessionEnd 钩子，验证是否正确读取对话、分析问题模式并生成技能文件

### Implementation for User Story 1

- [x] T009 [P] [US1] 创建对话读取器: `ccscaffold/continuous-learning/skills/continuous-learning/scripts/conversation_reader.py` (ConversationReader 类)
- [x] T010 [P] [US1] 创建问题分析器: `ccscaffold/continuous-learning/skills/continuous-learning/scripts/issue_analyzer.py` (IssueAnalyzer 类)
- [x] T011 [P] [US1] 创建技能生成器: `ccscaffold/continuous-learning/skills/continuous-learning/scripts/skill_generator.py` (SkillGenerator 类)
- [x] T012 [US1] 创建核心分析脚本: `ccscaffold/continuous-learning/skills/continuous-learning/scripts/summary_skills.py` (main 函数，整合所有组件)
- [x] T013 [US1] 创建 SessionEnd 钩子: `ccscaffold/continuous-learning/skills/continuous-learning/scripts/session_end_hook.py` (检测 Stop 事件并调用 summary_skills.py)

**Checkpoint**: 此时，User Story 1 应该完全功能化且可独立测试

---

## Phase 4: User Story 2 - 手动触发总结 (Priority: P2)

**Goal**: 用户可以通过命令手动触发总结功能

**Independent Test**: 执行 `/summary-skills` 命令，验证是否正确读取对话并生成技能

### Implementation for User Story 2

- [x] T014 [P] [US2] 创建命令定义: `.claude/commands/summary-skills.md` (命令说明和使用方法)
- [x] T015 [US2] 创建技能配置: `.claude/skills/continuous-learning/skill.json` (技能元数据)
- [x] T016 [US2] 创建技能说明: `.claude/skills/continuous-learning/SKILL.md` (技能功能说明)
- [x] T017 [US2] 更新全局配置: 在 `.claude/settings.json` 中添加 SessionEnd 钩子配置（如果尚未添加）

**Checkpoint**: 此时，User Stories 1 和 2 都应该独立工作

---

## Phase 5: User Story 3 - 配置灵活性 (Priority: P3)

**Goal**: 支持用户配置对话数量、文件路径等参数

**Independent Test**: 修改配置文件，验证参数是否正确生效

### Implementation for User Story 3

- [x] T018 [P] [US3] 扩展配置管理: 在 `config.py` 中添加命令行参数解析 (argparse, --max-conversations, --conversation-file) - 已实现
- [x] T019 [US3] 更新核心脚本: 在 `summary_skills.py` 中应用配置参数（从命令行或配置文件读取） - 已实现
- [x] T020 [US3] 创建配置示例: `ccscaffold/continuous-learning/config.example.json` (配置模板和说明)

**Checkpoint**: 所有用户故事现在应该独立功能化

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: 影响多个用户故事的改进

- [x] T021 [P] 创建功能文档: `ccscaffold/continuous-learning/docs/continuous-learning.md` (中文，功能说明)
- [x] T022 [P] 创建使用指南: `ccscaffold/continuous-learning/docs/continuous-learning-usage.md` (中文，使用方法)
- [x] T023 同步脚本到运行目录: 复制脚本从 `ccscaffold/continuous-learning/` 到 `.claude/skills/continuous-learning/`
- [x] T024 验证所有 README.md 包含必需章节（功能说明、使用方法、配置说明、依赖关系、注意事项）
- [x] T025 验证跨平台兼容性（Windows, Linux, macOS）

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: 无依赖 - 可以立即开始
- **Foundational (Phase 2)**: 依赖 Setup 完成 - 阻塞所有用户故事
- **User Stories (Phase 3-5)**: 都依赖 Foundational 完成
  - User Story 1 (P1): Foundational 完成后可开始 - 无其他用户故事依赖
  - User Story 2 (P2): Foundational 完成后可开始 - 可与 US1 并行
  - User Story 3 (P3): Foundational 完成后可开始 - 可与 US1/US2 并行
- **Polish (Phase 6)**: 依赖所需用户故事完成

### User Story Dependencies

- **User Story 1 (P1)**: Foundational 完成后可开始 - 不依赖其他用户故事
- **User Story 2 (P2)**: Foundational 完成后可开始 - 应与 US1 独立可测试
- **User Story 3 (P3)**: Foundational 完成后可开始 - 扩展 US1/US2 功能

### Within Each Phase

- 基础模型类优先 (T005-T008)
- 核心组件类其次 (T009-T011)
- 集成脚本最后 (T012-T013)

### Parallel Opportunities

- Phase 1 中的 T002, T003 可以并行（不同文件）
- Phase 2 中的 T005, T006, T007, T008 可以并行（不同文件）
- Phase 3 中的 T009, T010, T011 可以并行（不同文件）
- Phase 4 中的 T014, T015, T016 可以并行（不同文件）
- Phase 5 中的 T018, T020 可以并行（不同文件）
- Phase 6 中的 T021, T022 可以并行（不同文件）

---

## Parallel Example: User Story 1

```bash
# 并行创建核心组件（不同文件，无依赖）:
Task T009: ConversationReader
Task T010: IssueAnalyzer
Task T011: SkillGenerator

# 等待组件完成后，运行集成:
Task T012: summary_skills.py (depends on T009-T011)
Task T013: session_end_hook.py (depends on T012)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. 完成 Phase 1: Setup
2. 完成 Phase 2: Foundational (CRITICAL - 阻塞所有故事)
3. 完成 Phase 3: User Story 1
4. **停止并验证**: 独立测试 User Story 1
5. 如果准备就绪，部署/演示

### Incremental Delivery

1. 完成 Setup + Foundational → 基础就绪
2. 添加 User Story 1 → 独立测试 → 部署/演示 (MVP!)
3. 添加 User Story 2 → 独立测试 → 部署/演示
4. 添加 User Story 3 → 独立测试 → 部署/演示
5. 每个故事增加价值而不破坏之前的故事

### Parallel Team Strategy

有多个开发者时：

1. 团队一起完成 Setup + Foundational
2. Foundational 完成后:
   - 开发者 A: User Story 1
   - 开发者 B: User Story 2
   - 开发者 C: User Story 3
3. 故事独立完成和集成

---

## Compliance Checklist

在标记任何任务完成之前，验证：

- [ ] 临时文件使用 `.claude/tmp/` 并有适当的子目录结构
- [ ] 文档使用中文并放置在 `docs/` 目录
- [ ] 脚本文件使用英文命名
- [ ] Python 代码兼容 3.9+
- [ ] 代码中无特殊 Unicode 字符
- [ ] 组件自包含且有明确的依赖关系
- [ ] **每个功能组件有 README.md**
- [ ] **README 包含所有必需章节（功能说明、使用方法、配置说明、依赖关系、注意事项）**
- [ ] **代码遵循可读性标准：命名清晰、注释充分**
- [ ] **代码遵循高内聚低耦合原则**
- [ ] **无魔法数字或字符串，都定义为常量**
- [ ] **函数少于 50 行，类少于 300 行**
- [ ] **每个文件少于 1000 行代码（不包括注释/空行）**
- [ ] **功能支持 Windows、Linux 和 macOS 平台**
- [ ] **默认实现使用跨平台解决方案**
- [ ] **平台特定优化有 >30% 性能提升的正当理由**
- [ ] **平台特定代码包含回退到跨平台实现的逻辑**
- [ ] **文件路径使用跨平台库（pathlib, tempfile 等）**
- [ ] **移植工具提供交互式平台选择**
- [ ] **功能在所有三个目标平台上测试**
- [ ] **文档包含平台兼容性说明和限制**
- [ ] **Git 提交通过隐私安全检查**
- [ ] **代码中无敏感信息（绝对路径、电子邮件、凭据）**
- [ ] **敏感配置使用环境变量或模板**
- [ ] **测试数据已匿名化和掩码**
- [ ] **日志输出不包含敏感信息**
- [ ] **`.env` 和其他敏感文件已添加到 `.gitignore`**

---

## File Structure Reference

```
.claude/
├── commands/
│   └── summary-skills.md                # T014
├── skills/
│   └── continuous-learning/
│       ├── skill.json                   # T015
│       ├── SKILL.md                     # T015
│       ├── config.json                  # T002
│       └── scripts/
│           ├── models.py                # T005
│           ├── config.py                # T006
│           ├── state_manager.py         # T007
│           ├── prompts.py               # T008
│           ├── conversation_reader.py   # T009
│           ├── issue_analyzer.py        # T010
│           ├── skill_generator.py       # T011
│           ├── summary_skills.py        # T012
│           └── session_end_hook.py      # T013
└── settings.json                        # T017

ccscaffold/continuous-learning/
├── README.md                             # T003
├── config.example.json                   # T020
├── docs/
│   ├── continuous-learning.md            # T021
│   └── continuous-learning-usage.md      # T022
└── skills/
    └── continuous-learning/
        └── scripts/                      # T023 (同步到 .claude/skills/)

.claude/skills/learn/                      # 生成的技能存储目录
```

---

## Notes

- [P] 任务 = 不同文件，无依赖
- [Story] 标签将任务映射到特定用户故事以便追溯
- 每个用户故事应该可独立完成和测试
- 每个任务或逻辑组后提交
- 在任何检查点停止以独立验证故事
- 避免：模糊任务、同文件冲突、破坏独立性的跨故事依赖
