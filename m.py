import streamlit as st
import serial

# Function to open serial port
def open_port(port):
    try:
        ser = serial.Serial(port, timeout=1)
        st.success(f"Port {port} opened successfully!")
        return ser
    except serial.SerialException:
        st.error(f"Failed to open port {port}. Make sure the port is available.")

# Streamlit app
def main():
    st.title("Motor Control")

    # Open port selection
    port = st.sidebar.selectbox("Select Port", ["COM6", "COM7"])

    # Open selected port
    ser = open_port(port)

    # Button to run the motor
    if st.button("Run Motor"):
        # Send control commands to Arduino
        ser.write(b'f')  # Signal to Arduino to run the motor

if __name__ == "__main__":
    main()
