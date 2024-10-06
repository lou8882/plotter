import streamlit as st
from utils import constants, router
from utils import helpers
from utils import navigation
# base_dir = os.path.dirname(os.path.realpath(__file__))

print(f"\n============\nreload\n") 
# navigation.get_sidebar()

session = helpers.cur_session()

router.Router[session.page]()
