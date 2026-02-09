# 组件打包工具 (Component Packager)

## 概述

组件打包工具是一个通用的打包工具，支持两种打包模式：
1. **按组件类型打包**：选择并打包 skills/hooks/agents/commands 等组件
2. **按功能打包**（推荐）：根据功能自动打包相关的所有组件

## 功能特性

- **双打包模式**：
  - 按组件类型：skills、hooks、agents、commands
  - 按功能：自动收集功能相关的所有组件
- **Python版本配置**：打包时可指定目标项目的Python命令
- **自动发现**：自动扫描项目中的所有组件
- **可视化选择**：交互式界面选择要打包的内容
- **批量打包**：支持同时打包多个不同类型的组件
- **自包含安装**：生成的包包含完整的安装脚本
- **跨平台**：支持 Windows、macOS、Linux

## 目录结构

```
skills/skill-packager/
├── skill.json           # Skill 配置文件
├── SKILL.md            # Skill 触发说明
└── scripts/
    └── pack_skills.py   # 打包脚本

scripts/
└── functions.json      # 功能配置文件
```

## 使用方法

### 命令行使用

#### 基本语法

```bash
# 按组件类型打包
python skills/skill-packager/scripts/pack_skills.py -t <类型> [选项]

# 按功能打包（推荐）
python skills/skill-packager/scripts/pack_skills.py -f [选项]
python skills/skill-packager/scripts/pack_skills.py --function [选项]
```

#### 类型选项

**按组件类型：**
- `skills` - 打包 skills 组件（默认）
- `hooks` - 打包 hooks 组件
- `agents` - 打包 agents 组件
- `commands` - 打包 commands 组件
- `all` - 打包所有类型的组件

**按功能打包：**
- `-f` / `--function` - 按功能打包（会列出所有可用功能供选择）

#### 示例

**按组件类型打包：**
```bash
# 打包 skills（默认）
python skills/skill-packager/scripts/pack_skills.py

# 打包 skills
python skills/skill-packager/scripts/pack_skills.py -t skills

# 打包 hooks
python skills/skill-packager/scripts/pack_skills.py -t hooks

# 打包 agents
python skills/skill-packager/scripts/pack_skills.py -t agents

# 打包 commands
python skills/skill-packager/scripts/pack_skills.py -t commands

# 打包所有组件
python skills/skill-packager/scripts/pack_skills.py -t all

# 指定输出包名
python skills/skill-packager/scripts/pack_skills.py -t skills -o my-package

# 非交互模式（需要指定 -o）
python skills/skill-packager/scripts/pack_skills.py -t skills --non-interactive -o my-skills
```

**按功能打包（推荐）：**
```bash
# 按功能打包
python skills/skill-packager/scripts/pack_skills.py -f

# 或使用 --function
python skills/skill-packager/scripts/pack_skills.py --function

# 指定输出包名
python skills/skill-packager/scripts/pack_skills.py -f -o my-function-package
```

#### 可用功能列表

当前支持的功能（定义在 `scripts/functions.json`）：

1. **chat-recorder** - 会话记录
   - 自动记录每轮对话的上下文
   - 组件：skills/chat-recorder

2. **continuous-learning** - 持续学习
   - 自动分析对话内容，检测反复修改失败的情况并生成修复 skill
   - 组件：skills/continuous-learning, commands/summary-skills

