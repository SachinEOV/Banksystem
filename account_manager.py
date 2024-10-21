import configparser
from psycopg2 import connect

# Load configuration from config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

class AccountManager:
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

    def create_account(self, account_type, holder_name, balance, username, password, pin):
        try:
            query = """
            INSERT INTO accounts (account_type, holder_name, balance, username, password, pin)
            VALUES (%s, %s, %s, %s, %s, %s);
            """
            self.cursor.execute(query, (account_type, holder_name, balance, username, password, pin))
            self.connection.commit()
            print("Account created successfully.")
        except Exception as error:
            print("Error creating account:", error)

    def verify_login(self, username, password):
        try:
            query = """
            SELECT account_number FROM accounts
            WHERE username = %s AND password = %s;
            """
            self.cursor.execute(query, (username, password))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except Exception as error:
            print("Error verifying login:", error)
            return None

    def verify_pin(self, username, pin):
        try:
            query = """
            SELECT pin FROM accounts
            WHERE username = %s;
            """
            self.cursor.execute(query, (username,))
            result = self.cursor.fetchone()
            return result[0] == pin if result else False
        except Exception as error:
            print("Error verifying PIN:", error)
            return False

    def change_password(self, username, new_password):
        try:
            query = """
            UPDATE accounts
            SET password = %s
            WHERE username = %s;
            """
            self.cursor.execute(query, (new_password, username))
            self.connection.commit()
            print("Password changed successfully.")
        except Exception as error:
            print("Error changing password:", error)

    def change_pin(self, username, new_pin):
        try:
            query = """
            UPDATE accounts
            SET pin = %s
            WHERE username = %s;
            """
            self.cursor.execute(query, (new_pin, username))
            self.connection.commit()
            print("PIN changed successfully.")
        except Exception as error:
            print("Error changing PIN:", error)

    def get_balance(self, account_number):
        try:
            query = """
            SELECT balance FROM accounts
            WHERE account_number = %s;
            """
            self.cursor.execute(query, (account_number,))
            result = self.cursor.fetchone()
            return result[0] if result else print("Error")
        except Exception as error:
            print("Error retrieving balance:", error)
            return "Error re"

    def update_balance(self, account_number, new_balance):
        try:
            query = """
            UPDATE accounts
            SET balance = %s
            WHERE account_number = %s;
            """
            self.cursor.execute(query, (new_balance, account_number))
            self.connection.commit()
            print("Balance updated successfully.")
        except Exception as error:
            print("Error updating balance:", error)

    def record_transaction(self, account_number, transaction_type, amount):
        try:
            query = """
            INSERT INTO transactions (account_number, transaction_type, amount)
            VALUES (%s, %s, %s);
            """
            self.cursor.execute(query, (account_number, transaction_type, amount))
            self.connection.commit()
            print("Transaction recorded successfully.")
        except Exception as error:
            print("Error recording transaction:", error)

    def get_transaction_history(self, account_number):
        try:
            query = """
            SELECT transaction_type, amount, transaction_time FROM transactions
            WHERE account_number = %s
            ORDER BY transaction_time DESC;
            """
            self.cursor.execute(query, (account_number,))
            transactions = self.cursor.fetchall()
            return transactions
        except Exception as error:
            print("Error retrieving transaction history:", error)
            return None

    def close(self):
        try:
            self.cursor.close()
            self.connection.close()
            print("Connection closed.")
        except Exception as error:
            print("Error closing connection:", error)

if __name__ == "__main__":
    manager = AccountManager()
    manager.close()
