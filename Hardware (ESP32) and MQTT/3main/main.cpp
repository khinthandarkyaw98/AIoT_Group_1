#include <Arduino.h>
#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEScan.h>
#include <BLEAdvertisedDevice.h>

#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <HTTPClient.h>
#include <esp_log.h>

#include <string>

#define LED 40
#define SPK 12

#define TAG             "MQTT TASK"

// static variables
const char* ssid = "";
const char* password = "";
const char* mqtt_client_id = "";
const char* mqtt_broker = "";
const int mqtt_port = ;
const char* pub_topic_data = "";
const char* sub_topic_data = "";

// static variables
static WiFiClient espClient;
static PubSubClient mqttClient(espClient);
static HTTPClient http;
static DynamicJsonDocument doc(1024);

// HTTP
const char* http_user_name = "";
const char* http_password = "";
const char* api_authToken = "";
const char* api_link = "";
// const char* api_link = "http://127.0.0.1:5000";
// const char* api_link = "http://192.168.1.169:5000";

String knownBLEAddresses[100];
int totalNumAdd = 0;

// RSSI & BLE
int RSSI_THRESHOLD = -30;
bool device_found;
int scanTime = 1; //In seconds
BLEScan* pBLEScan;

int gainPoint = 0;

String* parseJsonMessage(const char* message) {
  StaticJsonDocument<256> doc;
  DeserializationError error = deserializeJson(doc, message);
  if (error) {
    Serial.print(F("deserializeJson() failed: "));
    Serial.println(error.f_str());
    return NULL;
  }

  int numAddresses = doc.size();
  totalNumAdd = numAddresses;
  for (int i = 0; i < numAddresses; i++) {
    String address = doc[String(i)];
    knownBLEAddresses[i] = address;
  }

  return knownBLEAddresses;
}

void setupWifi() {
  // setup:
  // - connect to wifi
  delay(3000);
  Serial.println("\nConnecting to: ");
  Serial.println(ssid);
  WiFi.mode(WIFI_OFF);
  delay(200);
  WiFi.mode(WIFI_STA);
  delay(200);
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print("-");
    delay(500);
  }
  Serial.println("\nConnected to: ");
  Serial.println(ssid);
}

void mqtt_callback(char* topic, byte* payload, unsigned int length) {
    Serial.print("Received messages: ");
    Serial.println(topic);
    // for(int i=0; i<length; i++) {
    //     Serial.print((char) payload[i]);
    // }
    // Serial.println();
    // char buf[1024];
    // memcpy(buf, payload, length);
    // buf[length] = '\0';
    // Serial.println(buf);
    // deserializeJson(doc, buf);
    payload[length] = '\0'; // Terminate the payload string
    String message = String((char*)payload);
    Serial.println(message);
    String* bleAddresses = parseJsonMessage(message.c_str());
    int numAddresses = sizeof(bleAddresses) / sizeof(bleAddresses[0]);
    if (bleAddresses != NULL) {
      for (int i = 0; i < numAddresses; i++) {
        Serial.print(F("Address "));
        Serial.print(i);
        Serial.print(F(": "));
        Serial.println(bleAddresses[i]);
      }
    }
    // int numAddresses = doc.size();
    // for (int i = 0; i < numAddresses; i++) {
    //   String address = doc[String(i)];
    //   Serial.print(F("Address "));
    //   Serial.print(i);
    //   Serial.print(F(": "));
    //   Serial.println(address);
    // }
    // ESP_LOGW(TAG, "MQTT received: %s", buf);
}

void reconnect() {
  Serial.println("Connecting to MQTT Broker...");
  while (!mqttClient.connected()) {
      Serial.println("Reconnecting to MQTT Broker...");
      String clientId = mqtt_client_id;
      clientId += String(random(0xffff), HEX);
      
      if (mqttClient.connect(clientId.c_str())) {
        Serial.println("Connected to MQTT Broker.");
        // subscribe to topic
        mqttClient.subscribe(sub_topic_data);
      }
      
  }
}

void setupMQTT() {
  mqttClient.setServer(mqtt_broker, mqtt_port);
  // set the callback function
  mqttClient.setCallback(mqtt_callback);
  
  mqttClient.subscribe(sub_topic_data);

  if (!mqttClient.connected())
      reconnect();
}

