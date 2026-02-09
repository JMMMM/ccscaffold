# Continuous Learning - 持续学习功能

## 功能概述

持续学习功能自动分析 Claude Code 对话内容，检测反复出现的问题（≥3次沟通未解决），并生成结构化的学习技能，帮助从错误中学习并改进后续对话质量。

## 核心功能

### 1. 自动会话总结

- **触发方式**: 会话结束时（SessionEnd 钩子）
- **功能**: 自动读取最近 20 条对话，检测反复问题，生成学习技能
- **优势**: 无需手动操作，在后台自动积累知识

### 2. 手动触发总结

- **触发方式**: `/summary-skills` 命令
- **功能**: 主动分析当前对话，生成学习技能
- **优势**: 可以随时触发，不受会话限制

### 3. 配置灵活性

- **可配置参数**:
  - `max_conversations`: 读取的最大对话条数（默认: 20）
  - `retry_threshold`: 触发技能生成的反复次数阈值（默认: 3）
  - `conversation_file`: 对话文件路径
  - `skills_output_dir`: 技能输出目录
- **配置方式**: 修改 `.claude/skills/continuous-learning/config.json`

## 工作原理

### 问题检测算法

1. **关键词匹配**: 检测包含重试关键词的对话
2. **相似度分析**: 识别不同表述的同一问题
3. **阈值判断**: 当沟通次数 ≥ 3 时触发技能生成

### 技能生成流程

1. **问题识别**: 从对话中提取问题主题和关键词
2. **模式分析**: 总结问题的常见模式
3. **解决方案提取**: 从对话中提取解决步骤
4. **技能生成**: 生成结构化的 markdown 格式技能文件

### 状态跟踪

- 记录已处理的对话行数
- 避免重复分析相同内容
- 支持增量分析

## 技术架构

### 核心组件

```
conversation_reader.py  # 对话文件读取器
    ↓
issue_analyzer.py     # 问题分析器
    ↓
skill_generator.py    # 技能生成器
    ↓
summary_skills.py     # 核心脚本（整合）
```

### 数据流

```
conversation.txt
    ↓ (读取最近 N 条)
ConversationEntry[]
    ↓ (分析问题模式)
IssuePattern[]
    ↓ (生成技能)
LearnedSkill
    ↓ (保存到文件)
.claude/skills/learn/{skill-name}.md
```

## 配置指南

### 基础配置

`.claude/skills/continuous-learning/config.json`:

```json
{
  "max_conversations": 20,
  "retry_threshold": 3,
  "conversation_file": ".claude/conversations/conversation.txt",
  "skills_output_dir": ".claude/skills/learn",
  "state_file": ".claude/skills/continuous-learning/state.json",
  "keywords": {
    "retry": ["修复", "修正", "解决", "还是不行", "还是有问题", "继续", "再试"],
    "issues": ["问题", "bug", "错误", "失败"]
  }
}
```

### 高级配置

#### 自定义关键词

根据项目特点添加自定义关键词：

```json
{
  "keywords": {
    "retry": ["重试", "再次尝试", "仍然"],
    "issues": ["缺陷", "异常", "故障"]
  }
}
```

#### 调整阈值

```json
{
  "max_conversations": 50,    // 增加分析范围
  "retry_threshold": 2      // 降低阈值，更敏感
}
```

## 使用示例

### 示例 1: 自动检测数据日历问题

**对话片段**:
```
user> 数据日历中，2月1日（星期日）显示红色
...
user> 问题没有得到解决，2月7日也显示红色
...
user> 还是显示红色，2月8日（星期六）也是
```

**生成的技能**:

```markdown
# fix-weekend-display-issue

## 问题概述
数据日历在非交易日错误地显示任务状态

## 触发点识别
当用户提到"周末显示红色"、"交易日"、"数据日历"时参考此技能

## 修复规律总结
- 根本原因: 交易日判断默认值错误（True → False）
- 解决方案: 修改默认值为 False，只在明确标记为交易日时检查

## 使用建议
- 使用明确的默认值（False 而非 True）
- 在涉及条件判断时，默认值应该是"更安全"的选项
```

### 示例 2: 检测代码反复修改失败

**对话片段**:
```
user> 修复这个 bug
...
user> 还是不能正常工作
...
user> 再次尝试修复
```

**生成的技能**:

```markdown
# fix-repeated-bug-attempts

## 问题概述
某个 bug 经过多次修复仍未解决

## 触发点识别
当用户反复提到同一个 bug，且沟通次数 ≥ 3 时

## 修复规律总结
- 可能原因: 未理解根本原因，只修复表面现象
- 建议: 深入分析代码逻辑，使用调试工具定位根因
```

## 最佳实践

### 1. 定期审核生成的技能

- 查看 `.claude/skills/learn/` 目录
- 删除低质量或过时的技能
- 合并相似的技能

### 2. 调整参数

- 对话项目较多: 增加 `max_conversations`
- 问题较复杂: 降低 `retry_threshold`
- 测试阶段: 使用较少对话条数

### 3. 结合人工审核

- 生成的技能需要人工审核后才能使用
- 可以手动编辑技能内容
- 删除不准确的技能

## 注意事项

1. **性能影响**: SessionEnd 钩子会增加会话结束时间（< 60 秒）
2. **API 调用**: 生成技能需要调用 Claude API
3. **文件权限**: 确保对 `.claude` 目录有写权限
4. **平台兼容**: 支持 Windows、Linux、macOS
5. **隐私保护**: 生成的技能会包含对话内容摘要，注意敏感信息

## 故障排除

### 问题: 没有检测到任何问题

**可能原因**:
- 对话内容没有达到反复阈值（< 3次）
- 关键词配置不匹配

**解决方案**:
- 增加 `max_conversations` 值
- 调整 `retry_threshold` 值
- 检查对话内容是否真的有反复问题

### 问题: 生成的技能质量不好

**可能原因**:
- 对话上下文不足
- 问题模式不够清晰

**解决方案**:
- 增加 `max_conversations` 值
- 人工编辑生成的技能
- 删除低质量技能

### 问题: Claude API 调用失败

**可能原因**:
- API 密钥未配置
- 网络连接问题

**解决方案**:
- 检查 Claude Code 配置
- 确认网络连接正常

## 相关文档

- [使用指南](continuous-learning-usage.md)
- [实现计划](../../specs/1-continuous-learning/plan.md)
- [数据模型](../../specs/1-continuous-learning/data-model.md)
