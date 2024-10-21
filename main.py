from account_manager import AccountManager
from decimal import Decimal

def show_menu():
    print("\n--- Main Menu ---")
    print("1. Check Balance")
    print("2. Deposit Money")
    print("3. Withdraw Money")
    print("4. View Transaction History")
    print("5. Change Password")
    print("6. Change PIN")
    print("7. Logout")
    print("8. Exit")

def register_new_user(manager):
    print("\n--- New Customer Registration ---")
    holder_name = input("Enter your name: ").strip()
    username = input("Choose a username: ").strip()
    password = input("Choose a password: ").strip()
    pin = input("Set a 4-digit secret PIN for transactions: ").strip()
    
    if len(pin) != 4 or not pin.isdigit():
        print("PIN must be a 4-digit number.")
        return
    
    balance = input("Enter the initial balance: ").strip()
    
    try:
        balance = balance 
    except ValueError:
        print("Invalid balance input.")
        return
    
    manager.create_account("savings", holder_name, balance, username, password, pin)
    print(f"Account created successfully for {holder_name}.")

def login(manager):
    print("\n--- Login ---")
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()

    account_number = manager.verify_login(username, password)
    if account_number:
        print(f"Login successful. Welcome {username}!")
        return account_number, username
    else:
        print("Invalid username or password.")
        return None, None

def main():
    manager = AccountManager()
    print("\nWelcome to the Bank System")

    try:
        while True:
            action = input("\nAre you a new customer? (yes/no/exit): ").lower()
            
            if action == "exit":
                print("Exiting the system. Goodbye!")
                break

            if action == "yes":
                register_new_user(manager)
            else:
                account_number, username = login(manager)
                if account_number:
                    while True:
                        show_menu()
                        choice = input("\nSelect an option: ").strip()

                        if choice == '1':  # Check Balance
                            balance = manager.get_balance(account_number)
                            if balance is not None:
                                print(f"\nYour balance: {balance}")
                            else:
                                print("Error retrieving balance.")

                        elif choice == '2':  # Deposit Money
                            pin = input("Enter your 4-digit PIN to proceed: ").strip()
                            if manager.verify_pin(username, pin):
                                balance = manager.get_balance(account_number)
                                amount = input("Enter amount to deposit: ").strip()
                                
                                try:
                                    amount = Decimal(amount)  # Convert to Decimal
                                    if amount > 0:
                                        new_balance = balance + amount
                                        manager.update_balance(account_number, new_balance)
                                        manager.record_transaction(account_number, "deposit", amount)
                                        print(f"{amount} deposited successfully. New balance: {new_balance}")
                                    else:
                                        print("Deposit amount must be positive.")
                                except ValueError:
                                    print("Invalid amount.")
                            else:
                                print("Invalid PIN.")

                        elif choice == '3':  # Withdraw Money
                            pin = input("Enter your 4-digit PIN to proceed: ").strip()
                            if manager.verify_pin(username, pin):
                                balance = manager.get_balance(account_number)
                                amount = input("Enter amount to withdraw: ").strip()
                                
                                try:
                                    amount = Decimal(amount)  # Convert to Decimal
                                    if amount > 0:
                                        if balance >= amount:
                                            new_balance = balance - amount
                                            manager.update_balance(account_number, new_balance)
                                            manager.record_transaction(account_number, "withdraw", amount)
                                            print(f"{amount} withdrawn successfully. New balance: {new_balance}")
                                        else:
                                            print("Insufficient funds.")
                                    else:
                                        print("Withdrawal amount must be positive.")
                                except ValueError:
                                    print("Invalid amount.")
                            else:
                                print("Invalid PIN.")

                        elif choice == '4':  
                            print("\nTransaction History:")
                            transactions = manager.get_transaction_history(account_number)
                            if transactions:
                                for transaction in transactions:
                                    transaction_type, amount, transaction_time = transaction

                                    formatted_time = transaction_time.strftime("%Y-%m-%d %H:%M:%S")
                                    print(f"{formatted_time} - {transaction_type.capitalize()}: ${amount:.2f}")

                            else:
                                print("No transactions found.")

                        elif choice == '5':  
                            new_password = input("Enter your new password: ").strip()
                            manager.change_password(username, new_password)
                            print("Password changed successfully.")

                        elif choice == '6':  
                            new_pin = input("Enter your new 4-digit PIN: ").strip()
                            if len(new_pin) == 4 and new_pin.isdigit():
                                manager.change_pin(username, new_pin)
                                print("PIN changed successfully.")
                            else:
                                print("Invalid PIN format.")

                        elif choice == '7':
                            print("You have logged out successfully.")
                            break

                        elif choice == '8':  
                            print("Exiting the system. Goodbye!")
                            return

                        else:
                            print("Invalid choice. Please try again.")
    finally:
        manager.close()  

if __name__ == "__main__":
    main()
