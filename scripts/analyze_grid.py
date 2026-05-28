import re
from collections import defaultdict

filepath = "/Users/uchun1ee/.gemini/antigravity/scratch/ocr_output.txt"
pattern = re.compile(r"Text: '([^']+)' at x=([\d.]+), y=([\d.]+), w=([\d.]+), h=([\d.]+)")

booths = []
width = 4500.0
height = 4000.0

with open(filepath, 'r') as f:
    for line in f:
        m = pattern.search(line)
        if m:
            text = m.group(1)
            x = float(m.group(2))
            y = float(m.group(3))
            w = float(m.group(4))
            h = float(m.group(5))
            
            px = x * width
            py = (1.0 - y - h) * height
            pw = w * width
            ph = h * height
            
            text_clean = text.replace("I", "1").replace("Z", "7").replace("O", "0").replace("S", "5")
            if re.match(r"^[A-H]\d+$", text_clean) or text == "기둥" or text == "무대":
                booths.append({
                    'text': text_clean,
                    'x': px,
                    'y': py,
                    'w': pw,
                    'h': ph,
                    'sec': '기둥' if text == '기둥' else ('무대' if text == '무대' else text_clean[0])
                })

# Print average stats for columns
# Group booths by Section and digit odd/even
# Standard booths are B, C, D, E, F, G, H
# Let's see the X coordinate range for each section
sec_x = defaultdict(list)
for b in booths:
    if b['sec'] in 'ABCDEFGH':
        sec_x[b['sec']].append(b['x'])

print("--- X coordinate ranges for each section ---")
for sec in sorted(sec_x.keys()):
    vals = sorted(sec_x[sec])
    print(f"Section {sec}: min={min(vals):.1f}, max={max(vals):.1f}, unique count={len(set(round(v) for v in vals))}")
    # Let's print unique X values (grouped within 10px)
    unique_xs = []
    for v in sorted(list(set(round(v) for v in vals))):
        if not unique_xs or v - unique_xs[-1] > 15:
            unique_xs.append(v)
    print(f"  Unique X clusters: {unique_xs}")

# Let's also print unique Y coordinates of G and H booths to see their spacing
print("\n--- G and H Y coordinates clusters ---")
g_ys = sorted([b['y'] for b in booths if b['sec'] == 'G'])
h_ys = sorted([b['y'] for b in booths if b['sec'] == 'H'])

unique_g_ys = []
for y in g_ys:
    if not unique_g_ys or y - unique_g_ys[-1] > 15:
        unique_g_ys.append(round(y))
print(f"G Section Y clusters: {unique_g_ys}")

unique_h_ys = []
for y in h_ys:
    if not unique_h_ys or y - unique_h_ys[-1] > 15:
        unique_h_ys.append(round(y))
print(f"H Section Y clusters: {unique_h_ys}")

# Let's print the Y coordinates for standard columns (say Section D)
print("\n--- D Section Y coordinates clusters ---")
d_ys = sorted([b['y'] for b in booths if b['sec'] == 'D'])
unique_d_ys = []
for y in d_ys:
    if not unique_d_ys or y - unique_d_ys[-1] > 15:
        unique_d_ys.append(round(y))
print(f"D Section Y clusters: {unique_d_ys}")
