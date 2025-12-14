
def update_title_header(doc):
    # Iterate through paragraphs to find the Main Title and update it
    # We suspect it's in the first few paragraphs or in a Header section
    
    # Check body paragraphs first (often Cover Page title is just a paragraph)
    for p in doc.paragraphs[:20]: # Check first 20 paragraphs
        if "Çoklu Para Birimi" in p.text or "Sihirbazı" in p.text:
            print(f"Updating Title: {p.text}")
            p.text = "El Terminali WMS Kullanım Kılavuzu"
            # Keep style, just change text
            
def extract_frame_with_labeled_redbox(video_path, time_sec, output_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return False
        
    cap.set(cv2.CAP_PROP_POS_MSEC, time_sec * 1000)
    ret1, frame_curr = cap.read()
    
    prev_time = max(0, time_sec - 1.5)
    cap.set(cv2.CAP_PROP_POS_MSEC, prev_time * 1000)
    ret2, frame_prev = cap.read()
    
    cap.release()
    
    if not ret1: return False
    
    final_image = frame_curr.copy()
    
    if ret2:
        try:
            gray_curr = cv2.cvtColor(frame_curr, cv2.COLOR_BGR2GRAY)
            gray_prev = cv2.cvtColor(frame_prev, cv2.COLOR_BGR2GRAY)
            
            diff = cv2.absdiff(gray_curr, gray_prev)
            _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
            kernel = np.ones((5,5), np.uint8)
            dilated = cv2.dilate(thresh, kernel, iterations=2)
            contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Sort contours by size and take top N significant ones
            contours = sorted(contours, key=cv2.contourArea, reverse=True)
            
            count = 1
            for c in contours:
                if cv2.contourArea(c) > 500: # Filter noise
                    x, y, w, h = cv2.boundingRect(c)
                    
                    # Draw Red Box
                    cv2.rectangle(final_image, (x, y), (x+w, y+h), (0, 0, 255), 3)
                    
                    # Add Label (1, 2, 3...)
                    label = str(count)
                    # White text with Red background
                    text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
                    cv2.rectangle(final_image, (x, y - text_size[1] - 10), (x + text_size[0] + 10, y), (0,0,255), -1)
                    cv2.putText(final_image, label, (x + 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                    
                    count += 1
                    if count > 5: # Limit to 5 boxes
                        break
        except Exception as e:
            print(f"RedBox Error: {e}")
            
    cv2.imwrite(output_path, final_image)
    return True
