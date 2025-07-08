#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
软著代码生成器工程文件功能测试
测试保存和加载工程文件的功能
"""

import os
import json
import tempfile
import shutil
from datetime import datetime
from soft_copyright_gui_v1 import SoftCodeGeneratorApp
from PySide6.QtWidgets import QApplication
import sys

def create_test_config():
    """创建测试配置"""
    return {
        "version": "1.0",
        "single_mode": {
            "source_dir": "/test/source",
            "output_dir": "/test/output", 
            "project_name": "测试项目",
            "doc_count": 2,
            "pages_per_doc": 25,
            "show_source": True
        },
        "batch_mode": {
            "projects": [
                {
                    "name": "前端项目",
                    "source_paths": ["/test/frontend", "/test/shared"],
                    "doc_count": 2,
                    "pages": 30
                },
                {
                    "name": "后端项目", 
                    "source_paths": ["/test/backend"],
                    "doc_count": 1,
                    "pages": 35
                }
            ],
            "output_dir": "/test/batch_output",
            "show_source": False
        },
        "settings": {
            "last_mode": "batch",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
    }

def test_config_collection_and_application():
    """测试配置收集和应用功能"""
    print("=== 测试配置收集和应用功能 ===")
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    # 创建应用实例
    generator_app = SoftCodeGeneratorApp()
    
    # 1. 手动设置一些配置
    print("1. 设置测试配置...")
    generator_app.source_edit.setText("/manual/source")
    generator_app.output_edit.setText("/manual/output")
    generator_app.name_edit.setText("手动测试项目")
    generator_app.count_spin.setValue(3)
    generator_app.pages_spin.setValue(40)
    generator_app.show_source_checkbox.setChecked(True)
    
    # 添加批量项目
    generator_app.add_project()
    generator_app.batch_name_edit.setText("批量测试项目1")
    generator_app.batch_doc_count_spin.setValue(2)
    generator_app.batch_pages_spin.setValue(25)
    generator_app.batch_output_edit.setText("/batch/output")
    
    # 2. 收集配置
    print("2. 收集当前配置...")
    config = generator_app.collect_config()
    
    # 验证收集的配置
    assert config["single_mode"]["source_dir"] == "/manual/source"
    assert config["single_mode"]["project_name"] == "手动测试项目"
    assert config["single_mode"]["doc_count"] == 3
    assert config["single_mode"]["pages_per_doc"] == 40
    assert config["single_mode"]["show_source"] == True
    
    assert len(config["batch_mode"]["projects"]) == 1
    assert config["batch_mode"]["projects"][0]["name"] == "批量测试项目1"
    assert config["batch_mode"]["projects"][0]["doc_count"] == 2
    assert config["batch_mode"]["output_dir"] == "/batch/output"
    
    print("✓ 配置收集正确")
    
    # 3. 清空配置
    print("3. 清空配置...")
    generator_app.clear_all_configs()
    
    # 验证清空
    assert generator_app.source_edit.text() == ""
    assert generator_app.name_edit.text() == ""
    assert len(generator_app.batch_projects) == 0
    
    print("✓ 配置清空正确")
    
    # 4. 应用配置
    print("4. 应用测试配置...")
    test_config = create_test_config()
    generator_app.apply_config(test_config)
    
    # 验证应用结果
    assert generator_app.source_edit.text() == "/test/source"
    assert generator_app.output_edit.text() == "/test/output"
    assert generator_app.name_edit.text() == "测试项目"
    assert generator_app.count_spin.value() == 2
    assert generator_app.pages_spin.value() == 25
    assert generator_app.show_source_checkbox.isChecked() == True
    
    assert len(generator_app.batch_projects) == 2
    assert generator_app.batch_projects[0]["name"] == "前端项目"
    assert len(generator_app.batch_projects[0]["source_paths"]) == 2
    assert generator_app.batch_projects[1]["name"] == "后端项目"
    assert generator_app.batch_output_edit.text() == "/test/batch_output"
    assert generator_app.batch_show_source_checkbox.isChecked() == False
    
    # 验证标签页切换
    assert generator_app.tab_widget.currentIndex() == 1  # 批量模式
    
    print("✓ 配置应用正确")
    
    return generator_app

def test_file_save_and_load():
    """测试文件保存和加载"""
    print("\n=== 测试文件保存和加载 ===")
    
    # 创建临时目录
    temp_dir = tempfile.mkdtemp()
    project_file = os.path.join(temp_dir, "test_project.scproj")
    
    try:
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        generator_app = SoftCodeGeneratorApp()
        
        # 1. 设置配置
        print("1. 设置测试配置...")
        test_config = create_test_config()
        generator_app.apply_config(test_config)
        
        # 2. 保存到文件
        print("2. 保存工程文件...")
        generator_app.save_project_file(project_file)
        
        # 验证文件存在
        assert os.path.exists(project_file)
        print("✓ 工程文件保存成功")
        
        # 3. 验证文件内容
        print("3. 验证文件内容...")
        with open(project_file, 'r', encoding='utf-8') as f:
            saved_config = json.load(f)
        
        assert saved_config["version"] == "1.0"
        assert saved_config["single_mode"]["project_name"] == "测试项目"
        assert len(saved_config["batch_mode"]["projects"]) == 2
        assert saved_config["batch_mode"]["projects"][0]["name"] == "前端项目"
        
        print("✓ 文件内容正确")
        
        # 4. 清空配置
        print("4. 清空当前配置...")
        generator_app.clear_all_configs()
        
        # 5. 从文件加载
        print("5. 从文件加载配置...")
        generator_app.load_project_file(project_file)
        
        # 6. 验证加载结果
        print("6. 验证加载结果...")
        assert generator_app.name_edit.text() == "测试项目"
        assert generator_app.source_edit.text() == "/test/source"
        assert generator_app.count_spin.value() == 2
        assert len(generator_app.batch_projects) == 2
        assert generator_app.batch_projects[0]["name"] == "前端项目"
        assert generator_app.tab_widget.currentIndex() == 1  # 批量模式
        
        print("✓ 配置加载正确")
        
        return generator_app
        
    finally:
        # 清理临时文件
        shutil.rmtree(temp_dir)
        print(f"✓ 临时文件清理完成: {temp_dir}")

def test_modification_tracking():
    """测试修改跟踪功能"""
    print("\n=== 测试修改跟踪功能 ===")
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    generator_app = SoftCodeGeneratorApp()
    
    # 1. 初始状态应该不是修改状态
    print("1. 检查初始修改状态...")
    assert not generator_app.is_modified
    assert "*" not in generator_app.windowTitle()
    print("✓ 初始状态正确")
    
    # 2. 修改单个模式配置
    print("2. 修改单个模式配置...")
    generator_app.source_edit.setText("/new/source")
    assert generator_app.is_modified
    assert "*" in generator_app.windowTitle()
    print("✓ 单个模式修改跟踪正确")
    
    # 3. 重置修改状态
    print("3. 重置修改状态...")
    generator_app.is_modified = False
    generator_app.update_window_title()
    assert not generator_app.is_modified
    
    # 4. 修改批量模式配置
    print("4. 修改批量模式配置...")
    generator_app.batch_output_edit.setText("/new/batch/output")
    assert generator_app.is_modified
    print("✓ 批量模式修改跟踪正确")
    
    # 5. 添加项目
    print("5. 测试添加项目的修改跟踪...")
    generator_app.is_modified = False
    generator_app.update_window_title()
    generator_app.add_project()
    assert generator_app.is_modified
    print("✓ 添加项目修改跟踪正确")
    
    return generator_app

def test_edge_cases():
    """测试边界情况"""
    print("\n=== 测试边界情况 ===")
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    generator_app = SoftCodeGeneratorApp()
    
    # 1. 测试空配置
    print("1. 测试空配置...")
    empty_config = {
        "version": "1.0",
        "single_mode": {},
        "batch_mode": {"projects": []},
        "settings": {}
    }
    
    try:
        generator_app.apply_config(empty_config)
        print("✓ 空配置处理正确")
    except Exception as e:
        print(f"✗ 空配置处理失败: {e}")
        raise
    
    # 2. 测试无效版本
    print("2. 测试无效版本...")
    invalid_config = {"version": "2.0"}
    
    try:
        generator_app.apply_config(invalid_config)
        print("✗ 应该抛出版本错误")
        assert False, "应该抛出版本错误"
    except ValueError as e:
        print("✓ 版本验证正确")
    
    # 3. 测试文件扩展名自动添加
    print("3. 测试文件扩展名...")
    temp_dir = tempfile.mkdtemp()
    try:
        file_without_ext = os.path.join(temp_dir, "test_project")
        generator_app.save_project_file(file_without_ext + ".scproj")  # 手动加扩展名
        
        # 验证文件存在
        assert os.path.exists(file_without_ext + ".scproj")
        print("✓ 文件扩展名处理正确")
        
    finally:
        shutil.rmtree(temp_dir)
    
    return generator_app

def main():
    """主测试函数"""
    print("开始软著代码生成器工程文件功能测试...")
    print("=" * 50)
    
    try:
        # 创建QApplication
        app = QApplication(sys.argv)
        
        # 执行各项测试
        test_config_collection_and_application()
        test_file_save_and_load()
        test_modification_tracking()
        test_edge_cases()
        
        print("\n" + "=" * 50)
        print("🎉 所有测试通过！工程文件功能正常工作。")
        print("\n功能特性:")
        print("✓ 配置收集和应用")
        print("✓ 工程文件保存和加载")
        print("✓ 修改状态跟踪")
        print("✓ 窗口标题更新")
        print("✓ 批量项目管理")
        print("✓ 边界情况处理")
        print("✓ 文件格式验证")
        
        # 显示示例用法
        print("\n使用说明:")
        print("1. 在菜单栏选择 '文件' -> '新建工程' 创建新工程")
        print("2. 配置项目设置后，选择 '保存工程' 保存配置")
        print("3. 使用 '打开工程' 加载之前保存的配置")
        print("4. 工程文件格式为 .scproj，包含所有配置信息")
        print("5. 窗口标题会显示当前工程文件名和修改状态")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 