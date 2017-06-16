
/*  PulseSensor™ Starter Project   http://www.pulsesensor.com
 *
This an Arduino project. It's Best Way to Get Started with your PulseSensor™ & Arduino.
-------------------------------------------------------------
1) This shows a live human Heartbeat Pulse.
2) Live visualization in Arduino's Cool "Serial Plotter".
3) Blink an LED on each Heartbeat.
4) This is the direct Pulse Sensor's Signal.
5) A great first-step in troubleshooting your circuit and connections.
6) "Human-readable" code that is newbie friendly."

*/

#include <Process.h>

//  Variables
int PulseSensorPurplePin = 0;        // Pulse Sensor PURPLE WIRE connected to ANALOG PIN 0
int LED13 = 13;   //  The on-board Arduion LED


int Signal;                // holds the incoming raw data. Signal value can range from 0-1024
int Threshold = 550;            // Determine which Signal to "count as a beat", and which to ingore.


// The SetUp Function:
void setup() {
  // Initialize Bridge
  Bridge.begin();
  
  pinMode(LED13,OUTPUT);         // pin that will blink to your heartbeat!
  Serial.begin(9600);         // Set's up Serial Communication at certain speed.

  // Wait until a Serial Monitor is connected.
  while (!Serial);
  
}


//String BACKEND_URL = "http://52c8954e.ngrok.io/soilmoisturesensor/54321";
String BACKEND_URL = "ec2-34-211-171-155.us-west-2.compute.amazonaws.com:3001/soilmoisturesensor/54321";

void doCurl(int sensorValue) {
  Serial.println(String("Sending Curl to ")+BACKEND_URL);

  Process p;
  p.begin("curl");
  //p.addParameter("http://www.google.fr");
  p.addParameter( BACKEND_URL+String("?moistureLevel=")+String(sensorValue));
  p.run();

  // A process output can be read with the stream methods
  while (p.available()>0) {
    char c = p.read();
    Serial.print(c);
  }
  Serial.flush();
  
  p.run();
}


// The Main Loop Function
void loop() {

  Signal = analogRead(PulseSensorPurplePin);  // Read the PulseSensor's value.
                                              // Assign this value to the "Signal" variable.

   Serial.println(Signal);                    // Send the Signal value to Serial Plotter.
   
   doCurl(Signal);


   if(Signal > Threshold){                          // If the signal is above "550", then "turn-on" Arduino's on-Board LED.
     digitalWrite(LED13,HIGH);
   } else {
     digitalWrite(LED13,LOW);                //  Else, the sigal must be below "550", so "turn-off" this LED.
   }

   delay(4000);
}
