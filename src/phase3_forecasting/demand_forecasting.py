"""
PHASE 3: Time-Series Demand Forecasting with Facebook Prophet & ARIMA
Includes data preparation, model training, and 90-day forecast
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Tuple, Dict
import logging
from prophet import Prophet
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_percentage_error, mean_absolute_error, mean_squared_error
from config.logging_config import logger_forecasting
from config.config import (
    GCP_PROJECT_ID,
    GCP_DATASET_ID,
    FORECAST_HORIZON_DAYS,
    PROPHET_SEASONALITY_MODE,
    PROPHET_YEARLY_SEASONALITY,
    PROPHET_WEEKLY_SEASONALITY,
    ARIMA_ORDER,
    ARIMA_SEASONAL_ORDER,
    TARGET_MAPE,
    PRODUCT_CATEGORIES,
    OUTPUT_DIR
)
from src.bigquery_utils import BigQueryManager


class TimeSeriesDataPreparation:
    """Prepares time-series data from BigQuery for forecasting"""
    
    def __init__(self, project_id: str = GCP_PROJECT_ID):
        """Initialize data preparation"""
        self.project_id = project_id
        self.dataset_id = GCP_DATASET_ID
        self.bq_manager = BigQueryManager(project_id)
        logger_forecasting.info("TimeSeriesDataPreparation initialized")
    
    def extract_daily_sales_by_category(self) -> Tuple[bool, Dict[str, pd.DataFrame]]:
        """
        Extract daily sales aggregated by product category from BigQuery
        
        Returns:
            Tuple of (success: bool, category_data_dict: Dict)
        """
        try:
            logger_forecasting.info("=" * 80)
            logger_forecasting.info("EXTRACTING DAILY SALES BY CATEGORY")
            logger_forecasting.info("=" * 80)
            
            query = f"""
            SELECT
                DATE(transaction_date) as date,
                product_category,
                COUNT(DISTINCT transaction_id) as num_transactions,
                SUM(quantity_sold) as total_quantity,
                ROUND(SUM(total_revenue), 2) as daily_revenue,
                ROUND(AVG(unit_price), 2) as avg_unit_price,
                ROUND(AVG(total_revenue), 2) as avg_transaction_value
            FROM `{self.project_id}.{self.dataset_id}.transactions`
            WHERE transaction_date IS NOT NULL
            GROUP BY date, product_category
            ORDER BY date, product_category
            """
            
            df = self.bq_manager.execute_query(query, timeout_seconds=300)
            
            if df is None or len(df) == 0:
                msg = "No data extracted from BigQuery"
                logger_forecasting.error(msg)
                return False, {}
            
            logger_forecasting.info(f"✓ Extracted {len(df)} daily sales records")
            logger_forecasting.info(f"  - Date range: {df['date'].min()} to {df['date'].max()}")
            logger_forecasting.info(f"  - Categories: {df['product_category'].nunique()}")
            
            # Split by category
            category_data = {}
            for category in PRODUCT_CATEGORIES:
                category_df = df[df['product_category'] == category].copy()
                category_df = category_df.sort_values('date').reset_index(drop=True)
                
                if len(category_df) > 0:
                    category_data[category] = category_df
                    logger_forecasting.info(
                        f"  - {category}: {len(category_df)} days, "
                        f"avg daily revenue: ${category_df['daily_revenue'].mean():.2f}"
                    )
            
            return True, category_data
        
        except Exception as e:
            error_msg = f"Error extracting daily sales: {str(e)}"
            logger_forecasting.error(error_msg)
            return False, {}
    
    def prepare_prophet_data(self, df: pd.DataFrame, category: str) -> pd.DataFrame:
        """
        Prepare data in Prophet format (ds, y columns)
        
        Args:
            df: DataFrame with date and daily_revenue columns
            category: Product category name
        
        Returns:
            DataFrame formatted for Prophet
        """
        prophet_df = pd.DataFrame({
            'ds': pd.to_datetime(df['date']),
            'y': df['daily_revenue'].astype(float),
            'category': category
        })
        
        return prophet_df.sort_values('ds').reset_index(drop=True)
    
    def prepare_arima_data(self, df: pd.DataFrame) -> np.ndarray:
        """
        Prepare time-series data for ARIMA
        
        Args:
            df: DataFrame with daily_revenue column
        
        Returns:
            NumPy array of revenue values
        """
        return df['daily_revenue'].astype(float).values


class ForecastingModels:
    """Implements Prophet and ARIMA forecasting models"""
    
    def __init__(self):
        """Initialize forecasting models"""
        logger_forecasting.info("ForecastingModels initialized")
    
    def fit_prophet_model(
        self,
        df: pd.DataFrame,
        category: str,
        forecast_horizon: int = FORECAST_HORIZON_DAYS
    ) -> Tuple[bool, Prophet, pd.DataFrame]:
        """
        Fit Facebook Prophet model
        
        Args:
            df: DataFrame with 'ds' and 'y' columns
            category: Product category name
            forecast_horizon: Number of days to forecast
        
        Returns:
            Tuple of (success, model, forecast_df)
        """
        try:
            logger_forecasting.info(f"\n  Training Prophet for {category}...")
            
            # Suppress Prophet's verbose output
            with logging.getLogger("cmdstanpy").propagate as _:
                model = Prophet(
                    yearly_seasonality=PROPHET_YEARLY_SEASONALITY,
                    weekly_seasonality=PROPHET_WEEKLY_SEASONALITY,
                    daily_seasonality=False,
                    seasonality_mode=PROPHET_SEASONALITY_MODE,
                    interval_width=0.95,
                    changepoint_prior_scale=0.05
                )
                
                # Fit model
                model.fit(df)
            
            # Create future dataframe
            future = model.make_future_dataframe(periods=forecast_horizon, freq='D')
            forecast = model.predict(future)
            
            logger_forecasting.info(f"    ✓ Prophet model fitted for {category}")
            
            return True, model, forecast
        
        except Exception as e:
            error_msg = f"Error fitting Prophet for {category}: {str(e)}"
            logger_forecasting.error(error_msg)
            return False, None, None
    
    def fit_arima_model(
        self,
        ts_data: np.ndarray,
        category: str,
        order: Tuple = ARIMA_ORDER,
        seasonal_order: Tuple = ARIMA_SEASONAL_ORDER,
        forecast_horizon: int = FORECAST_HORIZON_DAYS
    ) -> Tuple[bool, ARIMA, np.ndarray]:
        """
        Fit ARIMA model
        
        Args:
            ts_data: Time-series array
            category: Product category name
            order: ARIMA order (p, d, q)
            seasonal_order: Seasonal ARIMA order (P, D, Q, s)
            forecast_horizon: Number of days to forecast
        
        Returns:
            Tuple of (success, model, forecast_array)
        """
        try:
            logger_forecasting.info(f"  Training ARIMA{order} for {category}...")
            
            # Fit ARIMA model
            model = ARIMA(
                ts_data,
                order=order,
                seasonal_order=seasonal_order,
                enforce_stationarity=False,
                enforce_invertibility=False
            )
            
            results = model.fit()
            
            # Forecast
            forecast = results.get_forecast(steps=forecast_horizon).predicted_mean.values
            
            logger_forecasting.info(f"    ✓ ARIMA model fitted for {category}")
            
            return True, results, forecast
        
        except Exception as e:
            error_msg = f"Error fitting ARIMA for {category}: {str(e)}"
            logger_forecasting.error(error_msg)
            return False, None, None


class ForecastEvaluation:
    """Evaluates forecast accuracy"""
    
    @staticmethod
    def calculate_mape(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """
        Calculate Mean Absolute Percentage Error
        
        Args:
            y_true: Actual values
            y_pred: Predicted values
        
        Returns:
            MAPE value (0-1 scale)
        """
        # Filter out zero values to avoid division by zero
        mask = y_true != 0
        y_true_filtered = y_true[mask]
        y_pred_filtered = y_pred[mask]
        
        if len(y_true_filtered) == 0:
            return 0
        
        mape = np.mean(np.abs((y_true_filtered - y_pred_filtered) / y_true_filtered))
        return mape
    
    @staticmethod
    def evaluate_forecast(
        y_true: np.ndarray,
        y_pred: np.ndarray,
        category: str
    ) -> Dict[str, float]:
        """
        Comprehensive forecast evaluation
        
        Args:
            y_true: Actual values
            y_pred: Predicted values
            category: Category name for logging
        
        Returns:
            Dictionary of metrics
        """
        metrics = {
            'category': category,
            'mae': mean_absolute_error(y_true, y_pred),
            'mse': mean_squared_error(y_true, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_true, y_pred)),
            'mape': ForecastEvaluation.calculate_mape(y_true, y_pred),
            'accuracy': 1 - ForecastEvaluation.calculate_mape(y_true, y_pred)
        }
        
        return metrics
    
    @staticmethod
    def print_evaluation_report(metrics: Dict[str, float], target_mape: float = TARGET_MAPE):
        """Print formatted evaluation report"""
        logger_forecasting.info(
            f"\n  Evaluation Metrics for {metrics['category']}:\n"
            f"    - MAE:      ${metrics['mae']:.2f}\n"
            f"    - RMSE:     ${metrics['rmse']:.2f}\n"
            f"    - MAPE:     {metrics['mape']:.4f} ({metrics['mape']*100:.2f}%)\n"
            f"    - Accuracy: {metrics['accuracy']:.4f} ({metrics['accuracy']*100:.2f}%)\n"
            f"    - Target:   {target_mape:.4f} ({target_mape*100:.2f}%)\n"
            f"    - Status:   {'✓ PASS' if metrics['accuracy'] >= target_mape else '✗ MISS'}"
        )


class DemandForecasting:
    """Main forecasting orchestrator"""
    
    def __init__(self, project_id: str = GCP_PROJECT_ID):
        """Initialize forecasting"""
        self.project_id = project_id
        self.data_prep = TimeSeriesDataPreparation(project_id)
        self.models = ForecastingModels()
        self.eval = ForecastEvaluation()
        logger_forecasting.info("DemandForecasting initialized")
    
    def run_forecasting_pipeline(self) -> Tuple[bool, Dict]:
        """
        Execute complete forecasting pipeline
        
        Returns:
            Tuple of (success: bool, results_dict: Dict)
        """
        try:
            logger_forecasting.info("\n" + "🔮 " * 20)
            logger_forecasting.info("STARTING DEMAND FORECASTING PIPELINE")
            logger_forecasting.info("🔮 " * 20 + "\n")
            
            # Step 1: Extract data
            logger_forecasting.info("STEP 1: EXTRACTING TIME-SERIES DATA")
            success, category_data = self.data_prep.extract_daily_sales_by_category()
            if not success:
                logger_forecasting.error("Data extraction failed")
                return False, {}
            
            results = {
                'prophet_results': {},
                'arima_results': {},
                'evaluation_metrics': {}
            }
            
            # Step 2: Train models for each category
            logger_forecasting.info("\n" + "=" * 80)
            logger_forecasting.info("STEP 2: TRAINING FORECASTING MODELS")
            logger_forecasting.info("=" * 80)
            
            for category, df in category_data.items():
                logger_forecasting.info(f"\n📊 Processing {category} ({len(df)} days of data)...")
                
                # Prepare data
                prophet_df = self.data_prep.prepare_prophet_data(df, category)
                arima_data = self.data_prep.prepare_arima_data(df)
                
                # Split: 80% train, 20% test
                train_size = int(len(df) * 0.8)
                df_train = df.iloc[:train_size]
                df_test = df.iloc[train_size:]
                
                # PROPHET
                logger_forecasting.info(f"  Training Prophet...")
                success_p, prophet_model, prophet_forecast = self.models.fit_prophet_model(
                    self.data_prep.prepare_prophet_data(df_train, category),
                    category,
                    FORECAST_HORIZON_DAYS
                )
                
                if success_p:
                    # Get test period predictions
                    test_forecast = prophet_forecast[prophet_forecast['ds'] < df_test['date'].max()]
                    if len(test_forecast) > 0 and len(df_test) > 0:
                        prophet_pred = test_forecast['yhat'].values[-len(df_test):]
                        prophet_metrics = self.eval.evaluate_forecast(
                            df_test['daily_revenue'].values,
                            prophet_pred,
                            category
                        )
                        results['evaluation_metrics'][f"{category}_prophet"] = prophet_metrics
                        self.eval.print_evaluation_report(prophet_metrics)
                    
                    results['prophet_results'][category] = {
                        'model': prophet_model,
                        'forecast': prophet_forecast[-FORECAST_HORIZON_DAYS:]
                    }
                
                # ARIMA
                logger_forecasting.info(f"  Training ARIMA...")
                success_a, arima_model, arima_forecast = self.models.fit_arima_model(
                    arima_data[:train_size],
                    category,
                    ARIMA_ORDER,
                    ARIMA_SEASONAL_ORDER,
                    FORECAST_HORIZON_DAYS
                )
                
                if success_a:
                    # Get test period predictions
                    if len(arima_forecast) >= len(df_test):
                        arima_pred = arima_forecast[-len(df_test):]
                        arima_metrics = self.eval.evaluate_forecast(
                            df_test['daily_revenue'].values,
                            arima_pred,
                            category
                        )
                        results['evaluation_metrics'][f"{category}_arima"] = arima_metrics
                        self.eval.print_evaluation_report(arima_metrics)
                    
                    results['arima_results'][category] = {
                        'model': arima_model,
                        'forecast': arima_forecast
                    }
            
            # Step 3: Generate summary
            logger_forecasting.info("\n" + "=" * 80)
            logger_forecasting.info("FORECASTING PIPELINE SUMMARY")
            logger_forecasting.info("=" * 80)
            
            logger_forecasting.info(f"Categories forecasted: {len(results['prophet_results'])}")
            logger_forecasting.info(f"Prophet models: {len(results['prophet_results'])}")
            logger_forecasting.info(f"ARIMA models: {len(results['arima_results'])}")
            
            # Calculate average accuracy
            if results['evaluation_metrics']:
                accuracies = [m['accuracy'] for m in results['evaluation_metrics'].values()]
                avg_accuracy = np.mean(accuracies)
                logger_forecasting.info(f"\nAverage forecast accuracy: {avg_accuracy:.4f} ({avg_accuracy*100:.2f}%)")
                logger_forecasting.info(f"Target accuracy: {TARGET_MAPE:.4f} ({TARGET_MAPE*100:.2f}%)")
                logger_forecasting.info(f"Status: {'✓ TARGET MET' if avg_accuracy >= TARGET_MAPE else '✗ TARGET MISSED'}")
            
            logger_forecasting.info("\n" + "✓ " * 20)
            logger_forecasting.info("DEMAND FORECASTING PIPELINE COMPLETED")
            logger_forecasting.info("✓ " * 20)
            
            return True, results
        
        except Exception as e:
            error_msg = f"Fatal error in forecasting pipeline: {str(e)}"
            logger_forecasting.error(error_msg)
            return False, {}


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    import sys
    import time
    
    # Initialize forecasting
    forecasting = DemandForecasting()
    
    # Run pipeline
    start_time = time.time()
    success, results = forecasting.run_forecasting_pipeline()
    elapsed_time = time.time() - start_time
    
    print("\n" + "=" * 80)
    print("PHASE 3 DEMAND FORECASTING EXECUTION SUMMARY")
    print("=" * 80)
    print(f"Status: {'✓ SUCCESS' if success else '✗ FAILED'}")
    print(f"Execution time: {elapsed_time:.2f} seconds ({elapsed_time/60:.2f} minutes)")
    print("=" * 80)
    
    sys.exit(0 if success else 1)
