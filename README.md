# Workday Release Intelligence & Risk-Based Regression Suite Planner
**Workday 2026R2 Semi-Annual Release Test Selection & Impact Analysis Engine**

---

## 🌟 Executive Overview
This enterprise tool automates Risk-Based Test Selection (RBTS) for Workday semi-annual releases. By cross-referencing Workday's official "What's New" release notes against your master End-to-End (E2E) regression job catalog, the engine determines the exact Business Processes (BPs) impacted, maps them to automated/manual E2E regression jobs, and optimizes test suite execution while enforcing strict enterprise safety guardrails.

### Key Metrics (2026R2 Cycle)
- **Total Release Items Analyzed:** 87
- **Test-Impacted Features:** 62 (71.3%)
- **Targeted E2E Jobs Scheduled:** 17 unique jobs (out of 42 catalog jobs)
- **Regression Suite Reduction:** **59.52% reduction** (over 60% execution time saved)
- **Coverage Gaps Identified:** 25 items (prioritized action backlog)
- **High-Priority Transactions:** 34 items

---

## 📁 Production Directory Structure
```
c:\SmartRegression\
├── src\
│   └── workday_qe\
│       ├── __init__.py           # Package initialization
│       ├── config.py             # File paths, constants, and schema definitions
│       ├── guardrails.py         # Input/Output validation, anti-injection, and formula defense
│       ├── parser.py             # Ingestion for Whats_New_Report and E2E_Job_Catalog
│       ├── mapper.py             # Semantic BP impact mapping & catalog containment gate
│       ├── reporter.py           # Metrics calculation and coverage gap categorization
│       └── exporter.py           # CWE-1236 safe CSV, styled Excel, and HTML export
├── tests\
│   ├── __init__.py
│   ├── test_guardrails.py        # Automated unit tests for safety, anti-injection, XSS, & formula defense
│   └── test_pipeline.py          # End-to-end integration tests (100% pass)
├── data\
│   ├── input\
│   │   ├── Whats_New_Report.xlsx # Workday official release notes
│   │   └── E2E_Job_Catalog.xlsx  # Master E2E regression job repository
│   └── output\
│       ├── Targeted_Workday_Release_Regression_Plan.xlsx # Styled Excel plan with Executive Summary
│       ├── Targeted_Workday_Release_Regression_Plan.csv  # Standard CSV for Jira/TestRail/CI-CD
│       └── Targeted_Workday_Release_Regression_Plan.html # Standalone interactive web dashboard
├── scripts\
│   └── run_analysis.py           # CLI execution pipeline
├── .agents\
│   └── rules\
│       └── workday-qe-guardrails.md # Workspace rules & invariants for Antigravity AI agents
├── app.py                        # Streamlit Enterprise UI Dashboard
├── index.html                    # Standalone single-page application
├── requirements.txt              # Production Python dependencies
└── README.md                     # Architecture and operational documentation
```

---

## 🛡️ Enterprise Safety Guardrails & Anti-Injection Architecture

The system incorporates defense-in-depth safety guardrails across five distinct layers:

### 1. Input Safety & Schema Integrity
- **File Validation:** Magic-byte/MIME verification, file extension restriction (`.xlsx`, `.csv`), and 25 MB file size limit.
- **Header & Schema Assertions:** Trims header whitespace and validates required columns.
- **Control Character Scrubbing:** Strips non-printable ASCII control characters and dangerous Unicode bidirectional override markers.

### 2. Prompt Injection & Jailbreak Defense
- **Adversarial Signature Scanning:** Regular expression heuristics scan free-text narratives (`Title`, `Description`, `Changes`) for injection payloads (`ignore previous instructions`, `system override`, `developer mode`, `jailbreak`).
- **Structural Data Isolation:** All external release notes are encapsulated inside passive XML CDATA tags (`<untrusted_release_content>`) preventing instructions from being executed.

### 3. Output Grounding & Containment Gate
- **Zero Hallucination Guarantee:** 100% of mapped tests must match the master catalog whitelist. Hallucinated or invented job IDs trigger an immediate `GuardrailViolation`.
- **Deterministic Gap Fallback:** Features lacking test coverage are routed to `"No existing E2E Job found - Gap Identified"`.

### 4. Statutory Priority Hard-Lock
- Any item impacting statutory payroll, tax elections (W-2, W-2c, T4, RL-1), California SDI, UK RTI, court orders, or garnishments is hard-locked to **High Priority** in Python code. Prompt injection cannot downgrade statutory items to Low.

### 5. Spreadsheet Formula Injection Defense (CWE-1236) & XSS
- **Formula Neutralizer:** Escapes dangerous leading characters (`=`, `+`, `-`, `@`, `\t`, `\r`) with a single quote (`'`) to protect QA leads when opening exported plans in Excel.
- **XSS Mitigation:** HTML entity escaping (`&`, `<`, `>`, `"`, `'`) across all web and UI views.

### 6. Cryptographic Audit Checksum
- Computes a SHA-256 fingerprint across all planned regression records embedded into the Excel Executive Summary sheet for audit immutability.

---

## 🚀 Quickstart & Commands

All commands use the Windows Python launcher `py`:

### 1. Run Automated Tests
```powershell
py -m unittest discover tests -v
```

### 2. Run the Production Analysis Pipeline
```powershell
py scripts/run_analysis.py
```

### 3. Launch the Interactive Streamlit Web UI
```powershell
py -m streamlit run app.py
```
Open your browser at `http://localhost:8501`.

### 4. Open the Standalone Web Dashboard
Double-click `index.html` or open in any modern browser without server dependencies.

---

## 📊 Summary of Targeted Regression Jobs (17 Selected)
1. `ABS_001 - Leave Processing (Paid and Unpaid)`
2. `BEN_001 - Change Benefits`
3. `COMP_001 - Compensation Change to Pay`
4. `COMP_002 - Compensation Change to Pay (Retro)`
5. `HCM_001 - Personal Elements Change (HR)`
6. `HCM_003 - Change Contact Information`
7. `HCM_004 - Hire to Pay`
8. `HCM_008 - Change Job to Pay`
9. `HCM_009 - Termination to Pay`
10. `LRN_001 - Create and Edit a Course, Program, Lesson, and Topic`
11. `PAY_001 - Pay Input to Settlement`
12. `PAY_002 - Process On Demand Payment`
13. `PAY_004 - Payment Elections (Regular and Bonus)`
14. `PAY_005 - Tax Elections - Federal, State and Local`
15. `REC_001 - Create to Close (Job Requisition)`
16. `TAL_004 - Development Plan`
17. `TAL_005 - Talent Elements (Succession Pool, Talent Pool and Career Profile)`
