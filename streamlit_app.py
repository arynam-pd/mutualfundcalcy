import streamlit as st
import matplotlib.pyplot as plt

def calculate_lump_sum(amount, interest_rate, time_period):
    # Calculate the future value of a lump sum investment
    future_value = amount * (1 + interest_rate / 100) ** time_period
    return future_value

def calculate_sip(amount, interest_rate, time_period):
    # Calculate the future value of a series of periodic SIP investments
    monthly_rate = (interest_rate / 100) / 12
    future_values = []
    invested_amount = 0
    for i in range(time_period * 12):
        invested_amount += amount
        future_value = invested_amount * (1 + monthly_rate) ** (time_period * 12 - i)
        future_values.append(future_value)
    return future_values, invested_amount

def calculate_future_values(amount, interest_rate, investment_type, start_period, end_period):
    future_values = []
    invested_amount = 0
    
    for year in range(start_period, end_period + 1):
        if investment_type == "Lump Sum":
            future_value = calculate_lump_sum(amount, interest_rate, year)
            future_values.append(future_value)
        elif investment_type == "SIP":
            future_values, invested_amount = calculate_sip(amount, interest_rate, year)
            break  # Only need to calculate invested amount once for SIP

    return future_values, invested_amount

# Streamlit UI
st.title("Mutual Fund Calculator")

# User inputs
investment_type = st.selectbox("Select the type of investment", ("Lump Sum", "SIP"))
amount = st.number_input("Enter the amount", min_value=0.0, step=100.0)
interest_rate = st.number_input("Enter the expected annual interest rate (in %)", min_value=0.0, step=0.1)
time_period = st.number_input("Enter the time period (in years)", min_value=1, step=1)

# Calculate based on investment type
if st.button("Calculate"):
    # Calculate future values and optionally invested amount for SIP
    future_values, invested_amount = calculate_future_values(amount, interest_rate, investment_type, 1, time_period + 10)
    
    # Display result for the specified period to next 10 years
    result_html = """
    <div style="border: 2px solid #4CAF50; padding: 5px; border-radius: 10px;">
        <h5 style="color: green;">Future Values of Your Investment:</h5>
        <ul>
    """
    
    if investment_type == "SIP":
        result_html += f"<li>Invested Amount (total up to year {time_period}): <b>{invested_amount:.2f}</b></li>"
    
    for i, value in enumerate(future_values[time_period-1:time_period + 10]):
        year = time_period + i
        difference = value - invested_amount
        if i > 0:
            result_html += f"<li>Year {year}: <b>Future Value: {value:.2f}</b> | <b>Difference: {difference:.2f}</b></li>"
        else:
            result_html += f"<li>Year {year}: <b>Future Value: {value:.2f}</b></li>"

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
