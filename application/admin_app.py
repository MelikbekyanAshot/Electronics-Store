import pandas as pd
import sqlite3 as sq
import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

from database.customers import Customers
from database.providers import Providers
from database.purchases import Purchases
from database.shipment import Shipment
from database.storage import Storage
from database.database import get_connection
from application.base_app import Application


class AdminApplication(Application):
    @staticmethod
    def aggrid_dataframe(table: [Providers, Storage, Customers, Shipment, Purchases]):
        """Display aggregated dataframe.

        Args:
            table (Providers, Storage, Customers, Shipment, Purchases) - table to show.

        Returns:
            AgGrid() - aggregated dataframe.
        """
        values = table.select_from_table()
        df = pd.DataFrame(values, columns=[table.primary_key] + table.columns)
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

    @staticmethod
    def sidebar():
        with st.sidebar:
            selected_table = st.sidebar.selectbox(
                'Выберите таблицу',
                ('Поставщики', 'Склад', 'Доставка', 'Покупатели', 'Покупки'))
            if selected_table == 'Поставщики':
                table = Providers(get_connection())
            elif selected_table == 'Склад':
                table = Storage(get_connection())
            elif selected_table == 'Покупатели':
                table = Customers(get_connection())
            elif selected_table == 'Доставка':
                table = Shipment(get_connection())
            elif selected_table == 'Покупки':
                table = Purchases(get_connection())
            else:
                raise "Неверное название таблицы"
            for info in table.table_info():
                st.write(info)
            return table

    @staticmethod
    def run():
        selected_table = AdminApplication.sidebar()

        selection = AdminApplication.aggrid_dataframe(selected_table)['selected_rows']

        if selection and st.button(label='Удалить выбранные строки'):
            try:
                rows_to_delete = [str(selected[value]) for selected in selection for value in selected if
                                  value.endswith('_id')]
                rows_to_delete = ','.join(rows_to_delete)
                selected_table.delete(f"{selected_table.primary_key} in ({rows_to_delete})")
                st.experimental_rerun()
            except Exception as e:
                st.write(e)

        with st.form(key='form'):
            input_values = dict.fromkeys(selected_table.columns)
            for index, col in enumerate(st.columns(len(selected_table.columns))):
                with col:
                    input_cell = \
                        st.text_input(label=f'{selected_table.columns[index]}', key=index)
                    input_values[selected_table.columns[index]] = input_cell
            if st.form_submit_button(label='Добавить'):
                try:
                    input_values = ','.join(list(input_values.values())).split(',')
                    selected_table.add([(input_values)])
                    st.experimental_rerun()
                except Exception as e:
                    st.write(f'Input value is incorrect for {selected_table.table_name}', e)
