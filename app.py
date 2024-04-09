import serial
import streamlit as st

# Function to toggle LED
def toggle_led(led_state):
    try:
        with serial.Serial('COM5', timeout=0) as ser:
            ser.write(led_state.encode())
            if led_state == '1':
                st.success("LED turned on")
            elif led_state == '0':
                st.warning("LED turned off")
    except serial.SerialException:
        st.error("Failed to open COM5. Make sure the port is available.")

# Streamlit app
def main():
    st.title("LED Control")

    # Checkbox to toggle LED
    led_state = st.checkbox("Toggle LED")

    # If checkbox is checked, turn LED on, otherwise turn it off
    if led_state:
        toggle_led('1')
    else:
        toggle_led('0')

if __name__ == "__main__":
    main()
