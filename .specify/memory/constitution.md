# CC-Scaffold Constitution

<!--
Sync Impact Report:
- Version change: 1.2.0 → 1.3.0
- Added Principle IX: 跨平台可移植性优先原则 (Cross-Platform Portability Priority)
  - 平台兼容性强制要求 (Platform Compatibility Requirements)
  - 性能与可移植性权衡规则 (Performance vs Portability Trade-offs)
  - 平台特定优化策略 (Platform-Specific Optimization Strategy)
  - 移植交互模式要求 (Interactive Migration Mode)
- Updated all templates to include cross-platform portability compliance checks
- Template review:
  ✅ plan-template.md - 已添加跨平台兼容性检查项
  ✅ spec-template.md - 已添加跨平台需求
  ✅ tasks-template.md - 已添加跨平台合规清单
- Follow-up: 审查现有功能组件的跨平台兼容性并提供优化方案
-->

## Core Principles

### I. 临时文件路径标准化 (Temporary File Path Standardization)

所有功能在生成临时文件时,必须遵循统一的目录结构:

**规则:**
- 所有临时文件必须生成在当前项目根目录下的 `.claude/tmp/` 目录中
- 按功能类型进行子目录分类,例如:
  - 对话记录: `.claude/tmp/conversations/`
  - 缓存数据: `.claude/tmp/cache/`
  - 临时脚本: `.claude/tmp/scripts/`
  - 其他临时文件: 根据功能创建相应子目录
- 文件命名必须包含时间戳以确保唯一性,格式: `{功能名}-{timestamp}.{扩展名}`
  - 例如: `conversation-20250209143025.txt`

**理由:**
- 保持项目目录整洁,避免临时文件散落在各处
- 便于清理和维护临时文件
- 提供一致的临时文件访问路径
- 支持多会话并发操作而不会产生冲突

### II. 文档语言规范 (Documentation Language Standards)

**规则:**
- 所有项目文档必须使用中文编写
- 所有脚本文件必须使用英文命名
- 代码注释可以使用中文或英文,但应保持一致性

**理由:**
- 面向中文用户社区,提供更好的可读性
- 脚本英文命名确保跨平台兼容性
- 降低本地开发者的使用门槛

### III. Python 版本兼容性 (Python Version Compatibility)

**规则:**
- 所有 Python 脚本必须兼容 Python 3.9+
- 使用 `python39` 或 `python3.9` 命令运行脚本
- 避免使用仅在更高版本中可用的特性

**理由:**
- 确保在不同环境中的一致性
- 支持较旧的系统环境
- 提供更广泛的兼容性

### IV. 代码字符规范 (Code Character Standards)

**规则:**
- 代码禁止使用任何特殊 Unicode 字符
- 仅使用 ASCII 字符集
- 文件编码使用 UTF-8 (但不包含特殊字符)

**理由:**
- 避免编码问题导致的运行时错误
- 确保跨平台兼容性
- 减少因字符编码引起的调试困难

### V. 文档组织规范 (Documentation Organization)

**规则:**
- 所有 Markdown 文档都应该放在 `docs/` 文件夹内
- 按功能模块进行子目录分类
- 每个功能包必须有对应的 README 或使用文档

**理由:**
- 集中管理文档,便于查找和维护
- 清晰的文档结构提升用户体验
- 支持文档的模块化组织

### VI. 组件自包含原则 (Component Self-Containment)

**规则:**
- 每个 skill/hook/agent/command 必须自包含
- 包含必要的配置文件、文档和脚本
- 可以独立打包和分发
- 明确声明依赖关系

**理由:**
- 支持组件的独立开发和测试
- 便于组件的迁移和复用
- 降低组件间的耦合度

### VII. README.md 强制要求 (README Mandatory Requirement)

