import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFileDialog, QSpinBox, QMessageBox, QCheckBox,
    QTabWidget, QListWidget, QListWidgetItem, QSplitter, QFrame, QGroupBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView
)
from PySide6.QtCore import Qt

# 导入之前实现的软著生成函数（需确保在同一目录）
from soft_copyright_generator import generate_multiple_docs

class SoftCodeGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("软著代码文档生成器")
        self.setGeometry(200, 200, 800, 600)
        
        # 批量模式数据存储
        self.batch_projects = []
        self.current_project_index = -1
        
        # 创建主部件和标签页
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # 创建标签页控件
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # 创建单个模式标签页
        self.create_single_mode_tab()
        
        # 创建批量模式标签页
        self.create_batch_mode_tab()
    
    def create_single_mode_tab(self):
        """创建单个模式标签页"""
        single_widget = QWidget()
        self.tab_widget.addTab(single_widget, "单个模式")
        
        layout = QVBoxLayout(single_widget)
        layout.setAlignment(Qt.AlignTop)
        
        # 1. 源代码路径选择
        source_layout = QHBoxLayout()
        source_label = QLabel("源代码路径:")
        self.source_edit = QLineEdit()
        self.source_edit.setPlaceholderText("选择源代码目录...")
        browse_source_btn = QPushButton("浏览")
        browse_source_btn.clicked.connect(self.browse_source)
        source_layout.addWidget(source_label)
        source_layout.addWidget(self.source_edit)
        source_layout.addWidget(browse_source_btn)
        
        # 2. 输出路径选择
        output_layout = QHBoxLayout()
        output_label = QLabel("输出路径:")
        self.output_edit = QLineEdit()
        self.output_edit.setPlaceholderText("选择输出目录...")
        browse_output_btn = QPushButton("浏览")
        browse_output_btn.clicked.connect(self.browse_output)
        output_layout.addWidget(output_label)
        output_layout.addWidget(self.output_edit)
        output_layout.addWidget(browse_output_btn)
        
        # 3. 文档数量设置
        count_layout = QHBoxLayout()
        count_label = QLabel("文档数量:")
        self.count_spin = QSpinBox()
        self.count_spin.setRange(1, 100)
        self.count_spin.setValue(1)
        count_layout.addWidget(count_label)
        count_layout.addWidget(self.count_spin)
        count_layout.addStretch()
        
        # 4. 项目名称设置
        name_layout = QHBoxLayout()
        name_label = QLabel("项目名称:")
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("输入项目/系统名称")
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_edit)
        
        # 5. 页数设置
        pages_layout = QHBoxLayout()
        pages_label = QLabel("每个文档页数:")
        self.pages_spin = QSpinBox()
        self.pages_spin.setRange(5, 100)
        self.pages_spin.setValue(30)
        pages_layout.addWidget(pages_label)
        pages_layout.addWidget(self.pages_spin)
        pages_layout.addStretch()
        
        # 6. 显示来源开关
        source_display_layout = QHBoxLayout()
        self.show_source_checkbox = QCheckBox("显示文件来源信息")
        self.show_source_checkbox.setChecked(False)  # 默认不显示
        self.show_source_checkbox.setToolTip("在生成的文档中显示代码来源文件信息")
        source_display_layout.addWidget(self.show_source_checkbox)
        source_display_layout.addStretch()
        
        # 7. 生成按钮
        generate_btn = QPushButton("生成文档")
        generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        generate_btn.clicked.connect(self.generate_docs)
        
        # 添加到单个模式布局
        layout.addLayout(source_layout)
        layout.addLayout(output_layout)
        layout.addLayout(count_layout)
        layout.addLayout(name_layout)
        layout.addLayout(pages_layout)
        layout.addLayout(source_display_layout)
        layout.addWidget(generate_btn)
    
    def create_batch_mode_tab(self):
        """创建批量模式标签页"""
        batch_widget = QWidget()
        self.tab_widget.addTab(batch_widget, "批量模式")
        
        main_layout = QVBoxLayout(batch_widget)
        
        # 创建分割器（左右分割）
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # 左侧：项目列表
        left_frame = QFrame()
        left_layout = QVBoxLayout(left_frame)
        
        # 项目列表标题和按钮
        project_header_layout = QHBoxLayout()
        project_label = QLabel("项目列表:")
        project_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        add_project_btn = QPushButton("添加项目")
        remove_project_btn = QPushButton("删除项目")
        
        add_project_btn.clicked.connect(self.add_project)
        remove_project_btn.clicked.connect(self.remove_project)
        
        project_header_layout.addWidget(project_label)
        project_header_layout.addStretch()
        project_header_layout.addWidget(add_project_btn)
        project_header_layout.addWidget(remove_project_btn)
        
        # 项目列表
        self.project_list = QListWidget()
        self.project_list.currentRowChanged.connect(self.on_project_selected)
        
        left_layout.addLayout(project_header_layout)
        left_layout.addWidget(self.project_list)
        
        # 右侧：项目详情
        right_frame = QFrame()
        right_layout = QVBoxLayout(right_frame)
        
        # 项目详情标题
        detail_label = QLabel("项目详情:")
        detail_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        right_layout.addWidget(detail_label)
        
        # 项目名称
        name_group = QGroupBox("项目名称")
        name_layout = QHBoxLayout(name_group)
        self.batch_name_edit = QLineEdit()
        self.batch_name_edit.setPlaceholderText("输入项目/系统名称")
        self.batch_name_edit.textChanged.connect(self.update_current_project)
        name_layout.addWidget(self.batch_name_edit)
        right_layout.addWidget(name_group)
        
        # 源代码路径列表
        paths_group = QGroupBox("源代码路径")
        paths_layout = QVBoxLayout(paths_group)
        
        # 路径列表操作按钮
        path_btn_layout = QHBoxLayout()
        add_path_btn = QPushButton("添加路径")
        remove_path_btn = QPushButton("删除路径")
        add_path_btn.clicked.connect(self.add_source_path)
        remove_path_btn.clicked.connect(self.remove_source_path)
        path_btn_layout.addWidget(add_path_btn)
        path_btn_layout.addWidget(remove_path_btn)
        path_btn_layout.addStretch()
        
        # 路径列表
        self.source_paths_list = QListWidget()
        
        paths_layout.addLayout(path_btn_layout)
        paths_layout.addWidget(self.source_paths_list)
        right_layout.addWidget(paths_group)
        
        # 项目设置
        settings_group = QGroupBox("项目设置")
        settings_layout = QVBoxLayout(settings_group)
        
        # 文档数量
        doc_count_layout = QHBoxLayout()
        doc_count_label = QLabel("文档数量:")
        self.batch_doc_count_spin = QSpinBox()
        self.batch_doc_count_spin.setRange(1, 100)
        self.batch_doc_count_spin.setValue(1)
        self.batch_doc_count_spin.valueChanged.connect(self.update_current_project)
        doc_count_layout.addWidget(doc_count_label)
        doc_count_layout.addWidget(self.batch_doc_count_spin)
        doc_count_layout.addStretch()
        
        # 页数设置
        pages_layout = QHBoxLayout()
        pages_label = QLabel("每个文档页数:")
        self.batch_pages_spin = QSpinBox()
        self.batch_pages_spin.setRange(5, 100)
        self.batch_pages_spin.setValue(30)
        self.batch_pages_spin.valueChanged.connect(self.update_current_project)
        pages_layout.addWidget(pages_label)
        pages_layout.addWidget(self.batch_pages_spin)
        pages_layout.addStretch()
        
        settings_layout.addLayout(doc_count_layout)
        settings_layout.addLayout(pages_layout)
        right_layout.addWidget(settings_group)
        
        # 添加伸缩空间
        right_layout.addStretch()
        
        # 将左右两侧添加到分割器
        splitter.addWidget(left_frame)
        splitter.addWidget(right_frame)
        splitter.setStretchFactor(0, 1)  # 左侧占1份
        splitter.setStretchFactor(1, 2)  # 右侧占2份
        
        # 底部：全局设置和生成按钮
        bottom_layout = QVBoxLayout()
        
        # 全局设置
        global_group = QGroupBox("全局设置")
        global_layout = QVBoxLayout(global_group)
        
        # 输出路径
        output_layout = QHBoxLayout()
        output_label = QLabel("输出路径:")
        self.batch_output_edit = QLineEdit()
        self.batch_output_edit.setPlaceholderText("选择输出目录...")
        browse_output_btn = QPushButton("浏览")
        browse_output_btn.clicked.connect(self.browse_batch_output)
        output_layout.addWidget(output_label)
        output_layout.addWidget(self.batch_output_edit)
        output_layout.addWidget(browse_output_btn)
        
        # 显示来源开关
        self.batch_show_source_checkbox = QCheckBox("显示文件来源信息")
        self.batch_show_source_checkbox.setChecked(False)
        self.batch_show_source_checkbox.setToolTip("在生成的文档中显示代码来源文件信息")
        
        global_layout.addLayout(output_layout)
        global_layout.addWidget(self.batch_show_source_checkbox)
        
        # 批量生成按钮
        batch_generate_btn = QPushButton("批量生成文档")
        batch_generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                font-weight: bold;
                padding: 12px;
                border-radius: 6px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        batch_generate_btn.clicked.connect(self.batch_generate_docs)
        
        bottom_layout.addWidget(global_group)
        bottom_layout.addWidget(batch_generate_btn)
        
        main_layout.addLayout(bottom_layout)

    def browse_source(self):
        """选择源代码目录"""
        dir_path = QFileDialog.getExistingDirectory(self, "选择源代码目录")
        if dir_path:
            self.source_edit.setText(dir_path)

    def browse_output(self):
        """选择输出目录"""
        dir_path = QFileDialog.getExistingDirectory(self, "选择输出目录")
        if dir_path:
            self.output_edit.setText(dir_path)

    def generate_docs(self):
        """生成文档的核心函数"""
        # 获取输入参数
        source_dir = self.source_edit.text().strip()
        output_dir = self.output_edit.text().strip()
        doc_count = self.count_spin.value()
        project_name = self.name_edit.text().strip()
        pages_per_doc = self.pages_spin.value()
        show_source = self.show_source_checkbox.isChecked()
        
        # 验证输入
        if not all([source_dir, output_dir, project_name]):
            QMessageBox.warning(self, "输入错误", "请填写所有必填字段！")
            return
            
        if not os.path.isdir(source_dir):
            QMessageBox.warning(self, "路径错误", "源代码路径不存在或不是目录！")
            return
            
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        try:
            # 调用之前实现的生成函数
            generate_multiple_docs(
                source_dir=source_dir,
                output_dir=output_dir,
                doc_count=doc_count,
                software_name=project_name,
                version="1.0",
                pages=pages_per_doc,
                show_source=show_source
            )
            QMessageBox.information(
                self, 
                "生成成功",
                f"已成功生成 {doc_count} 份软著代码文档！\n"
                f"项目名称: {project_name}\n"
                f"每份文档: {pages_per_doc} 页\n"
                f"输出路径: {output_dir}"
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "生成错误",
                f"文档生成失败: {str(e)}"
            )

    # 批量模式相关方法
    def add_project(self):
        """添加新项目"""
        project_name = f"项目 {len(self.batch_projects) + 1}"
        new_project = {
            'name': project_name,
            'source_paths': [],
            'doc_count': 3,
            'pages': 30
        }
        self.batch_projects.append(new_project)
        
        # 添加到列表显示
        item = QListWidgetItem(project_name)
        self.project_list.addItem(item)
        
        # 选中新添加的项目
        self.project_list.setCurrentRow(len(self.batch_projects) - 1)
    
    def remove_project(self):
        """删除选中的项目"""
        current_row = self.project_list.currentRow()
        if current_row >= 0:
            # 从数据中删除
            del self.batch_projects[current_row]
            
            # 从列表中删除
            self.project_list.takeItem(current_row)
            
            # 更新当前项目索引
            if self.batch_projects:
                new_row = min(current_row, len(self.batch_projects) - 1)
                self.project_list.setCurrentRow(new_row)
            else:
                self.current_project_index = -1
                self.clear_project_details()
    
    def on_project_selected(self, row):
        """项目选择改变时的处理"""
        self.current_project_index = row
        if 0 <= row < len(self.batch_projects):
            self.load_project_details(self.batch_projects[row])
        else:
            self.clear_project_details()
    
    def load_project_details(self, project):
        """加载项目详情到右侧面板"""
        # 暂时断开信号连接，避免循环更新
        self.batch_name_edit.blockSignals(True)
        self.batch_doc_count_spin.blockSignals(True)
        self.batch_pages_spin.blockSignals(True)
        
        # 设置项目详情
        self.batch_name_edit.setText(project['name'])
        self.batch_doc_count_spin.setValue(project['doc_count'])
        self.batch_pages_spin.setValue(project['pages'])
        
        # 加载源代码路径列表
        self.source_paths_list.clear()
        for path in project['source_paths']:
            self.source_paths_list.addItem(path)
        
        # 重新连接信号
        self.batch_name_edit.blockSignals(False)
        self.batch_doc_count_spin.blockSignals(False)
        self.batch_pages_spin.blockSignals(False)
    
    def clear_project_details(self):
        """清空项目详情面板"""
        self.batch_name_edit.clear()
        self.batch_doc_count_spin.setValue(1)
        self.batch_pages_spin.setValue(30)
        self.source_paths_list.clear()
    
    def update_current_project(self):
        """更新当前选中项目的信息"""
        if 0 <= self.current_project_index < len(self.batch_projects):
            project = self.batch_projects[self.current_project_index]
            project['name'] = self.batch_name_edit.text()
            project['doc_count'] = self.batch_doc_count_spin.value()
            project['pages'] = self.batch_pages_spin.value()
            
            # 更新列表显示的项目名称
            item = self.project_list.item(self.current_project_index)
            if item:
                item.setText(project['name'])
    
    def add_source_path(self):
        """添加源代码路径"""
        if 0 <= self.current_project_index < len(self.batch_projects):
            dir_path = QFileDialog.getExistingDirectory(self, "选择源代码目录")
            if dir_path:
                project = self.batch_projects[self.current_project_index]
                if dir_path not in project['source_paths']:
                    project['source_paths'].append(dir_path)
                    self.source_paths_list.addItem(dir_path)
                else:
                    QMessageBox.warning(self, "路径重复", "该路径已存在！")
        else:
            QMessageBox.warning(self, "无选中项目", "请先选择一个项目！")
    
    def remove_source_path(self):
        """删除选中的源代码路径"""
        current_row = self.source_paths_list.currentRow()
        if current_row >= 0 and 0 <= self.current_project_index < len(self.batch_projects):
            project = self.batch_projects[self.current_project_index]
            del project['source_paths'][current_row]
            self.source_paths_list.takeItem(current_row)
    
    def browse_batch_output(self):
        """选择批量输出目录"""
        dir_path = QFileDialog.getExistingDirectory(self, "选择输出目录")
        if dir_path:
            self.batch_output_edit.setText(dir_path)
    
    def batch_generate_docs(self):
        """批量生成文档"""
        # 验证输入
        if not self.batch_projects:
            QMessageBox.warning(self, "无项目", "请至少添加一个项目！")
            return
        
        output_dir = self.batch_output_edit.text().strip()
        if not output_dir:
            QMessageBox.warning(self, "输出路径为空", "请选择输出目录！")
            return
        
        # 验证每个项目
        for i, project in enumerate(self.batch_projects):
            if not project['name'].strip():
                QMessageBox.warning(self, "项目名称为空", f"第 {i+1} 个项目的名称为空！")
                return
            if not project['source_paths']:
                QMessageBox.warning(self, "无源代码路径", f"项目 '{project['name']}' 没有源代码路径！")
                return
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        show_source = self.batch_show_source_checkbox.isChecked()
        
        try:
            total_docs = 0
            success_projects = []
            
            for project in self.batch_projects:
                project_name = project['name']
                source_paths = project['source_paths']
                doc_count = project['doc_count']
                pages = project['pages']
                
                # 为每个项目创建子目录
                project_output_dir = os.path.join(output_dir, project_name)
                
                try:
                    # 调用修改后的生成函数，支持多个源代码路径
                    self.generate_multiple_docs_from_paths(
                        source_paths=source_paths,
                        output_dir=project_output_dir,
                        doc_count=doc_count,
                        software_name=project_name,
                        version="1.0",
                        pages=pages,
                        show_source=show_source
                    )
                    total_docs += doc_count
                    success_projects.append(project_name)
                    
                except Exception as e:
                    QMessageBox.warning(
                        self, 
                        "项目生成失败", 
                        f"项目 '{project_name}' 生成失败:\n{str(e)}"
                    )
                    continue
            
            # 显示成功信息
            if success_projects:
                QMessageBox.information(
                    self,
                    "批量生成完成",
                    f"成功生成 {len(success_projects)} 个项目，共 {total_docs} 个文档\n"
                    f"成功的项目: {', '.join(success_projects)}\n"
                    f"输出路径: {output_dir}"
                )
            else:
                QMessageBox.critical(self, "批量生成失败", "所有项目都生成失败！")
                
        except Exception as e:
            QMessageBox.critical(self, "批量生成错误", f"批量生成过程中发生错误: {str(e)}")
    
    def generate_multiple_docs_from_paths(self, source_paths, output_dir, doc_count, software_name, version, pages, show_source):
        """从多个源代码路径生成文档"""
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        
        # 合并所有源代码路径的文件
        all_code_files = []
        for source_path in source_paths:
            if os.path.isdir(source_path):
                from soft_copyright_generator import scan_code_files
                files = scan_code_files(source_path)
                all_code_files.extend(files)
        
        if not all_code_files:
            raise FileNotFoundError(f"在指定的源代码路径中未找到支持的代码文件")
        
        # 调用原有的生成函数，但是传入合并后的文件列表
        generated_paths = []
        for i in range(1, doc_count + 1):
            if doc_count > 1:
                filename = f"源码 - {software_name} ({i}).docx"
            else:
                filename = f"源码 - {software_name}.docx"
            
            output_path = os.path.join(output_dir, filename)
            
            # 调用修改后的生成函数
            self.generate_doc_from_files(
                code_files=all_code_files,
                output_path=output_path,
                software_name=software_name,
                version=version,
                pages=pages,
                show_source=show_source
            )
            generated_paths.append(output_path)
            print(f"已生成文档: {filename}")
        
        return generated_paths
    
    def generate_doc_from_files(self, code_files, output_path, software_name, version, pages, show_source):
        """从文件列表生成单个文档（修改自原有函数）"""
        import random
        from docx import Document
        from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
        from docx.shared import Pt
        from soft_copyright_generator import preprocess_code, add_page_header_footer
        
        if not code_files:
            raise FileNotFoundError("未提供代码文件")
        
        doc = Document()
        # 设置基础样式（宋体小五）
        style = doc.styles['Normal']
        font = style.font
        font.name = '宋体'
        font.size = Pt(9)
        
        # 添加页眉页脚
        add_page_header_footer(doc, software_name, version)
        
        lines_accumulated = []
        files_used = set()
        
        # 随机打乱文件顺序确保不重复
        random.shuffle(code_files)
        
        # 收集足够的代码行
        for file_path in code_files:
            if len(lines_accumulated) >= pages * 50:
                break
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = preprocess_code(f.read())
                    lines = content.splitlines()
                    # 仅取非空行
                    lines = [line for line in lines if line.strip()]
                    lines_accumulated.extend(lines)
                    files_used.add(os.path.basename(file_path))
            except Exception as e:
                print(f"处理文件失败 {file_path}: {str(e)}")
        
        # 写入文档（每页50行）
        for page in range(pages):
            start_idx = page * 50
            end_idx = start_idx + 50
            
            if start_idx >= len(lines_accumulated):
                break
                
            # 根据设置决定是否添加文件名标签
            if show_source:
                doc.add_paragraph(f"// 来源: {', '.join(files_used)}", style='Intense Quote')
            
            # 添加代码行
            for line in lines_accumulated[start_idx:end_idx]:
                # 保留原始缩进
                p = doc.add_paragraph(line)
                p.style = doc.styles['Normal']
        
        doc.save(output_path)

def main():
    """主函数，用作程序入口点"""
    app = QApplication(sys.argv)
    window = SoftCodeGeneratorApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()