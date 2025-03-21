import streamlit as st
from utils import load_merged_data

# Set page configuration
st.set_page_config(
    page_title="GMV & KPI Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add CSS for rounded corner boxes
st.markdown("""
<style>
    div.stPlotlyChart, div.stText, div.stMarkdown, div.stNumber, div.stDataFrame, div.stSelectbox, div.stMultiselect {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #e6e6e6;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        margin-bottom: 15px;
    }
    div[data-testid="stMetricValue"] {
        background-color: #f8f9fa;
        padding: 15px 20px;
        border-radius: 10px;
        border: 1px solid #e6e6e6;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    div[data-testid="stHeader"] {
        background-color: transparent;
    }
    div.block-container {
        padding-top: 2rem;
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

# Create metrics for top KPIs
col1, col2, col3 = st.columns(3)

with col1:
    total_gmv = df['Total_GMV'].sum()
    st.metric("Total GMV", f"${total_gmv:,.2f}")

with col2:
    avg_roas = df['ROI'].mean()
    st.metric("Average ROAS", f"{avg_roas:.2f}")

with col3:
    avg_nps = df['NPS'].mean()
    st.metric("Average NPS", f"{avg_nps:.2f}")

# Quick tips for navigation
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
