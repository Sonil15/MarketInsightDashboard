import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils import (
    load_merged_data,
    create_kpi_time_series,
    create_clv_cac_comparison,
    create_performance_metrics_chart,
    create_nps_stock_chart,
    BLUE_PALETTE
)

# Set page configuration
st.set_page_config(
    page_title="KPI Analysis",
    page_icon="📊",
    layout="wide"
)

# Load data
df = load_merged_data()

# Page title
st.title("KPI/KRA/KRI Analysis")
st.markdown("This dashboard analyzes key performance indicators over time.")

# ROAS over time
st.subheader("ROAS (Return on Ad Spend) Over Time")
roas_chart = create_kpi_time_series(df, 'ROI', 'Monthly ROAS Trend', 'ROAS')
st.plotly_chart(roas_chart, use_container_width=True)

# CLV by month
st.subheader("Customer Lifetime Value (CLV) by Month")
clv_chart = create_kpi_time_series(df, 'CLV', 'Monthly CLV Trend', 'CLV')
st.plotly_chart(clv_chart, use_container_width=True)

# Normalized Procurement Performance
st.subheader("Procurement Performance vs Total GMV")

# Calculate normalized procurement performance
df['Procurement_Performance_Normalized'] = df['Procurement_Performance'] / df['Procurement_Performance'].max()
df['GMV_Normalized'] = df['Total_GMV'] / df['Total_GMV'].max()

# Create the dual line chart
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df['YearMonth'],
    y=df['Procurement_Performance_Normalized'],
    name='Normalized Procurement Performance',
    mode='lines+markers',
    line=dict(color=BLUE_PALETTE[0], width=2),
    marker=dict(color=BLUE_PALETTE[0], size=8)
))

fig.add_trace(go.Scatter(
    x=df['YearMonth'],
    y=df['GMV_Normalized'],
    name='Normalized GMV',
    mode='lines+markers',
    line=dict(color=BLUE_PALETTE[2], width=2),
    marker=dict(color=BLUE_PALETTE[2], size=8)
))

fig.update_layout(
    title='Normalized Procurement Performance vs GMV',
    plot_bgcolor='white',
    xaxis_title='Month',
    yaxis_title='Normalized Value (0-1)',
    hovermode='x unified',
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
)

st.plotly_chart(fig, use_container_width=True)

# CAC by month
st.subheader("Customer Acquisition Cost (CAC) by Month")
cac_chart = create_kpi_time_series(df, 'CAC', 'Monthly CAC Trend', 'CAC')
st.plotly_chart(cac_chart, use_container_width=True)

# CLV vs CAC Comparison
st.subheader("CLV vs CAC Comparison")
clv_cac_chart = create_clv_cac_comparison(df)
st.plotly_chart(clv_cac_chart, use_container_width=True)

# Explanation
st.markdown("""
The chart above compares Customer Lifetime Value (CLV) with Customer Acquisition Cost (CAC) over time.
- **CLV**: The total value a customer brings over their lifetime
- **CAC**: The cost to acquire a new customer
- **CLV/CAC Ratio**: A healthy business typically has a ratio > 3

A higher CLV/CAC ratio indicates more efficient customer acquisition and better long-term profitability.
""")

# Delivery and Procurement Performance
st.subheader("Delivery and Procurement Performance")
performance_chart = create_performance_metrics_chart(df)
st.plotly_chart(performance_chart, use_container_width=True)

# NPS and Stock Index Over Time
st.subheader("NPS and Stock Index Over Time")
nps_stock_chart = create_nps_stock_chart(df)
st.plotly_chart(nps_stock_chart, use_container_width=True)

# ROI Distribution
st.subheader("ROI Distribution")

fig = px.histogram(
    df, 
    x='ROI',
    nbins=10,
    title='ROI Distribution',
    color_discrete_sequence=[BLUE_PALETTE[0]]
)

fig.update_layout(
    plot_bgcolor='white',
    xaxis_title='ROI',
    yaxis_title='Frequency',
    hovermode='closest'
)

st.plotly_chart(fig, use_container_width=True)

# Key Takeaways
st.subheader("Key Takeaways")

col1, col2 = st.columns(2)

with col1:
    # Calculate metrics for insights
    avg_clv = df['CLV'].mean()
    avg_cac = df['CAC'].mean()
    avg_ratio = avg_clv / avg_cac
    
    st.markdown(f"""
    ### CLV/CAC Analysis
    
    - **Average CLV**: ${avg_clv:,.2f}
    - **Average CAC**: ${avg_cac:,.2f}
    - **Average CLV/CAC Ratio**: {avg_ratio:.2f}
    
    The business shows a CLV/CAC ratio of {avg_ratio:.2f}, which indicates 
    {'a healthy' if avg_ratio > 3 else 'an area for improvement in'} customer acquisition efficiency.
    """)

with col2:
    # Calculate performance metrics
    avg_delivery = df['Delivery_Performance'].mean()
    avg_procurement = df['Procurement_Performance'].mean()
    
    st.markdown(f"""
    ### Performance Metrics
    
    - **Average Delivery Performance**: {avg_delivery:.2f}
    - **Average Procurement Performance**: {avg_procurement:.2f}
    - **NPS Trend**: {'Improving' if df['NPS'].iloc[-1] > df['NPS'].iloc[0] else 'Declining'}
    
    Operational performance metrics show {'strong' if avg_delivery > 0 and avg_procurement > 0 else 'areas for improvement in'} 
    delivery and procurement processes.
    """)
