import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Smartphone Sales Forecast Dashboard")

st.title("Q1 2025 Smartphone Sales Forecast Dashboard")

# Sidebar inputs
st.sidebar.header("Input Parameters")
target_market_share = st.sidebar.slider("Target Market Share (%)", 0.0, 100.0, 10.0)
total_market_size = st.sidebar.number_input("Total Market Size", value=1000000)
weeks_of_stock = st.sidebar.slider("Weeks of Stock", 1, 12, 4)
price = st.sidebar.number_input("Price per Unit", value=500)
front_margin = st.sidebar.slider("Front Margin (%)", 0.0, 50.0, 20.0)
back_margin = st.sidebar.slider("Back Margin (%)", 0.0, 50.0, 10.0)
production_capacity = st.sidebar.number_input("Weekly Production Capacity", value=10000)

# Calculations
sell_out_forecast = int(total_market_size * (target_market_share / 100))
sell_in_forecast = sell_out_forecast + (sell_out_forecast * (weeks_of_stock / 13))  # Assuming 13 weeks in Q1
max_production = production_capacity * 13
sell_in_forecast = min(sell_in_forecast, max_production)
gross_sales = sell_in_forecast * price
net_sales = gross_sales * (1 - (front_margin / 100) - (back_margin / 100))

# Display results
st.header("Forecast Results")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Sell-out Forecast")
    st.metric("Units", f"{sell_out_forecast:,}")
with col2:
    st.subheader("Sell-in Forecast")
    st.metric("Units", f"{int(sell_in_forecast):,}")

st.subheader("Financial Projections")
col3, col4 = st.columns(2)
with col3:
    st.metric("Gross Sales", f"${gross_sales:,.2f}")
with col4:
    st.metric("Net Sales", f"${net_sales:,.2f}")

# Weekly breakdown
st.header("Weekly Breakdown")
weeks = range(1, 14)
weekly_sell_out = [sell_out_forecast // 13] * 13
weekly_sell_in = [min(production_capacity, sell_in_forecast // 13)] * 13

df = pd.DataFrame({
    'Week': weeks,
    'Sell-out': weekly_sell_out,
    'Sell-in': weekly_sell_in
})

st.dataframe(df)

# Plot
st.line_chart(df.set_index('Week'))
