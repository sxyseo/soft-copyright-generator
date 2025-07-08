#!/bin/bash

echo "🚀 软著代码生成器 - macOS/Linux打包工具"
echo "======================================="
echo

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3未安装"
    echo "请先安装Python 3.8或更高版本"
    exit 1
fi

# 检查必要文件
if [ ! -f "soft_copyright_gui_v1.py" ]; then
    echo "❌ 找不到 soft_copyright_gui_v1.py"
    exit 1
fi

if [ ! -f "soft_copyright_generator.py" ]; then
    echo "❌ 找不到 soft_copyright_generator.py"
    exit 1
fi

# 运行打包脚本
echo "📦 开始打包..."
python3 build.py

echo
echo "✨ 打包完成！" 