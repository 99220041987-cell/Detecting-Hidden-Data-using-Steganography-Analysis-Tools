# steg_analyzer.py
# Basic steganalysis: LSB extraction + chi-square + entropy

import sys
import math
from collections import Counter
from PIL import Image

def image_to_rgb_bytes(img):
    if img.mode != "RGB":
        img = img.convert("RGB")
    pixels = list(img.getdata())
    r = [p[0] for p in pixels]
    g = [p[1] for p in pixels]
    b = [p[2] for p in pixels]
    return r, g, b, img.size

def extract_lsb_plane(channel, size):
    w, h = size
    lsb = [(v & 1) * 255 for v in channel]
    img = Image.new("L", (w, h))
    img.putdata(lsb)
    return img

def chi_square_lsb(channel):
    # Compare count of 0s and 1s in LSBs
    bits = [v & 1 for v in channel]
    counts = Counter(bits)
    o0 = counts.get(0, 0)
    o1 = counts.get(1, 0)
    total = o0 + o1
    if total == 0:
        return 0.0
    expected = total / 2.0
    # Chi-square for 2 categories
    chi = ((o0 - expected) ** 2) / expected + ((o1 - expected) ** 2) / expected
    return chi

def entropy(channel):
    counts = Counter(channel)
    total = len(channel)
    ent = 0.0
    for v in counts.values():
        p = v / total
        ent -= p * math.log2(p)
    return ent

def analyze_image(path, out_prefix="lsb"):
    img = Image.open(path)
    r, g, b, size = image_to_rgb_bytes(img)

    lsb_r = extract_lsb_plane(r, size)
    lsb_g = extract_lsb_plane(g, size)
    lsb_b = extract_lsb_plane(b, size)

    lsb_r.save(f"{out_prefix}_R.png")
    lsb_g.save(f"{out_prefix}_G.png")
    lsb_b.save(f"{out_prefix}_B.png")

    chi_r = chi_square_lsb(r)
    chi_g = chi_square_lsb(g)
    chi_b = chi_square_lsb(b)

    ent_r = entropy(r)
    ent_g = entropy(g)
    ent_b = entropy(b)

    print("=== Steganalysis Report ===")
    print(f"Image: {path}")
    print(f"Size: {size[0]}x{size[1]}")
    print("Chi-square (LSB 0/1 balance):")
    print(f"  R: {chi_r:.4f}  G: {chi_g:.4f}  B: {chi_b:.4f}")
    print("Entropy (0-8 bits):")
    print(f"  R: {ent_r:.4f}  G: {ent_g:.4f}  B: {ent_b:.4f}")
    print("Saved LSB planes as:")
    print(f"  {out_prefix}_R.png, {out_prefix}_G.png, {out_prefix}_B.png")
    print("Interpretation:")
    print("  Higher chi-square + very random LSB planes may indicate hidden data.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python steg_analyzer.py <image_path> [out_prefix]")
        sys.exit(1)
    img_path = sys.argv[1]
    prefix = sys.argv[2] if len(sys.argv) > 2 else "lsb"
    analyze_image(img_path, prefix)
