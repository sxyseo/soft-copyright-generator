#!/usr/bin/env python3
"""
macOS应用程序打包脚本
使用PyInstaller将软著代码生成器打包成.app文件
"""

import os
import sys
import subprocess
import shutil

def build_macos_app():
    """打包macOS .app文件"""
    print("开始打包macOS应用程序...")
    
    # PyInstaller命令
    cmd = [
        'pyinstaller',
        '--onefile',                    # 打包成单个文件
        '--windowed',                   # 创建.app bundle
        '--name=软著代码生成器',          # 应用程序名称
        '--icon=app_icon.icns',         # macOS图标文件（如果有）
        '--add-data=soft_copyright_generator.py:.',  # 包含生成器模块（macOS用冒号）
        'soft_copyright_gui_v1.py'      # 主程序文件
    ]
    
    try:
        # 执行打包命令
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ macOS应用程序打包成功！")
        print(f"输出文件: dist/软著代码生成器.app")
        
        # 清理临时文件
        cleanup_build_files()
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 打包失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False
    except FileNotFoundError:
        print("❌ PyInstaller未安装，请先运行: pip install pyinstaller")
        return False
    
    return True

def cleanup_build_files():
    """清理打包过程中产生的临时文件"""
    dirs_to_remove = ['build', '__pycache__']
    files_to_remove = ['软著代码生成器.spec']
    
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"已清理: {dir_name}")
    
    for file_name in files_to_remove:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"已清理: {file_name}")

def create_dmg():
    """创建macOS安装包(.dmg文件)"""
    print("创建dmg安装包...")
    
    app_name = "软著代码生成器"
    dmg_name = f"{app_name}.dmg"
    
    cmd = [
        'hdiutil', 'create', '-volname', app_name,
        '-srcfolder', f'dist/{app_name}.app',
        '-ov', '-format', 'UDZO', dmg_name
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"✅ DMG文件创建成功: {dmg_name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ DMG创建失败: {e}")
        return False
    except FileNotFoundError:
        print("⚠️  hdiutil命令不可用，跳过DMG创建")
        return False

if __name__ == "__main__":
    print("软著代码生成器 - macOS打包工具")
    print("=" * 50)
    
    # 检查必要文件
    required_files = ['soft_copyright_gui_v1.py', 'soft_copyright_generator.py']
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"❌ 缺少必要文件: {missing_files}")
        sys.exit(1)
    
    # 开始打包
    success = build_macos_app()
    
    if success:
        print("\n🎉 应用程序打包完成！")
        print("生成的.app文件位于 dist/ 目录下")
        
        # 询问是否创建DMG
        create_dmg_choice = input("\n是否创建DMG安装包? (y/n): ").lower().strip()
        if create_dmg_choice == 'y':
            create_dmg()
    else:
        print("\n💥 打包失败，请检查错误信息")
        sys.exit(1) 