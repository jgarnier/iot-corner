int piezoPin = 9; // Declaring Piezo Buzzer on Pin 8

void setup()
{ 
}


void loop() 
{ // Starting the cycle functions below
   tone(piezoPin,1000); // Play a 1000Hz tone from the piezo (beep)
   delay(25); // wait a bit, change the delay for fast response.
   noTone(piezoPin); // stop the tone after 25 ms in this case 
   delay(25); // wait the amount of milliseconds in ldrValue
} // End of cycle functions 


