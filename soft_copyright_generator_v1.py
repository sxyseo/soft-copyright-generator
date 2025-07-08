import os
import random
import re
from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def scan_code_files(source_dir, extensions=['.py', '.js', '.ts', '.java', '.html', '.css']):
    """扫描源代码目录并过滤有效文件"""
    code_files = []
    skip_dirs = {'node_modules', '.git', '__pycache__', 'build', 'dist', 'venv', '.idea'}
    
    for root, dirs, files in os.walk(source_dir):
        dirs[:] = [d for d in dirs if d not in skip_dirs]  # 跳过指定目录
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                code_files.append(os.path.join(root, file))
    return code_files

def preprocess_code(content):
    """预处理代码：移除注释和空行"""
    content = re.sub(r'//.*|#.*', '', content)  # 移除单行注释
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)  # 移除多行注释
    return os.linesep.join([s for s in content.splitlines() if s.strip()])  # 移除空行

def add_page_header_footer(doc, software_name, version):
    """添加页眉（软件名+版本）和页脚（页码）"""
    # 页眉
    header = doc.sections[0].header
    header_para = header.paragraphs[0]
    header_para.text = f"{software_name} v{version}"
    header_para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    
    # 页脚（页码）
    footer = doc.sections[0].footer
    paragraph = footer.paragraphs[0]
    paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT
    run = paragraph.add_run()
    # 创建页码字段（XML操作）
    fld_char = OxmlElement('w:fldChar')
    fld_char.set(qn('w:fldCharType'), 'begin')
    instr_text = OxmlElement('w:instrText')
    instr_text.set(qn('xml:space'), 'preserve')
    instr_text.text = 'PAGE'
    fld_char2 = OxmlElement('w:fldChar')
    fld_char2.set(qn('w:fldCharType'), 'end')
    run._r.append(fld_char)
    run._r.append(instr_text)
    run._r.append(fld_char2)

def generate_doc(source_dir, output_path, software_name, version, pages=30):
    """生成单个代码文档"""
    code_files = scan_code_files(source_dir)
    if not code_files:
        raise FileNotFoundError("未找到支持的源代码文件")
    
    doc = Document()
    # 设置全局样式：宋体9号（软著标准）
    style = doc.styles['Normal']
    style.font.name = '宋体'
    style.font.size = Pt(9)
    add_page_header_footer(doc, software_name, version)  # 添加页眉页脚
    
    # 收集代码行（打乱文件顺序保证随机性）
    random.shuffle(code_files)
    lines_accumulated = []
    for file_path in code_files:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = preprocess_code(f.read())
                lines_accumulated.extend([line for line in content.splitlines() if line])
        except Exception as e:
            print(f"处理文件失败 {file_path}: {str(e)}")
        if len(lines_accumulated) >= pages * 50:  # 每页50行
            break
    
    # 写入文档
    for page in range(pages):
        start_idx = page * 50
        end_idx = start_idx + 50
        if start_idx >= len(lines_accumulated):
            break
        # 添加代码行（保留原始缩进）
        for line in lines_accumulated[start_idx:end_idx]:
            doc.add_paragraph(line, style='Normal')
    
    doc.save(output_path)

# ====== 新增核心功能：规范化文件名 ======
def generate_multiple_docs(source_dir, output_dir, doc_count, project_name, version, pages=30):
    """生成多个文档，文件名按'源码 - 项目/系统名称'格式命名"""
    os.makedirs(output_dir, exist_ok=True)
    for i in range(1, doc_count + 1):
        # 按规范生成文件名：如"源码 - 智慧医疗系统1.docx"
        filename = f"源码 - {project_name}{i}.docx"  # [1,4](@ref)
        output_path = os.path.join(output_dir, filename)
        generate_doc(source_dir, output_path, project_name, version, pages)
        print(f"已生成: {filename}")
    return [os.path.join(output_dir, f"源码 - {project_name}{i}.docx") for i in range(1, doc_count+1)]

# ====== 使用示例 ======
if __name__ == "__main__":
    # 配置参数
    SOURCE_DIR = "D:/dev/vibetunnel"  # 替换为源码目录
    OUTPUT_DIR = "./copyright_docs"      # 输出目录
    PROJECT_NAME = "智慧医疗系统"         # 项目/系统名称
    VERSION = "1.0"
    DOC_COUNT = 3                        # 需生成的文档数量
    
    # 执行生成
    generate_multiple_docs(
        source_dir=SOURCE_DIR,
        output_dir=OUTPUT_DIR,
        doc_count=DOC_COUNT,
        project_name=PROJECT_NAME,
        version=VERSION
    )