import streamlit as st

st.set_page_config(
    page_title="Cut-Urumbu",
    page_icon="🐜",
)

tabs = st.tabs(["About", "Functions", "Contact"])

with tabs[0]:
    st.write("# About Cut-Urumbu")
    st.markdown(
        """
        Introducing Cut-Urumbu: The Innovative Cake Cutting Machine

        Cut-Urumbu, born out of the collaborative efforts of Kalyani, Laxmi, Thej, Midhun, and Nihal at Superfablab Kerala during Fab Academy 2024, revolutionizes the way we slice and serve cakes. Inspired by Neil Gershenfeld's Urumbu project at MIT, our team has adapted and enhanced the electronics to create a cutting-edge device that ensures equal portions with every slice.

        At its core, Cut-Urumbu is not just a machine; it's a testament to ingenuity and precision engineering. Whether you're hosting a birthday party, a wedding, or simply indulging in a sweet treat at home, Cut-Urumbu guarantees consistent, perfectly portioned slices every time.

        This website is your gateway to experiencing the seamless functionality of Cut-Urumbu.
        """
    )

with tabs[1]:
    st.write("# Functions")
    

with tabs[2]:
    st.write("# Contact")
    st.markdown(
        """
        

        ## Address
        Superfablab Kerala,
        Fab Academy 2024,
        Kerala, India.
        """
    )
