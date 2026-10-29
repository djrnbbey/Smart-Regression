import json

with open('parsed_items.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

for it in items:
    print(f"[{it['num']}] ID:{it['id']} | Dom:{it['domain']} | M/O:{it['mandatory']} | Title:{it['title']}")
