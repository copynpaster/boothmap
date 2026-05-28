import re
import json

# 1. Read current data.js
with open("/Users/uchun1ee/.gemini/antigravity/scratch/teaworld2026/data.js", "r", encoding="utf-8") as f:
    content = f.read()

# Parse the EXHIBITORS_DATA block
exhibitors_data_match = re.search(r"const EXHIBITORS_DATA = \[(.*?)\n\];", content, re.DOTALL)
if not exhibitors_data_match:
    print("Error: Could not find EXHIBITORS_DATA in data.js")
    exit(1)

exhibitors_text = exhibitors_data_match.group(1)

# Parse lines into dict objects
items = []
for line in exhibitors_text.split("\n"):
    # E.g. { id: "A1", name: "미배정 부스", section: "A", gridX: 6, gridY: 2, gridW: 1, gridH: 1 },
    m = re.search(r'id:\s*["\']([^"\']+)["\'],\s*name:\s*["\']([^"\']+)["\'],\s*section:\s*["\']([^"\']+)["\'],\s*gridX:\s*(\d+),\s*gridY:\s*(\d+),\s*gridW:\s*(\d+),\s*gridH:\s*(\d+)', line)
    if m:
        items.append({
            'id': m.group(1),
            'name': m.group(2),
            'section': m.group(3),
            'gridX': int(m.group(4)),
            'gridY': int(m.group(5)),
            'gridW': int(m.group(6)),
            'gridH': int(m.group(7))
        })

# 2. Sort items by name (with vacant at bottom, facilities at very bottom)
def sort_key(item):
    name = item['name']
    bid = item['id']
    is_special = bid in ["무대", "등록대"] or bid.startswith("입구") or bid.startswith("출구")
    is_vacant = name == "미배정 부스"
    
    if is_special:
        return (2, bid)
    elif is_vacant:
        # Sort vacant booths by ID order (e.g. A1, A2...)
        sec = bid[0]
        num = int(bid[1:]) if bid[1:].isdigit() else 0
        return (1, sec, num)
    else:
        # Standard occupied booths sorted by name
        return (0, name)

items.sort(key=sort_key)

# 3. Format back into JS array text
sorted_js_rows = []
for item in items:
    sorted_js_rows.append(f'  {{ id: "{item["id"]}", name: "{item["name"]}", section: "{item["section"]}", gridX: {item["gridX"]}, gridY: {item["gridY"]}, gridW: {item["gridW"]}, gridH: {item["gridH"]} }},')

sorted_exhibitors_text = "\n".join(sorted_js_rows)

# Replace the array in the file content
new_content = content.replace(exhibitors_text, "\n" + sorted_exhibitors_text)

# Write back to data.js
with open("/Users/uchun1ee/.gemini/antigravity/scratch/teaworld2026/data.js", "w", encoding="utf-8") as f:
    f.write(new_content)

print("data.js successfully sorted by name!")
