import sys
import time

from src.phase1_etl.etl_pipeline import ETLPipeline
from src.phase2_segmentation.customer_segmentation import CustomerSegmentation
from src.phase3_forecasting.demand_forecasting import DemandForecasting
from src.phase4_dashboard.dashboard_blueprint import DashboardBlueprint


def run_phase_1():
    pipeline = ETLPipeline()
    return pipeline.run_etl_pipeline(generate_new_data=True)


def run_phase_2():
    segmentation = CustomerSegmentation()
    return segmentation.run_segmentation_pipeline()


def run_phase_3():
    forecasting = DemandForecasting()
    return forecasting.run_forecasting_pipeline()


def run_phase_4():
    dashboard = DashboardBlueprint()
    return dashboard.generate_blueprint()


def main():
    start = time.time()

    phases = [1, 2, 3, 4]

    if len(sys.argv) > 1:
        phases = [int(arg) for arg in sys.argv[1:] if arg.isdigit()]

    print("=" * 80)
    print("SALES DEMAND FORECASTING & BI DASHBOARD PROJECT")
    print("=" * 80)

    results = {}

    if 1 in phases:
        results["Phase 1 ETL"] = run_phase_1()

    if 2 in phases:
        results["Phase 2 Segmentation"] = run_phase_2()

    if 3 in phases:
        results["Phase 3 Forecasting"] = run_phase_3()

    if 4 in phases:
        results["Phase 4 Dashboard Blueprint"] = run_phase_4()

    print("\nEXECUTION SUMMARY")
    print("-" * 80)

    for phase, success in results.items():
        print(f"{phase}: {'SUCCESS' if success else 'FAILED'}")

    elapsed = time.time() - start
    print(f"\nTotal time: {elapsed:.2f} seconds")
    print("=" * 80)


if __name__ == "__main__":
    main()