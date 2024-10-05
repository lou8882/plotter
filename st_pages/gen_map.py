import streamlit as st
from utils import constants, helpers
from utils.session_data import SessionData


# @st.dialog("Create the Map")
# def create_map_form(session: SessionData) -> None:
#     # col1, col2 = st.columns([.2, .8])
#     lat_column = st.selectbox("Column Containing Latitude",
#                             key=constants2.SELECTBOX_LAT_COL,
#                             options=session.data.columns,
#                             index=None)
    
#     lon_column = st.selectbox("Column Containing Longitude",
#                             key=constants2.SELECTBOX_LON_COL,
#                             options=session.data.columns,
#                             index=None)
    
#     color_col = st.selectbox("(Optional) Column for color coding",
#                             key=constants2.SELECTBOX_COLOR,
#                             options=session.data.columns,
#                             index=None)
    
#     if lat_column != "" and lon_column != "":
#         if st.button("Continue",
#                      key=constants2.BUTTON_CONTINUE,
#                      on_click=)
    

def gen_map_page():
    st.title("Create map")
    session = helpers.cur_session()


    # col1, col2 = st.columns([.2, .8])
    lat_column = st.selectbox("Column Containing Latitude",
                            key=constants.SELECTBOX_LAT_COL,
                            options=session.data.columns,
                            index=None)
    
    lon_column = st.selectbox("Column Containing Longitude",
                            key=constants.SELECTBOX_LON_COL,
                            options=session.data.columns,
                            index=None)
    
    color_col = st.selectbox("(Optional) Column for color coding",
                            key=constants.SELECTBOX_COLOR,
                            options=session.data.columns,
                            index=None)
    
    if lat_column and lon_column:
        print(f"cat_column: {lat_column}, lon_col: {lon_column}, color_col: {color_col}")
        df = session.data
        if color_col:
            df = helpers.append_rand_color(df, color_col)
        else:
            df[constants.COLOR_COLUMN_NAME] = helpers.generate_random_color()
        st.map(session.data,
               latitude=lat_column,
               longitude=lon_column,
               color=constants.COLOR_COLUMN_NAME,
               )
    

