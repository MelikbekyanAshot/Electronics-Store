import datetime

import streamlit as st
import extra_streamlit_components as stx
from streamlit_option_menu import option_menu

from database.customers import Customers
from database.purchases import Purchases
from database.storage import Storage
from database.database import get_connection
from application.base_app import Application

import numpy as np
import pandas as pd

STORAGE = Storage(get_connection())
CUSTOMERS = Customers(get_connection())
PURCHASES = Purchases(get_connection)


@st.experimental_singleton
class Cart:
    def __init__(self):
        self.shopping_list = {}

    def update_amount(self, item, amount):
        self.shopping_list[item] = amount


class ConsumerApplication(Application):
    def __init__(self):
        self.username = st.session_state['username']
        self.cart = Cart()

    def run(self):
        self.set_navigation()
        self.logout()

    def set_navigation(self):
        """Define navigation bar."""
        with st.sidebar:
            self.display_user_info()
            navigation = option_menu(menu_title='',
                                     options=['Личный кабинет', 'Каталог', 'Корзина'],
                                     icons=['person', 'shop', 'cart'])
        if navigation == 'Каталог':
            selected_category = self.select_category()
            self.catalog(selected_category)
        elif navigation == 'Корзина':
            self.cart_products()
            if len(self.cart.shopping_list.values()) > 0:
                self.order_form()
        elif navigation == 'Личный кабинет':
            self.personal_account()

    def logout(self):
        """Implements logout algorithm."""
        with st.sidebar:
            if st.button(label='Выход'):
                st.session_state['logout'] = True
                st.session_state['name'] = None
                st.session_state['username'] = None
                st.session_state['authentication_status'] = None
                st.experimental_rerun()

    def display_user_info(self):
        """Displays information about user"""
        with st.sidebar:
            st.subheader(st.session_state['name'])

    def select_category(self):
        """"""
        selected_category = st.selectbox(
            'Выберите категорию',
            list(set([category[0] for category in
                      Storage(get_connection()).select_from_table('category').fetchall()])),
            key=hash('sidebar-select-box')
        )
        return selected_category

    def personal_account(self):
        balance = str(CUSTOMERS.select_from_table(columns='balance',
                                                  where=f"email == '{st.session_state['username']}'").fetchone()[0])
        st.write('Текущий баланс', balance)
        st.write('История заказов')
        customer_id = (CUSTOMERS.select_from_table(columns='customer_id',
                                                   where=f"email == '{st.session_state['username']}'").fetchone()[0])
        history = PURCHASES.select_from_table(columns='product_id,amount,purchase_date,'
                                                      'sum,discount,address,payment_method,purchase,delivery_date',
                                              where=f'customer_id == {customer_id}')
        history_df = pd.DataFrame(data=history, columns=PURCHASES.get_columns()[2:]).set_index('purchase')
        st.dataframe(history_df)

    def catalog(self, category):
        """Displays products in selected category.
        Args:
            category (str) - category selected by user."""
        selected_category_products = STORAGE.select_from_table(columns='name, price',
                                                               where=f'category == \'{category}\'')
        cols_in_grid = 4
        cols = st.columns(cols_in_grid)
        for index, (item, price) in enumerate(selected_category_products):
            with cols[index % cols_in_grid]:
                with st.container():
                    st.image('assets/image-holder.png')
                    st.subheader(item)
                    st.write(str(price), '₽')
                    in_cart_button = st.button(label='В корзину', key=hash(item))
                    if in_cart_button and item not in self.cart.shopping_list:
                        self.cart.shopping_list[item] = 1
                    elif in_cart_button and item in self.cart.shopping_list:
                        self.cart.shopping_list[item] += 1

    def cart_products(self):
        """Displays products in cart in sidebar."""
        st.subheader('Корзина')
        for item in list(self.cart.shopping_list.keys()):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('&nbsp;')
                st.write(item)
            with col2:
                number = st.number_input(label='', min_value=0, value=self.cart.shopping_list[item], key=item)
                if number == 0:
                    del self.cart.shopping_list[item]
                    st.experimental_rerun()
                else:
                    self.cart.update_amount(item, number)
            price = STORAGE.select_from_table(columns='price', where=f'name ==\'{item}\'').fetchone()[0]
            st.write(str(price * number), '₽')
            st.markdown('---')

    def order_form(self):
        """"""
        with st.form(key='order-form'):
            st.info('Ваш заказ:')
            total_cost = 0
            for product, amount in self.cart.shopping_list.items():
                current_cost = amount * STORAGE.select_from_table(columns='price',
                                                                  where=f'name ==\'{product}\'').fetchone()[0]
                st.markdown(f'Наименование: {product}')
                st.markdown(f'Количество: {str(amount)}')
                st.markdown(f'Стоимость: {current_cost} ₽')
                total_cost += current_cost
                st.markdown('---')
            st.markdown(f'**Итоговая стоимость: {total_cost} ₽**')
            delivery_date = st.date_input(label="Выберите дату доставки",
                                          min_value=datetime.datetime.now(),
                                          value=datetime.datetime.now() + datetime.timedelta(3),
                                          max_value=datetime.datetime.now() + datetime.timedelta(31))
            delivery_time = st.slider(
                "Выберите время доставки:",
                min_value=datetime.time(10, 0),
                value=(datetime.time(12, 0), datetime.time(18, 0)),
                max_value=datetime.time(21, 0))
            customer_address = \
                CUSTOMERS.select_from_table(columns='address',
                                            where=f"fullname == '{st.session_state['username']}'").fetchone()
            if customer_address is None:
                customer_address = st.text_input(label='Адрес доставки',
                                                 value=str(customer_address) if customer_address is not None else '')
            payment_method_choice = st.radio(label='Способ оплаты', options=['Наличными при получении', 'Онлайн'],
                                             index=1)
            payment_method = 0 if payment_method_choice == 'Наличными при получении' else 1
            discount = st.slider(label='Применить бонусы',
                                 min_value=0,
                                 max_value=CUSTOMERS.select_from_table(columns='balance',
                                                                       where=f"email == '{st.session_state['username']}'").fetchone()[
                                     0])
            submit_button = st.form_submit_button(label='Подтвердить')
            if submit_button:
                try:
                    purchase_id = np.random.randint(1000000, 999999999)
                    for product, amount in self.cart.shopping_list.items():
                        customer_id = CUSTOMERS.select_from_table(columns='customer_id',
                                                                  where=f"fullname == '{st.session_state['name']}'") \
                            .fetchone()[0]
                        product_id = STORAGE.select_from_table(columns='product_id',
                                                               where=f"name == '{product}'").fetchone()[0]
                        price = STORAGE.select_from_table(columns='price',
                                                          where=f'name ==\'{product}\'').fetchone()[0]
                        PURCHASES.add([(customer_id,
                                        product_id,
                                        amount,
                                        str(datetime.datetime.now()),
                                        price,
                                        discount,
                                        customer_address,
                                        payment_method,
                                        purchase_id,
                                        str(datetime.datetime.combine(delivery_date, delivery_time[0])))])
                    st.success('Заказ успешно оформлен')
                    self.cart.shopping_list.clear()
                except Exception as e:
                    st.error(str(e))
