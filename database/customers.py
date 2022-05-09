from database.database import Database


class Customers(Database):
    def __init__(self, connection):
        super().__init__(connection)
        self.table_name = 'Customers'
        self.primary_key = 'customer_id'
        self.columns = ['fullname', 'registration_date', 'balance', 'telephone', 'email', 'rank', 'age', 'gender']
