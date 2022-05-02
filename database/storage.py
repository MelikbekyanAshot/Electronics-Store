from database.database import Database


class Storage(Database):
    def __init__(self, connection):
        # .__init__(connection)
        super(Storage, self).__init__(connection)
        self.table_name = 'Склад'
        self.primary_key = 'id'
        self.columns = ['category', 'name', 'price', 'amount', 'storage', 'placement', 'provider_id']

    def add(self, values):
        with self.con:
            self.con.executemany(
                "INSERT INTO Storage ('category', 'name', 'price', 'amount', 'storage', 'placement', 'provider_id') "
                "values(?, ?, ?, ?, ?, ?, ?)",
                values)

    def delete(self, condition):
        with self.con:
            self.con.execute(
                f'DELETE FROM Storage WHERE {condition}')

    def get_table(self):
        with self.con:
            return self.con.execute(f'SELECT * FROM Storage'), \
                   [item[1] for item in self.con.execute(f'PRAGMA table_info(Storage)')]