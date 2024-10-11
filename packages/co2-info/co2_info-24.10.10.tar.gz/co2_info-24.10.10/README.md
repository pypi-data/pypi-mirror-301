# CO<sub>2</sub> Info

## Purpose

The tiny foreground app helps you to decide when and how long to ventilate a room.

![Screenshot](./fig/screenshot_data.png)
*CO<sub>2</sub> Info app on a desktop, indicating the CO<sub>2</sub> concentration by color (here: green) and numerically (here: 482 ppm in room B206). The app can also be used for logging, annotating and plotting data.*

The app alerts the user by changing its background color, when the CO<sub>2</sub> concentration in a room passes certain limits. As provided here, **the script is configured for receiving data via MQTT from sensors in the IoT Network at the Technology-Campus Steinfurt**, but may be adapted for other situations. The tiny window should stay on top of all other windows, hopefully also in presentation mode.

## Installation

Please execute the following steps:

1. Make sure, Python 3.x is installed on your system. 

2. Use pip to install the app.
   ```
   pip install co2_info
   ```
   
3. Open a terminal and run the script:
   ```
   python -m co2_info --config .config
   ```
   Here, `.config`, is a simple text file, that contains your MQTT credentials. Example: 
   ```
   {
        "MQTT_USER": "username",
        "MQTT_PASSWD": "password",
   }
   ```
   If your MQTT broker allows anonymous subscription, just provide empty strings:
   ```
   {
        "MQTT_USER": "",
        "MQTT_PASSWD": "",
   }
   ```
