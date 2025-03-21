import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Blue color palette
BLUE_PALETTE = ['#bbdefb', '#64b5f6', '#2196f3', '#1976d2', '#0d47a1']

# Set page configuration
st.set_page_config(
    page_title="Budget Optimization",
    page_icon="💰",
    layout="wide"
)

# Page title
st.title("Budget Optimization Analysis")
st.markdown("This dashboard shows two charts for budget optimization analysis.")

# Chart 1: Robyn Model Channel Budget Comparison
st.subheader("Robyn Model Channel Budget Comparison")

# Load and prepare Robyn budget data
robyn_budget_data = pd.read_csv('attached_assets/Robyn_marketing_budget_allocation.csv')

# Create clustered bar chart for Robyn channels
fig1 = go.Figure()

# Add bars for original budget
fig1.add_trace(go.Bar(
    x=robyn_budget_data['Channel'],
    y=robyn_budget_data['Original_Budget'],
    name='Original Budget',
    marker_color=BLUE_PALETTE[0],
    text=robyn_budget_data['Original_Budget'],
    textposition='outside'
))

# Add bars for new budget
fig1.add_trace(go.Bar(
    x=robyn_budget_data['Channel'],
    y=robyn_budget_data['New_Budget'],
    name='New Budget',
    marker_color=BLUE_PALETTE[2],
    text=robyn_budget_data['New_Budget'],
    textposition='outside'
))

# Update layout
fig1.update_layout(
    title='Robyn Model: Channel Budget Comparison',
    xaxis_title='Marketing Channel',
    yaxis_title='Budget (Million $)',
    barmode='group',
    plot_bgcolor='white',
    font=dict(color='#424242'),
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
    margin=dict(l=10, r=10, t=30, b=10),
    hovermode='x unified',
    bargap=0.2,
    bargroupgap=0.1
)

st.plotly_chart(fig1, use_container_width=True)

# Chart 2: Optym Model Channel Budget Allocation
st.subheader("Optym Model Channel Budget Allocation")

# Load merged file data for Optym channel allocation
optym_data = pd.read_csv('attached_assets/merged_file.csv')

# Select only the baseline columns needed
baseline_columns = [col for col in optym_data.columns if '_baseline' in col and 'Unnamed' not in col and 'Total' not in col]

# Calculate the average for each channel across all time periods
channel_averages = {}
for col in baseline_columns:
    channel_name = col.replace('_baseline', '')
    channel_averages[channel_name] = optym_data[col].mean()

# Create dataframe for the bar chart
channels = list(channel_averages.keys())
values = list(channel_averages.values())

optym_df = pd.DataFrame({'Channel': channels, 'Budget': values})

# Create clustered bar chart for Optym channels
fig2 = go.Figure()

# Add bars for each channel
fig2.add_trace(go.Bar(
    x=optym_df['Channel'],
    y=optym_df['Budget'],
    marker_color=BLUE_PALETTE[1],
    text=optym_df['Budget'].round(2),
    textposition='outside'
))

# Update layout
fig2.update_layout(
    title='Optym Model: Average Channel Budget Allocation',
    xaxis_title='Marketing Channel',
    yaxis_title='Budget',
    plot_bgcolor='white',
    font=dict(color='#424242'),
    margin=dict(l=10, r=10, t=30, b=10),
    hovermode='closest'
)

st.plotly_chart(fig2, use_container_width=True)
