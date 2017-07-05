#include <Process.h>
// constants won't change. They're used here to
// set pin numbers:
const int buttonPin = 2;     // the number of the pushbutton pin
const int ledPin =  13;      // the number of the LED pin

// variables will change:
int buttonState = 0;         // variable for reading the pushbutton status
int oneClick = 0;

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

void runCurl(String value){
  Process p;
  p.runShellCommand("curl -X POST -H \"X-Device-Secret: 12345\" \"http://54.246.192.181:8080/report?key=restroom_1" + value+"\" ");
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
    if(oneClick == 0){
      SerialUSB.print("Soap 1 pressed\n");
      runCurl("&label=soap_1&value=1");
      SerialUSB.print("http sent");
      oneClick = 1;
    }
  } else {
    // turn LED off:
    digitalWrite(ledPin, LOW);
    if(oneClick == 1 ){
      SerialUSB.print("end soap\n");
      oneClick=0;
     }
  }
}