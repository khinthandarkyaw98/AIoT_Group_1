# Everything Combined

This is the combination of every modules.

First this code will try to connect to WiFi

<img src="../media/connectWiFi.png" alt="Connect WiFi" style="display:block;float:none;margin-left:auto;margin-right:auto;width:40%"/>

and then will try to connect to MQTT broker.
<img src="../media/connectMQTT.png" alt="Connect MQTT" style="display:block;float:none;margin-left:auto;margin-right:auto;width:45%"/>

Then the server will send MQTT data every time there is an update in MAC address list. The received MQTT list will be saved in string array.

<img src="../media/mqtt_sent_received.png" alt="Connect MQTT" style="display:block;float:none;margin-left:auto;margin-right:auto;width:80%"/>

Found BLE addresses will be compared with the string array and if the RSSI is closed enough,

<img src="../media/found_dev.png" alt="MQTT BLE Addresses Sending and Receiving" style="display:block;float:none;margin-left:auto;margin-right:auto;width:50%"/>

the code will wait for the serial data from the Object Detection Model to send the **POINTS** and **MAC Address** to the database with HTTP POST.

<img src="../media/httpPost.png" alt="Connect MQTT" style="display:block;float:none;margin-left:auto;margin-right:auto;width:50%"/>

You may also use MQTT as an Publisher the code for the ESP32 and also for the server side is included in the repository.

<img src="../media/mqttPublish.png" alt="Connect MQTT" style="display:block;float:none;margin-left:auto;margin-right:auto;width:50%"/>

MQTT Subscribe for server side.

<img src="../media/mqttSubscribe.png" alt="Connect MQTT" style="display:block;float:none;margin-left:auto;margin-right:auto;width:50%"/>

The result of the request and subscription on server side.
<img src="../media/httpPostNmqttPub.png" alt="Connect MQTT" style="display:block;float:none;margin-left:auto;margin-right:auto;width:90%"/>