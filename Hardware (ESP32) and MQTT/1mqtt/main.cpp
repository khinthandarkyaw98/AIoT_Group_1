#include <Arduino.h>
#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEScan.h>
#include <BLEAdvertisedDevice.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <esp_log.h>

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
static DynamicJsonDocument doc(1024);

String knownBLEaddresses[100];
int totalNumAdd = 0;

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
    knownBLEaddresses[i] = address;
  }

  return knownBLEaddresses;
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
  Serial.print(ssid);
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
      Serial.println("Reconnecting to MQTT Broker..");
      String clientId = mqtt_client_id;
      clientId += String(random(0xffff), HEX);
      
      if (mqttClient.connect(clientId.c_str())) {
        Serial.println("Connected.");
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
}

void loop() {
  // put your main code here, to run repeatedly:
  if (!mqttClient.connected())
  reconnect();
  mqttClient.loop();
  //int numAddresses = sizeof(knownBLEaddresses) / sizeof(knownBLEaddresses[0]);
  Serial.println("This is inside Forever LOOP!");
  if (knownBLEaddresses != NULL) {
      for (int i = 0; i < totalNumAdd; i++) {
        Serial.print(F("Address "));
        Serial.print(i);
        Serial.print(F(": "));
        Serial.println(knownBLEaddresses[i]);
      }
    }

    delay(5000);
}