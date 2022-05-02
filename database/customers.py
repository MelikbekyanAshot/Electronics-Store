from database.database import Database


class Customers(Database):
    def __init__(self, connection):
        # .__init__(connection)
        super(Customers, self).__init__(connection)
        self.table_name = 'Покупатели'
        self.primary_key = None
        self.columns = ['category', 'name', 'price', 'amount', 'storage', 'placement', 'provider_id']

    def add(self, values):
        with self.con:
            self.con.executemany(
                "INSERT INTO Customers ('category', 'name', 'price', 'amount', 'storage', 'placement', 'provider_id') values(?, ?, ?, ?, ?, ?, ?)",
                values)

    def delete(self, condition):
        with self.con:
            self.con.execute(
                f'DELETE FROM Customers WHERE {condition}')

    def get_table(self):
        with self.con:
            return self.con.execute(f'SELECT * FROM Customers'), \
                   [item[1] for item in self.con.execute(f'PRAGMA table_info(Customers)')]