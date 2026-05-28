import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

image_path = "layout.jpg"
img = Image.open(image_path).convert('RGB')
width, height = img.size

# Let's resize it to 10% to quickly scan the color blobs
scale = 10
img_small = img.resize((width // scale, 3000 // scale), Image.Resampling.LANCZOS)
arr = np.array(img_small)

# Convert to HSV for better color thresholding
# We can do simple RGB thresholding since sections have distinct colors
# Let's sample colors in RGB:
# Green (A): roughly R < 120, G > 150, B < 120
# Cyan (B): roughly R < 120, G > 150, B > 150
# Yellow/Orange (C): roughly R > 200, G > 120, B < 100
# Purple/Indigo (D/E): roughly R > 100, G < 100, B > 150
# Pink (F): roughly R > 200, G < 100, B > 150
# Teal (G): roughly R < 120, G > 120, B > 100

print(f"Downsampled map size: {arr.shape[1]}x{arr.shape[0]}")

# Let's count colored pixels in horizontal and vertical bins
# to find where Section blocks are.
# We will print the RGB values at interesting grid points.
# Let's sample X coordinates: 100, 150, 200, 250, 300, 350, 400, 450
print("\nColor Grid Sample (Y: 10 to 250, X: 30 to 420):")
for y in range(10, 250, 10):
    row_chars = []
    for x in range(30, 420, 10):
        r, g, b = arr[y, x]
        # Classify color
        if r > 200 and g > 200 and b > 200:
            char = "." # White space
        elif r < 50 and g < 50 and b < 50:
            char = "P" # Pillar or Dark border
        elif g > 130 and r < 130 and b < 130:
            char = "A" # Greenish (A)
        elif g > 130 and b > 130 and r < 130:
            char = "B" # Cyanish (B)
        elif r > 160 and g > 130 and b < 100:
            char = "C" # Amber/Orange (C)
        elif r > 100 and b > 130 and g < 120:
            char = "E" # Purple/Pink (D/E/F)
        elif g > 120 and b > 120 and r > 120:
            char = "w" # Light gray/background
        else:
            char = "?" # Other color
        row_chars.append(char)
    print(f"Y {y*scale:4d}: " + "".join(row_chars))
