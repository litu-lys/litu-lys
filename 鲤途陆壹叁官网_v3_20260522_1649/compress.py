"""Compress all project images for GitHub Pages upload."""
import os
from PIL import Image

BASE = r"C:\Users\Administrator\Desktop\鲤途陆壹叁官网_v3_20260522_1649"
MAX_W = 1600
QUALITY = 80

def compress(inpath, outpath):
    img = Image.open(inpath).convert("RGB")
    w, h = img.size
    if w > MAX_W:
        ratio = MAX_W / w
        img = img.resize((MAX_W, int(h * ratio)), Image.LANCZOS)
    img.save(outpath, "JPEG", quality=QUALITY, optimize=True)

total_before = 0
total_after = 0
count = 0

for root, dirs, files in os.walk(BASE):
    for f in sorted(files):
        ext = f.lower()
        if not ext.endswith(('.jpg', '.jpeg', '.png')):
            continue
        inpath = os.path.join(root, f)
        if f.endswith('.png') and 'shop' not in root and 'logo' not in f:
            outname = f.rsplit('.',1)[0] + '.jpg'
        else:
            outname = f
        outpath = os.path.join(root, outname)
        size_before = os.path.getsize(inpath)
        compress(inpath, outpath)
        size_after = os.path.getsize(outpath)
        total_before += size_before
        total_after += size_after
        count += 1
        ratio = 100 * (1 - size_after/size_before)
        action = "  CONV" if outname != f else "  JPG"
        print(f"{action}  {f:<30}  {size_before//1024:>5}KB -> {size_after//1024:>5}KB  (-{ratio:.0f}%)")

print(f"\nDone: {count} images, {total_before/1e6:.1f}MB -> {total_after/1e6:.1f}MB")
