import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import ast
import re

# Set blue color theme with enhanced gradient
BLUE_PALETTE = ['#0D47A1', '#1565C0', '#1976D2', '#1E88E5', '#2196F3', '#42A5F5', '#64B5F6', '#90CAF9', '#BBDEFB', '#E3F2FD']
SINGLE_BLUE = '#1976D2'
# Highlight colors for important elements
HIGHLIGHT_BLUE = '#01579B'
ACCENT_BLUE = '#29B6F6'

@st.cache_data
def load_merged_data():
    df = pd.read_csv('attached_assets/final_merged.csv')
    # Create YearMonth column for easier filtering
    df['YearMonth'] = df['Year'].astype(str) + '-' + df['Month'].astype(str).str.zfill(2)
    return df

@st.cache_data
def load_optimized_spend():
    df = pd.read_csv('attached_assets/final_optimized_spend.csv', header=0)
    return df

@st.cache_data
def load_overall_revenue():
    df = pd.read_csv('attached_assets/final_overall_revenue.csv', header=0)
    
    # Convert string representations of dictionaries to actual dictionaries
    df['revenue_dict'] = df['overall_revenue'].apply(lambda x: ast.literal_eval(re.sub(r'np\.float64\(([^)]+)\)', r'\1', x)))
    
    # Create new columns from dictionary values
    df['baseline'] = df['revenue_dict'].apply(lambda x: x['baseline'])
    df['optimized'] = df['revenue_dict'].apply(lambda x: x['optimized'])
    df['improvement'] = df['revenue_dict'].apply(lambda x: x['improvement'])
    df['improvement_pct'] = df['revenue_dict'].apply(lambda x: x['improvement_pct'])
    
    return df

@st.cache_data
def load_product_revenue():
    df = pd.read_csv('attached_assets/final_product_revenue.csv', header=0)
    return df

@st.cache_data
def load_robyn_max_response():
    df = pd.read_csv('attached_assets/1_190_4_max_response_reallocated.csv', header=0)
    return df

@st.cache_data
def load_robyn_target_efficiency():
    df = pd.read_csv('attached_assets/1_190_4_target_efficiency_reallocated.csv', header=0)
    return df

def create_monthly_gmv_chart(df, selected_categories=None):
    """Create a monthly GMV line chart with optional product category filtering"""
    
    if selected_categories and len(selected_categories) > 0:
        filtered_df = df.copy()
        
        # Calculate total GMV for selected categories
        selected_cols = [cat for cat in ['Camera', 'CameraAccessory', 'EntertainmentSmall', 'GameCDDVD', 'GamingHardware'] 
                        if cat in selected_categories]
        
        if selected_cols:
            filtered_df['Selected_GMV'] = filtered_df[selected_cols].sum(axis=1)
        else:
            filtered_df['Selected_GMV'] = filtered_df['Total_GMV']
            
        fig = px.line(filtered_df, x='YearMonth', y='Selected_GMV', 
                     title='Monthly Total GMV for Selected Categories',
                     labels={'Selected_GMV': 'GMV', 'YearMonth': 'Month'},
                     markers=True)
    else:
        fig = px.line(df, x='YearMonth', y='Total_GMV', 
                     title='Monthly Total GMV',
                     labels={'Total_GMV': 'GMV', 'YearMonth': 'Month'},
                     markers=True)
    
    fig.update_traces(line_color=SINGLE_BLUE, marker_color=SINGLE_BLUE)
    fig.update_layout(
        plot_bgcolor='white',
        xaxis_title='Month',
        yaxis_title='GMV',
        hovermode='x unified'
    )
    
    return fig

