# To be run on the VM
# Converts, publishes, reverts and saves dummy image

import random
import time
import shutil
import os
import cv2
import glob # added counter
import numpy as np
from paho.mqtt import client as mqtt_client
from ultralytics import YOLO

model = YOLO('yolov8n.pt')  # load an official model
model = YOLO("/home/localadmin/PREN-Bildverarbeitung/EL-VM/runs/detect/train13/weights/best.pt") #load custom modelmodel = YOLO("runs/detect/train13/weights/best.pt")
counter = 1 # added counter

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    client = mqtt_client.Client(f'VM-Bilderkennung_{random.randint(0, 100)}')
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("localhost", 1883)
    return client

def subscribe(client):
     result = client.subscribe("test/image/raw")
     status = result[0]
     if status == 0:
         print("Subscribed to raw")
     else:
         print("Failed to subscribe to raw")

def on_message(client, userdata, message):
    print("on_message received")
    convert_image_raw(client, message)

# Convert from byteArray to Image
def convert_image_raw(client, message):
    global counter # added counter
    f = open("/home/localadmin/PREN-Bildverarbeitung/EL-VM/rawImage-{}.jpg".format(counter), 'wb') # added counter
    f.write(message.payload)
    f.close()
    print("Raw image saved")
    object_recognition(client, counter)
    counter += 1 # added counter

# Process Image with OpenCV and send to convert_image to publish
def object_recognition(client, counter): # added counter
    results = model.predict(source ='/home/localadmin/PREN-Bildverarbeitung/EL-VM/rawImage-{}.jpg'.format(counter), save=True, conf=0.5, project="/home/localadmin/PREN-Bildverarbeitung/EL-VM/runs/detect") # source already setup # added counter
    detetectObjectName = ""

    for r in results:
        for c in r.boxes.cls:
            print("Erkannt: ", model.names[int(c)])
            detetectObjectName = model.names[int(c)]

    if detetectObjectName != "":
        convert_image_processed(client, "test/image/processed/hit", counter) # added counter
    else:
        convert_image_processed(client, "test/image/processed/noHit", counter) # added counter


# Convert from image to byteArray
def convert_image_processed(client, topic, counter): # added counter
    if (os.path.exists("/home/localadmin/PREN-Bildverarbeitung/EL-VM/runs/detect/predict/")):
        with open("/home/localadmin/PREN-Bildverarbeitung/EL-VM/runs/detect/predict/rawImage-{}.jpg".format(counter),'rb') as file: # added counter
            filecontent = file.read()
            byteArr = bytearray(filecontent)
            publish(client, byteArr, topic)
            print("Processed Image published")
    else:
        print("dir not existing")

# Publish byteArray
def publish(client, data, topic):
    result = client.publish(topic, data, 0)
    status = result[0]
    if status == 0:
        print("Sent message")
    else:
        print("Failed to send message")

def run():
    if (os.path.exists("/home/localadmin/PREN-Bildverarbeitung/EL-VM/runs/detect/predict/")):
        shutil.rmtree("/home/localadmin/PREN-Bildverarbeitung/EL-VM/runs/detect/predict/")
    for filename in glob.glob("/home/localadmin/PREN-Bildverarbeitung/EL-VM/runs/detect/predict/rawImage-*.jpg"): # added counter
        os.remove(filename) # added counter
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

if __name__ == '__main__':
    run()
