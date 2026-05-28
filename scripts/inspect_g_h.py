import re

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
            if re.match(r"^[gGhH]\d+$", text_clean):
                booths.append({
                    'text': text_clean,
                    'x': px,
                    'y': py,
                    'w': pw,
                    'h': ph,
                    'sec': text_clean[0].upper()
                })

# Print G booths sorted by Y (top of image is smallest Y, bottom is largest Y)
print("=== G Section (sorted by Y descending, i.e., from bottom to top of image) ===")
g_booths = [b for b in booths if b['sec'] == 'G']
g_booths.sort(key=lambda b: b['y'], reverse=True)
for b in g_booths:
    print(f"Booth {b['text']:4s}: X={b['x']:.1f}, Y={b['y']:.1f}")

print("\n=== H Section (sorted by Y descending, i.e., from bottom to top of image) ===")
h_booths = [b for b in booths if b['sec'] == 'H']
# Filter out the table row H21 (which is at Y=3699)
h_booths = [b for b in h_booths if b['y'] < 3500]
h_booths.sort(key=lambda b: b['y'], reverse=True)
for b in h_booths:
    print(f"Booth {b['text']:4s}: X={b['x']:.1f}, Y={b['y']:.1f}")
