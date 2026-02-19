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
  s();
  letterDelayFunc();
  o();
  letterDelayFunc();
  s();
  wordDelayFunc();
}

void s(){
  dot();
  sameLetterDelay();
  dot();
  sameLetterDelay();
  dot();
}

void o(){
  dash();
  sameLetterDelay();
  dash();
  sameLetterDelay();
  dash();
}

void dot() {
  digitalWrite(ledPin, LOW);
  delay(timeUnit);
  digitalWrite(ledPin, HIGH);
}

void dash() {
  digitalWrite(ledPin, LOW);
  delay(dashUnit);
  digitalWrite(ledPin, HIGH);
}

void sameLetterDelay(){
  delay(timeUnit);
}

void letterDelayFunc(){
  delay(letterDelay);
}

void wordDelayFunc(){
  delay(wordDelay);
}
