import streamlit as st
from utils import load_merged_data

# Set page configuration
st.set_page_config(
    page_title="GMV & KPI Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add CSS inspired by the dashboard example
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-blue: #1e88e5;
        --light-blue: #e3f2fd;
        --medium-blue: #bbdefb;
        --dark-blue: #0d47a1;
        --accent-blue: #64b5f6;
    }
    
    /* Background color for the entire app */
    .main .block-container {
        background-color: #f8f9fa;
        padding-top: 1.5rem;
    }
    
    /* Card styling for metrics and charts */
    div.stPlotlyChart, div.stText, div.stMarkdown, div.stNumber, div.stDataFrame, div.stSelectbox, div.stMultiselect {
        background-color: #ffffff;
        padding: 1.2rem;
        border-radius: 8px;
        border: 1px solid #e6e6e6;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }
    
    /* Metric card styling inspired by dashboard */
    div.stMetric {
        background-color: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        border: 1px solid #e6e6e6;
        margin-bottom: 1rem;
    }
    
    /* Metric value styling - big numbers */
    div[data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        color: #212121 !important;
        text-align: center !important;
    }
    
    /* Metric label styling */
    div[data-testid="stMetricLabel"] {
        font-size: 1rem !important;
        color: #616161 !important;
        text-align: center !important;
        padding-bottom: 0.5rem;
        font-weight: 500;
    }
    
    /* Metric delta styling - red/green indicators */
    div[data-testid="stMetricDelta"] > div {
        text-align: center !important;
        font-size: 0.8rem !important;
        background-color: #f5f5f5;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
    }
    
    /* Header styling */
    div[data-testid="stHeader"] {
        background-color: transparent;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: white;
        border-right: 1px solid #e6e6e6;
    }
    
    /* Headings styling */
    h1 {
        color: #212121 !important;
        font-weight: 600 !important;
        font-size: 1.8rem !important;
    }
    
    h2 {
        color: #424242 !important;
        font-weight: 600 !important;
        font-size: 1.4rem !important;
    }
    
    h3 {
        color: #616161 !important;
        font-weight: 500 !important;
        font-size: 1.2rem !important;
    }
    
    /* Graph area styling - blue area chart */
    .js-plotly-plot .plotly .layer {
        fill-opacity: 0.2 !important;
    }
    
    /* Button styling */
    button[kind="primary"] {
        background-color: #1e88e5;
        border: none;
    }
    
    /* Card title styling */
    .card-title {
        font-size: 1rem;
        font-weight: 500;
        color: #616161;
        margin-bottom: 0.5rem;
    }
    
    /* Table styling for dashboard tables */
    div.stTable {
        border: none !important;
    }
    
    div.stTable table {
        border-collapse: separate;
        border-spacing: 0;
        width: 100%;
    }
    
    div.stTable thead tr th {
        background-color: #f5f5f5;
        color: #616161;
        font-weight: 500;
        text-align: left;
        padding: 0.7rem;
        border: none;
    }
    
    div.stTable tbody tr td {
        border-top: 1px solid #f0f0f0;
        padding: 0.7rem;
        color: #212121;
    }
    
    /* Positive/negative values styling */
    .positive {
        color: #4caf50 !important;
    }
    
    .negative {
        color: #f44336 !important;
    }
    
    /* Line chart styling */
    .js-plotly-plot .plotly .scatterlayer .trace path {
        stroke-width: 2 !important;
    }
    
    /* Area under the line chart */
    .js-plotly-plot .plotly .scatterlayer .fills .legendfill {
        fill-opacity: 0.2 !important;
    }
</style>
""", unsafe_allow_html=True)

# Load data
df = load_merged_data()

# Dashboard title and description
st.title("GMV & KPI Dashboard")
st.markdown("""
This dashboard provides comprehensive analysis of GMV, KPIs, and marketing budget optimization.
Use the navigation in the sidebar to explore different aspects of the data.
""")

# Main page content
st.header("Quick Overview")

# Create metrics for top KPIs with delta values like in the inspiration dashboard
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

with col1:
    total_gmv = df['Total_GMV'].sum()
    # Calculate simulated delta (for demonstration)
    prev_period_gmv = total_gmv * 0.93  # Simulating a 7% increase
    delta_pct = ((total_gmv - prev_period_gmv) / prev_period_gmv) * 100
    st.metric("Average Position", "19", delta="-4 vs previous period (14)", delta_color="inverse")

with col2:
    total_impressions = 5363
    delta_pct_impressions = -30
    st.metric("Impressions", f"{total_impressions:,}", 
              delta=f"{delta_pct_impressions}% vs previous period (8,413)", 
              delta_color="inverse")

with col3:
    total_clicks = 152
    delta_pct_clicks = -58
    st.metric("Clicks", f"{total_clicks:,}", 
              delta=f"{delta_pct_clicks}% vs previous period (359)", 
              delta_color="inverse")

with col4:
    # Create a gauge chart for CTR (Click-Through Rate)
    import plotly.graph_objects as go
    
    # CTR data
    ctr_value = 500  # CTR value in percentage (500%)
    
    # Create the gauge chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=ctr_value,
        title={"text": "CTR %", "font": {"size": 16, "color": "#616161"}},
        gauge={
            "axis": {"range": [None, 1000], "tickwidth": 1, "tickcolor": "#616161"},
            "bar": {"color": "#1e88e5"},
            "bgcolor": "white",
            "borderwidth": 0,
            "bordercolor": "white",
            "steps": [
                {"range": [0, 350], "color": "#e3f2fd"},
                {"range": [350, 650], "color": "#bbdefb"},
                {"range": [650, 1000], "color": "#90caf9"}
            ],
            "threshold": {
                "line": {"color": "red", "width": 4},
                "thickness": 0.75,
                "value": 490
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
    
    st.markdown("<div class='card-title'>Click-Through Rate</div>", unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)

# Add charts like in the inspiration dashboard
col1, col2 = st.columns(2)

with col1:
    # Create an area chart with line for impressions
    st.subheader("Impressions Over Time")
    
    # Create sample data for visualization
    import plotly.graph_objects as go
    import numpy as np
    import pandas as pd
    
    # Generate date range for x-axis
    dates = pd.date_range(start='2024-02-19', end='2024-03-20')
    
    # Generate random impressions data with slight upward trend
    np.random.seed(42)
    base = 6000
    impressions = np.random.normal(base, 1500, size=len(dates))
    
    # Create the area chart with line
    fig = go.Figure()
    
    # Add the filled area (lighter color)
    fig.add_trace(go.Scatter(
        x=dates, 
        y=impressions,
        fill='tozeroy',
        fillcolor='rgba(33, 150, 243, 0.2)',
        line=dict(color='rgba(0,0,0,0)'),
        showlegend=False
    ))
    
    # Add the line (darker blue)
    fig.add_trace(go.Scatter(
        x=dates, 
        y=impressions,
        line=dict(color='#2196F3', width=2),
        showlegend=False
    ))
    
    # Add light gray background trend
    fig.add_trace(go.Scatter(
        x=dates,
        y=[base + (i * 30) for i in range(len(dates))],
        line=dict(color='rgba(200, 200, 200, 0.5)', width=1),
        showlegend=False
    ))
    
    # Update layout to match inspiration
    fig.update_layout(
        height=250,
        margin=dict(l=0, r=10, t=10, b=0),
        paper_bgcolor='white',
        plot_bgcolor='white',
        xaxis=dict(
            showgrid=False,
            zeroline=False
        ),
        yaxis=dict(
            range=[0, max(impressions) * 1.2],
            tickvals=[0, 3000, 5000, 8000, 10000, 13000],
            showgrid=True,
            gridcolor='rgba(200, 200, 200, 0.2)',
            zeroline=False
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Create an area chart with line for clicks
    st.subheader("Clicks Over Time")
    
    # Generate random clicks data with slight upward trend
    base_clicks = 150
    clicks = np.random.normal(base_clicks, 50, size=len(dates))
    
    # Create the area chart with line
    fig = go.Figure()
    
    # Add the filled area (lighter color)
    fig.add_trace(go.Scatter(
        x=dates, 
        y=clicks,
        fill='tozeroy',
        fillcolor='rgba(33, 150, 243, 0.2)',
        line=dict(color='rgba(0,0,0,0)'),
        showlegend=False
    ))
    
    # Add the line (darker blue)
    fig.add_trace(go.Scatter(
        x=dates, 
        y=clicks,
        line=dict(color='#2196F3', width=2),
        showlegend=False
    ))
    
    # Add light gray background trend
    fig.add_trace(go.Scatter(
        x=dates,
        y=[base_clicks + (i * 0.5) for i in range(len(dates))],
        line=dict(color='rgba(200, 200, 200, 0.5)', width=1),
        showlegend=False
    ))
    
    # Update layout to match inspiration
    fig.update_layout(
        height=250,
        margin=dict(l=0, r=10, t=10, b=0),
        paper_bgcolor='white',
        plot_bgcolor='white',
        xaxis=dict(
            showgrid=False,
            zeroline=False
        ),
        yaxis=dict(
            range=[0, max(clicks) * 1.2],
            tickvals=[0, 100, 200, 300, 400, 500, 600],
            showgrid=True,
            gridcolor='rgba(200, 200, 200, 0.2)',
            zeroline=False
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Add a data table section like in the example dashboard
st.subheader("Queries Overview")

# Create sample data for the table
query_data = {
    'Query': [
        'digital marketing software', 
        'marketing report template', 
        'marketing software', 
        'hubspot integrations',
        'youtube dashboard'
    ],
    'Impressions': [986, 941, 790, 785, 741],
    'Impressions_Trend': ['+7%', '+14%', '+5%', '+70%', '+293%'],
    'Clicks': [374, 121, 820, 597, 370],
    'Clicks_Trend': ['-36%', '-83%', '+5%', '-32%', '-37%'],
    'Position': [4, 1, 7, 8, 7],
    'Position_Trend': ['-55.6%', '+70%', '+600%', '+100%', '+133.3%'],
    'CTR': ['66,100%', '21,800%', '53,100%', '27,200%', '35,200%'],
    'CTR_Trend': ['+107%', '-56%', '-45%', '+6%', '-56%']
}

import pandas as pd
table_df = pd.DataFrame(query_data)

# Custom function to format the table with colored trends
def format_with_trends(df):
    # Create a copy of the dataframe with formatted values
    formatted_df = df.copy()
    
    # Format the trend columns with HTML for colors
    for col in ['Impressions', 'Clicks', 'Position', 'CTR']:
        trend_col = f'{col}_Trend'
        if trend_col in formatted_df.columns:
            formatted_df[col] = formatted_df.apply(
                lambda row: f"{row[col]} <span style='color: {'green' if '+' in str(row[trend_col]) else 'red'};'>{row[trend_col]}</span>", 
                axis=1
            )
    
    # Drop the trend columns since they're now embedded in the main columns
    for col in [c for c in formatted_df.columns if c.endswith('_Trend')]:
        formatted_df = formatted_df.drop(columns=[col])
        
    return formatted_df

# Apply formatting
display_df = format_with_trends(table_df)

# Display the table with HTML formatting
st.markdown("""
<style>
.dataframe {
    font-size: 12px !important;
    width: 100% !important;
}
.dataframe th {
    background-color: #f8f9fa !important;
    color: #616161 !important;
    font-weight: 500 !important;
    text-align: left !important;
    padding: 8px !important;
}
.dataframe td {
    padding: 8px !important;
    border-top: 1px solid #f0f0f0 !important;
}
.dataframe tr:hover {
    background-color: #f5f9ff !important;
}
</style>
""", unsafe_allow_html=True)

# Display the styled table
st.write(display_df.to_html(escape=False, index=False), unsafe_allow_html=True)

# Navigation section
st.subheader("Navigate the Dashboard")
st.markdown("""
- **Overview**: View total GMV and product category breakdown
- **Exploratory Data Analysis**: Analyze relationships between variables
- **KPI Analysis**: Monitor key performance indicators over time
- **Budget Optimization**: Compare budget optimization models
""")

# Footer
st.markdown("---")
st.markdown("Dashboard created with Streamlit and Plotly")
