/*
/*
Exercise 1 - Morsing
Using ESP 8366 - meaning that LOW will turn the BuildInLED ON - in UNO LOW will turn the LED off
*/


//Let us define constants to be used in the program.
//These will be used throughout the entire program and not changed.

const byte ledPin = LED_BUILTIN;
const int timeUnit = 100;
const int dashUnit = timeUnit*3;
const int letterDelay = dashUnit;
const int wordDelay = timeUnit*7;


void setup() {
  pinMode(ledPin, OUTPUT);

}

void loop() {
  //S
  for (int i=0; i<3; i++){
    digitalWrite(ledPin, LOW);
    delay(timeUnit);
    digitalWrite(ledPin,HIGH);
    delay(timeUnit);
  }

  delay(timeUnit*2);
  //o
  for (int i=0; i<3; i++){
    digitalWrite(ledPin,LOW);
    delay(dashUnit);
    digitalWrite(ledPin,HIGH);
    delay(timeUnit);
  }

  delay(timeUnit*2);
   //S
  for (int i=0; i<3; i++){
    digitalWrite(ledPin, LOW);
    delay(timeUnit);
    digitalWrite(ledPin,HIGH);
    delay(timeUnit);
  } 
  delay(wordDelay);
}
