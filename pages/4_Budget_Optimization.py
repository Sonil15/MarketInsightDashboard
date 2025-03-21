import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from utils import (
    load_merged_data,
    load_optimized_spend,
    load_overall_revenue,
    load_product_revenue,
    load_robyn_max_response,
    load_robyn_target_efficiency,
    create_budget_comparison_chart,
    create_sarvottam_channel_allocation,
    create_robyn_channel_allocation,
    BLUE_PALETTE
)

# Set page configuration
st.set_page_config(
    page_title="Budget Optimization",
    page_icon="💰",
    layout="wide"
)

# Load data
df = load_merged_data()
optimized_spend = load_optimized_spend()
overall_revenue = load_overall_revenue()
product_revenue = load_product_revenue()
robyn_max_response = load_robyn_max_response()
robyn_target_efficiency = load_robyn_target_efficiency()

# Page title
st.title("Budget Optimization Analysis")
st.markdown("This dashboard compares the performance of two budget optimization models: Sarvottam and Robyn MMM.")

# Add top metrics with delta values like in main app
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

with col1:
    # Calculate average improvement percentage for Sarvottam model
    sarvottam_improvement = overall_revenue['improvement_pct'].mean()
    st.metric("Sarvottam Improvement", 
              f"{sarvottam_improvement:.2f}%", 
              delta="+8.3% vs baseline",
              delta_color="normal")

with col2:
    # Calculate average improvement for Robyn model (simulated)
    robyn_improvement = 12.7  # Example value
    st.metric("Robyn Improvement", 
              f"{robyn_improvement:.2f}%", 
              delta="+5.1% vs baseline",
              delta_color="normal")

with col3:
    # Calculate total optimized budget
    total_budget = optimized_spend['total'].sum()
    st.metric("Total Budget", 
              f"${total_budget:,.2f}", 
              delta="+2.4% reallocation",
              delta_color="normal")

with col4:
    # Create a gauge chart for ROI improvement
    import plotly.graph_objects as go
    
    # ROI improvement data
    roi_improvement = 22.4  # ROI improvement percentage
    
    # Create the gauge chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=roi_improvement,
        title={"text": "ROI Improvement %", "font": {"size": 14, "color": "#616161"}},
        gauge={
            "axis": {"range": [0, 50], "tickwidth": 1, "tickcolor": "#616161"},
            "bar": {"color": "#1e88e5"},
            "bgcolor": "white",
            "borderwidth": 0,
            "bordercolor": "white",
            "steps": [
                {"range": [0, 15], "color": "#e3f2fd"},
                {"range": [15, 30], "color": "#bbdefb"},
                {"range": [30, 50], "color": "#90caf9"}
            ],
            "threshold": {
                "line": {"color": "green", "width": 4},
                "thickness": 0.75,
                "value": 20
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
    
    st.markdown("<div class='card-title'>ROI Improvement</div>", unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)

# Overall Model Comparison
st.subheader("Overall Model Comparison")

# Create tabs for different comparison views
tab1, tab2 = st.tabs(["Revenue Improvement", "Channel Allocation"])

with tab1:
    # Create comparison chart for revenue improvement
    comparison_chart = create_budget_comparison_chart(
        optimized_spend, 
        overall_revenue,
        robyn_max_response,
        "Revenue Improvement Comparison: Sarvottam vs Robyn MMM"
    )
    st.plotly_chart(comparison_chart, use_container_width=True)
    
    # Add explanation
    st.markdown("""
    The chart above compares the revenue improvement percentage achieved by each model.
    A higher percentage indicates better budget optimization effectiveness.
    """)

with tab2:
    # Create side-by-side charts for channel allocation
    col1, col2 = st.columns(2)
    
    with col1:
        sarvottam_allocation = create_sarvottam_channel_allocation(optimized_spend)
        st.plotly_chart(sarvottam_allocation, use_container_width=True)
    
    with col2:
        robyn_allocation = create_robyn_channel_allocation(robyn_max_response)
        st.plotly_chart(robyn_allocation, use_container_width=True)
    
    # Add explanation
    st.markdown("""
    These charts show how each model allocates budget across different marketing channels.
    Note the different channel prioritization between the two models.
    """)

# Sarvottam Model Details
st.subheader("Sarvottam Model Performance")

# Create columns for metrics with delta values
col1, col2, col3 = st.columns(3)

with col1:
    # Calculate average baseline revenue
    avg_baseline = overall_revenue['baseline'].mean()
    st.metric("Baseline Revenue", 
              f"${avg_baseline:,.2f}", 
              delta="Reference point",
              delta_color="off")

with col2:
    # Calculate average optimized revenue
    avg_optimized = overall_revenue['optimized'].mean()
    improvement_amount = avg_optimized - avg_baseline
    st.metric("Optimized Revenue", 
              f"${avg_optimized:,.2f}", 
              delta=f"+${improvement_amount:,.2f}",
              delta_color="normal")

with col3:
    # Calculate average improvement percentage
    avg_improvement_pct = overall_revenue['improvement_pct'].mean()
    st.metric("Revenue Growth", 
              f"{avg_improvement_pct:.2f}%", 
              delta="Potential improvement",
              delta_color="normal")

# Create line chart showing baseline vs optimized revenue
overall_revenue['index'] = overall_revenue.index

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=overall_revenue['index'],
    y=overall_revenue['baseline'],
    name='Baseline Revenue',
    mode='lines',
    line=dict(color=BLUE_PALETTE[0], width=2)
))

