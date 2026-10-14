
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ---------------- PAGE CONFIGURATION ----------------
st.set_page_config(
    page_title="Sales & Customer Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------- LOAD DATA ----------------
DATA_PATH = Path(__file__).parent / "data" / "superstore.csv"

st.title("📊 Sales & Customer Analysis Dashboard")
st.markdown(
    "Analyze sales performance, profitability, products, "
    "and customer behavior."
)

if not DATA_PATH.exists():
    st.error(f"Dataset not found: {DATA_PATH}")
    st.info("Place superstore.csv inside the data folder.")
    st.stop()

try:
    df = pd.read_csv(DATA_PATH, encoding="utf-8-sig")
except UnicodeDecodeError:
    df = pd.read_csv(DATA_PATH, encoding="latin1")

# Clean column names and remove accidental whitespace
df.columns = df.columns.str.strip()

required_columns = [
    "Sales", "Profit", "Category", "Sub-Category",
    "Region", "Segment", "Customer Name"
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    st.error(f"Missing expected columns: {missing_columns}")
    st.write("Columns found in your file:", df.columns.tolist())
    st.stop()

# Convert numeric columns safely
for column in ["Sales", "Profit", "Quantity", "Discount"]:
    if column in df.columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")


# Convert order dates into proper datetime values
if "Order Date" in df.columns:
    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        errors="coerce"
    )



df = df.dropna(subset=["Sales", "Profit"])

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("🔎 Dashboard Filters")

filtered_df = df.copy()


# Date range filter
if "Order Date" in df.columns:
    valid_dates = df["Order Date"].dropna()

    if not valid_dates.empty:
        min_date = valid_dates.min().date()
        max_date = valid_dates.max().date()

        st.sidebar.subheader("📅 Order Date Range")

        selected_dates = st.sidebar.date_input(
            "Select date range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )

        if isinstance(selected_dates, (tuple, list)):
            if len(selected_dates) == 2:
                start_date, end_date = selected_dates

                filtered_df = filtered_df[
                    filtered_df["Order Date"].dt.date.between(
                        start_date, end_date
                    )
                ]


if "Region" in df.columns:
    regions = sorted(df["Region"].dropna().unique().tolist())
    selected_regions = st.sidebar.multiselect(
        "Select Region",
        regions,
        default=regions
    )
    filtered_df = filtered_df[
        filtered_df["Region"].isin(selected_regions)
    ]

if "Category" in df.columns:
    categories = sorted(df["Category"].dropna().unique().tolist())
    selected_categories = st.sidebar.multiselect(
        "Select Category",
        categories,
        default=categories
    )
    filtered_df = filtered_df[
        filtered_df["Category"].isin(selected_categories)
    ]

if "Segment" in df.columns:
    segments = sorted(df["Segment"].dropna().unique().tolist())
    selected_segments = st.sidebar.multiselect(
        "Select Customer Segment",
        segments,
        default=segments
    )
    filtered_df = filtered_df[
        filtered_df["Segment"].isin(selected_segments)
    ]

# ---------------- KPI METRICS ----------------
st.subheader("📌 Business Overview")

if filtered_df.empty:
    st.warning("No data matches your filters. Select different filters.")
    st.stop()

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = (
    filtered_df["Order ID"].nunique()
    if "Order ID" in filtered_df.columns
    else len(filtered_df)
)
total_customers = (
    filtered_df["Customer ID"].nunique()
    if "Customer ID" in filtered_df.columns
    else filtered_df["Customer Name"].nunique()
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Sales", f"${total_sales:,.2f}")
col2.metric("📈 Total Profit", f"${total_profit:,.2f}")
col3.metric("🛒 Orders", f"{total_orders:,}")
col4.metric("👥 Customers", f"{total_customers:,}")

# ---------------- CHART 1: SALES BY CATEGORY ----------------
st.subheader("📦 Sales by Product Category")

category_sales = (
    filtered_df.groupby("Category", as_index=False)["Sales"]
    .sum()
    .sort_values("Sales", ascending=False)
)

fig_category = px.bar(
    category_sales,
    x="Category",
    y="Sales",
    color="Category",
    title="Total Sales by Category",
    text_auto=".2s",
    template="plotly_white"
)

fig_category.update_layout(showlegend=False)
st.plotly_chart(fig_category, use_container_width=True)

# ---------------- CHART 2: SALES AND PROFIT BY REGION ----------------
st.subheader("🌎 Regional Performance")

region_data = (
    filtered_df.groupby("Region", as_index=False)[["Sales", "Profit"]]
    .sum()
)

fig_region = px.bar(
    region_data,
    x="Region",
    y=["Sales", "Profit"],
    barmode="group",
    title="Sales vs Profit by Region",
    template="plotly_white"
)

st.plotly_chart(fig_region, use_container_width=True)


# ---------------- CHART 3: MONTHLY SALES TREND ----------------
if "Order Date" in filtered_df.columns:
    st.subheader("📅 Monthly Sales Trend")

    dated_df = filtered_df.dropna(subset=["Order Date"]).copy()

    if not dated_df.empty:
        dated_df["Month"] = (
            dated_df["Order Date"]
            .dt.to_period("M")
            .dt.to_timestamp()
        )

        monthly_sales = (
            dated_df.groupby("Month", as_index=False)["Sales"]
            .sum()
            .sort_values("Month")
        )

        fig_monthly = px.line(
            monthly_sales,
            x="Month",
            y="Sales",
            markers=True,
            title="How Sales Change Month by Month",
            template="plotly_white"
        )

        fig_monthly.update_layout(
            xaxis_title="Month",
            yaxis_title="Total Sales ($)"
        )

        st.plotly_chart(
            fig_monthly,
            use_container_width=True
        )
    else:
        st.warning("No valid order dates are available.")


# ---------------- CHART 3: TOP 10 PRODUCTS ----------------
st.subheader("🏆 Top 10 Sub-Categories by Sales")

product_sales = (
    filtered_df.groupby("Sub-Category", as_index=False)["Sales"]
    .sum()
    .sort_values("Sales", ascending=False)
    .head(10)
)

fig_products = px.bar(
    product_sales.sort_values("Sales"),
    x="Sales",
    y="Sub-Category",
    orientation="h",
    color="Sales",
    title="Top 10 Sub-Categories",
    text_auto=".2s",
    color_continuous_scale="Viridis",
    template="plotly_white"
)

st.plotly_chart(fig_products, use_container_width=True)


# ---------------- LOSS-MAKING SUB-CATEGORIES ----------------
st.subheader("⚠️ Products with the Highest Losses")

subcategory_profit = (
    filtered_df.groupby("Sub-Category", as_index=False)["Profit"]
    .sum()
    .sort_values("Profit")
)

loss_making = subcategory_profit[
    subcategory_profit["Profit"] < 0
].head(10)

if not loss_making.empty:
    fig_losses = px.bar(
        loss_making,
        x="Profit",
        y="Sub-Category",
        orientation="h",
        color="Profit",
        color_continuous_scale="Reds_r",
        title="Sub-Categories with Negative Total Profit",
        template="plotly_white"
    )

    st.plotly_chart(
        fig_losses,
        use_container_width=True
    )
else:
    st.success("No loss-making sub-categories in the selected data.")


# ---------------- CHART 4: CUSTOMER SEGMENTS ----------------
st.subheader("👥 Sales by Customer Segment")

segment_sales = (
    filtered_df.groupby("Segment", as_index=False)["Sales"]
    .sum()
)

fig_segment = px.pie(
    segment_sales,
    names="Segment",
    values="Sales",
    title="Sales Contribution by Segment",
    hole=0.45
)

st.plotly_chart(fig_segment, use_container_width=True)


# ---------------- EXECUTIVE BUSINESS INSIGHTS ----------------
st.subheader("💡 Executive Business Insights")

# 1. Overall business performance
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()

profit_margin = (
    total_profit / total_sales * 100
    if total_sales != 0
    else 0
)

insight_col1, insight_col2 = st.columns(2)

with insight_col1:
    st.markdown("### 📊 Overall Performance")
    st.write(f"**Total sales:** ${total_sales:,.2f}")
    st.write(f"**Total profit:** ${total_profit:,.2f}")
    st.write(f"**Profit margin:** {profit_margin:.2f}%")

    if total_profit < 0:
        st.warning(
            "The selected transactions show an overall loss. "
            "Investigate product costs, discounts, and sales mix."
        )
    elif total_profit == 0:
        st.info("The selected transactions break even overall.")
    else:
        st.success(
            "The selected transactions are profitable overall."
        )

# 2. Category performance
with insight_col2:
    st.markdown("### 📦 Category Performance")

    category_insights = (
        filtered_df.groupby("Category", as_index=False)
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum")
        )
    )

    if not category_insights.empty:
        best_sales_category = category_insights.loc[
            category_insights["Sales"].idxmax()
        ]

        best_profit_category = category_insights.loc[
            category_insights["Profit"].idxmax()
        ]

        worst_profit_category = category_insights.loc[
            category_insights["Profit"].idxmin()
        ]

        st.write(
            f"**Highest sales:** {best_sales_category['Category']} "
            f"(${best_sales_category['Sales']:,.2f})"
        )

        st.write(
            f"**Highest total profit:** {best_profit_category['Category']} "
            f"(${best_profit_category['Profit']:,.2f})"
        )

        st.write(
            f"**Lowest total profit:** {worst_profit_category['Category']} "
            f"(${worst_profit_category['Profit']:,.2f})"
        )

# 3. Regional performance
if "Region" in filtered_df.columns:
    st.markdown("### 🌎 Regional Performance")

    region_insights = (
        filtered_df.groupby("Region", as_index=False)
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum")
        )
    )

    if not region_insights.empty:
        best_region = region_insights.loc[
            region_insights["Sales"].idxmax()
        ]

        lowest_profit_region = region_insights.loc[
            region_insights["Profit"].idxmin()
        ]

        col_region1, col_region2 = st.columns(2)

        col_region1.metric(
            "Highest-sales region",
            best_region["Region"],
            f"${best_region['Sales']:,.2f}"
        )

        col_region2.metric(
            "Lowest-profit region",
            lowest_profit_region["Region"],
            f"${lowest_profit_region['Profit']:,.2f}"
        )

# 4. Suggested follow-up investigation
st.markdown("### 🎯 Recommended Investigation")

if total_profit < 0:
    st.write(
        "- Review loss-making products and investigate their discounts, "
        "costs, and regional performance."
    )
elif profit_margin < 10:
    st.write(
        "- Investigate low-margin transactions and determine whether "
        "pricing, discounting, or product mix contributes to the result."
    )
else:
    st.write(
        "- Compare profitability across products, customers, and regions "
        "to identify opportunities for sustainable growth."
    )

st.caption(
    "Insights are calculated from the selected dataset and filters. "
    "Recommendations are hypotheses to investigate, not proof of causation."
)

# ---------------- DATA PREVIEW ----------------
with st.expander("🔍 Explore the Dataset"):
    st.write(f"Rows: {len(filtered_df):,}")
    st.dataframe(filtered_df.head(100), use_container_width=True)

    csv_data = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download Filtered Data as CSV",
        data=csv_data,
        file_name="filtered_sales_data.csv",
        mime="text/csv"
    )

st.caption("Sales & Customer Analysis Dashboard | Built with Python, Pandas, Plotly and Streamlit")
