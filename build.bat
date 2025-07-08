@echo off
chcp 65001 >nul
echo 🚀 软著代码生成器 - Windows打包工具
echo =======================================
echo.

:: 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python未安装或未添加到PATH
    echo 请先安装Python 3.8或更高版本
    pause
    exit /b 1
)

:: 检查必要文件
if not exist "soft_copyright_gui_v1.py" (
    echo ❌ 找不到 soft_copyright_gui_v1.py
    pause
    exit /b 1
)

if not exist "soft_copyright_generator.py" (
    echo ❌ 找不到 soft_copyright_generator.py
    pause
    exit /b 1
)

:: 运行打包脚本
echo 📦 开始打包...
python build.py

echo.
echo 打包完成！按任意键退出...
pause >nul 