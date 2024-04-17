import streamlit as st
import numpy as np

# Apply a custom theme for a professional look
st.set_page_config(
    page_title="Real Estate Financing Scenarios",
    page_icon="🏗️",
    initial_sidebar_state="expanded",
)

# Define financing methods with cost range
financing_methods = {
    'Bank Loan': {'cost_range': (0.03, 0.06)},
    'Senior Debt': {'cost_range': (0.15, 0.20)},
    'Mezzanine Debt': {'cost_range': (0.20, 0.25)},
    'ICO': {'cost_range': (0.01, 0.03)},
    'Developers Own Capital': {'cost_range': (0.0, 0.0)},
    'CrowdLending': {'cost_range': (0.12, 0.15)},
    'Private Equity': {'cost_range': (0.20, 0.25)},
    'Crowdfunding Recap': {'cost_range': (0.15, 0.20)}
}

# Define real estate development types
development_types = {
    'Build to Sell (BTS)': {'Bank Loan': 0.5, 'Senior Debt': 0.6, 'Mezzanine Debt': 0.3, 'CrowdLending': 0.6,'Developers Own Capital': 1.0, 'ICO': 0,  'Private Equity': 0.7, 'Crowdfunding Recap': 0.7},
    'Build to Rent (BTR)': {'Bank Loan': 0.6, 'Senior Debt': 0.7, 'Mezzanine Debt': 0.4, 'CrowdLending': 0.7, 'Developers Own Capital': 1.0,'ICO': 0,  'Private Equity': 0.7, 'Crowdfunding Recap': 0.7},
    'Flex Living': {'Bank Loan': 0.40, 'Senior Debt': 0.6, 'Mezzanine Debt': 0.2, 'CrowdLending': 0.6, 'Developers Own Capital': 1.0, 'ICO': 0, 'Private Equity': 0.7, 'Crowdfunding Recap': 0.7},
    'Data centers': {'Bank Loan': 0.3, 'Senior Debt': 0.6, 'Mezzanine Debt': 0.3, 'CrowdLending': 0.6, 'Developers Own Capital': 1.0, 'ICO': 0, 'Private Equity': 0.7, 'Crowdfunding Recap': 0.7},
    'Hotels': {'Bank Loan': 0.5, 'Senior Debt': 0.6, 'Mezzanine Debt': 0.3, 'CrowdLending': 0.6, 'Developers Own Capital': 1.0,'ICO': 0,  'Private Equity': 0.7, 'Crowdfunding Recap': 0.7},
    'Logistics': {'Bank Loan': 0.5, 'Senior Debt': 0.6, 'Mezzanine Debt': 0.3, 'CrowdLending': 0.6, 'Developers Own Capital': 1.0,'ICO': 0,  'Private Equity': 0.7, 'Crowdfunding Recap': 0.7},
    'Subsidized': {'Bank Loan': 0.5, 'Senior Debt': 0.6, 'Mezzanine Debt': 0.3, 'CrowdLending': 0.6, 'Developers Own Capital': 1.0,'ICO': 0.3,  'Private Equity': 0.7, 'Crowdfunding Recap': 0.7}
}

# Define development phases
development_phases = {
    'Pre-Construction': {'Senior Debt': 0.7, 'CrowdLending': 0.7, 'Developers Own Capital': 1.0},
    'Construction': {'Bank Loan': 0.6, 'Senior Debt': 0.7, 'Mezzanine Debt': 0.4,'Developers Own Capital': 1.0, 'ICO': 0,  'CrowdLending': 0.7},
    'Post-Construction': {'Private Equity': 0.7, 'Crowdfunding Recap': 0.7}
}

# Function to calculate WACC
def calculate_wacc(equities, interests):
    return np.dot(equities, interests)

# Function to calculate the Equity Multiplier
def calculate_multiplier(own_equity_pct):
    return 1 / own_equity_pct if own_equity_pct > 0 else float('inf')

st.title('Real Estate Development Financing Scenarios')

# User selects development phase
development_phase = st.selectbox('Select Development Phase', list(development_phases.keys()))

