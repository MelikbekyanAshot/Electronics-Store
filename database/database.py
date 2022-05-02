class Database:
    def __init__(self, connection):
        self.con = connection
        self.table_name = None
        self.primary_key = None
        self.columns = None

    def get_connection(self):
        return self.con

    def create_table(self, name, columns_info):
        with self.con:
            self.con.execute(f"""
                CREATE TABLE IF NOT EXISTS {name} (
                    {columns_info}
                );
            """)

    def add(self, values):
        with self.con:
            print(f"INSERT INTO {self.table_name} ({*self.columns,}) "
                f"values({'?,' * (len(self.columns) - 1)} ?)")
            self.con.executemany(
                f"INSERT INTO {self.table_name} {*self.columns,} "
                f"values({'?,' * (len(self.columns) - 1)} ?)",
                values)

    def delete(self, condition):
        with self.con:
            try:
                self.con.execute(
                    f'DELETE FROM {self.table_name} WHERE ({condition})')
            except Exception:
                pass

    def get_table(self):
        with self.con:
            return self.con.execute(f'SELECT * FROM {self.table_name}'), \
                   [item[1] for item in self.con.execute(f'PRAGMA table_info({self.table_name})')]

    def table_info(self):
        with self.con:
            return f'Первичный ключ: {self.primary_key}', \
                   f'Количество строк: {self.__get_table_len()}', \
                   'Типы данных столбцов', self.__get_column_types()

    def __get_table_len(self):
        with self.con:
            return self.con.cursor().execute(f'SELECT COUNT(*) FROM {self.table_name}').fetchone()[0]

    def __get_column_types(self):
        with self.con:
            return {item[1]: item[2] for item in self.con.cursor().execute(f'PRAGMA table_info({self.table_name})').fetchall()}
