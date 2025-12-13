import json
import cv2
import os
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

def extract_frame(video_path, time_sec, output_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}")
        return False
    
    cap.set(cv2.CAP_PROP_POS_MSEC, time_sec * 1000)
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(output_path, frame)
    else:
        print(f"Error: Could not read frame at {time_sec}")
    
    cap.release()
    return ret

def create_doc_from_plan(video_path, plan_path, output_docx):
    # Load Plan
    with open(plan_path, 'r', encoding='utf-8') as f:
        plan = json.load(f)
        
    doc = Document()
    
    # Simple Style Setup
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Calibri'
    font.size = Pt(11)
    
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
            
            if extract_frame(video_path, time_sec, img_path):
                try:
                    doc.add_picture(img_path, width=Inches(6))
                    caption = doc.add_paragraph(f"Ekran Görüntüsü {step_counter}")
                    caption.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
                    caption.style = "Caption"
                except Exception as e:
                    print(f"Error adding image: {e}")
            
            doc.add_paragraph("") # Spacing
            step_counter += 1
            
    doc.save(output_docx)
    print(f"Successfully saved {output_docx}")

if __name__ == "__main__":
    # Example Usage
    # Ensure video file path is correct
    video_file = r"..\1-El Terminali Eğitimi-20250623_092431-Toplantı Kaydı.mp4"
    plan_file = "content_plan.json"
    output_file = r"..\Taslak_Dokuman_AI_Output.docx"
    
    if os.path.exists(plan_file):
        create_doc_from_plan(video_file, plan_file, output_file)
    else:
        print("content_plan.json bulunamadı. Lütfen önce planı oluşturun.")