# User selects development type
development_type = st.selectbox('Select Development Type', list(development_types.keys()))

# Define maximum equity or leverage based on development type and phase
if development_phase == 'Pre-Construction':
    max_values = development_phases['Pre-Construction']
elif development_phase == 'Construction':
    max_values = development_types[development_type]
else:  # Post-Construction
    max_values = development_phases['Post-Construction']

# Default values for total investment and total revenue
total_investment_default = 500000
total_revenue_default = 1000000

# User inputs total investment
total_investment = st.number_input('Total Investment', min_value=100000, max_value=10000000, value=total_investment_default, step=100000)

# User inputs total revenue
total_revenue = st.number_input('Total Revenue', min_value=0, max_value=1000000000, value=total_revenue_default, step=100000)

equities = []
costs = []
interests = []
method_interests = []
total_leverage_pct = 0


# Display financing method sliders with checks for valid max value
for method, max_value in max_values.items():
    if method == 'Developers Own Capital':
        continue
    if method in financing_methods and max_value > 0 and (development_phase != 'Construction' or method not in ['Private Equity', 'Crowdfunding Recap']):
        leverage_pct = st.slider(f'{method} Leverage %', min_value=0.0, max_value=float(max_value), value=0.0, step=0.05, format='%f')
        equities.append(leverage_pct)
        # Calculate cost of financing
        loan_amount = leverage_pct * total_investment
        interest_rate_range = financing_methods[method]['cost_range']
        avg_interest_rate = np.mean(interest_rate_range)
        # Calculate interest payments
        interest_payments = avg_interest_rate * loan_amount
        # Total cost including principal and interest payments
        total_cost = loan_amount + interest_payments
        costs.append(total_cost)
        interests.append(avg_interest_rate)

# Calculate developers own equity or capital based on selected equities
developer_own_equity_pct = 1 - sum(equities)
equities.append(developer_own_equity_pct)
costs.append(0.0)  # No cost for developers own equity or capital
interests.append(0.0)

# Calculate and display WACC and Equity Multiplier if within bounds
wacc = calculate_wacc(equities, interests)
multiplier = calculate_multiplier(developer_own_equity_pct)

# Calculate revenue for each financing party
revenues = [equity * total_revenue for equity in equities[:-1]]

# Calculate total financing cost including principal amounts of selected financing methods and developer's own investment
total_financing_cost = sum(costs) + developer_own_equity_pct * total_investment

# Add principal amounts of selected financing methods
for method, pct in zip(max_values.keys(), equities):
    if pct > 0 and method != 'Developers Own Capital':
        total_financing_cost += pct * total_investment


# Calculate profit for each financing method
profits = [revenue - cost for revenue, cost in zip(revenues, costs)]

# Developer's profit from their own investment
developer_profit = total_revenue - total_financing_cost

# Display results
if sum(equities[:-1]) > 1:
    st.error('The total equity cannot exceed 100%. Please adjust the financing method percentages.')
