# main.py
import streamlit as st
from models import Debt
from validators import InputValidator
from formatters import Formatter
from calculator import DebtCalculator
from display import DebtDisplay
from input_handler import DebtInputHandler
from typing import List, Dict
import copy

# Set page config at the very top
st.set_page_config(
    page_title="Debt Repayment Calculator",
    page_icon="💰",
    layout="wide"
)

# Add custom CSS
st.markdown("""
    <style>
        /* Primary color updates */
        .stButton > button {
            background-color: #782F40;
            color: white;
        }
        .stButton > button:hover {
            background-color: #8F3A4D;  /* Slightly lighter for hover */
            color: white;
        }
        
        /* Progress bars */
        .stProgress > div > div {
            background-color: #782F40;
        }
        
        /* Slider */
        .stSlider .slider-track {
            background-color: rgba(120, 47, 64, 0.25);
        }
        .stSlider .slider-track .slider-track-selected {
            background-color: #782F40;
        }
        
        /* Metric color */
        .metric-label {
            color: #782F40 !important;
        }
        
        /* Headers */
        h1, h2, h3, h4, h5, h6 {
            color: #782F40;
        }
        
        /* Form submission button */
        .stFormSubmitButton > button {
            background-color: #782F40;
            color: white;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] button[data-baseweb="tab"] {
            color: #782F40;
        }
        .stTabs [data-baseweb="tab-list"] button[data-baseweb="tab"][aria-selected="true"] {
            color: #782F40;
            border-bottom-color: #782F40;
        }
        
        /* Custom container for header */
        .main-header {
            padding: 1.5rem;
            background-color: #782F40;
            color: white;
            border-radius: 0.5rem;
            margin-bottom: 2rem;
            text-align: center;
        }
        .main-header h1 {
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables if they don't exist."""
    if 'submitted' not in st.session_state:
        st.session_state.submitted = False
    if 'calculation_complete' not in st.session_state:
        st.session_state.calculation_complete = False
    if 'original_debts' not in st.session_state:
        st.session_state.original_debts = []
    if 'payment_schedule' not in st.session_state:
        st.session_state.payment_schedule = []

def reset_calculation():
    """Reset calculation-related session state variables."""
    st.session_state.submitted = False
    st.session_state.calculation_complete = False
    st.session_state.original_debts = []
    st.session_state.payment_schedule = []

def main():
    initialize_session_state()
    
    # Initialize components
    input_handler = DebtInputHandler()
    display = DebtDisplay()
    calculator = DebtCalculator()
    
    # Display header
    display.display_header()
    
    # Input Section
    with st.form(key="debt_calculator_form"):
        st.subheader("Enter Your Financial Information")
        
        col1, col2 = st.columns(2)
        with col1:
            monthly_cash_flow = st.number_input(
                "Monthly cash flow available for debt repayment:",
                min_value=0.0,
                step=0.01,
                help="Amount available each month beyond minimum payments"
            )
        
        with col2:
            months_to_display = st.number_input(
                "Maximum months to calculate:",
                min_value=1,
                value=60,
                step=1,
                help="Maximum number of months to calculate the repayment plan"
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
        has_errors = False
        
        for i in range(int(creditor_count)):
            st.write(f"### Debt {i + 1}")
            creditor, balance, limit, min_payment = input_handler.collect_debt_inputs(i)
            
            is_valid, error_message = InputValidator.validate_debt_input(
                creditor, balance, limit, min_payment
            )
            
            if not is_valid:
                st.error(f"Debt {i + 1}: {error_message}")
                has_errors = True
            else:
                debts.append(Debt.create(creditor, balance, limit, min_payment))
        
        submit_button = st.form_submit_button(label="Calculate Repayment Plan")
        
        if submit_button:
            st.session_state.submitted = True
            if not has_errors and debts:  # Make sure we have valid debts
                # Store original debts for progress tracking
                st.session_state.original_debts = copy.deepcopy(debts)
                
                # Calculate repayment schedule
                payment_schedule, total_months = calculator.calculate_repayment_schedule(
                    debts,
                    monthly_cash_flow,
                    months_to_display
                )
                
                st.session_state.payment_schedule = payment_schedule
                st.session_state.total_months = total_months
                st.session_state.calculation_complete = True
            elif has_errors:
                st.error("Please fix the errors before calculating the repayment plan.")
            elif not debts:
                st.error("Please enter at least one debt.")
    
    # Display results if calculation is complete
    if st.session_state.calculation_complete:
        display.display_repayment_plan(
            debts,
            st.session_state.original_debts,
            st.session_state.payment_schedule,
            st.session_state.total_months
        )
        
        # Add a reset button
        if st.button("Reset Calculator"):
            reset_calculation()
            st.rerun()  # Updated from experimental_rerun() to rerun()

if __name__ == "__main__":
    main()