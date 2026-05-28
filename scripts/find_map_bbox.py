import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

image_path = "layout.jpg"
img = Image.open(image_path).convert('L')
width, height = img.size

print(f"Original image size: {width}x{height}")

# Let's downsample the top Y: 0 to 6000 region to analyze
map_height_limit = 6000
img_top = img.crop((0, 0, width, map_height_limit))

# Find vertical and horizontal projection of edges to locate the map
arr = np.array(img_top)

# Compute gradients (edges)
dy = np.abs(arr[1:, :] - arr[:-1, :])
dx = np.abs(arr[:, 1:] - arr[:, :-1])

# Sum edges horizontally and vertically
row_edges = np.sum(dy > 30, axis=1)
col_edges = np.sum(dx > 30, axis=0)

# Print profiles to locate grid lines
print("\nVertical slices (Y-axis edges count) at top region:")
for i in range(0, len(row_edges), 100):
    chunk = row_edges[i:i+100]
    avg = int(np.mean(chunk))
    bar = "#" * (avg // 50)
    print(f"Y {i:4d} to {i+100:4d}: {avg:5d} {bar}")

print("\nHorizontal slices (X-axis edges count):")
for i in range(0, len(col_edges), 150):
    chunk = col_edges[i:i+150]
    avg = int(np.mean(chunk))
    bar = "#" * (avg // 10)
    print(f"X {i:4d} to {i+150:4d}: {avg:5d} {bar}")
