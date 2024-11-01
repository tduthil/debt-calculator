# validators.py
class InputValidator:
    @staticmethod
    def validate_creditor(creditor: str) -> bool:
        return bool(creditor.strip())
    
    @staticmethod
    def validate_amount(amount: float) -> bool:
        return amount >= 0
    
    @staticmethod
    def validate_min_payment(min_payment: float, balance: float) -> bool:
        return min_payment >= 0 and (balance == 0 or min_payment <= balance)
    
    @staticmethod
    def validate_debt_input(creditor: str, balance: float, limit: float, min_payment: float) -> Tuple[bool, str]:
        if not InputValidator.validate_creditor(creditor):
            return False, "Creditor name cannot be empty"
        if not InputValidator.validate_amount(balance):
            return False, "Balance cannot be negative"
        if not InputValidator.validate_amount(limit):
            return False, "Credit limit cannot be negative"
        if not InputValidator.validate_min_payment(min_payment, balance):
            return False, "Invalid minimum payment amount"
        return True, ""