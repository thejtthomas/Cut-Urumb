int buttonPin = 27; // Define the pin connected to the button

void setup() {
  Serial.begin(9600); // Initialize serial communication
  pinMode(buttonPin, INPUT_PULLUP); // Set the button pin as an input with internal pull-up resistor
}

void loop() {
  if (digitalRead(buttonPin) == HIGH) {
    Serial.println("Button pressed");
    delay(1000); // debounce delay
  }
}
