import cv2
import numpy as np
from time import time
from windowcapture import WindowCapture

# Load trained model
pet_cascade = cv2.CascadeClassifier('Testaufbau/PET/cascade/cascade.xml')
kronkorken_cascade = cv2.CascadeClassifier('Testaufbau/Kronkorken/cascade/cascade.xml')

cap = cv2.VideoCapture(0)
if cap.isOpened() == False:
    print("Error in opening video stream or file")
while(cap.isOpened()):
    ret, frame = cap.read()
    
    # Convert video to gray
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Start object detection for PET
    pet_detected = pet_cascade.detectMultiScale(gray, 1.3, 5)
    # Draw rectangles
    for (x, y, w, h) in pet_detected:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)

    # Start object detection for Kronkorken
    kronkorken_detected = kronkorken_cascade.detectMultiScale(gray, 1.3, 5)
    # Draw rectangles
    for (x, y, w, h) in kronkorken_detected:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)

    if ret:
        # Display the resulting frame
        cv2.imshow('Frame',frame)
        # Press esc to exit
        if cv2.waitKey(1) & 0xFF == 27:
            break
        # Press p to save screenshot in positive folder
        elif cv2.waitKey(1) == ord('p'):
            cv2.imwrite('Testaufbau/positive/{}.jpg'.format(time()), WindowCapture('Frame').get_screenshot())
        # Press n to save screenshot in negative folder
        elif cv2.waitKey(1) == ord('n'):
            cv2.imwrite('Testaufbau/negative/{}.jpg'.format(time()), WindowCapture('Frame').get_screenshot())
    else:
        break
cap.release()
cv2.destroyAllWindows()