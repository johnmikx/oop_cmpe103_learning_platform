"""
Encapsulation Example: BankAccount Class
Demonstrates private attributes, getters/setters, and data protection
"""

from datetime import datetime
from typing import List, Dict

class BankAccount:
    """
    Demonstrates ENCAPSULATION - the first pillar of OOP
    
    Private attributes:
    - __account_number (private)
    - __balance (private) 
    - __transactions (private)
    
    Public interface through methods to access/modify private data
    """
    
    def __init__(self, account_number: str, initial_balance: float = 0.0):
        # ⬅️ ENCAPSULATION: Private attributes (name mangling with __)
        self.__account_number = account_number
        self.__balance = initial_balance
        self.__transactions: List[Dict] = []
        
        # Record initial deposit
        if initial_balance > 0:
            self.__add_transaction("Initial Deposit", initial_balance)
    
    # ⬅️ ENCAPSULATION: Getter methods (controlled access to private data)
    def get_account_number(self) -> str:
        """Public method to access private account number"""
        return self.__account_number
    
    def get_balance(self) -> float:
        """Public method to access private balance"""
        return self.__balance
    
    def get_transaction_history(self) -> List[Dict]:
        """Public method to access private transaction history"""
        return self.__transactions.copy()  # Return copy to prevent external modification
    
    # ⬅️ ENCAPSULATION: Controlled modification of private data
    def deposit(self, amount: float) -> bool:
        """
        Public method to modify private balance (with validation)
        Demonstrates controlled access to private data
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        
        self.__balance += amount
        self.__add_transaction("Deposit", amount)
        return True
    
    def withdraw(self, amount: float) -> bool:
        """
        Public method to modify private balance (with business rules)
        Demonstrates encapsulation of business logic
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        
        if amount > self.__balance:
            raise ValueError("Insufficient funds")
        
        self.__balance -= amount
        self.__add_transaction("Withdrawal", -amount)
        return True
    
    # ⬅️ ENCAPSULATION: Private helper method (internal implementation detail)
    def __add_transaction(self, transaction_type: str, amount: float):
        """Private method - internal implementation detail hidden from outside"""
        transaction = {
            'type': transaction_type,
            'amount': amount,
            'timestamp': datetime.now().isoformat(),
            'balance_after': self.__balance
        }
        self.__transactions.append(transaction)
    
    # ⬅️ ENCAPSULATION: String representation without exposing internal structure
    def __str__(self) -> str:
        """Public interface for object representation"""
        return f"BankAccount({self.__account_number}): ${self.__balance:.2f}"
    
    def get_account_summary(self) -> Dict:
        """
        Public method returning summary without exposing private attributes directly
        Demonstrates controlled data access
        """
        return {
            'account_number': self.__account_number,
            'current_balance': self.__balance,
            'total_transactions': len(self.__transactions),
            'last_transaction': self.__transactions[-1] if self.__transactions else None
        }

# Example usage demonstrating encapsulation principles
if __name__ == "__main__":
    # Create account
    account = BankAccount("ACC123", 1000.0)
    
    # ✅ Correct way - using public interface
    print(f"Balance: ${account.get_balance()}")
    account.deposit(500.0)
    account.withdraw(200.0)
    
    # ❌ This would be wrong - direct access to private attributes
    # print(account.__balance)  # This would cause AttributeError
    
    # ✅ Correct way - using public methods
    print(f"Final balance: ${account.get_balance()}")
    print(f"Transaction count: {len(account.get_transaction_history())}")
