# To be run on the VM
# Converts dummy image and publishes it

import time
from paho.mqtt import client as mqtt_client

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    client = mqtt_client.Client("VM-Bilderkennung")
    client.on_connect = on_connect
    client.connect("localhost", 1883)
    return client

def convert_image(client):
    while True:
        with open("./dummyImage.jpg",'rb') as file:
            filecontent = file.read()
            byteArr = bytearray(filecontent)
            publish(client, byteArr, "test/image/raw")
        print("Published image (raw)")
        time.sleep(5)

def publish(client, data, topic):
    result = client.publish(topic, data, 0)
    status = result[0]
    if status == 0:
        print("Sent message")
    else:
        print("Failed to send message")

def run():
    client = connect_mqtt()
    client.loop_start()
    convert_image(client)

if __name__ == '__main__':
    run()

while True:
    time.sleep(1)