import streamlit as st

from database.storage import Storage
from database.database import get_connection
from application.application import Application
import extra_streamlit_components as stx


class ConsumerApplication(Application):
    def __init__(self, user):
        self.user = user

    @st.cache(ttl=3600)
    class Cart:
        def __init__(self, user):
            self.shopping_list = {user: []}

    def sidebar(self):
        with st.sidebar:
            with st.sidebar:
                if st.button(label='Выйти', key='выход'):
                    super(ConsumerApplication, self).login_form()
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
                st.subheader(product[1])
                if st.button(label='В корзину', key=hash(product[0])):
                    self.Cart(self.user).shopping_list[self.user].append(product[0])

    def cart(self):
        with st.sidebar:
            st.write(self.user)
            for item in self.Cart(self.user).shopping_list[self.user]:
                col1, col2 = st.columns(2)
                with col1:
                    st.write(item)
                with col2:
                    if st.button(label='X', key=hash(str(item) + 'in shopping list')):
                        self.Cart(self.user).shopping_list[self.user].remove(item)
                        st.experimental_rerun()
            if st.button(label='Оформить заказ', key=hash('оформление заказа')):
                pass

    def run(self):
        selected_category = self.sidebar()
        self.catalog(selected_category)
        self.cart()
