"""
Analytics, KPIs, and Coverage Gap Categorization Reporter
Zero-DLL Pure-Python Implementation (Compatible with Windows Application Control)
"""
from typing import List, Dict, Any
from collections import Counter

from src.workday_qe.config import GAP_IDENTIFIER
from src.workday_qe.guardrails import validate_suite_reduction_bounds

def compute_executive_metrics(records: List[Dict[str, Any]], catalog_jobs: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Computes summary metrics, test suite reduction percentage, and priority breakdown.
    Zero-DLL implementation (Pure Python).
    """
    total_items = len(records)
    total_catalog = len(catalog_jobs)
    
    covered_items = [r for r in records if r.get('Targeted E2E Job ID & Name') != GAP_IDENTIFIER]
    gap_items = [r for r in records if r.get('Targeted E2E Job ID & Name') == GAP_IDENTIFIER]
    
    unique_selected_jobs = sorted(list(set(r.get('Targeted E2E Job ID & Name', '') for r in covered_items)))
    unique_selected_count = len(unique_selected_jobs)
    
    # Statistical Bounds Guardrail
    is_valid_bounds, reduction_pct, bounds_msg = validate_suite_reduction_bounds(
        unique_selected_count, total_catalog
    )
    
    priority_counts = Counter(r.get('Selection Priority (High/Med/Low)', '') for r in records)
    
    return {
        "total_release_items": total_items,
        "mapped_items_count": len(covered_items),
        "gap_items_count": len(gap_items),
        "master_catalog_total": total_catalog,
        "unique_selected_jobs_count": unique_selected_count,
        "unique_selected_jobs": unique_selected_jobs,
        "suite_reduction_pct": reduction_pct,
        "bounds_validation_message": bounds_msg,
        "is_bounds_valid": is_valid_bounds,
        "high_priority_count": priority_counts.get("High", 0),
        "med_priority_count": priority_counts.get("Med", 0),
        "low_priority_count": priority_counts.get("Low", 0),
    }

def categorize_coverage_gaps(records: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Categorizes the 25 coverage gaps into prioritized QE architectural action domains.
    """
    gap_records = [r for r in records if r.get('Targeted E2E Job ID & Name') == GAP_IDENTIFIER]
    
    categories = {
        "UK Payroll & Statutory Compliance (High Risk)": [],
        "U.S. Federal Government Transactions (High/Med Risk)": [],
        "Global Integrations & AI SSA Agents (Med Risk)": [],
        "Workday Help & Case Management (Low Risk)": []
    }
    
    for r in gap_records:
        ws = str(r.get("Workstream", ""))
        name = str(r.get("Release Item ID / Feature Name", ""))
        
        if "UK Payroll" in ws:
            categories["UK Payroll & Statutory Compliance (High Risk)"].append(r)
        elif "Federal" in name or "PAR" in name or "Personnel Action" in name:
            categories["U.S. Federal Government Transactions (High/Med Risk)"].append(r)
        elif "Integrations" in ws or "SSA" in name or "PECI" in name or "Wellness" in name:
            categories["Global Integrations & AI SSA Agents (Med Risk)"].append(r)
        else:
            categories["Workday Help & Case Management (Low Risk)"].append(r)
            
    return categories
