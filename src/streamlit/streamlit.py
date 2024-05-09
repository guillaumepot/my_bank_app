"""
### STREAMLIT APP ###
"""

"""
LIBS
"""
import streamlit as st




"""
VARS
"""
from vars import available_account_types



"""
UI
"""
## Sidebar ##

# Title
st.sidebar.title("Personal bank app")

# Pages
pages=["Settings"]
page=st.sidebar.radio("", pages)





## Page call ##

# Home page
if page == pages[0]: 
    st.title("Settings")
    st.write("This is the settings page, use the options below to change the settings of the app.")

    # Settings
    if st.button("Create an account"):
        # Add account informations
        st.subheader("Please fill in the form below to create an account.")
        st.write("Name is free text")
        st.text_input("name")
        st.write(f"Type should be one of these values: {available_account_types}")
        st.text_input("type")
        st.write("Amount should be a number")
        st.number_input("amount", format="%.2f")

        if st.button("Submit"):
            # Request API
            pass















"""
SIDEBAR FOOTER
"""
def addSidebarFooter():
    st.markdown("""
        <style>
        .reportview-container .main footer {visibility: hidden;}
        </style>
        """, unsafe_allow_html=True)

    footer="""
     <footer style="margin-top: 350px;">
        <p>Author: Guillaume Pot</p>
        <p>Email: <a href="mailto:guillaumepot.pro@outlook.com">guillaumepot.pro@outlook.com</a></p>
        <p>LinkedIn: <a href="https://www.linkedin.com/in/062guillaumepot/" target="_blank">Click Here</a></p>
    </footer>
    """
    st.sidebar.markdown(footer, unsafe_allow_html=True)

addSidebarFooter()