# CC-Scaffold - Claude Code 经验管理工具

一个帮助你管理和迁移 Claude Code 经验的工具包,采用功能模块化组织结构,方便按需使用和分发。

## 项目结构

```
ccscaffold/
├── chat-record/           # 会话记录功能
│   ├── skills/           # 相关技能
│   ├── hooks/            # Hooks 源码（开发维护）
│   ├── commands/         # 相关命令
│   ├── docs/             # 文档
│   └── README.md         # 功能说明
├── continous-learning/   # 持续学习功能
│   ├── skills/
│   ├── hooks/
│   ├── commands/
│   ├── agents/
│   ├── docs/
│   └── README.md
├── package-skills/        # 组件打包功能
│   ├── skills/
│   ├── hooks/
│   ├── commands/
│   ├── agents/
│   ├── docs/
│   └── README.md
├── speckitAgent/          # SpecKit Agent 功能
│   ├── skills/
│   ├── hooks/
│   ├── commands/
│   ├── agents/
│   ├── docs/
│   └── README.md
├── scripts/               # 安装和工具脚本
│   ├── install_components.py  # 组件安装脚本
│   └── README.md              # 安装说明
├── .claude/              # Claude Code 配置目录
│   ├── skills/           # 已安装的技能
│   ├── scripts/          # Hooks 脚本（推荐位置）
│   │   └── hooks/
│   ├── commands/         # 已安装的命令
│   ├── agents/           # 已安装的代理
│   └── settings.json     # 配置文件
├── .specify/             # SpecKit 配置模板
├── CLAUDE.md             # 项目指令文档
├── package.json          # 项目配置
└── .gitignore           # Git 忽略规则
```

## 功能介绍

### 1. 会话记录 (chat-record)

自动记录每轮对话的上下文,方便后续回顾和持续学习。

**功能特点:**
- 单一文件:仅维护一份 `conversation.txt` 文件
- 自动记录:通过 Hooks 自动捕获所有对话
- 会话总结:SessionEnd 时自动生成会话总结
- 文件修改记录:自动记录文件修改历史
- 手动加载:通过 `/loadLastSession` 命令加载上一次会话

**使用方法:**
```bash
# 复制功能目录到目标项目
cp -r chat-record /path/to/target/project/
# 按照功能内的 README.md 进行配置
```

**详细文档:** [chat-record/README.md](chat-record/README.md)

### 2. 持续学习 (continous-learning)

自动总结对话内容并生成 skills。

**功能特点:**
- SessionEnd 钩子触发
- 自动分析最近 10 条以上对话
- 使用 Claude 总结并生成 skill
- 自动保存到 skills 目录

**使用方法:**
```bash
# 复制功能目录到目标项目
cp -r continous-learning /path/to/target/project/
# 按照功能内的 README.md 进行配置
```

**详细文档:** [continous-learning/README.md](continous-learning/README.md)

### 3. 组件打包 (package-skills)

通用的组件打包工具,支持打包 skills/hooks/agents/commands 四种组件类型。

**功能特点:**
- 支持多种组件类型(skills/hooks/agents/commands)
- 自动发现所有可用组件
- 交互式多选界面
- 生成自包含的安装包
- 跨平台支持

**使用方法:**
```bash
# 打包 skills
python package-skills/skills/skill-packager/scripts/pack_skills.py -t skills

# 打包所有组件
python package-skills/skills/skill-packager/scripts/pack_skills.py -t all
```

**详细文档:** [package-skills/README.md](package-skills/README.md)

### 4. SpecKit Agent (speckitAgent)

执行 spec-kit 方法论进行系统化功能开发的智能代理。

**功能特点:**
- 自动化工作流：按照预定义顺序执行 spec-kit 命令
- 进度跟踪：自动检测已完成的工作，从中断处继续
- 智能引导：在每个步骤提供清晰的说明和状态更新
- 灵活暂停：在需要用户输入时自动暂停等待
- 中文支持：所有交互使用中文进行

**使用方法:**
```bash
# 复制 agent 到项目
cp speckitAgent/agents/speckitAgent.md .claude/agents/

# 重启 Claude Code 后即可使用
```

**详细文档:** [speckitAgent/README.md](speckitAgent/README.md)

## 快速开始

### 1. 选择功能

根据需求选择要使用的功能模块:

- **新用户**: 推荐 先使用 `chat-record` 记录对话,再启用 `continous-learning` 持续学习
- **开发者**: 使用 `package-skills` 打包和分发自己的组件
- **项目经理**: 使用 `speckitAgent` 进行系统化功能开发

### 2. 安装功能

将需要的功能目录复制到目标项目:

```bash
# 方式 1: 直接复制目录
cp -r chat-record /path/to/target/project/

# 方式 2: 复制特定组件
cp -r chat-record/skills/* /path/to/target/project/.claude/skills/
cp -r chat-record/hooks/* /path/to/target/project/.claude-hooks/
```

### 3. 配置功能

按照每个功能目录下的 README.md 进行配置:

```bash
# 查看功能说明
cat chat-record/README.md
```

### 4. 开始使用

配置完成后,重启 Claude Code 即可开始使用。

## 开发指南

### 添加新功能

1. 创建新的功能目录:
   ```bash
   mkdir -p new-feature/{skills,hooks,commands,agents,docs}
   ```

