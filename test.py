import serial
import time

# Sender (Board 1)
def sender():
    ser = serial.Serial('COM5', 9600)  # Adjust 'COM1' to match your serial port
    button_state = False  # Initialize button state

    while True:
        if button_state:
            ser.write(b'1')  # Sending '1' to indicate button press
        else:
            ser.write(b'0')  # Sending '0' to indicate button release
        button_state = not button_state  # Toggle button state
        time.sleep(0.1)  # Adjust delay as needed

# Start sender function in a thread
import threading
threading.Thread(target=sender).start()
