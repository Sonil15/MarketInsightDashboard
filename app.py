import streamlit as st
from utils import load_merged_data

# Set page configuration
st.set_page_config(
    page_title="GMV & KPI Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add CSS for rounded corner boxes with blue color scheme
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
        background-color: #f5f9ff;
        padding-top: 2rem;
    }
    
    /* Styling for all chart, text and number containers */
    div.stPlotlyChart, div.stText, div.stMarkdown, div.stNumber, div.stDataFrame, div.stSelectbox, div.stMultiselect {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #bbdefb;
        box-shadow: 0 2px 8px rgba(13, 71, 161, 0.1);
        margin-bottom: 20px;
    }
    
    /* Metric value styling */
    div[data-testid="stMetricValue"] {
        background-color: #e3f2fd;
        padding: 15px 20px;
        border-radius: 10px;
        border: 1px solid #64b5f6;
        box-shadow: 0 2px 8px rgba(13, 71, 161, 0.1);
        color: #0d47a1;
        font-weight: bold;
    }
    
    /* Header styling */
    div[data-testid="stHeader"] {
        background-color: transparent;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #e3f2fd;
        border-right: 1px solid #bbdefb;
    }
    
    /* Headings styling */
    h1, h2, h3 {
        color: #0d47a1 !important;
    }
    
    /* Button styling */
    button[kind="primary"] {
        background-color: #1e88e5;
        border: 1px solid #1976d2;
    }
    
    /* Make tabs stand out with blue */
    button[data-baseweb="tab"] {
        background-color: #bbdefb;
        border-radius: 5px 5px 0 0;
    }
    
    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #64b5f6;
        color: white;
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