2. 按照标准结构组织文件:
   - skills/: 技能配置和脚本
   - hooks/: 钩子脚本和配置
   - commands/: 命令脚本
   - agents/: 代理配置
   - docs/: 相关文档

3. 创建 README.md:
   ```bash
   # 参考现有功能的 README.md 格式
   cp chat-record/README.md new-feature/README.md
   # 编辑内容
   ```

4. 遵循项目宪章:
   - 临时文件使用 `.claude/tmp/` 目录
   - 文档使用中文编写
   - 脚本文件使用英文命名
   - Python 代码兼容 3.9+
   - 包含完整的 README.md

### 目录结构规范

每个功能组件应遵循以下目录结构:

```
feature-name/
├── skills/              # 相关技能
│   └── skill-name/
│       ├── skill.json   # 技能配置
│       ├── SKILL.md     # 技能说明
│       └── scripts/     # 脚本文件
├── hooks/               # 相关钩子
│   ├── hook_name.py     # 钩子脚本
│   └── settings.json    # 钩子配置
├── commands/            # 相关命令
│   └── command_name.md  # 命令定义
├── agents/              # 相关代理
│   └── agent_name.md    # 代理定义
├── docs/                # 相关文档
│   ├── feature.md       # 功能文档
│   └── usage.md         # 使用说明
└── README.md            # ⚠️ 必需: 功能说明文档
```

### 组件打包

使用 `package-skills` 功能打包组件:

```bash
# 打包特定功能
python package-skills/skills/skill-packager/scripts/pack_skills.py -t skills

# 选择要打包的组件
# 生成的包保存到 packages/ 目录
```

## 配置说明

### Python 版本要求

所有脚本需要 Python 3.9 或更高版本:

```bash
# 使用指定的 Python 版本
python39 script.py
# 或
python3.9 script.py
```

### 临时文件路径

所有临时文件必须使用 `.claude/tmp/` 目录结构:

- 对话记录: `.claude/tmp/conversations/`
- 缓存数据: `.claude/tmp/cache/`
- 临时脚本: `.claude/tmp/scripts/`

### 代码规范

- **字符编码**: 仅使用 ASCII 字符,禁止特殊 Unicode 字符
- **文档语言**: 所有文档使用中文编写
- **文件命名**: 脚本文件使用英文命名
- **README 要求**: 每个功能必须包含 README.md

### 隐私保护 (Principle X)

根据 CC-Scaffold 宪章 Principle X，项目包含隐私保护机制：

- **Git 提交检查**: 自动检测并阻止包含敏感信息的提交
- **数据脱敏工具**: 提供日志和路径脱敏功能
- **环境变量**: 敏感配置必须使用环境变量
- **定期审计**: 定期审查代码库和提交历史

**安装 Git 钩子:**
```bash
# Bash 脚本安装
bash scripts/git/install_git_hooks.sh

# 或使用 Python 脚本安装
python39 scripts/git/install_git_hooks.py
```

**使用隐私工具:**
```python
from ccscaffold.utils.privacy_utils import PrivacySanitizer, safe_print_path

# 脱敏字符串
sanitized = PrivacySanitizer.sanitize_string("user@example.com")

# 脱敏日志
safe_log = PrivacySanitizer.sanitize_log_message(log_message)

# 安全打印路径
safe_print_path(file_path, "文件路径")
```

**详细文档:** [scripts/git/README.md](scripts/git/README.md)

## 注意事项

1. **备份重要**: 安装功能前建议备份项目
2. **权限检查**: 确保对相关目录有读写权限
3. **版本兼容**: 确保 Claude Code 版本兼容
4. **配置正确**: 仔细检查 `.claude/settings.json` 配置
5. **宪章遵守**: 遵循项目宪章的所有规范

## 故障排除

### 问题 1: Hooks 没有执行

**解决方案:**
- 检查 `.claude/settings.json` 配置
- 确认脚本路径正确
- 查看 Claude Code 日志
- 确认脚本有执行权限

### 问题 2: Skills 没有生效

**解决方案:**
- 重启 Claude Code
- 检查 skill.json 格式
- 查看 Claude Code 日志
- 确认技能目录正确

### 问题 3: 文件路径错误

**解决方案:**
- 使用绝对路径
- 检查路径分隔符(Windows 使用 `\\`)
- 确认目录存在
- 检查文件权限

## 许可证

MIT License

## 贡献

欢迎贡献!请遵循以下步骤:

1. Fork 项目
2. 创建功能分支
3. 遵循项目宪章
4. 提交 Pull Request

## 参考资源

- [Claude Code 文档](https://docs.anthropic.com/claude-code)
- [Hooks API](https://docs.anthropic.com/claude-code/hooks)
- [项目宪章](.specify/memory/constitution.md)
- [会话记录功能](chat-record/README.md)
- [持续学习功能](continous-learning/README.md)
- [组件打包功能](package-skills/README.md)
- [SpecKit Agent 功能](speckitAgent/README.md)
- [SpecKit Agent 使用指南](speckitAgent/docs/speckit-agent.md)
- [Git 隐私检查工具](scripts/git/README.md)

---

**版本**: 2.2.0 | **宪章版本**: 1.4.0 | **最后更新**: 2026-02-09
