# To be run on the Raspberry Pi
# Captures an Image and saves it to the working directory

import cv2
import time
from picamera2 import Picamera2

def image_capture_cv():
    cap = cv2.VideoCapture(0)
    if cap.isOpened() == False:
        print("Error in opening video stream or file")
    else:
        ret, frame = cap.read()
        if ret:
            cv2.imwrite('image_cv.png',frame)
    cap.release()
    cv2.destroyAllWindows()
    print("Saved file (cv)")

def image_capture_pi():
    picam = Picamera2()
    camera_config = picam.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
    picam.configure(camera_config)
    picam.start()
    time.sleep(2)
    picam.capture_file("/home/pi/PREN-Bildverarbeitung/RasPi/image_pi.jpg")
    print("Saved file (pi)")

def run():
    image_capture_pi()
#    image_capture_cv()

if __name__ == '__main__':
    run()