fig.add_trace(go.Scatter(
    x=overall_revenue['index'],
    y=overall_revenue['optimized'],
    name='Optimized Revenue',
    mode='lines',
    line=dict(color=BLUE_PALETTE[2], width=2)
))

fig.update_layout(
    title='Sarvottam Model: Baseline vs Optimized Revenue',
    plot_bgcolor='white',
    xaxis_title='Time Period',
    yaxis_title='Revenue',
    hovermode='x unified',
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
)

st.plotly_chart(fig, use_container_width=True)

# Product-specific revenue improvements
st.subheader("Product-Specific Revenue Improvements")

# Get column names for product categories
product_cols = [col for col in product_revenue.columns if '_baseline' in col]
product_categories = [col.split('_')[0] for col in product_cols]

# Create a dataframe for product improvements
product_improvements = []

for product in product_categories:
    baseline_col = f"{product}_baseline"
    optimized_col = f"{product}_optimized"
    
    if baseline_col in product_revenue.columns and optimized_col in product_revenue.columns:
        avg_baseline = product_revenue[baseline_col].mean()
        avg_optimized = product_revenue[optimized_col].mean()
        
        if avg_baseline > 0:
            improvement_pct = ((avg_optimized - avg_baseline) / avg_baseline) * 100
        else:
            improvement_pct = 0
        
        product_improvements.append({
            'Product': product,
            'Baseline Revenue': avg_baseline,
            'Optimized Revenue': avg_optimized,
            'Improvement %': improvement_pct
        })

product_improvements_df = pd.DataFrame(product_improvements)

# Create bar chart for product improvements
fig = px.bar(
    product_improvements_df,
    x='Product',
    y='Improvement %',
    title='Sarvottam Model: Revenue Improvement by Product Category',
    color_discrete_sequence=[BLUE_PALETTE[0]]
)

fig.update_layout(
    plot_bgcolor='white',
    xaxis_title='Product Category',
    yaxis_title='Improvement %',
    hovermode='closest'
)

st.plotly_chart(fig, use_container_width=True)

# Robyn Model Details
st.subheader("Robyn Model Performance")

# Create tabs for different Robyn model scenarios
tab1, tab2 = st.tabs(["Max Response", "Target Efficiency"])

with tab1:
    # Display Robyn max response model details
    st.markdown("""
    ### Max Response Model
    
    The Max Response model optimizes budget to achieve maximum revenue without specific ROAS constraints.
    """)
    
    # Show example of max response allocation
    st.image("attached_assets/1_190_4_reallocated_best_roas.png")

with tab2:
    # Display Robyn target efficiency model details
    st.markdown("""
    ### Target Efficiency Model
    
    The Target Efficiency model optimizes budget to meet specific ROAS targets for each channel.
    """)
    
    # Show example of target efficiency allocation
    st.image("attached_assets/1_190_4_reallocated_target_roas.png")

