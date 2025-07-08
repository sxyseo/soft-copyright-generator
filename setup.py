#!/usr/bin/env python3
"""
软著代码生成器 - 安装配置
"""

from setuptools import setup, find_packages
import os

# 读取README文件
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "软著代码生成器 - 从源代码生成软件著作权申请所需的代码文档"

setup(
    name="软著代码生成器",
    version="1.0.0",
    author="Developer",
    author_email="developer@example.com",
    description="从源代码生成软件著作权申请所需的代码文档",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/soft-copyright-generator",
    packages=find_packages(),
    py_modules=['soft_copyright_generator', 'soft_copyright_gui_v1'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Documentation",
        "Topic :: Text Processing :: Markup",
    ],
    python_requires=">=3.8",
    install_requires=[
        "PySide6>=6.4.0",
        "python-docx>=0.8.11",
    ],
    extras_require={
        "build": [
            "pyinstaller>=5.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "软著代码生成器=soft_copyright_gui_v1:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.ico", "*.icns", "*.png"],
    },
) 