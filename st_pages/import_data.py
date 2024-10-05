import streamlit as st
import pandas as pd

from utils import constants, helpers


def import_data_page():
    print("render import_data_page2")
    session = helpers.cur_session()
    if len(session.buttons) == 0:
        st.title("Create Dataset")
        col1, col2 = st.columns(2)
        col1.button("Import Dataset from CSV", 
                    key=constants.BUTTON_IMPORT_FROM_CSV, 
                    on_click=session.add_button, 
                    args=[constants.BUTTON_IMPORT_FROM_CSV],
                    )
        col2.button("Copy-Paste Data into empty chart", 
                    key=constants.BUTTON_IMPORT_FROM_COPY_PASTE, 
                    on_click=session.new_page, 
                    args=[constants.PAGE_EDIT_DATA],
                    )

    elif constants.BUTTON_IMPORT_FROM_CSV in session.buttons:
        st.title("Import data from CSV")
        uploaded_file = st.file_uploader("Choose a CSV file", 
                                         type="csv", 
                                         key=constants.BUTTON_IMPORT_FROM_CSV)
        if uploaded_file is not None:

            df = pd.read_csv(uploaded_file)
            st.data_editor(df, use_container_width=True)
            session.data = df
            st.button("Continue", 
                        key=constants.BUTTON_CONTINUE,
                        on_click=session.new_page,
                        args=[constants.PAGE_VIEW_DATA, []]
                        )
            