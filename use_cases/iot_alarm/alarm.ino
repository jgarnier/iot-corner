/*
  Button

 Turns on and off a light emitting diode(LED) connected to digital
 pin 13, when pressing a pushbutton attached to pin 2.


 The circuit:
 * LED attached from pin 13 to ground
 * pushbutton attached to pin 2 from +5V
 * 10K resistor attached to pin 2 from ground

 * Note: on most Arduinos there is already an LED on the board
 attached to pin 13.


 created 2005
 by DojoDave <http://www.0j0.org>
 modified 30 Aug 2011
 by Tom Igoe

 This example code is in the public domain.

 http://www.arduino.cc/en/Tutorial/Button
 */
#include <Process.h>
// constants won't change. They're used here to
// set pin numbers:
const int buttonPin = 2;     // the number of the pushbutton pin
const int ledPin =  13;      // the number of the LED pin
const int piezoPin = 9; // Declaring Piezo Buzzer on Pin 8

// variables will change:
int buttonState = 0;         // variable for reading the pushbutton status
int oneClick=0;

void setup() {

// Bridge takes about two seconds to start up
  // it can be helpful to use the on-board LED
  // as an indicator for when it has initialized
  pinMode(13, OUTPUT);
  digitalWrite(13, LOW);
  Bridge.begin();
  digitalWrite(13, HIGH);

  SerialUSB.begin(9600);

  while (!SerialUSB); // wait for a serial connection
}

void runCurl(String value) {
  Process p;    // Create a process and call it "p"
  p.begin("curl");  // Process that launch the "curl" command
  p.addParameter("﻿-k");
  p.addParameter("﻿-X");
  p.addParameter("POST");
  p.addParameter("-H");
  p.addParameter("X-Device-Secret:12345");
  //TODO: replace xxxxxx by the ngrok id
  p.addParameter("http://xxxxxx.ngrok.io/report?label=alarm&key=alarm&value="+value); 
  p.run();    // Run the process and wait for its termination

  // Print arduino logo over the Serial
  // A process output can be read with the stream methods
  while (p.available() > 0) {
    char c = p.read();
    SerialUSB.print(c);
  }
  // Ensure the last bit of data is sent.
  SerialUSB.flush();
}

void loop() {
  // read the state of the pushbutton value:
  buttonState = digitalRead(buttonPin);

  // check if the pushbutton is pressed.
  // if it is, the buttonState is HIGH:
  if (buttonState == HIGH) {
    // turn LED on:
    digitalWrite(ledPin, HIGH);
    tone(piezoPin,1000); // Play a 1000Hz tone from the piezo (beep)
    delay(1000); // wait a bit, change the delay for fast response.
    noTone(piezoPin); // stop the tone after 1s in this case 
    delay(1000); // wait the amount of milliseconds in ldrValue
    if(oneClick == 0){
     Serial.print("Alarm raised !!!!");
     runCurl("alarm%20raised%20zone%202");
     Serial.print("http sent");
     oneClick = 1;
   }
   
   
  } else {
    // turn LED off:
    digitalWrite(ledPin, LOW);
       noTone(piezoPin); // stop the tone after 1s in this case 
     if(oneClick==1){
      runCurl("end%20of%20alarm%20zone%202");
      oneClick=0;
     }
    
  }
}