import psycopg2
import getpass

# Connect to PostgreSQL database
def connect_db():
    try:
        connection = psycopg2.connect(
            database="bank_system", 
            user="postgres", 
            password="Yash@2000", 
            host="localhost", 
            port="5432"
        )
        return connection
    except Exception as error:
        print("Error connecting to the database:", error)
        return None

# Function to insert customer data into the database
def insert_customer(name, account_number, password, pin):
    connection = connect_db()
    if connection is None:
        return

    cursor = connection.cursor()
    
    try:
        query = """INSERT INTO customers (name, account_number, password, pin) 
                   VALUES (%s, %s, %s, %s);"""
        cursor.execute(query, (name, account_number, password, pin))
        connection.commit()
        print(f"Customer {name} added successfully!")
    except Exception as error:
        print("Error inserting customer data:", error)
    finally:
        cursor.close()
        connection.close()

# Function to get user input and store in the database
def create_customer():
    print("Enter customer details:")
    name = input("Name: ")
    account_number = input("Account Number: ")
    password = getpass.getpass("Password: ")  # Secure password input
    pin = getpass.getpass("PIN (4 digits): ")

    # Ensure PIN is exactly 4 digits
    if len(pin) != 4 or not pin.isdigit():
        print("PIN must be exactly 4 digits.")
        return
    
    # Insert the user input into the database
    insert_customer(name, account_number, password, pin)

if __name__ == "__main__":
    while True:
        print("\n--- Bank Interface ---")
        print("1. Create New Customer")
        print("2. Exit")
        choice = input("Enter choice: ")
        
        if choice == '1':
            create_customer()
        elif choice == '2':
            break
        else:
            print("Invalid choice. Try again.")
