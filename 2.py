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

# Function to calculate steps
def calculate_steps(num_slices):
    gear_ratio = 5
    no_of_steps = 200
    steps_per_slice = (gear_ratio * no_of_steps) / num_slices
    return round(steps_per_slice)

# Streamlit app
def main():
    st.title("Cut-Urumbu")

    # Open ports
    st.sidebar.header("Port Control")
    port5_open = st.sidebar.checkbox("Open Port 6")
    port7_open = st.sidebar.checkbox("Open Port 7")

    ser5, ser7 = None, None

    if port5_open:
        ser5 = open_port('COM6')
    if port7_open:
        ser7 = open_port('COM7')

    # Homing option
    homing_button = st.sidebar.button("Perform Homing")

    if homing_button:
        # Perform homing procedure
        st.info("Homing procedure initiated...")

    # Input for number of slices
    st.header("Slice Calculation")
    num_slices = st.number_input("Enter number of slices", min_value=1, step=1, value=8)

    # Cut button
    if num_slices > 0:
        steps = calculate_steps(num_slices)
        st.write(f"Number of steps required for a slice: {steps}")

    if st.button("Cut"):
        st.info("Cutting procedure initiated...")
        for _ in range(num_slices):
            # Send acknowledgment to COM7 board
            ser7.write(b'1')
            
            # Wait for acknowledgment from COM7 board
            knife = ser7.read().decode().strip()
            if knife == '1':
                st.write("Cutting completed")
            
            # Calculate steps and send to COM5 board
            ser5.write(str(steps).encode())  # Convert steps to bytes before sending
            
            # Wait for acknowledgment from COM5 board
            table = ser5.read().decode().strip()
            if table == '1':
                st.write("Angle rotation complete")

if __name__ == "__main__":
    main()
