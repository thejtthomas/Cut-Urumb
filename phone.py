import streamlit as st
import serial.tools.list_ports
import time
import matplotlib.pyplot as plt
import numpy as np
import websocket
from PIL import Image

image=Image.open('cuturumbu.png')



st.set_page_config(page_title='Cut-Urumbu', page_icon='cuturumbu.png')

st.sidebar.image(image, width=275)


# Function to open serial port
def open_ports(ports):
    ser_ports = []
    for port in ports:
        try:
            ser = serial.Serial(port, timeout=1)
            st.sidebar.success(f"Port {port} opened successfully!")
            ser_ports.append(ser)
        except serial.SerialException:
            st.sidebar.error(f"Failed to open port {port}. Make sure the port is available.")
    return ser_ports

# Function to generate the pie chart
def generate_pie_chart(num_slices):
    labels = [f'Slice {i+1}' for i in range(num_slices)]
    sizes = np.ones(num_slices)
    explode = [0.05] * num_slices  # Explode each slice slightly for better visualization
    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    ax.set_title('See your Cake Slices')
    st.pyplot(fig)

# Function to send message to WebSocket server
def send_message(message):
    ws = websocket.create_connection("ws://192.168.33.86:8765")
    ws.send(message)
    ws.close()

# Streamlit app
def main():
    st.title("Cut-Urumbu🐜🍰")

    # Get available serial ports
    available_ports = serial.tools.list_ports.comports()
    port_names = [port.device for port in available_ports]

    # Open port selection
    selected_ports = st.sidebar.multiselect("Select Ports", port_names)

    # Open selected ports
    ser_ports = open_ports(selected_ports)

    # Input for number of slices
    num_slices = st.number_input("Enter number of slices", min_value=2, value=2)

    # Input for speed
    speed = st.number_input("Enter speed", min_value=0.1, value=1.0, step=0.1)

    # Display the pie chart
    generate_pie_chart(num_slices)

    # Button to run the motors
    if st.sidebar.button("Cut Cake"):
        
        steps_per_slice = int((1 * 6400) / num_slices)  # Calculate steps per slice
        try:
            # Alternate between motor 1 and motor 2%
            for i in range(num_slices):
                # Motor 1
                for ser in ser_ports[:1]:  # Iterate over the first selected port
                    # Send control commands to Arduino for motor 1 ("f" motion)
                    for _ in range(steps_per_slice):
                        ser.write(b'f')  # Signal to Arduino to move motor 1 forward
                        time.sleep(speed / 1000000)
                    time.sleep(2)  # Delay before changing motor
                    # Send control commands to Arduino for motor 1 ("r" motion)
                    for _ in range(steps_per_slice):
                        ser.write(b'r')  # Signal to Arduino to move motor 1 backward
                        time.sleep(speed / 1000000)
                    time.sleep(2)  # Delay before changing motor

                # Motor 2
                for ser in ser_ports[1:]:  # Iterate over the second selected port onwards
                    # Send control commands to Arduino for motor 2 ("f" motion)
                    for _ in range(steps_per_slice):
                        ser.write(b'f')  # Signal to Arduino to move motor 2 forward
                        time.sleep(speed / 1000000)
                    time.sleep(2)  # Delay before changing motor
            st.balloons()
        except serial.SerialException:
            st.error("Error occurred while sending commands to Arduino.")

    # Close serial ports
    for ser in ser_ports:
        if ser.isOpen():
            ser.close()

# Footer
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.text("Made at Super FabLab Kerala")
    st.markdown("---")
    st.text("Made by Laxmi, Kalyani, Thej, Nihal & Midhun")

if __name__ == "__main__":
    main()
