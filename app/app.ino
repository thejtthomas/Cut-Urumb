int ledPin = 26; // Define the pin connected to the LED

void setup() {
  Serial.begin(9600); // Initialize serial communication
  pinMode(ledPin, OUTPUT); // Set the LED pin as an output
}

void loop() {
  if (Serial.available() > 0) {
    char receivedChar = Serial.read(); // Read the incoming data from Python
    if (receivedChar == '1') {
      digitalWrite(ledPin, HIGH); // Turn on the LED if '1' is received
      Serial.println("LED turned on");
    } else if (receivedChar == '0') {
      digitalWrite(ledPin, LOW); // Turn off the LED if '0' is received
      Serial.println("LED turned off");
    }
  }
}
