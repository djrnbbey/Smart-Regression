"""
Secure Ingestion Parser for Workday Release Notes and Master E2E Job Catalog
Zero-DLL Pure-Python Implementation (Compatible with Windows Application Control)
"""
from pathlib import Path
from typing import List, Dict, Tuple, Any
import openpyxl

from src.workday_qe.config import (
    REQUIRED_WHATS_NEW_COLUMNS,
    REQUIRED_CATALOG_COLUMNS,
    WHATS_NEW_FILE,
    E2E_CATALOG_FILE,
    FALLBACK_WHATS_NEW,
    FALLBACK_E2E_CATALOG
)
from src.workday_qe.guardrails import (
    validate_file_security,
    validate_input_schema,
    sanitize_input_text,
    detect_prompt_injection,
    GuardrailViolation
)

def load_whats_new_report(file_path: Path = None) -> Tuple[List[Dict[str, Any]], List[Dict[str, str]]]:
    """
    Safely loads and parses the Workday 'What's New' release notes spreadsheet.
    Returns:
        (parsed_items, flagged_injections)
    """
    target_path = Path(file_path) if file_path else (WHATS_NEW_FILE if WHATS_NEW_FILE.exists() else FALLBACK_WHATS_NEW)
    validate_file_security(target_path)
    
    wb = openpyxl.load_workbook(target_path, data_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    if not rows or len(rows) < 2:
        raise GuardrailViolation("Release notes spreadsheet contains no data rows.")
        
    headers = [sanitize_input_text(c) for c in rows[0]]
    cleaned_headers = validate_input_schema(headers, REQUIRED_WHATS_NEW_COLUMNS, "Whats_New_Report")
    
    parsed_items = []
    flagged_injections = []
    
    for idx, raw_row in enumerate(rows[1:], 1):
        r = dict(zip(cleaned_headers, [sanitize_input_text(c) for c in raw_row]))
        url = r.get('Release Note URL', '')
        item_id = url.split('/')[-1].replace('.html', '') if url else f"ITEM_{idx}"
        
        # Free text fields
        title = r.get('Title', '')
        desc = r.get('Description', '')
        changes = r.get('Changes', '')
        benefits = r.get('Business Benefits', '')
        
        # Adversarial scan across all user-facing narrative text
        for field_name, text_val in [('Title', title), ('Description', desc), ('Changes', changes)]:
            is_injected, pattern = detect_prompt_injection(text_val)
            if is_injected:
                flagged_injections.append({
                    "item_id": item_id,
                    "field": field_name,
                    "detected_pattern": pattern,
                    "preview": text_val[:100]
                })
        
        item = {
            "num": idx,
            "id": item_id,
            "domain": r.get('Functional Area (Domain)', r.get('Functional Area', '')),
            "mandatory": r.get('Mandatory or Optional', ''),
            "type": r.get('Release Note Type', ''),
            "product_line": r.get('Product Line', ''),
            "product_area": r.get('Product Area', ''),
            "using_workday": r.get('Using Workday', ''),
            "title": title,
            "desc": desc,
            "benefits": benefits,
            "changes": changes,
            "url": url
        }
        parsed_items.append(item)
        
    return parsed_items, flagged_injections

def load_e2e_job_catalog(file_path: Path = None) -> List[Dict[str, Any]]:
    """
    Safely loads and validates the Master E2E Job Catalog.
    Returns:
        List of catalog jobs with exact raw strings and normalized IDs.
    """
    target_path = Path(file_path) if file_path else (E2E_CATALOG_FILE if E2E_CATALOG_FILE.exists() else FALLBACK_E2E_CATALOG)
    validate_file_security(target_path)
    
    wb = openpyxl.load_workbook(target_path, data_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    if not rows or len(rows) < 2:
        raise GuardrailViolation("E2E Catalog spreadsheet contains no data rows.")
        
    headers = [sanitize_input_text(c) for c in rows[0]]
    cleaned_headers = validate_input_schema(headers, REQUIRED_CATALOG_COLUMNS, "E2E_Job_Catalog")
    
    jobs = []
    for raw_row in rows[1:]:
        r = dict(zip(cleaned_headers, raw_row))
        item_num = r.get('Item')
        workstream = sanitize_input_text(r.get('Work-Stream', ''))
        raw_e2e = sanitize_input_text(r.get('E2E', ''))
        
        if item_num is not None and str(item_num).strip() != "" and raw_e2e:
            try:
                item_int = int(item_num)
            except ValueError:
                continue
                
            if ' - ' in raw_e2e:
                job_id, name = raw_e2e.split(' - ', 1)
            else:
                job_id = f"EXP_{item_int:03d}" if workstream.lower() == 'expenses' else str(item_int)
                name = raw_e2e
                
            jobs.append({
                "item_num": item_int,
                "workstream": workstream,
                "raw_e2e": raw_e2e,
                "job_id": job_id,
                "job_name": name
            })
            
    return jobs
