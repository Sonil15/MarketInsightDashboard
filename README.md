# Market Insight Dashboard

A comprehensive Streamlit-based dashboard for analyzing market performance, KPIs, and budget optimization.

## Overview

This dashboard provides insights into:
- GMV (Gross Merchandise Value) analysis
- Key Performance Indicators (KPIs)
- Marketing budget optimization
- Product category performance
- Customer satisfaction metrics

## Features

- **Interactive Visualizations**: Dynamic charts and graphs using Plotly
- **Multi-page Interface**: Organized sections for different types of analysis
- **Real-time Data Processing**: Efficient data handling with pandas
- **Responsive Design**: Mobile-friendly interface
- **Custom Styling**: Modern and professional UI

## Pages

1. **Overview**
   - Quick summary of key metrics
   - High-level performance indicators
   - Recent trends and changes

2. **Exploratory Data Analysis**
   - Detailed data exploration
   - Correlation analysis
   - Pattern identification

3. **KPI Analysis**
   - Performance metrics tracking
   - Trend analysis
   - Goal tracking

4. **Budget Optimization**
   - Marketing spend analysis
   - ROI calculations
   - Budget allocation recommendations

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/MarketInsightDashboard.git
cd MarketInsightDashboard
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

## Project Structure

```
MarketInsightDashboard/
├── app.py                 # Main application file
├── utils.py              # Utility functions
├── requirements.txt      # Project dependencies
├── pages/               # Dashboard pages
│   ├── 1_Overview.py
│   ├── 2_Exploratory_Data_Analysis.py
│   ├── 3_KPI_Analysis.py
│   └── 4_Budget_Optimization.py
├── attached_assets/     # Data files
└── dashboard_images/    # Dashboard screenshots
```

## Dependencies

- Python 3.11+
- Streamlit
- Pandas
- NumPy
- Plotly
- Statsmodels

## Usage

1. Launch the application using the command above
2. Navigate through different pages using the sidebar
3. Interact with charts and filters to analyze data
4. Export insights and reports as needed

## Screenshots

### Overview Page
![Overview Page](dashboard_images/1.%20Overview.png)

### Exploratory Data Analysis
![Exploratory Data Analysis](dashboard_images/2.%20Exploratory%20Data%20Analysis.png)

### KPI Analysis
![KPI Analysis](dashboard_images/3.%20KPI%20Analysis.png)

### Budget Optimization
![Budget Optimization](dashboard_images/4.%20Budget%20Optimization.png)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Data provided by [Your Data Source]
- Built with Streamlit
- Visualizations powered by Plotly 