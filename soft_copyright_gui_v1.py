import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFileDialog, QSpinBox, QMessageBox, QCheckBox
)
from PySide6.QtCore import Qt

# 导入之前实现的软著生成函数（需确保在同一目录）
from soft_copyright_generator import generate_multiple_docs

class SoftCodeGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("软著代码文档生成器")
        self.setGeometry(200, 200, 600, 330)
        
        # 创建主部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setAlignment(Qt.AlignTop)
        
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
        self.count_spin.setValue(3)
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
        
        # 添加到主布局
        main_layout.addLayout(source_layout)
        main_layout.addLayout(output_layout)
        main_layout.addLayout(count_layout)
        main_layout.addLayout(name_layout)
        main_layout.addLayout(pages_layout)
        main_layout.addLayout(source_display_layout)
        main_layout.addWidget(generate_btn)

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

def main():
    """主函数，用作程序入口点"""
    app = QApplication(sys.argv)
    window = SoftCodeGeneratorApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()