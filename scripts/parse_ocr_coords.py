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
            
            # Pixel coordinates
            px = x * width
            py = (1.0 - y - h) * height  # Top-left is (0, 0)
            pw = w * width
            ph = h * height
            
            # Filter out non-booth shapes (only booth pattern: A-H + digits, or 무대, 기둥)
            text_clean = text.replace("I", "1").replace("Z", "7").replace("O", "0")
            if re.match(r"^[A-H]\d+$", text_clean) or text == "기둥" or text == "무대":
                booths.append({
                    'text': text_clean,
                    'x': px,
                    'y': py,
                    'w': pw,
                    'h': ph
                })

# Group by Section
sections = {}
for b in booths:
    if b['text'] in ["기둥", "무대"]:
        sec = b['text']
    else:
        sec = b['text'][0]
    if sec not in sections:
        sections[sec] = []
    sections[sec].append(b)

for sec in sorted(sections.keys()):
    print(f"\n--- Section {sec} ---")
    sec_booths = sections[sec]
    if sec in ["기둥", "무대"]:
        sec_booths.sort(key=lambda b: (b['x'], b['y']))
    else:
        sec_booths.sort(key=lambda b: int(re.search(r"\d+", b['text']).group()))
    
    for b in sec_booths:
        print(f"Booth {b['text']:4s}: X={b['x']:.1f}, Y={b['y']:.1f}, W={b['w']:.1f}, H={b['h']:.1f}")
