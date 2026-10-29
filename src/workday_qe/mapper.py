"""
Semantic Impact Mapper & Whitelist Containment Gate
"""
import json
from pathlib import Path
from typing import List, Dict, Set, Any

from src.workday_qe.config import BASE_DIR, GAP_IDENTIFIER
from src.workday_qe.guardrails import (
    validate_catalog_grounding,
    enforce_statutory_priority_lock,
    GuardrailViolation
)

def build_targeted_regression_records(
    parsed_items: List[Dict[str, Any]],
    catalog_jobs: List[Dict[str, Any]],
    mapping_spec_path: Path = None
) -> List[Dict[str, Any]]:
    """
    Cross-references release items with master catalog jobs according to QE impact rules.
    Enforces deterministic statutory hard-locks and strict catalog grounding.
    """
    spec_path = mapping_spec_path if mapping_spec_path else (BASE_DIR / "complete_mapping.json")
    with open(spec_path, 'r', encoding='utf-8') as f:
        mapping_rules = json.load(f)
        
    rules_by_num = {r['num']: r for r in mapping_rules}
    items_by_num = {it['num']: it for it in parsed_items}
    valid_catalog_names = set(j['raw_e2e'] for j in catalog_jobs)
    
    ws_map = {
        'HCM': 'HCM Core',
        'UK Payroll': 'UK Payroll (Gap)',
        'People Experience': 'People Experience (Help)',
        'Cross App': 'Cross Application',
        'Extend': 'Workday Extend'
    }
    
    final_records = []
    for num, it in items_by_num.items():
        rule = rules_by_num.get(num, {
            "impacted_bp": "General Workday BP",
            "job_id_name": GAP_IDENTIFIER,
            "priority": "Low",
            "impact_type": "Direct Impact",
            "justification": "Analysis pending for this release item."
        })
        
        feature_id_name = f"{it['id']} - {it['title']}"
        domain = it['domain']
        std_workstream = ws_map.get(domain, domain)
        
        rec = {
            "Release Item ID / Feature Name": feature_id_name,
            "Workstream": std_workstream,
            "Impacted Workday BP(s)": rule['impacted_bp'],
            "Targeted E2E Job ID & Name": rule['job_id_name'],
            "Selection Priority (High/Med/Low)": rule['priority'],
            "Risk & Impact Justification (\"Why it must be tested\")": rule['justification'],
            "Impact Type": rule['impact_type'],
            "Delivery Type": it['mandatory'],
            "Release Number": "2026R2",
            "Release Note URL": it.get('url', '')
        }
        
        # Guardrail: Enforce Statutory Priority Hard-Lock
        rec = enforce_statutory_priority_lock(rec)
        final_records.append(rec)
        
    # Output Containment Gate: Assert 100% whitelist grounding
    is_grounded, grounding_errors = validate_catalog_grounding(final_records, valid_catalog_names)
    if not is_grounded:
        raise GuardrailViolation(f"Containment Gate Violation: Ungrounded jobs detected: {grounding_errors}")
        
    return final_records
