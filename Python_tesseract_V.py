import cv2
import pytesseract

# Path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Path to the video file
video_path = '{ENTER VIDEO PATH}'

# Initialize video capture
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    raise IOError(f"Error opening video file {video_path}")

# Initialize a list to hold the extracted codes
codes = []

# Function to process the frames and extract text
def extract_text_from_frame(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, threshold_frame = cv2.threshold(gray_frame, 150, 255, cv2.THRESH_BINARY)
    text = pytesseract.image_to_string(threshold_frame, config='--psm 6')
    return text.strip()

# Frame skipping interval
frame_skip_interval = 3  # Process every 5th frame
frame_number = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if frame_number % frame_skip_interval == 0:
        text = extract_text_from_frame(frame)
        if text:
            codes.append(text)
            print(f"Frame {frame_number}: {text}")

    frame_number += 1

# Release the video capture
cap.release()

# Save the extracted codes to a text file
try:
    with open("extracted_text.txt", "w") as file:
        for code in codes:
            file.write(f"{code}\n")
except IOError as e:
    print(f"Error writing to file: {e}")

print("Extraction complete. Codes saved to 'extracted_text.txt'")
