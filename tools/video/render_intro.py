#!/usr/bin/env python3

import os
from PIL import Image, ImageDraw, ImageFont

WIDTH = 1080
HEIGHT = 1080
FPS = 30
DURATION = 7
TOTAL_FRAMES = FPS * DURATION

os.makedirs("frames", exist_ok=True)

try:
    font_big = ImageFont.truetype("DejaVuSans-Bold.ttf", 80)
    font_small = ImageFont.truetype("DejaVuSans.ttf", 40)
except:
    font_big = ImageFont.load_default()
    font_small = ImageFont.load_default()

for frame in range(TOTAL_FRAMES):
    img = Image.new("RGB", (WIDTH, HEIGHT), (10, 10, 20))
    draw = ImageDraw.Draw(img)

    # Fade in title
    progress = min(1.0, frame / (FPS * 1.5))
    alpha = int(255 * progress)

    text = "ExNulla"
    w, h = draw.textsize(text, font=font_big)
    draw.text(((WIDTH - w) / 2, HEIGHT / 2 - 100),
              text, fill=(255, 255, 255), font=font_big)

    if frame > FPS * 2:
        text2 = "@exnulla"
        w2, h2 = draw.textsize(text2, font=font_small)
        draw.text(((WIDTH - w2) / 2, HEIGHT / 2 + 20),
                  text2, fill=(200, 200, 200), font=font_small)

    img.save(f"frames/frame_{frame:04d}.png")

print("Frames generated.")
print("Run ffmpeg to encode the video.")

