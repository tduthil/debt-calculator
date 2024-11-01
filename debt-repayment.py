#install libraries######
###how to start project
# Create a new project folder
##mkdir myproject

# Navigate to the project folder
##cd myproject

# Create a new virtual environment
##python -m venv .venv

# Activate the virtual environment
##source .venv/Scripts/activate --start here after its been created once

# Install Streamlit
##pip install streamlit

# Test that the installation worked
#streamlit hello
#Run application
#streamlit run Greater_Orlando_Dashboard.py

##########################


import streamlit as st
from prettytable import PrettyTable

def apply_initial_cash_flow(debts, initial_cash_flow):
    """Applies the initial cash flow, along with any remaining cash, to the highest priority debt."""
    first_payment = 0  # Track the payment applied to the first debt

    # Apply payments to the first debt
    first_debt = debts[0]
    creditor, balance, limit, utilization, cash_flow_recap, min_payment = first_debt
    payment = min(balance, initial_cash_flow + min_payment)  # Total payment to the first debt
    ending_balance = balance - payment
    debts[0] = (creditor, ending_balance, limit, utilization, cash_flow_recap, min_payment)
    first_payment = payment  # Record the first payment

    # If the first debt is paid off, add its min payment to cash flow
    if ending_balance == 0:
        initial_cash_flow += min_payment

    # Return updated debts and the new initial cash flow, plus the first payment applied
    return debts, initial_cash_flow, first_payment



def pay_minimum_payments(debts):
    """Pays minimum payments to all debts except the highest priority debt."""
    payments = []  # Track payments for display
    for i in range(1, len(debts)):  # Start from the second debt
        creditor, balance, limit, utilization, cash_flow_recap, min_payment = debts[i]
        if balance > 0:  # Only pay if there's a balance
            payment = min(balance, min_payment)
            ending_balance = balance - payment
            debts[i] = (creditor, ending_balance, limit, utilization, cash_flow_recap, min_payment)
            payments.append((creditor, balance, payment, ending_balance))  # Track payment details for display
    return debts, payments


def calculate_total_payoff_time(debts, initial_cash_flow):
    """Calculates the total months needed to pay off all debts without display limit."""
    total_months = 0
    debts_sorted = sort_debts_by_cash_flow_recap(debts)

    while any(balance > 0 for _, balance, _, _, _, _ in debts_sorted):
        # Apply initial cash flow to the highest priority debt
        debts_sorted, initial_cash_flow, _ = apply_initial_cash_flow(debts_sorted, initial_cash_flow)

        # Pay minimum payments to other debts
        debts_sorted, _ = pay_minimum_payments(debts_sorted)

        # Remove fully paid debts
        debts_sorted = remove_paid_off_debts(debts_sorted)

        # Update initial cash flow if the first debt is fully paid off
        if debts_sorted and debts_sorted[0][1] == 0:
            initial_cash_flow += debts_sorted[0][5]  # Add min payment of paid-off debt to cash flow

        total_months += 1

    return total_months


def display_repayment_plan(debts, initial_cash_flow, months_to_display):
    st.write("\n### Repayment Plan:")
    st.write("=================================================================")

    current_month = 1
    debts_sorted = sort_debts_by_cash_flow_recap(debts)
    table = PrettyTable()
    table.field_names = ["Month", "Creditor", "Starting Balance", "Payment", "Ending Balance"]

    while current_month <= months_to_display and any(balance > 0 for _, balance, _, _, _, _ in debts_sorted):
        remaining_cash_flow = initial_cash_flow  # Reset remaining cash flow each month

        for idx, (creditor, balance, limit, utilization, cash_flow_recap, min_payment) in enumerate(debts_sorted):
            if balance > 0:
                # Calculate payment for this debt
                if idx == 0:
                    payment = min(remaining_cash_flow, balance)
                    remaining_cash_flow -= payment
                else:
                    payment = min(min_payment, balance)
                
                # Calculate new balance after payment
                new_balance = max(balance - payment, 0)

                # Add row to PrettyTable for the month
                table.add_row([
                    current_month,
                    creditor,
                    f"${balance:,.2f}",
                    f"${payment:,.2f}",
                    f"${new_balance:,.2f}"
                ])

                # Update the debt with the new balance
                debts_sorted[idx] = (creditor, new_balance, limit, utilization, cash_flow_recap, min_payment)

        # Remove debts with zero balance
        debts_sorted = [debt for debt in debts_sorted if debt[1] > 0]

        # Update initial cash flow if a debt was paid off
        if debts_sorted and debts_sorted[0][1] == 0:
            initial_cash_flow += debts_sorted[0][5]

        # Increment the month
        current_month += 1

    # Print the PrettyTable
    st.write(table)
    st.write("=================================================================")
    display_payoff_summary(current_month - 1)



