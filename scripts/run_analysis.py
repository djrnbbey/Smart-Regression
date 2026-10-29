"""
Production CLI Runner for Workday Release Impact Analysis & Regression Suite Selection
"""
import sys
import os
from pathlib import Path

# Ensure root is in sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.workday_qe.parser import load_whats_new_report, load_e2e_job_catalog
from src.workday_qe.mapper import build_targeted_regression_records
from src.workday_qe.reporter import compute_executive_metrics, categorize_coverage_gaps
from src.workday_qe.exporter import export_to_csv, export_to_excel
from src.workday_qe.guardrails import GuardrailViolation

def run():
    print("=" * 80)
    print("WORKDAY RELEASE INTELLIGENCE & REGRESSION SUITE PLANNER (PRODUCTION PIPELINE)")
    print("=" * 80)
    
    try:
        print("[1/5] Ingesting & Validating Input Spreadsheets...")
        items, injections = load_whats_new_report()
        print(f"      Loaded {len(items)} What's New items.")
        if injections:
            print(f"      [SECURITY ALERT] Flagged {len(injections)} potential prompt injection strings in raw text!")
            for inj in injections:
                print(f"         - Item {inj['item_id']} [{inj['field']}]: pattern '{inj['detected_pattern']}'")
        else:
            print("      [SECURITY PASSED] 0 adversarial prompt injections detected.")
            
        catalog_jobs = load_e2e_job_catalog()
        print(f"      Loaded {len(catalog_jobs)} Master Catalog jobs.")
        
        print("\n[2/5] Running Semantic BP Impact Mapping & Containment Gate...")
        records = build_targeted_regression_records(items, catalog_jobs)
        print(f"      Successfully generated {len(records)} targeted regression mappings.")
        print("      [SECURITY PASSED] 100% catalog whitelist containment verified.")
        
        print("\n[3/5] Computing Quality Engineering Metrics & Suite Reduction...")
        metrics = compute_executive_metrics(records, catalog_jobs)
        print(f"      Total Items Analyzed         : {metrics['total_release_items']}")
        print(f"      Test-Impacted Items          : {metrics['mapped_items_count']}")
        print(f"      Identified Coverage Gaps     : {metrics['gap_items_count']}")
        print(f"      Targeted E2E Jobs Selected   : {metrics['unique_selected_jobs_count']} / {metrics['master_catalog_total']}")
        print(f"      Suite Reduction Percentage   : {metrics['suite_reduction_pct']:.2f}%")
        print(f"      Reduction Bounds Check       : {metrics['bounds_validation_message']}")
        
        print("\n[4/5] Exporting Deliverables with CWE-1236 Formula Defense & SHA-256 Checksum...")
        csv_file = export_to_csv(records)
        excel_file = export_to_excel(records, catalog_jobs)
        print(f"      Saved CSV deliverable        : {csv_file}")
        print(f"      Saved Excel deliverable      : {excel_file}")
        
        print("\n[5/5] Pipeline Completed Successfully!")
        print("=" * 80)
        return 0
        
    except GuardrailViolation as gv:
        print(f"\n[FATAL GUARDRAIL VIOLATION]: {gv}")
        return 1
    except Exception as e:
        print(f"\n[UNEXPECTED ERROR]: {e}")
        import traceback
        traceback.print_exc()
        return 2

if __name__ == "__main__":
    sys.exit(run())