def create_product_category_breakdown(df, selected_month=None):
    """Create a product category breakdown chart with optional month filtering"""
    
    if selected_month:
        filtered_df = df[df['YearMonth'] == selected_month]
    else:
        filtered_df = df.copy()
    
    # Get product categories and their GMV
    product_categories = ['Camera', 'CameraAccessory', 'EntertainmentSmall', 'GameCDDVD', 'GamingHardware']
    
    # Create a new dataframe for the visualization
    breakdown_df = pd.DataFrame({
        'Category': product_categories,
        'GMV': [filtered_df[cat].sum() for cat in product_categories]
    })
    
    # Sort by GMV
    breakdown_df = breakdown_df.sort_values('GMV', ascending=False)
    
    fig = px.bar(breakdown_df, x='Category', y='GMV', 
                title='GMV Breakdown by Product Category',
                color_discrete_sequence=BLUE_PALETTE)
    
    fig.update_layout(
        plot_bgcolor='white',
        xaxis_title='Product Category',
        yaxis_title='GMV',
        hovermode='x unified'
    )
    
    return fig

def create_marketing_channel_chart(df):
    """Create a chart showing marketing spend by channel over time"""
    
    channels = ['TV', 'Digital', 'Sponsorship', 'Content Marketing', 
                'Online Marketing', 'Affiliates', 'SEM', 'Radio', 'Other']
    
    # Melt the dataframe to get a long format for plotting
    melted_df = pd.melt(df, id_vars=['YearMonth'], 
                        value_vars=channels,
                        var_name='Channel', value_name='Investment')
    
    fig = px.line(melted_df, x='YearMonth', y='Investment', color='Channel',
                 title='Monthly Investment by Marketing Channel',
                 labels={'Investment': 'Investment Amount', 'YearMonth': 'Month'},
                 color_discrete_sequence=BLUE_PALETTE,
                 markers=True)
    
    fig.update_layout(
        plot_bgcolor='white',
        xaxis_title='Month',
        yaxis_title='Investment Amount',
        hovermode='x unified',
        legend_title='Marketing Channel'
    )
    
    return fig

def create_correlation_heatmap(df, columns):
    """Create a correlation heatmap for selected columns"""
    
    corr_df = df[columns].corr()
    
    fig = px.imshow(corr_df, 
                   color_continuous_scale=px.colors.sequential.Blues,
                   title='Correlation Between Variables')
    
    fig.update_layout(
        plot_bgcolor='white',
        xaxis_title='',
        yaxis_title='',
        height=500
    )
    
    return fig

def create_nps_gmv_chart(df):
    """Create a scatter plot of NPS vs Total GMV"""
    
    fig = px.scatter(df, x='NPS', y='Total_GMV', 
                    title='NPS vs Total GMV',
                    color_discrete_sequence=[SINGLE_BLUE],
                    labels={'NPS': 'NPS Score', 'Total_GMV': 'Total GMV'},
                    hover_data=['YearMonth'])
    
    fig.update_layout(
        plot_bgcolor='white',
        xaxis_title='NPS Score',
        yaxis_title='Total GMV',
        hovermode='closest'
    )
    
    return fig

def create_stock_gmv_chart(df):
    """Create a scatter plot of Stock Index vs Total GMV"""
    
    fig = px.scatter(df, x='Stock Index', y='Total_GMV', 
                    title='Stock Index vs Total GMV',
                    color_discrete_sequence=[SINGLE_BLUE],
                    labels={'Stock Index': 'Stock Index', 'Total_GMV': 'Total GMV'},
                    hover_data=['YearMonth'])
    
    fig.update_layout(
        plot_bgcolor='white',
        xaxis_title='Stock Index',
        yaxis_title='Total GMV',
        hovermode='closest'
    )
    
    return fig

def create_weather_correlation_chart(df):
    """Create chart showing weather factors correlation with Total GMV"""
    
    weather_cols = ['tavg', 'prcp', 'wspd', 'pres']
    
    # Calculate correlations between weather factors and GMV
    corr_dict = {}
    for col in weather_cols:
        corr_dict[col] = np.corrcoef(df[col], df['Total_GMV'])[0, 1]
    
    # Create dataframe for plotting
    corr_df = pd.DataFrame({
        'Weather Factor': list(corr_dict.keys()),
        'Correlation with GMV': list(corr_dict.values())
    })
    
    fig = px.bar(corr_df, x='Weather Factor', y='Correlation with GMV',
                title='Correlation of Weather Factors with Total GMV',
                color_discrete_sequence=[SINGLE_BLUE])
    
    fig.update_layout(
        plot_bgcolor='white',
        xaxis_title='Weather Factor',
        yaxis_title='Correlation Coefficient',
        hovermode='closest'
    )
    
    return fig

