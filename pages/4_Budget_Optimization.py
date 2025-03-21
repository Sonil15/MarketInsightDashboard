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
    title='Optym Model: Baseline vs Optimized Revenue',
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
    
    # Create clustered bar chart for Robyn channels (as requested)
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
    
    # Load merged file data for Optym channel allocation (the second requested chart)
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
    
    # Show example of max response allocation
    st.image("attached_assets/1_190_4_reallocated_best_roas.png")

with tab2:
    # Display Robyn target efficiency model details
    st.markdown("""
    ### Target Efficiency Model
    
    The Target Efficiency model optimizes budget to meet specific ROAS targets for each channel.
    """)
    
    # Load merged file data for Optym channel comparison (baseline vs optimized)
    optym_data = pd.read_csv('attached_assets/merged_file.csv')
    
    # Create lists for channel names, baseline values, and optimized values
    channels = []
    baseline_values = []
    optimized_values = []
    
    # Process the data to extract channel comparison values
    for i, col in enumerate(optym_data.columns):
        if '_baseline' in col and 'Unnamed' not in col and 'Total' not in col:
            channel_name = col.replace('_baseline', '')
            channels.append(channel_name)
            baseline_values.append(optym_data[col].mean())
            
            # Find corresponding optimized column
            optimized_col = col.replace('_baseline', '_optimized')
            if optimized_col in optym_data.columns:
                optimized_values.append(optym_data[optimized_col].mean())
            else:
                optimized_values.append(0)  # Fallback if no matching optimized column
    
    # Create a dataframe for the comparison chart
    comparison_df = pd.DataFrame({
        'Channel': channels,
        'Baseline Budget': baseline_values,
        'Optimized Budget': optimized_values
    })
    
    # Melt the dataframe for plotting
    comparison_melted = pd.melt(
        comparison_df,
        id_vars=['Channel'],
        value_vars=['Baseline Budget', 'Optimized Budget'],
        var_name='Budget Type',
        value_name='Budget Value'
    )
    
    # Create clustered bar chart comparing baseline and optimized budgets
    fig = go.Figure()
    
    # Add bars for baseline budget
    fig.add_trace(go.Bar(
        x=comparison_melted[comparison_melted['Budget Type'] == 'Baseline Budget']['Channel'],
        y=comparison_melted[comparison_melted['Budget Type'] == 'Baseline Budget']['Budget Value'],
        name='Baseline Budget',
        marker_color=BLUE_PALETTE[0],
        text=comparison_melted[comparison_melted['Budget Type'] == 'Baseline Budget']['Budget Value'].round(2),
        textposition='outside'
    ))
    
    # Add bars for optimized budget
    fig.add_trace(go.Bar(
        x=comparison_melted[comparison_melted['Budget Type'] == 'Optimized Budget']['Channel'],
        y=comparison_melted[comparison_melted['Budget Type'] == 'Optimized Budget']['Budget Value'],
        name='Optimized Budget',
        marker_color=BLUE_PALETTE[2],
        text=comparison_melted[comparison_melted['Budget Type'] == 'Optimized Budget']['Budget Value'].round(2),
        textposition='outside'
    ))
    
    # Update layout
    fig.update_layout(
        title='Optym Model: Baseline vs Optimized Budget Comparison',
        xaxis_title='Marketing Channel',
        yaxis_title='Budget Value',
        barmode='group',
        plot_bgcolor='white',
        font=dict(color='#424242'),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        margin=dict(l=10, r=10, t=30, b=10),
        hovermode='x unified',
        bargap=0.2,
        bargroupgap=0.1
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Show example of target efficiency allocation
    st.image("attached_assets/1_190_4_reallocated_target_roas.png")

# Feature Importance Analysis
st.subheader("Channel Feature Importance by Product Category")

# Load feature importance data
feature_importance = pd.read_csv('attached_assets/feature_importance_values.csv')

# Prepare data for visualization
feature_importance = feature_importance.set_index('Unnamed: 0', drop=True) if 'Unnamed: 0' in feature_importance.columns else feature_importance.iloc[:, 1:].set_index(feature_importance.iloc[:, 0])

# Transpose for better visualization
feature_importance_t = feature_importance.transpose()

# Create heatmap of feature importance values by product
fig = px.imshow(
    feature_importance,
    labels=dict(x="Marketing Channel", y="Product Category", color="Importance Score"),
    x=feature_importance.columns,
    y=feature_importance.index,
    color_continuous_scale=['#e3f2fd', '#bbdefb', '#90caf9', '#64b5f6', '#42a5f5', '#2196f3', '#1e88e5', '#1976d2', '#1565c0', '#0d47a1'],
    title="Feature Importance by Product Category and Marketing Channel"
)

fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(color='#424242'),
    margin=dict(l=10, r=10, t=50, b=10),
    coloraxis_colorbar=dict(
        title="Importance",
        thicknessmode="pixels", thickness=20,
        lenmode="pixels", len=300,
        ticks="outside"
    )
)

st.plotly_chart(fig, use_container_width=True)

# Create a bar chart showing channel importance across all product categories
channel_importance = feature_importance.mean(axis=0).reset_index()
channel_importance.columns = ['Channel', 'Average Importance']
channel_importance = channel_importance.sort_values('Average Importance', ascending=False)

fig = px.bar(
    channel_importance,
    x='Channel',
    y='Average Importance',
    color='Average Importance',
    color_continuous_scale=['#e3f2fd', '#bbdefb', '#90caf9', '#64b5f6', '#42a5f5', '#2196f3', '#1e88e5', '#1976d2'],
    title='Average Channel Importance Across All Product Categories',
    text='Average Importance'
)

fig.update_traces(
    texttemplate='%{text:.3f}',
    textposition='outside'
)

fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(color='#424242'),
    xaxis_title='Marketing Channel',
    yaxis_title='Average Importance Score',
    coloraxis_showscale=False,
    margin=dict(l=10, r=10, t=50, b=10)
)

st.plotly_chart(fig, use_container_width=True)

# Channel ROAS Analysis
st.subheader("Channel ROAS Analysis")

# Calculate the actual ROAS using product revenue and budget data
st.markdown("""
This analysis uses the Robyn model data to calculate and compare the Return on Ad Spend (ROAS) for each marketing channel.
The ROAS values represent the revenue generated for each dollar spent in that marketing channel.
""")

# Load the Robyn data which has Revenue_Lift per channel
robyn_data = pd.read_csv('attached_assets/Robyn_marketing_budget_allocation.csv')

# Display the Revenue per Dollar metric which is already in the data
robyn_roas = robyn_data[['Channel', 'Revenue_per_Dollar']].copy()
robyn_roas = robyn_roas.sort_values('Revenue_per_Dollar', ascending=False)

fig = px.bar(
    robyn_roas,
    x='Channel',
    y='Revenue_per_Dollar',
    color='Revenue_per_Dollar',
    color_continuous_scale=px.colors.sequential.Blues,
    title='ROAS by Marketing Channel (Robyn Model)',
    text='Revenue_per_Dollar'
)

fig.update_traces(
    texttemplate='%{text:,.0f}',
    textposition='outside'
)

fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(color='#424242'),
    xaxis_title='Marketing Channel',
    yaxis_title='Revenue per Dollar Spent ($)',
    coloraxis_showscale=False,
    margin=dict(l=10, r=10, t=50, b=10)
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
