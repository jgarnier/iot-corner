# Sample code
Then load the [Rotary encoder sample code](./rotary_encoder.ino) in the Arduino IDE and download it to your Arduino:
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