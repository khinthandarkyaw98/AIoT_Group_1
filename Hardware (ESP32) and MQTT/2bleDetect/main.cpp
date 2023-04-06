#include <Arduino.h>
#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEScan.h>
#include <BLEAdvertisedDevice.h>
#include <Adafruit_NeoPixel.h>

#ifdef __AVR__
 #include <avr/power.h> // Required for 16 MHz Adafruit Trinket
#endif

#define NEOPIX 46
#define NUMPIXELS 1
#define DELAYVAL 500

#define LED 40
#define SPK 12

Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUMPIXELS, NEOPIX, NEO_GRB + NEO_KHZ800);

String knownBLEAddresses[] = { "ff:ff:ff:ff:ff:ff", "ff:ff:ff:ff:ff:ff",
                               "ff:ff:ff:ff:ff:ff", "ff:ff:ff:ff:ff:ff",
                               "ff:ff:ff:ff:ff:ff", "ff:ff:ff:ff:ff:ff",
                               "ff:ff:ff:ff:ff:ff"};
int RSSI_THRESHOLD = -38;
bool device_found;
int scanTime = 1; //In seconds
BLEScan* pBLEScan;

class MyAdvertisedDeviceCallbacks: public BLEAdvertisedDeviceCallbacks {
    void onResult(BLEAdvertisedDevice advertisedDevice) {
      // for (int i = 0; i < (sizeof(knownBLEAddresses) / sizeof(knownBLEAddresses[0])); i++)
      // {
      //   // Uncomment to Enable Debug Information
      //   // Serial.println("*************Start**************");
      //   // Serial.println(sizeof(knownBLEAddresses));
      //   // Serial.println(sizeof(knownBLEAddresses[0]));
      //   // Serial.println(sizeof(knownBLEAddresses)/sizeof(knownBLEAddresses[0]));
      //   // Serial.println(advertisedDevice.getAddress().toString().c_str());
      //   // Serial.println(knownBLEAddresses[i].c_str());
      //   // Serial.println("*************End**************");
      //   if (strcmp(advertisedDevice.getAddress().toString().c_str(), knownBLEAddresses[i].c_str()) == 1)
      //   {
      //     device_found = true;
      //     break;
      //   }
      //   else
      //     device_found = false;
      // }
      // Serial.printf("Advertised Device: %s \n", advertisedDevice.toString().c_str());
    }
};

void setup() {
  Serial.begin(115200); //Enable UART on ESP32
  #if defined(__AVR_ATtiny85__) && (F_CPU == 16000000)
    clock_prescale_set(clock_div_1);
  #endif
  Serial.println("Scanning..."); // Print Scanning
  
  strip.begin();
  strip.setBrightness(50);
  strip.show(); // Initialize all pixels to 'off'

  BLEDevice::init("");
  pBLEScan = BLEDevice::getScan(); //create new scan
  pBLEScan->setAdvertisedDeviceCallbacks(new MyAdvertisedDeviceCallbacks()); //Init Callback Function
  pBLEScan->setActiveScan(true); //active scan uses more power, but get results faster
  pBLEScan->setInterval(100); // set Scan interval
  pBLEScan->setWindow(99);  // less or equal setInterval value

  pinMode(LED, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:

  // digitalWrite(39, HIGH);
  // delay(3000);
  // digitalWrite(39, LOW);
  BLEScanResults foundDevices = pBLEScan->start(scanTime, false);
  for (int i = 0; i < foundDevices.getCount(); i++)
  {
    BLEAdvertisedDevice device = foundDevices.getDevice(i);
    //Serial.printf("Advertised Device: %s %s\n", device.toString().c_str(), device.getAddress().toString().c_str());
    for (int j = 0; j < (sizeof(knownBLEAddresses) / sizeof(knownBLEAddresses[0])); j++)
    {   
        //Serial.printf("Found Reg Device: %s %s %d\n", device.toString().c_str(), device.getAddress().toString().c_str(), device.getRSSI());
        //Serial.printf("%s: %s\n", device.getAddress().toString().c_str(), knownBLEAddresses[j].c_str());
        if(strcmp(device.getAddress().toString().c_str(), knownBLEAddresses[j].c_str()) == 0)
        {
            // Serial.printf("Found Reg Device: %s %s %d\n", device.toString().c_str(), device.getAddress().toString().c_str(), device.getRSSI());
            int rssi = device.getRSSI();
            // Serial.print("RSSI: ");
            // Serial.println(rssi);
            if(device.getRSSI() > RSSI_THRESHOLD)
            {
                Serial.printf("Found Reg Device in Proximity: %s %s %d\n", device.toString().c_str(), device.getAddress().toString().c_str(), device.getRSSI());
                digitalWrite(LED, HIGH);
                delay(500);
            }
            else if(device.getRSSI() < RSSI_THRESHOLD) {
                digitalWrite(LED, LOW);
                delay(100);
            }
        }
    } 
  }
  pBLEScan->clearResults();   // delete results fromBLEScan buffer to release memory
  delay(100);
}