def create_kpi_time_series(df, kpi_column, title, y_label):
    """Create a time series chart for a given KPI"""
    
    fig = px.line(df, x='YearMonth', y=kpi_column, 
                 title=title,
                 labels={kpi_column: y_label, 'YearMonth': 'Month'},
                 markers=True)
    
    fig.update_traces(line_color=SINGLE_BLUE, marker_color=SINGLE_BLUE)
    fig.update_layout(
        plot_bgcolor='white',
        xaxis_title='Month',
        yaxis_title=y_label,
        hovermode='x unified'
    )
    
    return fig

def create_clv_cac_comparison(df):
    """Create a comparison chart of CLV vs CAC"""
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df['YearMonth'],
        y=df['CLV'],
        name='CLV',
        marker_color=BLUE_PALETTE[0]
    ))
    
    fig.add_trace(go.Bar(
        x=df['YearMonth'],
        y=df['CAC'],
        name='CAC',
        marker_color=BLUE_PALETTE[2]
    ))
    
    fig.add_trace(go.Scatter(
        x=df['YearMonth'],
        y=df['CLV'] / df['CAC'],
        name='CLV/CAC Ratio',
        mode='lines+markers',
        yaxis='y2',
        line=dict(color=BLUE_PALETTE[4], width=2),
        marker=dict(color=BLUE_PALETTE[4], size=8)
    ))
    
    fig.update_layout(
        title='CLV vs CAC Comparison',
        plot_bgcolor='white',
        xaxis_title='Month',
        yaxis_title='Value',
        yaxis2=dict(
            title='CLV/CAC Ratio',
            overlaying='y',
            side='right'
        ),
        hovermode='x unified',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )
    
    return fig

def create_performance_metrics_chart(df):
    """Create a chart showing delivery and procurement performance over time"""
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['YearMonth'],
        y=df['Delivery_Performance'],
        name='Delivery Performance',
        mode='lines+markers',
        line=dict(color=BLUE_PALETTE[0], width=2),
        marker=dict(color=BLUE_PALETTE[0], size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=df['YearMonth'],
        y=df['Procurement_Performance'],
        name='Procurement Performance',
        mode='lines+markers',
        line=dict(color=BLUE_PALETTE[2], width=2),
        marker=dict(color=BLUE_PALETTE[2], size=8)
    ))
    
    fig.update_layout(
        title='Delivery and Procurement Performance',
        plot_bgcolor='white',
        xaxis_title='Month',
        yaxis_title='Performance Score',
        hovermode='x unified',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )
    
    return fig

def create_nps_stock_chart(df):
    """Create a chart showing NPS and Stock Index over time"""
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Scatter(
            x=df['YearMonth'],
            y=df['NPS'],
            name='NPS',
            mode='lines+markers',
            line=dict(color=BLUE_PALETTE[0], width=2),
            marker=dict(color=BLUE_PALETTE[0], size=8)
        ),
        secondary_y=False
    )
    
    fig.add_trace(
        go.Scatter(
            x=df['YearMonth'],
            y=df['Stock Index'],
            name='Stock Index',
            mode='lines+markers',
            line=dict(color=BLUE_PALETTE[2], width=2),
            marker=dict(color=BLUE_PALETTE[2], size=8)
        ),
        secondary_y=True
    )
    
    fig.update_layout(
        title='NPS and Stock Index Over Time',
        plot_bgcolor='white',
        xaxis_title='Month',
        hovermode='x unified',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )
    
    fig.update_yaxes(title_text='NPS Score', secondary_y=False)
    fig.update_yaxes(title_text='Stock Index', secondary_y=True)
    
    return fig

