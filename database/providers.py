from database.database import Database


class Providers(Database):
    def __init__(self, connection):
        super().__init__(connection)
        self.primary_key = 'provider_id'
        self.table_name = 'Поставщики'
        self.columns = ['name', 'email', 'telephone', 'address']

    def add(self, values):
        print(values)
        with self.con:
            self.con.executemany(
                "INSERT INTO Providers ('name', 'email', 'telephone', 'address') values(?, ?, ?, ?)",
                values)

    def delete(self, condition):
        with self.con:
            self.con.execute(
                f'DELETE FROM Providers WHERE {condition}')

    def get_table(self):
        with self.con:
            return self.con.execute(f'SELECT * FROM Providers'), \
                   [item[1] for item in self.con.execute(f'PRAGMA table_info(Providers)')]
