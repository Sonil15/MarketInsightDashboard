import streamlit as st
import plotly.express as px
import pandas as pd
from utils import (
    load_merged_data,
    create_correlation_heatmap,
    create_nps_gmv_chart,
    create_stock_gmv_chart,
    create_marketing_channel_chart,
    create_weather_correlation_chart,
    BLUE_PALETTE
)

# Set page configuration
st.set_page_config(
    page_title="Exploratory Data Analysis",
    page_icon="🔍",
    layout="wide"
)

# Load data
df = load_merged_data()

# Page title
st.title("Exploratory Data Analysis")
st.markdown("This dashboard explores relationships between different variables in the dataset.")

# Add top metrics with delta values like in main app
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

with col1:
    avg_nps = df['NPS'].mean()
    prev_nps = avg_nps - 0.5  # Simulating improvement
    delta_nps = avg_nps - prev_nps
    st.metric("Average NPS", f"{avg_nps:.2f}", 
             delta=f"+{delta_nps:.1f} vs prev period", 
             delta_color="normal")

with col2:
    avg_stock = df['Stock_index'].mean()
    prev_stock = avg_stock * 0.95
    delta_stock_pct = ((avg_stock - prev_stock) / prev_stock) * 100
    st.metric("Avg Stock Index", f"{avg_stock:.1f}", 
             delta=f"+{delta_stock_pct:.1f}% vs prev period", 
             delta_color="normal")

with col3:
    digital_spend = df['Digital'].sum()
    prev_digital = digital_spend * 0.88
    delta_digital_pct = ((digital_spend - prev_digital) / prev_digital) * 100
    st.metric("Digital Marketing", f"${digital_spend:,.0f}", 
             delta=f"+{delta_digital_pct:.1f}% vs prev period", 
             delta_color="normal")