void setup() {
  Serial.begin(115200); //Enable UART on ESP32
  // - connect to WiFi
  setupWifi();

  // - connect to mqtt broker
  setupMQTT();

  // BLE
  Serial.println("Scanning..."); // Print Scanning
  
  BLEDevice::init("");
  pBLEScan = BLEDevice::getScan(); //create new scan
  // pBLEScan->setAdvertisedDeviceCallbacks(); //Init Callback Function
  pBLEScan->setActiveScan(true); //active scan uses more power, but get results faster
  pBLEScan->setInterval(100); // set Scan interval
  pBLEScan->setWindow(99);  // less or equal setInterval value

  pinMode(LED, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (!mqttClient.connected())
  reconnect();
  mqttClient.loop();
  
  // To check knownBLEAddresses array
  // int numAddresses = sizeof(knownBLEaddresses) / sizeof(knownBLEaddresses[0]);
  // Serial.println("This is inside Forever LOOP!");
  // if (knownBLEaddresses != NULL) {
  //     for (int i = 0; i < totalNumAdd; i++) {
  //       Serial.print(F("Address "));
  //       Serial.print(i);
  //       Serial.print(F(": "));
  //       Serial.println(knownBLEaddresses[i]);
  //     }
  //   }

  BLEScanResults foundDevices = pBLEScan->start(scanTime, false);
  for (int i = 0; i < foundDevices.getCount(); i++)
  {
    BLEAdvertisedDevice device = foundDevices.getDevice(i);
    //Serial.printf("Advertised Device: %s %s\n", device.toString().c_str(), device.getAddress().toString().c_str());
    for (int j = 0; j < (sizeof(knownBLEAddresses) / sizeof(knownBLEAddresses[0])); j++)
    {   
      //Serial.printf("Found Advertised Device: %s %s %d\n", device.toString().c_str(), device.getAddress().toString().c_str(), device.getRSSI());
      // Serial.printf("%s: %s\n", device.getAddress().toString().c_str(), knownBLEAddresses[j].c_str());
      if(strcmp(device.getAddress().toString().c_str(), knownBLEAddresses[j].c_str()) == 0)
      {
        Serial.printf("Found Reg Device: %s %s %d\n", device.toString().c_str(), device.getAddress().toString().c_str(), device.getRSSI());
        int rssi = device.getRSSI();
        // Serial.print("RSSI: ");
        // Serial.println(rssi);
        if(device.getRSSI() > RSSI_THRESHOLD)
        {
          Serial.printf("Found Reg Device in Proximity: %s %s %d\n", device.toString().c_str(), device.getAddress().toString().c_str(), device.getRSSI());
          digitalWrite(LED, HIGH);

          if (Serial.available() > 0) {
            int recieve_signal = Serial.read() - '0'; // convert ASCII code to integer
            if (recieve_signal == 1) {
              gainPoint = gainPoint + 1;
            }
            else if(recieve_signal == -1) {
              gainPoint = gainPoint - 1;
            }
            // Serial.println(gainPoint); 
          }

          if (gainPoint != 0) {
          // Create a JSON object
          DynamicJsonDocument json(256);
          // knownBLEAddresses[j].c_str()
          // device.getAddress().toString().c_str()
          json["new_mac_address"] = knownBLEAddresses[j].c_str();
          json["new_point"] = gainPoint;
          // Convert the JSON object to a string
          String jsonString;
          serializeJson(json, jsonString);

          // HTTP POST
          http.begin(api_link);  // Replace with your server URL
          // http.addHeader("Authorization", api_authToken);
          http.setAuthorization(http_user_name, http_password);
          // Send the HTTP request
          http.addHeader("Content-Type", "application/json");
          int httpResponseCode = http.POST(jsonString);
          // Check the response code
          if (httpResponseCode > 0) {
            Serial.print("HTTP response code: ");
            Serial.println(httpResponseCode);
          } else {
            Serial.print("HTTP request failed: ");
            Serial.println(http.errorToString(httpResponseCode).c_str());
          }
          // Close the connection
          http.end();


          // MQTT publish
          // auto data = std::to_string(gainPoint);
          // mqttClient.publish(pub_topic_data, data.c_str());
          mqttClient.publish(pub_topic_data, jsonString.c_str());
          gainPoint = 0;
          }
          gainPoint = 0;
          delay(500);
        }
        else if(device.getRSSI() < RSSI_THRESHOLD) {
          digitalWrite(LED, LOW);
          gainPoint = 0;
          // Serial.println(gainPoint);
          delay(100);
        }
      }
    } 
  }
  pBLEScan->clearResults();   // delete results fromBLEScan buffer to release memory
  delay(100);
  delay(1000);
}