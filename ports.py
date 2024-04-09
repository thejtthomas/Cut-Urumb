import streamlit as st
import serial.tools.list_ports

def list_usb_ports():
    usb_ports = []
    ports = serial.tools.list_ports.comports()
    for port, desc, hwid in sorted(ports):
        if 'USB' in desc:
            usb_ports.append(port)
    return usb_ports

def main():
    st.title("List USB Ports")
    st.write("This app lists all the available USB ports on your system.")

    with st.spinner("Finding USB ports..."):
        usb_ports = list_usb_ports()

    if usb_ports:
        st.success(f"Found {len(usb_ports)} available USB ports:")
        st.write(usb_ports)
    else:
        st.error("No available USB ports found.")

if __name__ == "__main__":
    main()
