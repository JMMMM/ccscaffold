---
description: 在目标目录中部署 CC-Scaffold 的所有功能（会话记录、会话总结、加载上一次会话、SpecKit Agent等）。
---

# 部署 CC-Scaffold 功能到目标目录

请执行以下步骤将 CC-Scaffold 的所有功能部署到目标目录：

1. **确认目标目录**
   检查目标目录路径是否正确

2. **执行部署脚本**
   运行以下命令：
   ```bash
   python39 /path/to/ccscaffold/scripts/deploy_functions.py <目标目录>
   ```

3. **验证部署**
   检查目标目录下是否已创建以下组件：
   - `.claude/skills/chat-recorder/` - 会话记录功能
   - `.claude/scripts/hooks/chat-record/` - 会话结束钩子
   - `.claude/commands/loadLastSession.md` - 加载上一次会话命令
   - `.claude/agents/speckitAgent.md` - SpecKit Agent
   - `.claude/settings.json` - 配置文件（已更新）

4. **重启 Claude Code**
   重启目标项目的 Claude Code 以使更改生效

## 注意事项

- 如果目标目录已有 `.claude/settings.json`，脚本会尝试合并配置
- 部署会覆盖同名文件，建议在部署前备份重要数据
- 确保目标目录有写权限
- 需要使用 Python 3.9 或更高版本

## 示例

```bash
# 部署到当前目录
python39 /path/to/ccscaffold/scripts/deploy_functions.py .

# 部署到指定目录
python39 /path/to/ccscaffold/scripts/deploy_functions.py /path/to/target/project
```

部署完成后，目标目录将拥有 CC-Scaffold 的完整功能。
