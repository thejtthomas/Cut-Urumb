import streamlit as st
import serial.tools.list_ports
import time
import matplotlib.pyplot as plt
import numpy as np
from streamlit_extras.let_it_rain import rain
from streamlit_extras.customize_running import center_running

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
    explode = [0.1] * num_slices  # Explode each slice slightly for better visualization
    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    ax.set_title('See your Cake Slices')
    st.pyplot(fig)


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
    
    
    
    

    

    # Button to run the motor
    if st.sidebar.button("Cut Cake"):
        st.balloons()
        steps_per_slice = int((1 * 6400) / num_slices)  # Calculate steps per slice
        try:
            for _ in range(num_slices - 1):
                for ser in ser_ports:  # Iterate over selected ports
                    # Send control commands to Arduino for motor 1 ("f" motion)
                    for _ in range(steps_per_slice):
                        ser.write(b'f')  # Signal to Arduino to move motor 1 forward
                        time.sleep(speed/1000000)
                    time.sleep(2)  # Delay before changing motor

            for _ in range(num_slices - 2):
                for ser in ser_ports:  
                    # Send control commands to Arduino for motor 2 ("f" motion)
                    for _ in range(steps_per_slice):
                        ser.write(b'f')  # Signal to Arduino to move motor 2 forward
                        time.sleep(speed/1000000)
                    time.sleep(2)  # Delay before changing motor
        
        except serial.SerialException:
            st.error("Error occurred while sending commands to Arduino.")

       

    # Close serial ports
    for ser in ser_ports:
        if ser.isOpen():
            ser.close()

if __name__ == "__main__":
    main()
