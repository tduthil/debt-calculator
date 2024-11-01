# models.py
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Debt:
    creditor: str
    balance: float
    limit: float
    utilization: float
    cash_flow_recap: float
    min_payment: float

    @classmethod
    def create(cls, creditor: str, balance: float, limit: float, min_payment: float) -> 'Debt':
        """Factory method to create a Debt instance with calculated fields."""
        utilization = (balance / limit * 100) if limit > 0 else 0
        cash_flow_recap = (min_payment / balance * 100) if balance > 0 else 0
        return cls(creditor, balance, limit, utilization, cash_flow_recap, min_payment)