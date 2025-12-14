import json
import cv2
import os
import numpy as np
from datetime import datetime
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Twips
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml.ns import qn

def extract_frame_with_redbox(video_path, time_sec, output_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}")
        return False
    
    # 1. Get Current Frame
    cap.set(cv2.CAP_PROP_POS_MSEC, time_sec * 1000)
    ret1, frame_curr = cap.read()
    
    # 2. Get Previous Frame (1.5s before) to find what changed
    # (Using 1.5s to be safe against slow transitions)
    prev_time = max(0, time_sec - 1.5)
    cap.set(cv2.CAP_PROP_POS_MSEC, prev_time * 1000)
    ret2, frame_prev = cap.read()
    
    cap.release()
    
    if not ret1:
        print(f"Error: Could not read frame at {time_sec}")
        return False

    final_image = frame_curr
    
    # 3. Detect Red Box if we have a previous frame
    if ret2:
        try:
            gray_curr = cv2.cvtColor(frame_curr, cv2.COLOR_BGR2GRAY)
            gray_prev = cv2.cvtColor(frame_prev, cv2.COLOR_BGR2GRAY)
            
            diff = cv2.absdiff(gray_curr, gray_prev)
            _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
            kernel = np.ones((5,5), np.uint8)
            dilated = cv2.dilate(thresh, kernel, iterations=2)
            contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if contours:
                # Find largest change
                c = max(contours, key=cv2.contourArea)
                if cv2.contourArea(c) > 500: # Ignore noise
                    x, y, w, h = cv2.boundingRect(c)
                    # Draw Red Box
                    cv2.rectangle(final_image, (x, y), (x+w, y+h), (0, 0, 255), 3)
        except Exception as e:
            print(f"RedBox Error: {e}")

    # Save
    cv2.imwrite(output_path, final_image)
    return True

def set_aifteam_styles(doc):
    # 1. Page Margins
    section = doc.sections[0]
    section.left_margin = Twips(1134)
    section.right_margin = Twips(1418)
    section.top_margin = Twips(1418)
    section.bottom_margin = Twips(1418)

    # 2. Normal Style
    style_normal = doc.styles['Normal']
    font_normal = style_normal.font
    font_normal.name = 'Calibri'
    font_normal.size = Pt(12)
    # Space After ~10pt
    style_normal.paragraph_format.space_after = Pt(10)

    # 3. Heading 1
    style_h1 = doc.styles['Heading 1']
    font_h1 = style_h1.font
    font_h1.name = 'Calibri'
    font_h1.size = Pt(14)
    font_h1.color.rgb = RGBColor(0x80, 0x80, 0x80) # Gray
    font_h1.bold = True
    style_h1.paragraph_format.space_before = Pt(12)
    style_h1.paragraph_format.space_after = Pt(0)

    # 4. Heading 2
    style_h2 = doc.styles['Heading 2']
    font_h2 = style_h2.font
    font_h2.name = 'Calibri'
    font_h2.size = Pt(14)
    font_h2.color.rgb = RGBColor(0x80, 0x80, 0x80) # Gray
    font_h2.bold = False
    style_h2.paragraph_format.space_before = Pt(6)
    style_h2.paragraph_format.space_after = Pt(6)

    # 5. Heading 3 (Dark Blue)
    style_h3 = doc.styles['Heading 3']
    font_h3 = style_h3.font
    font_h3.name = 'Calibri'
    font_h3.size = Pt(12)
    font_h3.color.rgb = RGBColor(0x1F, 0x4D, 0x78) # Dark Blue
    font_h3.bold = True
    style_h3.paragraph_format.space_before = Pt(2)
    style_h3.paragraph_format.space_after = Pt(0)

def create_doc_from_plan(video_path, plan_path, output_docx):
    # Load Plan
    with open(plan_path, 'r', encoding='utf-8') as f:
        plan = json.load(f)
        
    doc = Document()
    
    # Apply Professional Styles
    set_aifteam_styles(doc)
    
    # Add Cover Page
    doc.add_heading('El Terminali Kullanım Kılavuzu', 0)
    doc.add_paragraph('Sürüm: 1.0').alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    doc.add_paragraph('Tarih: 14.12.2025').alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    doc.add_page_break()
    
    # Add Document History (Placeholder)
    doc.add_heading('Doküman Tarihçesi', level=1)
    table = doc.add_table(rows=2, cols=4)
    table.style = 'Table Grid'
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Versiyon'
    hdr_cells[1].text = 'Tarih'
    hdr_cells[2].text = 'Yazar'
    hdr_cells[3].text = 'Açıklama'
    
    start_cells = table.rows[1].cells
    start_cells[0].text = '1.0'
    start_cells[1].text = datetime.now().strftime("%d.%m.%Y")
    start_cells[2].text = 'Otomasyon Aracı'
    start_cells[3].text = 'İlk Taslak'
    
    doc.add_page_break()

    # Content Body
    img_dir = "final_images"
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
        
    step_counter = 1
    
    for item in plan:
        if item['type'] == 'heading':
            doc.add_heading(item['text'], level=item['level'])
            
        elif item['type'] == 'step':
            # Add Text
            p = doc.add_paragraph(item['text'])
            
            # Extract and Add Image
            time_sec = item['time']
            img_name = f"step_{step_counter}_{int(time_sec)}.jpg"
            img_path = os.path.join(img_dir, img_name)
            
            print(f"Processing Step {step_counter}: {item['text'][:30]}... at {time_sec}s")
            
            if extract_frame_with_redbox(video_path, time_sec, img_path):
                try:
                    doc.add_picture(img_path, width=Inches(6))
                    caption = doc.add_paragraph(f"Ekran Görüntüsü {step_counter}")
                    caption.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
                    caption.style = "Caption"
                except Exception as e:
                    print(f"Error adding image: {e}")
            
            # Remove explicit empty paragraph if style handles spacing
            # doc.add_paragraph("") 
            step_counter += 1
            
    doc.save(output_docx)
    print(f"Successfully saved {output_docx}")

if __name__ == "__main__":
    video_file = r"..\1-El Terminali Eğitimi-20250623_092431-Toplantı Kaydı.mp4"
    plan_file = "content_plan.json"
    output_file = r"..\Taslak_Dokuman_v7_Styled.docx"
    
    create_doc_from_plan(video_file, plan_file, output_file)
