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

# NPS vs GMV Plot
st.subheader("NPS vs GMV")
nps_gmv_chart = create_nps_gmv_chart(df)
st.plotly_chart(nps_gmv_chart, use_container_width=True)

# Explanation
st.markdown("""
The scatter plot above shows the relationship between NPS (Net Promoter Score) and total GMV (Gross Merchandise Value).
The trend line indicates the general relationship between customer satisfaction and sales.
""")



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

# Create columns for weather correlation charts
col1, col2 = st.columns(2)

with col1:
    # Weather Factors Correlation with GMV
    st.subheader("Weather Factors Correlation with Total GMV")
    weather_corr_chart = create_weather_correlation_chart(df)
    st.plotly_chart(weather_corr_chart, use_container_width=True)

    # Explanation
    st.markdown("""
    This chart shows the correlation between various weather factors and total GMV:
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

# Create correlation heatmap within col2
corr_heatmap = create_correlation_heatmap(df, corr_columns)
st.plotly_chart(corr_heatmap, use_container_width=True)

# Insights section
st.subheader("Key Insights")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### Marketing Channel Effectiveness
    - **Sponsorship** has the highest investment among all channels
    - **Digital** marketing shows consistent investment over time
    - **TV** advertising has varied investment patterns
    """)

with col2:
    st.markdown("""
    ### Weather and Sales Relationship
    - Temperature shows a moderate correlation with GMV
    - Precipitation has a weak negative correlation with sales
    - Understanding these relationships can help in seasonal planning
    """)
