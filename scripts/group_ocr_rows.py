import os
import subprocess
from PIL import Image

image_path = "/Users/uchun1ee/.gemini/antigravity/brain/9c55d14c-dd38-45b4-8ae3-ec1af5913b15/.tempmediaStorage/media_9c55d14c-dd38-45b4-8ae3-ec1af5913b15_1779802711962.jpg"
img = Image.open(image_path)
width, height = img.size

# We start from where the list begins (Y: 650) to ignore the map part at the top
list_start_y = 650
list_height = height - list_start_y

chunk_h = 600
overlap = 50
start_y = 0

fragments = []

while start_y < list_height:
    end_y = min(start_y + chunk_h, list_height)
    crop_y_start = list_start_y + start_y
    crop_y_end = list_start_y + end_y
    
    chunk = img.crop((0, crop_y_start, width, crop_y_end))
    # Zoom for better OCR accuracy
    zoomed = chunk.resize((chunk.width * 2, chunk.height * 2), Image.Resampling.LANCZOS)
    
    temp_name = "temp_row_chunk.jpg"
    zoomed.save(temp_name)
    
    res = subprocess.run(["swift", "ocr.swift", temp_name], capture_output=True, text=True)
    os.remove(temp_name)
    
    # Parse lines
    for line in res.stdout.split("\n"):
        if not line.strip() or ":" not in line:
            continue
        parts = line.split(":", 1)
        coords_str = parts[0]
        text = parts[1].strip()
        
        try:
            x, y, w, h = map(float, coords_str.split(","))
            # Convert normalized chunk coordinates to global pixel coordinates
            # Note: Swift Y is 0 at bottom, 1 at top of the image
            global_y = crop_y_start + (1.0 - y) * chunk.height
            global_x = x * width
            fragments.append((global_x, global_y, text))
        except Exception as e:
            pass
            
    if end_y == list_height:
        break
    start_y += chunk_h - overlap

# Remove duplicate fragments (from overlapping chunks)
unique_fragments = []
seen = set()
for x, y, text in fragments:
    # Use rounded coordinates to identify duplicates
    key = (round(x, 1), round(y, 1), text)
    if key not in seen:
        seen.add(key)
        unique_fragments.append((x, y, text))

# Group fragments into rows
unique_fragments.sort(key=lambda item: item[1]) # Sort by Y (top to bottom)

rows = []
current_row = []
threshold_y = 6.0 # Pixels range to group into the same row

for x, y, text in unique_fragments:
    # Filter out header/footer noise
    if "제23회" in text or "국제차문화대전" in text or "WORLD FESTIVAL" in text:
        continue
        
    if not current_row:
        current_row.append((x, y, text))
    else:
        # Check if this fragment is at the same vertical level as the current row
        avg_y = sum(item[1] for item in current_row) / len(current_row)
        if abs(y - avg_y) <= threshold_y:
            current_row.append((x, y, text))
        else:
            rows.append(current_row)
            current_row = [(x, y, text)]

if current_row:
    rows.append(current_row)

# Format and print grouped rows
print(f"Grouped {len(rows)} rows:")
for r in rows:
    # Sort fragments in the same row from left to right (X ascending)
    r.sort(key=lambda item: item[0])
    combined_text = " ".join(item[2] for item in r)
    print(combined_text)
