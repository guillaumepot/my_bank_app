"""
### STREAMLIT APP ###
"""

"""
LIBS
"""
import os
import requests
import streamlit as st

#from mybankpackage import available_account_types
available_account_types = ("checking", "savings")

"""
VARS
"""
api_version = os.getenv("API_VERSION")
api_url = os.getenv("API_URL")

"""
INIT
"""
# Initialize session state
if 'access_token' not in st.session_state:
    st.session_state.access_token = None


"""
UI
"""
## Sidebar ##


# Authentication
st.sidebar.title("Authentication")
st.sidebar.subheader("Log In")
login_username = st.sidebar.text_input("Username")
login_password = st.sidebar.text_input("Password", type="password")

# Login button
if st.sidebar.button("Log In"):
    login_data = {
        "grant_type": "",
        "username": login_username,
        "password": login_password,
        "scope": "",
        "client_id": "",
        "client_secret": ""
    }
    
    # Request API
    url = f"{api_url}/api/{api_version}/login"
    headers = {"accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, headers=headers, data=login_data)
    if response.status_code == 200:
        st.sidebar.success("Logged In Successfully!")
        access_token = response.json().get("access_token")
        st.session_state.access_token = access_token
        
    else:
        st.sidebar.error("Incorrect Username or Password.")
  

# Logout button
if st.session_state.access_token:
    st.sidebar.empty()
    st.sidebar.button("Log Out", on_click=lambda: st.session_state.pop('access_token'))
    st.sidebar.empty()



# Navigation
st.sidebar.title("Personal bank app")

# Pages
pages=["Settings"]
page=st.sidebar.radio("", pages)



## Page call ##

# Settings page
if page == pages[0]: 
    st.title("Settings")
    st.write("This is the settings page, use the options below to change the settings of the app.")

    # Settings
    if st.button("Check API status"):
        # Request API
        url = f"{api_url}/api/{api_version}/status"
        if response.status_code == 200:
            st.success(response.json())
        else:
            st.error("An error occurred while checking the API status.")


    if st.button("Create an account"):
        # Add account informations
        st.subheader("Please fill in the form below to create an account.")
        st.write("Name is free text")
        name = st.text_input("name")

        type = st.selectbox("Choose account type", available_account_types)

        st.write("Amount should be a number")
        amount = st.number_input("amount", format="%.2f")


        if st.button("Submit"):
            # Request API
            url = f"{api_url}/api/{api_version}/create/account?name={name}&type={type}&amount={amount}"
            if response.status_code == 200:
                st.success(response.json())
            else:
                st.error("An error occurred.")












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