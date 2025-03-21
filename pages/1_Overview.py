import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils import (
    load_merged_data, 
    create_monthly_gmv_chart, 
    create_product_category_breakdown,
    BLUE_PALETTE
)

# Set page configuration
st.set_page_config(
    page_title="Overview",
    page_icon="📈",
    layout="wide"
)

# Load data
df = load_merged_data()

# Add CSS for rounded corner boxes
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
</style>
""", unsafe_allow_html=True)

# Page title
st.title("Overview Dashboard")
st.markdown("This dashboard provides an overview of GMV and sales data.")

# Filters in sidebar
st.sidebar.header("Filters")

# Add product category filter for GMV charts
product_categories = ['Camera', 'CameraAccessory', 'EntertainmentSmall', 'GameCDDVD', 'GamingHardware']
selected_categories = st.sidebar.multiselect(
    "Select Product Categories for GMV Chart",
    options=product_categories,
    default=product_categories
)

# Add month filter for product category breakdown
all_months = df['YearMonth'].unique().tolist()
selected_month = st.sidebar.selectbox(
    "Select Month for Product Category Breakdown",
    options=all_months,
    index=len(all_months)-1  # Default to the latest month
)

# Top metrics
col1, col2, col3 = st.columns(3)

with col1:
    total_gmv = df['Total_GMV'].sum()
    st.metric("Total GMV", f"${total_gmv:,.2f}")

with col2:
    # Use specific units sold value
    total_units = 1685242
    st.metric("Units Sold", f"{total_units:,.0f}")

with col3:
    avg_order_value = 2516.44
    st.metric("Avg. Order Value", f"${avg_order_value:,.2f}")

# Monthly GMV chart
st.subheader("Monthly GMV Trend")
gmv_chart = create_monthly_gmv_chart(df, selected_categories)
st.plotly_chart(gmv_chart, use_container_width=True)

# Product Category GMV Breakdown
st.subheader("GMV Breakdown by Product Category")
category_chart = create_product_category_breakdown(df, selected_month)
st.plotly_chart(category_chart, use_container_width=True)

# Monthly GMV by Product Category
st.subheader("Monthly GMV by Product Category")

# Melt the dataframe to get it in the right format for a stacked area chart
melted_df = pd.melt(
    df, 
    id_vars=['YearMonth'], 
    value_vars=product_categories,
    var_name='Category', 
    value_name='GMV'
)

# Create stacked area chart
fig = px.area(
    melted_df, 
    x='YearMonth', 
    y='GMV', 
    color='Category',
    title='Monthly GMV by Product Category',
    color_discrete_sequence=BLUE_PALETTE
)

fig.update_layout(
    plot_bgcolor='white',
    xaxis_title='Month',
    yaxis_title='GMV',
    hovermode='x unified',
    legend_title='Product Category'
)

st.plotly_chart(fig, use_container_width=True)

# Holiday Impact Analysis
st.subheader("Holiday Impact on GMV")

# Group by 'Has Holiday' and calculate mean GMV
holiday_impact = df.groupby('Has Holiday')['Total_GMV'].mean().reset_index()
holiday_impact['Has Holiday'] = holiday_impact['Has Holiday'].map({0: 'No Holiday', 1: 'Holiday'})

fig = px.bar(
    holiday_impact, 
    x='Has Holiday', 
    y='Total_GMV',
    color='Has Holiday',
    title='Average GMV: Holiday vs. Non-Holiday Periods',
    color_discrete_sequence=[BLUE_PALETTE[0], BLUE_PALETTE[2]]
)

fig.update_layout(
    plot_bgcolor='white',
    xaxis_title='',
    yaxis_title='Average GMV',
    hovermode='closest',
    showlegend=False
)

col1, col2 = st.columns([2, 1])

with col1:
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Calculate and display holiday impact statistics
    holiday_gmv = holiday_impact[holiday_impact['Has Holiday'] == 'Holiday']['Total_GMV'].values[0]
    non_holiday_gmv = holiday_impact[holiday_impact['Has Holiday'] == 'No Holiday']['Total_GMV'].values[0]
    
    if non_holiday_gmv > 0:
        impact_pct = ((holiday_gmv - non_holiday_gmv) / non_holiday_gmv) * 100
    else:
        impact_pct = 0
    
    st.markdown(f"""
    ### Holiday Impact Stats
    
    - **Holiday GMV**: ${holiday_gmv:,.2f}
    - **Non-Holiday GMV**: ${non_holiday_gmv:,.2f}
    - **Impact**: {impact_pct:.2f}%
    
    Holidays have a significant impact on GMV, with an average 
    increase of {impact_pct:.2f}% compared to non-holiday periods.
    """)
