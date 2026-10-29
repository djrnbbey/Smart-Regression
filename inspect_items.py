import json

with open('parsed_items.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

with open('catalog_jobs.json', 'r', encoding='utf-8') as f:
    jobs = json.load(f)

print(f"Total Release Items: {len(items)}")
print(f"Total Catalog Jobs: {len(jobs)}")
print("\n--- MASTER CATALOG JOBS ---")
for j in jobs:
    print(f"[{j['item_num']:02d}] {j['workstream']:22s} | {j['raw_e2e']}")

print("\n--- RELEASE ITEMS SAMPLE (First 10) ---")
for it in items[:10]:
    print(f"[{it['num']:02d}] ID:{it['id']} | Domain:{it['domain']} | M/O:{it['mandatory']} | Title:{it['title']}")
    print(f"     Desc: {it['desc'][:120]}...")
