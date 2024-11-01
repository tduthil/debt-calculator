# calculator.py
class DebtCalculator:
    @staticmethod
    def calculate_repayment(debts: List[Debt], initial_cash_flow: float) -> Tuple[List[Debt], float, float]:
        """Calculates one month of debt repayment."""
        if not debts:
            return debts, initial_cash_flow, 0
        
        first_debt = debts[0]
        payment = min(first_debt.balance, initial_cash_flow + first_debt.min_payment)
        ending_balance = first_debt.balance - payment
        
        debts[0] = Debt.create(
            first_debt.creditor,
            ending_balance,
            first_debt.limit,
            first_debt.min_payment
        )
        
        if ending_balance == 0:
            initial_cash_flow += first_debt.min_payment
        
        return debts, initial_cash_flow, payment
    
    @staticmethod
    def sort_debts_by_priority(debts: List[Debt]) -> List[Debt]:
        """Sorts debts by cash flow recapture percentage."""
        return sorted(debts, key=lambda x: x.cash_flow_recap, reverse=True)