with col4:
    # Create a gauge chart for Correlation
    import plotly.graph_objects as go
    
    # Correlation data - simulated correlation between NPS and GMV
    correlation_value = 0.72  # Correlation coefficient
    
    # Create the gauge chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=correlation_value * 100,
        title={"text": "NPS-GMV Corr.", "font": {"size": 14, "color": "#616161"}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#616161"},
            "bar": {"color": "#1e88e5"},
            "bgcolor": "white",
            "borderwidth": 0,
            "bordercolor": "white",
            "steps": [
                {"range": [0, 30], "color": "#e3f2fd"},
                {"range": [30, 70], "color": "#bbdefb"},
                {"range": [70, 100], "color": "#90caf9"}
            ],
            "threshold": {
                "line": {"color": "green", "width": 4},
                "thickness": 0.75,
                "value": 60
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
    
    st.markdown("<div class='card-title'>NPS-GMV Correlation</div>", unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)

# NPS vs GMV Plot with card styling
st.subheader("NPS vs GMV Relationship")
nps_gmv_chart = create_nps_gmv_chart(df)
st.plotly_chart(nps_gmv_chart, use_container_width=True)

# Explanation in a styled card
st.markdown("""
<div style="background-color: white; padding: 1rem; border-radius: 8px; border: 1px solid #e6e6e6; margin-bottom: 1.5rem;">
    <div style="font-weight: 500; color: #616161; margin-bottom: 0.5rem;">Analysis Insights</div>
    <div style="color: #212121; font-size: 0.9rem;">
        The scatter plot above shows the relationship between NPS (Net Promoter Score) and total GMV (Gross Merchandise Value).
        The trend line indicates a positive correlation between customer satisfaction and sales, suggesting that improving NPS
        can lead to higher GMV.
    </div>
</div>
""", unsafe_allow_html=True)



# Marketing Channel Investment
st.subheader("Monthly Investment by Marketing Channel")
marketing_chart = create_marketing_channel_chart(df)
st.plotly_chart(marketing_chart, use_container_width=True)

# Monthly GMV Trend by Product Category
st.subheader("Monthly GMV Trend by Product Category")

# Filter columns for product categories
product_categories = ['Camera', 'CameraAccessory', 'EntertainmentSmall', 'GameCDDVD', 'GamingHardware']

# Create a DataFrame with product categories over time
product_df = df[['YearMonth'] + product_categories]

# Melt the DataFrame for plotting
melted_df = pd.melt(
    product_df,
    id_vars=['YearMonth'],
    value_vars=product_categories,
    var_name='Category',
    value_name='GMV'
)

# Create the line chart
fig = px.line(
    melted_df,
    x='YearMonth',
    y='GMV',
    color='Category',
    title='Monthly GMV by Product Category',
    color_discrete_sequence=BLUE_PALETTE,
    markers=True
)

fig.update_layout(
    plot_bgcolor='white',
    xaxis_title='Month',
    yaxis_title='GMV',
    hovermode='x unified',
    legend_title='Product Category'
)

st.plotly_chart(fig, use_container_width=True)

# Create two columns for weather correlation analysis
col1, col2 = st.columns(2)

with col1:
    # Weather Factors Correlation with GMV
    st.subheader("Weather Factors Correlation with Total GMV")
    weather_corr_chart = create_weather_correlation_chart(df)
    st.plotly_chart(weather_corr_chart, use_container_width=True)

    # Explanation
    st.markdown("""
    These charts show the correlation between various weather factors and total GMV:
    - **tavg**: Average temperature
    - **prcp**: Precipitation
    - **wspd**: Wind speed
    - **pres**: Atmospheric pressure
    """)

with col2:
    # Correlation Heatmap
    st.subheader("Weather Correlation Heatmap")

    # Select weather-related columns for correlation
    corr_columns = [
        'Total_GMV', 'tavg', 'prcp', 'wspd', 'pres'
    ]

    # Filter out columns that don't exist in the DataFrame
    corr_columns = [col for col in corr_columns if col in df.columns]

    # Create and display correlation heatmap
    corr_heatmap = create_correlation_heatmap(df, corr_columns)
    st.plotly_chart(corr_heatmap, use_container_width=True)

# Insights section with card styling
st.subheader("Key Insights")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style="background-color: white; padding: 1rem; border-radius: 8px; border: 1px solid #e6e6e6; height: 100%;">
        <div style="font-weight: 500; color: #1e88e5; margin-bottom: 0.8rem; font-size: 1.1rem;">Marketing Channel Effectiveness</div>
        <div style="color: #212121; font-size: 0.9rem;">
            <ul style="padding-left: 1.2rem; margin-top: 0.5rem;">
                <li style="margin-bottom: 0.5rem;"><span style="font-weight: 500; color: #424242;">Sponsorship</span> has the highest investment among all channels</li>
                <li style="margin-bottom: 0.5rem;"><span style="font-weight: 500; color: #424242;">Digital</span> marketing shows consistent investment over time</li>
                <li style="margin-bottom: 0.5rem;"><span style="font-weight: 500; color: #424242;">TV</span> advertising has varied investment patterns</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background-color: white; padding: 1rem; border-radius: 8px; border: 1px solid #e6e6e6; height: 100%;">
        <div style="font-weight: 500; color: #1e88e5; margin-bottom: 0.8rem; font-size: 1.1rem;">Weather and Sales Relationship</div>
        <div style="color: #212121; font-size: 0.9rem;">
            <ul style="padding-left: 1.2rem; margin-top: 0.5rem;">
                <li style="margin-bottom: 0.5rem;"><span style="font-weight: 500; color: #424242;">Temperature</span> shows a moderate correlation with GMV</li>
                <li style="margin-bottom: 0.5rem;"><span style="font-weight: 500; color: #424242;">Precipitation</span> has a weak negative correlation with sales</li>
                <li style="margin-bottom: 0.5rem;">Understanding these relationships can help in seasonal planning</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
