import sqlite3 as sq
import pandas as pd
import streamlit as st


class Database:
    def __init__(self, connection):
        self.con = connection

    def get_connection(self):
        return self.con

    def create_table(self, name, columns_info):
        with self.con:
            self.con.execute(f"""
                CREATE TABLE IF NOT EXISTS {name} (
                    {columns_info}
                );
            """)

    def get_table(self):
        pass
        # with self.con:
        #     return self.con.execute(f'SELECT * FROM {table_name}'), \
        #            [item[1] for item in self.con.execute(f'PRAGMA table_info({table_name})')]
