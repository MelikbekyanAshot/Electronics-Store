import streamlit as st
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid import GridUpdateMode, DataReturnMode

from database.database import Database
from database.providers import Providers
from database.storage import Storage
from database.customers import Customers

import sqlite3 as sq

import pandas as pd
import numpy as np

import random

CONNECTION = sq.connect('electronics.db')


class Application:
    def __init__(self):
        self.database = Database(CONNECTION)
        self.selected_table = None

    def set_config(self):
        """Configurate web-site settings."""
        st.set_page_config(page_title='Курсовая',
                           page_icon='K',
                           layout="wide")
        st.title('Курсовая')
        st.markdown(""" <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style> """, unsafe_allow_html=True)

    def aggrid_dataframe(self, table: [Providers, Storage, Customers]):
        st.write(table.table_name)
        values, columns = table.get_table()
        df = pd.DataFrame(values, columns=columns)
        gb = GridOptionsBuilder.from_dataframe(df)
        # gb.configure_default_column(enablePivot=True, enableValue=True, enableRowGroup=True)
        gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, editable=True)
        gb.configure_selection(selection_mode="multiple", use_checkbox=True)
        gb.configure_side_bar()
        gb.configure_pagination()
        grid_options = gb.build()

        return AgGrid(
            df,
            gridOptions=grid_options,
            enable_enterprise_modules=True,
            update_mode=GridUpdateMode.MODEL_CHANGED,
            data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
            fit_columns_on_grid_load=False
        )

    # def get_df(self, table_name):
    #     values, columns = self.database.get_table(table_name)
    #     return pd.DataFrame(values, columns=columns)

    def set_sidebar(self):
        with st.sidebar:
            selected_table = st.sidebar.selectbox(
                'Выберите таблицу',
                ('Поставщики', "Склад", "Доставка", 'Покупатели'))
            if selected_table == 'Поставщики':
                table = Providers(CONNECTION)
            elif selected_table == 'Склад':
                table = Storage(CONNECTION)
            else:
                table = None
            st.write('Здесь будет основная информация про таблицу')
            return table


if __name__ == '__main__':
    app = Application()
    app.set_config()

    selected_table = app.set_sidebar()

    # selection = app.aggrid_dataframe(table_dict[selected_table])['selected_rows']
    selection = app.aggrid_dataframe(selected_table)['selected_rows']

    if selection and st.button(label='Удалить выбранные строки'):
        rows_to_delete = [str(selected[value]) for selected in selection for value in selected if value.endswith('_id')]
        rows_to_delete = ','.join(rows_to_delete)
        selected_table.delete(f"{selected_table.primary_key} in ({rows_to_delete})")

    # input_values = [(st.text_input(label='Введите значения').split(','))]

    with st.form(key='form'):
        input_values = dict.fromkeys(selected_table.columns)
        for index, col in enumerate(st.columns(len(selected_table.columns))):
            with col:
                input_cell = \
                    st.text_input(label=f'{selected_table.columns[index]}', key=index)
                input_values[selected_table.columns[index]] = input_cell
        if st.form_submit_button(label='Submit'):
            st.write((input_values.values()))

    if st.button(label='Добавить'):
        try:
            input_values = ','.join(list(input_values.values())).split(',')
            selected_table.add([(input_values)])
        except Exception as e:
            st.write(f'Input value is incorrect for {selected_table.table_name}', e)
