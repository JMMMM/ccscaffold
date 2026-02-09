# Continuous Learning - 持续学习功能

## 功能概述

持续学习功能自动分析对话内容，检测反复修改失败的情况，并生成相应的修复 skill，帮助 Claude 从错误中学习并改进。

## 核心功能

- **自动问题检测**: 检测对话中反复出现的修改失败模式
- **智能总结**: 分析问题根因并生成解决方案
- **自动生成 skill**: 将学习到的经验保存为可复用的 skill
- **命令触发**: 支持手动触发总结功能

## 使用方法

### 自动触发（待实现）

持续学习功能应该在以下情况下自动触发：
- 会话结束时（SessionEnd hook）
- 检测到多次修改失败时

### 手动触发

使用命令手动触发总结功能：

```bash
# 在 Claude Code 对话中输入
/summary-skills
```

## 配置说明

### skill.json 配置

```json
{
  "name": "continuous-learning",
  "description": "持续学习功能 - 分析对话中反复出现的问题并生成修复 skill",
  "version": "1.0.0",
  "commands": [
    {
      "name": "summary-skills",
      "description": "分析当前对话内容,检测反复修改失败的情况并生成修复 skill",
      "matcher": "/summary-skills",
      "handler": "python3 ${PROJECT_DIR}/skills/continuous-learning/scripts/summary_skills.py"
    }
  ],
  "configuration": {
    "learns_dir": "skills/learns",
    "retry_threshold": 3
  }
}
```

### 配置参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `learns_dir` | 生成的 skill 保存目录 | `skills/learns` |
| `retry_threshold` | 触发总结的失败次数阈值 | `3` |

## 目录结构

```
skills/continuous-learning/
├── skill.json              # 功能配置文件
├── SKILL.md                # 功能说明文档
├── CLAUDE.md               # 本文件
└── scripts/
    └── summary_skills.py   # 总结脚本
```

## 工作流程

1. **触发**: 通过命令或自动触发
2. **分析**: 读取对话历史，检测重复失败模式
3. **总结**: 使用 Claude 分析问题根因和解决方案
4. **生成**: 创建新的 skill 文件
5. **保存**: 将 skill 保存到 `learns_dir` 指定的目录

## 输出示例

生成的 skill 文件将包含：

- 问题描述
- 失败模式分析
- 解决方案步骤
- 预防措施

## 使用文档

详细使用文档请参考: [docs/continuous-learning.md](../../docs/continuous-learning.md)

## 注意事项

1. Python 版本要求: Python 3.9+
2. 需要确保 `learns_dir` 目录有写权限
3. 生成的 skill 需要人工审核后才能启用
4. 建议定期清理和整理生成的 skill

## 依赖关系

- 依赖于 `.claude/conversations/` 目录中的对话历史
- 可能与其他 context-manager 类功能配合使用
