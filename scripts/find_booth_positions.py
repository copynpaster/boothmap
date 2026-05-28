import subprocess
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

image_path = "layout.jpg"
img = Image.open(image_path)
width, height = img.size

# Map region: Y from 100 to 3300
map_crop = img.crop((0, 100, width, 3300))

# Save the crop
temp_map_name = "temp_map_crop.jpg"
map_crop.save(temp_map_name)

print("Running OCR on map region...")
res = subprocess.run(["swift", "ocr.swift", temp_map_name], capture_output=True, text=True)

# Parse output
detected_booths = []

for line in res.stdout.split("\n"):
    if not line.strip() or ":" not in line:
        continue
    parts = line.split(":", 1)
    coords_str = parts[0]
    text = parts[1].strip()
    
    # Check if text looks like a booth ID: e.g. A12, B5, G10
    # Allow minor OCR errors like AI2 -> A12, O2 -> D2, etc.
    text_clean = text.replace("I", "1").replace("Z", "7").replace("O", "0")
    
    # Match pattern like [A-H]\d+ or 무대
    if re.match(r"^[A-H]\d+$", text_clean) or "무대" in text_clean:
        try:
            x, y, w, h = map(float, coords_str.split(","))
            # Global Y (Vision Y=0 is bottom of crop)
            global_y = 100 + (1.0 - y) * map_crop.height
            global_x = x * map_crop.width
            detected_booths.append((global_x, global_y, text_clean))
        except Exception as e:
            pass

detected_booths.sort(key=lambda item: item[2])

print(f"\nFound {len(detected_booths)} booth positions on the map:")
for gx, gy, txt in detected_booths:
    print(f"Booth: {txt:5s} | X: {gx:6.1f} | Y: {gy:6.1f}")

import os
if os.path.exists(temp_map_name):
    os.remove(temp_map_name)
