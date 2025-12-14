import cv2
import numpy as np
import os

def detect_change_region(video_path, time_sec):
    cap = cv2.VideoCapture(video_path)
    
    # Get frame at time_sec
    cap.set(cv2.CAP_PROP_POS_MSEC, time_sec * 1000)
    ret1, frame_curr = cap.read()
    
    # Get frame slightly before (e.g. 1 second before) to see change
    cap.set(cv2.CAP_PROP_POS_MSEC, (time_sec - 1.0) * 1000)
    ret2, frame_prev = cap.read()
    
    if not ret1 or not ret2:
        print("Could not read frames")
        return
        
    # Convert to grayscale
    gray_curr = cv2.cvtColor(frame_curr, cv2.COLOR_BGR2GRAY)
    gray_prev = cv2.cvtColor(frame_prev, cv2.COLOR_BGR2GRAY)
    
    # Absdiff
    diff = cv2.absdiff(gray_curr, gray_prev)
    
    # Threshold
    _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
    
    # Dilate to merge close regions
    kernel = np.ones((5,5), np.uint8)
    dilated = cv2.dilate(thresh, kernel, iterations=2)
    
    # Find contours
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Find largest contour (assumed to be the interaction)
    output_img = frame_curr.copy()
    found = False
    
    if contours:
        # Sort by area
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        
        # Take the largest one
        c = contours[0]
        if cv2.contourArea(c) > 500: # Filter small noise
            x, y, w, h = cv2.boundingRect(c)
            # Draw Red Box (BGR: 0, 0, 255)
            cv2.rectangle(output_img, (x, y), (x+w, y+h), (0, 0, 255), 3)
            print(f"Detected change at {time_sec}s: Box at ({x},{y},{w},{h})")
            found = True
            
    if not found:
        print("No significant change detected.")
        
    # Save result
    out_name = f"redbox_test_{int(time_sec)}.jpg"
    cv2.imwrite(out_name, output_img)
    print(f"Saved: {out_name}")
    
    cap.release()

if __name__ == "__main__":
    video_file = r"..\1-El Terminali Eğitimi-20250623_092431-Toplantı Kaydı.mp4"
    # Test on a few timestamps from the plan
    # 544s -> Genel Parametreler Click
    # 2814s -> Buton Parametre Click
    detect_change_region(video_file, 544)
    detect_change_region(video_file, 2814)
