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

def on_message(client, userdata, message):
    print ("Raw image received")
    convert_image_raw(client, message)

# Convert from byteArray to Image
def convert_image_raw(client, message):
    f = open("./rawImage.jpg", 'wb')
    f.write(message.payload)
    f.close()
    print ("image received")

# Process Image with OpenCV and send to convert_imgae to publish
def obect_recognition(client):
    print()

# Convert from image to byteArray
def convert_image_processed(client, topic):
    with open("./processedImage.jpg",'rb') as file:
        filecontent = file.read()
        byteArr = bytearray(filecontent)
        publish(client, byteArr, topic)
    print("Published image (raw)")

# Publish byteArray
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

if __name__ == '__main__':
    run()

while True:
    time.sleep(1)