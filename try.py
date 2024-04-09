import serial
import time

arduino_led = serial.Serial(port='COM7', timeout=0)
arduino_button = serial.Serial(port='COM5', timeout=0)
time.sleep(2)

while True:
    if arduino_button.in_waiting:
        button_state = arduino_button.readline().strip()
        if button_state:
            print("Button pressed")
            arduino_led.write(b'1')  # Turn on the LED
            time.sleep(1)  # Delay to debounce the button
    else:
        arduino_led.write(b'0')  # Turn off the LED when the button is released