else:
   # After selecting leverage percentages and before calculating WACC and other metrics
    st.markdown('## Adjust Interest Rates')

    # Hold the adjusted interest rates
    adjusted_interests = []

    # Keep track of which methods have been selected with non-zero leverage
    selected_methods = [method for method, equity in zip(max_values.keys(), equities) if equity > 0]

    for method in selected_methods:
        if method != 'Developers Own Capital':  # Exclude developers own capital from interest adjustments
            min_rate, max_rate = financing_methods[method]['cost_range']
            # Use average rate as the default value for the slider
            avg_rate = np.mean([min_rate, max_rate])
            # Create a slider for adjusting the interest rate
            adjusted_rate = st.slider(f"{method} Interest Rate", min_value=min_rate, max_value=max_rate, value=avg_rate, step=0.01, format='%f')
            # Append the adjusted rate to the list
            adjusted_interests.append(adjusted_rate)
        else:
            # Append a 0.0 interest rate for developers own capital
            adjusted_interests.append(0.0)

    # Ensure the list of interests is the same length as the list of equities
    # Fill in any missing entries with 0.0, assuming no interest for unselected methods
    while len(adjusted_interests) < len(equities) - 1:  # Exclude the last entry for developers own capital
        adjusted_interests.append(0.0)

    # Add 0.0 for Developers Own Capital as before
    adjusted_interests.append(0.0)

    # Update the interests list with the adjusted values
    interests = adjusted_interests

    # After collecting adjusted interest rates from sliders
    # Update cost calculations to reflect adjusted interest rates
    adjusted_costs = []
    for i, pct in enumerate(equities[:-1]):  # Exclude the Developers Own Capital for cost calculation
        method = list(max_values.keys())[i]
        if method in financing_methods:  # Check if the method is one of the financing methods
            loan_amount = pct * total_investment  # Principal for the method
            adjusted_rate = adjusted_interests[i]  # Get the adjusted rate for the method
            interest_payments = adjusted_rate * loan_amount  # Calculate interest based on the adjusted rate
            total_cost = loan_amount + interest_payments  # Total cost including interest
            adjusted_costs.append(total_cost)
        else:
            adjusted_costs.append(0)  # Add 0 for methods not in financing_methods or Developers Own Capital

    # Note: Developers Own Capital does not incur costs, so it's excluded from the above loop

    # Update the WACC calculation to use the adjusted interest rates
    wacc = calculate_wacc(equities, adjusted_interests)

    # Recalculate the profits based on adjusted costs
    # This includes recalculating developer's profit
    total_financing_cost = sum(adjusted_costs) + developer_own_equity_pct * total_investment  # Include Developers Own Capital
    developer_profit = total_revenue - total_financing_cost  # Recalculate developer's profit

    st.markdown('# Summary')

    col1, col2 = st.columns(2)

    with col1:
        st.metric(label="Weighted Average Cost of Capital (WACC)", value=f"{wacc:.2%}")
        st.metric(label="Developper's Multiplier", value=f"{(developer_profit + (developer_own_equity_pct * total_investment))/ (developer_own_equity_pct * total_investment):.2f}")

    with col2:
        st.metric(label="Total Financing Cost", value=f"${total_financing_cost:,.2f}")
        st.metric(label="Developer's Profit from Own Investment", value=f"${developer_profit:,.2f}")

    st.markdown('---')
    st.subheader('Financing Method Details')

    for method, pct in zip(max_values.keys(), equities):
        if pct > 0:
            if method == 'Developers Own Capital':
                revenue = pct * total_revenue
                profit = revenue - (developer_own_equity_pct * total_investment) 
                col1, col2, col3 = st.columns([3, 2, 2])
                with col1:
                    st.caption(f'{method} Leverage')
                    st.progress(pct)
                with col2:
                    st.caption('Revenue ($)')
                    st.write(f"${revenue:,.2f}")
                with col3:
                    st.caption('Profit ($)')
                    st.write(f"${profit:,.2f}")
            else:
                # Calculate Principal and Interest
                loan_amount = pct * total_investment  # Principal
                avg_interest_rate = np.mean(financing_methods[method]['cost_range'])
                interest_payments = avg_interest_rate * loan_amount  # Interest
                
                # Calculate total cost and profit for the method
                total_cost = loan_amount + interest_payments  # Principal + Interest
                revenue = pct * total_revenue
                profit = revenue - total_cost
                
                # Display financing method, revenue, profit, and cost details
                col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
                with col1:
                    st.caption(f'{method} Leverage')
                    st.progress(pct)
                with col2:
                    st.caption('Revenue ($)')
                    st.write(f"${revenue:,.2f}")
                with col3:
                    st.caption('Cost (Principal + Int) ($)')
                    st.write(f"${total_cost:,.2f}")
                with col4:
                    st.caption('Profit ($)')
                    st.write(f"${profit:,.2f}")


    st.markdown('---')
    st.subheader("Developer's Investment Details")
    st.metric(label="Own Investment", value=f"${developer_own_equity_pct * total_investment:,.2f}")
    st.metric(label="Developer Multiplier", value=f"{(developer_profit + (developer_own_equity_pct * total_investment))/ (developer_own_equity_pct * total_investment):.2f}")