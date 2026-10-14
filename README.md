# Sales & Customer Analysis Dashboard

An interactive business analytics dashboard built with Python, Pandas, Plotly, and Streamlit to explore sales performance, customer behavior, profitability, and product trends.

## Features

- **Business KPIs:** Total sales, total profit, orders, and unique customers.
- **Interactive filters:** Filter by region, product category, customer segment, and order date.
- **Sales trends:** Analyze monthly sales performance.
- **Product analysis:** Compare category sales and investigate loss-making sub-categories.
- **Customer analysis:** Identify customers with the highest sales.
- **Profitability analysis:** Explore discount and profit relationships.
- **Data quality:** Inspect missing values and duplicate records.
- **Executive insights:** Generate summaries from the selected data.
- **Data export:** Download filtered records as CSV.

## Technology Stack

- Python
- Pandas
- Plotly
- Streamlit

## Project Structure

```text
Sales-Customer-Dashboard/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── data/
    └── superstore.csv
```

## Installation

1. Clone this repository:

   ```bash
   git clone <YOUR_GITHUB_REPOSITORY_URL>
   cd Sales-Customer-Dashboard
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Place the dataset at `data/superstore.csv`.

5. Run the dashboard:

   ```bash
   streamlit run app.py
   ```

6. Open `http://localhost:8501` in your browser.

## Dataset

This project uses the Sample Superstore dataset. Review the dataset source and its applicable terms before redistribution.

Dataset source: https://www.kaggle.com/datasets/vivek468/superstore-dataset-final

## Analytical Objectives

- Compare sales and profit across categories and regions.
- Identify high-sales customers and loss-making product sub-categories.
- Examine monthly sales patterns.
- Explore associations between discounts and profitability.
- Convert analytical findings into business questions and recommendations.

## Limitations

The findings are descriptive and depend on the selected dataset and filters. Correlations do not establish causation, and historical sales patterns do not guarantee future performance.

## Future Improvements

- Add unit tests and automated data validation.
- Improve accessibility and dashboard formatting.
- Add forecasting with a suitable time-series evaluation method.
- Deploy the dashboard online.

## Author

Amlan Mishra