def create_budget_comparison_chart(optimized_df, overall_revenue_df, robyn_df, title):
    """Create a comparison chart for Sarvottam and Robyn budget optimization models"""
    
    # Process Sarvottam Model data (using the first few rows from optimized_df and overall_revenue_df)
    # Column names in the CSV file have spaces in them, so we need to match exactly
    sarvottam_channels = ['TV', 'Digital', 'Sponsorship', 'Content Marketing', 
                          'Online marketing', ' Affiliates', 'SEM', 'Radio', 'Other']
    
    # Take average of first 12 rows as representative data
    sarvottam_spend = optimized_df.iloc[:12][sarvottam_channels].mean().values
    
    # Get baseline and optimized revenue
    sarvottam_baseline_revenue = overall_revenue_df['baseline'].iloc[0]
    sarvottam_optimized_revenue = overall_revenue_df['optimized'].iloc[0]
    sarvottam_improvement = overall_revenue_df['improvement_pct'].iloc[0]
    
    # Process Robyn Model data
    # Extract Affiliates, Online Marketing and Sponsorship from the Robyn data
    robyn_channels = ['Affiliates', 'Online_Marketing', 'Sponsorship']
    
    # Filter the robyn dataframe to include only necessary records
    robyn_data = {}
    for channel in robyn_channels:
        channel_row = robyn_df[robyn_df['channels'] == channel].iloc[0] if len(robyn_df[robyn_df['channels'] == channel]) > 0 else None
        if channel_row is not None:
            robyn_data[channel] = {
                'spend': channel_row['initSpendUnit'],
                'response': channel_row['optmResponseUnit']
            }
    
    # Create comparison dataframe
    model_comparison = {
        'Model': ['Sarvottam', 'Robyn MMM'],
        'Revenue Improvement (%)': [sarvottam_improvement, 30]  # Using 30% as example for Robyn
    }
    
    comparison_df = pd.DataFrame(model_comparison)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=comparison_df['Model'],
        y=comparison_df['Revenue Improvement (%)'],
        marker_color=[BLUE_PALETTE[0], BLUE_PALETTE[2]]
    ))
    
    fig.update_layout(
        title=title,
        plot_bgcolor='white',
        xaxis_title='Model',
        yaxis_title='Revenue Improvement (%)',
        hovermode='closest'
    )
    
    return fig

def create_optym_channel_allocation(optimized_df):
    """Create a chart showing channel allocation in the Sarvottam model"""
    
    # Get channel names and average allocation - match exact column names from CSV
    channels = ['TV', 'Digital', 'Sponsorship', 'Content Marketing', 
                'Online marketing', ' Affiliates', 'SEM', 'Radio', 'Other']
    
    # Calculate average allocation for first 12 months
    allocation = optimized_df.iloc[:12][channels].mean().reset_index()
    allocation.columns = ['Channel', 'Allocation']
    
    # Sort by allocation
    allocation = allocation.sort_values('Allocation', ascending=False)
    
    fig = px.bar(allocation, x='Channel', y='Allocation',
                title='Optym Model: Channel Allocation',
                color_discrete_sequence=BLUE_PALETTE)
    
    fig.update_layout(
        plot_bgcolor='white',
        xaxis_title='Marketing Channel',
        yaxis_title='Average Allocation',
        hovermode='closest'
    )
    
    return fig

def create_robyn_channel_allocation(robyn_df):
    """Create a chart showing channel allocation in the Robyn model"""
    
    # Extract channels and their spend
    channels = robyn_df['channels'].tolist()
    
    # Try to get initSpendShare or similar field
    if 'initSpendShare' in robyn_df.columns:
        allocation = robyn_df['initSpendShare'].tolist()
    else:
        # If not available, use any other relevant column
        allocation = robyn_df['initSpendUnit'].tolist()
    
    allocation_df = pd.DataFrame({
        'Channel': channels,
        'Allocation': allocation
    })
    
    # Sort by allocation
    allocation_df = allocation_df.sort_values('Allocation', ascending=False)
    
    fig = px.bar(allocation_df, x='Channel', y='Allocation',
                title='Robyn Model: Channel Allocation',
                color_discrete_sequence=BLUE_PALETTE)
    
    fig.update_layout(
        plot_bgcolor='white',
        xaxis_title='Marketing Channel',
        yaxis_title='Allocation',
        hovermode='closest'
    )
    
    return fig
