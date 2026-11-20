#!/usr/bin/env python3
"""Draw the 20 November 2026 front page: one 1024x1024 PNG.

Layout, top to bottom: navy masthead, gold rule, hero photo, a 2x2 grid of
main stories, a navy rule, an IN BRIEF block (2x2), and a footer line.
All headlines were verified against news reports dated 20 November 2026.
Run from the repo root:  python3 draw_frontpage.py  ->  entry.png
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BASE = os.path.dirname(os.path.abspath(__file__))

CREAM = (246, 241, 231)
NAVY = (27, 47, 74)
GOLD = (201, 162, 39)
RED = (176, 30, 30)
INK = (26, 26, 26)
GREY = (85, 85, 85)
FAINT = (170, 165, 155)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, fill, max_w, leading):
    """Draw wrapped text; returns the y just below the last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def tracked(draw, cx, y, text, fnt, fill, tracking):
    """Draw centred text with extra space between letters."""
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += w + tracking
    return total


def cover(im, w, h):
    """Resize + centre-crop so the image exactly covers w x h."""
    iw, ih = im.size
    scale = max(w / iw, h / ih)
    im = im.resize((round(iw * scale), round(ih * scale)), Image.LANCZOS)
    left = (im.width - w) // 2
    top = (im.height - h) // 2
    return im.crop((left, top, left + w, top + h))


MAIN = [
    ("ASIA \u00b7 SUMMIT", "Trump, Xi and Putin issue peace declaration",
     "First trilateral ends with a four-point declaration; Ukraine and Iran omitted."),
    ("MIDDLE EAST", "Iran steps up Hormuz tanker attacks",
     "Mines hit tankers east of the Strait; oil prices slide as Gulf tension rises."),
    ("CLIMATE \u00b7 COP31", "COP31 ends with fossil fuels cut from deal",
     "Near-final texts drop the fossil-fuel transition; Pacific nations call it an outrage."),
    ("EUROPE \u00b7 WAR", "Ukraine hits Crimea bridge again",
     "Kyiv strikes the Kerch bridge a second time; Putin rules out any sea or energy truce."),
]

BRIEFS = [
    ("World court verdict welcomed on Myanmar",
     "UN expert hails ICJ genocide ruling on the Rohingya."),
    ("Voyager 1 phones home from a light-day away",
     "NASA hears the probe a full 24 light-hours out."),
    ("Houthis strike Riyadh's tallest tower",
     "Saudi wealth fund HQ hit in a new attack."),
    ("Meta rethinks its 2030 net-zero goal",
     "AI buildout forces a rethink of the climate pledge."),
]


def story_cell(d, x, y, kicker, head, deck, col_w):
    """Draw one main story; returns the y just below its deck."""
    d.text((x, y), kicker, font=font(SANS_B, 17), fill=RED)
    y = para(d, x, y + 26, head, font(SERIF_B, 33), INK, col_w, 40)
    return para(d, x, y + 4, deck, font(SANS, 18), GREY, col_w, 24)


def brief_cell(d, x, y, title, sub, col_w):
    """Draw one brief; returns the y just below its sub."""
    d.text((x, y), "\u2022", font=font(SANS_B, 17), fill=INK)
    y = para(d, x + 22, y, title, font(SANS_B, 17), INK, col_w - 22, 22)
    return para(d, x + 22, y + 2, sub, font(SANS, 15), GREY, col_w - 22, 19)


def main():
    page = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(page)

    # --- masthead ---
    d.rectangle([0, 0, W, 108], fill=NAVY)
    d.text((W / 2, 22), "THE WORLD IN ONE DAY", font=font(SERIF_B, 62),
           fill=(255, 255, 255), anchor="ma")
    tracked(d, W / 2, 84, "FRIDAY, 20 NOVEMBER 2026", font(SANS_B, 19), GOLD, 5)
    d.rectangle([0, 108, W, 112], fill=GOLD)

    # --- hero photo ---
    hero = Image.open(os.path.join(BASE, "hero.png")).convert("RGB")
    page.paste(cover(hero, W, 300), (0, 112))

    # --- main stories: 2 columns x 2 rows, y flows from real cell bottoms ---
    col_w = 452
    xs = [36, 536]
    y = 436
    row1 = max(story_cell(d, xs[0], y, *MAIN[0], col_w),
               story_cell(d, xs[1], y, *MAIN[1], col_w))
    d.line([(512, y), (512, row1)], fill=FAINT, width=1)
    d.line([(36, row1 + 12), (988, row1 + 12)], fill=FAINT, width=1)
    y = row1 + 26
    row2 = max(story_cell(d, xs[0], y, *MAIN[2], col_w),
               story_cell(d, xs[1], y, *MAIN[3], col_w))
    d.line([(512, y), (512, row2)], fill=FAINT, width=1)

    # --- navy rule + IN BRIEF ---
    d.rectangle([36, row2 + 14, 988, row2 + 17], fill=NAVY)
    y = row2 + 30
    d.text((36, y), "IN BRIEF", font=font(SANS_B, 20), fill=NAVY)
    y += 34
    brow1 = max(brief_cell(d, xs[0], y, *BRIEFS[0], col_w),
                brief_cell(d, xs[1], y, *BRIEFS[1], col_w))
    y = brow1 + 16
    brief_cell(d, xs[0], y, *BRIEFS[2], col_w)
    brief_cell(d, xs[1], y, *BRIEFS[3], col_w)

    # --- footer ---
    d.text((W / 2, 984),
           "All stories checked against news reports dated 20 November 2026 "
           "\u00b7 make.fun news-image-20261120",
           font=font(SANS, 15), fill=GREY, anchor="ma")

    out = os.path.join(BASE, "entry.png")
    page.save(out, optimize=True)
    print("wrote", out)


if __name__ == "__main__":
    main()
