import streamlit as st
import numpy as np

# Apply a custom theme for a professional look
st.set_page_config(
    page_title="Real Estate Financing Scenarios",
    page_icon="🏗️",
    layout="wide",  
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

# Requirements section
st.markdown("## State of the Project")
col1, col2, col3, col4 = st.columns(4)

with col1:
    land_acquired = st.radio("Land Acquired", ['Yes', 'No'], index=1)

with col2:
    if land_acquired == 'No':
        presales_options = [0, 25]
        presales = st.select_slider("Current Pre-sales (%)", options=presales_options, value=0)
    else:
        presales_options = [0, 25, 50, 75, 100]
        presales = st.select_slider("Current Pre-sales (%)", options=presales_options, value=0)

with col3:
    # If land has not been acquired
    if land_acquired == 'No':
        st.markdown("### Construction Progress (%)")
        st.markdown("**Land has not been acquired. Pre-sales are limited to a maximum of 25%, and construction progress is set to 0%.**")
        construction_progress = 0
    # If land has been acquired and there are no pre-sales
    elif presales == 0:
        st.markdown("### Construction Progress (%)")
        st.markdown("**Construction progress cannot be set when there are no pre-sales.**")
        construction_progress = 0
    # If land has been acquired and there are pre-sales
    else:
        construction_progress = st.select_slider("Construction Progress (%)", options=[i for i in range(0, presales + 1, 25)], value=min(25, presales))

with col4:
    location_options = ["Urban of a growing or coastal city", "Suburbs of a growing city", "Non-growing or coastal city"]
    development_location = st.selectbox("Development Location", location_options)

# Recommendations/Warnings/Considerations based on inputs
st.markdown("#### Recommendations/Warnings/Considerations")

# Define logic for displaying recommendations based on conditions
if development_location == "Non-growing or coastal city":
    location_warning = " Note: Being in a non-growing city may alter access to financing conditions."
else:
    location_warning = ""

if land_acquired == 'Yes':
    if presales > 70 and construction_progress > 50:
        st.success(f"At this stage, recapitalization is a strategic choice that enables you to refresh your project's equity—substituting your initial investment with external capital for the final stages. This approach allows you to reallocate your resources to new ventures sooner, rather than waiting until the project's end. Consider exploring options like crowdfunding or private equity funds to make this transition efficiently and kickstart your next investment..{location_warning}")
    elif 50 <= presales <= 60 and 50 <= construction_progress <= 60:
        st.info(f"In this construction phase, with pre-sales and progress both exceeding 50% but not yet reaching 60%, your project is in a strong position. If you've already secured financing through traditional banking or private debt but find yourself in need of further investment to complete construction and enhance sales, consider leveraging mezzanine debt. This option layers on top of your existing financing structure, offering the additional capital needed, albeit at a higher cost. Should you not yet have a banking loan, your project's current status also places you in an advantageous position to secure one..{location_warning}")
    elif presales >= 50 and construction_progress < 50:
        st.success(f"At this juncture, with pre-sales surpassing 50% yet construction in its nascent stages or not yet commenced, you're ideally positioned to meet the prerequisites for traditional banking. This scenario presents a prime opportunity to secure a construction loan from a bank, providing you with the necessary funding to advance from initial construction phases to completion. Leveraging this financial avenue could significantly benefit your project's progression and financial structure.{location_warning}")
    elif presales < 50 and construction_progress < 50:
        st.warning(f"With pre-sales not reaching 50% and construction either not started or in the early stages, your project currently falls short of the requirements for more cost-effective traditional bank financing. However, your development can still progress by accessing alternative financing options. Consider obtaining a construction loan through senior debt from a private debt fund or tapping into crowd-lending platforms. These avenues can provide the necessary capital to move your project forward, albeit at a higher cost than traditional loans.{location_warning}")
else:  # Land not acquired
    if presales < 50 and construction_progress < 50:
        st.warning(f"If you haven't acquired land or covered initial costs yet and pre-sales are low, a short-term bridge loan from private debt funds or crowd-lending platforms can be your lifeline. It’s designed to get your project to the point where it meets traditional banking requirements, allowing you to then secure a more affordable construction loan. This step is essential for moving your development forward efficiently.{location_warning}")

if land_acquired == 'No':
    development_phase_default = 'Pre-Construction'
elif land_acquired == 'Yes' and presales < 60:
    development_phase_default = 'Construction'
else:  # Land acquired and pre-sales >= 60
    development_phase_default = 'Post-Construction'


# Since we cannot dynamically set the value of a selectbox after it's been created,
# we use a workaround by creating a dictionary that maps the development phase to an index.
development_phase_options = list(development_phases.keys())
development_phase_index = development_phase_options.index(development_phase_default)

st.markdown("#### Scenario Builder")

# Now we use the index to set the default value dynamically.
development_phase = st.selectbox(
    'Select Development Phase',
    options=development_phase_options,
    index=development_phase_index  # Dynamically set default value
)

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
    st.markdown('### Adjust Interest Rates')

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
