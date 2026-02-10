# Console.log Cleaner Hook - 功能说明

## 功能概述

Console.log Cleaner 是一个在会话结束时自动触发的钩子，用于扫描和清理前端代码中的 `console.log` 等调试语句。

## 文件结构

```
.claude/scripts/hooks/console-cleaner/
├── clean_console_log.py    # 钩子主脚本
├── config.json              # 配置文件
└── README.md                # 使用说明
```

## 主要功能

### 1. 自动扫描

- 扫描项目中的所有前端文件（.js, .jsx, .ts, .tsx, .vue, .svelte）
- 自动排除常见的构建目录和依赖目录（node_modules, dist, build 等）
- 检测多种 console 方法（log, debug, info, warn, error, trace）

### 2. 生成报告

每次会话结束时自动生成报告，包含：

- 总体统计（发现多少处 console.log）
- 按类型统计（console.log, console.error 等）
- 详细列表（按文件分组，显示具体位置和代码）

报告保存在：`.claude/tmp/console_clean_report.md`

### 3. 智能清理（可选）

支持三种工作模式：

**仅报告模式**（默认）：
- 只生成报告，不修改文件
- 适合代码审查和持续监控

**预览模式**：
- 显示将要进行的修改
- 不实际执行修改
- 适合测试和验证

**自动清理模式**：
- 自动清理 console.log
- 原文件备份为 `.backup` 后缀
- ⚠️ 谨慎使用

## 配置选项

配置文件：`.claude/scripts/hooks/console-cleaner/config.json`

```json
{
  "enabled": true,                      // 是否启用钩子
  "auto_clean": false,                  // 是否自动清理（false 仅生成报告）
  "dry_run": true,                      // 预览模式（true 不实际修改文件）
  "exclude_patterns": [],               // 额外的排除模式（正则表达式）
  "report_file": ".claude/tmp/console_clean_report.md"  // 报告文件路径
}
```

## 使用方法

### 自动触发（推荐）

1. 部署钩子到项目：
```bash
python scripts/deploy_functions.py /path/to/target/project
```

2. 配置 `.claude/scripts/hooks/console-cleaner/config.json`

3. 正常使用 Claude Code，每次会话结束时自动触发

### 手动运行

```bash
# Linux/macOS
python3 .claude/scripts/hooks/console-cleaner/clean_console_log.py

# Windows
python .claude/scripts/hooks/console-cleaner/clean_console_log.py
```

## 清理策略

### 整行清理

如果一行代码完全是 console 语句，会整行删除：

```javascript
// 删除前
console.log('Debug info');

// 删除后
（空行）
```

### 注释策略

如果 console.log 和其他代码在同一行，会注释掉整行：

```javascript
// 处理前
const x = 1; console.log('Debug'); const y = 2;

// 处理后
const x = 1; // console.log('Debug'); const y = 2;
```

## 最佳实践

### 1. 开发阶段

使用仅报告模式，定期查看报告：

```json
{
  "enabled": true,
  "auto_clean": false
}
```

### 2. 代码审查

在提交前手动运行，查看是否有遗漏的 console.log。

### 3. 生产准备

使用预览模式验证，确认无误后再自动清理：

```json
{
  "enabled": true,
  "auto_clean": true,
  "dry_run": true
}
```

### 4. 持续集成

在 CI/CD 流程中运行，确保没有 console.log 进入生产。

## 报告示例

```markdown
# Console.log 清理报告
生成时间: 2026-02-10 15:30:45

总计发现 15 处 console 使用，分布在 3 个文件中

## 按类型统计
- console.log: 12 处
- console.error: 2 处
- console.warn: 1 处

## 详细列表

### src/utils/helpers.js
共 8 处

- 行 25: `console.log`
  ```console.log('Debug info', data)```
- 行 42: `console.error`
  ```console.error('Error occurred', err)```
```

## 注意事项

1. ⚠️ 自动清理会修改代码，建议先在预览模式测试
2. ⚠️ 备份文件会占用磁盘空间，定期清理 `.backup` 文件
3. ⚠️ 某些 console.error 可能是必要的错误处理，清理前请检查
4. ⚠️ 建议在版本控制下使用，以便随时回滚

## 故障排除

### 问题: 钩子没有执行

**解决方案**:
1. 检查 `.claude/settings.json` 配置是否正确
2. 确认 Python 命令路径正确
3. 查看 `.claude/tmp/` 目录下的日志文件
4. 手动运行脚本测试

### 问题: 某些文件没有被扫描

**解决方案**:
1. 检查文件扩展名是否在支持列表中
2. 确认文件不在自动排除的目录中
3. 检查文件权限

### 问题: 不想清理某些 console.log

**解决方案**:
1. 使用预览模式查看报告
2. 手动删除需要保留的 console.log
3. 或者配置 `exclude_patterns` 排除特定文件

## 高级用法

### 自定义排除模式

```json
{
  "exclude_patterns": [
    ".*\\.test\\.js",
    ".*\\.spec\\.ts",
    "src/debug/.*"
  ]
}
```

这会排除所有测试文件和 `src/debug/` 目录。

### 与其他钩子配合

可以将 console-cleaner 与其他钩子配合使用：

```json
{
  "hooks": {
    "Stop": [
      {
        "type": "command",
        "command": "python3 .claude/scripts/hooks/console-cleaner/clean_console_log.py",
        "timeout": 30
      }
    ]
  }
}
```

## 相关文档

- [Console.log Cleaner 详细说明](.claude/scripts/hooks/console-cleaner/README.md)
- [钩子系统说明](docs/hooks-system.md)
- [配置文件说明](docs/configuration.md)

## 更新日志

- v1.0.0 (2026-02-10): 初始版本
  - 支持 6 种前端文件类型
  - 检测 6 种 console 方法
  - 三种工作模式（报告、预览、自动清理）
  - 智能清理策略
  - 备份机制
