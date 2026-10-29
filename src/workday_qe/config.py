"""
Configuration constants and paths for Workday QE Regression Planner
"""
import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_INPUT_DIR = BASE_DIR / "data" / "input"
DATA_OUTPUT_DIR = BASE_DIR / "data" / "output"

# Canonical File Names
WHATS_NEW_FILE = DATA_INPUT_DIR / "Whats_New_Report.xlsx"
E2E_CATALOG_FILE = DATA_INPUT_DIR / "E2E_Job_Catalog.xlsx"

FALLBACK_WHATS_NEW = BASE_DIR / "Whats_New_Report.xlsx"
FALLBACK_E2E_CATALOG = BASE_DIR / "E2E_Job_Catalog.xlsx"

OUTPUT_EXCEL = DATA_OUTPUT_DIR / "Targeted_Workday_Release_Regression_Plan.xlsx"
OUTPUT_CSV = DATA_OUTPUT_DIR / "Targeted_Workday_Release_Regression_Plan.csv"
OUTPUT_HTML = DATA_OUTPUT_DIR / "Targeted_Workday_Release_Regression_Plan.html"

ROOT_OUTPUT_EXCEL = BASE_DIR / "Targeted_Workday_Release_Regression_Plan.xlsx"
ROOT_OUTPUT_CSV = BASE_DIR / "Targeted_Workday_Release_Regression_Plan.csv"
ROOT_OUTPUT_HTML = BASE_DIR / "index.html"

# Required Schema Definitions
REQUIRED_WHATS_NEW_COLUMNS = [
    "Functional Area",
    "Mandatory or Optional",
    "Title",
    "Description",
    "Changes"
]

REQUIRED_CATALOG_COLUMNS = [
    "Item",
    "Work-Stream",
    "E2E"
]

# Output Table Column Specification
OUTPUT_COLUMNS = [
    "Release Item ID / Feature Name",
    "Workstream",
    "Impacted Workday BP(s)",
    "Targeted E2E Job ID & Name",
    "Selection Priority (High/Med/Low)",
    "Risk & Impact Justification (\"Why it must be tested\")"
]

# Safety & Guardrail Thresholds
MAX_FILE_SIZE_MB = 25.0
MIN_SUITE_REDUCTION_PCT = 20.0
MAX_SUITE_REDUCTION_PCT = 85.0

# Statutory & Regulatory Priority Hard-Lock Keywords
STATUTORY_KEYWORDS = [
    "tax", "w-2", "w-2c", "w-4", "t4", "rl-1", "nr4",
    "rti", "fps", "court order", "garnishment", "sdi",
    "proration", "direct deposit", "salary sacrifice", "pensioner"
]

# Standard Gap Identifier
GAP_IDENTIFIER = "No existing E2E Job found - Gap Identified"
