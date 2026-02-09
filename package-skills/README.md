# 组件打包功能 (Package Skills)

## 功能说明

通用的组件打包工具,支持将 skills、hooks、agents、commands 四种组件类型打包成独立的安装包,方便分发和安装到其他项目。

### 主要特点

- **多类型支持**: 支持 skills/hooks/agents/commands 四种组件
- **自动发现**: 自动扫描并列出所有可用组件
- **交互式选择**: 友好的多选界面
- **自包含包**: 生成自包含的安装包
- **跨平台**: 支持 Windows、Linux、macOS

## 使用方法

### 前置条件

1. Python 3.9+
2. 对项目目录的读权限
3. 对输出目录的写权限

### 基本使用

#### 打包 skills

```bash
python package-skills/skills/skill-packager/scripts/pack_skills.py -t skills
```

#### 打包 hooks

```bash
python package-skills/skills/skill-packager/scripts/pack_skills.py -t hooks
```

#### 打包所有组件

```bash
python package-skills/skills/skill-packager/scripts/pack_skills.py -t all
```

#### 打包特定组件

```bash
# 打包多个组件
python package-skills/skills/skill-packager/scripts/pack_skills.py -t skills

# 在交互式菜单中选择要打包的组件
```

### 高级用法

#### 指定输出目录

```bash
python package-skills/skills/skill-packager/scripts/pack_skills.py -t skills -o /path/to/output
```

#### 批量打包

```bash
# 打包所有类型到不同目录
for type in skills hooks agents commands; do
    python package-skills/skills/skill-packager/scripts/pack_skills.py -t $type
done
```

#### 自动化脚本

创建自动化打包脚本:

```python
#!/usr/bin/env python3
import subprocess
import os

components = ['skills', 'hooks', 'agents', 'commands']

for component in components:
    print(f"Packing {component}...")
    subprocess.run([
        'python', 'package-skills/skills/skill-packager/scripts/pack_skills.py',
        '-t', component
    ])
    print(f"✓ {component} packed")
```

## 配置说明

### 必需配置

无。该工具不需要额外的配置。

### 可选配置

#### 组件扫描路径

默认: 当前目录的 `skills/`、`hooks/`、`agents/`、`commands/` 目录

可通过修改脚本中的扫描路径来自定义。

#### 输出目录

默认: 当前目录的 `packages/` 目录

可通过 `-o` 参数指定自定义输出目录。

#### 打包格式

默认: ZIP 格式

可通过修改脚本中的打包格式来支持其他格式(如 TAR、TAR.GZ)。

### 环境变量

无。

## 依赖关系

- **Python**: 3.9+ 必需
- **标准库**: zipfile, json, pathlib (无需额外安装)

## 注意事项

1. **路径问题**: Windows 路径使用 `\\` 或原始字符串 `r"path"`
2. **权限问题**: 确保对源目录和目标目录有相应权限
3. **大文件**: 组件文件过大时打包可能需要较长时间
4. **编码问题**: 确保所有文件使用 UTF-8 编码
5. **特殊字符**: 避免文件名中包含特殊字符

## 打包流程

1. **扫描组件**: 根据类型扫描对应的目录
2. **列出组件**: 显示所有找到的组件
3. **用户选择**: 用户选择要打包的组件
4. **收集文件**: 收集组件相关的所有文件
5. **创建包**: 将文件打包成 ZIP
6. **保存包**: 保存到指定目录
7. **生成清单**: 生成组件清单文件

## 目录结构

```
package-skills/
├── skills/
│   └── skill-packager/       # 组件打包技能
│       ├── skill.json        # 技能配置
│       ├── SKILL.md          # 技能说明
│       ├── CLAUDE.md         # Claude 指令
│       └── scripts/
│           └── pack_skills.py  # 打包脚本
├── docs/
│   ├── skill-packager.md     # 详细文档
│   └── migrate-script.md     # 迁移脚本文档
└── README.md                 # 本文件
```

## 打包内容

每个打包的安装包包含:

- **组件文件**: skill.json、.py 脚本等
- **文档文件**: README.md、SKILL.md 等
- **依赖声明**: 依赖的其他组件或库
- **安装脚本**: 自动安装脚本(可选)
- **清单文件**: package-manifest.json

## 使用场景

### 场景 1: 分享单个 skill

```bash
# 打包特定的 skill
python package-skills/skills/skill-packager/scripts/pack_skills.py -t skills
# 选择要分享的 skill
# 将生成的 ZIP 文件分享给他人
```

### 场景 2: 批量分发

```bash
# 打包所有组件类型
python package-skills/skills/skill-packager/scripts/pack_skills.py -t all
# 将所有 ZIP 文件上传到服务器或分享给团队
```

### 场景 3: 版本管理

```bash
# 为特定版本创建打包
python package-skills/skills/skill-packager/scripts/pack_skills.py -t skills
# 在文件名中包含版本号
```

## 安装打包的组件

### 方法 1: 手动解压

```bash
# 解压打包文件
unzip package-name.zip -d .claude/skills/
```

### 方法 2: 使用安装脚本

```bash
# 如果打包文件包含 install.sh 或 install.py
python install.py
```

### 方法 3: 使用迁移脚本

```bash
# 将打包文件放到 CC-Scaffold 的对应目录
# 然后使用迁移脚本安装
python /path/to/ccscaffold/scripts/migrate_experience.py
```

## 故障排除

### 问题 1: 找不到组件

**症状**: 扫描不到任何组件

**解决方案**:
1. 检查目录结构是否正确
2. 确认组件配置文件存在(skill.json)
3. 查看扫描路径配置
4. 运行调试模式查看详细信息

### 问题 2: 打包失败

**症状**: 打包过程中出现错误

**解决方案**:
1. 检查文件权限
2. 确认磁盘空间充足
3. 检查文件名是否包含特殊字符
4. 查看错误日志了解详情

### 问题 3: 打包文件过大

**症状**: 生成的 ZIP 文件很大

**解决方案**:
1. 排除不必要的文件(如 __pycache__)
2. 压缩文档和图片
3. 分离依赖和主文件
4. 使用增量打包

## 最佳实践

1. **版本控制**: 在打包前打上版本标签
2. **文档完整**: 确保每个组件都有完整的文档
3. **依赖声明**: 清晰声明所有依赖关系
4. **测试验证**: 打包前在测试项目中验证
5. **清单文件**: 包含详细的组件清单

## 扩展建议

1. **自动发布**: 集成 CI/CD 自动打包和发布
2. **仓库管理**: 建立组件仓库系统
3. **版本管理**: 支持多版本共存
4. **依赖解析**: 自动解析和安装依赖
5. **签名验证**: 添加包签名和验证机制

## 相关文档

- [组件打包详细文档](docs/skill-packager.md)
- [迁移脚本使用](docs/migrate-script.md)
- [Python zipfile 文档](https://docs.python.org/3/library/zipfile.html)

## 更新日志

- v1.0.0 (2025-02-09): 初始版本
