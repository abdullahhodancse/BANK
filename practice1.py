import random

class User:
    def __init__(self, name, email, address):
        self.name = name
        self.email = email
        self.address = address

class Customer(User):
    def __init__(self, name, email, address, account_type):
        super().__init__(name, email, address)
        self.account_type = account_type
        self.balance = 0
        self.account_number = self.auto_account_number()
        self.transaction_history = []  
        self.loan_count = 0  
        self.deposit_balance = 0  

    def auto_account_number(self):
        return ''.join(str(random.randint(0, 9)) for _ in range(8))

    def deposit(self, amount):

        self.balance += amount
        self.deposit_balance += amount 
        self.transaction_history.append(f"Deposit of {amount} made. New balance: {self.balance}")

    def withdraw(self, amount):
        if amount > self.balance:
            print("Withdrawal amount exceeded. Transaction canceled.")
        elif amount > self.deposit_balance:
            print("The bank is bankrupt. Transaction canceled.")
        else:
            self.balance -= amount
            self.transaction_history.append(f"Withdrawal of {amount} made. New balance: {self.balance}")

    def take_loan(self, loan_amount):
        if self.loan_count < 2:
            self.balance += loan_amount
            self.loan_count += 1
            self.transaction_history.append(f"Loan of {loan_amount} taken. New balance: {self.balance}")
            print(f"Loan of {loan_amount} taken. New balance: {self.balance}")
        else:
            print("You have already taken the maximum number of loans.")

    def check_balance(self):
        print(f"Available balance: {self.balance}")   
    

    def transfer_funds(self, recipient, amount):
        if isinstance(recipient, Customer):
            if amount <= self.balance:
                self.withdraw(amount)
                recipient.deposit(amount)
                self.transaction_history.append(f"You transfar {amount} to {recipient.name}")
                print(f"Transfer of {amount} to {recipient.name} successful.")
            else:
                print("Insufficient funds for transfer.")
        else:
            print("Recipient account does not exist.")
    def view_transaction_history(self):
        print("Transaction History:")
        for transaction in self.transaction_history:
            print(transaction)
    def __repr__(self):
        return f'Name: {self.name}, Email: {self.email}, Address: {self.address}, Account_type: {self.account_type}, Balance: {self.balance}, Account_Number: {self.account_number}'

class Admin(User):
    def __init__(self, name, email, address):
        super().__init__(name, email, address)
        self.accounts = []  
        self.loan_enabled = True 
        self.balance=0    

    def create_account(self, name, email, address, account_type,balance):
        new_customer = Customer(name, email, address, account_type,balance)
        self.accounts.append(new_customer)  
        print("Account created successfully.")
        return new_customer

    def delete_account(self, account_number):
        for account in self.accounts:
            if account.account_number == account_number:
                self.accounts.remove(account)
                print("Account deleted successfully.")
                return
        print("Account does not exist or cannot be deleted.")

    def list_accounts(self):
        print("List of User Accounts:")
        for account in self.accounts:
            if isinstance(account, Customer):  
                print(f"Name: {account.name}, Account Number: {account.account_number}")

    def total_available_balance(self):
        total_balance = sum(account.balance for account in self.accounts if isinstance(account, Customer))
        print(f"Total Available Balance in the bank: {total_balance}")

    def total_loan_amount(self):
        total_loan = sum(account.balance for account in self.accounts if isinstance(account, Customer))
        print(f"Total Loan Amount in the bank: {total_loan}")

    def toggle_loan_feature(self):
        self.loan_enabled = not self.loan_enabled
        status = "enabled" if self.loan_enabled else "disabled"
        print(f"Loan feature is now {status}.")

    def __repr__(self):
        return f'Name: {self.name}, Email: {self.email}, Address: {self.address}'

# Example usage:
customer1 = Customer("John Doe", "john@example.com", "123 Main St", "Savings")
customer2 = Customer("Jane Smith", "jane@example.com", "456 Elm St", "Savings")
print(customer1)
print(customer2)

customer1.deposit(500)
customer1.withdraw(200)
customer1.take_loan(1000)
customer1.take_loan(500)
customer1.take_loan(200)  # This loan attempt will fail due to the limit
customer1.check_balance()

customer1.transfer_funds(customer2, 300)
customer1.transfer_funds(customer2, 1500)  # This transfer attempt will fail due to insufficient funds
customer1.transfer_funds("Nonexistent", 200) 
customer1.view_transaction_history()
 # This transfer attempt will fail due to recipient account not existing

admin = Admin("Admin", "admin@example.com", "789 Elm St")
admin.create_account("John Doe", "john@example.com", "123 Main St", "Savings",200)
admin.create_account("Jane Smith", "jane@example.com", "456 Elm St", "Savings",500)

admin.total_available_balance()
# Check total loan amount
admin.total_loan_amount()

# Disable loan feature
admin.toggle_loan_feature()

# Try taking a loan
admin.accounts[0].take_loan(500)
  