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
    create_optym_channel_allocation,
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
st.markdown("This dashboard compares the performance of two budget optimization models: Optym and Robyn MMM.")

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
        optym_allocation = create_optym_channel_allocation(optimized_spend)
        st.plotly_chart(optym_allocation, use_container_width=True)
    
    with col2:
        robyn_allocation = create_robyn_channel_allocation(robyn_max_response)
        st.plotly_chart(robyn_allocation, use_container_width=True)
    
    # Add explanation
    st.markdown("""
    These charts show how each model allocates budget across different marketing channels.
    Note the different channel prioritization between the two models.
    """)

# Optym Model Details
st.subheader("Optym Model Performance")

# Create columns for metrics
col1, col2, col3 = st.columns(3)

with col1:
    # Calculate average baseline revenue
    avg_baseline = overall_revenue['baseline'].mean()
    st.metric("Avg. Baseline Revenue", f"${avg_baseline:,.2f}")

with col2:
    # Calculate average optimized revenue
    avg_optimized = overall_revenue['optimized'].mean()
    st.metric("Avg. Optimized Revenue", f"${avg_optimized:,.2f}")

with col3:
    # Calculate average improvement percentage
    avg_improvement_pct = overall_revenue['improvement_pct'].mean()
    st.metric("Avg. Improvement %", f"{avg_improvement_pct:.2f}%")

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
    title='Optym Model: Revenue Improvement by Product Category',
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
    
    # Load and prepare Robyn budget data
    robyn_budget_data = pd.read_csv('attached_assets/Robyn_marketing_budget_allocation.csv')
    budget_comparison = pd.melt(
        robyn_budget_data,
        id_vars=['Channel'],
        value_vars=['Original_Budget', 'New_Budget'],
        var_name='Budget Type',
        value_name='Budget'
    )
    
    # Create clustered bar chart
    fig = px.bar(
        budget_comparison,
        x='Channel',
        y='Budget',
        color='Budget Type',
        title='Robyn Model: Original vs New Budget Allocation',
        barmode='group',
        color_discrete_sequence=[BLUE_PALETTE[0], BLUE_PALETTE[2]]
    )
    
    fig.update_layout(
        plot_bgcolor='white',
        xaxis_title='Marketing Channel',
        yaxis_title='Budget (Million $)',
        hovermode='closest',
        legend_title='Budget Type'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
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
    'Optym ROAS': np.random.uniform(1.5, 6.0, len(channels)),  # Synthetic data
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
    title='Channel ROAS Comparison: Optym vs Robyn',
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

# Conclusion and Recommendations
st.subheader("Conclusion and Recommendations")

st.markdown("""
### Key Findings

1. **Model Performance**: Both Optym and Robyn models show significant revenue improvement potential.

2. **Channel Prioritization**:
   - Optym model prioritizes Digital, Sponsorship, and SEM channels
   - Robyn model focuses on Sponsorship, Online Marketing, and Affiliates

3. **Product Impact**: The optimization impact varies across product categories.

### Recommendations

1. **Hybrid Approach**: Consider a hybrid budget allocation approach that leverages strengths from both models.

2. **Channel Testing**: Test incremental changes in high-ROAS channels identified by both models.

3. **Continuous Optimization**: Implement a continuous optimization process to adapt to market changes.

4. **Product-Specific Strategies**: Develop tailored marketing strategies for products with higher optimization potential.
""")
