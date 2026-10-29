import json

with open('parsed_items.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

def print_range(start, end):
    for i in range(start-1, end):
        it = items[i]
        print(f"=== [{it['num']}] ID:{it['id']} | Dom:{it['domain']} | M/O:{it['mandatory']} ===")
        print(f"Title: {it['title']}")
        print(f"Area: {it['product_area']} | Sub: {it['using_workday']}")
        print(f"Desc: {it['desc'].strip()[:200]}")
        print(f"Changes: {it['changes'].strip()[:300]}")
        print()

print_range(61, 87)
