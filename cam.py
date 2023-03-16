import cv2
from picamera2 import Picamera2

def image_capture_cv():
    cap = cv2.VideoCapture(0)
    if cap.isOpened() == False:
        print("Error in opening video stream or file")
    else:
        ret, frame = cap.read()
        cv2.imwrite('image_cv.png',frame)
    cap.release()
    print("Saved file (cv)")

def image_capture_pi(cient):
    picam = Picamera2()
    picam.capture_file("image_pi.jpg")
    print("Saved file (pi)")

def run():
    image_capture_pi()
    image_capture_cv()

if __name__ == '__main__':
    run()