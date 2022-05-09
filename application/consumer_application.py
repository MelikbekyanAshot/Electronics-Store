import datetime

import streamlit as st

from database.storage import Storage
from database.database import get_connection
from application.application import Application

import numpy as np
import extra_streamlit_components as stx


@st.experimental_singleton
class Cart:
    def __init__(self):
        self.shopping_list = []


class ConsumerApplication:
    def run(self):
        selected_category = self.sidebar()
        self.catalog(selected_category)
        self.cart()

    def sidebar(self):
        with st.sidebar:
            st.subheader(st.session_state['name'])
            selected_category = st.sidebar.selectbox(
                'Выберите категорию',
                list(set([category[0] for category in
                          Storage(get_connection()).select_from_table('category').fetchall()])),
                key=hash('sidebar')
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
                    Cart().shopping_list.append(product[0])

    def cart(self):
        with st.sidebar:
            for item in Cart().shopping_list:
                col1, col2 = st.columns(2)
                with col1:
                    st.write(item)
                with col2:
                    if st.button(label='X', key=str(item)):
                        Cart().shopping_list.remove(item)
                        st.experimental_rerun()
            if st.button(label='Оформить заказ', key=hash('оформление заказа')):
                self.order()

    def order(self):
        order_time = st.date_input("Выберите дату доставки", datetime.datetime.now())
        if st.button('Подтвердить'):
            st.success('Заказ успешно оформлен')
