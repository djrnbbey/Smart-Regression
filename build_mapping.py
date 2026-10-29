import json

with open('parsed_items.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

with open('catalog_jobs.json', 'r', encoding='utf-8') as f:
    jobs = json.load(f)

print(f"Loaded {len(items)} items and {len(jobs)} catalog jobs.")

# Let's write out each item's analysis
mapping_rules = [
    # 1
    {
        "num": 1,
        "impacted_bp": "Change Job",
        "job_id_name": "HCM_008 - Change Job to Pay",
        "priority": "High",
        "impact_type": "Direct Impact",
        "justification": "Mandatory redesign alters the initiation lifecycle, delays in-progress Change Job event creation until subprocess submission, and adds Move to New Manager warnings. This directly affects transactional state flow in HCM_008 - Change Job to Pay, risking unpropagated job attribute changes to downstream payroll."
    },
    # 2
    {
        "num": 2,
        "impacted_bp": "Maintain Additional Payroll Data / Payroll Input",
        "job_id_name": "PAY_001 - Pay Input to Settlement",
        "priority": "Med",
        "impact_type": "Direct Impact",
        "justification": "Mandatory update introduces vendor-provided document attachments and collapsible field groups on the Additional Payroll Data task. Must be validated during pay input entry in PAY_001 - Pay Input to Settlement to prevent UI exceptions or missing third-party payroll deduction inputs."
    },
    # 3
    {
        "num": 3,
        "impacted_bp": "Mass Job Change / Change Job",
        "job_id_name": "HCM_008 - Change Job to Pay",
        "priority": "Med",
        "impact_type": "Direct Impact",
        "justification": "Introduces high-volume staffing updates using Mass Job Change on Mass Action Tables. Directly impacts the underlying Change Job business process and staffing data structures validated in HCM_008 - Change Job to Pay."
    },
    # 4
    {
        "num": 4,
        "impacted_bp": "Manage Career Profile / Talent Highlights",
        "job_id_name": "TAL_005 - Talent Elements (Succession Pool, Talent Pool and Career Profile)",
        "priority": "Low",
        "impact_type": "Direct Impact",
        "justification": "Extends multi-language support for AI-generated Talent Highlights content and source data displayed on Career Profiles. Directly impacts UI rendering and locale evaluation in TAL_005 - Talent Elements (Succession Pool, Talent Pool and Career Profile)."
    },
    # 5
    {
        "num": 5,
        "impacted_bp": "Change Job",
        "job_id_name": "HCM_008 - Change Job to Pay",
        "priority": "High",
        "impact_type": "Direct Impact",
        "justification": "Mandatory security enhancement allows configuring security groups for specific Change Job template fields, overriding step access. If field overrides block compensation or job classification fields, it breaks data propagation in HCM_008 - Change Job to Pay."
    },
    # 6
    {
        "num": 6,
        "impacted_bp": "Maintain Lookup Table / Payroll Calculation",
        "job_id_name": "PAY_001 - Pay Input to Settlement",
        "priority": "Med",
        "impact_type": "Downstream/Upstream Impact",
        "justification": "Enhances View/Edit Lookup Table interface with snapshot prompts. Advanced lookup tables calculate wage bases and deduction rates during gross-to-net payroll execution in PAY_001 - Pay Input to Settlement."
    },
    # 7
    {
        "num": 7,
        "impacted_bp": "Change Job",
        "job_id_name": "HCM_008 - Change Job to Pay",
        "priority": "High",
        "impact_type": "Direct Impact",
        "justification": "Mandatory tenant-wide conversion retiring legacy Change Job experience and forcing Enhanced Change Job Experience across all templates and in-progress events. Directly alters initiation and approval workflows in HCM_008 - Change Job to Pay."
    },
    # 8
    {
        "num": 8,
        "impacted_bp": "Manage Wellness Partner Connections",
        "job_id_name": "No existing E2E Job found - Gap Identified",
        "priority": "Low",
        "impact_type": "Direct Impact",
        "justification": "Enables managing connection status and use cases of external wellness partners. This is a partner-hub integration administration task not covered by BEN_001 or any existing catalog job."
    },
    # 9
    {
        "num": 9,
        "impacted_bp": "Process Payroll / Payroll Processing Checklist",
        "job_id_name": "PAY_001 - Pay Input to Settlement",
        "priority": "Med",
        "impact_type": "Direct Impact",
        "justification": "Enables uploading and viewing attachments on payroll processing checklist items in Payroll Hub. Directly alters operational settlement checklist steps in PAY_001 - Pay Input to Settlement."
    },
    # 10
    {
        "num": 10,
        "impacted_bp": "Create Job Requisition / Edit Job Requisition",
        "job_id_name": "REC_001 - Create to Close (Job Requisition)",
        "priority": "High",
        "impact_type": "Direct Impact",
        "justification": "Mandatory removal of feature opt-in permanently enforces job profile visibility restrictions by country, company, and organization during job requisition creation. Directly impacts job profile prompt filtering in REC_001 - Create to Close (Job Requisition)."
    },
    # 11
    {
        "num": 11,
        "impacted_bp": "Request Leave of Absence / Connected Absence API",
        "job_id_name": "ABS_001 - Leave Processing (Paid and Unpaid)",
        "priority": "Med",
        "impact_type": "Downstream/Upstream Impact",
        "justification": "Delivers leave management configuration and Get Workers Data API overrides for Connected Absence partners. Modifies absence plan and worked hours data structures shared with ABS_001 - Leave Processing (Paid and Unpaid)."
    },
    # 12
    {
        "num": 12,
        "impacted_bp": "Calculate Payroll / Maintain Tax Rules",
        "job_id_name": "PAY_001 - Pay Input to Settlement",
        "priority": "High",
        "impact_type": "Direct Impact",
        "justification": "Mandatory statutory update for California State Disability Insurance (SDI) taxable wages when wages are allocated across multiple states. Incorrect wage resolution causes severe payroll tax compliance failures during PAY_001 - Pay Input to Settlement."
    },
    # 13
    {
        "num": 13,
        "impacted_bp": "Hire / Inbound Recruiting Integration",
        "job_id_name": "HCM_004 - Hire to Pay",
        "priority": "Med",
        "impact_type": "Downstream/Upstream Impact",
        "justification": "Delivers 3 new unconfigured security domains controlling document access for Kenexa and Unistaff hiring integrations. Alters document generation and attachment visibility during the Hire business process in HCM_004 - Hire to Pay."
    },
    # 14
    {
        "num": 14,
        "impacted_bp": "Change Personal Information",
        "job_id_name": "HCM_001 - Personal Elements Change (HR)",
        "priority": "Med",
        "impact_type": "Direct Impact",
        "justification": "Introduces redesigned user experience for standalone and onboarding personal information BPs with guided workflow, active consent, and Quick Tips. Directly alters UI steps in HCM_001 - Personal Elements Change (HR) and HCM_002 - Personal Elements Change (ESS)."
    },
    # 15
    {
        "num": 15,
        "impacted_bp": "Canadian Year-End Tax Query / SSA",
        "job_id_name": "No existing E2E Job found - Gap Identified",
        "priority": "Low",
        "impact_type": "Direct Impact",
        "justification": "Adds conversational AI querying for Canadian year-end tax forms (T4, T4A, RL-1, NR4) via Self-Service Agent. Existing tax catalog job PAY_005 only covers US Federal/State/Local tax elections; no Canadian tax E2E job exists."
    },
    # 16
    {
        "num": 16,
        "impacted_bp": "Calculate UK Payroll / Work Schedule Proration",
        "job_id_name": "No existing E2E Job found - Gap Identified",
        "priority": "High",
        "impact_type": "Direct Impact",
        "justification": "Mandatory UK payroll calculation update using work schedule calendars for mid-period proration. No UK Payroll regression jobs exist in E2E_Job_Catalog.xlsx (master catalog only has US Payroll PAY_001-PAY_005) - High-Risk Regulatory Gap!"
    },
    # 17
    {
        "num": 17,
        "impacted_bp": "Cancel Pay Complete / Payroll Settlement",
        "job_id_name": "PAY_001 - Pay Input to Settlement",
        "priority": "High",
        "impact_type": "Direct Impact",
        "justification": "Mandatory architectural update improving Cancel Pay Complete performance and locking mechanisms. Directly impacts payroll completion rollbacks and reprocessing steps executed in PAY_001 - Pay Input to Settlement."
    },
    # 18
    {
        "num": 18,
        "impacted_bp": "Pay Accounting Reallocation / Retroactive Pay",
        "job_id_name": "PAY_001 - Pay Input to Settlement",
        "priority": "High",
        "impact_type": "Downstream/Upstream Impact",
        "justification": "Mandatory update ensuring retroactive pay adjustments generate corrective accounting reallocations to match updated worktags. Directly impacts ledger postings and retro settlement in PAY_001 - Pay Input to Settlement and COMP_002 - Compensation Change to Pay (Retro)."
    },
    # 19
    {
        "num": 19,
        "impacted_bp": "Data Changes on Demand / Payroll Integration",
        "job_id_name": "PAY_001 - Pay Input to Settlement",
        "priority": "Med",
        "impact_type": "Downstream/Upstream Impact",
        "justification": "Delivers new REST API for Data Changes on Demand to extract delta worker payroll changes without full sweeps. Affects upstream data extraction feeding pay calculations in PAY_001 - Pay Input to Settlement."
    },
    # 20
    {
        "num": 20,
        "impacted_bp": "Manage Dependents / Change Benefits",
        "job_id_name": "BEN_001 - Change Benefits",
        "priority": "High",
        "impact_type": "Direct Impact",
        "justification": "Mandatory feature introducing effective dating for worker dependents, tracking changes over time and preventing gaps in coverage histories. Directly alters dependent eligibility validation in BEN_001 - Change Benefits."
    },
    # 21
    {
        "num": 21,
        "impacted_bp": "Earned Wage Access / Payroll Deductions",
        "job_id_name": "PAY_001 - Pay Input to Settlement",
        "priority": "Med",
        "impact_type": "Downstream/Upstream Impact",
        "justification": "Enables Earned Wage Access (EWA) deduction integration with third-party providers. Modifies payroll deduction calculation rules executed in PAY_001 - Pay Input to Settlement."
    },
    # 22
    {
        "num": 22,
        "impacted_bp": "Maintain Payment Elections",
        "job_id_name": "PAY_004 - Payment Elections (Regular and Bonus)",
        "priority": "High",
        "impact_type": "Direct Impact",
        "justification": "Mandatory enhancement to Direct Deposit setup and validations. Modifies worker account verification and disbursement routing rules in PAY_004 - Payment Elections (Regular and Bonus)."
    },
    # 23
    {
        "num": 23,
        "impacted_bp": "Run Retroactive Pay / Exclude Workers",
        "job_id_name": "COMP_002 - Compensation Change to Pay (Retro)",
        "priority": "High",
        "impact_type": "Direct Impact",
        "justification": "Mandatory capability to exclude specific workers from Retro Pay Calculation. Directly impacts retro calculation batches and worker selection logic in COMP_002 - Compensation Change to Pay (Retro) and ABS_003 - Retro Leave to Pay."
    },
    # 24
    {
        "num": 24,
        "impacted_bp": "Global Payroll Connect / PECI Integration",
        "job_id_name": "No existing E2E Job found - Gap Identified",
        "priority": "Med",
        "impact_type": "Downstream/Upstream Impact",
        "justification": "Enables restarting failed PECI/WECI integrations using completed DIS documents. Catalog lacks dedicated Global Payroll Connect / PECI integration E2E jobs - Integration Gap Identified."
    },
    # 25
    {
        "num": 25,
        "impacted_bp": "Personnel Action Request (PAR) / Payroll Status",
        "job_id_name": "No existing E2E Job found - Gap Identified",
        "priority": "Med",
        "impact_type": "Direct Impact",
        "justification": "Mandatory U.S. Federal government enhancement adding statuses to Personnel Action Status field and enabling PAR resending. Catalog lacks dedicated U.S. Federal PAR E2E test cases - U.S. Federal Gap Identified."
    },
    # 26
    {
        "num": 26,
        "impacted_bp": "Personnel Action Request Setup / Nature of Action",
        "job_id_name": "No existing E2E Job found - Gap Identified",
        "priority": "Low",
        "impact_type": "Direct Impact",
        "justification": "Mandatory U.S. Federal report update separating Legal Authorities and Remarks columns in Nature of Action setup. Administrative/setup reporting feature with no matching job in catalog."
    },
    # 27
    {
        "num": 27,
        "impacted_bp": "Maintain Worker Tax Elections",
        "job_id_name": "PAY_005 - Tax Elections - Federal, State and Local",
        "priority": "High",
        "impact_type": "Direct Impact",
        "justification": "Mandatory reporting field indicating worker or system account that last modified U.S. tax elections on Worker Tax Election business object. Directly impacts audit trail validations in PAY_005 - Tax Elections - Federal, State and Local."
    },
    # 28
    {
        "num": 28,
        "impacted_bp": "Calculate Payroll / Circular Reference Detection",
        "job_id_name": "PAY_001 - Pay Input to Settlement",
        "priority": "Med",
        "impact_type": "Downstream/Upstream Impact",
        "justification": "Delivers Limit to Job Warning for Circular Calculations checkbox to bypass blocking errors during payroll calculation. Directly impacts calculation engine error-handling in PAY_001 - Pay Input to Settlement."
    },
    # 29
    {
        "num": 29,
        "impacted_bp": "Compensation Step Adjustment / Mass Operation",
        "job_id_name": "COMP_001 - Compensation Change to Pay",
        "priority": "Med",
        "impact_type": "Direct Impact",
        "justification": "Introduces new Mass Operation Management task type for Compensation Step Adjustment to update grade step defaults at scale. Directly modifies compensation step assignments tested in COMP_001 - Compensation Change to Pay."
    },
    # 30
    {
        "num": 30,
        "impacted_bp": "Manage Development Plan / AI Generation",
        "job_id_name": "TAL_004 - Development Plan",
        "priority": "Med",
        "impact_type": "Direct Impact",
        "justification": "Mandatory UI change standardizing the Generate with AI prompt for development items in Career Hub and Manager Insights Hub. Directly alters user interaction flow in TAL_004 - Development Plan."
    },
    # 31
    {
        "num": 31,
        "impacted_bp": "Case Management / Edit Tenant Setup - Help",
        "job_id_name": "No existing E2E Job found - Gap Identified",
        "priority": "Low",
        "impact_type": "Direct Impact",
        "justification": "Enables configuration of auto-close timelines for HR cases in Workday Help. Help/Case Management is not covered in the master E2E job catalog."
    },
    # 32
    {
        "num": 32,
        "impacted_bp": "UK RTI Full Payment Submission (FPS) Reporting",
        "job_id_name": "No existing E2E Job found - Gap Identified",
        "priority": "High",
        "impact_type": "Direct Impact",
        "justification": "Mandatory UK Payroll regulatory update adding negative Statutory Neonatal Care Pay (SNCP) exception reporting to UK RTI FPS reports. No UK Payroll compliance jobs exist in catalog - High-Risk Regulatory Gap!"
    },
    # 33
    {
        "num": 33,
        "impacted_bp": "Minimum Wage Analysis / Payroll Agent",
        "job_id_name": "No existing E2E Job found - Gap Identified",
        "priority": "Low",
        "impact_type": "Downstream/Upstream Impact",
        "justification": "Delivers local authority support for Minimum Wage Analysis Skill in conversational Payroll Agent. AI agent skills have no test coverage in catalog."
    },
    # 34
    {
        "num": 34,
        "impacted_bp": "Maintain Payroll Accounting Options",
        "job_id_name": "PAY_001 - Pay Input to Settlement",
        "priority": "Med",
        "impact_type": "Downstream/Upstream Impact",
        "justification": "Introduces No Pay Accounting Reallocation Prior To Date to prevent reallocations prior to closed fiscal periods. Impacts accounting entries generated during payroll settlement in PAY_001 - Pay Input to Settlement."
    },
    # 35
    {
        "num": 35,
        "impacted_bp": "Process On-Demand Payment / Recalculation",
        "job_id_name": "PAY_002 - Process On Demand Payment",
        "priority": "High",
        "impact_type": "Direct Impact",
        "justification": "Mandatory architectural update preventing on-demand payroll result recalculation conflicts when results are locked by background jobs. Directly alters execution reliability in PAY_002 - Process On Demand Payment."
    },
    # 36
    {
        "num": 36,
        "impacted_bp": "Request Compensation Change / Bonus Plan",
        "job_id_name": "COMP_001 - Compensation Change to Pay",
        "priority": "High",
        "impact_type": "Direct Impact",
        "justification": "Mandatory enhancement to percent-based bonus plans enabling multiple bonus plans with individual targets and prorated payout calculations. Directly impacts compensation calculation and downstream pay in COMP_001 - Compensation Change to Pay."
    },
    # 37
    {
        "num": 37,
        "impacted_bp": "Personnel Action Request Mass Cancel / Correct",
        "job_id_name": "No existing E2E Job found - Gap Identified",
        "priority": "Med",
        "impact_type": "Direct Impact",
        "justification": "Delivers Mass Cancel and Mass Correct for U.S. Federal Personnel Action Requests. U.S. Federal PAR transactions lack coverage in master catalog."
    },
    # 38
    {
        "num": 38,
        "impacted_bp": "Post-Separation Personnel Action Request",
        "job_id_name": "HCM_009 - Termination to Pay",
        "priority": "Med",
        "impact_type": "Downstream/Upstream Impact",
        "justification": "Mandatory U.S. Federal update ensuring post-separation PARs reflect accurate termination attributes. Modifies termination data structures downstream of HCM_009 - Termination to Pay."
    },
    # 39
    {
        "num": 39,
        "impacted_bp": "Purge Worker Data / Maintain Address Purge",
        "job_id_name": "HCM_003 - Change Contact Information",
        "priority": "Low",
        "impact_type": "Downstream/Upstream Impact",
        "justification": "Introduces Worker Addresses purgeable data type for data retention compliance. Alters contact data storage rules validated in HCM_003 - Change Contact Information."
    },
    # 40
    {
        "num": 40,
        "impacted_bp": "Pay Accounting Reallocation",
        "job_id_name": "PAY_001 - Pay Input to Settlement",
        "priority": "Med",
        "impact_type": "Downstream/Upstream Impact",
        "justification": "Enhances Pay Accounting Reallocation task to support reallocations by position and earning component. Impacts financial journal postings downstream of PAY_001 - Pay Input to Settlement."
    },
    # 41
    {
        "num": 41,
        "impacted_bp": "Roll Out Compensation Plans / Manage Compensation",
        "job_id_name": "COMP_001 - Compensation Change to Pay",
        "priority": "High",
        "impact_type": "Direct Impact",
        "justification": "Mandatory update to Compensation Plan Rollout Process replacing background tasks with optimized asynchronous framework. Affects compensation updates feeding COMP_001 - Compensation Change to Pay and ADVCOMP_001."
    },
    # 42
    {
        "num": 42,
        "impacted_bp": "Personnel Action Request on Union Membership",
        "job_id_name": "No existing E2E Job found - Gap Identified",
        "priority": "Low",
        "impact_type": "Direct Impact",
        "justification": "Enables initiating PARs upon union membership changes for U.S. Federal workers. Specialized federal union process not represented in catalog."
    },
    # 43
    {
        "num": 43,
        "impacted_bp": "Pay Accounting Reallocation by Status Report",
        "job_id_name": "PAY_001 - Pay Input to Settlement",
        "priority": "Low",
        "impact_type": "Downstream/Upstream Impact",
        "justification": "Mandatory operational report detailing accounting reallocation status. Used for post-settlement audit during PAY_001 - Pay Input to Settlement."
    },
    # 44
    {
        "num": 44,
        "impacted_bp": "Payroll Accounting Reallocation Fringe",
        "job_id_name": "PAY_001 - Pay Input to Settlement",
        "priority": "Med",
        "impact_type": "Downstream/Upstream Impact",
        "justification": "Delivers fringe benefit cost reallocation during payroll accounting runs. Impacts ledger distributions in PAY_001 - Pay Input to Settlement."
    },
    # 45
    {
        "num": 45,
        "impacted_bp": "Calculate Payroll / Circular Reference Warning",
        "job_id_name": "PAY_001 - Pay Input to Settlement",
        "priority": "Med",
        "impact_type": "Downstream/Upstream Impact",
        "justification": "Mandatory warning notification when circular component calculations occur during pay calculation. Directly alters batch run diagnostics in PAY_001 - Pay Input to Settlement."
    },
    # 46
    {
        "num": 46,
        "impacted_bp": "UK Pensioner Payroll / Process Payroll",
        "job_id_name": "No existing E2E Job found - Gap Identified",
        "priority": "High",
        "impact_type": "Direct Impact",
        "justification": "Delivers dedicated UK Pensioner Payroll functionality to process occupational pension payments under PAYE rules. No UK Payroll jobs exist in master catalog - Critical Regulatory Gap!"
    },
    # 47
    {
        "num": 47,
        "impacted_bp": "Manage Learning / Manage Development Plan",
        "job_id_name": "LRN_001 - Create and Edit a Course, Program, Lesson, and Topic",
        "priority": "Med",
        "impact_type": "Direct Impact",
        "justification": "Enables linking learning courses directly to worker development items. Directly modifies course assignment metadata in LRN_001 and cross-functional integration with TAL_004 - Development Plan."
    },
    # 48
    {
        "num": 48,
        "impacted_bp": "Get Workers REST API / Staffing Integration",
        "job_id_name": "HCM_004 - Hire to Pay",
        "priority": "High",
        "impact_type": "Downstream/Upstream Impact",
        "justification": "Mandatory API update adding email filtering parameters and surfacing pre-hire IDs for pending hires in Get Workers API. Downstream integrations consuming new worker records in HCM_004 - Hire to Pay are impacted."
    },
    # 49
    {
        "num": 49,
        "impacted_bp": "Maintain HMRC Gateway Credentials / UK RTI",
        "job_id_name": "No existing E2E Job found - Gap Identified",
        "priority": "High",
        "impact_type": "Direct Impact",
        "justification": "Mandatory UK tax authority credential management task per Employer Reference for RTI filings. No UK Payroll integration tests in catalog - High-Risk Gap!"
    },
    # 50
    {
        "num": 50,
        "impacted_bp": "Request Compensation Change / In-Progress Change Job",
        "job_id_name": "COMP_001 - Compensation Change to Pay",
        "priority": "High",
        "impact_type": "Direct Impact",
        "justification": "Enables mass compensation actions to process workers who have an in-progress Change Job event. Directly tests concurrency resolution between HCM_008 - Change Job to Pay and COMP_001 - Compensation Change to Pay."
    },
    # 51
    {
        "num": 51,
        "impacted_bp": "Personnel Action Request Sequence Validation",
        "job_id_name": "No existing E2E Job found - Gap Identified",
        "priority": "Med",
        "impact_type": "Direct Impact",
        "justification": "Mandatory alert preventing multiple PAR events with identical effective dates and non-zero sequence numbers. U.S. Federal specific - Gap Identified."
    },
    # 52
    {
        "num": 52,
        "impacted_bp": "UK Salary Sacrifice / Payroll Third-Party Payments",
        "job_id_name": "No existing E2E Job found - Gap Identified",
        "priority": "High",
        "impact_type": "Direct Impact",
        "justification": "Mandatory support for UK Salary Sacrifice earning components in Payroll Third-Party Payments. UK Payroll gap in master catalog."
    },
    # 53
    {
        "num": 53,
        "impacted_bp": "Payroll Effective Change Interface (PECI)",
        "job_id_name": "PAY_001 - Pay Input to Settlement",
        "priority": "Med",
        "impact_type": "Downstream/Upstream Impact",
        "justification": "Delivers Worker Has Additional Jobs field attribute on Worker Status section in PECI integration templates. Downstream payroll extract feeds touched during PAY_001 settlement are impacted."
    },
    # 54
    {
        "num": 54,
        "impacted_bp": "Calculate Payroll / Work Schedule IVC",
        "job_id_name": "PAY_001 - Pay Input to Settlement",
        "priority": "Med",
        "impact_type": "Downstream/Upstream Impact",
        "justification": "Delivers new position-based Instance Value Calculations (IVCs) for work schedule calendars. Impacts proration formulas evaluated during PAY_001 - Pay Input to Settlement."
    },
    # 55
    {
        "num": 55,
        "impacted_bp": "Manage Languages / Configure Optional Fields",
        "job_id_name": "TAL_005 - Talent Elements (Succession Pool, Talent Pool and Career Profile)",
        "priority": "Low",
        "impact_type": "Direct Impact",
        "justification": "Adds Fluent checkbox to Configure Optional Fields for Manage Languages BP. Directly impacts profile qualification maintenance in TAL_005."
    },
    # 56
    {
        "num": 56,
        "impacted_bp": "Manage Development Plan / Put Development Item API",
        "job_id_name": "TAL_004 - Development Plan",
        "priority": "Med",
        "impact_type": "Direct Impact",
        "justification": "Mandatory v47.0 SOAP API update adding Skills to Develop fields to Put/Get Development Items web services. Impacts automated payload exchanges in TAL_004 - Development Plan."
    },
    # 57
    {
        "num": 57,
        "impacted_bp": "Request Quality Step Increase / Request Compensation Change",
        "job_id_name": "COMP_001 - Compensation Change to Pay",
        "priority": "High",
        "impact_type": "Direct Impact",
        "justification": "Enables simultaneous in-progress execution of Request Quality Step Increase (QSI) and Request Compensation Change for the same worker. Directly impacts compensation concurrency in COMP_001 - Compensation Change to Pay."
    },
    # 58
    {
        "num": 58,
        "impacted_bp": "Cancel Pay Complete / Process On-Demand Payment",
        "job_id_name": "PAY_002 - Process On Demand Payment",
        "priority": "High",
        "impact_type": "Direct Impact",
        "justification": "Mandatory locking restrictions preventing simultaneous actions on payroll results while Cancel Pay Complete or On Demand calculation runs. Directly affects PAY_002 - Process On Demand Payment and PAY_001."
    },
    # 59
    {
        "num": 59,
        "impacted_bp": "Payroll Register by Period Report",
        "job_id_name": "PAY_001 - Pay Input to Settlement",
        "priority": "Low",
        "impact_type": "Downstream/Upstream Impact",
        "justification": "Mandatory performance optimization for Payroll Register by Period report without changing output schema. Post-payroll validation step in PAY_001."
    },
    # 60
    {
        "num": 60,
        "impacted_bp": "Maintain Deduction Recipients / Payroll Third-Party Payments",
        "job_id_name": "No existing E2E Job found - Gap Identified",
        "priority": "High",
        "impact_type": "Direct Impact",
        "justification": "Mandatory enhancement to Create/Edit Deduction Recipient for UK salary sacrifice arrangements. UK third-party payment flow is not covered in catalog."
    },
    # 61
    {
        "num": 61,
        "impacted_bp": "Case Collaboration in Workday Help",
        "job_id_name": "No existing E2E Job found - Gap Identified",
        "priority": "Low",
        "impact_type": "Direct Impact",
        "justification": "Enables multi-agent collaboration on Help cases. Case management is not covered in master catalog."
    },
    # 62
    {
        "num": 62,
        "impacted_bp": "Article Downloading / Workday Help",
        "job_id_name": "No existing E2E Job found - Gap Identified",
        "priority": "Low",
        "impact_type": "Direct Impact",
        "justification": "Mandatory feature allowing users to download knowledge articles as PDFs in Workday Help. Not covered in master catalog."
    },
    # 63
    {
        "num": 63,
        "impacted_bp": "Change Benefits / Health Care Rate Calculations",
        "job_id_name": "BEN_001 - Change Benefits",
        "priority": "High",
        "impact_type": "Direct Impact",
        "justification": "Delivers custom calculated rates for health care benefit plans based on worker attributes. Directly alters rate determination and deduction calculations in BEN_001 - Change Benefits and downstream payroll."
    },
    # 64
    {
        "num": 64,
        "impacted_bp": "Periodic Tax Filing Integration / Payroll Tax",
        "job_id_name": "PAY_001 - Pay Input to Settlement",
        "priority": "High",
        "impact_type": "Downstream/Upstream Impact",
        "justification": "Mandatory integration updates for MasterTax, ADP, and Ceridian periodic tax filing integrations. Downstream tax filing extraction executed following PAY_001 - Pay Input to Settlement settlement is directly impacted."
    },
    # 65
    {
        "num": 65,
        "impacted_bp": "Personnel Action Request BP Consolidation",
        "job_id_name": "No existing E2E Job found - Gap Identified",
        "priority": "Med",
        "impact_type": "Direct Impact",
        "justification": "Consolidates multiple PAR business processes into a single unified BP definition for U.S. Federal. Catalog lacks federal PAR coverage."
    },
    # 66
    {
        "num": 66,
        "impacted_bp": "Report Trailing Payments / PECI",
        "job_id_name": "PAY_001 - Pay Input to Settlement",
        "priority": "Med",
        "impact_type": "Downstream/Upstream Impact",
        "justification": "Enables PECI integration to extract trailing payments dispatched after worker pay group changes. Impacts pay history synchronization downstream of PAY_001."
    },
    # 67
    {
        "num": 67,
        "impacted_bp": "Request Edit Payroll Inputs",
        "job_id_name": "PAY_001 - Pay Input to Settlement",
        "priority": "High",
        "impact_type": "Direct Impact",
        "justification": "Introduces new Request Edit Payroll Inputs business process enabling audited, workflow-driven edits to existing payroll inputs. Directly modifies pay input adjustment paths in PAY_001 - Pay Input to Settlement."
    },
    # 68
    {
        "num": 68,
        "impacted_bp": "Manage Stock Grants / Stock Vesting Schedule",
        "job_id_name": "COMP_001 - Compensation Change to Pay",
        "priority": "Med",
        "impact_type": "Direct Impact",
        "justification": "Enhances stock vesting schedule configurations and custom schedules. Modifies stock compensation awards tested in COMP_001 - Compensation Change to Pay and ADVCOMP_001."
    },
    # 69
    {
        "num": 69,
        "impacted_bp": "Run Retroactive Pay Calculation",
        "job_id_name": "COMP_002 - Compensation Change to Pay (Retro)",
        "priority": "High",
        "impact_type": "Direct Impact",
        "justification": "Mandatory architectural update optimizing Run Retro Pay Calculation processing performance and memory management. Core engine impact directly affecting COMP_002 - Compensation Change to Pay (Retro) and ABS_003."
    },
    # 70
    {
        "num": 70,
        "impacted_bp": "Correct Change Job",
        "job_id_name": "HCM_008 - Change Job to Pay",
        "priority": "High",
        "impact_type": "Direct Impact",
        "justification": "Delivers configurable field editing on completed Change Job events using Edit Correct Change Job Configuration. Directly modifies retroactive job correction steps in HCM_008 - Change Job to Pay."
    },
    # 71
    {
        "num": 71,
        "impacted_bp": "Personnel Action Request Reporting Fields",
        "job_id_name": "No existing E2E Job found - Gap Identified",
        "priority": "Low",
        "impact_type": "Downstream/Upstream Impact",
        "justification": "Delivers new reporting fields for U.S. Federal PAR variables on Personnel Action business object. U.S. Federal reporting feature - Gap Identified."
    },
    # 72
    {
        "num": 72,
        "impacted_bp": "Standard Payroll Reports / Payroll Settlement",
        "job_id_name": "PAY_001 - Pay Input to Settlement",
        "priority": "Low",
        "impact_type": "Downstream/Upstream Impact",
        "justification": "Mandatory performance updates to standard payroll audit reports used during payroll settlement signoff in PAY_001 - Pay Input to Settlement."
    },
    # 73
    {
        "num": 73,
        "impacted_bp": "Withholding Tax Query / Self-Service Agent",
        "job_id_name": "PAY_005 - Tax Elections - Federal, State and Local",
        "priority": "Med",
        "impact_type": "Downstream/Upstream Impact",
        "justification": "Enables worker self-service queries of State tax and Federal W-4 withholding selections via Self-Service Agent. Validates tax election data structures established in PAY_005 - Tax Elections - Federal, State and Local."
    },
    # 74
    {
        "num": 74,
        "impacted_bp": "Maintain Tax Rules / State-Level Local Exceptions",
        "job_id_name": "PAY_005 - Tax Elections - Federal, State and Local",
        "priority": "High",
        "impact_type": "Direct Impact",
        "justification": "Mandatory statutory update for state-level exceptions on local resident taxes (e.g., PA Act 32 / MD counties). Miscalculated local taxes cause regulatory non-compliance in PAY_005 and PAY_001."
    },
    # 75
    {
        "num": 75,
        "impacted_bp": "Maintain Payroll Payslip Configuration / UK Payslip",
        "job_id_name": "No existing E2E Job found - Gap Identified",
        "priority": "Med",
        "impact_type": "Direct Impact",
        "justification": "Enables display of position details on UK payslips in UI and PDF format. UK payslip generation is not covered in catalog."
    },
    # 76
    {
        "num": 76,
        "impacted_bp": "Edit Tenant Setup - Help / Article Ownership",
        "job_id_name": "No existing E2E Job found - Gap Identified",
        "priority": "Low",
        "impact_type": "Direct Impact",
        "justification": "Mandatory tenant configuration enabling display of article ownership in Workday Help. Non-E2E HR Help feature."
    },
    # 77
    {
        "num": 77,
        "impacted_bp": "Maintain Dependents / Wage Garnishment Relevance",
        "job_id_name": "BEN_001 - Change Benefits",
        "priority": "Med",
        "impact_type": "Downstream/Upstream Impact",
        "justification": "Introduces Garnishment-relevant flag on dependent records supporting wage garnishment calculations. Alters dependent data structures in BEN_001 and downstream payroll withholding in PAY_001."
    },
    # 78
    {
        "num": 78,
        "impacted_bp": "Maintain Dependents / Relocation Data",
        "job_id_name": "BEN_001 - Change Benefits",
        "priority": "Low",
        "impact_type": "Downstream/Upstream Impact",
        "justification": "Adds Dependent Relocation tracking for international assignments with effective dating. Extends dependent profile schema tested in BEN_001 - Change Benefits."
    },
    # 79
    {
        "num": 79,
        "impacted_bp": "Submit Payroll Input Web Service",
        "job_id_name": "PAY_001 - Pay Input to Settlement",
        "priority": "High",
        "impact_type": "Direct Impact",
        "justification": "Mandatory optimization of Submit Payroll Input SOAP web service processing engine. Core inbound data pipeline directly executed during automated test runs of PAY_001 - Pay Input to Settlement."
    },
    # 80
    {
        "num": 80,
        "impacted_bp": "Maintain Staffing Field Defaults / PAR Agency Fields",
        "job_id_name": "No existing E2E Job found - Gap Identified",
        "priority": "Low",
        "impact_type": "Direct Impact",
        "justification": "Delivers defaulting rules for agency-specific SF-50 fields on Personnel Action Requests. U.S. Federal specific setup - Gap Identified."
    },
    # 81
    {
        "num": 81,
        "impacted_bp": "Record UK Court Order for Worker",
        "job_id_name": "No existing E2E Job found - Gap Identified",
        "priority": "High",
        "impact_type": "Direct Impact",
        "justification": "Mandatory UK Payroll update allowing multiple court orders across different issuing authorities with protected earnings priority rules. No UK Payroll tests in catalog - High-Risk Gap!"
    },
    # 82
    {
        "num": 82,
        "impacted_bp": "Put UK Court Order SOAP Web Service",
        "job_id_name": "No existing E2E Job found - Gap Identified",
        "priority": "Med",
        "impact_type": "Direct Impact",
        "justification": "Delivers v47.0 web services to record UK court orders from multiple issuing authorities. UK Payroll web services not covered in catalog."
    },
    # 83
    {
        "num": 83,
        "impacted_bp": "W-2 Tax Document Queries / Self-Service Agent",
        "job_id_name": "PAY_005 - Tax Elections - Federal, State and Local",
        "priority": "Low",
        "impact_type": "Downstream/Upstream Impact",
        "justification": "Enables worker conversational queries of W-2 box values via Self-Service Agent. Relies on tax election and year-end data validated in PAY_005 and PAY_001."
    },
    # 84
    {
        "num": 84,
        "impacted_bp": "Generate W-2 / Year End Tax Forms",
        "job_id_name": "PAY_005 - Tax Elections - Federal, State and Local",
        "priority": "High",
        "impact_type": "Direct Impact",
        "justification": "Mandatory statutory update for 2026 tax year adding Box 12 Code 12 TA (Trump account contributions) and renaming Box 14a. Directly impacts year-end tax form generation downstream of PAY_005 and PAY_001 settlement."
    },
    # 85
    {
        "num": 85,
        "impacted_bp": "Workday Graph API / Job Profile Query",
        "job_id_name": "REC_001 - Create to Close (Job Requisition)",
        "priority": "Med",
        "impact_type": "Downstream/Upstream Impact",
        "justification": "Mandatory Graph API schema enhancement exposing job classification, management level, and restrictions on jobProfile queries. Impacts external integrations and job profiles used in REC_001 - Create to Close (Job Requisition)."
    },
    # 86
    {
        "num": 86,
        "impacted_bp": "Generate W-2C / Year End Tax Corrections",
        "job_id_name": "PAY_005 - Tax Elections - Federal, State and Local",
        "priority": "High",
        "impact_type": "Direct Impact",
        "justification": "Mandatory statutory update for W-2C corrected tax statements supporting H.R. 1 Box 12/14 changes. Affects tax correction processing downstream of PAY_005 and PAY_001 settlement."
    },
    # 87
    {
        "num": 87,
        "impacted_bp": "Worker Effective Change Interface (WECI)",
        "job_id_name": "PAY_001 - Pay Input to Settlement",
        "priority": "Med",
        "impact_type": "Downstream/Upstream Impact",
        "justification": "Adds Worker Has Additional Jobs field attribute to Worker Status data section on WECI integration template. Touches downstream payroll interface payloads generated from worker changes in PAY_001."
    }
]

print(f"Total mapped rules defined: {len(mapping_rules)}")
with open('complete_mapping.json', 'w', encoding='utf-8') as f:
    json.dump(mapping_rules, f, indent=2)
print("Saved complete_mapping.json")
