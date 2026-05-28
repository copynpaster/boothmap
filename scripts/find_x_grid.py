import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

image_path = "layout.jpg"
img = Image.open(image_path).convert('L')
width, height = img.size

# Crop top region containing the map (Y: 100 to 3300)
img_top = img.crop((0, 100, width, 3300))
arr = np.array(img_top)

# Compute horizontal gradient (vertical edges)
dx = np.abs(arr[:, 1:] - arr[:, :-1])
col_edges = np.sum(dx > 30, axis=0)

# Print X-axis edge counts with 20px resolution
print("X-axis vertical edges count (X: 300 to 3100):")
for i in range(300, 3100, 20):
    chunk = col_edges[i:i+20]
    avg = int(np.mean(chunk))
    bar = "#" * (avg // 8)
    print(f"X {i:4d} to {i+20:4d}: {avg:5d} {bar}")
