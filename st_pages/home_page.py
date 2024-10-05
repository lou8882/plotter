import streamlit as st
from utils import constants, helpers


def home_page():
    print("render home_page2")
    session = helpers.cur_session()

    st.title("Welcome to MappyMap")
    st.image("https://dgalywyr863hv.cloudfront.net/pictures/strava_o_auth/applications/56623/17689676/1/large.jpg")

    st.button("Get Started by Importing Data", 
              key=constants.BUTTON_IMPORT_DATA, 
              on_click=session.new_page,
              args=[constants.PAGE_IMPORT_DATA],
              type="primary"
              )