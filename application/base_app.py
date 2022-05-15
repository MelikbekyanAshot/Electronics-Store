import datetime

import extra_streamlit_components as stx
import numpy as np
import streamlit as st
import streamlit_authenticator as stauth

from database.customers import Customers
from database.database import get_connection
from extensions.my_authenticate import MyAuthenticate

customers = Customers(get_connection())


class Application:
    """"""
    @staticmethod
    def set_config():
        """Configurate web-site settings."""
        st.set_page_config(page_title='Курсовая',
                           page_icon='K')
        st.write('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)
        st.markdown(""" <style>#MainMenu {visibility: hidden;}footer {visibility: hidden;}</style> """, unsafe_allow_html=True)
        st.markdown('''<style>button[title="View fullscreen"]{visibility: hidden;}</style>''', unsafe_allow_html=True)
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

    @staticmethod
    def authorize():
        placeholder = st.empty()
        customers = Customers(get_connection())
        choice = placeholder.radio('', ['Авторизация', 'Регистрация'])
        if choice == 'Авторизация':
            names = [item[0] for item in customers.select_from_table('fullname').fetchall()]
            usernames = [item[0] for item in customers.select_from_table('email').fetchall()]
            passwords = [item[0] for item in customers.select_from_table('password').fetchall()]
            hashed_passwords = stauth.Hasher(passwords).generate()
            authenticator = MyAuthenticate(names, usernames, hashed_passwords,
                                           str(np.random.randint(0, 100000)), str(np.random.randint(0, 100000)),
                                           cookie_expiry_days=30)
            name, authentication_status, username = authenticator.login(form_name='Авторизация',
                                                                        login='Почта',
                                                                        password='Пароль',
                                                                        button_name='Войти',
                                                                        location='main')
            if authentication_status:
                placeholder.empty()
                authenticator.logout('Выйти', 'sidebar')
            elif not authentication_status and username:
                st.error('Логин или пароль введены неверно')
        elif choice == 'Регистрация':
            with st.form(key='registration-form'):
                fullname = st.text_input(label='ФИО')
                email = st.text_input(label='Почта')
                telephone = st.text_input(label='Телефон')
                password = st.text_input(label='Пароль')
                age = st.number_input(label='Возраст', min_value=14, step=1)
                gender = st.radio(label='Пол', options=['М', 'Ж'])
                address = st.text_input(label='Адрес')
                if st.form_submit_button(label='Зарегистрироваться'):
                    try:
                        customers.add(
                            [(fullname, str(datetime.datetime.now()), 0, telephone, email, 0, age, gender,
                              password, address)])
                        st.success('Вы успешно зарегистрировались!')
                    except Exception as e:
                        st.error('Регистрация не удалась')
