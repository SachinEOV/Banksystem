from account import Account

class SavingsAccount(Account):
    def __init__(self, account_number, holder_name, balance=0.0):
        super().__init__(account_number, holder_name, balance) 

    def apply_interest(self):
        interest_rate = 0.05 
        interest = self.balance * interest_rate
        self.balance += interest
        self.transaction_history.append(f"Interest applied: {interest}")
        return interest
