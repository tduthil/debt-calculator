# calculator.py

# Import necessary libraries and modules
import streamlit as st
import copy
from models import Debt
from typing import List, Tuple, Dict


class DebtCalculator:
    @staticmethod
    def calculate_repayment(debts: List[Debt], additional_cash_flow: float) -> Tuple[List[Debt], float, float]:
        """
        Calculate monthly repayment with minimum payments separate from additional cash flow.
        
        Args:
        - debts: List of debts to process
        - additional_cash_flow: Extra money available BEYOND minimum payments
        
        Returns:
        - updated debts
        - remaining additional cash flow
        - total payment made
        """
        total_payment_made = 0.0
        remaining_cash_flow = additional_cash_flow
        
        # First, make all minimum payments (not using additional cash flow)
        for debt in debts:
            if debt.balance <= 0:
                continue
                
            # Make minimum payment
            if debt.balance <= debt.min_payment:
                # If balance is less than minimum payment, pay off the debt
                payment = debt.balance
                debt.balance = 0
            else:
                # Make the minimum payment
                payment = debt.min_payment
                debt.balance -= debt.min_payment
                
            total_payment_made += payment
        
        # Then apply additional cash flow to priority debt
        for debt in debts:
            if debt.balance <= 0:
                continue
                
            if remaining_cash_flow > 0:
                # Apply additional payment from cash flow
                additional_payment = min(remaining_cash_flow, debt.balance)
                debt.balance -= additional_payment
                total_payment_made += additional_payment
                remaining_cash_flow -= additional_payment
                
                if remaining_cash_flow <= 0:
                    break
        
        return debts, remaining_cash_flow, total_payment_made
    
    @staticmethod
    def calculate_repayment_schedule(debts: List[Debt], additional_cash_flow: float, months_to_display: int) -> tuple[List[Dict], int]:
        """
        Calculate the complete repayment schedule.
        
        Args:
        - debts: List of debts to process
        - additional_cash_flow: Extra money available BEYOND minimum payments
        - months_to_display: Maximum months to calculate
        
        Returns:
        - payment schedule
        - total months
        """
        payment_schedule = []
        current_cash_flow = additional_cash_flow
        total_months = 0
        
        # Make a deep copy of debts to avoid modifying the original list
        working_debts = copy.deepcopy(debts)
        sorted_debts = DebtCalculator.sort_debts_by_priority(working_debts)
        
        # Track total minimum payments for reference
        total_min_payments = sum(debt.min_payment for debt in debts)
        
        for month in range(1, months_to_display + 1):
            month_payments = []
            debts_snapshot = copy.deepcopy(sorted_debts)
            
            # Calculate payments for this month
            sorted_debts, remaining_cash_flow, total_payment = DebtCalculator.calculate_repayment(
                sorted_debts, 
                current_cash_flow
            )
            
            # Record payments and balances for each debt
            for original, current in zip(debts_snapshot, sorted_debts):
                payment = original.balance - current.balance if original.balance > current.balance else 0
                month_payments.append({
                    'month': month,
                    'creditor': current.creditor,
                    'min_payment': current.min_payment,
                    'additional_payment': max(0, payment - current.min_payment),
                    'total_payment': payment,
                    'balance': current.balance,
                    'cash_flow_used': current_cash_flow - remaining_cash_flow,
                    'remaining_cash_flow': remaining_cash_flow
                })
            
            payment_schedule.extend(month_payments)
            
            # When a debt is paid off, its minimum payment becomes additional cash flow
            newly_freed_payments = sum(
                debt.min_payment 
                for debt in sorted_debts 
                if debt.balance == 0 and debt.min_payment > 0
            )
            
            if newly_freed_payments > 0:
                current_cash_flow = additional_cash_flow + newly_freed_payments
                # Zero out minimum payments for paid off debts
                for debt in sorted_debts:
                    if debt.balance == 0:
                        debt.min_payment = 0
            
            total_months += 1
            
            # Check if all debts are paid off
            if all(debt.balance <= 0 for debt in sorted_debts):
                break
        
        return payment_schedule, total_months
    
    @staticmethod
    def sort_debts_by_priority(debts: List[Debt]) -> List[Debt]:
        """Sorts debts by cash flow recapture percentage."""
        return sorted(debts, key=lambda x: x.cash_flow_recap, reverse=True)