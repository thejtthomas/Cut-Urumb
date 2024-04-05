import streamlit as st

# Function to calculate steps
def steps_per_slices(num_slices):
    gear_ratio = 5
    no_of_steps = 200
    steps_per_slice = (gear_ratio * no_of_steps) / num_slices
    return round(steps_per_slice)

# Streamlit app
def main():
    st.title("Cake Slicer")

    # Input for number of slices
    num_slices = st.number_input("Enter number of slices", min_value=1, step=1, value=8)

    # Calculate steps per slice
    steps = steps_per_slices(num_slices)

    # Display result
    st.write(f"Number of steps required for a slice: {steps}")

if __name__ == "__main__":
    main()
