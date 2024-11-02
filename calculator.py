# calculator.py

# Import necessary libraries and modules
import streamlit as st
import copy
from models import Debt
from typing import List, Tuple, Dict


class DebtCalculator:
    @staticmethod
    def calculate_repayment(debts: List[Debt], monthly_cash_flow: float) -> Tuple[List[Debt], float, float]:
        """
        Calculate monthly repayment.
        
        Returns:
        - updated debts
        - new monthly cash flow
        - payment made
        """
        payment_made = 0.0
        remaining_cash_flow = monthly_cash_flow
        original_cash_flow = monthly_cash_flow
        
        for debt in debts:
            if debt.balance <= 0:
                continue
                
            # Calculate total available payment
            total_payment = debt.min_payment + remaining_cash_flow
            
            if total_payment >= debt.balance:
                # Can pay off the debt completely
                actual_payment = debt.balance
                payment_made += actual_payment
                remaining_cash_flow = total_payment - actual_payment
                
                # Add freed up minimum payment to cash flow
                monthly_cash_flow = original_cash_flow + debt.min_payment
                
                # Clear the debt
                debt.balance = 0
                
            else:
                # Partial payment
                debt.balance -= total_payment
                payment_made += total_payment
                remaining_cash_flow = 0
                break
                
        return debts, monthly_cash_flow, payment_made
    
    @staticmethod
    def calculate_repayment_schedule(debts: List[Debt], monthly_cash_flow: float, months_to_display: int) -> tuple[List[Dict], int]:
        """
        Calculate the complete repayment schedule.
        Returns:
        - payment schedule
        - total months
        """
        payment_schedule = []
        current_cash_flow = monthly_cash_flow
        total_months = 0
        
        # Make a deep copy of debts to avoid modifying the original list
        working_debts = copy.deepcopy(debts)
        sorted_debts = DebtCalculator.sort_debts_by_priority(working_debts)
        
        for month in range(1, months_to_display + 1):
            month_payments = []
            debts_snapshot = copy.deepcopy(sorted_debts)
            
            # Calculate payments for this month
            sorted_debts, new_cash_flow, payment_made = DebtCalculator.calculate_repayment(
                sorted_debts, 
                current_cash_flow
            )
            
            # Record payments and balances for each debt
            for original, current in zip(debts_snapshot, sorted_debts):
                payment = original.balance - current.balance if original.balance > current.balance else 0
                month_payments.append({
                    'month': month,
                    'creditor': current.creditor,
                    'payment': payment,
                    'balance': current.balance,
                    'cash_flow_used': payment_made,
                    'remaining_cash_flow': new_cash_flow
                })
            
            payment_schedule.extend(month_payments)
            current_cash_flow = new_cash_flow
            total_months += 1
            
            # Check if all debts are paid off
            if all(debt.balance <= 0 for debt in sorted_debts):
                break
        
        return payment_schedule, total_months
    
    @staticmethod
    def sort_debts_by_priority(debts: List[Debt]) -> List[Debt]:
        """Sorts debts by cash flow recapture percentage."""
        return sorted(debts, key=lambda x: x.cash_flow_recap, reverse=True)