"""
MAIN ORCHESTRATOR: Sales Demand Forecasting & BI Dashboard Project
Executes all phases sequentially with monitoring and error handling
"""

import sys
import time
from datetime import datetime
from config.logging_config import logger_etl

# Import phase modules
from src.phase1_etl.etl_pipeline import ETLPipeline
from src.phase2_segmentation.customer_segmentation import CustomerSegmentation
from src.phase3_forecasting.demand_forecasting import DemandForecasting


class ProjectOrchestrator:
    """Orchestrates execution of all project phases"""
    
    def __init__(self):
        """Initialize orchestrator"""
        self.start_time = None
        self.phase_results = {}
        logger_etl.info("Project Orchestrator initialized")
    
    def print_header(self, title: str, level: int = 1):
        """Print formatted header"""
        width = 100
        if level == 1:
            print("\n" + "=" * width)
            print(title.center(width))
            print("=" * width)
        elif level == 2:
            print("\n" + "-" * width)
            print(title)
            print("-" * width)
    
    def print_separator(self):
        """Print visual separator"""
        print("\n" + "🚀 " * 25 + "\n")
    
    def run_phase_1_etl(self) -> bool:
        """Execute Phase 1: Data Synthesis & ETL Pipeline"""
        self.print_header("PHASE 1: DATA SYNTHESIS & ETL PIPELINE TO BIGQUERY", level=2)
        
        try:
            pipeline = ETLPipeline()
            success = pipeline.run_etl_pipeline(generate_new_data=True)
            
            self.phase_results['phase_1'] = {
                'status': 'SUCCESS' if success else 'FAILED',
                'timestamp': datetime.now(),
                'description': 'Synthetic data generation and ETL pipeline'
            }
            
            return success
        
        except Exception as e:
            logger_etl.error(f"Phase 1 execution failed: {str(e)}")
            self.phase_results['phase_1'] = {
                'status': 'ERROR',
                'timestamp': datetime.now(),
                'error': str(e)
            }
            return False
    
    def run_phase_2_segmentation(self) -> bool:
        """Execute Phase 2: Customer Segmentation"""
        self.print_header("PHASE 2: CUSTOMER SEGMENTATION USING BIGQUERY ML", level=2)
        
        try:
            segmentation = CustomerSegmentation()
            success = segmentation.run_segmentation_pipeline()
            
            self.phase_results['phase_2'] = {
                'status': 'SUCCESS' if success else 'FAILED',
                'timestamp': datetime.now(),
                'description': 'K-Means customer segmentation and RFM analysis'
            }
            
            return success
        
        except Exception as e:
            logger_etl.error(f"Phase 2 execution failed: {str(e)}")
            self.phase_results['phase_2'] = {
                'status': 'ERROR',
                'timestamp': datetime.now(),
                'error': str(e)
            }
            return False
    
    def run_phase_3_forecasting(self) -> bool:
        """Execute Phase 3: Time-Series Forecasting"""
        self.print_header("PHASE 3: DEMAND FORECASTING (PROPHET & ARIMA)", level=2)
        
        try:
            forecasting = DemandForecasting()
            success, results = forecasting.run_forecasting_pipeline()
            
            self.phase_results['phase_3'] = {
                'status': 'SUCCESS' if success else 'FAILED',
                'timestamp': datetime.now(),
                'description': 'Time-series forecasting with Prophet and ARIMA',
                'num_categories': len(results.get('prophet_results', {}))
            }
            
            return success
        
        except Exception as e:
            logger_etl.error(f"Phase 3 execution failed: {str(e)}")
            self.phase_results['phase_3'] = {
                'status': 'ERROR',
                'timestamp': datetime.now(),
                'error': str(e)
            }
            return False
    
    def run_phase_4_dashboard(self) -> bool:
        """Execute Phase 4: Dashboard Blueprint Generation"""
        self.print_header("PHASE 4: LOOKER STUDIO DASHBOARD BLUEPRINT", level=2)
        
        try:
            from src.phase4_dashboard.dashboard_blueprint import LOOKER_STUDIO_DASHBOARD_BLUEPRINT
            from config.config import OUTPUT_DIR
            
            # Generate blueprint
            print("Generating Looker Studio Dashboard Blueprint...")
            
            # Save blueprint to file
            output_file = OUTPUT_DIR / "Looker_Studio_Complete_Blueprint.md"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(LOOKER_STUDIO_DASHBOARD_BLUEPRINT)
            
            logger_etl.info(f"✓ Dashboard blueprint generated and saved to {output_file}")
            
            self.phase_results['phase_4'] = {
                'status': 'SUCCESS',
                'timestamp': datetime.now(),
                'description': 'Looker Studio 3-tab dashboard blueprint',
                'output_file': str(output_file)
            }
            
            return True
        
        except Exception as e:
            logger_etl.error(f"Phase 4 execution failed: {str(e)}")
            self.phase_results['phase_4'] = {
                'status': 'ERROR',
                'timestamp': datetime.now(),
                'error': str(e)
            }
            return False
    
    def print_execution_summary(self, elapsed_time: float):
        """Print final execution summary"""
        self.print_header("EXECUTION SUMMARY", level=1)
        
        print("\nPhase Results:")
        print("-" * 80)
        
        all_success = True
        for phase_name, phase_result in self.phase_results.items():
            status = phase_result['status']
            description = phase_result.get('description', '')
            status_symbol = '✓' if status == 'SUCCESS' else '✗'
            
            print(f"{status_symbol} {phase_name.upper()}: {status}")
            print(f"  Description: {description}")
            
            if status != 'SUCCESS':
                all_success = False
                if 'error' in phase_result:
                    print(f"  Error: {phase_result['error']}")
            
            if 'num_categories' in phase_result:
                print(f"  Categories processed: {phase_result['num_categories']}")
            
            if 'output_file' in phase_result:
                print(f"  Output: {phase_result['output_file']}")
            
            print()
        
        print("-" * 80)
        print(f"Total Execution Time: {elapsed_time:.2f} seconds ({elapsed_time/60:.2f} minutes)")
        print(f"Overall Status: {'✓ ALL PHASES COMPLETED' if all_success else '✗ SOME PHASES FAILED'}")
        print("=" * 80)
    
    def run_full_pipeline(self, run_phases: list = None):
        """
        Execute complete pipeline
        
        Args:
            run_phases: List of phases to run (default: all)
                       e.g., [1, 2, 3, 4] or [1, 3] to skip phase 2
        """
        if run_phases is None:
            run_phases = [1, 2, 3, 4]
        
        self.print_separator()
        self.print_header("🎯 SALES DEMAND FORECASTING & BI DASHBOARD PROJECT", level=1)
        print("\n📋 EXECUTION PLAN:")
        print(f"  - Phase 1 (ETL): {'✓' if 1 in run_phases else '✗'} Data Synthesis & BigQuery Pipeline")
        print(f"  - Phase 2 (ML): {'✓' if 2 in run_phases else '✗'} Customer Segmentation (K-Means)")
        print(f"  - Phase 3 (TS): {'✓' if 3 in run_phases else '✗'} Demand Forecasting (Prophet & ARIMA)")
        print(f"  - Phase 4 (BI): {'✓' if 4 in run_phases else '✗'} Looker Studio Dashboard")
        self.print_separator()
        
        self.start_time = time.time()
        
        # Phase 1: Data Synthesis & ETL
        if 1 in run_phases:
            if not self.run_phase_1_etl():
                print("⚠️  Phase 1 failed. Subsequent phases may not work correctly.")
                # Continue anyway, as later phases might use existing data
        
        # Phase 2: Customer Segmentation
        if 2 in run_phases:
            if not self.run_phase_2_segmentation():
                print("⚠️  Phase 2 failed. Phase 3+ will proceed with existing data.")
        
        # Phase 3: Forecasting
        if 3 in run_phases:
            if not self.run_phase_3_forecasting():
                print("⚠️  Phase 3 failed.")
        
        # Phase 4: Dashboard Blueprint
        if 4 in run_phases:
            if not self.run_phase_4_dashboard():
                print("⚠️  Phase 4 failed.")
        
        elapsed_time = time.time() - self.start_time
        
        # Print summary
        self.print_execution_summary(elapsed_time)
        
        # Print next steps
        self.print_next_steps()
    
    def print_next_steps(self):
        """Print recommended next steps"""
        print("\n📝 NEXT STEPS:")
        print("""
1. BigQuery Setup:
   ✓ Verify all tables created successfully in BigQuery
   ✓ Check data quality and record counts

2. Dashboard Creation (Looker Studio):
   ✓ Review the generated blueprint in output/Looker_Studio_Complete_Blueprint.md
   ✓ Follow step-by-step implementation checklist
   ✓ Connect BigQuery datasets to Looker Studio
   ✓ Build tabs 1-3 following the detailed specifications

3. Model Validation:
   ✓ Review forecast accuracy metrics (target: 87%)
   ✓ If accuracy is below target, consider:
     - Adjusting hyperparameters (seasonality, trend change points)
     - Using ensemble methods combining Prophet and ARIMA
     - Collecting more historical data

4. Customer Segmentation Review:
   ✓ Analyze cluster profiles in the customer_segments table
   ✓ Validate that segments are business-meaningful
   ✓ Consider adjusting K (number of clusters) if needed

5. Operational Automation:
   ✓ Set up BigQuery scheduled queries for daily refreshes
   ✓ Configure alerts for forecast accuracy drops
   ✓ Set up email notifications for dashboard updates

6. Optimization:
   ✓ Create materialized views for frequently used aggregations
   ✓ Implement incremental data loading for large datasets
   ✓ Monitor BigQuery costs and optimize queries

📧 For questions or issues:
   - Check logs in: logs/
   - Review output samples in: output/
   - Consult project README.md for troubleshooting
        """)


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main entry point"""
    
    # Check if specific phases are requested
    run_phases = [1, 2, 3, 4]  # Default: run all phases
    
    if len(sys.argv) > 1:
        # Example: python main.py 1 3 (run phases 1 and 3 only)
        try:
            run_phases = [int(p) for p in sys.argv[1:] if p.isdigit()]
            if not run_phases:
                run_phases = [1, 2, 3, 4]
        except ValueError:
            pass
    
    # Create orchestrator and run pipeline
    orchestrator = ProjectOrchestrator()
    orchestrator.run_full_pipeline(run_phases)


if __name__ == "__main__":
    main()
