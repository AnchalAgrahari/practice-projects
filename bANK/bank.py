import json
import datetime
import os

class BankAccount:
    def __init__(self, user_id, name, balance, history):
        self.user_id = user_id
        self.name = name
        self.balance = float(balance)
        self.history = history

    def _record_transaction(self, t_type, amount):
        transaction = {
            'type': t_type, 
            'amount': amount, 
            'new_balance': self.balance,
            'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.history.append(transaction)

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self._record_transaction("Deposit", amount)
            return f"Success! New Balance: ${self.balance:.2f}"
        return "Failed: Amount must be positive."

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            self._record_transaction("Withdraw", amount)
            return f"Success! New Balance: ${self.balance:.2f}"
        return "Failed: Insufficient funds."
    
    def get_balance(self):
        return f"current Baance: ${self.balance: .2f}"
    
    def print_history(self, n=5):
        print(f"\n--- Last {n} Transactions ---")

        transaction_to_show = self.history[-n:]

        if not transaction_to_show:
            print("No transactions found.")
            return
        for i, t in enumerate(transaction_to_show):
            sign = "+" if t["type"] == "Deposit" or t["type"] == "Initial Deposit" else "-"
            print(f"[{i+1}/{len(self.history)}] {t['time']} | {t['type'] : <18} | {sign}${t['amount']: <8.2f} | Balance after transaction: ${t['new_balance']: .2f}")
        


# --- DATA HANDLING FUNCTIONS ---

def load_account(target_id):
    """Loads the data and finds the specific user ID"""
    if not os.path.exists('data.json'):
        print("Error: data.json file not found!")
        return None, None

    with open('data.json', 'r') as f:
        all_data = json.load(f)
    
    if target_id in all_data:
        user_info = all_data[target_id]
        # Create the BankAccount object using the data from JSON
        account_obj = BankAccount(
            target_id, 
            user_info['name'], 
            user_info['balance'], 
            user_info['history']
        )
        return account_obj, all_data
    else:
        print("User ID not found.")
        return None, None

def save_data(all_data, current_account):
    """Saves the updated object back into the dictionary and writes to file"""
    all_data[current_account.user_id] = {
        "name": current_account.name,
        "balance": current_account.balance,
        "history": current_account.history
    }
    with open('data.json', 'w') as f:
        json.dump(all_data, f, indent=4)
    print("\n[System: Progress Saved to data.json]")

# --- MAIN PROGRAM ---

user_input_id = input("Please enter your User ID: ")
current_account, full_database = load_account(user_input_id)

if current_account:
    print(f"\nWelcome, {current_account.name}!")
    
    while True:
        print("\n1. Deposit | 2. Withdraw | 3. Check Balance | 4. Show Transaction History | 5. save and exit")
        choice = input("Choose (1-5): ")

        if choice == "1":
            amt = float(input("Enter amount to deposit: "))
            print(current_account.deposit(amt))
        elif choice == "2":
            amt = float(input("Enter amount to withdraw: "))
            print(current_account.withdraw(amt))
        elif choice == "3":
            print(current_account.get_balance())
        elif choice == "4":
            n = int(input("How many recent transactions to show? "))
            current_account.print_history(n)
        elif choice == "5":
            save_data(full_database, current_account)
            print("Goodbye!")
            break
