"""
### STREAMLIT APP ###
"""

"""
LIBS
"""
import streamlit as st

## Sidebar ##

# Title
st.sidebar.title("Personal bank app")

# Pages
pages=["Home"]
page=st.sidebar.radio("", pages)



## Page call ##

# Home page
if page == pages[0]: 
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