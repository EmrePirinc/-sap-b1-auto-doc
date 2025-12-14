
from docx import Document

def find_indices(path):
    doc = Document(path)
    body = doc.element.body
    
    start_index = -1
    end_index = -1
    
    # Check paragraphs for "1. Amaç"
    for i, child in enumerate(body.iterchildren()):
        if child.tag.endswith('p'): # Paragraph
            text = child.xpath('.//w:t') # Get text via XML to be sure
            full_text = "".join([t.text for t in text if t.text])
            if "1. Amaç" in full_text:
                print(f"Found '1. Amaç' at index: {i}")
                start_index = i
                break
                
    # Check tables
    for i, child in enumerate(body.iterchildren()):
        if child.tag.endswith('tbl'):
            # Check if it's the history table
            # Simple check: assumes only one table or the last one
            print(f"Found Table at index: {i}")
            end_index = i
            
    print(f"Deletion Range: {start_index} to {end_index}")

if __name__ == "__main__":
    find_indices(r"..\Çoklu Para Birimi Sihirbazı Kullanıcı Dokümanı.docx")
