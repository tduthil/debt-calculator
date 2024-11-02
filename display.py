# display.py
import streamlit as st
import pandas as pd
import altair as alt
from models import Debt
from formatters import Formatter
from typing import List, Dict

class DebtDisplay:
    def __init__(self):
        self.formatter = Formatter()

    def display_header(self):
        """Displays the application header with styling."""
        st.title("💰 Debt Repayment Calculator")
        st.markdown("Track your path to financial freedom")

    def get_month_data(self, payment_schedule: List[Dict], month: int) -> Dict:
        """Get the debt states for a specific month."""
        month_data = {}
        for payment in payment_schedule:
            if payment['month'] == month:
                month_data[payment['creditor']] = {
                    'balance': payment['balance'],
                    'payment': payment['payment']
                }
        return month_data

    def display_progress_metrics(self, debts: List[Debt], original_debts: List[Debt], 
                               payment_schedule: List[Dict]):
        """Displays key metrics and progress bars for selected month."""
        # Get unique months from payment schedule
        months = sorted(list(set(payment['month'] for payment in payment_schedule)))
        
        st.markdown("### View Progress By Month")
        selected_month = st.select_slider(
            "Select month to view progress:",
            options=months,
            value=1,  # Default to first month
            format_func=lambda x: f"Month {x}"
        )
        
        # Get data for selected month
        month_data = self.get_month_data(payment_schedule, selected_month)
        
        # Calculate progress for selected month
        total_original = sum(d.balance for d in original_debts)
        total_current = sum(data['balance'] for data in month_data.values())
        total_progress = ((total_original - total_current) / total_original * 100) if total_original > 0 else 100
        
        # Display metrics for selected month
        st.markdown(f"#### Status at Month {selected_month}")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Original Debt", 
                self.formatter.format_currency(total_original)
            )
        with col2:
            st.metric(
                "Current Debt", 
                self.formatter.format_currency(total_current)
            )
        with col3:
            st.metric(
                "Total Progress", 
                f"{round(total_progress, 1)}%"
            )

        # Display individual debt progress
        st.markdown("#### Individual Debt Progress")
        for debt in original_debts:
            if debt.creditor in month_data:
                current_balance = month_data[debt.creditor]['balance']
                original_balance = debt.balance
                if original_balance > 0:
                    progress = ((original_balance - current_balance) / original_balance * 100)
                    
                    # Create columns for each piece of information
                    cols = st.columns([3, 1, 1, 1])
                    with cols[0]:
                        st.progress(progress / 100)
                    with cols[1]:
                        st.write(f"{debt.creditor}")
                    with cols[2]:
                        st.write(f"{round(progress, 1)}%")
                    with cols[3]:
                        st.write(self.formatter.format_currency(current_balance))

    def display_payment_schedule(self, payment_schedule: List[Dict]):
        """Displays the monthly payment schedule."""
        st.markdown("### Payment Schedule")
        
        # Create DataFrame for payment schedule
        df = pd.DataFrame(payment_schedule)
        
        # Create tabs for different views
        tab1, tab2 = st.tabs(["📊 Chart View", "📑 Table View"])
        
        with tab1:
            # Create payment chart
            chart_data = df.copy()
            chart = alt.Chart(chart_data).mark_line(point=True).encode(
                x=alt.X('month:Q', title='Month'),
                y=alt.Y('balance:Q', title='Balance ($)'),
                color=alt.Color('creditor:N', title='Creditor'),
                tooltip=['month', 'creditor', 'payment', 'balance']
            ).properties(
                width=700,
                height=400,
                title='Debt Payoff Timeline'
            ).interactive()
            
            st.altair_chart(chart, use_container_width=True)
        
        with tab2:
            # Display detailed table
            st.dataframe(
                df,
                column_config={
                    "month": "Month",
                    "creditor": "Creditor",
                    "payment": st.column_config.NumberColumn(
                        "Payment",
                        format="$%.2f"
                    ),
                    "balance": st.column_config.NumberColumn(
                        "Remaining Balance",
                        format="$%.2f"
                    ),
                    "cash_flow_used": st.column_config.NumberColumn(
                        "Cash Flow Used",
                        format="$%.2f"
                    ),
                    "remaining_cash_flow": st.column_config.NumberColumn(
                        "Remaining Cash Flow",
                        format="$%.2f"
                    )
                },
                hide_index=True
            )

    def display_summary(self, total_months: int):
        """Displays the final payoff summary."""
        st.markdown("### 📋 Payoff Summary")
        
        years = total_months // 12
        months = total_months % 12
        
        st.metric(
            "Time to Debt Freedom",
            f"{years} years, {months} months"
        )

    def display_repayment_plan(self, debts: List[Debt], original_debts: List[Debt], 
                             payment_schedule: List[Dict], total_months: int):
        """Main method to display the complete repayment plan."""
        st.markdown("---")
        self.display_progress_metrics(debts, original_debts, payment_schedule)
        
        st.markdown("---")
        self.display_payment_schedule(payment_schedule)
        
        st.markdown("---")
        self.display_summary(total_months)