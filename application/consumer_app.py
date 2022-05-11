import datetime

import streamlit as st

from database.storage import Storage
from database.database import get_connection
from application.base_app import Application

import numpy as np
import extra_streamlit_components as stx
import pandas as pd


@st.experimental_singleton
class Cart:
    def __init__(self):
        self.shopping_list = []


class ConsumerApplication(Application):
    def __init__(self):
        self.username = st.session_state['username']
        self.shopping_list = Cart().shopping_list

    def run(self):
        selected_category = self.sidebar()
        self.catalog(selected_category)
        self.cart()

    def sidebar(self):
        with st.sidebar:
            if st.button(label='Выход'):
                # self.cookie_manager.delete(self.cookie_name)
                st.session_state['logout'] = True
                st.session_state['name'] = None
                st.session_state['username'] = None
                st.session_state['authentication_status'] = None
            #     Application.authorize()
            st.subheader(st.session_state['name'])
            selected_category = st.sidebar.selectbox(
                'Выберите категорию',
                list(set([category[0] for category in
                          Storage(get_connection()).select_from_table('category').fetchall()])),
                key=hash('sidebar-select-box')
            )
            return selected_category

    def catalog(self, category):
        products = Storage(get_connection()).select_from_table(columns='name, price',
                                                               condition=f'category == \'{category}\'')
        cols_in_grid = 4
        cols = st.columns(cols_in_grid)
        for index, product in enumerate(products):
            with cols[index % cols_in_grid]:
                st.image('assets/image-holder.png')
                st.subheader(product[0])
                st.write(product[1])
                if st.button(label='В корзину', key=hash(product[0])) and product[0] not in Cart().shopping_list:
                    self.shopping_list.append(product[0])

    def cart(self):
        with st.sidebar:
            for value in self.shopping_list:
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown('&nbsp;')
                    st.write(value)
                with col2:
                    number = st.number_input(label='', min_value=0, value=1, key=value)
            if st.button(label='Оформить заказ', key=hash('оформление заказа')):
                self.order()

    def order(self):
        with st.form(key='order-form'):
            order_time = st.date_input(label="Выберите дату доставки", min_value=datetime.datetime.now())
            st.text_input(label='Адрес доставки')
            if st.form_submit_button('Подтвердить'):
                st.success('Заказ успешно оформлен')
