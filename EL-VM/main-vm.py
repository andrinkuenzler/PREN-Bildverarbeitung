# To be run on the VM
# Converts, publishes, reverts and saves dummy image

import random
import time
import cv2
import numpy as np
from paho.mqtt import client as mqtt_client
from keras.models import load_model

port = 1883
topic = "test/image/raw"
client_id = f'python-mqtt-{random.randint(0, 100)}'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    #client.on_message = on_message
    client.connect("localhost", port)
    return client

def subscribe(client: mqtt_client):
    def on_message(client, userdata, message):
        print ("Raw image received")
        convert_image_raw(client, message)
    client.subscribe(topic)
    client.on_message = on_message

# def subscribeX(client, topic):
#     def on_message(client, userdata, msg):
#         print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
#     client.subscribe(topic)
#     client.on_message = on_message
#     #result = client.subscribe(topic)
#     #status = result[0]
#     #if status == 0:
#         #print("Subscribed")
#     #else:
#         #print("Failed to subscribe")

# Convert from byteArray to Image
def convert_image_raw(client, message):
    f = open("./rawImage.jpg", 'wb')
    f.write(message.payload)
    f.write(message.payload)
    f.close()
    print ("image received")
    object_recognition(client)

# Process Image with OpenCV and send to convert_image to publish
def object_recognition(client):
    # Disable scientific notation for clarity
    np.set_printoptions(suppress=True)
    # Load the model
    model = load_model("./converted_keras/keras_model.h5", compile=False)
    # Load the labels
    class_names = open("./converted_keras/labels.txt", "r").readlines()
    # Grab the webcamera's image.
    cv2.imread("./images/schluessel2.webp")
    # Resize the raw image into (224-height,224-width) pixels
    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
    # Make the image a numpy array and reshape it to the models input shape.
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
    # Normalize the image array
    image = (image / 127.5) - 1
    # Predicts the model
    prediction = model.predict(image)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    print("Class:", class_name[2:], end="")
    print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")

    # if (str(np.round(confidence_score * 100))[:-2] >= 75):
    #     convert_image_processed(client, "test/image/processed/hit")
    # else:
    #     convert_image_processed(client, "test/image/processed/noHit")


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
    subscribe(client)
    client.loop_forever()

if __name__ == '__main__':
    run()