**规则:**
- 每个功能组件(包括 skills/hooks/agents/commands)必须包含 README.md 文件
- README.md 必须使用中文编写
- README.md 必须包含以下章节:
  1. **功能说明**: 清晰描述该功能的作用和目的
  2. **使用方法**: 详细的使用步骤和示例
  3. **配置说明**: 所需的配置项、环境变量或设置
  4. **依赖关系**: 该功能依赖的其他组件或库
  5. **注意事项**: 使用时需要注意的重要事项

**理由:**
- 确保每个功能都有完整的使用文档
- 降低新用户的学习成本
- 提供统一的文档结构,便于快速查找信息
- 支持组件的独立使用和维护

### VIII. 代码质量标准 (Code Quality Standards)

**规则:**

#### VIII.1 可读性优化 (Readability Optimization)

所有代码必须以人类可理解的方式编写:

- **命名规范**: 变量、函数、类名必须清晰表达其用途
  - 变量名使用名词或形容词名词组合
  - 函数名使用动词或动词短语
  - 类名使用名词,采用大驼峰命名法
  - 常量使用全大写下划线分隔

- **注释要求**:
  - 复杂逻辑必须添加注释说明
  - 函数必须有文档字符串说明其功能、参数、返回值
  - 注释应说明"为什么"而非"是什么"

- **代码结构**:
  - 使用一致的缩进和格式(推荐 4 空格)
  - 相关代码组织在一起,不相关代码分离
  - 单个函数不应超过 50 行(特殊算法除外)
  - 单个类不应超过 300 行

- **魔法值消除**:
  - 禁止在代码中直接使用魔法数字或字符串
  - 必须定义为有意义的常量
  - 配置值应集中管理

#### VIII.2 高内聚低耦合原则 (High Cohesion, Low Coupling)

**高内聚要求**:
- 模块内的元素应当紧密相关,共同完成单一职责
- 一个类或模块应有明确的单一职责
- 相关的功能应组织在同一个模块内

**低耦合要求**:
- 模块间依赖应最小化
- 使用接口或抽象类而非具体实现
- 依赖注入优于直接依赖
- 避免循环依赖

**实现指导**:
```python
# 不好的示例 - 高耦合
class UserService:
    def __init__(self):
        self.db = Database()  # 直接依赖具体实现

# 好的示例 - 低耦合
class UserService:
    def __init__(self, db: DatabaseInterface):  # 依赖抽象接口
        self.db = db
```

#### VIII.3 模块化思维要求 (Modular Thinking)

**模块划分原则**:
- 按功能领域划分模块,而非技术层次
- 每个模块应能独立理解、测试和修改
- 模块间通过明确的接口通信

**模块设计检查清单**:
- [ ] 模块是否有清晰的职责边界?
- [ ] 模块是否可以独立测试?
- [ ] 模块是否可以独立部署?
- [ ] 模块接口是否简洁明确?
- [ ] 模块内部实现是否可以自由修改而不影响其他模块?

**目录结构示例**:
```
feature-module/
├── core/           # 核心业务逻辑
├── api/            # 对外接口
├── models/         # 数据模型
├── utils/          # 工具函数
└── tests/          # 测试用例
```

#### VIII.4 文件行数限制 (File Line Limit)

**强制要求**:
- 每个文件代码行数不得超过 1000 行(不含注释和空行)
- 推荐单个文件保持在 500 行以内

**超出限制时的处理**:
1. 分析文件结构,识别功能边界
2. 将文件拆分为多个更小的模块
3. 按职责重新组织代码
4. 确保拆分后的模块保持高内聚低耦合

**特殊情况说明**:
- 生成的代码(如协议缓冲区)可以豁免
- 数据文件(如配置、常量定义)可以适当放宽
- 必须在文件头部注释说明原因

**代码示例**:
```python
# 不好的示例 - 单个文件过长(超过 1000 行)
# user_manager.py (1500 行)
class UserManager:
    # ... 大量代码 ...

# 好的示例 - 拆分为多个文件
# user_manager/
#     __init__.py (20 行)
#     manager.py (150 行) - 核心管理逻辑
#     validator.py (200 行) - 验证逻辑
#     repository.py (180 行) - 数据访问
#     models.py (120 行) - 数据模型
```

