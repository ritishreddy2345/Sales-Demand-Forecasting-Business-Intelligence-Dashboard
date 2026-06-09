import pandas as pd

from config.config import TRANSACTIONS_CSV
from config.logging_config import logger_etl
from src.phase1_etl.data_synthesis import SyntheticDataGenerator


class ETLPipeline:
    def __init__(self):
        self.generator = SyntheticDataGenerator()

    def run_etl_pipeline(self, generate_new_data: bool = True) -> bool:
        try:
            logger_etl.info("Starting Phase 1 ETL Pipeline")

            if generate_new_data:
                df = self.generator.generate_transactions()
                is_valid, message = self.generator.validate_data_quality(df)

                if not is_valid:
                    logger_etl.error(message)
                    return False

                self.generator.export_transactions(df)

            else:
                df = pd.read_csv(TRANSACTIONS_CSV)

            logger_etl.info(f"Phase 1 completed. Records: {len(df):,}")
            print(f"Phase 1 completed successfully. File created: {TRANSACTIONS_CSV}")
            return True

        except Exception as e:
            logger_etl.error(f"Phase 1 failed: {str(e)}")
            print(f"Phase 1 failed: {str(e)}")
            return False


if __name__ == "__main__":
    pipeline = ETLPipeline()
    pipeline.run_etl_pipeline(generate_new_data=True)