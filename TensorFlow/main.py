##########################################################################################
'''
must create virtual environment: .venv
python -m venv /path/to/new/virtual/environment
must install pakages to .venv:
- Activate .venv:
.venv\Scripts\Activate
- Adafruit_IO:
pip install adafruit-io
- setuptools:
pip3 install setuptools
pip3 install --upgrade setuptools
- paho-mqtt
pip install paho-mqtt==1.6.1
'''
##########################################################################################
import sys
import time
import random
import datetime

from Adafruit_IO import MQTTClient

from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import numpy as np


AIO_FEED_ID = ["button1", "button2", "button3"]
AIO_USERNAME = ""
AIO_KEY = ""

def connected(client):
    print("Ket noi thanh cong ...")
    for topic in AIO_FEED_ID:
        client.subscribe(topic)

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribe thanh cong ...")

def disconnected(client):
    print("Ngat ket noi ...")
    sys.exit (1)

def message(client , feed_id , payload):
    print("Nhan du lieu: " + payload)

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model("keras_Model.h5", compile=False)

# Load the labels
class_names = open("labels.txt", "r").readlines()

# CAMERA can be 0 or 1 based on default camera of your computer
camera = cv2.VideoCapture(0)

counter = 5
sensor_type = 1
while True:
    counter -= 1
    if counter <= 0:
        counter = 5
        #TODO
        print("Random data is publishing...")
        print(datetime.datetime.now())
        print("Sensor ",sensor_type)
        
        if sensor_type == 1: # Update sensor 1
            temp = random.randint(10, 20)
            client.publish("sensor1", temp)
        elif sensor_type == 2: # Update sensor 2
            light = random.randint(100, 500) 
            client.publish("sensor2", light)
        elif sensor_type == 3: # Update sensor 3
            humi = random.randint(30, 70)
            client.publish("sensor3", humi)
        # reset sensor_type to 1 when come to 3
        sensor_type = 1 if sensor_type >= 3 else sensor_type + 1
        
        # Grab the web camera's image.
        ret, image = camera.read()
        # Resize the raw image into (224-height,224-width) pixels
        image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
        # Show the image in a window
        cv2.imshow("Webcam Image", image)
        # Make the image a numpy array and reshape it to the models input shape.
        image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
        # Normalize the image array
        image = (image / 127.5) - 1
        # Predicts the model
        prediction = model.predict(image)
        index = np.argmax(prediction)
        class_name = class_names[index]
        confidence_score = prediction[0][index]
        # Print prediction and confidence score
        print("Class:", class_name[2:], end="")
        print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")
        client.publish("sensor4",np.round(confidence_score*100))
        # Listen to the keyboard for presses.
        keyboard_input = cv2.waitKey(1)
        # 27 is the ASCII for the esc key on your keyboard.
        if keyboard_input == 27:
            break        
    time.sleep(1)
    pass

camera.release()
cv2.destroyAllWindows()