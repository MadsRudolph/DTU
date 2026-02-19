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
  //1. Write a program that morse SOS - The simple way
  //S: . . .
  digitalWrite(ledPin, LOW);
  delay(timeUnit);
  digitalWrite(ledPin, HIGH);
  delay(timeUnit);
  
  digitalWrite(ledPin, LOW);
  delay(timeUnit);
  digitalWrite(ledPin, HIGH);
  delay(timeUnit);
  
  digitalWrite(ledPin, LOW);
  delay(timeUnit);
  digitalWrite(ledPin, HIGH);

  //Pause between letters is 3 timeunits
  delay(letterDelay);

  //O: - - -
  digitalWrite(ledPin, LOW);
  delay(dashUnit);
  digitalWrite(ledPin, HIGH);
  delay(timeUnit);

  
  digitalWrite(ledPin, LOW);
  delay(dashUnit);
  digitalWrite(ledPin, HIGH);
  delay(timeUnit);

  
  digitalWrite(ledPin, LOW);
  delay(dashUnit);
  digitalWrite(ledPin, HIGH);

  //Pause between letters is 3 timeunits
  delay(letterDelay);

  //S: . . .
  digitalWrite(ledPin, LOW);
  delay(timeUnit);
  digitalWrite(ledPin, HIGH);
  delay(timeUnit);
  
  digitalWrite(ledPin, LOW);
  delay(timeUnit);
  digitalWrite(ledPin, HIGH);
  delay(timeUnit);
  
  digitalWrite(ledPin, LOW);
  delay(timeUnit);
  digitalWrite(ledPin, HIGH);
  
  //Pause between Words is 7 timeunits
  delay(wordDelay);
}
