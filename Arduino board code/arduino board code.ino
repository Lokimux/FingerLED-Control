int ledPins[5] = {2, 3, 4, 5, 6};  // Define pins for the 5 LEDs

void setup() {
  for (int i = 0; i < 5; i++) {
    pinMode(ledPins[i], OUTPUT);
  }
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    int fingerCount = Serial.read() - '0';  // Convert from ASCII to integer

    for (int i = 0; i < 5; i++) {
      if (i < fingerCount) {
        digitalWrite(ledPins[i], HIGH);  // Turn on the LED
      } else {
        digitalWrite(ledPins[i], LOW);   // Turn off the LED
      }
    }
  }
}
