from abc import ABC, abstractmethod

class ITransaction(ABC):

    @abstractmethod
    def deposit(self, amount):
        pass

    @abstractmethod
    def withdraw(self, amount):
        pass

    @abstractmethod
    def get_balance(self):
        pass

    @abstractmethod
    def get_transaction_history(self):
        pass
