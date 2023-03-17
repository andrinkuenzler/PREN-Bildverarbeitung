# To be run on the VM
# Converts, publishes, reverts and saves dummy image

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
    client.on_message = on_message
    client.connect("localhost", 1883)
    return client

def subscribe(client, topic):
    result = client.subscribe(topic)
    status = result[0]
    if status == 0:
        print("Subscribed")
    else:
        print("Failed to subscribe")

def convert_image(client):
    with open("./dummyImage.jpg",'rb') as file:
        filecontent = file.read()
        byteArr = bytearray(filecontent)
        publish(client, byteArr, "test/image/raw")
    print("Published image (raw)")

def on_message(client, userdata, message):
    print ("Raw image received")
    process_image(client, message)

def process_image(client, message):
    f = open("./dummyImageReceived.jpg", 'wb')
    f.write(message.payload)
    f.close()
    print ("image received")
    #publish(client, message.payload, "test/image/processed")

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
    subscribe(client, "test/image/raw")
    time.sleep(5)
    convert_image(client)

if __name__ == '__main__':
    run()

while True:
    time.sleep(1)