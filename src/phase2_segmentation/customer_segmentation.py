import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

from config.config import (
    TRANSACTIONS_CSV,
    CUSTOMER_SEGMENTS_CSV,
    KMEANS_NUM_CLUSTERS,
    KMEANS_MAX_ITERATIONS,
    KMEANS_INIT_METHOD,
    RANDOM_SEED,
)
from config.logging_config import logger_segmentation


class CustomerSegmentation:
    def __init__(self):
        self.scaler = StandardScaler()
        self.model = KMeans(
            n_clusters=KMEANS_NUM_CLUSTERS,
            init=KMEANS_INIT_METHOD,
            max_iter=KMEANS_MAX_ITERATIONS,
            random_state=RANDOM_SEED,
            n_init=10,
        )

    def create_rfm_features(self, transactions: pd.DataFrame) -> pd.DataFrame:
        transactions["transaction_date"] = pd.to_datetime(transactions["transaction_date"])
        reference_date = transactions["transaction_date"].max()

        rfm = transactions.groupby("customer_id").agg(
            recency_days=("transaction_date", lambda x: (reference_date - x.max()).days),
            frequency_purchases=("transaction_id", "count"),
            monetary_value=("total_revenue", "sum"),
            avg_transaction_value=("total_revenue", "mean"),
            distinct_categories_purchased=("product_category", "nunique"),
            total_quantity_purchased=("quantity_sold", "sum"),
        ).reset_index()

        rfm["recency_score"] = pd.qcut(
            rfm["recency_days"].rank(method="first"),
            5,
            labels=[5, 4, 3, 2, 1]
        ).astype(int)

        rfm["frequency_score"] = pd.qcut(
            rfm["frequency_purchases"].rank(method="first"),
            5,
            labels=[1, 2, 3, 4, 5]
        ).astype(int)

        rfm["monetary_score"] = pd.qcut(
            rfm["monetary_value"].rank(method="first"),
            5,
            labels=[1, 2, 3, 4, 5]
        ).astype(int)

        return rfm

    def assign_segment_label(self, row) -> str:
        if row["monetary_score"] >= 4 and row["frequency_score"] >= 4 and row["recency_score"] >= 4:
            return "VIP_ACTIVE"
        elif row["monetary_score"] >= 4:
            return "HIGH_VALUE"
        elif row["recency_score"] <= 2:
            return "AT_RISK"
        elif row["frequency_score"] <= 2:
            return "LOW_FREQUENCY"
        else:
            return "STANDARD"

    def run_segmentation_pipeline(self) -> bool:
        try:
            logger_segmentation.info("Starting Phase 2 Customer Segmentation")

            transactions = pd.read_csv(TRANSACTIONS_CSV)
            rfm = self.create_rfm_features(transactions)

            features = [
                "recency_days",
                "frequency_purchases",
                "monetary_value",
                "avg_transaction_value",
                "distinct_categories_purchased",
                "total_quantity_purchased",
            ]

            scaled_features = self.scaler.fit_transform(rfm[features])
            rfm["assigned_cluster"] = self.model.fit_predict(scaled_features)

            rfm["cluster_name"] = "Cluster " + rfm["assigned_cluster"].astype(str)
            rfm["segment_label"] = rfm.apply(self.assign_segment_label, axis=1)
            rfm["prediction_timestamp"] = pd.Timestamp.now()

            rfm.to_csv(CUSTOMER_SEGMENTS_CSV, index=False)

            logger_segmentation.info(f"Phase 2 completed. Customers segmented: {len(rfm):,}")
            print(f"Phase 2 completed successfully. File created: {CUSTOMER_SEGMENTS_CSV}")
            return True

        except Exception as e:
            logger_segmentation.error(f"Phase 2 failed: {str(e)}")
            print(f"Phase 2 failed: {str(e)}")
            return False


if __name__ == "__main__":
    segmentation = CustomerSegmentation()
    segmentation.run_segmentation_pipeline()