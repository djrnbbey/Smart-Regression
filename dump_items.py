import json

with open('parsed_items.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

for it in items:
    print("=" * 80)
    print(f"ITEM #{it['num']} | ID: {it['id']} | Domain: {it['domain']} | M/O: {it['mandatory']}")
    print(f"Title: {it['title']}")
    print(f"Product Area: {it['product_area']} | Using Workday: {it['using_workday']}")
    print(f"Desc: {it['desc'].strip()}")
    print(f"Changes: {it['changes'][:300].strip()}...")
