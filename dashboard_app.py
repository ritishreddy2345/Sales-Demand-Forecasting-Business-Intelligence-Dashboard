import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sales Demand Forecasting BI Dashboard", layout="wide")

st.title("Sales Demand Forecasting & Business Intelligence Dashboard")

transactions = pd.read_csv("output/transactions.csv")
segments = pd.read_csv("output/customer_segments.csv")
daily_sales = pd.read_csv("output/daily_sales_aggregated.csv")
forecast = pd.read_csv("output/forecast_results.csv")
metrics = pd.read_csv("output/forecast_model_metrics.csv")

transactions["transaction_date"] = pd.to_datetime(transactions["transaction_date"])
daily_sales["date"] = pd.to_datetime(daily_sales["date"])
forecast["forecast_date"] = pd.to_datetime(forecast["forecast_date"])

tab1, tab2, tab3 = st.tabs([
    "Revenue Trends",
    "Demand Forecasting",
    "Customer Segmentation"
])

with tab1:
    st.header("Revenue Trends")

    total_revenue = transactions["total_revenue"].sum()
    total_transactions = transactions["transaction_id"].count()
    avg_order_value = transactions["total_revenue"].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Revenue", f"${total_revenue:,.2f}")
    col2.metric("Total Transactions", f"{total_transactions:,}")
    col3.metric("Average Order Value", f"${avg_order_value:,.2f}")

    revenue_trend = daily_sales.groupby("date")["daily_revenue"].sum().reset_index()

    fig = px.line(
        revenue_trend,
        x="date",
        y="daily_revenue",
        title="Daily Revenue Trend"
    )
    st.plotly_chart(fig, use_container_width=True)

    category_revenue = transactions.groupby("product_category")["total_revenue"].sum().reset_index()
    fig2 = px.bar(
        category_revenue,
        x="product_category",
        y="total_revenue",
        title="Revenue by Product Category"
    )
    st.plotly_chart(fig2, use_container_width=True)

with tab2:
    st.header("Demand Forecasting")

    selected_category = st.selectbox(
        "Select Product Category",
        sorted(forecast["product_category"].unique())
    )

    category_forecast = forecast[forecast["product_category"] == selected_category]

    fig3 = px.line(
        category_forecast,
        x="forecast_date",
        y="forecasted_revenue",
        color="model",
        title=f"90-Day Forecast for {selected_category}"
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Forecast Model Metrics")
    st.dataframe(metrics)

with tab3:
    st.header("Customer Segmentation")

    total_customers = segments["customer_id"].nunique()
    vip_customers = len(segments[segments["segment_label"] == "VIP_ACTIVE"])
    high_value = len(segments[segments["segment_label"] == "HIGH_VALUE"])
    at_risk = len(segments[segments["segment_label"] == "AT_RISK"])

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Customers", f"{total_customers:,}")
    col2.metric("VIP Active", f"{vip_customers:,}")
    col3.metric("High Value", f"{high_value:,}")
    col4.metric("At Risk", f"{at_risk:,}")

    segment_counts = segments["segment_label"].value_counts().reset_index()
    segment_counts.columns = ["segment_label", "count"]

    fig4 = px.pie(
        segment_counts,
        names="segment_label",
        values="count",
        title="Customer Segment Distribution"
    )
    st.plotly_chart(fig4, use_container_width=True)

    fig5 = px.scatter(
        segments,
        x="frequency_purchases",
        y="monetary_value",
        color="segment_label",
        title="Customer Frequency vs Monetary Value"
    )
    st.plotly_chart(fig5, use_container_width=True)

    st.subheader("Customer Segmentation Data")
    st.dataframe(segments.head(100))