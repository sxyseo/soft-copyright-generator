import os
import random
import re
from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import Pt, RGBColor
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def scan_code_files(source_dir, extensions=['.py', '.js', '.ts', '.java', '.html', '.css']):
    """扫描源代码目录并过滤有效文件"""
    code_files = []
    skip_dirs = {'node_modules', '.git', '__pycache__', 'build', 'dist', 'venv', '.idea'}
    
    for root, dirs, files in os.walk(source_dir):
        # 跳过指定目录
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                code_files.append(os.path.join(root, file))
    return code_files

def preprocess_code(content):
    """预处理代码：移除注释和空行"""
    # 移除单行注释（支持#、//）
    content = re.sub(r'//.*|#.*', '', content)
    # 移除多行注释（/* ... */）
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    # 移除空行
    content = os.linesep.join([s for s in content.splitlines() if s.strip()])
    return content

def add_page_header_footer(doc, software_name, version):
    """添加页眉页脚（软件名+版本号+页码）"""
    # 添加页眉
    section = doc.sections[0]
    header = section.header
    header_para = header.paragraphs[0]
    header_para.text = f"{software_name} v{version}"
    header_para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    # 添加页脚（页码）
    footer = section.footer
    paragraph = footer.paragraphs[0]
    paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT
    
    # 创建页码字段
    fld_char = OxmlElement('w:fldChar')
    fld_char.set(qn('w:fldCharType'), 'begin')
    instr_text = OxmlElement('w:instrText')
    instr_text.set(qn('xml:space'), 'preserve')
    instr_text.text = 'PAGE'
    
    fld_char2 = OxmlElement('w:fldChar')
    fld_char2.set(qn('w:fldCharType'), 'end')
    
    run = paragraph.add_run()
    run._r.append(fld_char)
    run._r.append(instr_text)
    run._r.append(fld_char2)

def generate_doc(source_dir, output_path, software_name, version, pages=30, show_source=True):
    """生成单个代码文档"""
    code_files = scan_code_files(source_dir)
    if not code_files:
        raise FileNotFoundError("未找到支持的源代码文件")
    
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
    while len(lines_accumulated) < pages * 50 and code_files:
        file_path = code_files.pop()
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
    return True

def generate_multiple_docs(source_dir, output_dir, doc_count, software_name, version, pages=30, show_source=True):
    """生成多个不重复文档，文件名格式：源码 - 项目/系统名称"""
    os.makedirs(output_dir, exist_ok=True)
    generated_paths = []
    
    for i in range(1, doc_count + 1):
        # 按要求的格式命名：源码 - 项目/系统名称
        if doc_count > 1:
            filename = f"源码 - {software_name} ({i}).docx"
        else:
            filename = f"源码 - {software_name}.docx"
        output_path = os.path.join(output_dir, filename)
        generate_doc(source_dir, output_path, software_name, version, pages, show_source)
        generated_paths.append(output_path)
        print(f"已生成文档 #{i}: {filename}")
    
    return generated_paths

# ======== 使用示例 ========
if __name__ == "__main__":
    # 配置参数
    SOURCE_DIR = "D:/dev/vibetunnel"  # 替换为源码目录
    OUTPUT_DIR = "./output_docs"              # 输出目录
    SOFTWARE_NAME = "MyApp"
    VERSION = "1.0"
    DOC_COUNT = 1                             # 需要生成的文档数量
    PAGES_PER_DOC = 30                        # 每个文档页数
    
    # 执行生成
    result = generate_multiple_docs(
        source_dir=SOURCE_DIR,
        output_dir=OUTPUT_DIR,
        doc_count=DOC_COUNT,
        software_name=SOFTWARE_NAME,
        version=VERSION,
        pages=PAGES_PER_DOC
    )
    
    print(f"\n成功生成 {len(result)} 个文档，路径: {OUTPUT_DIR}")
