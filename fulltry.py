import streamlit as st
import serial.tools.list_ports
import time
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

# Importing the image
image = Image.open('cuturumbu.png')

# Setting up the Streamlit page configuration
st.set_page_config(page_title='Cut-Urumbu', page_icon='cuturumbu.png')

# Displaying the image in the sidebar
st.sidebar.image(image, width=275)

# Function to open serial ports
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

# Function to return the motor to home position
def home(ser_ports):
    for ser in ser_ports[:1]:
        response = ''
        while response != '0':
            ser.write(b'?')  # Send command to check if motor is in home position
            response = ser.read().decode().strip()
            if response == '0':  # Motor is in home position
                st.info("Motor is in home position.")
                break
            else:  # Motor is not in home position, move towards home
                ser.write(b'r')  # Move motor towards home
                time.sleep(1/1000000000)

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
    speed = st.number_input("Enter speed", min_value=0.01, value=1.00, step=0.01)

    height = st.number_input("Enter height of the cake")

    # Display the pie chart
    generate_pie_chart(num_slices)

    # Return the motor to home position
    home(ser_ports)

    # Button to run the motors
    if st.sidebar.button("Cut Cake"):
        steps_per_slice1 = int((63.5 * 6400) / 2)
        steps_per_slice2 = int((7.067 * 6400) / num_slices)
        steps_per_slice3 = int((height * 6400) / num_slices)
        slice_counter = 0
        print(steps_per_slice1) # Calculate steps per slice
        print(steps_per_slice2)
        print(steps_per_slice3)
        try:
            # Alternate between motor 1 and motor 2%
            for ser in ser_ports[:1]:
                # Motor 1
                
                    # Move Motor 1 forward (f) in steps_per_slice1
                    for _ in range(steps_per_slice1):
                        ser.write(b'f')  # Signal to Arduino to move motor 1 forward
                        time.sleep(speed / 1000000)
                    time.sleep(0.5)  # Delay before changing motor direction
            for i in range(num_slices):
                # Motor 1
                for ser in ser_ports[:1]:

                    # Move Motor 1 backward (r) in steps_per_slice3
                    for _ in range(steps_per_slice3):
                        ser.write(b'r')  # Signal to Arduino to move motor 1 backward
                        time.sleep(speed / 1000000)
                    time.sleep(0.5)  # Delay before changing motor direction

                # Motor 2
                 # Counter for tracking the number of slices for Motor 2
                for ser in ser_ports[1:]:  # Iterate over the second selected port onwards
                    # Move Motor 2 forward (f) in steps_per_slice2
                    for _ in range(steps_per_slice2):
                        ser.write(b'f')  # Signal to Arduino to move motor 2 forward
                        time.sleep(speed / 1000000)
                    time.sleep(0.5)  # Delay before changing motor direction
                    

                for ser in ser_ports[:1]:

                    
                    if slice_counter == num_slices - 1:
                        break
                    else:
                        for _ in range(steps_per_slice3):
                            ser.write(b'f')  # Signal to Arduino to move motor 1 backward
                            time.sleep(speed / 1000000)
                        time.sleep(0.5)  # Delay before changing motor direction
                        slice_counter += 1  # Increment the slice counter for Motor 2

                    # If Motor 2 has completed num_slices - 1 slices, break the loop
                    

                

            st.balloons()
        except serial.SerialException:
            st.error("Error occurred while sending commands to Arduino.")

    # Close serial ports
    for ser in ser_ports:
        if ser.isOpen():
            ser.close()

    # Footer
    st.sidebar.markdown("---")
    st.sidebar.text("Made at Super FabLab Kerala")
    st.markdown("---")
    st.text("Made by Laxmi, Kalyani, Thej, Nihal & Midhun")

if __name__ == "__main__":
    main()
