from singleton_decorator import singleton
import sqlite3 as sq


@singleton
def get_connection():
    return sq.connect('electronics.db')


class Database:
    def __init__(self, connection):
        self.con = get_connection()
        self.table_name = None
        self.primary_key = None
        self.columns = None

    def get_connection(self):
        return self.con

    def add(self, values):
        with sq.connect('electronics.db') as con:
            cur = con.cursor()
            cur.executemany(
                f"INSERT INTO {self.table_name} {*self.get_columns()[1:],} "
                f"values({'?,' * (len(self.get_columns()[1:]) - 1)}?)",
                values)

    def delete(self, condition):
        with sq.connect('electronics.db') as con:
            cur = con.cursor()
            try:
                cur.execute(
                    f'DELETE FROM {self.table_name} WHERE {condition}')
            except Exception:
                pass

    def select_from_table(self, columns='*', where='TRUE'):
        """"""
        with sq.connect('electronics.db') as con:
            cur = con.cursor()
            return cur.execute(f'SELECT {columns} FROM {self.table_name} WHERE {where}')

    def table_info(self):
        with sq.connect('electronics.db') as con:
            return f'Первичный ключ: {self.primary_key}', \
                   f'Количество строк: {self.__get_table_len()}', \
                   f'Типы данных столбцов: {self.__get_column_types()}'

    def __get_table_len(self):
        with sq.connect('electronics.db') as con:
            cur = con.cursor()
            return cur.execute(f'SELECT COUNT(*) FROM {self.table_name}').fetchone()[0]

    def get_columns(self):
        with sq.connect('electronics.db') as con:
            cur = con.cursor()
            return list(map(lambda x: x[0], cur.execute(f'select * from {self.table_name}').description))

    def __get_column_types(self):
        with sq.connect('electronics.db') as con:
            cur = con.cursor()
            return {item[1]: item[2] for item in
                    cur.execute(f'PRAGMA table_info({self.table_name})').fetchall()}
