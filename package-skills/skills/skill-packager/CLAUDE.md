# Skill Packager - 组件打包工具

## 功能概述

组件打包工具是 CC-Scaffold 的核心工具，用于打包和迁移 Claude Code 的各种组件（skills、hooks、agents、commands）。它支持交互式选择、自动发现组件、生成自包含的安装包。

## 核心功能

- **多类型组件支持**: 支持 skills/hooks/agents/commands 四种组件类型
- **自动发现**: 自动扫描并识别所有可用的组件
- **交互式选择**: 提供友好的多选界面
- **自包含安装包**: 生成包含所有依赖的安装包
- **跨平台支持**: 支持 Windows/Linux/macOS

## 使用方法

### 基本用法

```bash
# 打包 skills
python skills/skill-packager/scripts/pack_skills.py -t skills

# 打包 hooks
python skills/skill-packager/scripts/pack_skills.py -t hooks

# 打包所有组件
python skills/skill-packager/scripts/pack_skills.py -t all
```

### 高级选项

```bash
# 指定输出目录
python skills/skill-packager/scripts/pack_skills.py -t skills -o /path/to/output

# 查看帮助
python skills/skill-packager/scripts/pack_skills.py --help
```

## 配置说明

### skill.json 配置

```json
{
  "name": "component-packager",
  "description": "Claude Code 组件打包工具 - 支持打包 skills/hooks/agents/commands",
  "version": "2.0.0",
  "configuration": {
    "skills_dir": "skills",
    "hooks_dir": "hooks",
    "agents_dir": "agents",
    "commands_dir": "commands",
    "output_dir": "dist"
  }
}
```

### 配置参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `skills_dir` | skills 组件目录 | `skills` |
| `hooks_dir` | hooks 组件目录 | `hooks` |
| `agents_dir` | agents 组件目录 | `agents` |
| `commands_dir` | commands 组件目录 | `commands` |
| `output_dir` | 打包输出目录 | `dist` |

## 目录结构

```
skills/skill-packager/
├── skill.json              # 功能配置文件
├── SKILL.md                # 功能说明文档
├── CLAUDE.md               # 本文件
└── scripts/
    └── pack_skills.py      # 打包脚本
```

## 工作流程

1. **选择组件类型**: 选择要打包的组件类型
2. **发现组件**: 自动扫描指定目录
3. **交互选择**: 在界面上选择要打包的组件
4. **收集依赖**: 收集组件相关的所有文件
5. **生成安装包**: 创建自包含的安装包
6. **保存**: 将安装包保存到输出目录

## 输出格式

生成的安装包包含：

- 组件源文件
- 配置文件
- 文档文件
- 安装脚本（如果需要）
- 依赖说明

## 使用文档

详细使用文档请参考: [docs/skill-packager.md](../../docs/skill-packager.md)

## 使用场景

### 场景 1: 分发单个 skill

```bash
# 打包特定的 skill 分发给团队成员
python skills/skill-packager/scripts/pack_skills.py -t skills
# 在交互界面中选择要打包的 skill
```

### 场景 2: 迁移到新项目

```bash
# 打包所有组件，准备迁移到新项目
python skills/skill-packager/scripts/pack_skills.py -t all
```

### 场景 3: 备份配置

```bash
# 定期打包 hooks 和 commands 作为备份
python skills/skill-packager/scripts/pack_skills.py -t hooks
python skills/skill-packager/scripts/pack_skills.py -t commands
```

## 注意事项

1. Python 版本要求: Python 3.9+
2. 打包前确保组件文件完整
3. 生成的安装包需要测试后再分发
4. 注意保护敏感信息（如 API keys）

## 最佳实践

1. **版本管理**: 每次打包前更新版本号
2. **文档更新**: 确保文档与代码同步
3. **依赖说明**: 明确列出所有依赖项
4. **测试验证**: 打包后在测试环境中验证

## 相关功能

- **migrate_experience.py**: 使用打包的组件进行迁移
- **functions.json**: 定义功能与组件的映射关系

## 依赖关系

- 依赖于项目目录结构的规范性
- 需要正确的 skill.json 配置
