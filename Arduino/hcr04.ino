/*
 * created by Rui Santos, https://randomnerdtutorials.com
 * 
 * Complete Guide for Ultrasonic Sensor HC-SR04
 *
    Ultrasonic sensor Pins:
        VCC: +5VDC
        Trig : Trigger (INPUT) - Pin11
        Echo: Echo (OUTPUT) - Pin 12
        GND: GND
 */
 
int trigPinMiddle = 3;    // Trigger
int echoPinMiddle = 2;    // Echo
int trigPinLeft = 6;    // Trigger
int echoPinLeft = 7;    // Echo
int trigPinRight = 4;    // Trigger
int echoPinRight = 5;    // Echo
long duration, cmMiddle, cmLeft, cmRight;
unsigned long timedeb;
 
void setup() {
  //Serial Port begin
  Serial.begin (9600);
  //Define inputs and outputs
  pinMode(trigPinMiddle, OUTPUT);
  pinMode(echoPinMiddle, INPUT);
  
  pinMode(trigPinLeft, OUTPUT);
  pinMode(echoPinLeft, INPUT);
  
  pinMode(trigPinRight, OUTPUT);
  pinMode(echoPinRight, INPUT);
}
 
void loop() {
  // The sensor is triggered by a HIGH pulse of 10 or more microseconds.
  // Give a short LOW pulse beforehand to ensure a clean HIGH pulse:

  timedeb = millis();
  
  digitalWrite(trigPinMiddle, LOW);
  delayMicroseconds(5);
  digitalWrite(trigPinMiddle, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPinMiddle, LOW);
 
  // Read the signal from the sensor: a HIGH pulse whose
  // duration is the time (in microseconds) from the sending
  // of the ping to the reception of its echo off of an object.
  pinMode(echoPinMiddle, INPUT);
  duration = pulseIn(echoPinMiddle, HIGH);
 
  // Convert the time into a distance
  cmMiddle = (duration/2) / 29.1;     // Divide by 29.1 or multiply by 0.0343


//

  timedeb = millis();
  
  digitalWrite(trigPinLeft, LOW);
  delayMicroseconds(5);
  digitalWrite(trigPinLeft, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPinLeft, LOW);
 
  // Read the signal from the sensor: a HIGH pulse whose
  // duration is the time (in microseconds) from the sending
  // of the ping to the reception of its echo off of an object.
  pinMode(echoPinLeft, INPUT);
  duration = pulseIn(echoPinLeft, HIGH);
 
  // Convert the time into a distance
  cmLeft = (duration/2) / 29.1;     // Divide by 29.1 or multiply by 0.0343

 

//

  timedeb = millis();
  
  digitalWrite(trigPinRight, LOW);
  delayMicroseconds(5);
  digitalWrite(trigPinRight, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPinRight, LOW);
 
  // Read the signal from the sensor: a HIGH pulse whose
  // duration is the time (in microseconds) from the sending
  // of the ping to the reception of its echo off of an object.
  pinMode(echoPinRight, INPUT);
  duration = pulseIn(echoPinRight, HIGH);
 
  // Convert the time into a distance
  cmRight = (duration/2) / 29.1;     // Divide by 29.1 or multiply by 0.0343

  
  Serial.print("{\"type\":\"obstacle\",\"middle\":\"");
  Serial.print(cmMiddle);  
  Serial.print("\",\"left\":\"");  
  Serial.print(cmLeft);  
  Serial.print("\",\"right\":\"");  
  Serial.print(cmRight);
  Serial.println("\"}");
  
  delay(100);
}
