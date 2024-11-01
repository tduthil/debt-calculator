# display.py
import streamlit as st
import pandas as pd

class DebtDisplay:
    @staticmethod
    def create_debt_dataframe(debts: List[Debt]) -> pd.DataFrame:
        """Creates a DataFrame for displaying debt information."""
        formatter = Formatter()
        data = {
            'Creditor': [],
            'Balance': [],
            'Limit': [],
            'Utilization': [],
            'Min Payment': []
        }
        
        for debt in debts:
            data['Creditor'].append(debt.creditor)
            data['Balance'].append(formatter.format_currency(debt.balance))
            data['Limit'].append(formatter.format_currency(debt.limit))
            data['Utilization'].append(formatter.format_percentage(debt.utilization))
            data['Min Payment'].append(formatter.format_currency(debt.min_payment))
        
        return pd.DataFrame(data)
    
    @staticmethod
    def display_initial_debts(debts: List[Debt]):
        """Displays the initial debt information."""
        st.write("### Initial Debts")
        st.write("---")
        df = DebtDisplay.create_debt_dataframe(debts)
        st.dataframe(df, hide_index=True)
    
    @staticmethod
    def display_repayment_summary(total_months: int):
        """Displays the payoff summary."""
        years = total_months // 12
        months = total_months % 12
        st.write("### Payoff Summary")
        st.write(f"Total time to pay off all debts: {years} years, {months} months")