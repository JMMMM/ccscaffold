# Continuous Learning - 持续学习功能

## 功能说明

持续学习功能自动分析 Claude Code 对话内容，检测反复出现的问题（≥3次沟通未解决），并生成结构化的学习技能，帮助从错误中学习并改进后续对话质量。

### 主要特点

- **自动分析**: SessionEnd 钩子自动触发，无需手动操作
- **手动触发**: 支持 `/summary-skills` 命令手动分析
- **智能检测**: 检测反复问题模式（沟通次数≥3次）
- **技能生成**: 使用 Claude API 生成学习技能
- **状态跟踪**: 避免重复分析，记录已处理的对话位置
- **可配置**: 支持配置对话数量、文件路径等参数

## 使用方法

### 前置条件

1. 确保已安装 Claude Code
2. 确保已启用 Hooks 功能
3. 确保对 `.claude` 目录有写权限
4. 建议先安装"会话记录"功能，以便有对话数据可供分析

### 基本使用

#### 自动触发（推荐）

会话结束时自动触发分析，无需手动操作。

#### 手动触发

在 Claude Code 对话中输入：

```
/summary-skills
```

### 高级用法

#### 配置对话数量

编辑 `.claude/skills/continuous-learning/config.json`:

```json
{
  "max_conversations": 30
}
```

#### 指定对话文件

```bash
python3.9 .claude/skills/continuous-learning/scripts/summary_skills.py --conversation-file /path/to/conversation.txt
```

## 配置说明

### 必需配置

无。该功能使用默认配置即可工作。

### 可选配置

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `max_conversations` | 20 | 读取的最大对话条数 |
| `retry_threshold` | 3 | 触发技能生成的反复次数阈值 |
| `conversation_file` | `.claude/conversations/conversation.txt` | 对话文件路径 |
| `skills_output_dir` | `.claude/skills/learn` | 技能输出目录 |
| `state_file` | `.claude/skills/continuous-learning/state.json` | 状态文件路径 |

### 环境变量

无。

## 依赖关系

- **Claude Code**: 必需，版本 1.0+
- **Python**: 3.9+ (用于脚本)
- **会话记录功能**: 推荐，用于提供对话数据

## 注意事项

1. **API 调用**: 生成技能需要调用 Claude API，可能需要几秒钟
2. **质量审核**: 生成的技能需要人工审核后才能使用
3. **状态跟踪**: 首次运行后会创建状态文件，记录分析进度
4. **平台兼容**: 支持 Windows、Linux、macOS 三个平台
5. **性能**: 钩子执行时间 < 60 秒，不影响会话正常结束

## 工作流程

1. **触发**: SessionEnd 钩子或 `/summary-skills` 命令
2. **读取**: 从对话文件读取最近 N 条对话
3. **分析**: 检测反复问题模式（≥3次）
4. **生成**: 使用 Claude API 生成学习技能
5. **保存**: 将技能保存到 `.claude/skills/learn/` 目录
6. **更新**: 更新状态文件，记录已处理的对话位置

## 目录结构

```
.claude/
├── commands/
│   └── summary-skills.md        # 手动触发命令
├── skills/
│   └── continuous-learning/
│       ├── skill.json           # 技能配置
│       ├── SKILL.md             # 技能说明
│       ├── config.json          # 功能配置
│       └── scripts/
│           ├── models.py        # 数据模型
│           ├── config.py        # 配置管理
│           ├── state_manager.py # 状态管理
│           ├── prompts.py       # 提示词模板
│           ├── conversation_reader.py  # 对话读取
│           ├── issue_analyzer.py       # 问题分析
│           ├── skill_generator.py      # 技能生成
│           ├── summary_skills.py       # 核心脚本
│           └── session_end_hook.py     # SessionEnd 钩子
└── skills/learn/                 # 生成的技能存储目录
```

## 故障排除

### 问题 1: 没有检测到任何问题

**症状**: 运行后提示"未检测到反复问题"

**解决方案**:
1. 检查对话文件是否存在
2. 确认对话内容是否包含反复提及的问题
3. 增加 `max_conversations` 值
4. 降低 `retry_threshold` 值

### 问题 2: Claude API 调用失败

**症状**: 提示"Claude API 调用失败"

**解决方案**:
1. 检查 Claude Code 配置
2. 确认网络连接正常
3. 查看 Claude Code 日志

### 问题 3: 生成的技能质量不好

**症状**: 技能内容不准确或不完整

**解决方案**:
1. 检查对话内容是否充分
2. 增加 `max_conversations` 值
3. 人工编辑生成的技能

## 最佳实践

1. **定期审核**: 定期检查生成的技能，删除低质量内容
2. **调整参数**: 根据实际情况调整配置参数
3. **人工优化**: 对生成的技能进行人工优化和分类
4. **版本控制**: 将生成的技能纳入版本控制

## 相关文档

- [功能文档](docs/continuous-learning.md)
- [使用指南](docs/continuous-learning-usage.md)
- [实现计划](../specs/1-continuous-learning/plan.md)

## 更新日志

- v2.0.0 (2026-02-09): 全面重构，支持自动和手动触发
- v1.0.0: 初始版本
