import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import plotly.express as px

# Blue color palette
BLUE_PALETTE = ['#0D2A63', '#2073BC', '#2196f3', '#64b5f6', '#bbdefb']

# Set page configuration
st.set_page_config(
    page_title="Budget Optimization",
    page_icon="💰",
    layout="wide"
)

# CSS for rounded box corners
st.markdown("""
<style>
    div.stPlotlyChart, div.stText, div.stMarkdown, div.stMetric {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #e6e6e6;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    
    div.block-container {
        padding-top: 2rem;
    }
    
    div.stSelectbox > div[data-baseweb="select"] {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Page title
st.title("Budget Optimization Analysis")

# Big number metrics for model comparison
col1, col2 = st.columns(2)

with col1:
    st.metric("Optym Model Revenue Improvement", "32.44%", delta="Better performance")

with col2:
    st.metric("Robyn Model Revenue Improvement", "31.90%", delta="Strong performance")

# Load monthly revenue data
revenue_data = pd.read_csv('attached_assets/overall_revenue_monthly.csv')
revenue_data['month'] = ['March', 'April', 'May', 'June']

# Create four bar charts, one for each month
st.subheader("Monthly Revenue Comparison: Baseline vs Optimized")

# Create a combined chart for all months
fig = go.Figure()

# Add baseline bars
fig.add_trace(go.Bar(
    x=revenue_data['month'],
    y=revenue_data['baseline'],
    name='Baseline',
    marker_color=BLUE_PALETTE[0],
    text=revenue_data['baseline'].round(1),
    textposition='auto'
))

# Add optimized bars
fig.add_trace(go.Bar(
    x=revenue_data['month'],
    y=revenue_data['optimized'],
    name='Optimized',
    marker_color=BLUE_PALETTE[1],
    text=revenue_data['optimized'].round(1),
    textposition='auto'
))

# Add percentage labels
for i, row in revenue_data.iterrows():
    improvement_pct = (row['optimized'] - row['baseline']) / row['baseline'] * 100
    
    # Create a percentage label with a box around it
    fig.add_annotation(
        x=row['month'],
        y=row['optimized'] + 30,  # Position above the optimized bar
        text=f"{improvement_pct:.1f}%",
        showarrow=False,
        font=dict(size=12, color="black"),
        bgcolor="white",
        bordercolor="#2196f3",
        borderwidth=2,
        borderpad=4,
        opacity=0.8
    )

# Update layout
fig.update_layout(
    barmode='group',
    plot_bgcolor='white',
    font=dict(family="Arial", size=12),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
    margin=dict(l=50, r=50, t=80, b=50),
    yaxis=dict(
        title="Revenue",
        gridcolor='lightgrey',
        zerolinecolor='lightgrey'
    ),
    xaxis=dict(
        title="Month",
        tickfont=dict(size=14)
    ),
    height=500
)

st.plotly_chart(fig, use_container_width=True)

# Separate charts for individual months
cols = st.columns(4)
months = ['March', 'April', 'May', 'June']

for i, (col, month) in enumerate(zip(cols, months)):
    with col:
        monthly_data = revenue_data[revenue_data['month'] == month].iloc[0]
        
        # Create individual chart
        fig = go.Figure()
        
        # Add baseline bar
        fig.add_trace(go.Bar(
            x=['Baseline'],
            y=[monthly_data['baseline']],
            marker_color=BLUE_PALETTE[0],
            width=0.4,
            text=[round(monthly_data['baseline'], 1)],
            textposition='auto'
        ))
        
        # Add optimized bar
        fig.add_trace(go.Bar(
            x=['Optimized'],
            y=[monthly_data['optimized']],
            marker_color=BLUE_PALETTE[1],
            width=0.4,
            text=[round(monthly_data['optimized'], 1)],
            textposition='auto'
        ))
        
        # Calculate improvement percentage
        improvement_pct = (monthly_data['optimized'] - monthly_data['baseline']) / monthly_data['baseline'] * 100
        
        # Add percentage label
        fig.add_annotation(
            x=0.5,
            y=monthly_data['optimized'] + (monthly_data['optimized'] * 0.1),
            text=f"{improvement_pct:.1f}%",
            showarrow=False,
            font=dict(size=12, color="black"),
            bgcolor="white",
            bordercolor="#2196f3",
            borderwidth=2,
            borderpad=4,
            opacity=0.8
        )
        
        # Update layout
        fig.update_layout(
            title=month,
            plot_bgcolor='white',
            showlegend=False,
            margin=dict(l=10, r=10, t=40, b=10),
            height=250,
            yaxis=dict(
                gridcolor='lightgrey',
                zerolinecolor='lightgrey'
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)

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
    marker_color=BLUE_PALETTE[1],
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

# Feature Importance chart with slicer
st.subheader("Product-wise Feature Importance by Marketing Channel")

# Load feature importance data
feature_data = pd.read_csv('attached_assets/feature_importance_values.csv', index_col=0)

# Add product selector
product_options = feature_data.index.tolist()
product_options.insert(0, "All Products")  # Add "All Products" option
selected_product = st.selectbox("Select Product Category", product_options)

# Filter data based on selection
if selected_product == "All Products":
    # Calculate average across all products
    feature_importance_data = feature_data.mean().reset_index()
    feature_importance_data.columns = ['Channel', 'Importance']
    
    # Create bar chart for all products
    fig3 = px.bar(
        feature_importance_data, 
        x='Channel', 
        y='Importance',
        title='Average Feature Importance Across All Products',
        color='Importance',
        color_continuous_scale=px.colors.sequential.Blues,
        text='Importance'
    )
    
    fig3.update_traces(
        texttemplate='%{text:.3f}',
        textposition='outside'
    )
else:
    # Get data for selected product
    product_data = feature_data.loc[selected_product].reset_index()
    product_data.columns = ['Channel', 'Importance']
    
    # Create bar chart for selected product
    fig3 = px.bar(
        product_data, 
        x='Channel', 
        y='Importance',
        title=f'Feature Importance for {selected_product}',
        color='Importance',
        color_continuous_scale=px.colors.sequential.Blues,
        text='Importance'
    )
    
    fig3.update_traces(
        texttemplate='%{text:.3f}',
        textposition='outside'
    )

# Update layout
fig3.update_layout(
    plot_bgcolor='white',
    font=dict(color='#424242'),
    xaxis_title='Marketing Channel',
    yaxis_title='Feature Importance',
    margin=dict(l=10, r=10, t=50, b=10),
    coloraxis_showscale=False
)

st.plotly_chart(fig3, use_container_width=True)