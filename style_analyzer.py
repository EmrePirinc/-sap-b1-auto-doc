
from docx import Document
from docx.shared import RGBColor

def get_color_hex(color):
    if color and color.rgb:
        return str(color.rgb)
    return "Theme/Default"

def analyze_styles(doc_path):
    doc = Document(doc_path)
    print(f"--- ANALYZING STYLES: {doc_path} ---")
    
    # 1. Page Margins (from first section)
    section = doc.sections[0]
    print(f"Margins (Twips): Left={section.left_margin.twips}, Right={section.right_margin.twips}, Top={section.top_margin.twips}, Bottom={section.bottom_margin.twips}")
    
    # 2. Collect unique paragraph styles
    styles_found = set()
    for para in doc.paragraphs:
        if para.style.name not in styles_found and para.text.strip():
            styles_found.add(para.style.name)
            style = para.style
            
            font_name = style.font.name
            font_size = style.font.size.pt if style.font.size else "Default"
            font_color = get_color_hex(style.font.color)
            
            # Paragraph formatting
            # Check direct formatting on paragraph vs style default
            # (Simplification: just checking style for now)
            
            print(f"\nStyle: {style.name}")
            print(f"  Font: {font_name}, Size: {font_size}")
            print(f"  Color: {font_color}")
            
            # Check paragraph format
            pf = style.paragraph_format
            print(f"  Spacing: Before={pf.space_before}, After={pf.space_after}")
            
            print(f"  Sample Text: {para.text[:50]}...")

if __name__ == "__main__":
    analyze_styles(r"..\Çoklu Para Birimi Sihirbazı Kullanıcı Dokümanı.docx")
