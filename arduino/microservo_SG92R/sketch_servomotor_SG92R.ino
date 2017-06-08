#include <Servo.h> 
  
Servo monservo;  // crée l’objet pour contrôler le servomoteur 

void setup() {
  // put your setup code here, to run once:
  monservo.attach(9);  // utilise la broche 9 pour le contrôle du servomoteur 
  monservo.write(0); // positionne le servomoteur à 0° 

}

void loop() {
  monservo.write(0); 
  delay(1000); 
  monservo.write(90); 
  delay(1000); 
  monservo.write(100); 
  delay(1000); 
  monservo.write(110); 
  delay(1000); 
  monservo.write(120); 
  delay(1000); 
  monservo.write(130); 
  delay(1000); 
  monservo.write(140); 
  delay(1000); 
  monservo.write(150); 
  delay(1000); 
  monservo.write(160); 
  delay(1000); 
  monservo.write(170); 
  delay(1000); 
  monservo.write(180); 
}
