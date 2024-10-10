
import unittest
from transaction import Deposit, Withdrawal
from Python.SavingsAccount import SavingsAccount

class TestTransactions(unittest.TestCase):
    def test_deposit(self):
        account = SavingsAccount(123, "Yash", 1000)
        deposit = Deposit(account, 500)
        deposit.execute()
        self.assertEqual(account.get_balance(), 1500)

    def test_withdrawal(self):
        account = SavingsAccount(123, "Yash", 1000)
        withdrawal = Withdrawal(account, 200)
        withdrawal.execute()
        self.assertEqual(account.get_balance(), 800)

if __name__ == "__main__":
    unittest.main()
