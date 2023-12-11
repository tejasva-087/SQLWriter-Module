import mysql.connector as sql


class EasySQL:
    """Parent class to get the basic details of the user's host, user and password"""
    # Datatype: ['DatatypeInSQL', 'Length']
    __value__ = 30  # Default value for datatypes
    __datatype_relation__ = {
        "num": ["INT"],  # Integer
        "txt": ["CHAR", __value__],  # String for faster usage
        "txt_s": ["VARCHAR", __value__],  # For saving space
        "date": ["DATE"],  # Date YYYY-MM-DD
        "time": ["TIME"],  # Time HH-MM-SS
        "decimal": ["DOUBLE"]  # Decimal point values
    }
    __condition__ = ''  # Condition for the CHECK constraint
    __constraints__ = {
        'p': "PRIMARY KEY",
        'n': "NOT NULL",
        'u': "UNIQUE",
        'c': ["CHECK", __condition__],
        'd': ["DEFAULT", __value__]
    }

    __alias_non_value__ = ["num", "data", "time", "decimal", "p", "n", "u"]
    __alias_value__ = ["txt", "txt_s", "c", "d"]

    def __init__(self, host: str, user: str, password: str, database: str, table: str):
        # Checking fot the parameters
        assert type(host) == str, "host expected to be a string"
        assert type(user) == str, "user expected to be a string"
        assert type(password) == str, "password expected to be a string"
        assert type(database) == str, "database expected to be a string"
        assert type(table) == str, "table expected to be a string"

        # Assigning parameters  parameters
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.table = table

        """Internal assignment and checks"""
        # Checking connection
        self.connection = self.check_connection()
        assert bool(self.connection), "Connection error"
        self.cursor = self.connection.cursor()  # Checking cursor
        self.database_exist = self.check_database()  # Checking if database exist or not
        self.table_exist = self.check_table()  # check if table exist or not

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
            return False

    def check_table(self):
        self.cursor.execute("SHOW TABLES;")
        tables = self.cursor.fetchall()
        if (self.table,) in tables:
            return True
        else:
            return False

    def create_database(self):
        self.cursor.execute(f"CREATE DATABASE {self.database}")
        self.cursor.execute(f"USE {self.database}")


mySql_thing = EasySQL(host="localhost", user='root', password='12345678', database='host', table='mysql_table')
