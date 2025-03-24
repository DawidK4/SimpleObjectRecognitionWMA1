import cv2
import numpy as np

video = cv2.VideoCapture(r'snow.mp4')
video.open(r'snow.mp4')
total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

frame_width = int(video.get(3))
frame_height = int(video.get(4))
size = (frame_width, frame_height)
result = cv2.VideoWriter(
    'catRes.avi', cv2.VideoWriter_fourcc(*'MJPG'), 20, size)

counter = 1

while True:
    success, frame = video.read()
    if not success:
        break
    
    progress = (counter / total_frames) * 100
    print(f'Processing frame {counter} of {total_frames} ({progress:.2f}%)')
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 50])

    # Creates a binary mask where black pixels appear white (255) and everything else is black (0)
    mask = cv2.inRange(hsv, lower_black, upper_black)

    # Finds the boundaries of the detected black areas 
    # RETR_EXTERNAL -> retrieves only the outermost contours
    # CHAIN_APPROX_SIMPLE -> reduces the number of points in the contour
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) > 1000:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)
            cx, cy = x + w // 2, y + h // 2
            cv2.drawMarker(frame, (cx, cy), (0, 0, 255), markerType=cv2.MARKER_CROSS, thickness=2)
    
    result.write(frame)
    counter += 1

print("Processing complete!")
video.release()
result.release()
