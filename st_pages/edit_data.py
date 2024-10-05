import streamlit as st
import pandas as pd

from utils import constants, helpers
from utils.session_data import SessionData


@st.dialog("Edit Data")
def add_column(session: SessionData) -> None:
    col1, col2 = st.columns([.2,.8])
    col_name = col2.text_input("New Column Name", 
                    key=constants.INPUT_ADD_COL_NAME,
                    placeholder="New Column Name", 
                    label_visibility="collapsed",
                    )

    add_col = col1.button("Add Column", 
                    key=constants.BUTTON_ADD_COLUMN_NOW, 
                    )
    if add_col or col_name != "": 
        session.add_column(col_name)
        st.rerun()


@st.dialog("Remove Columns", width="large")
def remove_columns(session: SessionData) -> None:
    st.text("Please select all columns you wish to remove")
    columns = st.multiselect("Columns", 
                            key=constants.LABEL_COL_NAME,
                            options=session.data.columns,
                            )
    remove = st.button("Remove", 
                       disabled=(columns == None or len(columns) == 0))
    if columns != None and remove:
        for column in columns:
            session.remove_column(column)

        st.rerun()
    if st.button("Back"):
        st.rerun()


@st.dialog("Delete Data")
def remove_data(session: SessionData) -> None:
    st.text("Are you sure you want to delete your data?")
    col1, col2 = st.columns(2)
    if col1.button("Yes"):
        del session.data
        del session.buttons
        session.new_page(constants.PAGE_IMPORT_DATA)
        st.rerun()
    if col2.button("No"):
        st.rerun()
        

@st.dialog("Append Latitude and Longitude Data", width="large")
def add_lat_lon_to_data(session: SessionData):
    address_col = st.selectbox("Please select the column containing the street address",
                               options=session.data.columns,
                               index=None,
                               )
    if address_col != None:
        add_btn = st.button("Add Lat/Lon Now", 
                  key=constants.BUTTON_CONTINUE,
                  )
        if add_btn:
            helpers.add_address_data(session, address_col)
    if st.button("Close"):
        # del st.session_state[constants2.BUTTON_ADD_LAT_LON]
        st.rerun()