**理由:**
- **可读性**: 代码必须易于人类阅读和理解
- **可维护性**: 降低修改风险,提高代码质量
- **可测试性**: 小模块更容易编写单元测试
- **团队协作**: 清晰的模块边界便于并行开发
- **代码复用**: 高内聚低耦合的模块更易复用

### IX. 跨平台可移植性优先原则 (Cross-Platform Portability Priority)

**规则:**

#### IX.1 平台兼容性强制要求 (Platform Compatibility Requirements)

所有新建功能必须优先考虑跨平台可移植性:

- **强制支持平台**: Windows、Linux、macOS
- **优先级排序**: 可移植性 > 性能 > 开发便利性
- **默认实现**: 使用跨平台的通用解决方案
- **测试要求**: 每个功能必须在三个平台上进行测试

**实现指南:**
```python
# 不好的示例 - 平台特定实现
def get_temp_path():
    return "C:\\Temp"  # 仅适用于 Windows

# 好的示例 - 跨平台实现
import os
import tempfile

def get_temp_path():
    return tempfile.gettempdir()  # 跨平台兼容
```

#### IX.2 性能与可移植性权衡规则 (Performance vs Portability Trade-offs)

当存在平台特定的高性能解决方案时:

1. **默认使用跨平台方案**: 即使性能略低
2. **平台优化作为可选增强**: 如果平台特定方案性能显著更优
3. **性能差异阈值**: 只有当性能提升超过 30% 时才考虑平台特定优化

**决策树:**
```
开始
  |
  v
是否存在平台特定的高性能方案?
  |
  +-- 否 --> 使用跨平台方案 ✅
  |
  +-- 是 --> 性能提升 > 30%?
              |
              +-- 否 --> 使用跨平台方案 ✅
              |
              +-- 是 --> 添加平台特定优化 📊
                          |
                          v
                    保持跨平台默认实现
                    添加平台特定实现作为可选
```

**代码示例:**
```python
# 默认跨平台实现 (Python)
def process_files(file_list):
    """跨平台默认实现 - 使用 Python"""
    for file in file_list:
        process_file(file)

# Windows 平台优化 (PowerShell) - 可选增强
def process_files_windows_optimized(file_list):
    """Windows 专用高性能实现"""
    if platform.system() == "Windows":
        # 调用 PowerShell 脚本
        subprocess.run([
            "powershell",
            "-File",
            "process_files.ps1",
            *file_list
        ])
    else:
        # 回退到跨平台实现
        process_files(file_list)
```

#### IX.3 平台特定优化策略 (Platform-Specific Optimization Strategy)

当实现平台特定优化时:

- **文件命名约定**: `{功能名}-{平台}.{扩展名}`
  - 示例: `deploy-windows.ps1`, `deploy-linux.sh`, `deploy-macos.sh`

- **目录结构组织**:
  ```
  feature-name/
  ├── scripts/
  │   ├── core.py              # 跨平台核心实现
  │   ├── windows/
  │   │   └── optimize.ps1     # Windows 优化
  │   ├── linux/
  │   │   └── optimize.sh      # Linux 优化
  │   └── macos/
  │       └── optimize.sh      # macOS 优化
  └── README.md
  ```

- **自动检测与回退**: 平台检测失败时自动回退到跨平台实现

**实现示例:**
```python
import platform
import subprocess
from pathlib import Path

class PlatformOptimizer:
    def __init__(self):
        self.system = platform.system()
        self.script_dir = Path(__file__).parent

    def optimize(self, args):
        """根据平台选择最优实现"""
        if self.system == "Windows":
            return self._windows_optimize(args)
        elif self.system == "Linux":
            return self._linux_optimize(args)
        elif self.system == "Darwin":  # macOS
            return self._macos_optimize(args)
        else:
            return self._default_optimize(args)

    def _windows_optimize(self, args):
        """Windows 平台优化实现"""
        ps_script = self.script_dir / "windows" / "optimize.ps1"
        if ps_script.exists():
            return subprocess.run([
                "powershell",
                "-ExecutionPolicy", "Bypass",
                "-File", str(ps_script),
                *args
            ])
        else:
            return self._default_optimize(args)

    def _default_optimize(self, args):
        """跨平台默认实现"""
        # Python 实现
        pass
```

