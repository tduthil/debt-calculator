# main.py
def main():
    st.set_page_config(
        page_title="Debt Repayment Calculator",
        page_icon="💰",
        layout="wide"
    )
    
    st.title("Debt Repayment Calculator")
    
    input_handler = DebtInputHandler()
    calculator = DebtCalculator()
    display = DebtDisplay()
    
    with st.form(key="debt_calculator_form"):
        st.subheader("Enter Your Financial Information")
        
        monthly_cash_flow = st.number_input(
            "Monthly cash flow available for debt repayment:",
            min_value=0.0,
            step=0.01,
            help="Amount available each month beyond minimum payments"
        )
        
        months_to_display = st.number_input(
            "Number of months to display in repayment plan:",
            min_value=1,
            value=12,
            step=1,
            help="How many months of the repayment plan you want to see"
        )
        
        creditor_count = st.number_input(
            "Number of creditors:",
            min_value=1,
            value=1,
            step=1,
            help="How many debts do you want to analyze?"
        )
        
        # Collect debt inputs
        debts = []
        for i in range(int(creditor_count)):
            st.write(f"### Debt {i + 1}")
            creditor, balance, limit, min_payment = input_handler.collect_debt_inputs(i)
            is_valid, error_message = InputValidator.validate_debt_input(
                creditor, balance, limit, min_payment
            )
            if not is_valid:
                st.error(f"Debt {i + 1}: {error_message}")
            else:
                debts.append(Debt.create(creditor, balance, limit, min_payment))
        
        submit_button = st.form_submit_button(label="Calculate Repayment Plan")
    
    if submit_button and debts:
        display.display_initial_debts(debts)
        sorted_debts = calculator.sort_debts_by_priority(debts)
        # Continue with repayment calculation and display...

if __name__ == "__main__":
    main()