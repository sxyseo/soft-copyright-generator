# 软著代码生成器

一个用于生成软件著作权申请所需代码文档的GUI工具。

## 功能特点

- 🎯 **智能代码扫描**：自动扫描源代码目录，支持多种编程语言
- 📄 **标准格式输出**：生成符合软著申请要求的Word文档
- 🔄 **批量生成**：支持生成多个不重复的代码文档
- 🎨 **用户友好界面**：基于PySide6的现代GUI界面
- ⚙️ **灵活配置**：可自定义文档页数、项目名称等参数

## 支持的编程语言

- Python (.py)
- JavaScript (.js)
- TypeScript (.ts)
- Java (.java)
- HTML (.html)
- CSS (.css)

## 系统要求

- Python 3.8+
- Windows 10+ / macOS 10.14+
- 内存: 至少 512MB
- 磁盘空间: 至少 100MB

## 安装方法

### 方法1: 使用预编译程序（推荐）

1. 下载对应系统的可执行文件：
   - Windows: `软著代码生成器.exe`
   - macOS: `软著代码生成器.app`

2. 直接运行即可使用

### 方法2: 从源码安装

```bash
# 克隆项目
git clone https://github.com/yourusername/soft-copyright-generator
cd soft-copyright-generator

# 安装依赖
pip install -r requirements.txt

# 运行程序
python soft_copyright_gui_v1.py
```

## 使用说明

1. **选择源代码路径**：点击"浏览"按钮选择包含源代码的文件夹
2. **选择输出路径**：选择生成文档的保存位置
3. **设置参数**：
   - 文档数量：需要生成几份不同的文档
   - 项目名称：软件或系统的名称
   - 每个文档页数：控制每份文档的页数（5-100页）
4. **点击生成**：开始生成软著代码文档

## 打包说明

### Windows exe打包

```bash
# 安装打包依赖
pip install pyinstaller

# 执行打包脚本
python build_exe.py
```

生成的exe文件位于 `dist/` 目录下。

### macOS 应用程序打包

```bash
# 安装打包依赖
pip install pyinstaller

# 执行打包脚本
python build_macos.py
```

生成的.app文件位于 `dist/` 目录下。

## 文件命名规则

生成的文档按以下格式命名：
- 单个文档：`源码 - 项目名称.docx`
- 多个文档：`源码 - 项目名称 (1).docx`, `源码 - 项目名称 (2).docx` ...

## 技术栈

- **GUI框架**: PySide6
- **文档生成**: python-docx
- **打包工具**: PyInstaller
- **语言**: Python 3.8+

## 许可证

MIT License

## 支持与反馈

如有问题或建议，请提交Issue或联系开发者。

---

© 2024 软著代码生成器. All rights reserved. 