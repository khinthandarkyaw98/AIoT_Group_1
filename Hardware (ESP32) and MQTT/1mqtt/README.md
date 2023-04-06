# MQTT BLE Address Collector

This code will receive known BLE addresses as JSON format from the web database using MQTT as a communication channel. You may also use **HTTP GET** method, however ICT720 course was taught mostly in MQTT. Therefore, we used MQTT as communication channel. We will use **HTTP POST** for data injection to the database for student points but that will be in the bleDetect and main code base.

Used **PlatformIO** extension from VS Code and **<Arduino.h>**. Also used **NimBLE**, **PubSubClient** & **ArduinoJson** library.

You may change ```ssid``` & ```password``` for WiFi, ```mqtt_client_id```, ```mqtt_broker``` & ```mqtt_port``` for your desire MQTT broker and ```pub_topic_data``` & ```sub_topic_data``` for your desire channels inside ***main.cpp***.

```c++
const char* ssid = "";
const char* password = "";
const char* mqtt_client_id = "";
const char* mqtt_broker = "";
const int mqtt_port = ;
const char* pub_topic_data = "";
const char* sub_topic_data = "";
```

After programmed the ESP32 device will be able to wait for the published data through ```sub_topic_data```. The data received should be in JSON format with **index** and **MAC address**. For example,
```json
{
    "0":"ff:ff:ff:ff:ff:ff",
    "1":"ff:ff:ff:ff:ff:ff"
}
```

After receiving the JSON of BLE addresses, those MAC addressess will be stored inside ```knownBLEaddresses``` with 100 indices. You may change the size as you see fit or may use dynamic array, as I do not really know how to use dynamic array in CPP.

On the right, you may see the testing done by python program for sending JSON of arrays of BLE addresses. Use ```requirements.txt``` and ```sendBLEAddList.py``` to test MQTT publish. Put the broker and port accordingly. ```pub_topic_data``` from python file and ```sub_topic_data``` from ```.cpp``` file should be matched.

On the left, you can see the data received through MQTT and then the prints with looping of ```knownBLEaddresses``` array.

<img src="../media/mqtt_sent_received.png" alt="MQTT BLE Addresses Sending and Receiving" style="display:block;float:none;margin-left:auto;margin-right:auto;width:100%"/>