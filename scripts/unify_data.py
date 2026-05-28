import re
import json

# 1. Read current data.js to load the state
with open("/Users/uchun1ee/.gemini/antigravity/scratch/teaworld2026/data.js", "r", encoding="utf-8") as f:
    content = f.read()

# We can parse RAW_EXHIBITORS and BOOTH_GRID_MAP using python's regex and json parser
raw_exhibitors_match = re.search(r"const RAW_EXHIBITORS = \[(.*?)\n\];", content, re.DOTALL)
booth_grid_map_match = re.search(r"const BOOTH_GRID_MAP = (\{.*?\n\});", content, re.DOTALL)

if not raw_exhibitors_match or not booth_grid_map_match:
    print("Error: Could not find raw exhibitors or grid map in data.js")
    exit(1)

# Extract exhibitors map
raw_exhibitors_text = raw_exhibitors_match.group(1)
exhibitorsMap = {}
# Find all lines like { id: "...", name: "..." }
for line in raw_exhibitors_text.split("\n"):
    m = re.search(r'id:\s*["\']([^"\']+)["\'],\s*name:\s*["\']([^"\']+)["\']', line)
    if m:
        exhibitorsMap[m.group(1).strip()] = m.group(2).strip()

# Load booth grid map json
grid_map = json.loads(booth_grid_map_match.group(1))

# 2. Merge them into a single consolidated list
unified_data = []

# Special helper to determine section from ID
def get_section(booth_id):
    if booth_id == "무대" or booth_id.startswith("입구") or booth_id.startswith("출구") or booth_id == "등록대":
        return "SPECIAL"
    return booth_id[0].upper()

# We want to sort the unified list logically:
# A1-A49, B1-B29, C1-C31, D1-D34, E1-E34, F1-F32, G1-G28, H1-H27, then Special Entities (무대, 입구, 출구, 등록대)
all_booth_ids = list(grid_map.keys())

def sort_key(booth_id):
    if booth_id == "무대":
        return (9, 0, "무대")
    elif booth_id.startswith("입구"):
        num = int(booth_id.split("_")[1]) if "_" in booth_id else 1
        return (9, 1, num)
    elif booth_id.startswith("출구"):
        num = int(booth_id.split("_")[1]) if "_" in booth_id else 1
        return (9, 2, num)
    elif booth_id == "등록대":
        return (9, 3, "등록대")
    
    sec = booth_id[0]
    num = int(booth_id[1:])
    sec_order = "ABCDEFGH".index(sec)
    return (sec_order, num, "")

all_booth_ids.sort(key=sort_key)

for bid in all_booth_ids:
    coords = grid_map[bid]
    
    # Get Name
    if bid == "무대":
        name = "메인 무대 (차 시연 및 공연)"
    elif bid.startswith("입구"):
        name = "입구"
    elif bid.startswith("출구"):
        name = "출구"
    elif bid == "등록대":
        name = "등록대"
    else:
        name = exhibitorsMap.get(bid, "미배정 부스")
    
    unified_data.append({
        "id": bid,
        "name": name,
        "section": get_section(bid),
        "gridX": coords["gridX"],
        "gridY": coords["gridY"],
        "gridW": coords["gridW"],
        "gridH": coords["gridH"]
    })

# 3. Create the clean Javascript content
js_content = f"""// Unified Exhibition Booth Layout Data
// 쉽게 수정할 수 있는 단일 통합 데이터 세트 (ID, 상호명, 구역/그룹, 그리드 좌표 및 크기)
const EXHIBITORS_DATA = [
"""

for item in unified_data:
    js_content += f'  {{ id: "{item["id"]}", name: "{item["name"]}", gridX: {item["gridX"]}, gridY: {item["gridY"]}, gridW: {item["gridW"]}, gridH: {item["gridH"]} }},\n'

js_content += f"""];

// Helper function to map booth ID to grid coordinates and cell dimensions
function getBoothGrid(id) {{
  const booth = EXHIBITORS_DATA.find(b => b.id === id);
  if (!booth) return null;
  return {{
    gridX: booth.gridX,
    gridY: booth.gridY,
    gridW: booth.gridW,
    gridH: booth.gridH
  }};
}}

// Helper function to convert grid units to pixels
function getBoothCoordinatesForGrid(gridX, gridY, gridW, gridH) {{
  const COL_UNIT = 28; // cell width (26px) + gap (2px)
  const ROW_UNIT = 22; // cell height (20px) + gap (2px)
  const margin_left = 32;
  const margin_top = 23;
  
  const x = margin_left + gridX * COL_UNIT;
  // gridY = 26 is Row 1 (top of SVG), gridY = 0 is Row 27 (bottom of SVG)
  const y = margin_top + (26 - (gridY + gridH - 1)) * ROW_UNIT;
  
  const width = gridW * 26 + (gridW - 1) * 2;
  const height = gridH * 20 + (gridH - 1) * 2;
  
  return {{ x, y, width, height, gridX, gridY, gridW, gridH }};
}}

// Generate coordinates dynamically based on booth ID
function getBoothCoordinates(id) {{
  const grid = getBoothGrid(id);
  if (!grid) return null;
  return getBoothCoordinatesForGrid(grid.gridX, grid.gridY, grid.gridW, grid.gridH);
}}

// Helper to dynamically extract section from first letter of ID (A-H), defaulting to 'SPECIAL'
function getBoothSection(id) {{
  const firstChar = id.charAt(0);
  return (firstChar >= 'A' && firstChar <= 'H') ? firstChar : 'SPECIAL';
}}

// Compile final list with coordinates for app.js rendering
const DEFAULT_EXHIBITORS = EXHIBITORS_DATA.map(booth => {{
  const coords = getBoothCoordinatesForGrid(booth.gridX, booth.gridY, booth.gridW, booth.gridH);
  return {{
    ...booth,
    section: getBoothSection(booth.id),
    ...coords
  }};
}});

// Pillar Coordinates (Located on the grid map)
const PILLARS = [
  {{ "gridX": 5, "gridY": 18, "gridW": 1, "gridH": 1 }},
  {{ "gridX": 5, "gridY": 9, "gridW": 1, "gridH": 1 }}
].map(p => {{
  const coords = getBoothCoordinatesForGrid(p.gridX, p.gridY, p.gridW, p.gridH);
  return {{ ...p, ...coords }};
}});
"""

# Save updated data.js
with open("/Users/uchun1ee/.gemini/antigravity/scratch/teaworld2026/data.js", "w", encoding="utf-8") as f:
    f.write(js_content)

print("data.js unified and cleaned successfully!")
