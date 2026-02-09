# 组件打包工具

当一个用户请求打包、导出或迁移 Claude Code 组件时使用此工具。

## 何时使用

当用户说以下内容时触发：
- "帮我打包 [skills/hooks/agents/commands]"
- "打包 [skills/hooks/agents/commands] 组件"
- "导出 [skills/hooks/agents/commands]"
- "迁移 [skills/hooks/agents/commands] 到其他项目"
- "打包所有组件"
- "创建组件包"

## 组件类型

- **skills**: 技能组件，包含特定功能的可重用技能
- **hooks**: 钩子组件，在特定事件时触发的脚本
- **agents**: 代理组件，执行特定任务的 AI 代理
- **commands**: 命令组件，自定义的快捷命令
- **all**: 所有组件类型

## 使用方法

1. 识别用户请求的组件类型（skills/hooks/agents/commands/all）
2. 运行打包脚本：`python skills/skill-packager/scripts/pack_skills.py --type <组件类型>`
3. 如果未指定类型，默认为 skills
4. 如果指定 "all"，则列出所有类型的组件供选择

## 输出

工具会：
1. 列出指定类型的所有可用组件
2. 显示每个组件的名称和描述
3. 让用户选择要打包的组件
4. 生成包含安装脚本的自包含包
5. 提供安装命令

## 示例

用户输入："帮我打包 skills"
-> 运行：`python skills/skill-packager/scripts/pack_skills.py --type skills`

用户输入："打包所有 hooks"
-> 运行：`python skills/skill-packager/scripts/pack_skills.py --type hooks`

用户输入："帮我打包所有组件"
-> 运行：`python skills/skill-packager/scripts/pack_skills.py --type all`
