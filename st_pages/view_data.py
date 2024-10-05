import streamlit as st
from utils import constants, helpers
from st_pages.edit_data import remove_data

def view_data_page():
    print("render view_data_page2")
    session = helpers.cur_session()
    if len(session.data) == 0:
        session.new_page(constants.PAGE_IMPORT_DATA)
        st.rerun()

    st.title("View Data")
    st.dataframe(session.data)
    
    col1, col2, col3 = st.columns(3)

    col1.button("Edit Data", 
                key=constants.BUTTON_EDIT_DATA, 
                on_click=session.new_page,
                args=[constants.PAGE_EDIT_DATA]
                )
    
    col2.button("Delete Data",
                key=constants.BUTTON_REMOVE_DATA,
                on_click=remove_data,
                args=[session])
    
    col3.button("Make Map",
                key=constants.BUTTON_GEN_MAP,
                on_click=session.new_page,
                args=[constants.PAGE_GEN_MAP]
                )
