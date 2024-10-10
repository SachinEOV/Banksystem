### Bank System Example: Exploring OOP and SOLID Principles

# Welcome to this beginner-friendly repository! This project is designed to help you understand Object-Oriented Programming (OOP) concepts and the SOLID principles through a simple Bank System example.
# By the end of this project, you’ll gain hands-on experience with:

    * Encapsulation, Inheritance, Abstraction, and Polymorphism
    * Applying SOLID principles to create clean, maintainable, and scalable code.

# Table of Contents

    Project Overview
    OOP Concepts Covered
    SOLID Principles Implemented
    Getting Started
    Project Structure
    How to Contribute
    Contact

Project Overview

This Bank System simulates basic banking operations like creating accounts, depositing, withdrawing, and checking balances. The design focuses on implementing core OOP concepts and adhering to SOLID principles to make the system modular and flexible.
OOP Concepts Covered

**Encapsulation** : Each class hides its data and exposes only what is necessary through methods.

**Inheritance**: We have a base class Account and derived classes like SavingsAccount and CheckingAccount that inherit common properties and behavior.

**Abstraction**: Users interact with abstract classes or interfaces, without needing to understand the internal workings.

**Polymorphism**: Objects can be treated as instances of their base class or interface, allowing dynamic method overriding.
    
SOLID Principles Implemented
  **S: Single Responsibility Principle** — Each class in the system has one responsibility (e.g., AccountManager only manages accounts).
    
  **O: Open/Closed Principle** — Classes are open for extension but closed for modification (e.g., new account types can be added without altering the existing code).
    
  **L: Liskov Substitution Principle** — Subclasses can replace base classes without altering the functionality (e.g., SavingsAccount can replace Account without issue).
  
  **I: Interface Segregation Principle** — Clients are not forced to depend on interfaces they don't use (e.g., separate interfaces for transaction operations and account info).
  
  **D: Dependency Inversion Principle** — High-level modules do not depend on low-level modules; both depend on abstractions (e.g., an interface ITransaction defines the contract for transaction handling).

Getting Started Prerequisites

**Python 3.x (recommended)**

**Basic understanding of Python and OOP principles**

Installing

    Clone the repository:

    bash

git clone https://github.com/************************************
cd bank-system-oop-solid

Install dependencies (if any):

bash

pip install -r requirements.txt

Run the Bank System:

bash

    python main.py

Example Usage

python

from bank_system import SavingsAccount, AccountManager

# Create a savings account
savings = SavingsAccount(account_holder="John Doe", initial_balance=1000)

# Deposit money
savings.deposit(500)

# Check balance
print(savings.get_balance())  # Output: 1500

Project Structure

    
    ├── bank_system/
    │   ├── account.py             # Base Account class
    │   ├── savings_account.py     # Savings account class (inherits from Account)
    │   ├── checking_account.py    # Checking account class (inherits from Account)
    │   ├── transaction.py         # Transaction handling (Deposit, Withdrawal)
    │   ├── account_manager.py     # Manages account operations
    │   └── interfaces/
    │       ├── iaccount.py        # Interface for accounts
    │       └── itransaction.py    # Interface for transactions
    ├── tests/
    │   ├── test_account.py        # Unit tests for account classes
    │   └── test_transaction.py    # Unit tests for transactions
    ├── main.py                    # Entry point of the application
    └── README.md

How to Contribute

We welcome contributions from the community! Whether it's bug fixes, new features, or suggestions for improvement, feel free to:

    Fork the repository
    Create a feature branch (git checkout -b feature-branch)
    Commit your changes (git commit -m 'Add some feature')
    Push to the branch (git push origin feature-branch)
    Create a new Pull Request

Contact

Feel free to reach out with any questions or feedback:

    GitHub Issues: Open an issue
    Email: your-email@example.com
