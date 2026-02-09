# CC-Scaffold 更新日志

## [2.2.0] - 2026-02-09

### 新增 (Added)

- **Principle X: 隐私保护与信息安全原则**
  - 添加 Git 提交前隐私检查脚本 (`scripts/git/privacy_check.py`)
  - 添加 Git 钩子安装脚本 (`scripts/git/install_git_hooks.sh`, `.py`)
  - 添加数据脱敏工具模块 (`ccscaffold/utils/privacy_utils.py`)
  - 更新 `.gitignore` 添加隐私相关忽略规则
  - 更新主 README.md 添加隐私保护说明

- **隐私保护功能**
  - 自动检测敏感信息（电子邮件、绝对路径、API 密钥、密码、IP 地址等）
  - Git 提交前自动检查，阻止包含敏感信息的提交
  - 提供数据脱敏工具类，支持日志、路径、字典等数据结构脱敏
  - 安全打印路径功能，自动隐藏用户名

### 更新 (Changed)

- **宪章版本**: 1.3.0 -> 1.4.0
  - 新增 Principle X: 隐私保护与信息安全原则
  - 更新所有模板文件包含隐私合规检查项

- **模板更新**
  - `plan-template.md`: 添加隐私合规检查项
  - `spec-template.md`: 添加隐私需求 (FR-018 ~ FR-022)
  - `tasks-template.md`: 添加隐私合规清单
  - `checklist-template.md`: 添加隐私检查项 (CHK025 ~ CHK033)
  - `agent-file-template.md`: 添加隐私安全规范

### 文档 (Documentation)

- 新增 `scripts/git/README.md` - Git 隐私检查工具文档
- 新增 `ccscaffold/__init__.py` - 包初始化文件
- 新增 `ccscaffold/utils/__init__.py` - 工具模块初始化
- 更新主 README.md 添加隐私保护章节

### 安全 (Security)

- 默认阻止包含敏感信息的 Git 提交
- 增强日志脱敏功能
- 更新 `.gitignore` 防止敏感文件被提交

## [2.1.0] - 2025-02-09

### 新增 (Added)

- **functionUse 和 functionRemove 命令**
  - 简化功能部署和移除流程
  - 支持一键安装/卸载所有 CC-Scaffold 功能

### 更新 (Changed)

- **宪章版本**: 1.2.0 -> 1.3.0
  - 新增跨平台可移植性优先原则 (Principle IX)

### 文档 (Documentation)

- 更新所有模板包含跨平台要求

## [2.0.0] - 2025-02-08

### 重大变更 (Breaking Changes)

- 重构项目结构，采用功能模块化组织
- 新增 SpecKit Agent 支持

### 新增 (Added)

- **持续学习功能** (continous-learning)
  - 自动分析对话内容
  - 检测反复修改失败的模式
  - 生成修复 skill

- **SpecKit Agent** (speckitAgent)
  - 执行 spec-kit 方法论
  - 自动化工作流
  - 进度跟踪

### 更新 (Changed)

- **宪章版本**: 1.1.0 -> 1.2.0
  - 新增代码质量标准 (Principle VIII)
  - 新增 README.md 强制要求 (Principle VII)

## [1.0.0] - 2025-01-XX

### 初始版本

- **会话记录功能** (chat-record)
- **组件打包功能** (package-skills)
- **项目宪章** (Principle I-VI)
