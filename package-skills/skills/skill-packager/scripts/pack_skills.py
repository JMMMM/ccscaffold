#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Claude Code 组件打包工具
用于选择并打包多个组件（skills/hooks/agents/commands）或按功能打包，方便迁移到其他项目
"""

import argparse
import json
import os
import shutil
import sys
from pathlib import Path
from typing import List, Dict, Optional

# 添加项目根目录到 Python 路径
project_root = Path(__file__).resolve().parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from ccscaffold.utils import (
    detect_available_python_commands,
    interactive_python_command_selection
)


class ComponentPackager:
    """Claude Code 组件打包器"""

    # 组件类型映射
    COMPONENT_TYPES = {
        "skills": {"dir": "skills", "config": "skill.json", "name_field": "name"},
        "hooks": {"dir": "hooks", "config": "hook.json", "name_field": "name"},
        "agents": {"dir": "agents", "config": "agent.json", "name_field": "name"},
        "commands": {"dir": "commands", "config": "command.json", "name_field": "command"}
    }

    def __init__(self, project_dir: Path, component_type: str = "skills"):
        self.project_dir = project_dir
        self.component_type = component_type
        self.dist_dir = project_dir / "dist"
        self.python_command = "python39"  # 默认Python命令

        # 加载功能配置
        self.functions_config = self._load_functions_config()

        # 根据类型设置目录
        if component_type == "all":
            self.components = []
            self.types_to_scan = ["skills", "hooks", "agents", "commands"]
        elif component_type == "function":
            self.components = []
            self.types_to_scan = ["skills", "hooks", "agents", "commands"]
        else:
            type_config = self.COMPONENT_TYPES.get(component_type, {})
            self.components_dir = project_dir / type_config.get("dir", component_type)
            self.config_file = type_config.get("config", "config.json")
            self.name_field = type_config.get("name_field", "name")
            self.components = []

    def _load_functions_config(self) -> Dict:
        """加载功能配置文件"""
        config_file = self.project_dir / "scripts" / "functions.json"
        if config_file.exists():
            try:
                with open(config_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"[警告] 读取功能配置文件失败: {e}")
        return {}

    def set_python_command(self, python_cmd: str):
        """设置Python命令"""
        self.python_command = python_cmd

    def discover_components(self, comp_type: Optional[str] = None) -> List[Dict]:
        """发现指定类型的组件"""
        if comp_type is None:
            comp_type = self.component_type

        if comp_type == "all":
            return self._discover_all_components()

        type_config = self.COMPONENT_TYPES.get(comp_type, {})
        components_dir = self.project_dir / type_config.get("dir", comp_type)
        config_file = type_config.get("config", "config.json")
        name_field = type_config.get("name_field", "name")

        components = []
        if not components_dir.exists():
            return components

        for comp_path in components_dir.iterdir():
            if comp_path.is_dir() and not comp_path.name.startswith("_"):
                config_path = comp_path / config_file
                if config_path.exists():
                    try:
                        with open(config_path, "r", encoding="utf-8") as f:
                            data = json.load(f)
                            components.append({
                                "type": comp_type,
                                "name": data.get(name_field, comp_path.name),
                                "description": data.get("description", "无描述"),
                                "version": data.get("version", "1.0.0"),
                                "path": comp_path
                            })
                    except Exception as e:
                        print(f"[警告] 读取 {config_path} 失败: {e}")
        return components

    def _discover_all_components(self) -> List[Dict]:
        """发现所有类型的组件"""
        all_components = []
        for comp_type in ["skills", "hooks", "agents", "commands"]:
            all_components.extend(self.discover_components(comp_type))
        return all_components

    def discover_function_components(self, function_key: str) -> List[Dict]:
        """根据功能配置发现相关组件"""
        if not self.functions_config:
            print("[错误] 未找到功能配置文件 (scripts/functions.json)")
            return []

        functions = self.functions_config.get("functions", {})
        if function_key not in functions:
            print(f"[错误] 未知的功能: {function_key}")
            return []

        function_config = functions[function_key]
        components = []

        # 处理 skills 组件
        for skill_name in function_config.get("components", {}).get("skills", []):
            # 查找 .claude/skills 目录
            skill_path = self.project_dir / ".claude" / "skills" / skill_name
            if not skill_path.exists():
                # 尝试 skills 目录
                skill_path = self.project_dir / "skills" / skill_name

            if skill_path.exists():
                config_path = skill_path / "skill.json"
                description = function_config.get("description", "")
                version = "1.0.0"

                if config_path.exists():
                    try:
                        with open(config_path, "r", encoding="utf-8") as f:
                            data = json.load(f)
                            description = data.get("description", description)
                            version = data.get("version", version)
                    except:
                        pass

                components.append({
                    "type": "skills",
                    "name": skill_name,
                    "description": description,
                    "version": version,
                    "path": skill_path
                })

        # 处理 hooks 组件（项目级 hooks）
        hooks_dir = function_config.get("hooks_dir", ".claude-hooks")
        for hook_file in function_config.get("components", {}).get("hooks", []):
            hook_path = self.project_dir / hooks_dir / hook_file
            if hook_path.exists():
                components.append({
                    "type": "hooks",
                    "name": hook_file.replace(".py", ""),
                    "description": f"Hook: {hook_file}",
                    "version": "1.0.0",
                    "path": hook_path,
                    "is_file": True  # 标记为单个文件
                })

        # 处理 commands 组件
        for cmd_name in function_config.get("components", {}).get("commands", []):
            # commands 通常在 skills 的配置中
            # 这里我们添加一个标记，让安装脚本知道要处理 commands
            components.append({
                "type": "commands",
                "name": cmd_name,
                "description": f"Command: {cmd_name}",
                "version": "1.0.0",
                "path": None,  # commands 通常是配置，不是独立的目录
                "is_config": True
            })

        return components

    def list_functions(self) -> None:
        """列出所有可用功能"""
        if not self.functions_config:
            print("\n[信息] 未找到功能配置文件 (scripts/functions.json)")
            return

        functions = self.functions_config.get("functions", {})

        print("\n" + "=" * 80)
        print("可用功能列表".center(80))
        print("=" * 80)

        for idx, (key, config) in enumerate(functions.items(), 1):
            print(f"\n[{idx}] {key}")
            print(f"    名称: {config.get('name', '未知')}")
            print(f"    描述: {config.get('description', '无描述')}")

            components = config.get("components", {})
            comp_summary = []
            if components.get("skills"):
                comp_summary.append(f"skills: {', '.join(components['skills'])}")
            if components.get("hooks"):
                comp_summary.append(f"hooks: {', '.join(components['hooks'])}")
            if components.get("commands"):
                comp_summary.append(f"commands: {', '.join(components['commands'])}")

            if comp_summary:
                print(f"    组件: {', '.join(comp_summary)}")

        print("\n" + "=" * 80)

    def select_function(self) -> Optional[str]:
        """选择功能"""
        self.list_functions()

        if not self.functions_config:
            return None

        functions = list(self.functions_config.get("functions", {}).keys())

        print("\n请输入要打包的功能编号")
        print("输入 'q' 退出\n")

        while True:
            try:
                user_input = input("选择> ").strip()

                if user_input.lower() == "q":
                    return None

                idx = int(user_input)
                if 1 <= idx <= len(functions):
                    return functions[idx - 1]
                else:
                    print(f"[警告] 索引超出范围，请输入 1-{len(functions)}")
            except ValueError:
                print("[错误] 输入格式错误，请输入数字编号")
            except (EOFError, KeyboardInterrupt):
                print("\n[信息] 已取消")
                return None

    def prompt_python_command(self) -> str:
        """提示用户选择 Python 命令"""
        print("\n" + "=" * 80)
        print("Python 版本配置".center(80))
        print("=" * 80)

        # 使用交互式选择
        python_cmd = interactive_python_command_selection()

        if python_cmd is None:
            # 如果用户取消，使用默认值
            default = self.functions_config.get("python_command", {}).get("default", "python3")
            print(f"\n使用默认 Python 命令: {default}")
            return default

        return python_cmd

    def display_components(self, components: List[Dict]) -> None:
        """显示组件列表"""
        if not components:
            print(f"\n[信息] 未找到任何组件")
            return

        # 按类型分组
        grouped = {}
        for comp in components:
            comp_type = comp.get("type", self.component_type)
            if comp_type not in grouped:
                grouped[comp_type] = []
            grouped[comp_type].append(comp)

        print("\n" + "=" * 80)
        print(f"可用的组件".center(80))
        print("=" * 80)

        for comp_type, comps in grouped.items():
            print(f"\n【{comp_type.upper()}】")
            print("-" * 80)
            for idx, comp in enumerate(comps, 1):
                # 计算全局索引
                global_idx = 0
                for prev_type in grouped:
                    if prev_type == comp_type:
                        break
                    global_idx += len(grouped[prev_type])
                global_idx += idx

                print(f"\n[{global_idx}] {comp['name']}")
                print(f"    描述: {comp['description']}")
                print(f"    版本: {comp['version']}")
                print(f"    路径: {comp['path']}")

        print("\n" + "=" * 80)

    def select_components(self, components: List[Dict]) -> List[Dict]:
        """选择组件"""
        self.display_components(components)

        if not components:
            return []

        print("\n请输入要打包的组件编号（多个用空格或逗号分隔）")
        print("例如: 1 3 5  或  1,3,5  或  all (选择全部)")
        print("输入 'q' 退出\n")

        while True:
            try:
                user_input = input("选择> ").strip()

                if user_input.lower() == "q":
                    return []

                if user_input.lower() == "all":
                    return components

                # 解析输入
                indices = []
                for part in user_input.replace(",", " ").split():
                    if part:
                        indices.append(int(part))

                # 验证索引
                selected = []
                for idx in indices:
                    if 1 <= idx <= len(components):
                        selected.append(components[idx - 1])
                    else:
                        print(f"[警告] 索引 {idx} 超出范围，已跳过")

                if selected:
                    # 去重
                    seen = set()
                    unique_selected = []
                    for s in selected:
                        key = (s['type'], s['name'])
                        if key not in seen:
                            seen.add(key)
                            unique_selected.append(s)
                    return unique_selected
                else:
                    print("[错误] 未选择有效的组件，请重新输入")
            except ValueError:
                print("[错误] 输入格式错误，请输入数字编号")
            except (EOFError, KeyboardInterrupt):
                print("\n[信息] 已取消")
                return []

    def create_package(self, components: List[Dict], output_name: str = None) -> Optional[Path]:
        """创建打包文件"""
        if not components:
            print("[错误] 没有选择任何组件")
            return None

        # 创建输出目录
        self.dist_dir.mkdir(exist_ok=True)

        # 生成包名
        if output_name is None:
            type_names = "-".join(sorted(set(c.get('type', 'unknown') for c in components)))
            comp_names = "-".join([c['name'] for c in components[:3]])
            if len(components) > 3:
                comp_names += "-etc"
            output_name = f"ccscaffold-{type_names}-{comp_names}"

        # 清理包名中的非法字符
        output_name = "".join(c if c.isalnum() or c in "-_" else "-" for c in output_name)

        package_dir = self.dist_dir / output_name
        package_dir.mkdir(exist_ok=True)

        # 清空包目录
        for item in package_dir.iterdir():
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()

        # 按类型复制组件
        for comp in components:
            comp_type = comp.get('type', self.component_type)

            # 检查是否是单个文件（如 hook 文件）
            if comp.get('is_file'):
                # 单个文件直接复制
                dest_dir = package_dir / ".claude-hooks"
                dest_dir.mkdir(parents=True, exist_ok=True)
                shutil.copy2(comp['path'], dest_dir / comp['path'].name)
            elif comp.get('is_config'):
                # 配置类型（如 commands），不需要复制文件
                pass
            else:
                # 目录类型的组件
                type_dir = comp_type if comp_type in self.COMPONENT_TYPES else self.component_type
                dest_dir = package_dir / type_dir / comp['name']
                dest_dir.mkdir(parents=True, exist_ok=True)

                # 复制所有文件
                if comp.get('path'):
                    for item in comp['path'].iterdir():
                        if item.is_dir():
                            shutil.copytree(item, dest_dir / item.name, dirs_exist_ok=True)
                        else:
                            shutil.copy2(item, dest_dir / item.name)

        # 创建清单文件
        manifest = {
            "package": output_name,
            "version": "1.0.0",
            "python_command": self.python_command,
            "components": [
                {
                    "type": c.get('type', self.component_type),
                    "name": c['name'],
                    "description": c['description'],
                    "version": c['version']
                }
                for c in components
            ],
            "install_command": f"{self.python_command} {output_name}/install.py"
        }

        manifest_file = package_dir / "manifest.json"
        with open(manifest_file, "w", encoding="utf-8") as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)

        # 创建安装脚本
        self._create_install_script(package_dir)

        print(f"\n[成功] 包已创建: {package_dir}")
        print(f"       共包含 {len(components)} 个组件")
        print(f"       Python命令: {self.python_command}")

        return package_dir

    def _create_install_script(self, package_dir: Path) -> None:
        """创建安装脚本"""
        install_script = package_dir / "install.py"

        script_content = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Claude Code 组件包安装脚本"""

