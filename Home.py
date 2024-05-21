import streamlit as st



st.sidebar.write("Hello World")


st.title("Hello World")

import datetime
import streamlit as st

d = st.date_input("When's your birthday", format="DD/MM/YYYY")
st.write("Your birthday is:", d)