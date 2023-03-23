# To be run on the Raspberry Pi
# Captures an Image, saves it to the working directory and publishes it to the mqtt-Broker

import time
from paho.mqtt import client as mqtt_client
from picamera2 import Picamera2

def image_capture(client):
    picam = Picamera2()
    camera_config = picam.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
    picam.configure(camera_config)
    picam.start()
    time.sleep(2)
    picam.capture_file("image_pi.jpg")
    print("Saved file (pi)")
    with open("./image_pi.jpg",'rb') as file:
        filecontent = file.read()
        byteArr = bytearray(filecontent)
        publish(client, byteArr, "test/image/raw")
    print("Published file (pi)")

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

def publish(client, data, topic):
    result = client.publish(topic, data, 0) #changed to param
    status = result[0]
    if status == 0:
        print("Sent message")
    else:
        print("Failed to send message")

def run():
    client = connect_mqtt()
    client.loop_start()
    time.sleep(5) #testing purpose
    image_capture(client)

if __name__ == '__main__':
    run()