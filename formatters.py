# formatters.py
class Formatter:
    @staticmethod
    def format_currency(amount: float) -> str:
        return f"${amount:,.2f}"
    
    @staticmethod
    def format_percentage(value: float) -> str:
        return f"{value:.2f}%"