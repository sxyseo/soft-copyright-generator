#!/usr/bin/env python3
"""
跨平台打包脚本
自动检测平台并执行相应的打包命令
"""

import os
import sys
import platform
import subprocess
import shutil

def get_platform():
    """检测当前平台"""
    system = platform.system().lower()
    if system == 'windows':
        return 'windows'
    elif system == 'darwin':
        return 'macos'
    elif system == 'linux':
        return 'linux'
    else:
        return 'unknown'

def install_dependencies():
    """安装打包依赖"""
    print("📦 安装打包依赖...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], check=True)
        print("✅ 依赖安装成功")
        return True
    except subprocess.CalledProcessError:
        print("❌ 依赖安装失败")
        return False

def build_windows():
    """Windows平台打包"""
    print("🪟 开始打包Windows应用程序...")
    
    cmd = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        '--name=软著代码生成器',
        '--add-data=soft_copyright_generator.py;.',
        'soft_copyright_gui_v1.py'
    ]
    
    # 如果存在图标文件，添加图标
    if os.path.exists('app_icon.ico'):
        cmd.append('--icon=app_icon.ico')
    
    return run_pyinstaller(cmd)

def build_macos():
    """macOS平台打包"""
    print("🍎 开始打包macOS应用程序...")
    
    cmd = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        '--name=软著代码生成器',
        '--add-data=soft_copyright_generator.py:.',
        'soft_copyright_gui_v1.py'
    ]
    
    # 如果存在图标文件，添加图标
    if os.path.exists('app_icon.icns'):
        cmd.append('--icon=app_icon.icns')
    
    return run_pyinstaller(cmd)

def build_linux():
    """Linux平台打包"""
    print("🐧 开始打包Linux应用程序...")
    
    cmd = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        '--name=软著代码生成器',
        '--add-data=soft_copyright_generator.py:.',
        'soft_copyright_gui_v1.py'
    ]
    
    # 如果存在图标文件，添加图标
    if os.path.exists('app_icon.png'):
        cmd.append('--icon=app_icon.png')
    
    return run_pyinstaller(cmd)

def run_pyinstaller(cmd):
    """执行PyInstaller命令"""
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ 打包成功！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 打包失败: {e}")
        if e.stderr:
            print(f"错误信息: {e.stderr}")
        return False
    except FileNotFoundError:
        print("❌ PyInstaller未找到，请先安装")
        return False

def cleanup():
    """清理临时文件"""
    print("🧹 清理临时文件...")
    
    dirs_to_remove = ['build', '__pycache__']
    files_to_remove = ['软著代码生成器.spec']
    
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"  已清理: {dir_name}")
    
    for file_name in files_to_remove:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"  已清理: {file_name}")

def main():
    """主函数"""
    print("🚀 软著代码生成器 - 跨平台打包工具")
    print("=" * 50)
    
    # 检测平台
    current_platform = get_platform()
    print(f"🔍 检测到平台: {current_platform}")
    
    if current_platform == 'unknown':
        print("❌ 不支持的平台")
        sys.exit(1)
    
    # 检查必要文件
    required_files = ['soft_copyright_gui_v1.py', 'soft_copyright_generator.py']
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"❌ 缺少必要文件: {missing_files}")
        sys.exit(1)
    
    # 安装依赖
    if not install_dependencies():
        sys.exit(1)
    
    # 根据平台执行打包
    success = False
    if current_platform == 'windows':
        success = build_windows()
    elif current_platform == 'macos':
        success = build_macos()
    elif current_platform == 'linux':
        success = build_linux()
    
    # 清理临时文件
    cleanup()
    
    # 显示结果
    if success:
        print("\n🎉 打包完成！")
        print(f"📁 输出文件位于: dist/")
        
        # 显示生成的文件
        dist_path = "dist"
        if os.path.exists(dist_path):
            files = os.listdir(dist_path)
            if files:
                print("📄 生成的文件:")
                for file in files:
                    print(f"  - {file}")
    else:
        print("\n💥 打包失败")
        sys.exit(1)

if __name__ == "__main__":
    main() 