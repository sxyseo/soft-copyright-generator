#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
软著代码生成器工程文件功能演示
展示如何使用工程文件保存和加载配置
"""

import sys
import os
from PySide6.QtWidgets import QApplication, QMessageBox
from soft_copyright_gui_v1 import SoftCodeGeneratorApp

def demo_project_file_usage():
    """演示工程文件功能"""
    print("=== 软著代码生成器工程文件功能演示 ===\n")
    
    # 创建应用程序
    app = QApplication(sys.argv)
    
    # 创建主窗口
    generator_app = SoftCodeGeneratorApp()
    generator_app.show()
    
    # 显示使用说明
    usage_info = """
🎯 工程文件功能使用指南

📁 工程文件功能特性：
• 保存所有配置到 .scproj 文件
• 支持单个模式和批量模式设置
• 自动跟踪修改状态（窗口标题显示 * 表示有未保存修改）
• 加载工程文件时自动恢复所有设置

🛠️ 菜单操作：
• 文件 -> 新建工程 (Ctrl+N): 创建新的空白工程
• 文件 -> 打开工程 (Ctrl+O): 加载现有工程文件
• 文件 -> 保存工程 (Ctrl+S): 保存当前工程
• 文件 -> 另存为 (Ctrl+Shift+S): 另存工程文件

📋 配置信息包含：
• 单个模式：源码路径、输出路径、项目名称、文档数量、页数设置、来源显示
• 批量模式：多个项目配置、各项目的源码路径列表、输出目录、全局设置
• 界面状态：当前选中的模式（单个/批量）

💡 使用建议：
1. 首次使用时配置好所有设置，然后保存为工程文件
2. 每次需要生成软著文档时，直接加载工程文件即可
3. 如有调整，修改后重新保存工程文件
4. 可以为不同项目创建不同的工程文件

📝 示例工程文件：
项目中包含 example_project.scproj 文件，展示了完整的配置结构
    """
    
    # 显示使用说明对话框
    QMessageBox.information(generator_app, "工程文件功能演示", usage_info)
    
    # 如果存在示例工程文件，询问是否加载
    example_file = "example_project.scproj"
    if os.path.exists(example_file):
        reply = QMessageBox.question(
            generator_app, 
            "加载示例工程",
            f"发现示例工程文件 {example_file}，是否加载查看？\n\n"
            "这将展示工程文件的完整配置结构。",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                generator_app.load_project_file(example_file)
                generator_app.current_project_file = example_file
                generator_app.is_modified = False
                generator_app.update_window_title()
                
                QMessageBox.information(
                    generator_app,
                    "示例工程已加载",
                    "✅ 示例工程配置已成功加载！\n\n"
                    "你可以看到：\n"
                    "• 单个模式中配置了'智慧医疗管理系统'项目\n"
                    "• 批量模式中包含3个子模块项目\n"
                    "• 当前处于批量模式\n\n"
                    "可以尝试修改配置，然后使用菜单保存工程文件。"
                )
            except Exception as e:
                QMessageBox.critical(
                    generator_app,
                    "加载失败",
                    f"示例工程文件加载失败：\n{str(e)}"
                )
    
    # 运行应用程序
    print("🚀 应用程序已启动，请在GUI中体验工程文件功能...")
    print("\n📋 操作提示：")
    print("1. 查看菜单栏中的'文件'菜单")
    print("2. 尝试修改配置，观察窗口标题的变化")
    print("3. 使用快捷键快速操作：")
    print("   - Ctrl+N: 新建工程")
    print("   - Ctrl+O: 打开工程")
    print("   - Ctrl+S: 保存工程")
    print("   - Ctrl+Shift+S: 另存为")
    print("\n✨ 关闭窗口时，如有未保存的修改会自动提醒！")
    
    return app.exec()

def main():
    """主函数"""
    try:
        return demo_project_file_usage()
    except Exception as e:
        print(f"❌ 演示运行失败: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main()) 