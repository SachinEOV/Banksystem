
class Transaction:
    def __init__(self, account, amount):
        self.account = account
        self.amount = amount

class Deposit(Transaction):
    def execute(self):
        return self.account.deposit(self.amount)

class Withdrawal(Transaction):
    def execute(self):
        return self.account.withdraw(self.amount)
