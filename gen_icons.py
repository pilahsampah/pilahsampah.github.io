from PIL import Image, ImageDraw
import math, os

def draw_icon(size):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    r = int(size * 0.18)
    d.rounded_rectangle([0, 0, size-1, size-1], radius=r, fill="#1a7a4a")
    cx, cy = size // 2, size // 2
    ring_r = size * 0.34
    stroke = max(4, int(size * 0.075))
    bbox = [cx - ring_r, cy - ring_r, cx + ring_r, cy + ring_r]
    d.arc(bbox, start=30, end=300, fill="white", width=stroke)
    d.arc(bbox, start=150, end=420, fill="white", width=stroke)
    ar = int(size * 0.14)
    d.polygon([
        (cx, cy - ring_r - ar),
        (cx - ar, cy - ring_r + ar//2),
        (cx + ar, cy - ring_r + ar//2),
    ], fill="white")
    dot_r = int(size * 0.09)
    d.ellipse([cx - dot_r, cy - dot_r, cx + dot_r, cy + dot_r], fill="white")
    return img

out = "/Users/user/Desktop/pilahsampah/assets"
os.makedirs(out, exist_ok=True)

draw_icon(192).save(f"{out}/icon-192.png")
draw_icon(512).save(f"{out}/icon-512.png")
print("OK: icon-192.png dan icon-512.png berhasil dibuat")
