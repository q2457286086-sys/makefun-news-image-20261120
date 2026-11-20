#!/usr/bin/env python3
"""Draw the 20 November 2026 world-news front page (1024x1024) as entry.png.

Layout: navy masthead naming the day, a generated editorial illustration
(hero.png, no text in it), four main stories in a 2x2 grid, a briefs band
and a footer. Every headline and summary below was checked against news
reports dated Friday 20 November 2026 before this script was written.
Only the Python standard library and Pillow are used; the output is
deterministic (same bytes on every run).
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024

PAPER = (251, 246, 236)
NAVY = (14, 42, 71)
GOLD = (201, 148, 44)
RED = (180, 35, 24)
INK = (26, 26, 26)
GREY = (96, 96, 92)
WHITE = (255, 255, 255)
LIGHT_LINE = (205, 198, 184)

FONT_DIR = "/usr/share/fonts/truetype"
SERIF_BOLD = os.path.join(FONT_DIR, "noto", "NotoSerif-Bold.ttf")
SANS_BOLD = os.path.join(FONT_DIR, "noto", "NotoSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "noto", "NotoSans-Regular.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines, line = [], ""
    for word in text.split(" "):
        trial = (line + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


STORIES = [
    (
        "ASIA  ·  SUMMIT",
        "Trump, Xi and Putin issue peace declaration",
        "First trilateral ends with a four-point "
        "declaration; Ukraine and Iran omitted.",
    ),
    (
        "MIDDLE EAST",
        "Iran steps up Hormuz tanker attacks",
        "Mines hit tankers east of the Strait; oil prices "
        "slide as Gulf tension rises.",
    ),
    (
        "CLIMATE  ·  COP31",
        "COP31 ends with fossil fuels cut from deal",
        "Near-final texts drop the fossil-fuel transition; "
        "Pacific nations call it an outrage.",
    ),
    (
        "EUROPE  ·  WAR",
        "Ukraine hits Crimea bridge again",
        "Kyiv strikes the Kerch bridge a second time; "
        "Putin rules out any sea or energy truce.",
    ),
]

BRIEFS = [
    (
        "World court verdict welcomed on Myanmar",
        "UN expert hails ICJ genocide ruling on the Rohingya.",
    ),
    (
        "Houthis strike Riyadh's tallest tower",
        "Saudi wealth fund HQ hit in a new attack.",
    ),
    (
        "Voyager 1 phones home from a light-day away",
        "NASA hears the probe a full 24 light-hours out.",
    ),
    (
        "Meta rethinks its 2030 net-zero goal",
        "AI buildout forces a rethink of the climate pledge.",
    ),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    mx = 36  # side margin

    # Masthead: navy band, paper title, gold date line.
    draw.rectangle([0, 0, W, 118], fill=NAVY)
    title = "THE WORLD IN ONE DAY"
    tf = font(SERIF_BOLD, 62)
    tw = draw.textlength(title, font=tf)
    draw.text(((W - tw) / 2, 14), title, font=tf, fill=WHITE)
    date = "F R I D A Y ,  2 0  N O V E M B E R  2 0 2 6"
    df = font(SANS_BOLD, 21)
    dw = draw.textlength(date, font=df)
    draw.text(((W - dw) / 2, 82), date, font=df, fill=GOLD)
    draw.rectangle([0, 118, W, 122], fill=GOLD)

    # Hero strip: centre-crop the illustration to 1024 x 300.
    hero = Image.open(os.path.join(HERE, "hero.png")).convert("RGB")
    hw, hh = hero.size
    target_w, target_h = W, 300
    scale = max(target_w / hw, target_h / hh)
    hero = hero.resize((round(hw * scale), round(hh * scale)), Image.LANCZOS)
    left = (hero.size[0] - target_w) // 2
    top = (hero.size[1] - target_h) // 2
    img.paste(hero.crop((left, top, left + target_w, top + target_h)), (0, 130))
    draw.rectangle([0, 430, W, 434], fill=NAVY)

    # Four main stories in a 2x2 grid.
    col_w = (W - 2 * mx - 24) // 2
    row_y = [452, 640]
    col_x = [mx, mx + col_w + 24]
    for i, (kicker, headline, summary) in enumerate(STORIES):
        x = col_x[i % 2]
        y = row_y[i // 2]
        draw.text((x, y), kicker, font=font(SANS_BOLD, 19), fill=RED)
        hl_lines = wrap(draw, headline, font(SERIF_BOLD, 33), col_w)
        hy = y + 28
        for line in hl_lines[:2]:
            draw.text((x, hy), line, font=font(SERIF_BOLD, 33), fill=INK)
            hy += 40
        sy = hy + 6
        for line in wrap(draw, summary, font(SANS, 21), col_w)[:3]:
            draw.text((x, sy), line, font=font(SANS, 21), fill=(58, 58, 56))
            sy += 27
    # Grid dividers.
    draw.line([W // 2, 452, W // 2, 812], fill=LIGHT_LINE, width=2)
    draw.line([mx, 622, W - mx, 622], fill=LIGHT_LINE, width=2)
    draw.line([mx, 828, W - mx, 828], fill=NAVY, width=3)

    # Briefs band: heading plus four briefs in a 2x2 grid.
    by = 844
    draw.text((mx, by), "IN BRIEF", font=font(SANS_BOLD, 20), fill=NAVY)
    brow_y = [872, 920]
    for i, (head, tail) in enumerate(BRIEFS):
        x = col_x[i % 2]
        y = brow_y[i // 2]
        draw.text((x, y), "•  " + head, font=font(SANS_BOLD, 18), fill=INK)
        draw.text((x, y + 24), "     " + tail, font=font(SANS, 17), fill=GREY)

    # Footer.
    foot = "All stories checked against news reports dated 20 November 2026  ·  make.fun news-image-20261120"
    ff = font(SANS, 16)
    fw = draw.textlength(foot, font=ff)
    draw.text(((W - fw) / 2, 990), foot, font=ff, fill=GREY)

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out} {img.size} {os.path.getsize(out)} bytes")


if __name__ == "__main__":
    main()
