# Import lib for basic function
import sys
import time
import random
import datetime
# Import lib contains function camera detector return result:
# 1. Non-person
# 2. Person wear mask
# 3. Person non-wear mask
from simple_ai import *
# Import lib contains function to connect to COM port
from uart import *
# import lib MQTTClient to connect to Adafruit_IO webpage
from Adafruit_IO import MQTTClient
# Credentials to connect Adafruit_IO webpage
AIO_FEED_ID = ["button1", "button2", "button3"]
AIO_USERNAME = "khanhnh88"
AIO_KEY = "aio_PpmO254iuQYSF7G0TEkDeojHoKes"
# Function to connect, disconnect, message, subscribe
# for MQTTClient connect to Adafruit_IO webpage
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
# Assign functions to MQTTClient
client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()
# timer for get variables to ai
counter_ai = 5
# if don't change result of camera dectector, don't change state of ai
ai_result = ""
previous_result = ""
while True:
    # Block code to get result after detect person exist on camera and if exists that person wear mask or not
    counter_ai -= 1
    if counter_ai <= 0:
        #TODO
        counter_ai = 5  # Reset timer
        previous_result = ai_result
        ai_result = image_detector()
        print("AI Output: ",ai_result)
        if previous_result != ai_result:
            client.publish("ai",ai_result)

    # read data form hardware and transfer it to server
    readSerial(client)
    time.sleep(1)
    pass