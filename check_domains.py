import json

with open('parsed_items.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

with open('catalog_jobs.json', 'r', encoding='utf-8') as f:
    jobs = json.load(f)

# Let's inspect items by domain and title
domains = {}
for it in items:
    dom = it['domain']
    domains.setdefault(dom, []).append(it)

print("Domains count:")
for d, it_list in sorted(domains.items()):
    print(f"  {d:25s}: {len(it_list)} items")
