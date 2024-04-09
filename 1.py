import streamlit as st
import serial

# Function to open serial port
def open_port(port):
    try:
        ser = serial.Serial(port, timeout=20)
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

# Function to send steps to COM5 and receive acknowledgment
def send_steps_to_com5(ser, steps):
    if ser:
        ser.write(str(steps).encode())
        st.info(f"Sent {steps} steps to COM5")
        acknowledgment = ser.readline().decode().strip()
        st.success(acknowledgment)

# Streamlit app
def main():
    st.title("Cut-Urumbu")

    # Open COM5 port
    ser5 = open_port('COM5')

    # Homing option
    homing_button = st.sidebar.button("Perform Homing")

    if homing_button:
        # Perform homing procedure
        st.info("Homing procedure initiated...")

    # Input for number of slices
    st.header("Slice Calculation")
    num_slices = st.number_input("Enter number of slices", min_value=1, step=1, value=8)

    # Calculate steps per slice
    if num_slices > 0:
        steps = calculate_steps(num_slices)
        st.write(f"Number of steps required for a slice: {steps}")

    # Cut button
    if st.button("Cut"):
        # Send steps to COM5 and receive acknowledgment
        send_steps_to_com5(ser5, steps)
        

if __name__ == "__main__":
    main()
