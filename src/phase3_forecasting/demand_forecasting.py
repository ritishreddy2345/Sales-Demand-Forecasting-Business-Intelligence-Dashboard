import pandas as pd
import numpy as np
from datetime import timedelta
from typing import Dict, Tuple

from prophet import Prophet
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error

from config.config import (
    TRANSACTIONS_CSV,
    DAILY_SALES_CSV,
    FORECAST_RESULTS_CSV,
    MODEL_METRICS_CSV,
    FORECAST_HORIZON_DAYS,
    PRODUCT_CATEGORIES,
    PROPHET_SEASONALITY_MODE,
    PROPHET_YEARLY_SEASONALITY,
    PROPHET_WEEKLY_SEASONALITY,
    ARIMA_ORDER,
)
from config.logging_config import logger_forecasting


class DemandForecasting:
    def aggregate_daily_sales(self) -> pd.DataFrame:
        df = pd.read_csv(TRANSACTIONS_CSV)
        df["transaction_date"] = pd.to_datetime(df["transaction_date"]).dt.date

        daily = (
            df.groupby(["transaction_date", "product_category"])
            .agg(
                num_transactions=("transaction_id", "count"),
                total_quantity=("quantity_sold", "sum"),
                daily_revenue=("total_revenue", "sum"),
                avg_unit_price=("unit_price", "mean"),
            )
            .reset_index()
        )

        daily = daily.rename(columns={"transaction_date": "date"})
        daily["daily_revenue"] = daily["daily_revenue"].round(2)
        daily["avg_unit_price"] = daily["avg_unit_price"].round(2)

        daily.to_csv(DAILY_SALES_CSV, index=False)
        return daily

    def calculate_mape(self, actual, predicted) -> float:
        actual = np.array(actual)
        predicted = np.array(predicted)

        mask = actual != 0
        if mask.sum() == 0:
            return 0.0

        return np.mean(np.abs((actual[mask] - predicted[mask]) / actual[mask]))

    def train_prophet(self, category_df: pd.DataFrame, category: str) -> Tuple[pd.DataFrame, Dict]:
        prophet_df = category_df[["date", "daily_revenue"]].copy()
        prophet_df.columns = ["ds", "y"]
        prophet_df["ds"] = pd.to_datetime(prophet_df["ds"])

        train_size = int(len(prophet_df) * 0.8)
        train_df = prophet_df.iloc[:train_size]
        test_df = prophet_df.iloc[train_size:]

        model = Prophet(
            yearly_seasonality=PROPHET_YEARLY_SEASONALITY,
            weekly_seasonality=PROPHET_WEEKLY_SEASONALITY,
            daily_seasonality=False,
            seasonality_mode=PROPHET_SEASONALITY_MODE,
        )

        model.fit(train_df)

        future = model.make_future_dataframe(
            periods=len(test_df) + FORECAST_HORIZON_DAYS,
            freq="D",
        )

        forecast = model.predict(future)

        test_forecast = forecast.tail(len(test_df) + FORECAST_HORIZON_DAYS).head(len(test_df))

        y_true = test_df["y"].values
        y_pred = test_forecast["yhat"].values

        mape = self.calculate_mape(y_true, y_pred)
        mae = mean_absolute_error(y_true, y_pred)
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))

        future_forecast = forecast.tail(FORECAST_HORIZON_DAYS)[
            ["ds", "yhat", "yhat_lower", "yhat_upper"]
        ].copy()

        future_forecast["product_category"] = category
        future_forecast["model"] = "Prophet"
        future_forecast = future_forecast.rename(
            columns={
                "ds": "forecast_date",
                "yhat": "forecasted_revenue",
                "yhat_lower": "lower_bound",
                "yhat_upper": "upper_bound",
            }
        )

        metrics = {
            "product_category": category,
            "model": "Prophet",
            "mae": round(mae, 2),
            "rmse": round(rmse, 2),
            "mape": round(mape, 4),
            "accuracy": round(max(0, 1 - mape), 4),
        }

        return future_forecast, metrics

    def train_arima(self, category_df: pd.DataFrame, category: str) -> Tuple[pd.DataFrame, Dict]:
        series = category_df.sort_values("date")["daily_revenue"].astype(float).values

        train_size = int(len(series) * 0.8)
        train = series[:train_size]
        test = series[train_size:]

        model = ARIMA(train, order=ARIMA_ORDER)
        result = model.fit()

        test_pred = result.forecast(steps=len(test))

        mape = self.calculate_mape(test, test_pred)
        mae = mean_absolute_error(test, test_pred)
        rmse = np.sqrt(mean_squared_error(test, test_pred))

        final_model = ARIMA(series, order=ARIMA_ORDER).fit()
        future_pred = final_model.forecast(steps=FORECAST_HORIZON_DAYS)

        last_date = pd.to_datetime(category_df["date"]).max()
        future_dates = [
            last_date + timedelta(days=i)
            for i in range(1, FORECAST_HORIZON_DAYS + 1)
        ]

        forecast_df = pd.DataFrame({
            "forecast_date": future_dates,
            "forecasted_revenue": future_pred,
            "lower_bound": future_pred * 0.90,
            "upper_bound": future_pred * 1.10,
            "product_category": category,
            "model": "ARIMA",
        })

        metrics = {
            "product_category": category,
            "model": "ARIMA",
            "mae": round(mae, 2),
            "rmse": round(rmse, 2),
            "mape": round(mape, 4),
            "accuracy": round(max(0, 1 - mape), 4),
        }

        return forecast_df, metrics

    def run_forecasting_pipeline(self) -> bool:
        try:
            logger_forecasting.info("Starting Phase 3 Demand Forecasting")

            daily_sales = self.aggregate_daily_sales()

            all_forecasts = []
            all_metrics = []

            for category in PRODUCT_CATEGORIES:
                category_df = daily_sales[daily_sales["product_category"] == category].copy()
                category_df = category_df.sort_values("date")

                if len(category_df) < 60:
                    logger_forecasting.warning(f"Skipping {category}: not enough data")
                    continue

                try:
                    prophet_forecast, prophet_metrics = self.train_prophet(category_df, category)
                    all_forecasts.append(prophet_forecast)
                    all_metrics.append(prophet_metrics)
                    logger_forecasting.info(f"Prophet completed for {category}")
                except Exception as e:
                    logger_forecasting.warning(f"Prophet failed for {category}: {str(e)}")

                try:
                    arima_forecast, arima_metrics = self.train_arima(category_df, category)
                    all_forecasts.append(arima_forecast)
                    all_metrics.append(arima_metrics)
                    logger_forecasting.info(f"ARIMA completed for {category}")
                except Exception as e:
                    logger_forecasting.warning(f"ARIMA failed for {category}: {str(e)}")

            if not all_forecasts:
                raise ValueError("No forecasting results generated")

            forecast_results = pd.concat(all_forecasts, ignore_index=True)
            metrics_results = pd.DataFrame(all_metrics)

            forecast_results["forecasted_revenue"] = forecast_results["forecasted_revenue"].round(2)
            forecast_results["lower_bound"] = forecast_results["lower_bound"].round(2)
            forecast_results["upper_bound"] = forecast_results["upper_bound"].round(2)

            forecast_results.to_csv(FORECAST_RESULTS_CSV, index=False)
            metrics_results.to_csv(MODEL_METRICS_CSV, index=False)

            logger_forecasting.info(f"Forecast results saved to {FORECAST_RESULTS_CSV}")
            logger_forecasting.info(f"Model metrics saved to {MODEL_METRICS_CSV}")

            print(f"Phase 3 completed successfully. File created: {FORECAST_RESULTS_CSV}")
            print(f"Metrics file created: {MODEL_METRICS_CSV}")

            return True

        except Exception as e:
            logger_forecasting.error(f"Phase 3 failed: {str(e)}")
            print(f"Phase 3 failed: {str(e)}")
            return False


if __name__ == "__main__":
    forecasting = DemandForecasting()
    forecasting.run_forecasting_pipeline()