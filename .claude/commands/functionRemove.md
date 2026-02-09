---
description: 从目标目录中移除 CC-Scaffold 的所有功能，包括删除相关文件和清理配置。
---

# 从目标目录移除 CC-Scaffold 功能

请执行以下步骤从目标目录移除 CC-Scaffold 的所有功能：

1. **确认目标目录**
   检查目标目录路径是否正确

2. **执行移除脚本**
   运行以下命令：
   ```bash
   python39 /path/to/ccscaffold/scripts/remove_functions.py <目标目录>
   ```

3. **验证移除**
   脚本会移除以下组件：
   - `.claude/skills/chat-recorder/` - 会话记录功能
   - `.claude/scripts/hooks/chat-record/` - 会话结束钩子
   - `.claude/commands/loadLastSession.md` - 加载上一次会话命令
   - `.claude/agents/speckitAgent.md` - SpecKit Agent
   - `.claude/settings.json` 中的相关配置

4. **重启 Claude Code**
   重启目标项目的 Claude Code 以使更改生效

## 注意事项

- 移除操作不可逆，建议在移除前备份重要数据
- 如果 `.claude/settings.json` 中还有其他 hooks，会保留它们
- 空的父目录会被自动清理
- 确保目标目录有写权限

## 示例

```bash
# 从当前目录移除
python39 /path/to/ccscaffold/scripts/remove_functions.py .

# 从指定目录移除
python39 /path/to/ccscaffold/scripts/remove_functions.py /path/to/target/project
```

移除完成后，目标目录将不再包含 CC-Scaffold 的任何功能。
