import streamlit as st
from utils import constants, helpers
from utils.session_data import SessionData
    

def gen_map_page():
    st.title("Create map")
    session = helpers.cur_session()

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
    
    disable = not (lat_column and lon_column)

    if st.button(
        label="Make Map",
        key=constants.BUTTON_CONTINUE,
        disabled=disable):

        print(f"cat_column: {lat_column}, lon_col: {lon_column}, color_col: {color_col}")
        df = session.data
        if color_col:
            df = helpers.append_rand_color(df, color_col)
        else:
            df[constants.COLOR_COLUMN_NAME] = helpers.generate_random_color()
        
        df = df.dropna(subset=['lat', 'lon'])

        st.map(df,
               latitude=lat_column,
               longitude=lon_column,
               color=constants.COLOR_COLUMN_NAME,
               )
    

    st.button("Return to Data",
              key=constants.BUTTON_BACK,
              on_click=session.new_page,
              args=[constants.PAGE_EDIT_DATA]
              )