#### IX.4 移植交互模式要求 (Interactive Migration Mode)

所有组件打包和迁移工具必须提供交互式平台选择:

**必需功能:**
1. **平台检测**: 自动检测当前平台
2. **交互确认**: 显示检测到的平台并请求确认
3. **多平台选择**: 允许用户选择目标平台
4. **平台特定配置**: 根据选择生成平台特定配置

**交互流程示例:**
```
检测到当前平台: Windows

请选择目标平台:
[1] Windows (当前平台)
[2] Linux
[3] macOS
[4] 所有平台
[5] 自定义选择

请输入选项 [1-5]: 4

将为以下平台生成安装包:
✓ Windows
✓ Linux
✓ macOS

是否继续? [Y/n]: Y

正在生成跨平台安装包...
✓ Windows 安装包已生成: dist/windows-feature.zip
✓ Linux 安装包已生成: dist/linux-feature.zip
✓ macOS 安装包已生成: dist/macos-feature.zip
```

**实现模板:**
```python
def interactive_platform_selection():
    """交互式平台选择"""
    platforms = {
        "1": ("Windows", "windows"),
        "2": ("Linux", "linux"),
        "3": ("macOS", "macos"),
        "4": ("所有平台", "all"),
        "5": ("自定义", "custom")
    }

    current = platform.system()
    print(f"\n检测到当前平台: {current}\n")

    print("请选择目标平台:")
    for key, (name, _) in platforms.items():
        marker = " (当前平台)" if name == current else ""
        print(f"[{key}] {name}{marker}")

    choice = input("\n请输入选项 [1-5]: ").strip()

    if choice == "5":
        return custom_platform_selection()
    elif choice in platforms:
        return platforms[choice][1]
    else:
        print("无效选项,使用当前平台")
        return current.lower()
```

**理由:**
- **用户覆盖**: 最大化用户群体,支持主流操作系统
- **可维护性**: 减少平台特定代码,降低维护成本
- **性能平衡**: 在保证可移植性的前提下提供平台优化
- **用户体验**: 交互模式简化跨平台部署流程
- **未来扩展**: 清晰的平台分层便于添加新平台支持

## 组件结构规范

每个功能组件应遵循以下目录结构:

```
component-name/
├── skill.json        # 技能配置 (如果是 skill)
├── SKILL.md          # 技能说明 (如果是 skill)
├── hooks/            # 相关 hooks
├── scripts/          # 相关脚本
├── README.md         # ⚠️ 必需: 使用文档,包含功能说明、使用方法、配置说明
└── docs/             # 详细文档 (可选)
```

### README.md 标准模板

```markdown
# [功能名称]

## 功能说明

[清晰描述该功能的作用和目的]

## 使用方法

### 前置条件

[列出使用该功能前需要满足的条件]

### 基本使用

[详细的使用步骤和示例]

### 高级用法

[可选: 高级使用场景和技巧]

## 配置说明

### 必需配置

[列出所有必需的配置项]

### 可选配置

[列出所有可选的配置项及其默认值]

### 环境变量

[如果需要,列出相关的环境变量]

## 依赖关系

- [依赖项 1]: [版本要求]
- [依赖项 2]: [版本要求]

## 注意事项

- [重要注意事项 1]
- [重要注意事项 2]

## 故障排除

[可选: 常见问题和解决方法]

## 相关文档

- [链接到其他相关文档]
```

## 开发工作流

### 功能包开发流程

1. 在相应目录下创建新组件目录
2. 创建必要的配置文件和脚本
3. **编写 README.md 文档(必需)**
4. 遵循本宪章的所有原则
5. 在迁移脚本中注册新功能(如果需要)

### 代码审查检查点

