import streamlit as st
from utils import constants, router
from utils import helpers
from utils import navigation
import os

print(f"\n============\nreload\n") 
if os.getenv("HOSTNAME") == "streamlit":
    navigation.get_sidebar()

session = helpers.cur_session()

router.Router[session.page]()
