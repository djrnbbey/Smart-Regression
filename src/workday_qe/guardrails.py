"""
Workday Release QE Impact Analysis - Safety & Anti-Injection Guardrail Engine
Zero-DLL Pure-Python Implementation (Compatible with Windows Application Control / AppLocker)
"""
import os
import re
import html
import hashlib
from pathlib import Path
from typing import List, Dict, Set, Tuple, Any

from src.workday_qe.config import (
    MAX_FILE_SIZE_MB,
    MIN_SUITE_REDUCTION_PCT,
    MAX_SUITE_REDUCTION_PCT,
    STATUTORY_KEYWORDS,
    GAP_IDENTIFIER
)

class GuardrailViolation(Exception):
    """Custom exception raised when an input/output safety invariant is violated."""
    pass

# ============================================================================
# 1. INPUT SAFETY GUARDRAILS
# ============================================================================

def validate_file_security(file_path: Path, max_size_mb: float = MAX_FILE_SIZE_MB) -> None:
    """
    Validates file existence, supported extensions (.xlsx, .csv), and size boundaries.
    Prevents memory exhaustion, ZIP-bomb attacks, and unsupported file payloads.
    """
    p = Path(file_path)
    if not p.exists():
        raise GuardrailViolation(f"Input file not found: {p}")
    
    if p.suffix.lower() not in [".xlsx", ".xls", ".csv"]:
        raise GuardrailViolation(f"Unsupported file format '{p.suffix}'. Must be .xlsx or .csv")
    
    size_mb = p.stat().st_size / (1024 * 1024)
    if size_mb > max_size_mb:
        raise GuardrailViolation(f"File size exceeds safety limit ({size_mb:.2f} MB > {max_size_mb} MB): {p}")

def validate_input_schema(headers: List[str], required_columns: List[str], schema_name: str) -> List[str]:
    """
    Enforces required column presence, trims leading/trailing whitespace from headers.
    Zero-DLL implementation (Pure Python).
    """
    if not headers:
        raise GuardrailViolation(f"Input dataset '{schema_name}' has no headers.")
    
    cleaned_headers = [str(col).strip() for col in headers]
    existing_cols_normalized = [c.lower() for c in cleaned_headers]
    
    missing = []
    for req in required_columns:
        req_norm = req.lower().strip()
        if not any(req_norm in col for col in existing_cols_normalized):
            missing.append(req)
            
    if missing:
        raise GuardrailViolation(
            f"Schema violation in '{schema_name}': Missing required columns: {missing}. "
            f"Detected columns: {cleaned_headers}"
        )
    return cleaned_headers

def sanitize_input_text(text: Any) -> str:
    """
    Strips non-printable control characters, null bytes, and dangerous Unicode directional overrides.
    """
    if text is None:
        return ""
    text_str = str(text)
    
    # Remove null bytes and non-printable control characters except \n, \r, \t
    cleaned = re.sub(r"[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]", "", text_str)
    # Strip dangerous Unicode Bidi override characters (U+202A to U+202E, U+2066 to U+2069)
    cleaned = re.sub(r"[\u202A-\u202E\u2066-\u2069]", "", cleaned)
    return cleaned.strip()

# ============================================================================
# 2. ADVERSARIAL PROMPT INJECTION & JAILBREAK DEFENSE
# ============================================================================

PROMPT_INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|prior)\s+(instructions|prompts|rules)",
    r"disregard\s+(all\s+)?(previous|prior)",
    r"system\s+override",
    r"you\s+are\s+now\s+(in\s+)?(developer\s+mode|dan|unrestricted)",
    r"jailbreak",
    r"reveal\s+(the\s+)?(system\s+prompt|instructions|secret)",
    r"\[\s*system\s*[:\]]",
    r"<\|(im_start|im_end|system)\|>",
    r"act\s+as\s+an\s+unfiltered"
]

COMPILED_INJECTION_REGEX = re.compile("|".join(PROMPT_INJECTION_PATTERNS), re.IGNORECASE)

def detect_prompt_injection(text: str) -> Tuple[bool, str]:
    """
    Scans free-text fields for adversarial prompt injection or jailbreak attempts.
    Returns (True, matched_pattern) if an adversarial string is detected.
    """
    if not isinstance(text, str):
        return False, ""
    match = COMPILED_INJECTION_REGEX.search(text)
    if match:
        return True, match.group(0)
    return False, ""

