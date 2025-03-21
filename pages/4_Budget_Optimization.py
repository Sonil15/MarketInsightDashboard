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

# Load data for April 2024
optym_data = pd.read_csv('attached_assets/merged_file.csv')
april_data = optym_data.iloc[1]  # Second row is April 2024

# Define channels and get their baseline and optimized values
channels = ['Digital', 'Sponsorship', 'Content Marketing', 'in Online marketing', 'Affiliates', 'SEM', 'Radio', 'Other']
baseline_values = [april_data[f"{channel}_baseline"] for channel in channels]
optimized_values = [april_data[f"{channel}_optimized"] for channel in channels]

# Calculate percentage changes
pct_changes = [((opt - base) / base * 100) if base != 0 else 0 
               for base, opt in zip(baseline_values, optimized_values)]

# Create the figure
fig2 = go.Figure()

# Add baseline bars
fig2.add_trace(go.Bar(
    name='Baseline',
    x=channels,
    y=baseline_values,
    marker_color='navy',
))

# Add optimized bars
fig2.add_trace(go.Bar(
    name='Optimized',
    x=channels,
    y=optimized_values,
    marker_color='royalblue',
))

# Add percentage change annotations
for i, (pct, baseline, optimized) in enumerate(zip(pct_changes, baseline_values, optimized_values)):
    if baseline != 0 or optimized != 0:  # Only add annotation if there's a bar
        fig2.add_annotation(
            x=i,
            y=max(baseline, optimized),
            text=f"{pct:.1f}%",
            showarrow=False,
            yshift=10,
            font=dict(size=10)
        )

# Update layout
fig2.update_layout(
    title='Marketing Spend Allocation - Apr 2024',
    xaxis_title='Marketing Channel',
    yaxis_title='Spend',
    barmode='group',
    plot_bgcolor='white',
    font=dict(color='#424242'),
    showlegend=True,
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.02,
        xanchor='right',
        x=1
    ),
    margin=dict(l=10, r=10, t=60, b=10),
    yaxis=dict(gridcolor='lightgrey'),
)

st.plotly_chart(fig2, use_container_width=True)

# Feature Importance Chart
st.subheader("Product-wise Feature Importance by Marketing Channel")

# Load feature importance data
feature_data = pd.read_csv('attached_assets/feature_importance_values.csv', index_col=0)

# Create stacked bar chart
fig3 = go.Figure()

colors = ['navy', 'royalblue', 'cornflowerblue', 'lightsteelblue', 'powderblue']
products = feature_data.index

# Add traces for each product
for i, product in enumerate(products):
    fig3.add_trace(go.Bar(
        name=product,
        x=feature_data.columns,
        y=feature_data.loc[product],
        marker_color=colors[i]
    ))

# Update layout
fig3.update_layout(
    barmode='stack',
    title='Product-wise Feature Importance by Marketing Channel',
    xaxis_title='Marketing Channels',
    yaxis_title='Feature Importance',
    plot_bgcolor='white',
    showlegend=True,
    legend_title='Products',
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.02,
        xanchor='right',
        x=1
    ),
    margin=dict(l=10, r=10, t=60, b=10),
    yaxis=dict(
        gridcolor='lightgrey',
        range=[0, 2.5]
    )
)

st.plotly_chart(fig3, use_container_width=True)
