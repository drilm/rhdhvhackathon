import streamlit as st


def get_results():
    st.write("Another line")


st.title("Hi I'm new")


st.button("Refresh", on_click=get_results())
