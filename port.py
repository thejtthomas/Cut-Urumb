import serial
import streamlit as st

# Function to open serial port
def open_port(port):
    try:
        ser = serial.Serial(port, timeout=1)
        st.success(f"Port {port} opened successfully!")
        return ser
    except serial.SerialException:
        st.error(f"Failed to open port {port}. Make sure the port is available.")

# Function to close serial port
def close_port(ser):
    if ser:
        ser.close()
        st.success(f"Port {ser.port} closed successfully!")

# Streamlit app
def main():
    st.title("Port Control")

    # Dropdown to select action for port 5
    action_port_5 = st.selectbox("Port 5:", ["Select action", "Open", "Close"])
    ser5 = None
    if action_port_5 == "Open":
        ser5 = open_port('COM5')
    elif action_port_5 == "Close":
        close_port(ser5)

    # Dropdown to select action for port 7
    action_port_7 = st.selectbox("Port 7:", ["Select action", "Open", "Close"])
    ser7 = None
    if action_port_7 == "Open":
        ser7 = open_port('COM7')
    elif action_port_7 == "Close":
        close_port(ser7)

    # Button to open both ports together
    if st.button("Open Both Ports"):
        ser5 = open_port('COM5')
        ser7 = open_port('COM7')

if __name__ == "__main__":
    main()
