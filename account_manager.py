import psycopg2

class AccountManager:
    def __init__(self):
        self.connection = psycopg2.connect(
            database="bank_system",
            user="postgres",
            password="Yash@2000",  # Your PostgreSQL password
            host="localhost",
            port="5432"
        )
        self.cursor = self.connection.cursor()

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
        query = """
        SELECT account_number FROM accounts WHERE username=%s AND password=%s;
        """
        self.cursor.execute(query, (username, password))
        result = self.cursor.fetchone()
        if result:
            return result[0]  # account_number
        else:
            return None

    def verify_pin(self, username, pin):
        query = """
        SELECT pin FROM accounts WHERE username=%s;
        """
        self.cursor.execute(query, (username,))
        result = self.cursor.fetchone()
        if result and result[0] == pin:
            return True
        else:
            return False

    def change_password(self, username, new_password):
        query = """
        UPDATE accounts SET password=%s WHERE username=%s;
        """
        self.cursor.execute(query, (new_password, username))
        self.connection.commit()

    def change_pin(self, username, new_pin):
        query = """
        UPDATE accounts SET pin=%s WHERE username=%s;
        """
        self.cursor.execute(query, (new_pin, username))
        self.connection.commit()

    def get_balance(self, account_number):
        query = """
        SELECT balance FROM accounts WHERE account_number=%s;
        """
        self.cursor.execute(query, (account_number,))
        result = self.cursor.fetchone()
        if result:
            return float(result[0])  # Convert deCimal to float
        else:
            return None


    def update_balance(self, account_number, new_balance):
        query = """
        UPDATE accounts SET balance=%s WHERE account_number=%s;
        """
        self.cursor.execute(query, (new_balance, account_number))
        self.connection.commit()

    def record_transaction(self, account_number, transaction_type, amount):
        query = """
        INSERT INTO transactions (account_number, transaction_type, amount) VALUES (%s, %s, %s);
        """
        self.cursor.execute(query, (account_number, transaction_type, amount))
        self.connection.commit()

    def get_transaction_history(self, account_number):
        query = """
        SELECT * FROM transactions WHERE account_number=%s;
        """
        self.cursor.execute(query, (account_number,))
        return self.cursor.fetchall()
    
   

    def create_transactions_table(self):
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

