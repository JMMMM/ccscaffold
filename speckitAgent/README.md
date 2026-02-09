# SpecKit Agent 功能

## 功能说明

SpecKit Agent 是一个执行 spec-kit 方法论进行系统化功能开发的智能代理。它通过按正确顺序执行斜杠命令，引导用户完成完整的功能开发工作流。

### 主要特点

- **自动化工作流**: 按照预定义的顺序执行 spec-kit 命令
- **进度跟踪**: 自动检测用户已完成的工作，从中断处继续
- **智能引导**: 在每个步骤提供清晰的说明和状态更新
- **灵活暂停**: 在需要用户输入时自动暂停等待
- **中文支持**: 所有交互使用中文进行

### 工作流步骤

1. `/speckit.constitution` - 生成质量和一致性治理原则
2. `/speckit.specify` - 定义功能需求和范围
3. `/speckit.clarify` - 使用问答填补空白和解决歧义
4. `/speckit.checklist` - 创建验证检查清单
5. `/speckit.plan` - 制定实施计划
6. `/speckit.tasks` - 分解为可执行任务
7. `/speckit.analyze` - 分析方法
8. `/speckit.checklist` - 最终验证检查清单
9. `/speckit.implement` - 按照计划开始执行

## 使用方法

### 前置条件

1. 确保已安装 Claude Code
2. 确保已配置 spec-kit 相关命令
3. 确保 `.claude/agents/` 目录存在

### 基本使用

#### 方法 1: 自动安装(推荐)

使用 CC-Scaffold 的迁移脚本:

```bash
# 在目标项目中运行
python /path/to/ccscaffold/scripts/migrate_experience.py
# 选择 speckitAgent 功能
```

#### 方法 2: 手动安装

1. **复制文件到项目**:
   ```bash
   # 复制 agent
   cp speckitAgent/agents/speckitAgent.md .claude/agents/
   ```

2. **重启 Claude Code**

### 使用场景

#### 场景 1: 开始新的功能开发

```
user: 使用spec-kit，完成一个团队看板+评论功能的需求
assistant: 我将使用spec-kit-feature-agent来为您的团队看板+评论功能执行spec-kit工作流。
```

#### 场景 2: 继续未完成的工作流

```
user: 我已经执行了/speckit.constitution和/speckit.specify，现在需要继续
assistant: 我将使用spec-kit-feature-agent从您中断的地方继续spec-kit工作流。
```

#### 场景 3: 指定使用 spec-kit 方法论

```
user: 我想用spec-kit来实现一个用户认证系统
assistant: 我将使用spec-kit-feature-agent来执行spec-kit工作流，帮您系统化地开发用户认证系统功能。
```

## 配置说明

### 必需配置

无。该功能不需要额外的配置。

### 可选配置

#### Agent 模型

默认: `sonnet`

可在 agent 配置文件中修改 `model` 字段来更改使用的模型。

#### 主题颜色

默认: `cyan`

可在 agent 配置文件中修改 `color` 字段来更改显示颜色。

### 环境变量

无。

## 依赖关系

- **Claude Code**: 必需,版本 1.0+
- **spec-kit commands**: 必需,所有 `/speckit.*` 命令

## 目录结构

```
speckitAgent/
├── agents/
│   └── speckitAgent.md        # Agent 配置文件
├── docs/
│   └── speckit-agent.md       # 使用文档
├── commands/                  # 命令目录(预留)
├── skills/                    # 技能目录(预留)
├── hooks/                     # 钩子目录(预留)
└── README.md                  # 本文件
```

## 注意事项

1. **命令顺序**: Agent 严格按照预定义的顺序执行命令，不可跳过
2. **用户交互**: 在需要用户输入时（如 clarify 阶段），Agent 会暂停等待
3. **进度保存**: 建议在每步完成后保存工作，以便从中断处继续
4. **命令依赖**: 确保所有 `/speckit.*` 命令都已正确配置
5. **模型选择**: 使用 sonnet 模型可获得最佳平衡的性能和成本

## 故障排除

### 问题 1: Agent 没有响应

**症状**: 调用 Agent 时没有反应

**解决方案**:
1. 检查 agent 文件是否在正确的位置 (`.claude/agents/`)
2. 确认文件格式正确 (YAML frontmatter + markdown 内容)
3. 重启 Claude Code

### 问题 2: 命令执行失败

**症状**: Agent 执行命令时出现错误

**解决方案**:
1. 确认所有 `/speckit.*` 命令已正确配置
2. 检查命令路径是否正确
3. 查看错误日志了解具体失败原因

### 问题 3: 进度跟踪不准确

**症状**: Agent 没有正确识别已完成的步骤

**解决方案**:
1. 确认相关文档 (spec.md, plan.md, tasks.md) 存在
2. 检查文档内容是否符合预期格式
3. 手动指定需要执行的命令

## 相关文档

- [使用文档](docs/speckit-agent.md)
- [SpecKit 官方文档](https://github.com/anthropics/spec-kit)

## 更新日志

- v1.0.0 (2025-02-09): 初始版本
