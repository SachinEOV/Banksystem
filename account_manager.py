import psycopg2

class AccountManager:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                database="bank_system",
                user="postgres",
                password="Yash@2000",  # Your PostgreSQL password
                host="localhost",
                port="5432"
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
            SELECT account_number FROM accounts WHERE username=%s AND password=%s;
            """
            self.cursor.execute(query, (username, password))
            result = self.cursor.fetchone()
            if result:
                return result[0]  # account_number
            else:
                return None
        except Exception as error:
            print("Error verifying login:", error)

    def verify_pin(self, username, pin):
        try:
            query = """
            SELECT pin FROM accounts WHERE username=%s;
            """
            self.cursor.execute(query, (username,))
            result = self.cursor.fetchone()
            if result and result[0] == pin:
                return True
            else:
                return False
        except Exception as error:
            print("Error verifying PIN:", error)

    def change_password(self, username, new_password):
        try:
            query = """
            UPDATE accounts SET password=%s WHERE username=%s;
            """
            self.cursor.execute(query, (new_password, username))
            self.connection.commit()
            print("Password updated successfully.")
        except Exception as error:
            print("Error updating password:", error)

    def change_pin(self, username, new_pin):
        try:
            query = """
            UPDATE accounts SET pin=%s WHERE username=%s;
            """
            self.cursor.execute(query, (new_pin, username))
            self.connection.commit()
            print("PIN updated successfully.")
        except Exception as error:
            print("Error updating PIN:", error)

    def get_balance(self, account_number):
        try:
            query = """
            SELECT balance FROM accounts WHERE account_number=%s;
            """
            self.cursor.execute(query, (account_number,))
            result = self.cursor.fetchone()
            if result:
                return float(result[0])  # Convert Decimal to float
            else:
                print("Account not found.")
                return None
        except Exception as error:
            print("Error fetching balance:", error)

    def update_balance(self, account_number, new_balance):
        try:
            query = """
            UPDATE accounts SET balance=%s WHERE account_number=%s;
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
            SELECT * FROM transactions WHERE account_number=%s;
            """
            self.cursor.execute(query, (account_number,))
            return self.cursor.fetchall()
        except Exception as error:
            print("Error fetching transaction history:", error)

    def create_transactions_table(self):
        try:
            query = """
            CREATE TABLE IF NOT EXISTS transactions (
                id SERIAL PRIMARY KEY,
                account_number VARCHAR(50) NOT NULL,
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
        """Close cursor and connection"""
        try:
            self.cursor.close()
            self.connection.close()
            print("Connection closed.")
        except Exception as error:
            print("Error closing connection:", error)

# Example usage
if __name__ == "__main__":
    manager = AccountManager()
    
    # Create transactions table
    manager.create_transactions_table()

    # Add other functionality or menu as needed