import json
import os
import shutil
import sys
from pathlib import Path


# Python命令配置 - 由打包工具设置
PYTHON_COMMAND = "{self.python_command}"


def install():
    """安装组件到当前项目"""
    project_dir = Path.cwd()
    claude_dir = project_dir / ".claude"
    settings_file = claude_dir / "settings.json"

    # 读取清单
    manifest_file = Path(__file__).parent / "manifest.json"
    with open(manifest_file, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    print("=" * 70)
    print(f"安装包: {{manifest['package']}}")
    print(f"包含 {{len(manifest['components'])}} 个组件")
    print(f"Python命令: {{manifest.get('python_command', PYTHON_COMMAND)}}\\n")
    print("=" * 70)

    # 获取Python命令
    python_cmd = manifest.get("python_command", PYTHON_COMMAND)

    # 创建.claude目录
    claude_dir.mkdir(exist_ok=True)

    # 读取现有settings
    settings = {{}}
    if settings_file.exists():
        with open(settings_file, "r", encoding="utf-8") as f:
            settings = json.load(f)

    # 按类型安装组件
    for comp in manifest['components']:
        comp_type = comp['type']
        comp_name = comp['name']

        if comp_type == 'skills':
            dest_dir = claude_dir / "skills" / comp_name
            src_dir = Path(__file__).parent / "skills" / comp_name
        elif comp_type == 'hooks':
            # hooks 可能在 .claude-hooks 目录
            dest_dir = project_dir / ".claude-hooks"
            src_file = Path(__file__).parent / ".claude-hooks" / f"{{comp_name}}.py"
            if src_file.exists():
                dest_dir.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_file, dest_dir / src_file.name)
                # 更新settings.json以注册hooks
                if "hooks" not in settings:
                    settings["hooks"] = {{}}
                # 这里需要根据实际的hook类型来配置
                # 简化处理：提示用户手动配置
                print(f"[安装] {{comp_type}}: {{comp_name}} -> .claude-hooks/")
                print(f"[提示] 请手动在 settings.json 中配置此hook")
                continue
            else:
                print(f"[跳过] 源文件不存在: {{src_file}}")
                continue
        elif comp_type == 'agents':
            dest_dir = claude_dir / "agents" / comp_name
            src_dir = Path(__file__).parent / "agents" / comp_name
        elif comp_type == 'commands':
            # commands通常是skill的一部分，跳过
            print(f"[信息] {{comp_type}}: {{comp_name}} (已包含在skill配置中)")
            continue
        else:
            print(f"[跳过] 未知类型: {{comp_type}}")
            continue

        if not src_dir.exists():
            print(f"[警告] 源目录不存在: {{src_dir}}")
            continue

        # 删除旧版本
        if dest_dir.exists():
            shutil.rmtree(dest_dir)

        # 复制组件
        shutil.copytree(src_dir, dest_dir)
        print(f"[安装] {{comp_type}}: {{comp_name}}")

        # 更新settings（如果是skill）
        if comp_type == 'skills':
            config_file = dest_dir / "skill.json"
            if config_file.exists():
                with open(config_file, "r", encoding="utf-8") as f:
                    skill_config = json.load(f)
                # 更新hooks中的Python命令
                if "hooks" in skill_config:
                    if "hooks" not in settings:
                        settings["hooks"] = {{}}
                    for hook_type, hook_configs in skill_config["hooks"].items():
                        if hook_type not in settings["hooks"]:
                            settings["hooks"][hook_type] = []
                        for hook_config in hook_configs:
                            # 更新Python命令
                            if "command" in hook_config:
                                # 替换Python命令
                                old_command = hook_config["command"]
                                hook_config["command"] = old_command.replace(
                                    "python39", python_cmd
                                ).replace(
                                    "python3.9", python_cmd
                                ).replace(
                                    "python3", python_cmd
                                )
                            if hook_config not in settings["hooks"][hook_type]:
                                settings["hooks"][hook_type].append(hook_config)

    # 保存settings
    with open(settings_file, "w", encoding="utf-8") as f:
        json.dump(settings, ensure_ascii=False, indent=2)

    print("\\n" + "=" * 70)
    print("[成功] 组件安装完成!")
    print(f"配置已更新: {{settings_file}}")
    print(f"使用Python命令: {{python_cmd}}")
    print("=" * 70)


