"""アプリアイコン（波とブイ）を docs/ に書き出す"""
import math, pathlib
from PIL import Image, ImageDraw

out = pathlib.Path(__file__).parent / "docs"
out.mkdir(exist_ok=True)
S = 1024
img = Image.new("RGB", (S, S), "#0f3a4a")
g = ImageDraw.Draw(img)
g.ellipse((600, 170, 830, 400), fill="#e0561c")  # 朝日（ブイの橙）
for k, (y, col) in enumerate([(560, "#5fb8cf"), (700, "#cfe6ea"), (840, "#ffffff")]):
    pts = [(x, y + 45 * math.sin(x / S * 2 * math.pi * 1.5 + k * 1.2)) for x in range(-10, S + 11, 8)]
    g.line(pts, fill=col, width=52, joint="curve")
for size in (512, 192, 180):
    img.resize((size, size), Image.LANCZOS).save(out / f"icon-{size}.png")
print("icons ok")
