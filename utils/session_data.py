import pandas as pd
import streamlit as st
from typing import List, Dict

# import constants


class SessionData():
    def __init__(self, page: str):
        print("SessionData __init__")
        self._data = pd.DataFrame()
        self._page = page
        self._buttons = []
        self._filters = None


    # ===== DATA ===== 
    @property
    def data(self) -> pd.DataFrame:
        print("SessionData get_data")
        """ dataset as a pandas dataframe """
        return self._data


    @data.setter
    def data(self, df: pd.DataFrame) -> None:
        print("SessionData set_data")
        self._data = df


    @data.deleter
    def data(self) -> None:
        print("SessionData del_data")
        self._data = pd.DataFrame()


    def remove_column(self, col_name: str) -> None:
        print("SessionData remove_column")
        if col_name in self._data.columns:
            self._data = self._data.drop(col_name, axis=1)


    def add_column(self, col_name: str) -> None:
        print("SessionData add_columns")
        if col_name not in self._data.columns:
            self._data[col_name] = ""


    def get_dataset(self) -> pd.DataFrame:
        print("SessionData get_dataset")
        if not self._filters:
            return self._data
        else:
            return self._data


    # ===== PAGE ===== 
    @property
    def page(self) -> str:
        print("SessionData get_page")
        return self._page


    @page.setter
    def set_page(self, page: str) -> None:
        print("SessionData set_page")
        self.page = page


    def new_page(self, page: str, buttons: List[str] = None) -> None:
        print(f"SessionData new_page(page={page},buttons={buttons})")
        self._page = page
        if buttons: 
            self._buttons = buttons
        else:
            self._buttons = []


    # ===== BUTTONS ===== 
    @property
    def buttons(self) -> List[str]:
        print("SessionData get_buttons")
        return self._buttons


    @buttons.setter
    def buttons(self, button: str) -> None:
        print("SessionData set_buttons")
        self._buttons.append(button)


    @buttons.deleter
    def buttons(self) -> None:
        print("SessionData del_buttons")
        self._buttons = []


    def button(self, button: str) -> bool:
        if button in self._buttons:
            return True
        return False

    def add_button(self, button: str) -> None:
        print(f"SessionData add_button({button})\n")
        self._buttons.append(button)
        del st.session_state[button]


    def remove_button(self, button: str) -> None:
        print(f"SessionData remove_buttons({button})\n")
        self._buttons.remove(button)


    # ===== FILTERS ===== 
    @property
    def filters(self) -> Dict[str, Dict[str, List[str]]]:
        print("SessionData get_filters")
        return self._filters


    @filters.setter
    def add_filter(self, col_name: str, filter_type: str, filter_val: str):
        print("SessionData set_filters")
        if col_name in self.filters:
            if filter_type in self.filters[col_name]:
                self.filters[col_name][filter_type].append(filter_val)
            else:
                self.filters[col_name][filter_type] = [filter_val]
        else:
            self.filters[col_name] = {filter_type: [filter_val]}


    @filters.deleter
    def delete_filter(self):
        print("SessionData del_filters")
        self.filters = {}


    # ===== DEBUG ===== 
    def print_attr(self) -> None:
        print(f"""
session._data: {self._data}
session._page: {self._page}
session._buttons: {self._buttons}
session._filters: {self._filters}
""")
        
    def get_all_attrs(self) -> dict:
        return f"""
data: {self._data}
page: {self._page}
buttons: {self._buttons}
filters: {self._filters}"""


    


## test script

# if __name__ == "__main__":
#     session = SessionData("home")
    # session.print_attr()
    # print(session.data)
    # session.data = pd.DataFrame({"col1": [1,2,3],"col2": [3,4,5]})
    # print(session.data)
    # del session.data
    # print(session.data)


