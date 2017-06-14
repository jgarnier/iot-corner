/*
 
 All the resources for this project:
 http://randomnerdtutorials.com/
 
*/

int rainPin = A0;
int greenLED = 6;
int redLED = 7;
// you can adjust the threshold value
int thresholdValue = 800;

void setup(){
  pinMode(rainPin, INPUT);
  pinMode(greenLED, OUTPUT);
  pinMode(redLED, OUTPUT);
  digitalWrite(greenLED, LOW);
  digitalWrite(redLED, LOW);
  Serial.begin(9600);
}

void loop() {
  // read the input on analog pin 0:
  int sensorValue = analogRead(rainPin);
  Serial.print(sensorValue);
  if(sensorValue < thresholdValue){
    Serial.println(" - Doesn't need watering");
    digitalWrite(redLED, LOW);
    digitalWrite(greenLED, HIGH);
  }
  else {
    Serial.println(" - Time to water your plant");
    digitalWrite(redLED, HIGH);
    digitalWrite(greenLED, LOW);
  }

  // Example of posting measure through an HTTP POST
  //Process p;
  //String cmd = "curl --data \"moistureLevel="+sensorValue;
  //cmd = cmd + "\" http://mysite.com/soilmoisturesensor/12345";
  //p.runShellCommand(cmd);

  // Example of posting measure through an HTTP GET
  //Process p;
  //String cmd = "curl http://mysite.com/soilmoisturesensor/12345?moistureLevel="+sensorValue;
  //p.runShellCommand(cmd);

  delay(500);
}
