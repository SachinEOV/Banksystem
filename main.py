from account_manager import AccountManager

def show_menu():
    print("\n--- Main Menu ---")
    print("1. Check Balance")
    print("2. Deposit Money")
    print("3. Withdraw Money")
    print("4. View Transaction History")
    print("5. Change Password")
    print("6. Change PIN")
    print("7. Logout")

def register_new_user(manager):
    print("\n--- New Customer Registration ---")
    holder_name = input("Enter your name: ")
    username = input("Choose a username: ")
    password = input("Choose a password: ")
    pin = input("Set a 4-digit secret PIN for transactions: ")
    balance = float(input("Enter the initial balance: "))

    
    manager.create_account("savings", holder_name, balance, username, password, pin)
    print(f"Account created successfully for {holder_name}.")

def login(manager):
    print("\n--- Login ---")
    username = input("Enter your username: ")
    password = input("Enter your password: ")

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

    while True:
        action = input("\nAre you a new customer? (yes/no): ").lower()
        if action == "yes":
            register_new_user(manager)
        else:
            account_number, username = login(manager)
            if account_number:
                while True:
                    show_menu()
                    choice = input("\nSelect an option: ")

                    if choice == '1':  # Check Balance
                        balance = manager.get_balance(account_number)
                        if balance is not None:
                            print(f"\nYour balance: {balance}")
                        else:
                            print("Error retrieving balance.")

                    elif choice == '2':  # Deposit Money
                        pin = input("Enter your 4-digit PIN to proceed: ")
                        if manager.verify_pin(username, pin):
                            balance = manager.get_balance(account_number)  # Fetch balance first
                            amount = float(input("Enter amount to deposit: "))
                            if amount > 0:  #positive deposit amount
                                new_balance = balance + amount
                                manager.update_balance(account_number, new_balance)
                                manager.record_transaction(account_number, "deposit", amount)
                                print(f"{amount} deposited successfully. New balance: {new_balance}")
                            else:
                                print("Deposit amount must be positive.")
                        else:
                            print("Invalid PIN.")

                    elif choice == '3':  # Withdraw Money
                        pin = input("Enter your 4-digit PIN to proceed: ")
                        if manager.verify_pin(username, pin):
                            balance = manager.get_balance(account_number)  # Fetch balance first
                            amount = float(input("Enter amount to withdraw: "))
                            if amount > 0:  # Epositive withdrawal amount
                                if balance >= amount:
                                    new_balance = balance - amount
                                    manager.update_balance(account_number, new_balance)
                                    manager.record_transaction(account_number, "withdraw", amount)
                                    print(f"{amount} withdrawn successfully. New balance: {new_balance}")
                                else:
                                    print("Insufficient funds.")
                            else:
                                print("Withdrawal amount must be positive.")
                        else:
                            print("Invalid PIN.")

                    elif choice == '4':  # View Transaction History
                        print("\nTransaction History:")
                        transactions = manager.get_transaction_history(account_number)
                        if transactions:
                            for transaction in transactions:
                                print(transaction)
                        else:
                            print("No transactions found.")

                    elif choice == '5':  # Change Password
                        new_password = input("Enter your new password: ")
                        manager.change_password(username, new_password)
                        print("Password changed successfully.")

                    elif choice == '6':  # Change PIN
                        new_pin = input("Enter your new 4-digit PIN: ")
                        manager.change_pin(username, new_pin)
                        print("PIN changed successfully.")

                    elif choice == '7':  # Logout
                        print("You have logged out successfully.")
                        break

                    else:
                        print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
