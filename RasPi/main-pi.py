# To be run on the Raspberry Pi
# Captures an Image, saves it to the working directory and publishes it to the mqtt-Broker

import time
import shutil
import os
import glob
from paho.mqtt import client as mqtt_client
from picamera2 import Picamera2

counter = 1

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

def image_capture(client):
    picam = Picamera2()
    camera_config = picam.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
    picam.configure(camera_config)
    picam.start()
    time.sleep(2)
    while True:
        global counter
        picam.capture_file("/home/pi/PREN-Bildverarbeitung/RasPi/rawImage-{}.jpg".format(counter))
        with open("/home/pi/PREN-Bildverarbeitung/RasPi/rawImage-{}.jpg".format(counter),'rb') as file:
            filecontent = file.read()
            byteArr = bytearray(filecontent)
            publish(client, byteArr, "test/image/raw")
        counter += 1
        time.sleep(1) #Image capture intervall

def publish(client, data, topic):
    result = client.publish(topic, data, 0)
    status = result[0]
    if status == 0:
        print("Pi published image to raw")
    else:
        print("Pi failed to publish raw image")

def run():
    for filename in glob.glob("/home/pi/PREN-Bildverarbeitung/RasPi/rawImage-*.jpg"):
        os.remove(filename)
    client = connect_mqtt()
    client.loop_start()
    image_capture(client)

if __name__ == '__main__':
    run()

while True:
    time.sleep(1)