import configparser
from psycopg2 import connect

config = configparser.ConfigParser() #To Load the Crediantials
config.read('config.ini')

class DBSetup:
    def __init__(self):
        try:
            self.connection = connect(
                database=config['database']['DB_NAME'],
                user=config['database']['DB_USER'],
                password=config['database']['DB_PASSWORD'],
                host=config['database']['DB_HOST'],
                port=config['database']['DB_PORT']
            )
            self.cursor = self.connection.cursor()
            print("Database connection successful.")
        except Exception as error:
            print("Error connecting to the database:", error)

    def create_accounts_table(self):
        try:
            query = """
            CREATE TABLE IF NOT EXISTS accounts (
                account_number SERIAL PRIMARY KEY,
                account_type VARCHAR(20) NOT NULL,
                holder_name VARCHAR(100) NOT NULL,
                balance DECIMAL(10, 2) NOT NULL,
                username VARCHAR(50) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                pin VARCHAR(4) NOT NULL
            );
            """
            self.cursor.execute(query)
            self.connection.commit()
            print("Accounts table created or already exists.")
        except Exception as error:
            print("Error creating accounts table:", error)

    def create_transactions_table(self):
        try:
            query = """
            CREATE TABLE IF NOT EXISTS transactions (
                id SERIAL PRIMARY KEY,
                account_number INTEGER REFERENCES accounts(account_number),
                transaction_type VARCHAR(10) NOT NULL,
                amount DECIMAL(10, 2) NOT NULL,
                transaction_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
            self.cursor.execute(query)
            self.connection.commit()
            print("Transactions table created or already exists.")
        except Exception as error:
            print("Error creating transactions table:", error)

    def close(self):
        try:
            self.cursor.close()
            self.connection.close()
            print("Connection closed.")
        except Exception as error:
            print("Error closing connection:", error)

if __name__ == "__main__":
    setup = DBSetup()
    setup.create_accounts_table()  #to create account_table
    setup.create_transactions_table()  #to create transaction_table
    setup.close()