@st.dialog("Parse Data From Existing Field", width="large")
def parse_data_from_existing_field(session: SessionData):
    
    delimiter_caption = f"'Taco - Cat' -> 'Taco' OR 'Cat'"
    regex_caption = f"eg 'Address 123 (TC)' -> 'TC'"

    col_name = st.selectbox("Column",
                            key=constants.SELECT_COLUMN_NAME,
                            options=session.data.columns,
                            index=None)

    parse_type = st.radio("Parse by", 
                          key=constants.BUTTON_PARSE_TYPE,
                          options=[constants.LABEL_DELIMITER, constants.LABEL_REGEX],
                          horizontal=True,
                          captions=[delimiter_caption, regex_caption],
                          index=None,
                        )
     
    if parse_type == constants.LABEL_DELIMITER and col_name:
        st.subheader("Parse by Delimiter")
        delimiter = st.text_input("Delimiter", 
                                  key=constants.TEXT_BOX_DELIMITER,
                                  placeholder="Eg '-', '@', '/', etc",
                                  )
        
        delimiter_before_caption = f"'Taco {delimiter} Cat' -> 'Taco'"
        delimiter_after_caption = f"'Taco {delimiter} Cat' -> 'Cat'"

        delimiter_index = st.radio("Delimiter Index - Before or After",
                 key=constants.RADIO_DELMITER_INDEX,
                 options = [
                    constants.BUTTON_BEFORE, 
                    constants.BUTTON_AFTER,
                    ],
                    captions=[delimiter_before_caption, delimiter_after_caption],
                    index=None,
                    horizontal=True,
                )
        if delimiter != "" and delimiter_index != "":
            sample_button = st.button("Get Sample",
                                key=constants.BUTTON_SAMPLE)
            if sample_button:
                sample_df = helpers.parse_from_existing_column(session.data.head(2),
                                                               parse_type=constants.LABEL_DELIMITER,
                                                               ref_col=col_name,
                                                               new_col_name='sample output',
                                                               expression=delimiter,
                                                               delimiter_index=0)
                st.dataframe(sample_df[[col_name, 'sample output']])

            col1, col2 = st.columns([.2,.8])
            new_col_name = col2.text_input("Column Name", 
                                        key=constants.INPUT_ADD_COL_NAME,
                                        placeholder="New Column Name",
                                        label_visibility="collapsed")
            add_col = col1.button("Add Column", 
                                  key=constants.BUTTON_ADD_COLUMN,
                                  disabled=(new_col_name==""),
                                  )
            if add_col:
                new_df = helpers.parse_from_existing_column(session.data,
                                            parse_type=constants.LABEL_DELIMITER,
                                            ref_col=col_name,
                                            new_col_name=new_col_name,
                                            expression=delimiter,
                                            delimiter_index=(0 if delimiter_index == constants.BUTTON_BEFORE else 1),
                                            )
                session.data = new_df
                st.rerun()
    
    elif parse_type == constants.LABEL_REGEX and col_name:
        st.subheader("Parse by Regex")
        regex = st.text_input("Regex", 
                    key=constants.TEXT_BOX_REGEX,
                    placeholder="Eg '\((.{1,3})\)'",
                    )
        if regex != "":
            sample_button = st.button("Get Sample",
                                key=constants.BUTTON_SAMPLE)
            if sample_button:
                sample_df = helpers.parse_from_existing_column(session.data.head(2),
                                                               parse_type=constants.LABEL_REGEX,
                                                               ref_col=col_name,
                                                               new_col_name='sample output',
                                                               expression=regex)
                st.dataframe(sample_df[[col_name, 'sample output']])

            col1, col2 = st.columns([.2,.8])
            new_col_name = col2.text_input("Column Name", 
                                        key=constants.INPUT_ADD_COL_NAME,
                                        placeholder="New Column Name",
                                        label_visibility="collapsed")
            add_col = col1.button("Add Column", 
                                  key=constants.BUTTON_ADD_COLUMN,
                                  disabled=(new_col_name==""),
                                  )
            if add_col:
                new_df = helpers.parse_from_existing_column(session.data,
                                            parse_type=constants.LABEL_REGEX,
                                            ref_col=col_name,
                                            new_col_name=new_col_name,
                                            expression=regex, 
                                            )
                session.data = new_df
                st.rerun()



    go_back = st.button("Back")
    if go_back:
        st.rerun()


def edit_data_page():
    print("Render edit_data_page2")
    st.title("Edit Data")
    session = helpers.cur_session()
    
    df = session.data
    edited_df = st.data_editor(session.data, 
                               num_rows="dynamic", 
                               width=1000
                               )
    if len(df.columns) == 0:
        if st.button("Add Column", key=constants.BUTTON_ADD_COLUMN):
            add_column(session)
    else: 
        col1, col2, col3 = st.columns(3)
        col1.subheader("Edit Data")
        if col1.button("Save Changes", use_container_width=True):
            session.data = edited_df
        if col1.button("Add Column", key=constants.BUTTON_ADD_COLUMN, use_container_width=True):
            add_column(session)
        if col1.button("Remove Columns", key=constants.BUTTON_REMOVE_COLUMN, use_container_width=True):
            remove_columns(session)
        if col1.button("Delete Dataset", key=constants.BUTTON_REMOVE_DATA, use_container_width=True):
            remove_data(session)

        col2.subheader("Helpers")
        if col2.button("Lat/Lon from street address", key=constants.BUTTON_ADD_LAT_LON, use_container_width=True):
            add_lat_lon_to_data(session)
        if col2.button("Parse Data From Column", key=constants.BUTTON_PARSE_FROM_COLUMN, use_container_width=True):
            parse_data_from_existing_field(session)

        col3.subheader("Continue")
        col3.button("Continue", 
                    key=constants.BUTTON_VIEW_DATA,
                    on_click=session.new_page,
                    args=[constants.PAGE_VIEW_DATA],
                    use_container_width=True)