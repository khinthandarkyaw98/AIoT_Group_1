from paho.mqtt import client as mqtt_client
import random, time
import json

broker = ''
port = 
pub_topic_data = ""
client_id = f'id-{random.randint(0, 1000)}'

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

def publish(client):
    knownBLEAdd = ["ff:ff:ff:ff:ff:ff", "ff:ff:ff:ff:ff:ff",
                    "ff:ff:ff:ff:ff:ff", "ff:ff:ff:ff:ff:ff",
                    "ff:ff:ff:ff:ff:ff", "ff:ff:ff:ff:ff:ff",
                    "ff:ff:ff:ff:ff:ff"]
    
    knownBLEAddDict = {str(i): add for i, add in enumerate(knownBLEAdd)}

    # knownBLEAddJson = jsonify(knownBLEAddDict)
    knownBLEAddJson = json.dumps(knownBLEAddDict)
    time.sleep(1)
    result = client.publish(pub_topic_data, knownBLEAddJson)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{knownBLEAddJson}` to topic `{pub_topic_data}`")
    else:
        print(f"Failed to send message to topic {pub_topic_data}")

    #  while True:
    #      time.sleep(1)
    #      msg = f"messages: {msg_count}"
    #      result = client.publish(pub_topic_data, msg)
    #      # result: [0, 1]
    #      status = result[0]
    #      if status == 0:
    #          print(f"Send `{msg}` to topic `{pub_topic_data}`")
    #      else:
    #          print(f"Failed to send message to topic {pub_topic_data}")
    #      msg_count += 1

def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)

if __name__ == '__main__':
    run()

# def subscribe(client: mqtt_client):
#     def on_message(client, userdata, msg):
#         print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

#     client.subscribe(pub_topic_data)
#     client.on_message = on_message

# def run():
#     client = connect_mqtt()
#     subscribe(client)
#     client.loop_forever()