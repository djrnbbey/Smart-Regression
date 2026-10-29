import openpyxl
import json

wb = openpyxl.load_workbook('E2E_Job_Catalog.xlsx', data_only=True)
ws = wb.active
jobs = []
for r in list(ws.iter_rows(values_only=True))[1:]:
    item_num, workstream, e2e_name = r[0], r[1], r[2]
    if item_num is not None and e2e_name is not None:
        e2e_str = str(e2e_name).strip()
        if ' - ' in e2e_str:
            job_id, name = e2e_str.split(' - ', 1)
        else:
            job_id = f"EXP_{item_num:03d}" if str(workstream).strip().lower() == 'expenses' else str(item_num)
            name = e2e_str
        jobs.append({
            'item_num': item_num,
            'workstream': str(workstream).strip(),
            'raw_e2e': e2e_str,
            'job_id': job_id,
            'job_name': name
        })

print(f"Total jobs: {len(jobs)}")
with open('catalog_jobs.json', 'w', encoding='utf-8') as f:
    json.dump(jobs, f, indent=2)
print("Saved catalog_jobs.json")
