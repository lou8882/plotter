import random
import time

import requests
import pandas as pd
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile

from utils import constants
from utils.session_data import SessionData


def cur_session() -> SessionData:
    if constants.SES_DATA_KEY not in st.session_state:
        st.session_state[constants.SES_DATA_KEY] = SessionData(constants.PAGE_HOME)

    return st.session_state[constants.SES_DATA_KEY]


def new_page(page: str) -> None: 
    print("helpers2.new_page")
    ses = st.session_state[constants.SES_DATA_KEY]
    ses.new_page(page)


def generate_random_color(): 
    # Generate random RGB values 
    red = random.randint(0, 255) 
    green = random.randint(0, 255) 
    blue = random.randint(0, 255) 
     
    # Convert the RGB values to a hexadecimal color code 
    color_code = '#{:02X}{:02X}{:02X}'.format(red, green, blue) 
    return color_code 


def append_rand_color(df: pd.DataFrame, color_key: str) -> pd.DataFrame:

    colors = {}
    df[constants.COLOR_COLUMN_NAME] = ""
    for i, row in df.iterrows():
        color_val = row[color_key]
        if not color_val in colors:
            colors[color_val] = generate_random_color()
        df[constants.COLOR_COLUMN_NAME][i] = colors[color_val]
    return df


@st.cache_data(show_spinner=False)
def get_single_lat_lon(address: str) -> tuple[int, int]:
    time.sleep(1)
    headers = {"User-Agent": constants.USER_AGENT}
    params = {"q": address, "format": "json"}
    resp = requests.get(url=f"https://nominatim.openstreetmap.org/search",params=params, headers=headers)
    print(resp)
    resp_json = resp.json()
    print(f"address: {address}\nresp: {resp_json}\n\n")
    try:
        latitude = float(resp_json[0][constants.LABEL_LATITUDE])
        longitude = float(resp_json[0][constants.LABEL_LONGITUDE])
        return latitude, longitude
    except:
        return None, None


def add_address_data(session: SessionData, address_col: str):
    df = session.data

    lat = constants.LABEL_LATITUDE
    lon = constants.LABEL_LONGITUDE

    if not lat in df.columns:
        df[lat] = pd.Series(dtype=float)
    if not lon in df.columns:
        df[lon] = pd.Series(dtype=float)
    prog_bar = st.progress(0)
    status_text = st.empty()
    errors = 0
    successes = 0
    for i, row in df.iterrows():
        prog_bar.progress((i+1) / (len(df) +1))
        status_text.text(f"Progress: {i} out of {len(df)} addresses parsed\n{successes} successes\n{errors} failures\n")
        latitude, longitude = get_single_lat_lon(row[address_col])
        if latitude:
            successes += 1
            df[lat][i] = latitude
            df[lon][i] = longitude
        else:
            errors += 1
            df[lat][i] = None
            df[lon][i] = None
    prog_bar.balloons()
    status_text.text(f"Retrieving Lat/Lon Completed\n{successes} successful\n{errors} failures\n")

    session.data = df


def parse_from_existing_column(df: pd.DataFrame, parse_type: str, ref_col: str, new_col_name: str, expression: str, delimiter_index=0):
    print(f"parse_from_existing_column\ndf: {df}\nparse_type: {parse_type}\nref_col: {ref_col}\nnew_col_name: {new_col_name}\nexpression: {expression}\ndelimiter_index: {delimiter_index}")
    if parse_type == constants.LABEL_DELIMITER:
        if delimiter_index == 0:
            df[new_col_name] = df[ref_col].str.replace(fr"{expression}.*", "", regex=True).str.strip()
            return df
        elif delimiter_index == 1:
            df[new_col_name] = df[ref_col].str.replace(fr".*{expression}", "", regex=True).str.strip()
            return df
    elif parse_type == constants.LABEL_REGEX:
        df[new_col_name] = df[ref_col].str.findall(fr"{expression}")
        df[new_col_name] = df[new_col_name].apply(",".join)
        return df