if __name__ == "__main__":
    install()
'''

        install_script.write_text(script_content, encoding="utf-8")

    def get_install_command(self, package_dir: Path, target_project: str = ".") -> str:
        """获取安装命令"""
        relative_path = package_dir.relative_to(self.project_dir)
        if target_project == ".":
            return f"python {relative_path}/install.py"
        else:
            return f"cd {target_project} && python ../{relative_path}/install.py"


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="Claude Code 组件打包工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 按组件类型打包
  python pack_skills.py              # 打包 skills（默认）
  python pack_skills.py -t skills    # 打包 skills
  python pack_skills.py -t hooks     # 打包 hooks
  python pack_skills.py -t agents    # 打包 agents
  python pack_skills.py -t commands  # 打包 commands
  python pack_skills.py -t all       # 打包所有组件

  # 按功能打包（推荐）
  python pack_skills.py -f           # 按功能打包
  python pack_skills.py --function   # 按功能打包

  # 指定Python版本
  python pack_skills.py -f           # 交互时输入Python命令
        """
    )
    parser.add_argument(
        "-t", "--type",
        choices=["skills", "hooks", "agents", "commands", "all", "function"],
        default="skills",
        help="组件类型或'function'按功能打包 (默认: skills)"
    )
    parser.add_argument(
        "-f", "--function",
        action="store_true",
        help="按功能打包（会列出所有可用功能供选择）"
    )
    parser.add_argument(
        "-o", "--output",
        help="输出包名称"
    )
    parser.add_argument(
        "--non-interactive",
        action="store_true",
        help="非交互模式（需要配合 --output 使用）"
    )
    return parser.parse_args()


def main():
    """主函数"""
    args = parse_arguments()

    # 获取项目目录
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent.parent.parent

    # 判断是否按功能打包
    if args.function or args.type == "function":
        print("=" * 80)
        print("Claude Code 组件打包工具 - 按功能打包".center(80))
        print("=" * 80)

        packager = ComponentPackager(project_dir, "function")

        # 选择功能
        function_key = packager.select_function()
        if not function_key:
            print("[信息] 未选择任何功能，退出")
            return 0

        # 获取功能配置
        function_config = packager.functions_config.get("functions", {}).get(function_key, {})
        function_name = function_config.get("name", function_key)

        # 发现该功能的所有组件
        components = packager.discover_function_components(function_key)
        if not components:
            print(f"[错误] 功能 '{function_key}' 没有找到任何组件，退出")
            return 1

        # 显示发现的组件
        print(f"\n功能 '{function_name}' 包含以下组件:")
        for comp in components:
            comp_type = comp.get('type', 'unknown')
            print(f"  [{comp_type}] {comp['name']}: {comp['description']}")

        # 确认
        if not args.non_interactive:
            try:
                confirm = input("\n确认打包? (y/n): ").strip().lower()
                if confirm != "y":
                    print("[信息] 已取消")
                    return 0
            except (EOFError, KeyboardInterrupt):
                print("\n[信息] 已取消")
                return 0

        # 获取Python命令
        python_cmd = packager.prompt_python_command()
        packager.set_python_command(python_cmd)

        # 生成输出包名
        output_name = args.output or f"ccscaffold-function-{function_key}"

        # 创建包
        package_dir = packager.create_package(components, output_name)
        if package_dir:
            print("\n" + "=" * 80)
            print("打包完成!".center(80))
            print("=" * 80)
            print(f"\n功能: {function_name} ({function_key})")
            print(f"Python命令: {python_cmd}")
            print("\n安装命令:")
            print(f"  {python_cmd} {package_dir.relative_to(project_dir)}/install.py")
            print("\n或复制到其他项目后运行:")
            print(f"  {python_cmd} <package>/install.py")
            print("=" * 80)

    else:
        # 按组件类型打包
        print("=" * 80)
        print(f"Claude Code 组件打包工具 - 打包 {args.type}".center(80))
        print("=" * 80)

        packager = ComponentPackager(project_dir, args.type)

        # 发现组件
        components = packager.discover_components()
        if not components:
            print(f"[错误] 未找到任何 {args.type} 组件，退出")
            return 1

        # 选择组件
        if args.non_interactive:
            selected = components
        else:
            selected = packager.select_components(components)

        if not selected:
            print("[信息] 未选择任何组件，退出")
            return 0

        # 显示选择的组件
        print(f"\n已选择 {len(selected)} 个组件:")
        for comp in selected:
            comp_type = comp.get('type', args.type)
            print(f"  [{comp_type}] {comp['name']}: {comp['description']}")

        # 确认
        if not args.non_interactive:
            try:
                confirm = input("\n确认打包? (y/n): ").strip().lower()
                if confirm != "y":
                    print("[信息] 已取消")
                    return 0
            except (EOFError, KeyboardInterrupt):
                print("\n[信息] 已取消")
                return 0

        # 获取Python命令
        python_cmd = packager.prompt_python_command()
        packager.set_python_command(python_cmd)

        # 创建包
        package_dir = packager.create_package(selected, args.output)
        if package_dir:
            print("\n" + "=" * 80)
            print("打包完成!".center(80))
            print("=" * 80)
            print(f"\nPython命令: {python_cmd}")
            print("\n安装命令:")
            print(f"  {python_cmd} {package_dir.relative_to(project_dir)}/install.py")
            print("\n或复制到其他项目后运行:")
            print(f"  {python_cmd} <package>/install.py")
            print("=" * 80)

    return 0


if __name__ == "__main__":
    sys.exit(main())
