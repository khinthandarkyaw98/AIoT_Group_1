# Register BLE Detector

Proximity Detector for BLE Devices. Every availale BLE devices and then compare all those devices with the known BLE devices using loops.

Used **PlatformIO** extension from VS Code and **<Arduino.h>**. Also used **NimBLE** library.

You may change the name of the ```knownBLEAddresses``` inside ***main.cpp***.
```c++
String knownBLEAddresses[] = { "ff:ff:ff:ff:ff:ff", "ff:ff:ff:ff:ff:ff""};
```
You may also add more.

You may also change the ```RSSI_THRESHOLD``` for any desire values as this threshold will depend on the environment being noisy or not.

<img src="../media/found_dev.png" alt="BLE Tags" style="display:block;float:none;margin-left:auto;margin-right:auto;width:50%"/>

<video src="../media/found_reg_BLE.mp4" controls="controls" style="display:block;float:none;margin-left:auto;margin-right:auto;max-width: 1280px;"></video>