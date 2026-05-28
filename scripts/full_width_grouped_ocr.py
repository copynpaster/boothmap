import os
import subprocess
from PIL import Image

image_path = "/Users/uchun1ee/.gemini/antigravity/brain/9c55d14c-dd38-45b4-8ae3-ec1af5913b15/.tempmediaStorage/media_9c55d14c-dd38-45b4-8ae3-ec1af5913b15_1779802711962.jpg"
img = Image.open(image_path)
width, height = img.size

list_start_y = 650
list_height = height - list_start_y

chunk_h = 450
overlap = 30
start_y = 0

fragments = []
chunk_idx = 0

print("Extracting fragments with upscaled full-width OCR chunks...")

while start_y < list_height:
    end_y = min(start_y + chunk_h, list_height)
    crop_y_start = list_start_y + start_y
    
    # Crop the FULL width (20 to 680)
    chunk = img.crop((20, crop_y_start, 680, list_start_y + end_y))
    
    # Upscale by 2.5x
    zoomed = chunk.resize((int(chunk.width * 2.5), int(chunk.height * 2.5)), Image.Resampling.LANCZOS)
    temp_name = f"full_chunk_{chunk_idx}.jpg"
    zoomed.save(temp_name)
    
    res = subprocess.run(["swift", "ocr.swift", temp_name], capture_output=True, text=True)
    os.remove(temp_name)
    
    for line in res.stdout.split("\n"):
        if not line.strip() or ":" not in line:
            continue
        parts = line.split(":", 1)
        coords_str = parts[0]
        text = parts[1].strip()
        
        try:
            x, y, w, h = map(float, coords_str.split(","))
            # Global coordinates
            global_y = crop_y_start + (1.0 - y) * chunk.height
            global_x = 20 + x * chunk.width
            fragments.append((global_x, global_y, text))
        except Exception as e:
            pass
            
    if end_y == list_height:
        break
    start_y += chunk_h - overlap
    chunk_idx += 1

# Deduplicate fragments (overlapping Y ranges)
unique_fragments = []
seen = set()
for x, y, text in fragments:
    # Round coordinates to identify duplicates
    key = (round(x, 0), round(y, 0), text)
    if key not in seen:
        seen.add(key)
        unique_fragments.append((x, y, text))

# Group fragments horizontally into rows
unique_fragments.sort(key=lambda item: item[1]) # Sort by Y coordinate

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
        # Check Y distance to current row average Y
        avg_y = sum(item[1] for item in current_row) / len(current_row)
        if abs(y - avg_y) <= threshold_y:
            current_row.append((x, y, text))
        else:
            rows.append(current_row)
            current_row = [(x, y, text)]

if current_row:
    rows.append(current_row)

# Format and print grouped rows
print(f"\nGrouped {len(rows)} rows:")
for r in rows:
    r.sort(key=lambda item: item[0]) # Sort horizontally left to right
    combined_text = " ".join(item[2] for item in r)
    print(combined_text)
