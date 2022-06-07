from datetime import datetime

from application.base_app import Application
from application.admin_app import AdminApplication
from application.consumer_app import ConsumerApplication
from extensions.my_authenticate import MyAuthenticate

import streamlit as st
import streamlit_authenticator as stauth
import extra_streamlit_components as stx

import numpy as np
from database.customers import Customers
from database.database import get_connection

if __name__ == '__main__':
    Application.set_config()
    if 'authentication_status' not in st.session_state or \
            st.session_state['authentication_status'] is False or \
            st.session_state['authentication_status'] is None:
        Application.authorize()
    else:
        if st.session_state['authentication_status'] is True and st.session_state['username'] != 'admin':
            app = ConsumerApplication()
            app.run()
        elif st.session_state['authentication_status'] is True and st.session_state['username'] == 'admin':
            app = AdminApplication()
            app.run()
