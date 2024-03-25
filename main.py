import streamlit as st
import pandas as pd

from datetime import datetime, timedelta


# Function to calculate the payoff dates and milestones
def calculate_payoff_dates(total_loan_debt, total_credit_card_debt,
                           emergency_fund_target, investment_fund_target,
                           monthly_debt_payment, monthly_credit_card_payment,
                           monthly_expenses, monthly_income, monthly_savings,
                           monthly_investment, credit_card_apr):
    total_monthly_outgoings = monthly_debt_payment + \
                              monthly_credit_card_payment + \
                              monthly_expenses + \
                              monthly_savings + \
                              monthly_investment
    if total_monthly_outgoings > monthly_income:
        return "The sum of monthly payments exceeds monthly income. Please adjust your payments."

    # Initialize current date

    current_date = datetime.now()
    start_month = current_date.strftime("%B %Y")

    # Initialize accumulators
    current_emergency_funds = 0
    current_investment_funds = 0

    # Initialize goal achievement flags
    loan_paid_off_date = None
    credit_card_paid_off_date = None
    emergency_fund_achieved_date = None
    investment_fund_achieved_date = None

    # Initialize 50% goal achievement flags
    loan_half_paid_date = None
    credit_card_half_paid_date = None
    emergency_fund_half_achieved_date = None
    investment_fund_half_achieved_date = None

    half_loan_target = total_loan_debt / 2
    half_credit_card_target = total_credit_card_debt / 2
    half_emergency_fund_target = emergency_fund_target / 2
    half_investment_fund_target = investment_fund_target / 2

    while (
            total_loan_debt > 0
            or
            total_credit_card_debt > 0
            or
            current_emergency_funds < emergency_fund_target
            or
            current_investment_funds < investment_fund_target
    ):
        if total_loan_debt > 0:
            total_loan_debt -= monthly_debt_payment
            if total_loan_debt <= half_loan_target and not loan_half_paid_date:
                loan_half_paid_date = current_date
            if total_loan_debt <= 0 and not loan_paid_off_date:
                loan_paid_off_date = current_date

        if total_credit_card_debt > 0:
            monthly_interest = (total_credit_card_debt * (credit_card_apr / 100)) / 12
            total_credit_card_debt += monthly_interest - monthly_credit_card_payment
            if total_credit_card_debt <= half_credit_card_target and not credit_card_half_paid_date:
                credit_card_half_paid_date = current_date
            if total_credit_card_debt <= 0 and not credit_card_paid_off_date:
                credit_card_paid_off_date = current_date

        if current_emergency_funds < emergency_fund_target:
            current_emergency_funds += monthly_savings
            if current_emergency_funds >= half_emergency_fund_target and not emergency_fund_half_achieved_date:
                emergency_fund_half_achieved_date = current_date
            if current_emergency_funds >= emergency_fund_target and not emergency_fund_achieved_date:
                emergency_fund_achieved_date = current_date

        if current_investment_funds < investment_fund_target:
            current_investment_funds += monthly_investment
            if current_investment_funds >= half_investment_fund_target and not investment_fund_half_achieved_date:
                investment_fund_half_achieved_date = current_date
            if current_investment_funds >= investment_fund_target and not investment_fund_achieved_date:
                investment_fund_achieved_date = current_date

        # Move to the next month
        current_date += timedelta(days=30)  # Approximate, for simplicity

    # Format dates for output
    def format_date(date_):
        return date_.strftime("%B %Y") if date_ else "Goal not achieved within the timeframe"

    return {
        "Start Month": start_month,
        "Loan 50% Paid off": format_date(loan_half_paid_date),
        "Credit Card 50% Paid off": format_date(credit_card_half_paid_date),
        "Emergency Fund 50% Accrued": format_date(emergency_fund_half_achieved_date),
        "Investment Fund 50% Accrued": format_date(investment_fund_half_achieved_date),
        "Total Loan Pay-off": format_date(loan_paid_off_date),
        "Total Credit Card Pay-off": format_date(credit_card_paid_off_date),
        "Emergency Fund Locked in": format_date(emergency_fund_achieved_date),
        "Investment Fund Ready": format_date(investment_fund_achieved_date)
    }


