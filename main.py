import cv2
from paho.mqtt import client as mqtt_client
from picamera2 import Picamera2

def video_capture(client):
    cap = cv2.VideoCapture(0)
    if cap.isOpened() == False:
        print("Error in opening video stream or file")
    else:
        ret, frame = cap.read()
        cv2.imwrite('images/c1.png',frame)
        fileContent = frame.read()
        byteArr = bytearray(fileContent)
        publish(client, byteArr)
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret:
            publish(client, frame, 0)
        else:
            break
    cap.release()

def image_capture(client):
    picam = Picamera2()
    picam.capture_file("test.jpg")
    f = open("test.jpg")
    fileContent = f.read()
    byteArr = bytearray(fileContent)
    publish(client, byteArr)

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    client = mqtt_client.Client("RasPi-Bilderkennung")
    client.on_connect = on_connect
    client.connect("prenf23-banthama.el.eee.intern", 1883)
    return client

def publish(client, data):
    result = client.publish("testTopic", data, 0)
    status = result[0]
    if status == 0:
        print(f"Send message")
    else:
        print(f"Failed to send message")

def run():
    client = connect_mqtt()
    client.loop_start()
    image_capture(client)

if __name__ == '__main__':
    run()