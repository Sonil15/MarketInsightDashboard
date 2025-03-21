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

# Chart 2: Monthly Revenue Comparison
st.subheader("Monthly Revenue Comparison")

# Load merged file data
df = pd.read_csv('attached_assets/merged_file.csv')

# Extract dates and totals
dates = pd.to_datetime(df['Unnamed: 0_baseline']).dt.strftime('%b %Y')
baseline = df['Total_baseline']
optimized = df['Total_optimized']

# Calculate percentage improvements
pct_improvement = ((optimized - baseline) / baseline * 100).round(1)

# Create figure
fig2 = go.Figure()

# Add baseline bars
fig2.add_trace(go.Bar(
    x=dates,
    y=baseline,
    name='Baseline',
    marker_color=BLUE_PALETTE[0],
    width=0.35
))

# Add optimized bars
fig2.add_trace(go.Bar(
    x=dates,
    y=optimized,
    name='Optimized',
    marker_color=BLUE_PALETTE[2],
    width=0.35,
    text=[f"{pct}%" for pct in pct_improvement],
    textposition='outside'
))

# Update layout
fig2.update_layout(
    title='Monthly Revenue Comparison',
    xaxis_title='Month',
    yaxis_title='Revenue',
    plot_bgcolor='white',
    barmode='group',
    bargap=0.15,
    bargroupgap=0.1,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
    yaxis=dict(gridcolor='lightgrey'),
    font=dict(color='#424242')
)

st.plotly_chart(fig2, use_container_width=True)
