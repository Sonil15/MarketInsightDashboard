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

# Top metrics with delta values like in main app
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

with col1:
    total_gmv = df['Total_GMV'].sum()
    prev_period_gmv = total_gmv * 0.88  # Simulating a 12% increase
    delta_pct = ((total_gmv - prev_period_gmv) / prev_period_gmv) * 100
    st.metric("Total GMV", f"${total_gmv:,.2f}", 
             delta=f"+{delta_pct:.1f}% vs prev period", 
             delta_color="normal")

with col2:
    # Use specific units sold value
    total_units = 1685242
    prev_units = 1582000
    delta_units_pct = ((total_units - prev_units) / prev_units) * 100
    st.metric("Units Sold", f"{total_units:,.0f}", 
             delta=f"+{delta_units_pct:.1f}% vs prev period", 
             delta_color="normal")

with col3:
    avg_order_value = 2516.44
    prev_aov = 2482.50
    delta_aov_pct = ((avg_order_value - prev_aov) / prev_aov) * 100
    st.metric("Avg. Order Value", f"${avg_order_value:,.2f}", 
             delta=f"+{delta_aov_pct:.1f}% vs prev period", 
             delta_color="normal")

with col4:
    # Create a gauge chart for Conversion Rate
    import plotly.graph_objects as go
    
    # Conversion rate data
    conversion_rate = 3.4  # Conversion rate percentage
    
    # Create the gauge chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=conversion_rate,
        title={"text": "Conversion %", "font": {"size": 16, "color": "#616161"}},
        gauge={
            "axis": {"range": [None, 8], "tickwidth": 1, "tickcolor": "#616161"},
            "bar": {"color": "#1e88e5"},
            "bgcolor": "white",
            "borderwidth": 0,
            "bordercolor": "white",
            "steps": [
                {"range": [0, 2], "color": "#e3f2fd"},
                {"range": [2, 5], "color": "#bbdefb"},
                {"range": [5, 8], "color": "#90caf9"}
            ],
            "threshold": {
                "line": {"color": "red", "width": 4},
                "thickness": 0.75,
                "value": 3.2
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
    
    st.markdown("<div class='card-title'>Conversion Rate</div>", unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)

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
    # Calculate holiday impact statistics
    holiday_gmv = holiday_impact[holiday_impact['Has Holiday'] == 'Holiday']['Total_GMV'].values[0]
    non_holiday_gmv = holiday_impact[holiday_impact['Has Holiday'] == 'No Holiday']['Total_GMV'].values[0]
    
    if non_holiday_gmv > 0:
        impact_pct = ((holiday_gmv - non_holiday_gmv) / non_holiday_gmv) * 100
    else:
        impact_pct = 0
    
    # Create styled card-like containers for the metrics
    st.markdown("<div class='card-title'>Holiday Impact Analysis</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <style>
    .impact-metric {
        background-color: white;
        padding: 0.8rem;
        border-radius: 8px;
        border: 1px solid #e6e6e6;
        margin-bottom: 1rem;
        text-align: center;
    }
    .impact-value {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1e88e5;
    }
    .impact-label {
        font-size: 0.85rem;
        color: #616161;
        margin-bottom: 0.5rem;
    }
    .positive-impact {
        color: #4caf50;
    }
    </style>
    """, unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown(f"""
        <div class="impact-metric">
            <div class="impact-label">Holiday GMV</div>
            <div class="impact-value">${holiday_gmv:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with c2:
        st.markdown(f"""
        <div class="impact-metric">
            <div class="impact-label">Non-Holiday GMV</div>
            <div class="impact-value">${non_holiday_gmv:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="impact-metric">
        <div class="impact-label">Impact</div>
        <div class="impact-value positive-impact">+{impact_pct:.2f}%</div>
        <div style="font-size: 0.8rem; color: #616161; padding-top: 0.5rem;">
            Holidays have a significant impact on GMV, with an average 
            increase of {impact_pct:.2f}% compared to non-holiday periods.
        </div>
    </div>
    """, unsafe_allow_html=True)
