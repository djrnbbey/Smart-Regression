import json

with open('catalog_jobs.json', 'r', encoding='utf-8') as f:
    jobs = json.load(f)

with open('complete_mapping.json', 'r', encoding='utf-8') as f:
    mapping = json.load(f)

with open('parsed_items.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

# valid raw names
valid_names = set(j['raw_e2e'] for j in jobs)
print(f"Valid catalog job names ({len(valid_names)}):")
for v in sorted(valid_names):
    print(f"  '{v}'")

print("\nVerifying all 87 mappings...")
errors = 0
unique_selected_jobs = set()
gap_count = 0
for m in mapping:
    target = m['job_id_name']
    if target == "No existing E2E Job found - Gap Identified":
        gap_count += 1
    elif target in valid_names:
        unique_selected_jobs.add(target)
    else:
        print(f"ERROR: Item #{m['num']} mapped to ungrounded job: '{target}'")
        errors += 1

print(f"\nVerification Results:")
print(f"Errors found: {errors}")
print(f"Total Release Items: {len(mapping)}")
print(f"Gaps identified: {gap_count}")
print(f"Items mapped to catalog jobs: {len(mapping) - gap_count}")
print(f"Unique E2E jobs selected: {len(unique_selected_jobs)} out of {len(valid_names)} total catalog jobs")
reduction_pct = (1 - (len(unique_selected_jobs) / len(valid_names))) * 100
print(f"Suite Reduction: {reduction_pct:.2f}% reduction")
print("\nUnique Selected E2E Jobs:")
for j in sorted(unique_selected_jobs):
    print(f"  * {j}")
