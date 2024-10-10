
from account import Account

class CheckingAccount(Account):
    def __init__(self, account_number, holder_name, balance=0.0, overdraft_limit=500):
        super().__init__(account_number, holder_name, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if 0 < amount <= (self.balance + self.overdraft_limit):
            self.balance -= amount
            return True
        return False