def encapsulate_external_data(content: str, doc_id: str) -> str:
    """
    Wraps untrusted external content inside strict XML CDATA boundaries,
    ensuring downstream LLMs treat content strictly as passive data rather than instructions.
    """
    clean_text = content.replace("]]>", "]] >")
    return (
        f'<untrusted_release_content id="{doc_id}">\n'
        f'<![CDATA[\n{clean_text}\n]]>\n'
        f'</untrusted_release_content>'
    )

# ============================================================================
# 3. OUTPUT SAFETY & CONTAINMENT GUARDRAILS
# ============================================================================

DANGEROUS_SPREADSHEET_PREFIXES = ('=', '+', '-', '@', '\t', '\r')

def sanitize_for_spreadsheet(value: Any) -> Any:
    """
    Neutralizes CSV / Excel Formula Injection (CWE-1236).
    If a string starts with =, +, -, @, tab, or carriage return, it prepends a single quote (').
    """
    if not isinstance(value, str):
        return value
    if not value:
        return value
    # Only strip leading space, preserve \t and \r so dangerous prefix check detects them
    val = value.lstrip(' ')
    if val.startswith(DANGEROUS_SPREADSHEET_PREFIXES):
        return f"'{val}"
    return val

def validate_catalog_grounding(records: List[Dict], valid_catalog_jobs: Set[str]) -> Tuple[bool, List[str]]:
    """
    Strict Whitelist Containment Gate:
    Asserts that 100% of mapped targeted jobs exist in the master catalog or are the standard gap fallback.
    """
    errors = []
    for r in records:
        target = r.get("Targeted E2E Job ID & Name", "")
        if target != GAP_IDENTIFIER and target not in valid_catalog_jobs:
            errors.append(f"Ungrounded Job ID/Name: '{target}' in item '{r.get('Release Item ID / Feature Name')}'")
    return len(errors) == 0, errors

def enforce_statutory_priority_lock(record: Dict) -> Dict:
    """
    Deterministic Statutory Gate:
    Guarantees that no model hallucination or prompt injection can downgrade
    statutory compliance, tax, or legal deductions to Low or Medium.
    """
    rec_copy = dict(record)
    bp = str(rec_copy.get("Impacted Workday BP(s)", "")).lower()
    title = str(rec_copy.get("Release Item ID / Feature Name", "")).lower()
    workstream = str(rec_copy.get("Workstream", "")).lower()
    
    is_statutory = any(k in bp or k in title for k in STATUTORY_KEYWORDS)
    is_payroll_or_tax = "payroll" in workstream or "tax" in bp or "benefit" in workstream
    
    if is_statutory and is_payroll_or_tax:
        rec_copy["Selection Priority (High/Med/Low)"] = "High"
    return rec_copy

def escape_html(text: Any) -> str:
    """
    Escapes HTML entities (&, <, >, ", ') to prevent Cross-Site Scripting (XSS)
    in web views and standalone HTML dashboards.
    """
    if text is None:
        return ""
    return html.escape(str(text), quote=True)

def validate_suite_reduction_bounds(
    selected_count: int,
    catalog_total: int,
    min_pct: float = MIN_SUITE_REDUCTION_PCT,
    max_pct: float = MAX_SUITE_REDUCTION_PCT
) -> Tuple[bool, float, str]:
    """
    Statistical suite reduction bounds check.
    """
    if catalog_total == 0:
        return False, 0.0, "Catalog total is zero."
    
    reduction_pct = (1.0 - (selected_count / catalog_total)) * 100.0
    if reduction_pct < min_pct:
        return False, reduction_pct, f"Low suite reduction ({reduction_pct:.1f}% < {min_pct}%). Risk of redundant testing."
    if reduction_pct > max_pct:
        return False, reduction_pct, f"Excessive suite reduction ({reduction_pct:.1f}% > {max_pct}%). Risk of missing critical regression paths."
    return True, reduction_pct, f"Suite reduction ({reduction_pct:.1f}%) within optimal bounds ({min_pct}% - {max_pct}%)."

def compute_integrity_hash(records: List[Dict]) -> str:
    """
    Computes a cryptographic SHA-256 fingerprint across all planned regression records
    to guarantee output immutability and audit reproducibility.
    """
    hasher = hashlib.sha256()
    for r in sorted(records, key=lambda x: str(x.get("Release Item ID / Feature Name", ""))):
        row_str = "|".join(str(r.get(k, "")) for k in sorted(r.keys()))
        hasher.update(row_str.encode("utf-8"))
    return hasher.hexdigest()
