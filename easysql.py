import mysql.connector as sql

if __name__ == '__main__':
    class TableAlreadyExist(Exception):
        """Custom error generation"""
        def __init__(self, reason):
            self.reason = reason


class EasySQL:
    """Parent class to get the basic details of the user's host, user and password"""
    # Datatype: ['DatatypeInSQL', 'Length']
    __value__ = 30  # Default value for datatypes
    __datatype_relation__ = {
        "num": "INT",  # Integer
        "txt": ["CHAR", __value__],  # String for faster usage
        "txt_s": ["VARCHAR", __value__],  # For saving space
        "date": "DATE",  # Date YYYY-MM-DD
        "time": "TIME",  # Time HH-MM-SS
        "decimal": "DOUBLE",  # Decimal point values
        'p': "PRIMARY KEY",
        'n': "NOT NULL",
        'u': "UNIQUE",
        'c': ["CHECK", __value__],
        'd': ["DEFAULT", __value__]
    }
    __alias__ = __datatype_relation__.keys()

    def __init__(self, host: str, user: str, password: str, database: str):
        # Checking fot the parameters
        assert type(host) == str, "host expected to be a string"
        assert type(user) == str, "user expected to be a string"
        assert type(password) == str, "password expected to be a string"
        assert type(database) == str, "database expected to be a string"

        # Assigning parameters  parameters
        self.host = host
        self.user = user
        self.password = password
        self.database = database

        """Internal assignment and checks"""
        # Checking connection
        self.connection = self.check_connection()
        assert bool(self.connection), "Connection error"
        self.cursor = self.connection.cursor()  # Checking cursor
        self.database_exist = self.check_database()  # Checking if database exist or not

    def check_connection(self):
        """For checking the connection; returns False if connection not valid else return the connection object"""
        try:
            sql_connection = sql.connect(host=self.host, user=self.user, password=self.password)
            if sql_connection.is_connected():
                return sql_connection

        except (sql.InterfaceError, sql.ProgrammingError):
            return False

    def check_database(self):
        self.cursor.execute("SHOW DATABASES;")
        databases = self.cursor.fetchall()
        if (self.database,) in databases:  # fetchall returns tuples so checking condition using tuple (self.database,)
            self.cursor.execute(f"USE {self.database};")
            return True
        else:
            self.create_database()

    def create_database(self):
        self.cursor.execute(f"CREATE DATABASE {self.database}")
        self.cursor.execute(f"USE {self.database}")

    def check_table(self, table):
        self.cursor.execute("SHOW TABLES;")
        tables = self.cursor.fetchall()
        if (table,) in tables:
            return True
        else:
            return False

    @classmethod
    def check_class_name(cls, name):
        print(name)

    @classmethod
    def query_generator(cls, table_data):
        for i in table_data:
            cls.check_class_name(i[0])

    def create_table(self, table, data):
        query = ''
        if self.check_table(table):
            raise TableAlreadyExist(f"A table with name {table} already exist")

        self.query_generator(data)


# ['Column1', "column2", "column3", 'column4']
# [['column', ('txt', 30), 'p'], ['column', 'int', 'u']]
# [['column', 'p', ('txt', 30)], ['column', 'int', '(c, '==10')']]
# [['column', int], ['column', 'int', '(c, '==10')']]


mySql_thing = EasySQL(host="localhost", user='root', password='12345678', database='host')
mySql_thing.create_table(table='tableName', data=[['column', ('txt', 30), 'p'], ['column', 'int', 'u']])
