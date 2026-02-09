# [PROJECT NAME] Development Guidelines

Auto-generated from all feature plans. Last updated: [DATE]

## Active Technologies

[EXTRACTED FROM ALL PLAN.MD FILES]

## Project Structure

```text
[ACTUAL STRUCTURE FROM PLANS]
```

## Commands

[ONLY COMMANDS FOR ACTIVE TECHNOLOGIES]

## Code Style

[LANGUAGE-SPECIFIC, ONLY FOR LANGUAGES IN USE]

### Universal Standards (All Languages)

- **临时文件路径**: 所有临时文件必须使用 `.claude/tmp/` 目录结构
  - 对话记录: `.claude/tmp/conversations/`
  - 缓存数据: `.claude/tmp/cache/`
  - 临时脚本: `.claude/tmp/scripts/`
  - 文件命名格式: `{功能名}-{timestamp}.{扩展名}`

- **文档规范**:
  - 所有 Markdown 文档必须放在 `docs/` 目录
  - 文档使用中文编写
  - 脚本文件使用英文命名

- **Python 特定**:
  - 兼容 Python 3.9+
  - 使用 `python39` 或 `python3.9` 运行
  - 禁止特殊 Unicode 字符,仅使用 ASCII 字符集
  - 文件编码: UTF-8 (不含特殊字符)

- **跨平台可移植性优先原则**:
  - **强制支持平台**: Windows、Linux、macOS
  - **优先级排序**: 可移植性 > 性能 > 开发便利性
  - **默认实现**: 使用跨平台的通用解决方案
  - **文件路径**: 必须使用跨平台库 (pathlib, tempfile 等)
  - **平台优化**: 仅在性能提升超过 30% 时才考虑平台特定实现
  - **回退机制**: 平台特定代码必须有回退到跨平台实现的逻辑
  - **交互模式**: 移植工具必须提供交互式平台选择
  - **测试覆盖**: 每个功能必须在三个平台上进行测试

- **组件自包含**:
  - 每个 skill/hook/agent/command 必须自包含
  - 明确声明依赖关系
  - 可独立打包和分发

- **README 强制要求**:
  - 每个功能组件必须包含 README.md
  - README 必须使用中文编写
  - 必须包含: 功能说明、使用方法、配置说明、依赖关系、注意事项
  - 文档必须与代码实现保持同步
  - 必须说明平台兼容性和限制

## Recent Changes

[LAST 3 FEATURES AND WHAT THEY ADDED]

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
