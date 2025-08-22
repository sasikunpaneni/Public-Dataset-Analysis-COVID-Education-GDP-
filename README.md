
# Public Dataset Analysis – COVID, Education & GDP (Python | Power BI)

Analyze global health and education trends by merging **Our World in Data (COVID)**, **World Bank (GDP)**, and **UNDP (Education Index)** datasets.

## Tools Used
- Python (pandas, matplotlib, Prophet for forecasting)
- Power BI (interactive dashboards)
- Data sources: Our World in Data, World Bank, UNDP

## Key Features
- Cleaned and merged multi-source datasets.
- Interactive Power BI dashboard with continent/year/income filters.
- Correlation analysis between GDP and Education Index (Pearson r).
- Forecasting COVID trends using Prophet.

## Key Insight
*Education Index improved in 60% of developing countries post-2015.*

## Repository Structure
```
public-dataset-analysis/
├── README.md
├── requirements.txt
├── data/
│   ├── raw/
│   └── processed/
├── scripts/
│   ├── 01_clean_merge.py
│   ├── 02_analysis.py
│   └── 03_forecasting_prophet.py
├── powerbi/
│   └── measures_dax.txt
└── images/
    └── dashboard_screenshot.png
```
