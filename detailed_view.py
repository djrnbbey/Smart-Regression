import json

with open('parsed_items.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

for it in items:
    print(f"--- ITEM {it['num']} [{it['id']}] ---")
    print(f"Title: {it['title']}")
    print(f"Domain: {it['domain']} | M/O: {it['mandatory']} | Area: {it['product_area']}")
    print(f"Desc: {it['desc'][:250].strip()}")
    print(f"Changes: {it['changes'][:350].strip()}")
    print()
