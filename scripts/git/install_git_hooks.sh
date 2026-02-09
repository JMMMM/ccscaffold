#!/usr/bin/env bash
#
# Install Git Hooks Script
# 安装 Git 钩子脚本 - 将隐私检查脚本安装到项目的 .git/hooks/
#

set -e

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

# 钩子目录
GIT_HOOKS_DIR="${PROJECT_ROOT}/.git/hooks"
PRIVACY_CHECK_SCRIPT="${SCRIPT_DIR}/privacy_check.py"

echo "================================"
echo "Installing Git Hooks"
echo "================================"
echo ""

# 检查是否在 Git 仓库中
if [ ! -d "${PROJECT_ROOT}/.git" ]; then
    echo "错误: 当前目录不是一个 Git 仓库"
    echo "请确保在项目根目录运行此脚本"
    exit 1
fi

# 创建钩子目录（如果不存在）
mkdir -p "${GIT_HOOKS_DIR}"

# 安装 pre-commit 钩子
echo "安装 pre-commit 钩子..."

cat > "${GIT_HOOKS_DIR}/pre-commit" << 'EOF'
#!/usr/bin/env bash
#
# Git Pre-commit Hook - Privacy Check
# Git 提交前隐私检查钩子
#

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
PRIVACY_CHECK_SCRIPT="${PROJECT_ROOT}/scripts/git/privacy_check.py"

# 检查隐私检查脚本是否存在
if [ -f "${PRIVACY_CHECK_SCRIPT}" ]; then
    python39 "${PRIVACY_CHECK_SCRIPT}"
    EXIT_CODE=$?

    if [ ${EXIT_CODE} -ne 0 ]; then
        echo ""
        echo "警告: 提交被阻止 - 检测到敏感信息"
        echo "使用 'git commit --no-verify' 跳过检查（不推荐）"
        exit 1
    fi
else
    echo "警告: 隐私检查脚本不存在: ${PRIVACY_CHECK_SCRIPT}"
    echo "继续提交..."
fi

exit 0
EOF

# 设置钩子可执行权限
chmod +x "${GIT_HOOKS_DIR}/pre-commit"

echo "  pre-commit 钩子已安装"
echo ""

echo "================================"
echo "安装完成！"
echo "================================"
echo ""
echo "已安装的 Git 钩子:"
echo "  - pre-commit: 提交前自动检查隐私安全"
echo ""
echo "每次执行 'git commit' 时会自动运行隐私检查"
echo ""
echo "如需跳过检查（不推荐）:"
echo "  git commit --no-verify"
echo ""
