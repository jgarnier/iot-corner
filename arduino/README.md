# Arduino platform
Before going through some use case using a set of sensors, ensure you have a development environment and the right board, we will consider the [Arduino Yun Board](https://www.arduino.cc/en/Main/ArduinoBoardYun)

## Prerequisite

### Arduino IDE
Before using your Arduino board, download the [Arduino IDE](https://www.arduino.cc/en/Main/Software), we suggest not to use the online version as you will not be able to test everything.
In the tool menu, ensure you select the Arduino board and also the right port.

### Getting started with your Arduino Yun
In order to get started with the Arduino Yun, we will use a simple example & code to check your environment is well setup.
In term of hardware for this section, you will need:
1. Your Arduino Yun connect to your computer using the USB cable provided in the box
2. one [Breadboard](https://learn.adafruit.com/lesson-0-getting-started/breadboard) which is used to easily play with all sensors without having to use a soldering iron. Also you will need [wire](https://www.adafruit.com/product/153)
3. a [Rotary Encoder](https://www.adafruit.com/product/377)

#### Physical setup
For breadboard use, simply bend back the metal flaps on each side so that the knob will sit flat in the breadboard. Otherwise, those metal flaps can be attached to a mounting surface for increased stability. Then connect it to the Ardhuino following this schema:
![Rotatry encoder physical setup](./images/rotary_encoder.png)

#### Sample code
Then load the [Rotary encoder sample code](./src/rotary_encoder.ino) in the Arduino IDE and download it to your Arduino:
```
//Any digital pin for the push button effect if used.
int pushButton = 6;

//DO NOT CHANGE THESE PINS!  2 and 3 are special intrupt pins 
//on the Yun and can not be changed for another pin.
int encoderPinA = 3;
int encoderPinB = 2;

//helper set up:
volatile unsigned int encoderPos = 0;  // a counter for the dial
unsigned int lastReportedPos = 1;   // change management
static boolean rotating=false;      // debounce management
// interrupt service routine vars
boolean A_set = false;              
boolean B_set = false;


void setup() {
  pinMode(encoderPinA, INPUT_PULLUP);
  pinMode(encoderPinB, INPUT_PULLUP); 
  pinMode(pushButton, INPUT_PULLUP);

// encoder pin on interrupt 0 (pin 2)
  attachInterrupt(0, doEncoderA, CHANGE);
// encoder pin on interrupt 1 (pin 3)
  attachInterrupt(1, doEncoderB, CHANGE);

  Serial.begin(9600);
}


void loop() { 
  rotating = true;  // reset the debouncer

  if (lastReportedPos != encoderPos) {
    Serial.print("Index:");
    Serial.println(encoderPos, DEC);
    lastReportedPos = encoderPos;
  }
  
  //reset the counter to 0 if the button is pressed.
  if (digitalRead(pushButton) == LOW )  {
    encoderPos = 0;
    Serial.println("bien tu as appuyé sur le bouton");
  }
}

// Interrupt on A changing state
void doEncoderA(){
  // debounce
  if ( rotating ) delay (1);  // wait a little until the bouncing is done

  // Test transition, did things really change? 
  if( digitalRead(encoderPinA) != A_set ) {  // debounce once more
    A_set = !A_set;

    // adjust counter + if A leads B
    if ( A_set && !B_set ) 
      encoderPos += 1;

    rotating = false;  // no more debouncing until loop() hits again
  }
}

// Interrupt on B changing state, same as A above
void doEncoderB(){
  if ( rotating ) delay (1);
  if( digitalRead(encoderPinB) != B_set ) {
    B_set = !B_set;
    //  adjust counter - 1 if B leads A
    if( B_set && !A_set ) 
      encoderPos -= 1;

    rotating = false;
  }
}
```

Then once the program is running, on the Arduino IDE, open the serial monitor in order to see the output. If you turn the button, you should see the index value increasing/decreasing and if you push the button, it resets the index to 0