import streamlit as st

from utils.helpers import cur_session
from utils import constants
import os
# def get_navigation():
#     print("get nav")

def get_ses_state():
    ses_state = "st.Session_State: "
    for k in st.session_state:
        ses_state = f"{ses_state}\n{k}: {st.session_state[k]}"
    ses_state += f"\n========"
    return ses_state

def get_sidebar():
    session = cur_session()
    env = os.environ
    with st.sidebar:
        st.button("debug",
                     constants.BUTTON_DEBUG,
                     on_click=session.debug_switch)
        if session.debug:
            st.text(get_ses_state())
            st.text(f"SessionData: {session.get_all_attrs()}")

            env_text = ""
            for k, v in env.items():
                env_text = f"{env_text}\n{k}: {v}"
            st.text(f"Env vars: {env_text}")
