import datetime

import extra_streamlit_components as stx
import numpy as np
import streamlit as st
import streamlit_authenticator as stauth

from database.customers import Customers
from database.database import get_connection


customers = Customers(get_connection())


class Application:
    """"""
    @staticmethod
    def set_config():
        """Configurate web-site settings."""
        st.set_page_config(page_title='Курсовая',
                           page_icon='K',
                           layout="wide")
        st.markdown(""" <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style> """, unsafe_allow_html=True)
        hide_img_fs = '''
        <style>
        button[title="View fullscreen"]{
            visibility: hidden;}
        </style>
        '''

        st.markdown(hide_img_fs, unsafe_allow_html=True)
