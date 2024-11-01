# input_handler.py
class DebtInputHandler:
    def __init__(self):
        self.validator = InputValidator()
    
    def collect_debt_inputs(self, index: int) -> Tuple[str, float, float, float]:
        """Collects inputs for a single debt."""
        col1, col2 = st.columns(2)
        
        with col1:
            creditor = st.text_input(f"Creditor name:", key=f"creditor_{index}")
            balance = st.number_input(f"Current balance:", min_value=0.0, step=0.01, key=f"balance_{index}")
        
        with col2:
            limit = st.number_input(f"Credit limit:", min_value=0.0, step=0.01, key=f"limit_{index}")
            min_payment = st.number_input(f"Minimum payment:", min_value=0.0, step=0.01, key=f"min_payment_{index}")
        
        return creditor, balance, limit, min_payment