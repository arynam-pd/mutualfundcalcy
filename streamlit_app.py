import streamlit as st
import matplotlib.pyplot as plt

def calculate_lump_sum(amount, interest_rate, time_period):
    # Calculate the future value of a lump sum investment
    future_value = amount * (1 + interest_rate / 100) ** time_period
    return future_value

def calculate_sip(amount, interest_rate, time_period):
    # Calculate the future value of a series of periodic SIP investments
    monthly_rate = (interest_rate / 100) / 12
    future_value = 0
    for i in range(time_period * 12):
        future_value += amount * (1 + monthly_rate) ** (time_period * 12 - i)
    return future_value

def calculate_invested_amount(amount, time_period):
    # Calculate the total amount invested up to the specified time period
    return amount * time_period

def calculate_future_values(amount, interest_rate, investment_type, start_period, end_period):
    future_values = []
    invested_amounts = []
    for year in range(start_period, end_period + 1):
        if investment_type == "Lump Sum":
            future_value = calculate_lump_sum(amount, interest_rate, year)
        elif investment_type == "SIP":
            future_value = calculate_sip(amount, interest_rate, year)
        future_values.append(future_value)
        invested_amount = calculate_invested_amount(amount, year)
        invested_amounts.append(invested_amount)
    return future_values, invested_amounts

# Streamlit UI
st.title("Mutual Fund Calculator")

# User inputs
investment_type = st.selectbox("Select the type of investment", ("Lump Sum", "SIP"))
amount = st.number_input("Enter the amount", min_value=0.0, step=100.0)
interest_rate = st.number_input("Enter the expected annual interest rate (in %)", min_value=0.0, step=0.1)
time_period = st.number_input("Enter the time period (in years)", min_value=1, step=1)

# Calculate based on investment type
if st.button("Calculate"):
    # Calculate future values and invested amounts from 1 to the end period
    future_values, invested_amounts = calculate_future_values(amount, interest_rate, investment_type, 1, time_period + 10)
    
    # Display result for the specified period to next 10 years
    result_html = """
    <div style="border: 2px solid #4CAF50; padding: 5px; border-radius: 10px;">
        <h5 style="color: green;">Future Values of Your Investment:</h5>
        <ul>
    """
    
    for i, value in enumerate(future_values[time_period-1:time_period + 10]):
        year = time_period + i
        difference = value - invested_amounts[time_period + i - 1]
        if i > 0:
            result_html += f"<li>Year {year}: <b>Future Value: {value:.2f}</b> | <b>Invested Amount: {invested_amounts[time_period + i - 1]:.2f}</b> | <b>Difference: {difference:.2f}</b></li>"
        else:
            result_html += f"<li>Year {year}: <b>Future Value: {value:.2f}</b> | <b>Invested Amount: {invested_amounts[time_period + i - 1]:.2f}</b></li>"

    result_html += """
        </ul>
    </div>
    """
    
    st.markdown(result_html, unsafe_allow_html=True)

    # Add some space above the graph
    st.markdown("<br><br>", unsafe_allow_html=True)

    # Plot the graph from year 1 to end period
    years = list(range(1, time_period + 11))
    plt.figure(figsize=(10, 6))
    plt.plot(years, future_values, marker='o', linestyle='-', color='b', label='Future Value')
    plt.xlabel('Years')
    plt.ylabel('Future Value')
    plt.title('Future Value of Investment Over Time')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)
