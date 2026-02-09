# 持续学习功能 (Continuous Learning)

## 功能说明

自动总结 Claude Code 对话内容并生成 skills,实现知识的持续积累和复用。

### 主要特点

- **自动总结**: SessionEnd 钩子触发,自动分析最近对话
- **智能生成**: 使用 Claude 总结对话并生成 skill
- **自动保存**: 生成的 skills 自动保存到 skills 目录
- **可配置**: 可设置总结的对话数量阈值

## 使用方法

### 前置条件

1. 确保已安装 Claude Code
2. 确保已启用 Hooks 功能
3. 确保有对 `.claude` 目录的写权限
4. 建议先安装"会话记录"功能,以便有对话数据可供总结

### 基本使用

#### 方法 1: 自动安装(推荐)

使用 CC-Scaffold 的迁移脚本:

```bash
# 在目标项目中运行
python /path/to/ccscaffold/scripts/migrate_experience.py
# 选择 continous-learning 功能
```

#### 方法 2: 手动安装

1. **复制文件到项目**:
   ```bash
   # 复制 skills
   cp -r continous-learning/skills/continuous-learning .claude/skills/

   # 复制脚本
   cp continous-learning/skills/continuous-learning/scripts/summary_skills.py .claude/skills/
   ```

2. **配置 settings.json**:

   在项目的 `.claude/settings.json` 中添加:

   ```json
   {
     "hooks": {
       "SessionEnd": [
         {
           "script": "../.claude/skills/continuous-learning/scripts/summary_skills.py",
           "description": "持续学习:自动总结对话并生成 skills"
         }
       ]
     }
   }
   ```

3. **重启 Claude Code**

### 高级用法

#### 调整总结阈值

修改脚本中的对话数量要求:

```python
# 在 summary_skills.py 中
MIN_CONVERSATIONS = 10  # 修改为自定义数量
```

#### 自定义总结 prompt

修改脚本中的总结 prompt 模板:

```python
SUMMARY_PROMPT = """
根据以下对话内容,生成一个 skill:
{conversation_text}

要求:
1. 提取关键知识点
2. 生成可复用的 skill
3. 使用标准格式
"""
```

## 配置说明

### 必需配置

无。该功能不需要额外的配置。

### 可选配置

#### 对话数量阈值

默认: 10 条对话

可通过修改脚本中的 `MIN_CONVERSATIONS` 变量来自定义。

#### 总结输出目录

默认: `.claude/skills/`

可通过修改脚本中的输出路径来自定义。

### 环境变量

无。

## 依赖关系

- **Claude Code**: 必需,版本 1.0+
- **Python**: 3.9+ (用于总结脚本)
- **会话记录功能**: 推荐,用于提供对话数据

## 注意事项

1. **API 调用**: 总结过程会调用 Claude API,可能产生费用
2. **对话数量**: 只有当对话数量达到阈值时才会总结
3. **时间消耗**: SessionEnd 钩子可能会延长会话结束时间
4. **文件权限**: 确保 `.claude/skills/` 目录有写权限
5. **质量控制**: 生成的 skills 需要人工审核后使用

## 工作流程

1. **会话结束**: SessionEnd 钩子被触发
2. **读取对话**: 从 `.claude/tmp/conversations/` 读取最新的对话文件
3. **数量检查**: 检查对话数量是否达到阈值
4. **调用 Claude**: 如果达到阈值,调用 Claude API 进行总结
5. **生成 Skill**: 根据总结内容生成 skill 文件
6. **保存文件**: 将 skill 保存到 `.claude/skills/` 目录

## 目录结构

```
continous-learning/
├── skills/
│   └── continuous-learning/    # 持续学习技能
│       ├── skill.json          # 技能配置
│       ├── CLAUDE.md           # 技能说明
│       └── scripts/
│           └── summary_skills.py  # 总结脚本
├── docs/
│   ├── continuous-learning.md  # 功能文档
│   └── continuous-learning-usage.md  # 使用说明
└── README.md                   # 本文件
```

## 故障排除

### 问题 1: 没有生成 skill

**症状**: 对话结束后没有生成新的 skill

**解决方案**:
1. 检查对话数量是否达到阈值(默认 10 条)
2. 确认会话记录功能是否正常工作
3. 查看 Claude Code 日志是否有错误信息
4. 运行总结脚本进行调试

### 问题 2: 生成的 skill 质量不好

**症状**: skill 内容不准确或不完整

**解决方案**:
1. 检查对话记录是否完整
2. 调整总结 prompt 模板
3. 增加对话数量阈值
4. 人工编辑生成的 skill

### 问题 3: API 调用失败

**症状**: 总结过程中出现 API 错误

**解决方案**:
1. 检查 API 密钥是否正确
2. 确认网络连接正常
3. 检查 API 配额是否用完
4. 查看错误日志了解详情

## 最佳实践

1. **先记录再学习**: 先使用会话记录功能积累对话,再启用持续学习
2. **定期审核**: 定期检查生成的 skills,删除低质量内容
3. **调整阈值**: 根据实际情况调整对话数量阈值
4. **人工优化**: 对生成的 skills 进行人工优化和分类
5. **版本控制**: 将生成的 skills 纳入版本控制

## 扩展建议

1. **skill 去重**: 检测并删除重复的 skills
2. **skill 合并**: 将相似的知识点合并
3. **分类管理**: 按主题对 skills 进行分类
4. **质量评分**: 为生成的 skills 打分
5. **自动应用**: 自动应用高质量的 skills

## 相关文档

- [持续学习功能文档](docs/continuous-learning.md)
- [使用说明](docs/continuous-learning-usage.md)
- [Claude Code Hooks 文档](https://docs.anthropic.com/claude-code/hooks)

## 更新日志

- v1.0.0 (2025-02-09): 初始版本
