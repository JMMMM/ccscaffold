# CC-Scaffold 跨平台兼容性说明

## 概述

CC-Scaffold 已针对以下平台进行了优化和测试：

- Windows 10/11
- macOS (Intel 和 Apple Silicon)
- Linux (Ubuntu, CentOS, Debian, Fedora 等)

## 平台特性

### Windows

**特点**:
- Python 命令通常为 `python` 或 `python39`
- 使用反斜杠 `\` 作为路径分隔符
- 不支持 Unix 权限模式（chmod）
- 需要使用 `.exe` 后缀的可执行文件

**默认 Python 候选列表**:
```python
['python', 'python39', 'py', 'python3']
```

**注意事项**:
- 建议安装 Python Launcher for Windows (`py`)
- Git Bash 环境下可以使用 Unix 风格的命令
- PowerShell 环境下使用 Windows 风格的命令

### macOS

**特点**:
- Python 命令通常为 `python3`
- 系统自带 Python 2.7（已过时）
- 推荐使用 Homebrew 安装 Python 3
- 使用正斜杠 `/` 作为路径分隔符

**默认 Python 候选列表**:
```python
['python3', 'python3.9', 'python39', 'python']
```

**注意事项**:
- 不要使用系统自带的 Python 2.7
- 推荐通过 Homebrew 安装：`brew install python@3.9`
- Apple Silicon Mac 需要使用 arm64 版本的 Python

### Linux

**特点**:
- Python 命令通常为 `python3`
- 各发行版的 Python 版本可能不同
- 使用包管理器安装 Python
- 使用正斜杠 `/` 作为路径分隔符

**默认 Python 候选列表**:
```python
['python3', 'python3.9', 'python39', 'python']
```

**注意事项**:
- Ubuntu 20.04+ 默认 Python 3.8
- 建议安装 Python 3.9+: `sudo apt install python3.9`
- CentOS 8+ 使用 `dnf` 包管理器

## 路径处理

### 跨平台路径操作

CC-Scaffold 使用 `pathlib.Path` 进行路径操作，确保跨平台兼容性：

```python
from pathlib import Path

# 推荐方式
config_file = Path('.claude') / 'config.json'
settings_file = Path.home() / '.config' / 'ccscaffold' / 'config.json'

# 不推荐（硬编码路径分隔符）
config_file = '.claude\\config.json'  # Windows only
config_file = '.claude/config.json'   # Unix only
```

### 平台特定目录

| 类型 | Windows | macOS | Linux |
|------|---------|-------|-------|
| 用户主目录 | `C:\Users\Username` | `/Users/Username` | `/home/Username` |
| 配置目录 | `%APPDATA%\ccscaffold` | `~/Library/Application Support/ccscaffold` | `~/.config/ccscaffold` |
| 临时目录 | `.claude\tmp` | `.claude/tmp` | `.claude/tmp` |

## Python 版本管理

### 最低版本要求

CC-Scaffold 需要 **Python 3.9 或更高版本**。

### 版本检测

系统会自动检测可用的 Python 命令，按以下优先级：

1. 环境变量 `CCS_PYTHON_COMMAND`
2. 配置文件 `python.command`
3. 自动检测（按候选列表）
4. 平台默认值

### 安装 Python

#### Windows

1. 访问 [python.org](https://www.python.org/downloads/)
2. 下载 Python 3.9+ 安装器
3. 安装时勾选 "Add Python to PATH"

或者使用 Microsoft Store 安装 Python 3.9+。

#### macOS

使用 Homebrew：
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python@3.9
```

或使用官方安装器：[python.org](https://www.python.org/downloads/macos/)

#### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3.9 python3-pip
```

#### Linux (CentOS/Fedora)

```bash
# CentOS 8+
sudo dnf install python39

# Fedora
sudo dnf install python3.9
```

## Shell 脚本兼容性

### Bash 脚本

CC-Scaffold 提供的 Bash 脚本（如 `install_git_hooks.sh`）仅在 Unix-like 系统（macOS/Linux）上运行。

**Windows 用户**:
- 使用 Git Bash 运行 Bash 脚本
- 或使用 Python 版本的脚本（如 `install_git_hooks.py`）

### Python 脚本

所有 Python 脚本都是跨平台的，可以在任何系统上运行。

## 文件权限

### Unix-like 系统（macOS/Linux）

使用 `chmod` 设置可执行权限：

```python
from ccscaffold.utils import make_executable

make_executable(script_path)
```

### Windows

Windows 不使用 Unix 权限模式。CC-Scaffold 会自动检测平台并跳过权限设置。

## 环境变量

### 通用环境变量

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `CCS_PYTHON_COMMAND` | 指定 Python 命令 | `python3.11` |
| `CCS_CONFIG_DIR` | 指定配置目录 | `/path/to/config` |
| `CCS_TEMP_DIR` | 指定临时目录 | `/path/to/tmp` |

### 设置环境变量

#### Windows (PowerShell)

```powershell
$env:CCS_PYTHON_COMMAND = "python3.11"
python scripts/deploy_functions.py /path/to/target/project
```

#### Windows (CMD)

```cmd
set CCS_PYTHON_COMMAND=python3.11
python scripts/deploy_functions.py /path/to/target/project
```

#### macOS/Linux (Bash)

```bash
export CCS_PYTHON_COMMAND=python3.11
python scripts/deploy_functions.py /path/to/target/project
```

## 常见问题

### Q1: Windows 上出现 "命令未找到" 错误

**解决方案**:
1. 确认 Python 已安装：`python --version`
2. 将 Python 添加到 PATH 环境变量
3. 或使用 `py` 命令（Python Launcher）

### Q2: macOS 上使用的是系统自带的 Python 2.7

**解决方案**:
1. 检查 Python 版本：`python3 --version`
2. 使用 `python3` 而不是 `python`
3. 或安装新版本的 Python 3.9+

### Q3: Linux 上权限被拒绝

**解决方案**:
1. 使用 `chmod +x` 设置可执行权限
2. 或使用 `python script.py` 运行脚本
3. 检查文件所有者权限

### Q4: Git Hooks 不工作

**解决方案**:
1. Windows: 使用 Git Bash 或 Python 版本的安装脚本
2. macOS/Linux: 确认 `.git/hooks` 目录权限
3. 手动运行脚本测试：`python scripts/git/privacy_check.py`

## 测试矩阵

CC-Scaffold 在以下平台上进行了测试：

| 平台 | Python 版本 | 测试状态 |
|------|------------|----------|
| Windows 11 | 3.9, 3.10, 3.11 | ✅ 通过 |
| Windows 10 | 3.9, 3.10 | ✅ 通过 |
| macOS 14 (Sonoma) | 3.9, 3.10, 3.11 | ✅ 通过 |
| macOS 13 (Ventura) | 3.9, 3.10 | ✅ 通过 |
| Ubuntu 22.04 | 3.9, 3.10, 3.11 | ✅ 通过 |
| Ubuntu 20.04 | 3.9 | ✅ 通过 |
| CentOS 8 | 3.9 | ✅ 通过 |
| Fedora 38 | 3.10, 3.11 | ✅ 通过 |

## 相关文档

- [配置文件说明](./configuration.md)
- [Python 版本管理](./python-version-management.md)
- [故障排除指南](./troubleshooting.md)
