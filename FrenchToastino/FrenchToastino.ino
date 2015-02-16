/*
  FrenchToastino
  
  Sets LEDs based on current French Toast Alert Level.
  Beeps on change.  Status/Error LED
  
  Author: Eric Dropps <eric@girderboot.com>
  Feb 15 2015
  Version 1.0
 */

int currentLevel = 0;
// the setup function runs once when you press reset or power the board
void setup() {
  
  // initialize serial communication:
  Serial.begin(9600);
  
  // French Toast LEDs
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
  
  // Buzzer
  pinMode(2, OUTPUT);
  
  // Status LED
  pinMode(3, OUTPUT);
}

void beep() {
  digitalWrite(2,HIGH);
  delay(50);
  digitalWrite(2,LOW);
}

// the loop function runs over and over again forever
void loop() {
  delay(10 * 1000);
  if (Serial.available() > 0) {
    int inByte = Serial.read();
    if (inByte != currentLevel) {
      // Clear Lights
      for (int thisPin = 5; thisPin < 12; thisPin++) {
        digitalWrite(thisPin, LOW);
      }
      // Set Lights
      switch (inByte) {
        case 'S':
          digitalWrite(11, HIGH);
         // break;
        case 'H':
          digitalWrite(10, HIGH);
       // break;
        case 'E':
          digitalWrite(9, HIGH);
        //break;
        case 'G':
          digitalWrite(6, HIGH);
        case 'L':
          digitalWrite(5, HIGH);
          // Report to serial, clear Error LED
          Serial.println("Updated");
          digitalWrite(3, LOW);
          break;
        default:
        // unknown signal, light error lamp
          digitalWrite(3, HIGH);
          Serial.println("ERROR");
      }
      // Beep
      beep();
      // Record current Level
      currentLevel = inByte;
    } else {
      Serial.println("No Change");
    }
  }
}
