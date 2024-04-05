import streamlit as st
import serial.tools.list_ports
import time

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

    # Get available serial ports
    available_ports = serial.tools.list_ports.comports()
    port_names = [port.device for port in available_ports]

    # Open port selection
    selected_port = st.sidebar.selectbox("Select Port", port_names)

    # Open selected port
    ser = open_port(selected_port)

    # Input for number of slices and speed
    num_slices = st.number_input("Enter number of slices", min_value=1, value=1)
    speed = st.number_input("Enter speed (delay in seconds)", min_value=0.1, value=1.0, step=0.1)

    # Button to run the motor
    if st.button("Run Motor"):
        steps_per_slice = int((4 * 6400) / num_slices)  # Calculate steps per slice
        print(steps_per_slice)
        try:
            for _ in range(num_slices):
            
                # Send control commands to Arduino
                for _ in range(steps_per_slice):
                    ser.write(b'r')  # Signal to Arduino to move forward
                    time.sleep(speed/1000000)
                time.sleep(2)

                for _ in range(steps_per_slice):
                        ser.write(b'f')  # Signal to Arduino to move motor 1 backward
                        time.sleep(speed / 1000000)
                time.sleep(2)  # Delay before changing motor
        except serial.SerialException:
            st.error("Error occurred while sending commands to Arduino.")

    # Button to stop the motor
    if st.button("Stop Motor"):
        ser.write(b's')  # Signal to stop the motor

    

if __name__ == "__main__":
    main()
