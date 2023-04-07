from paho.mqtt import client as mqtt_client
import random, time
import json
from software_design.models import Student
from software_design.serializers import StudentSerializer
from django.shortcuts import render, HttpResponse, redirect
from django.conf import settings

# MQTT broker and port configuration.
broker = 'broker.hivemq.com'
port = 1883
pub_topic_data = "ict720/waste_recycling/known_ble_add"
client_id = f'waste-segregation-{random.randint(0, 1000)}'

# Callback function for successful MQTT connection.

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

# Function to publish messages to MQTT broker.
def publish(client, method):
    if method == 'POST':
        student_mac_address = Student.objects.all().values_list('student_mac_address', flat=True)
        knownBLEAddDict = {str(i): add for i, add in enumerate(student_mac_address)}
        knownBLEAddJson = json.dumps(knownBLEAddDict)
        time.sleep(1)
        result = client.publish(pub_topic_data, knownBLEAddJson)
        status = result[0]
        if status == 0:
            print(f"Send {knownBLEAddJson} to topic `{pub_topic_data}`")
            return True
        else:
            print(f"Failed to send message to topic {pub_topic_data}")
            return False

# Function to subscribe to topics and handle received messages.
def subscribe(client: mqtt_client):
     def on_message(client, userdata, msg):
         print(f"Received {msg.payload.decode()} from {msg.topic} topic")

     client.subscribe(pub_topic_data)
     client.on_message = on_message

        
# Main function to initiate MQTT connection and perform actions.
def run():
     client = connect_mqtt()
     subscribe(client)
#     client.loop_forever()


# Overloaded run function to support publish operations.
def run(method='POST'):
    client = connect_mqtt()
    client.loop_start()
    publish(client, method)


# Run the script if executed as a standalone program.
if __name__ == '__main__':
    run()
