import streamlit as st
import serial.tools.list_ports
import time
import matplotlib.pyplot as plt
import numpy as np
import websocket

# Function to open serial port
def open_ports(ports):
    ser_ports = []
    for port in ports:
        try:
            ser = serial.Serial(port, timeout=5)
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

    # Tabs for different options
    tab1, tab2 = st.tabs(["Cake Cutting", "Extras"])

    with tab1:
        st.header("Cake cutting")
        # Input for number of slices
        num_slices = st.number_input("Enter number of slices", min_value=2, value=2)
        # Input for speed
        speed = st.number_input("Enter speed", min_value=0.1, value=1.0, step=0.1)
        # Display the pie chart
        generate_pie_chart(num_slices)
        
        # Button to run the motors
        if st.button("Cut Cake"):
            steps_per_slice = int((1 * 6400) / num_slices)  # Calculate steps per slice
            try:
                for i in range(num_slices - 1):
                    # Motor 1 ("f" motion)
                    for ser in ser_ports[:1]:
                        for _ in range(steps_per_slice):
                            ser.write(b'f')
                            time.sleep(speed / 1000000)
                        time.sleep(2)
                        # Motor 1 ("r" motion)
                        for _ in range(steps_per_slice):
                            ser.write(b'r')
                            time.sleep(speed / 1000000)
                        time.sleep(2)

                    # Motor 2 ("f" motion)
                    for ser in ser_ports[1:]:
                        for _ in range(steps_per_slice):
                            ser.write(b'f')
                            time.sleep(speed / 1000000)
                        time.sleep(2)

                # Send message to WebSocket server
                send_message("Cake cutting completed")

            except serial.SerialException:
                st.error("Error occurred while sending commands to Arduino.")

    with tab2:
        st.header("Additional Settings")
        # Additional tab for height and time
        with st.expander("Height and Time Settings"):
            height_of_cake = st.number_input("Enter height of the cake (in cm)")
            time_of_rotation = st.number_input("Enter time for endless rotation (in seconds)")

        # Motor 1 movement based on cake height
        for ser in ser_ports[:1]:
            # Send control commands to Arduino for motor 1 ("f" motion)
            while True:
                # Assume a step size of 1 cm, adjust according to your motor
                ser.write(b'f')
                time.sleep(speed / 1000000)
                current_height = ...  # You need to read the height sensor here
                if current_height >= height_of_cake:
                    break  # Stop motor 1 when height is reached

        # Motor 2 endless rotation
        start_time = time.time()
        for ser in ser_ports[1:]:
            while time.time() - start_time < time_of_rotation:
                # Send control commands to Arduino for motor 2 ("f" motion)
                ser.write(b'f')
                time.sleep(speed / 1000000)

    # Close serial ports
    for ser in ser_ports:
        if ser.isOpen():
            ser.close()

if __name__ == "__main__":
    main()