3. **modify-logs** - 修改文件笔记
   - 记录文件修改操作，在会话开始时读取历史修改记录
   - 组件：.claude-hooks/*.py

4. **skill-packager** - 组件打包
   - 打包工具本身
   - 组件：skills/skill-packager, scripts/pack_skills.py

### 自然语言触发

当与 Claude Code 对话时，可以使用自然语言触发此工具：

**按组件类型打包：**
- "帮我打包 skills"
- "打包所有 hooks"
- "导出 agents"
- "迁移 commands 到其他项目"
- "打包所有组件"

**按功能打包（推荐）：**
- "打包会话记录功能"
- "打包持续学习功能"
- "按功能打包 modify-logs"
- "打包所有功能"

## 使用流程

### 按功能打包（推荐）

1. **运行打包脚本**:
   ```bash
   python skills/skill-packager/scripts/pack_skills.py -f
   ```

2. **查看可用功能**:
   ```
   ================================================================================
                                   可用功能列表
   ================================================================================

   [1] chat-recorder
       名称: 会话记录
       描述: 自动记录每轮对话的上下文，包括用户请求和AI响应
       组件: skills: chat-recorder

   [2] continuous-learning
       名称: 持续学习
       描述: 自动分析对话内容，检测反复修改失败的情况并生成修复 skill
       组件: skills: continuous-learning, commands: summary-skills

   [3] modify-logs
       名称: 修改文件笔记
       描述: 记录文件修改操作，在会话开始时读取历史修改记录
       组件: hooks: post_tool_use_logger.py, session_start_reader.py

   [4] skill-packager
       名称: 组件打包
       描述: 打包工具本身，用于打包和迁移组件
       组件: skills: skill-packager
   ```

3. **选择功能**:
   ```
   请输入要打包的功能编号
   输入 'q' 退出

   选择> 1
   ```

4. **确认组件**:
   ```
   功能 '会话记录' 包含以下组件:
     [skills] chat-recorder: 自动记录每轮对话的上下文，包括用户请求和AI响应

   确认打包? (y/n): y
   ```

5. **配置Python版本**:
   ```
   ================================================================================
                                  Python 版本配置
   ================================================================================

   请输入目标项目的 Python 命令
   常用选项: python39, python3.9, python3.14, python3
   例如: 如果目标项目使用 python39 运行脚本，请输入 'python39'

   Python命令 [默认: python39]: python39
   ```

6. **获取安装命令**:
   ```
   ================================================================================
                                  打包完成!
   ================================================================================

   功能: 会话记录 (chat-recorder)
   Python命令: python39

   安装命令:
     python39 dist/ccscaffold-function-chat-recorder/install.py

   或复制到其他项目后运行:
     python39 <package>/install.py
   ```

### 按组件类型打包

1. **运行打包脚本**:
   ```bash
   python skills/skill-packager/scripts/pack_skills.py -t skills
   ```

2. **查看可用组件**:
   ```
   ================================================================================
                                   可用的组件
   ================================================================================

   【SKILLS】
   --------------------------------------------------------------------------------

   [1] continuous-learning
       描述: 自动总结对话内容并生成 skills
       版本: 1.0.0
       路径: F:\ccscaffold\skills\continuous-learning

   [2] skill-packager
       描述: 打包skills组件工具 - 可视化选择并打包多个skills组件
       版本: 1.0.0
       路径: F:\ccscaffold\skills\skill-packager
   ```

3. **选择组件**:
   ```
   请输入要打包的组件编号（多个用空格或逗号分隔）
   例如: 1 3 5  或  1,3,5  或  all (选择全部)
   输入 'q' 退出

   选择> 1 2
   ```

4. **确认打包**:
   ```
   已选择 2 个组件:
     [skills] continuous-learning: 自动总结对话内容并生成 skills
     [skills] skill-packager: 打包skills组件工具 - 可视化选择并打包多个skills组件

   确认打包? (y/n): y
   ```

5. **获取安装命令**:
   ```
   ================================================================================
                                  打包完成!
   ================================================================================

   安装命令:
     python dist/ccscaffold-skills-continuous-learning-skill-packager/install.py
   ```

## 打包所有组件

当使用 `-t all` 选项时，工具会扫描所有类型的组件并按类别分组显示：

```bash
python skills/skill-packager/scripts/pack_skills.py -t all
```

输出示例：
```
================================================================================
                              可用的组件
================================================================================

【SKILLS】
--------------------------------------------------------------------------------
[1] continuous-learning
[2] skill-packager

【HOOKS】
--------------------------------------------------------------------------------
[3] pre-commit-hook
[4] post-commit-hook

【AGENTS】
--------------------------------------------------------------------------------
[5] code-reviewer

【COMMANDS】
--------------------------------------------------------------------------------
[6] deploy-command
```

## 安装到其他项目

### 方法一：直接安装

1. **复制包到目标项目**:
   ```bash
   cp -r dist/ccscaffold-xxx /path/to/target-project/
   ```

2. **运行安装脚本**:
   ```bash
   cd /path/to/target-project
   python ccscaffold-xxx/install.py
   ```

### 方法二：使用绝对路径

```bash
cd /path/to/target-project
python /path/to/ccscaffold/dist/ccscaffold-xxx/install.py
```

## 包结构

打包后的目录结构:

```
dist/ccscaffold-{types}-{names}/
├── manifest.json          # 包清单文件
├── install.py            # 安装脚本
├── skills/               # Skills 目录（如果包含）
│   ├── skill-name-1/
│   └── skill-name-2/
├── hooks/                # Hooks 目录（如果包含）
│   └── hook-name-1/
├── agents/               # Agents 目录（如果包含）
│   └── agent-name-1/
└── commands/             # Commands 目录（如果包含）
    └── command-name-1/
```

## manifest.json 格式

### 按组件类型打包的 manifest

```json
{
  "package": "ccscaffold-skills-continuous-learning-skill-packager",
  "version": "1.0.0",
  "python_command": "python39",
  "components": [
    {
      "type": "skills",
      "name": "continuous-learning",
      "description": "自动总结对话内容并生成 skills",
      "version": "1.0.0"
    }
  ],
  "install_command": "python39 ccscaffold-xxx/install.py"
}
```

### 按功能打包的 manifest

```json
{
  "package": "ccscaffold-function-chat-recorder",
  "version": "1.0.0",
  "python_command": "python39",
  "components": [
    {
      "type": "skills",
      "name": "chat-recorder",
      "description": "自动记录每轮对话的上下文",
      "version": "1.0.0"
    }
  ],
  "install_command": "python39 ccscaffold-function-chat-recorder/install.py"
}
```

## functions.json 格式

功能配置文件定义了每个功能包含哪些组件：

```json
{
  "$schema": "./functions-schema.json",
  "version": "1.0.0",
  "description": "CC-Scaffold 功能配置文件",
  "functions": {
    "function-key": {
      "name": "功能名称",
      "description": "功能描述",
      "components": {
        "skills": ["skill-name-1", "skill-name-2"],
        "hooks": ["hook-file-1.py", "hook-file-2.py"],
        "commands": ["command-name"]
      },
      "hooks_dir": ".claude-hooks",
      "docs": "docs/function-doc.md"
    }
  },
  "python_command": {
    "default": "python39",
    "description": "默认的 Python 命令"
  }
}
```

### 添加新功能

要添加新功能，编辑 `scripts/functions.json`：

```json
{
  "functions": {
    "my-new-function": {
      "name": "我的新功能",
      "description": "功能描述",
      "components": {
        "skills": ["my-skill"],
        "hooks": [],
        "commands": []
      },
      "docs": "docs/my-function.md"
    }
  }
}
```

## 组件配置规范

### Skills 配置 (skill.json)

```json
{
  "name": "skill-name",
  "description": "技能描述",
  "version": "1.0.0",
  "hooks": {...}
}
```

### Hooks 配置 (hook.json)

```json
{
  "name": "hook-name",
  "description": "钩子描述",
  "version": "1.0.0",
  "event": "PreToolUse",
  "command": "python hooks/hook.py"
}
```

### Agents 配置 (agent.json)

```json
{
  "name": "agent-name",
  "description": "代理描述",
  "version": "1.0.0",
  "type": "general-purpose"
}
```

### Commands 配置 (command.json)

```json
{
  "command": "command-name",
  "description": "命令描述",
  "version": "1.0.0",
  "script": "commands/command.py"
}
```

## 高级用法

### 自定义包名

```bash
python pack_skills.py -t skills -o my-custom-package
```

### 非交互模式

适用于自动化脚本，跳过选择和确认步骤：

```bash
python pack_skills.py -t skills --non-interactive -o all-skills
```

### 编程式使用

```python
from pathlib import Path
from skills.skill_packager.scripts.pack_skills import ComponentPackager

project_dir = Path("/path/to/project")
packager = ComponentPackager(project_dir, "skills")

# 发现组件
components = packager.discover_components()

# 选择要打包的组件
selected = components[:2]

# 创建包
package_dir = packager.create_package(selected, output_name="my-package")

# 获取安装命令
install_cmd = packager.get_install_command(package_dir)
print(install_cmd)
```

## 常见问题

### Q: 如何按功能打包组件?

A: 使用 `-f` 或 `--function` 选项：
```bash
python skills/skill-packager/scripts/pack_skills.py -f
```
然后从列表中选择要打包的功能。

### Q: 如何添加新功能到打包列表?

A: 编辑 `scripts/functions.json` 文件，添加新的功能配置：
```json
{
  "functions": {
    "my-function": {
      "name": "功能名称",
      "description": "功能描述",
      "components": {
        "skills": ["skill-name"],
        "hooks": [],
        "commands": []
      }
    }
  }
}
```

### Q: Python命令的作用是什么?

A: 打包时会让你指定目标项目的Python命令（如python39、python3.9等）。安装脚本会使用这个命令来运行hook脚本，确保在不同Python环境下都能正常工作。

### Q: 如何只打包特定的组件?

A: 使用按组件类型打包模式，输入要打包的组件编号，如 `1 3 5`

### Q: 打包后的文件在哪里?

A: 默认在项目的 `dist/` 目录下

### Q: 安装会覆盖现有配置吗?

A: 安装脚本会合并 `.claude/settings.json`，不会删除其他配置

### Q: 如何打包所有类型的组件?

A: 使用 `-t all` 选项

### Q: 按功能打包和按组件打包有什么区别?

A:
- **按功能打包**：自动收集一个功能相关的所有组件（skills/hooks/commands等），适合迁移完整功能
- **按组件打包**：手动选择具体的组件，适合精细控制

### Q: 如何卸载已安装的组件?

A: 删除 `.claude/<type>/<component-name>` 目录，并手动编辑 `.claude/settings.json` 移除相关配置

### Q: 支持打包到压缩文件吗?

A: 当前版本不支持，但你可以手动压缩生成的包目录

## 技术实现

### 核心功能

1. **组件发现**: 扫描对应目录，读取配置文件
2. **功能配置**: 从 functions.json 读取功能定义
3. **类型支持**: 支持 skills、hooks、agents、commands 四种类型
4. **交互选择**: 命令行界面选择多个组件或功能
5. **Python版本管理**: 打包时指定目标项目的Python命令
6. **文件复制**: 递归复制整个组件目录
7. **配置生成**: 自动生成 manifest 和安装脚本
8. **路径处理**: 使用 `pathlib` 确保跨平台兼容

### 安装脚本

安装脚本会：
1. 读取 `manifest.json`
2. 获取配置的Python命令
3. 根据组件类型复制到对应目录
4. 更新 hooks 配置中的Python命令
5. 合并 hooks 配置到 `.claude/settings.json`
6. 保留现有配置

## 依赖项

- Python 3.9+
- Claude Code (可选，用于使用打包的组件)

## 设计原则

1. **用户友好**: 清晰的交互界面
2. **类型灵活**: 支持多种组件类型
3. **零配置**: 自动发现和配置
4. **自包含**: 打包后独立可安装
5. **跨平台**: 支持 Windows/macOS/Linux
6. **可扩展**: 易于添加新的组件类型

## 与旧版本的区别

### 旧版本 (仅支持 skills)

```bash
python pack_skills.py  # 只能打包 skills
```

### 新版本 (支持所有组件类型)

```bash
python pack_skills.py -t skills    # 打包 skills
python pack_skills.py -t hooks     # 打包 hooks
python pack_skills.py -t agents    # 打包 agents
python pack_skills.py -t commands  # 打包 commands
python pack_skills.py -t all       # 打包所有
```

## 未来扩展

- [ ] 支持压缩包格式 (zip/tar.gz)
- [ ] 在线分享功能
- [ ] 版本管理和更新检查
- [ ] 依赖关系检查和自动解析
- [ ] 配置文件验证
- [ ] GUI 界面

## 参考资源

- [Claude Code 文档](https://docs.anthropic.com/claude-code)
- [CC-Scaffold 项目总结](project-summary.md)
- [迁移脚本使用](migrate-script.md)

## 许可证

MIT License

---

**创建日期:** 2025-02-09
**版本:** 3.0.0
**作者:** CC-Scaffold Team

## 版本历史

### v3.0.0 (2025-02-09)
- 新增按功能打包模式
- 新增Python版本配置
- 新增functions.json功能配置文件
- 改进安装脚本，支持Python命令替换

### v2.0.0
- 支持所有组件类型（skills/hooks/agents/commands）
- 新增批量打包功能

### v1.0.0
- 初始版本，仅支持skills打包
