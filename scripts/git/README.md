# Git 隐私检查工具

## 功能说明

根据 CC-Scaffold 宪章 **Principle X: 隐私保护与信息安全原则**，本工具在 Git 提交前自动检查暂存区中是否包含敏感信息，防止隐私泄露。

## 检测的敏感信息类型

- **电子邮件地址**: `test@example.com`
- **绝对路径包含用户名**: `/Users/username/`, `/home/username/`, `C:\Users\username\`
- **API 密钥/访问令牌**: `api_key=`, `access_token=`, `secret=`
- **密码字段**: `password=`, `passwd=`, `pwd=`
- **IP 地址**: `192.168.1.1`
- **URL 中的凭证**: `://user:pass@`
- **私钥文件**: `-----BEGIN PRIVATE KEY-----`

## 使用方法

### 自动安装

在项目根目录运行：

```bash
# Bash 脚本安装
bash scripts/git/install_git_hooks.sh

# 或使用 Python 脚本安装
python39 scripts/git/install_git_hooks.py
```

### 手动安装

将 `scripts/git/privacy_check.py` 复制到项目中，然后在 `.git/hooks/pre-commit` 中添加：

```bash
#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
PRIVACY_CHECK_SCRIPT="${PROJECT_ROOT}/scripts/git/privacy_check.py"

if [ -f "${PRIVACY_CHECK_SCRIPT}" ]; then
    python39 "${PRIVACY_CHECK_SCRIPT}"
    if [ $? -ne 0 ]; then
        echo "提交被阻止 - 检测到敏感信息"
        exit 1
    fi
fi

exit 0
```

### 手动检查

可以在任何时间手动运行检查：

```bash
python39 scripts/git/privacy_check.py
```

## 跳过检查（不推荐）

如果确认内容安全，可以使用 `--no-verify` 跳过检查：

```bash
git commit --no-verify -m "commit message"
```

## 常见问题

### 误报处理

如果检查出现误报，可以：

1. 修改代码，使用相对路径或占位符
2. 使用环境变量存储敏感信息
3. 确认安全后使用 `--no-verify` 跳过

### 正确的做法

```python
# 不好的示例 - 硬编码敏感信息
API_KEY = "sk-1234567890abcdef"
log_file = "/Users/username/work/app.log"

# 好的示例 - 使用环境变量和相对路径
import os
API_KEY = os.getenv("API_KEY")
log_file = "logs/app.log"
```

## 配置说明

### 自定义检测模式

编辑 `privacy_check.py` 中的 `SENSITIVE_PATTERNS` 字典来自定义检测规则：

```python
SENSITIVE_PATTERNS = {
    'custom_pattern': r'your_regex_here',
}
```

## 依赖关系

- Python 3.9+
- Git

## 相关文档

- [CC-Scaffold 宪章](../../.specify/memory/constitution.md)
- [隐私保护原则](../../.specify/memory/constitution.md#x-隐私保护与信息安全原则-privacy-protection-and-information-security)

## 许可证

MIT License
