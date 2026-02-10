# CC-Scaffold 配置文件说明

## 配置文件位置

CC-Scaffold 的配置文件存储在以下位置（根据操作系统不同）：

- **Windows**: `%APPDATA%\ccscaffold\config.json`
- **macOS**: `~/Library/Application Support/ccscaffold/config.json`
- **Linux**: `~/.config/ccscaffold/config.json`

## 配置文件结构

```json
{
  "python": {
    "command": null,           // Python 命令（如 'python3', 'python39'）
    "auto_detect": true,       // 是否自动检测
    "min_version": "3.9",      // 最低版本要求
    "candidates": []           // 自定义候选列表（可选）
  },
  "platform": {
    "name": null,              // 平台名称（自动检测）
    "auto_detect": true        // 是否自动检测
  },
  "paths": {
    "config_dir": null,        // 配置目录（自动设置）
    "temp_dir": ".claude/tmp"  // 临时目录（可自定义）
  }
}
```

## 配置项说明

### python 配置组

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `command` | string/null | null | Python 命令。如果设置为 null，系统会自动检测可用的 Python 命令 |
| `auto_detect` | boolean | true | 是否自动检测 Python 命令。如果设置为 false，将使用 `command` 指定的命令 |
| `min_version` | string | "3.9" | 最低 Python 版本要求 |
| `candidates` | array | [] | 自定义 Python 命令候选列表。如果为空，系统使用默认候选列表 |

**平台特定的默认候选列表**:

- **Windows**: `['python', 'python39', 'py', 'python3']`
- **macOS/Linux**: `['python3', 'python3.9', 'python39', 'python']`

### platform 配置组

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `name` | string/null | null | 平台名称（'windows', 'macos', 'linux'）。通常不需要手动设置 |
| `auto_detect` | boolean | true | 是否自动检测平台 |

### paths 配置组

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `config_dir` | string/null | null | 配置目录路径（自动设置） |
| `temp_dir` | string | ".claude/tmp" | 临时文件目录，相对于项目根目录 |

## 使用方法

### 方法 1: 交互式配置（推荐）

当你运行 CC-Scaffold 的安装或部署脚本时，系统会自动提示你选择 Python 版本：

```bash
# 运行部署脚本
python scripts/deploy_functions.py /path/to/target/project

# 系统会显示：
# 检测可用的 Python 版本...
# 可用的 Python 版本:
#   1. python3 (3.11.0)
#   2. python39 (3.9.7)
#   3. 自定义
#
# 请选择 [1-3]，或留空使用第一个:
```

选择后，配置会自动保存到配置文件。

### 方法 2: 手动编辑配置文件

1. 找到配置文件位置（根据你的操作系统）
2. 使用文本编辑器打开 `config.json`
3. 修改配置项
4. 保存文件

**示例**:

```json
{
  "python": {
    "command": "python3.11",
    "auto_detect": false,
    "min_version": "3.9",
    "candidates": []
  }
}
```

### 方法 3: 使用环境变量（临时）

你也可以通过环境变量临时指定 Python 命令：

```bash
# Windows
set CCS_PYTHON_COMMAND=python3.11
python scripts/deploy_functions.py /path/to/target/project

# Linux/macOS
CCS_PYTHON_COMMAND=python3.11 python scripts/deploy_functions.py /path/to/target/project
```

## 配置优先级

系统按以下优先级查找 Python 命令：

1. 环境变量 `CCS_PYTHON_COMMAND`（最高优先级）
2. 配置文件中的 `python.command`（如果 `auto_detect` 为 false）
3. 自动检测（按候选列表顺序）
4. 平台默认值（最低优先级）

## 常见配置场景

### 场景 1: Windows 上使用 python39

```json
{
  "python": {
    "command": "python39",
    "auto_detect": false
  }
}
```

### 场景 2: Linux/macOS 上使用系统默认的 python3

```json
{
  "python": {
    "command": "python3",
    "auto_detect": false
  }
}
```

### 场景 3: 使用虚拟环境中的 Python

```json
{
  "python": {
    "command": "/path/to/venv/bin/python",
    "auto_detect": false
  }
}
```

### 场景 4: 自定义候选列表

```json
{
  "python": {
    "command": null,
    "auto_detect": true,
    "candidates": [
      "python3.11",
      "python3.10",
      "python3.9",
      "python3"
    ]
  }
}
```

## 故障排除

### 问题 1: 未检测到 Python 命令

**原因**: 系统中没有配置的 Python 命令

**解决方案**:
1. 检查 Python 是否已安装：`python3 --version` 或 `python --version`
2. 手动指定 Python 命令（参考上面的配置场景）
3. 安装 Python 3.9 或更高版本

### 问题 2: 检测到的 Python 版本过低

**原因**: 系统中的 Python 版本低于 3.9

**解决方案**:
1. 安装 Python 3.9 或更高版本
2. 或者降低 `min_version` 要求（不推荐）

### 问题 3: 配置文件不生效

**原因**:
- 配置文件位置错误
- 配置文件格式错误（JSON 语法错误）
- `auto_detect` 设置为 true 但 `command` 为 null

**解决方案**:
1. 确认配置文件位置正确
2. 使用 JSON 验证工具检查格式
3. 如果要使用指定命令，设置 `auto_detect` 为 false

## 高级用法

### 程序化访问配置

你可以在 Python 脚本中访问和修改配置：

```python
from ccscaffold.utils import get_config

# 获取配置实例
config = get_config()

# 获取 Python 命令
python_cmd = config.get_python_command()

# 设置 Python 命令
config.set_python_command('python3.11')

# 获取配置值
min_version = config.get('python', 'min_version')

# 设置配置值
config.set('python', 'min_version', value='3.10')
```

### 重置配置

如果配置出现问题，可以删除配置文件，系统会重新创建默认配置：

```bash
# Windows
del %APPDATA%\ccscaffold\config.json

# macOS
rm ~/Library/Application Support/ccscaffold/config.json

# Linux
rm ~/.config/ccscaffold/config.json
```

## 相关文档

- [跨平台兼容性说明](./cross-platform.md)
- [Python 版本管理](./python-version-management.md)
- [项目配置最佳实践](./best-practices.md)
