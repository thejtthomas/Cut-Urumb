import streamlit as st
import serial.tools.list_ports
import time

# Function to open serial port
def open_ports(ports):
    ser_ports = []
    for port in ports:
        try:
            ser = serial.Serial(port, timeout=1)
            st.success(f"Port {port} opened successfully!")
            ser_ports.append(ser)
        except serial.SerialException:
            st.error(f"Failed to open port {port}. Make sure the port is available.")
    return ser_ports

# Function to close serial port
def close_port(ser):
    try:
        if ser.isOpen():
            ser.close()
            st.success(f"Port {ser.port} closed successfully!")
    except Exception as e:
        st.error(f"Error occurred while closing port {ser.port}: {e}")

# Function to get available serial ports
def get_available_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

# Streamlit app
def main():
    st.title("Motor Control")

    # Get available serial ports
    available_ports = get_available_ports()

    # Open port selection
    selected_ports = st.sidebar.multiselect("Select Ports", available_ports)

    # Open selected ports
    ser_ports = open_ports(selected_ports)

    # Input for delay
    delay = st.number_input("Enter delay (in seconds)", min_value=0.1, value=1.0, step=0.1)

    # Flag to control motor control loop
    motor_running = False

    # Button to run the motor
    if st.button("Run Motor"):
        motor_running = True
        try:
            while motor_running:
                # Send control commands to each Arduino
                for ser in ser_ports:
                    ser.write(b'f')  # Signal to Arduino to run motor 1
                    time.sleep(delay/10000)  # Delay
                    
        except serial.SerialException:
            st.error("Error occurred while sending commands to Arduino.")
            motor_running = False

    # Sidebar button for homing
    if st.sidebar.button("Perform Homing"):
        for ser in ser_ports:
            ser.write(b'h')  # Signal to Arduino to perform homing

    # Sidebar button to close port
    for ser in ser_ports:
        if st.sidebar.button(f"Close Port {ser.port}"):
            motor_running = False  # Stop motor control loop
            close_port(ser)



if __name__ == "__main__":
    main()
