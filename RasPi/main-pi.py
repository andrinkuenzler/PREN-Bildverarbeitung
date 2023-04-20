# To be run on the Raspberry Pi
# Captures an Image, saves it to the working directory and publishes it to the mqtt-Broker

import time
import shutil # added counter
import os # added counter
from paho.mqtt import client as mqtt_client
from picamera2 import Picamera2

counter = 0

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
        global counter # added counter
        picam.capture_file("/home/pi/PREN-Bildverarbeitung/RasPi/rawImage-{}.jpg".format(counter)) # added counter
        with open("/home/pi/PREN-Bildverarbeitung/RasPi/rawImage-{}.jpg".format(counter),'rb') as file: # added counter
            filecontent = file.read()
            byteArr = bytearray(filecontent)
            publish(client, byteArr, "test/image/raw")
        counter += 1 # added counter
        time.sleep(5) # verringern oder entfernen

def publish(client, data, topic):
    result = client.publish(topic, data, 0)
    status = result[0]
    if status == 0:
        print("Pi published image to raw")
    else:
        print("Pi failed to publish raw image")

def run():
    if (os.path.exists("/home/pi/PREN-Bildverarbeitung/RasPi/rawImage-*.jpg")): # added counter
        shutil.rmtree("/home/pi/PREN-Bildverarbeitung/RasPi/rawImage-*.jpg") # added counter
    client = connect_mqtt()
    client.loop_start()
    image_capture(client)

if __name__ == '__main__':
    run()

while True:
    time.sleep(1)