class Account:
    def __init__(self, account_number, holder_name, balance=0.0):
        self.account_number = account_number
        self.holder_name = holder_name
        self.balance = balance
        self.transaction_history = []  # Initialize transaction history

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transaction_history.append(f"Deposited: {amount}")
            return True
        return False

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            self.transaction_history.append(f"Withdrew: {amount}")
            return True
        return False

    def get_balance(self):
        return self.balance

    # Add get_transaction_history method
    def get_transaction_history(self):
        return self.transaction_history  # Return the transaction history
