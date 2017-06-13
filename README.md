# IoT Corner
This repo aims to provide a playground on IoT in order to easily built/prototype IoT solutions/use cases.
We will support severals platform / sensors linked to services.

## Arduino
The first platform is [Arduino Yun Board](https://www.arduino.cc/en/Main/ArduinoBoardYun), which is the cheap and easy to use.

### Getting started on sensors
Please follow this [section](./arduino/README.md) to start using your Arduino Yun with some sensors.

### Use cases
Now that you've done the getting started, let's see some use cases:
* [IoT Alarm](./use_cases/iot_alarm/README.md): In this use case, we will see how to build a simple alarm connected to [Cisco Spark](https://www.ciscospark.com/) using two sensors (one [button](./arduino/button/README.md) and one [piezo buzzer](./arduino/piezo_buzzer/README.md)). This connected alarm will publish message to Cisco Spark using the [gateway](./sparkgw/README.md)
* more to come

## Raspberry Pi
Coming soon