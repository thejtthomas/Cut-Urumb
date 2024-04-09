import streamlit as st
import serial.tools.list_ports
import time
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

steps_per_mm_blade = 800       
steps_per_deg_table =  (7.067 * 6400)/360
cake_height=170 
cut_bottom_limit=254 
num_slices=2

speed= 1
speed_delay=1 / (1000000*speed)

ser_ports = []

# Importing the image
image = Image.open('cuturumbu.png')

# Setting up the Streamlit page configuration
st.set_page_config(page_title='Cut-Urumbu', page_icon='cuturumbu.png')

# Displaying the image in the sidebar
st.sidebar.image(image, width=275)

# Function to open serial ports
def open_ports(ports):
    for port in ports:
        try:
            ser = serial.Serial(port, timeout=1)
            st.sidebar.success(f"Port {port} opened successfully!")
            ser_ports.append(ser)
        except serial.SerialException:
            st.sidebar.error(f"Failed to open port {port}. Make sure the port is available.")

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
def home():
        try:
                ser = ser_ports[:1][0]
                global speed_delay
                response = ''
                while response != '0':
                    ser.write(b'?')  # Send command to check if motor is in home position
                    response = ser.read().decode().strip()
                    if response == '0':  # Motor is in home position
                        st.info("Motor is in home position.")
                        break
                    else:  # Motor is not in home position, move towards home
                        ser.write(b'r')  # Move motor towards home
                        time.sleep(speed_delay)

        except serial.SerialException:
            st.error("Error occurred while sending commands to Arduino.")

def setCutHeight():
    try:
        steps_to_set_height=int((cut_bottom_limit-cake_height)*steps_per_mm_blade)
        global speed_delay
        ser = ser_ports[:1][0]
        for _ in range(steps_to_set_height):
                ser.write(b'f')  # Signal to Arduino to move motor 1 backward
                time.sleep(speed_delay)
          
    except serial.SerialException:
            st.error("Error occurred while sending commands to Arduino.")


def cut():
    try:
        steps_per_slice_mm = int(steps_per_mm_blade*cake_height)
        global speed_delay
        # Motor 1
        ser = ser_ports[:1][0]
        print(ser)
            # Move Motor 1 backward (r) in steps_per_slice3
        for _ in range(steps_per_slice_mm):
                ser.write(b'f')  # Signal to Arduino to move motor 1 backward
                time.sleep(speed_delay)
        time.sleep(0.1)  # Delay before changing motor direction

            # Move Motor 1 backward (r) in steps_per_slice3
        for _ in range(steps_per_slice_mm):
                ser.write(b'r')  # Signal to Arduino to move motor 1 backward
                time.sleep(speed_delay)
               
    except serial.SerialException:
        st.error("Error occurred while sending commands to Arduino.")


def rotate():
    ser = ser_ports[1:][0]
    steps_per_slice = int(steps_per_deg_table*(360/num_slices))
    global speed_delay
    for _ in range(steps_per_slice):
        ser.write(b'f')  # Signal to Arduino to move motor 2 forward
        time.sleep(speed_delay)
    
    


# Streamlit app
def main():

    st.title("Cut-Urumbu🐜🍰")

    # Get available serial ports
    available_ports = serial.tools.list_ports.comports()
    port_names = [port.device for port in available_ports]

    # Open port selection
    selected_ports = st.sidebar.multiselect("Select Ports", port_names)

    # Open selected ports
    open_ports(selected_ports)
    print(ser_ports)
    # Input for number of slices
    global num_slices
    num_slices = st.number_input("Enter number of slices", min_value=2, value=2)

    # Input for speed
    global speed
    speed = st.number_input("Enter speed", min_value=0.01, value=1.00, step=0.01)
    global cake_height
    cake_height = st.number_input("Enter height of the cake (in mm)",min_value=0, value=0, step=1)
    global speed_delay
    speed_delay=1 / (100000000000*speed)
        

    # Display the pie chart
    generate_pie_chart(num_slices)

    

    if st.sidebar.button("Home"):# Return the motor to home position
        home()
    #setCutHeight()
   
    

    # Button to run the motors
    if st.sidebar.button("Cut Cake"):
        if cake_height == 0:
             st.error("Warning: Cake height is 0. Set a non-zero height value.")
        else:
            home()
            setCutHeight()

            for _ in range(num_slices):
                cut()
                rotate()
            st.balloons()
            home()

        

        
        # cut()
    
        

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