def display_payoff_summary(total_months):
    years = total_months // 12
    months = total_months % 12
    summary_table = PrettyTable()
    summary_table.field_names = ["Total Time to Pay Off All Debts"]
    summary_table.add_row([f"{years} years, {months} months"])
    st.write(summary_table)


def sort_debts_by_cash_flow_recap(debts):
    """Sorts debts by cash flow recapture percentage in descending order."""
    return sorted(debts, key=lambda x: x[4], reverse=True)

def pay_minimum_payments(debts):
    """Pays minimum payments to all debts except the highest priority debt."""
    payments = []  # Track payments for display
    for i in range(1, len(debts)):
        creditor, balance, limit, utilization, cash_flow_recap, min_payment = debts[i]
        payment = min(balance, min_payment)
        ending_balance = balance - payment
        debts[i] = (creditor, ending_balance, limit, utilization, cash_flow_recap, min_payment)
        payments.append((creditor, balance, payment, ending_balance))  # Track payment details for display
    return debts, payments

def remove_paid_off_debts(debts):
    """Removes fully paid-off debts from the list."""
    return [debt for debt in debts if debt[1] > 0]



def print_initial_debts(debts):
    """Displays the initial debts before starting the repayment plan."""
    st.write("\n### Initial Debts:")
    st.write("=================================================================")

    # Create a PrettyTable for the initial debts
    initial_debt_table = PrettyTable()
    initial_debt_table.field_names = ["Creditor", "Balance", "Limit", "Utilization", "Min Payment"]

    for creditor, balance, limit, utilization, cash_flow_recap, min_payment in debts:
        initial_debt_table.add_row([
            creditor,
            f"${balance:,.2f}", 
            f"${limit:,.2f}",
            f"{utilization:.2f}%",
            f"${min_payment:,.2f}"
        ])

    # Display the initial debt table
    st.write(initial_debt_table)

    st.write("=================================================================")


def display_payoff_summary(total_months):
    years = total_months // 12
    months = total_months % 12
    summary_table = PrettyTable()
    summary_table.field_names = ["Total Time to Pay Off All Debts"]
    summary_table.add_row([f"{years} years, {months} months"])
    st.write(summary_table)




def debt_repayment_calculator():
    """Main function to gather debt information and calculate repayment plan."""
    st.title("Debt Repayment Calculator")

    monthly_cash_flow = st.number_input("Enter your initial monthly cash flow:", min_value=0.0, step=0.01)
    months_to_display = st.number_input("Enter the number of months to display repayment for (optional):", min_value=1, step=1)

    debts = []
    creditor_count = st.number_input("Enter the number of creditors:", min_value=1, step=1)

    for i in range(creditor_count):
        creditor = st.text_input(f"Enter creditor name for debt {i + 1}:")
        balance = st.number_input(f"Enter balance for {creditor}:", min_value=0.0, step=0.01)
        limit = st.number_input(f"Enter credit limit for {creditor}:", min_value=0.0, step=0.01)
        min_payment = st.number_input(f"Enter minimum payment for {creditor}:", min_value=0.0, step=0.01)

        # Calculate Cash Flow Recap % and Utilization %
        cash_flow_recap = (min_payment / balance) * 100 if balance > 0 else 0
        utilization = (balance / limit) * 100 if limit > 0 else 0

        # Append the debt information as a tuple
        debts.append((creditor, balance, limit, utilization, cash_flow_recap, min_payment))

    if st.button("Calculate Repayment Plan"):
        print_initial_debts(debts)
        display_repayment_plan(debts, monthly_cash_flow, months_to_display)
        

if __name__ == "__main__":
    debt_repayment_calculator()
