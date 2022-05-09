import datetime

import extra_streamlit_components as stx
import numpy as np
import streamlit as st
import streamlit_authenticator as stauth

from database.customers import Customers
from database.database import get_connection

import time

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

    @staticmethod
    def login_form():
        placeholder = st.empty()
        with placeholder.container():
            chosen_id = stx.tab_bar(data=[
                stx.TabBarItemData(id=1, title="Sign in", description=''),
                stx.TabBarItemData(id=2, title="Sign up", description='')
            ], default=1)
            if chosen_id == '1':
                with st.form(key='authorization-form'):
                    input_email = st.text_input(label='Почта')
                    input_password = st.text_input(label='Пароль')
                    button = st.form_submit_button(label='Войти')
                    if button and input_password and input_password:
                        try:
                            true_login, true_password = customers.select_from_table('email, password',
                                                                                    f"email = '{input_email}'").fetchone()
                            if input_email == true_login and input_password == true_password:
                                placeholder.empty()
                                return True, input_email
                            else:
                                st.error('Вы ввели неверные логин или пароль')
                        except Exception:
                            st.error('Вы ввели неверные логин или пароль')
                    elif button and (not input_password or not input_password):
                        st.error('Введите почту и пароль')
            elif chosen_id == '2':
                with st.form(key='registration-form'):
                    fullname = st.text_input(label='ФИО')
                    email = st.text_input(label='Почта')
                    telephone = st.text_input(label='Телефон')
                    password = st.text_input(label='Пароль')
                    age = st.number_input(label='Возраст', min_value=14, step=1)
                    gender = st.radio(label='Пол', options=['М', 'Ж'])
                    if st.form_submit_button(label='Зарегистрироваться'):
                        try:
                            customers.add(
                                [(fullname, str(datetime.datetime.now()), 0, telephone, email, 0, age, gender,
                                  password)])
                            st.success('Вы успешно зарегистрировались!')
                        except Exception as e:
                            st.error('Регистрация не удалась', e)
            return False, 'unknown'
