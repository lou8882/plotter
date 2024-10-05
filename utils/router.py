import streamlit as st

from st_pages.home_page import home_page
from st_pages.import_data import import_data_page
from st_pages.edit_data import edit_data_page
from st_pages.view_data import view_data_page
from st_pages.gen_map import gen_map_page

from utils import constants, helpers
# import st_pages

Router = {
    constants.PAGE_HOME: home_page,
    constants.PAGE_IMPORT_DATA: import_data_page,
    constants.PAGE_EDIT_DATA: edit_data_page,
    constants.PAGE_VIEW_DATA: view_data_page,
    constants.PAGE_GEN_MAP: gen_map_page,
}