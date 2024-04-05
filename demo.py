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
    port5_open = st.sidebar.checkbox("Open Port 5")
    port7_open = st.sidebar.checkbox("Open Port 7")

    ser5, ser7 = None, None

    if port5_open:
        ser5 = open_port('COM5')
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
    

        # Calculate steps per slice
    if num_slices > 0:
            steps = calculate_steps(num_slices)
            st.write(f"Number of steps required for a slice: {steps}")

    if st.button("Cut"):
        # Perform cutting procedure
        st.info("Cutting procedure initiated...")

if __name__ == "__main__":
    main()