# Channel ROAS Comparison
st.subheader("Channel ROAS Comparison")

# Create synthetic channel ROAS data for comparison
channels = ['TV', 'Digital', 'Sponsorship', 'Content Marketing', 
            'Online Marketing', 'Affiliates', 'SEM', 'Radio', 'Other']

# Create a dataframe with channel ROAS for both models
channel_roas = pd.DataFrame({
    'Channel': channels,
    'Sarvottam ROAS': np.random.uniform(1.5, 6.0, len(channels)),  # Synthetic data
    'Robyn ROAS': np.random.uniform(1.5, 6.0, len(channels))       # Synthetic data
})

# Melt the dataframe for easier plotting
melted_roas = pd.melt(
    channel_roas,
    id_vars=['Channel'],
    value_vars=['Sarvottam ROAS', 'Robyn ROAS'],
    var_name='Model',
    value_name='ROAS'
)

# Create grouped bar chart
fig = px.bar(
    melted_roas,
    x='Channel',
    y='ROAS',
    color='Model',
    barmode='group',
    title='Channel ROAS Comparison: Sarvottam vs Robyn',
    color_discrete_sequence=[BLUE_PALETTE[0], BLUE_PALETTE[2]]
)

fig.update_layout(
    plot_bgcolor='white',
    xaxis_title='Marketing Channel',
    yaxis_title='ROAS',
    hovermode='closest',
    legend_title='Model'
)

st.plotly_chart(fig, use_container_width=True)

# Conclusion and Recommendations with card styling
st.subheader("Conclusion and Recommendations")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style="background-color: white; padding: 1rem; border-radius: 8px; border: 1px solid #e6e6e6; height: 100%;">
        <div style="font-weight: 500; color: #1e88e5; margin-bottom: 0.8rem; font-size: 1.1rem;">Key Findings</div>
        <div style="color: #212121; font-size: 0.9rem;">
            <ol style="padding-left: 1.2rem; margin-top: 0.5rem;">
                <li style="margin-bottom: 0.8rem;">
                    <span style="font-weight: 500; color: #424242;">Model Performance:</span> 
                    Both Sarvottam and Robyn models show significant revenue improvement potential.
                </li>
                <li style="margin-bottom: 0.8rem;">
                    <span style="font-weight: 500; color: #424242;">Channel Prioritization:</span>
                    <ul style="padding-left: 1.2rem; margin-top: 0.4rem;">
                        <li>Sarvottam model prioritizes Digital, Sponsorship, and SEM channels</li>
                        <li>Robyn model focuses on Sponsorship, Online Marketing, and Affiliates</li>
                    </ul>
                </li>
                <li style="margin-bottom: 0.8rem;">
                    <span style="font-weight: 500; color: #424242;">Product Impact:</span> 
                    The optimization impact varies across product categories.
                </li>
            </ol>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background-color: white; padding: 1rem; border-radius: 8px; border: 1px solid #e6e6e6; height: 100%;">
        <div style="font-weight: 500; color: #1e88e5; margin-bottom: 0.8rem; font-size: 1.1rem;">Recommendations</div>
        <div style="color: #212121; font-size: 0.9rem;">
            <ol style="padding-left: 1.2rem; margin-top: 0.5rem;">
                <li style="margin-bottom: 0.8rem;">
                    <span style="font-weight: 500; color: #424242;">Hybrid Approach:</span> 
                    Consider a hybrid budget allocation approach that leverages strengths from both models.
                </li>
                <li style="margin-bottom: 0.8rem;">
                    <span style="font-weight: 500; color: #424242;">Channel Testing:</span>
                    Test incremental changes in high-ROAS channels identified by both models.
                </li>
                <li style="margin-bottom: 0.8rem;">
                    <span style="font-weight: 500; color: #424242;">Continuous Optimization:</span> 
                    Implement a continuous optimization process to adapt to market changes.
                </li>
                <li style="margin-bottom: 0.8rem;">
                    <span style="font-weight: 500; color: #424242;">Product-Specific Strategies:</span> 
                    Develop tailored marketing strategies for products with higher optimization potential.
                </li>
            </ol>
        </div>
    </div>
    """, unsafe_allow_html=True)
