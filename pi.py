import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Function to generate the pie chart
def generate_pie_chart(num_slices):
    labels = [f'Slice {i+1}' for i in range(num_slices)]
    sizes = np.ones(num_slices)
    explode = [0.1] * num_slices  # Explode each slice slightly for better visualization
    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=140)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    ax.set_title('Distribution of Slices')
    st.pyplot(fig)

# Streamlit app
def main():
    st.title("Interactive Pie Chart")

    # Input for number of slices
    num_slices = st.number_input("Enter number of slices", min_value=1, value=1)

    # Generate the pie chart
    generate_pie_chart(num_slices)

if __name__ == "__main__":
    main()
