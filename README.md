# AIoT_Group_1

# ICT720 project

## Group 1
### Project brief

### Objectives
1. To implement **a waste segregation system** with an object detection camera
2. To create a database for the **point based reward** for different users
3. To build a **web interface** for point rewarding system

## User stories and acceptance criteria
1. As a **Student Affair Unit**, we want to **know which student threw trash properly** so that **we can reward that student**.
   * Scenario: **student threw trash**, given **student is in the database**, when **student threw bottles in the bottle bin**, then **POINTS will be rewarded**. 
   * Scenario: **student threw trash**, given **student is in the database**, when **student threw other types of trash into both of the bins**, then **POINTS will be reducted**.
2. As a **student**, I want to **see how many POINTS I have collected** so that **I can decide to cash out**.
   * Scenario: **student query**, given **he/she is in the database**, when **student is queried**, then **POINTS of that student is responsed**.
3. As a **Reward Center**, we want to **know how many points the student received** so that **we can give a proper reward to the student**.
   * Scenario: **student**, given **he/she came to cash out**, when **they have enough POINTS**, then **the reward is given**.
   * Scenario: **student**, given **he/she left**, when **the reward is given**, then **the POINTS will be reduced**.

## Impacts of the project
By proceeding this project, we can acquire the following impacts:
   1. Reduction in littering: By rewarding people for throwing trash in designated bins, the reward point system can motivate individuals to dispose of waste properly, 
      reducing littering in public spaces. 
   3. Increased recycling rates: The reward point system can encourage people to separate recyclable materials from non-recyclable waste, leading to an increase in           recycling rates.
   4. Reduced waste generation: As people become more conscious of the environmental impact of waste, they may reduce their overall waste generation, leading to a           reduction in the amount of waste that ends up in landfills or incinerators.
   5. Environmental conservation: Proper waste management conserves natural resources and prevents pollution, while a reward point system for throwing trash fosters         community ownership and responsibility while preventing pollution.
   6. Economic benefits:  Proper waste management can also create economic benefits by reducing costs associated with waste disposal, promoting resource conservation,       and generating revenue through recycling and waste-to-energy initiatives.

### Members
1. Limhourlaurent Meam (limhourlaurent.meam@dome.tu.ac.th)
2. Wetu Vexo (m6522040622@g.SIIT.tu.ac.th)
3. Aeint Shune Thar (aeint.shu@dome.tu.ac.th)
4. Khin Thandar Kyaw (khinthandar.k@live.ku.th)
5. Nyan Lin Mya (m6522040523@g.siit.tu.ac.th)
6. Hrang Kap Lian (hrangkap.l@live.ku.th)

### Hardware
![Picture of group 1 hardware](https://github.com/khinthandarkyaw98/ict720-project/blob/main/images/HW_group_1.jpg)
1. [ESP32-S3-Box](https://github.com/espressif/esp-box) (Espressif ESP32-S3-Box)
   * USB serial
   * LCD 240x320: ILI9342C
   * [6-axis IMU ICM-42607-P](https://invensense.tdk.com/products/motion-tracking/6-axis/icm-42670-p/)
2. [LILYGO T-Display-S3](https://github.com/Xinyuan-LilyGO/T-Display-S3) (Espressif ESP32-S3-DevKitC-1)
   * USB serial
   * LCD 170x320
3. [LILYGO T-Camera S3](https://www.lilygo.cc/products/t-camera-s3) (Espressif ESP32-S3-DevKitC-1)
   * USB serial
   * OV2640 camera module
   * OLED 128x64
4. [LILYGO T-Dongle S3](https://github.com/Xinyuan-LilyGO/T-Dongle-S3) (Espressif ESP32-S3-DevKitC-1)
   * USB serial
   * LCD 80x160
5. [LILYGO T-PicoC3](https://github.com/Xinyuan-LilyGO/T-PicoC3) (Espressif ESP32-C3-DevKitM-1)
   * Dual-processor with RP2040
   * LED 135x240


## Scope
1. Concepts: 
   * Lectures: L1(AIoT architecture), L2(software models), L3(), L4(), L5(), L6(), L7(), L8(), L9(), L10()
   * Practices: P1(cross-platform development/Bluetooth Low Energy), P2(multi-threading application), P3(), P4(), P6(), P7(), P8(), P9(), P10().
2. Skills:
   * Lectures: L1(user story), L2(UML diagram), L3(), L4(), L5(), L6(), L7(), L8(), L9(), L10().
   * Practices: P1(embedded programming/BLE programming), P2(state machine coding/RTOS programming), P3(), P4(), P6(), P7(), P8(), P9(), P10().
3. Tools: GitHub, VS Code, Platform.io, HiveMQ, 
4. Case study: MarTech using BLE beacon.

## User stories and acceptance criteria
1. As a **Student Affair Unit**, we want to **know which students properly throw what kind of trash to designated bins** so that **points can be rewarded**.
   * Scenario: **student**, given **he/she is in the database and near the trash bin**, when **student threw bottles to bottle bin**, then **POINTS will be rewarded to that person**. 
   * Scenario: **student**, **he/she is in the database and near the trash bin**, when **student threw other trash to both of the bins**, then **POINTS will be reducted from that person**.
2. As a **student**, I want to **see how many points I received** so that **I can decide to cash out as a specific reward**.
   * Scenario: **student query**, given **his/her records are in database**, when **queried**, then **POINTS of he/she is responsed**.
3. As a **Reward Center**, we want to **know how much POINTS each student received** so that **we can reward properly**.
   * Scenario: **student came in**, given **to cash out the reward**, when **they have enough POINTS**, then **the proper reward will be given**.
   * Scenario: **student**, given **cashed out**, when **they have got their reward**, then **the POINTS will be used**.

## System requirements
### Things layer:

### Gateway layer:

### Server layer:

### Service layer:

### UI layer:

## Software architecture
### ESP32 tag:

### ESP32 scanner:

### LINE bot:

### AI:

### LIFF UI: 

## Software implementation
### Firmware development

### LINE bot development

### LIFF UI development
