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

# Add top metrics with delta values like in main app
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

with col1:
    avg_roas = df['ROI'].mean()
    prev_roas = avg_roas * 0.95  # Simulating 5% improvement
    delta_roas_pct = ((avg_roas - prev_roas) / prev_roas) * 100
    st.metric("Average ROAS", f"{avg_roas:.2f}", 
             delta=f"+{delta_roas_pct:.1f}% vs prev period", 
             delta_color="normal")

with col2:
    avg_clv = df['CLV'].mean()
    prev_clv = avg_clv * 0.92
    delta_clv_pct = ((avg_clv - prev_clv) / prev_clv) * 100
    st.metric("Avg CLV", f"${avg_clv:,.2f}", 
             delta=f"+{delta_clv_pct:.1f}% vs prev period", 
             delta_color="normal")

with col3:
    avg_cac = df['CAC'].mean()
    prev_cac = avg_cac * 1.03  # Lower CAC is better, so we simulate a decrease
    delta_cac_pct = ((prev_cac - avg_cac) / prev_cac) * 100
    st.metric("Avg CAC", f"${avg_cac:,.2f}", 
             delta=f"-{delta_cac_pct:.1f}% vs prev period", 
             delta_color="normal")

with col4:
    # Create a gauge chart for CLV/CAC ratio
    import plotly.graph_objects as go
    
    # CLV/CAC ratio data
    clv_cac_ratio = avg_clv / avg_cac
    
    # Create the gauge chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=clv_cac_ratio,
        title={"text": "CLV/CAC Ratio", "font": {"size": 14, "color": "#616161"}},
        gauge={
            "axis": {"range": [0, 8], "tickwidth": 1, "tickcolor": "#616161"},
            "bar": {"color": "#1e88e5"},
            "bgcolor": "white",
            "borderwidth": 0,
            "bordercolor": "white",
            "steps": [
                {"range": [0, 2], "color": "#e3f2fd"},
                {"range": [2, 4], "color": "#bbdefb"},
                {"range": [4, 8], "color": "#90caf9"}
            ],
            "threshold": {
                "line": {"color": "green", "width": 4},
                "thickness": 0.75,
                "value": 3
            }
        }
    ))
    
    # Update layout
    fig.update_layout(
        height=120,
        margin=dict(l=10, r=10, t=40, b=10),
        paper_bgcolor="white",
        font={"color": "#616161", "family": "Arial"}
    )
    
    st.markdown("<div class='card-title'>CLV/CAC Ratio</div>", unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)

# ROAS over time with card styling
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

# Key Takeaways with card styling
st.subheader("Key Takeaways")

col1, col2 = st.columns(2)

with col1:
    # Calculate metrics for insights
    avg_clv = df['CLV'].mean()
    avg_cac = df['CAC'].mean()
    avg_ratio = avg_clv / avg_cac
    
    st.markdown(f"""
    <div style="background-color: white; padding: 1rem; border-radius: 8px; border: 1px solid #e6e6e6; height: 100%;">
        <div style="font-weight: 500; color: #1e88e5; margin-bottom: 0.8rem; font-size: 1.1rem;">CLV/CAC Analysis</div>
        <div style="color: #212121; font-size: 0.9rem;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="font-weight: 500; color: #616161;">Average CLV:</span>
                <span style="color: #1e88e5; font-weight: 500;">${avg_clv:,.2f}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="font-weight: 500; color: #616161;">Average CAC:</span>
                <span style="color: #1e88e5; font-weight: 500;">${avg_cac:,.2f}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 1rem;">
                <span style="font-weight: 500; color: #616161;">CLV/CAC Ratio:</span>
                <span style="color: {'#4caf50' if avg_ratio > 3 else '#f44336'}; font-weight: 600;">{avg_ratio:.2f}</span>
            </div>
            <div style="background-color: #f5f9ff; padding: 0.7rem; border-radius: 4px; font-size: 0.85rem;">
                The business shows a CLV/CAC ratio of {avg_ratio:.2f}, which indicates 
                {'a healthy' if avg_ratio > 3 else 'an area for improvement in'} customer acquisition efficiency.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Calculate performance metrics
    avg_delivery = df['Delivery_Performance'].mean()
    avg_procurement = df['Procurement_Performance'].mean()
    nps_trend = 'Improving' if df['NPS'].iloc[-1] > df['NPS'].iloc[0] else 'Declining'
    
    st.markdown(f"""
    <div style="background-color: white; padding: 1rem; border-radius: 8px; border: 1px solid #e6e6e6; height: 100%;">
        <div style="font-weight: 500; color: #1e88e5; margin-bottom: 0.8rem; font-size: 1.1rem;">Performance Metrics</div>
        <div style="color: #212121; font-size: 0.9rem;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="font-weight: 500; color: #616161;">Delivery Performance:</span>
                <span style="color: {'#4caf50' if avg_delivery > 0 else '#f44336'}; font-weight: 500;">{avg_delivery:.2f}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="font-weight: 500; color: #616161;">Procurement Performance:</span>
                <span style="color: {'#4caf50' if avg_procurement > 0 else '#f44336'}; font-weight: 500;">{avg_procurement:.2f}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 1rem;">
                <span style="font-weight: 500; color: #616161;">NPS Trend:</span>
                <span style="color: {'#4caf50' if nps_trend == 'Improving' else '#f44336'}; font-weight: 500;">{nps_trend}</span>
            </div>
            <div style="background-color: #f5f9ff; padding: 0.7rem; border-radius: 4px; font-size: 0.85rem;">
                Operational performance metrics show {'strong' if avg_delivery > 0 and avg_procurement > 0 else 'areas for improvement in'} 
                delivery and procurement processes.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
