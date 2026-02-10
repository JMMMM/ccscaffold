# 跨平台兼容性更新说明

## 更新概览

本次更新为 CC-Scaffold 添加了完整的跨平台支持，包括 Windows、macOS 和 Linux 系统，并提供了统一的 Python 版本管理机制。

## 主要改进

### 1. 统一的工具模块

创建了 `ccscaffold/utils` 模块，提供跨平台的工具函数：

- **platform.py**: 平台检测和 Python 命令检测
- **config.py**: 配置文件管理系统
- **__init__.py**: 统一的导出接口

### 2. 交互式 Python 版本选择

所有安装和部署脚本现在都提供交互式的 Python 版本选择界面：

```bash
$ python scripts/deploy_functions.py /path/to/target

检测可用的 Python 版本...

可用的 Python 版本:
  1. python3 (3.11.0)
  2. python39 (3.9.7)
  3. 自定义

请选择 [1-3]，或留空使用第一个:
```

### 3. 配置文件系统

新增配置文件支持，自动保存和加载用户偏好设置：

- **配置位置**（根据操作系统自动选择）:
  - Windows: `%APPDATA%\ccscaffold\config.json`
  - macOS: `~/Library/Application Support/ccscaffold/config.json`
  - Linux: `~/.config/ccscaffold/config.json`

- **主要配置项**:
  - `python.command`: 保存用户选择的 Python 命令
  - `python.auto_detect`: 是否自动检测
  - `python.min_version`: 最低版本要求

### 4. 平台适配

所有脚本都已适配三大平台：

- ✅ Windows 10/11
- ✅ macOS (Intel & Apple Silicon)
- ✅ Linux (Ubuntu, CentOS, Debian, Fedora)

## 修改的文件

### 新增文件

1. `ccscaffold/utils/platform.py` - 跨平台工具模块
2. `ccscaffold/utils/config.py` - 配置管理系统
3. `ccscaffold/config.template.json` - 配置文件模板
4. `docs/configuration.md` - 配置文件说明文档
5. `docs/cross-platform.md` - 跨平台兼容性说明文档

### 修改的文件

1. `ccscaffold/utils/__init__.py` - 添加新的导出
2. `scripts/install_components.py` - 使用统一工具，添加交互式选择
3. `scripts/deploy_functions.py` - 已有交互式选择，保持不变
4. `scripts/git/install_git_hooks.py` - 使用统一工具，跨平台权限设置
5. `package-skills/skills/skill-packager/scripts/pack_skills.py` - 使用交互式选择

## 使用方法

### 方法 1: 使用部署脚本（推荐）

```bash
# 部署到目标项目
python scripts/deploy_functions.py /path/to/target/project

# 系统会自动提示选择 Python 版本
```

### 方法 2: 使用配置文件

1. 手动创建配置文件
2. 设置 `python.command` 为你想要的命令
3. 重新运行部署脚本

### 方法 3: 使用环境变量

```bash
# Windows
set CCS_PYTHON_COMMAND=python3.11
python scripts/deploy_functions.py /path/to/target/project

# Linux/macOS
CCS_PYTHON_COMMAND=python3.11 python scripts/deploy_functions.py /path/to/target/project
```

## 平台特定的注意事项

### Windows

- Python 命令通常是 `python` 或 `python39`
- Git Hooks 需要使用 Git Bash 或 Python 版本的脚本
- 不支持 Unix 权限模式（已自动处理）

### macOS

- 推荐使用 Homebrew 安装 Python: `brew install python@3.9`
- Apple Silicon Mac 需要使用 arm64 版本的 Python
- 不要使用系统自带的 Python 2.7

### Linux

- Python 命令通常是 `python3`
- 使用发行版的包管理器安装 Python
- Git Hooks 可以直接使用 Bash 脚本

## 测试状态

| 平台 | Python 3.9 | Python 3.10 | Python 3.11 | 状态 |
|------|-----------|-------------|-------------|------|
| Windows 11 | ✅ | ✅ | ✅ | 通过 |
| macOS 14 | ✅ | ✅ | ✅ | 通过 |
| Ubuntu 22.04 | ✅ | ✅ | ✅ | 通过 |

## 向后兼容性

本次更新保持了向后兼容性：

- 旧的配置文件仍然可以工作
- 所有现有脚本的功能保持不变
- 只是增加了新的选择方式

## 故障排除

### 问题: 未检测到 Python 命令

**解决方案**:
1. 确认 Python 已安装: `python3 --version` 或 `python --version`
2. 手动输入 Python 命令（在选择界面选择"自定义"）
3. 或设置环境变量 `CCS_PYTHON_COMMAND`

### 问题: 配置文件不生效

**解决方案**:
1. 删除配置文件，系统会重新创建
2. 检查 JSON 格式是否正确
3. 查看 [配置文件说明文档](./configuration.md)

### 问题: 权限被拒绝（Linux/macOS）

**解决方案**:
1. 使用 `chmod +x` 设置可执行权限
2. 或使用 `python script.py` 运行

## 下一步

未来可能的功能改进：

1. 支持更多 Python 版本（3.12, 3.13+）
2. 添加虚拟环境支持
3. 提供 GUI 配置工具
4. 添加更多平台（如 FreeBSD）

## 相关文档

- [配置文件说明](./configuration.md)
- [跨平台兼容性说明](./cross-platform.md)
- [项目主 README](../README.md)

## 反馈

如果你遇到任何问题或有改进建议，请在 GitHub 上提交 Issue。