#### 基础合规检查
- [ ] 临时文件路径符合 `.claude/tmp/` 规范
- [ ] 文档使用中文,脚本使用英文命名
- [ ] Python 代码兼容 3.9+
- [ ] 无特殊 Unicode 字符
- [ ] 文档放置在 `docs/` 目录
- [ ] 组件自包含且可独立运行
- [ ] **包含 README.md 且符合标准模板**
- [ ] **README 包含功能说明、使用方法、配置说明**

#### 代码质量检查
- [ ] **变量、函数、类命名清晰表达用途**
- [ ] **复杂逻辑添加注释说明**
- [ ] **函数有完整的文档字符串**
- [ ] **无魔法数字或字符串,已定义为常量**
- [ ] **单个函数不超过 50 行**
- [ ] **单个类不超过 300 行**
- [ ] **模块职责单一,边界清晰**
- [ ] **模块间依赖最小化,无循环依赖**
- [ ] **使用依赖注入而非直接依赖具体实现**
- [ ] **模块可以独立测试**
- [ ] **每个文件不超过 1000 行代码**

#### 跨平台可移植性检查
- [ ] **功能支持 Windows、Linux、macOS 三个平台**
- [ ] **默认使用跨平台实现**
- [ ] **平台特定优化有明确的性能提升依据 (>30%)**
- [ ] **平台特定代码有回退到跨平台实现的逻辑**
- [ ] **文件路径使用跨平台库 (pathlib, tempfile 等)**
- [ ] **移植工具提供交互式平台选择**
- [ ] **在目标平台进行了测试**
- [ ] **文档中说明平台兼容性和限制**

## 质量标准

### 可维护性

- 代码必须有清晰的注释
- 每个功能必须有对应的使用文档
- **README.md 必须完整且及时更新**
- 文档应包含使用示例和注意事项
- **代码结构清晰,易于理解和修改**

### 可测试性

- 组件应支持独立测试
- 提供测试用例或测试说明
- 明确的输入输出规范
- **模块化设计便于编写单元测试**

### 可移植性

- **强制要求**: 必须支持 Windows、Linux、macOS 三个主流平台
- **优先级**: 可移植性 > 性能 > 开发便利性
- **默认策略**: 使用跨平台的通用解决方案
- **平台优化**: 仅在性能提升超过 30% 时才考虑平台特定实现
- **文件路径**: 必须使用跨平台库 (pathlib, tempfile 等)
- **交互模式**: 移植工具必须提供交互式平台选择
- **回退机制**: 平台特定代码必须有回退到跨平台实现的逻辑
- **测试覆盖**: 每个功能必须在三个平台上进行测试

### 文档完整性

- **每个功能组件必须有 README.md**
- **README 必须包含所有必需章节**
- **文档必须与代码实现保持同步**
- **代码注释充分,解释设计决策**

## 治理规则

### 宪章修订流程

1. 修订必须通过团队讨论和批准
2. 修订后必须更新版本号
3. 必须更新所有相关模板和文档
4. 必须提供迁移计划(如需要)

### 版本控制规则

- 遵循语义化版本规范 (MAJOR.MINOR.PATCH)
- MAJOR: 重大架构变更或原则移除
- MINOR: 新增原则或功能扩展
- PATCH: 文档修正或小改进

### 合规性审查

- 所有代码审查必须验证宪章合规性
- **所有功能组件必须检查 README.md 的存在和完整性**
- **所有代码必须通过代码质量检查**
- **所有功能必须通过跨平台可移植性检查**
- **文件行数超过 1000 行必须提供拆分方案**
- 复杂度增加必须有充分理由
- 违反原则必须有明确的例外说明

### 运行时指导

- 开发过程中参考本宪章进行决策
- 遇到冲突时以本宪章为准
- 定期审查和更新宪章内容
- **持续关注代码质量,及时重构优化**
- **优先考虑跨平台可移植性,再考虑性能优化**

---

**Version**: 1.3.0 | **Ratified**: 2025-02-09 | **Last Amended**: 2026-02-09