def main():
    st.title("Freedom Forecast :crystal_ball:")
    col1, col2 = st.columns(2)
    # streamlit user inputs (total and targets)
    with col1:
        total_loan_debt = st.number_input(
            "Total Loan Debt",
            min_value=0,
            value=15000,
            step=500,
            placeholder="Enter the debt amount without commas or $..."
        )
        total_credit_card_debt = st.number_input(
            "Total Credit Card Debt",
            min_value=0,
            value=5000,
            step=500,
            placeholder="Enter the debt amount without commas or $..."
        )
    with col2:
        # st.header("Financial Targets")
        emergency_fund_target = st.number_input(
            "Emergency Fund Target",
            min_value=0,
            value=6000,
            step=500,
            placeholder="Enter the amount without commas or $..."
        )
        investment_fund_target = st.number_input(
            "Investment Fund Target",
            min_value=0,
            value=100000,
            step=500,
            placeholder="Enter the amount without commas or $..."
        )

    # streamlit user inputs (monthly average)
    st.write("## Average Monthly Transactions")
    col1, col2, col3 = st.columns(3)
    with col1:
        monthly_debt_payment = st.number_input(
            "Debt payment",
            min_value=0,
            value=500,
            step=100,
            placeholder="Enter the amount without commas or $..."
        )
        monthly_credit_card_payment = st.number_input(
            "Credit Card Debt payment",
            min_value=0,
            value=500,
            step=100,
            placeholder="Enter the amount without commas or $..."
        )
    with col2:
        monthly_expenses = st.number_input(
            "Expenses",
            min_value=0,
            value=1500,
            step=100,
            placeholder="Enter the amount without commas or $..."
        )
        monthly_income = st.number_input(
            "Income",
            min_value=0,
            value=5000,
            step=500,
            placeholder="Enter the amount without commas or $..."
        )
    with col3:
        monthly_savings = st.number_input(
            "Savings",
            min_value=0,
            value=1000,
            step=100,
            placeholder="Enter the amount without commas or $..."
        )
        monthly_investment = st.number_input(
            "Investment",
            min_value=0,
            value=250,
            step=50,
            placeholder="Enter the amount without commas or $..."
        )

    credit_card_apr = st.slider("Average APR for credit card (%) ?", min_value=0, max_value=100, step=1, value=20)

    results = calculate_payoff_dates(total_loan_debt=total_loan_debt,
                                     total_credit_card_debt=total_credit_card_debt,
                                     emergency_fund_target=emergency_fund_target,
                                     investment_fund_target=investment_fund_target,
                                     monthly_debt_payment=monthly_debt_payment,
                                     monthly_credit_card_payment=monthly_credit_card_payment,
                                     monthly_expenses=monthly_expenses,
                                     monthly_income=monthly_income,
                                     monthly_savings=monthly_savings,
                                     monthly_investment=monthly_investment,
                                     credit_card_apr=credit_card_apr)

    st.header("Progress Tracker")
    st.write("You are now on the right track to being debt-free and achieving your financial targets! :trophy:")

    if isinstance(results, dict):
        data = {
            "Category 📋": ["Loan Payment 💰", "Credit Card Payment 💳", "Emergency Fund 🚑", "Investment 📈"],
            "Start Month 🗓️": [results["Start Month"], results["Start Month"], results["Start Month"],
                               results["Start Month"]],
            "50% milestone 🏁": [
                results["Loan 50% Paid off"],
                results["Credit Card 50% Paid off"],
                results["Emergency Fund 50% Accrued"],
                results["Investment Fund 50% Accrued"]
            ],
            "Achievement Done 🔓": [
                results["Total Loan Pay-off"],
                results["Total Credit Card Pay-off"],
                results["Emergency Fund Locked in"],
                results["Investment Fund Ready"]
            ]
        }

        df = pd.DataFrame(data)
        st.dataframe(df, hide_index=True, use_container_width=True)
        current_time = datetime.now()
        download_data = f'''
            Start Month 🗓️: {results['Start Month']}\n
            Total Loan Debt 💰: ${total_loan_debt}
            Total Credit card debt 💳: ${total_credit_card_debt}
            Emergency fund target 🚑: ${emergency_fund_target}
            Investment fund target 📈: ${investment_fund_target}\n
            
            Average monthly transactions\n
            Debt payment: ${monthly_debt_payment}
            Credit card payment: ${monthly_credit_card_payment}
            Credit card APR: {credit_card_apr}%
            Expenses: ${monthly_expenses}
            Income: ${monthly_income}
            Savings: ${monthly_savings}
            Investment: ${monthly_investment}\n
            
            50% Milestone reached 🏁\n
            Loan 50% Paid off Month: {results['Loan 50% Paid off']}
            Credit Card 50% Paid off Month: {results['Credit Card 50% Paid off']}
            Emergency Fund 50% Accrued Month: {results['Emergency Fund 50% Accrued']}
            Investment Fund 50% Accrued Month: {results['Investment Fund 50% Accrued']}
            
            Achievement Unlocked 🔓\n
            Total Loan Pay-off Month: {results['Total Loan Pay-off']}
            Total Credit Card Pay-off Month: {results['Total Credit Card Pay-off']}
            Emergency Fund Locked in Month: {results['Emergency Fund Locked in']}
            Investment Fund Ready Month: {results['Investment Fund Ready']}
            
            Snapshot generation time: {current_time.strftime('%Y-%m-%d::%H:%M:%S')}
        '''
        st.download_button(
            label="Download snapshot to Freedom",
            data=download_data,
            type="secondary",
            file_name=f"snapshot_{current_time.strftime('%Y%m%d%H%M%S')}.txt"
        )
    else:
        st.write(f":red[{results}]")


if __name__ == "__main__":
    main()
