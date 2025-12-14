
import cv2
import numpy as np

def smart_redbox_test(image_path, output_path):
    img = cv2.imread(image_path)
    if img is None:
        print("Image not found")
        return

    # Simulate a "Region of Interest" (ROI) where change happened.
    # Since we don't have the video stream here for diffing, 
    # let's assume the "Mouse Click" happened at a specific point 
    # or we simulate 'contours' from a diff.
    # For testing, we will just try to find ALL UI elements (rectangles)
    # and pick one to highlight to see if the detection works.
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 1. Edge Detection to find UI structure
    edged = cv2.Canny(gray, 50, 150)
    
    # Dilate edges to connect gaps
    kernel = np.ones((3,3), np.uint8)
    edged = cv2.dilate(edged, kernel, iterations=1)
    
    contours, _ = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter for UI-like rectangles
    ui_elements = []
    
    vis = img.copy()
    
    for c in contours:
        approx = cv2.approxPolyDP(c, 0.01 * cv2.arcLength(c, True), True)
        # Rectangles have 4 points
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(c)
            # Filter huge boxes (entire screen) and tiny noise
            if w > 20 and h > 10 and w < img.shape[1] - 50:
                ui_elements.append((x, y, w, h))
                # cv2.rectangle(vis, (x, y), (x+w, y+h), (0, 255, 0), 1)
    
    # Now simulate a "Change Event" (e.g., pixel diff cluster)
    # Let's say the change happened around point (x=500, y=300) - purely hypothetical
    # In real code, this comes from 'diff' contours.
    
    # We want to find the UI element that best fits this change.
    
    # To demonstrate, I'll just highlight the top 5 largest "valid looking" UI elements
    # to show that we can grab clean boxes.
    
    ui_elements = sorted(ui_elements, key=lambda b: b[2]*b[3], reverse=True)
    
    count = 1
    for i in range(min(5, len(ui_elements))):
        x, y, w, h = ui_elements[i]
        
        # Draw Red Box
        cv2.rectangle(vis, (x, y), (x+w, y+h), (0, 0, 255), 2)
        
        # Circle Label
        center_x = x
        center_y = y
        radius = 12
        cv2.circle(vis, (center_x, center_y), radius, (0, 0, 255), -1)
        
        label = str(count)
        cv2.putText(vis, label, (center_x - 5, center_y + 5), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        
        count += 1
        
    cv2.imwrite(output_path, vis)
    print(f"Saved test to {output_path}")

if __name__ == "__main__":
    # Use one of the extracted frames
    smart_redbox_test(r"final_images\step_3_544.jpg", "smart_box_test.jpg")
