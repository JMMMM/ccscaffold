# CC-Scaffold - Claude Code 经验管理工具

一个帮助你管理和迁移 Claude Code 经验的工具包,采用功能模块化组织结构。

## 项目结构

```
ccscaffold/
├── chat-record/           # 会话记录功能
├── continous-learning/   # 持续学习功能
├── package-skills/        # 组件打包功能
├── modify-logs/           # 文件修改记录功能(开发中)
├── .claude/              # Claude Code 配置目录
├── .claude-hooks/        # Hooks 脚本存放位置
├── .specify/             # SpecKit 配置模板
└── README.md             # 项目说明文档
```

## 功能介绍

### 1. 会话记录 (chat-record)

自动记录每轮对话的上下文,方便后续回顾和持续学习。

**功能特点:**
- PreToolUse 钩子:记录用户请求(格式: `user> 请求内容`)
- PostToolUse 钩子:记录 Claude 响应(格式: `Claude> 响应内容`)
- 自动保存到 `.claude/conversations/` 目录
- 按会话自动归档

**使用文档:** [chat-record/README.md](chat-record/README.md)

### 2. 持续学习 (continous-learning)

自动总结对话内容并生成 skills。

**功能特点:**
- SessionEnd 钩子触发
- 自动分析最近 10 条以上对话
- 使用 Claude 总结并生成 skill
- 自动保存到 skills 目录

**使用文档:** [continous-learning/README.md](continous-learning/README.md)

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

**使用文档:** [package-skills/README.md](package-skills/README.md)

### 4. 文件修改记录 (modify-logs)

自动记录项目中文件的修改历史,包括修改时间、修改内容、修改原因等信息。

**状态:** 开发中 ⚠️

**使用文档:** [modify-logs/README.md](modify-logs/README.md)

## 快速开始

### 1. 选择功能

根据需求选择要使用的功能模块:

- **新用户**: 推荐 先使用 `chat-record` 记录对话,再启用 `continous-learning` 持续学习
- **开发者**: 使用 `package-skills` 打包和分发自己的组件
- **高级用户**: 等待 `modify-logs` 功能开发完成

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

## 文档索引

- [项目说明文档](README.md)
- [会话记录功能](chat-record/README.md)
- [持续学习功能](continous-learning/README.md)
- [组件打包功能](package-skills/README.md)
- [文件修改记录功能](modify-logs/README.md)
- [项目宪章](.specify/memory/constitution.md)

## 注意事项

1. **备份重要**: 安装功能前建议备份项目
2. **权限检查**: 确保对相关目录有读写权限
3. **版本兼容**: 确保 Claude Code 版本兼容
4. **配置正确**: 仔细检查 `.claude/settings.json` 配置
5. **宪章遵守**: 遵循项目宪章的所有规范

## 许可证

MIT License
