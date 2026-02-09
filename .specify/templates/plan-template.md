# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

[Extract from feature spec: primary requirement + technical approach from research]

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: [e.g., Python 3.11, Swift 5.9, Rust 1.75 or NEEDS CLARIFICATION]  
**Primary Dependencies**: [e.g., FastAPI, UIKit, LLVM or NEEDS CLARIFICATION]  
**Storage**: [if applicable, e.g., PostgreSQL, CoreData, files or N/A]  
**Testing**: [e.g., pytest, XCTest, cargo test or NEEDS CLARIFICATION]  
**Target Platform**: [e.g., Linux server, iOS 15+, WASM or NEEDS CLARIFICATION]
**Project Type**: [single/web/mobile - determines source structure]  
**Performance Goals**: [domain-specific, e.g., 1000 req/s, 10k lines/sec, 60 fps or NEEDS CLARIFICATION]  
**Constraints**: [domain-specific, e.g., <200ms p95, <100MB memory, offline-capable or NEEDS CLARIFICATION]  
**Scale/Scope**: [domain-specific, e.g., 10k users, 1M LOC, 50 screens or NEEDS CLARIFICATION]

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### 临时文件路径规范 (PRINCIPLE I)
- [ ] 所有临时文件使用 `.claude/tmp/` 目录
- [ ] 按功能类型正确分类 (conversations/, cache/, scripts/)
- [ ] 文件命名包含时间戳

### 文档语言规范 (PRINCIPLE II)
- [ ] 文档使用中文编写
- [ ] 脚本文件使用英文命名
- [ ] 代码注释保持一致性

### Python 版本兼容性 (PRINCIPLE III)
- [ ] Python 脚本兼容 3.9+
- [ ] 避免使用高版本特性

### 代码字符规范 (PRINCIPLE IV)
- [ ] 无特殊 Unicode 字符
- [ ] 仅使用 ASCII 字符集

### 文档组织规范 (PRINCIPLE V)
- [ ] Markdown 文档放置在 `docs/` 目录
- [ ] 按功能模块分类

### 组件自包含原则 (PRINCIPLE VI)
- [ ] 组件可独立运行
- [ ] 依赖关系明确声明

### README.md 强制要求 (PRINCIPLE VII)
- [ ] 每个功能组件包含 README.md
- [ ] README 使用中文编写
- [ ] 包含功能说明、使用方法、配置说明
- [ ] 包含依赖关系和注意事项
- [ ] 文档与代码实现同步

### 代码质量标准 (PRINCIPLE VIII)
- [ ] 变量、函数、类命名清晰表达用途
- [ ] 复杂逻辑添加注释说明
- [ ] 函数有完整的文档字符串
- [ ] 无魔法数字或字符串,已定义为常量
- [ ] 单个函数不超过 50 行
- [ ] 单个类不超过 300 行
- [ ] 模块职责单一,边界清晰
- [ ] 模块间依赖最小化,无循环依赖
- [ ] 使用依赖注入而非直接依赖具体实现
- [ ] 模块可以独立测试
- [ ] 每个文件不超过 1000 行代码

### 跨平台可移植性优先原则 (PRINCIPLE IX)
- [ ] 功能支持 Windows、Linux、macOS 三个平台
- [ ] 默认使用跨平台实现
- [ ] 平台特定优化有明确的性能提升依据 (>30%)
- [ ] 平台特定代码有回退到跨平台实现的逻辑
- [ ] 文件路径使用跨平台库 (pathlib, tempfile 等)
- [ ] 移植工具提供交互式平台选择
- [ ] 在目标平台进行了测试
- [ ] 文档中说明平台兼容性和限制

### 隐私保护与信息安全原则 (PRINCIPLE X)
- [ ] Git 提交前已运行隐私检查脚本
- [ ] 无绝对路径包含用户目录名 (如 /Users/username/, /home/username/)
- [ ] 无个人身份识别信息 (电子邮件、真实姓名、电话等)
- [ ] 无认证凭据 (密码、API 密钥、令牌等)
- [ ] 敏感配置使用环境变量或配置模板
- [ ] 测试数据已脱敏处理
- [ ] 日志输出不包含敏感信息
- [ ] `.env` 等敏感文件已添加到 `.gitignore`
- [ ] 文档和注释中无真实敏感信息

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
# [REMOVE IF UNUSED] Option 1: Single project (DEFAULT)
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# [REMOVE IF UNUSED] Option 2: Web application (when "frontend" + "backend" detected)
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

# [REMOVE IF UNUSED] Option 3: Mobile + API (when "iOS/Android" detected)
api/
└── [same as backend above]

ios/ or android/
└── [platform-specific structure: feature modules, UI flows, platform tests]
```

**Structure Decision**: [Document the selected structure and reference the real
directories captured above]

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
