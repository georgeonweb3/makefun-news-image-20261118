#!/usr/bin/env python3
"""Draw the 18 November 2026 world-news summary image (1024x1024 PNG).

One image, six stories, drawn programmatically with Pillow from the news
reported on Wednesday 18 November 2026. No photos, no scraped art: every
shape is code. Run: python3 draw.py  -> writes entry.png beside this file.

Stories (all first reported / happened 18 Nov 2026, cross-checked against
multiple news outlets the same day):
 1. US jets strike an Iranian missile site on Qeshm Island, Strait of Hormuz;
    Iran hits back at US bases in Kuwait and Bahrain.
 2. Trump lands in Shenzhen, China, for the first-ever trilateral with Xi
    Jinping and Vladimir Putin at the APEC summit (Thu 19 Nov).
 3. Cyclone Akvan strengthens to a severe cyclonic storm over the Bay of
    Bengal; landfall on India's Andhra Pradesh / Odisha coast expected Fri.
 4. Nvidia reports a record quarter: revenue $115.8bn (+103%), profit
    $65.3bn; board rules out ousted CEO Jensen Huang's return.
 5. Israel begins a "concentrated operation" in three areas of central Gaza.
 6. The United States loses its measles-free (elimination) status after
    26 years, as cases spread for over a year.
Footer ticker: Ukraine hits the Kerch Bridge a second day; Democrat Mary
Peltola wins the Alaska Senate seat (Democrats 56-44); magnitude 6 quake
in Papua New Guinea.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

NAVY = (11, 29, 51)
NAVY2 = (16, 42, 71)
GOLD = (212, 175, 55)
PAPER = (247, 243, 234)
INK = (17, 24, 33)
MUTED = (74, 84, 96)
WHITE = (255, 255, 255)

FONT_BLACK = "/usr/share/fonts/truetype/noto/NotoSans-Black.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_star(d, cx, cy, r, color):
    """Five-point star."""
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=color)


# ---------------------------------------------------------------- icons
def icon_hormuz(d, x, y, s):
    """Explosion burst over strait waves + tanker."""
    cx, cy = x + s // 2, y + s // 2 - 14
    for r, c in ((52, (255, 122, 26)), (40, (255, 176, 32)), (26, (255, 224, 102))):
        pts = []
        for i in range(16):
            ang = i * math.pi / 8
            rr = r if i % 2 == 0 else r * 0.62
            pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
        d.polygon(pts, fill=c)
    # tanker hull
    d.polygon([(x + 8, y + s - 34), (x + s - 8, y + s - 34),
               (x + s - 18, y + s - 20), (x + 18, y + s - 20)], fill=(38, 52, 68))
    d.rectangle([x + s // 2 - 16, y + s - 52, x + s // 2 + 16, y + s - 34],
                fill=(38, 52, 68))
    # waves (3 arcs, kept clear of the text column)
    for wy in (y + s - 14, y + s - 4):
        for k in range(3):
            wx = x + 6 + k * (s - 12) // 3
            d.arc([wx, wy - 5, wx + 22, wy + 7], 180, 360,
                  fill=(46, 134, 193), width=4)


def icon_summit(d, x, y, s):
    """Three small flags: USA, China, Russia, over a table arc."""
    fw, fh = s // 3 - 8, 44
    # USA: stripes + blue canton
    ux, uy = x + 2, y + 18
    for i in range(7):
        d.rectangle([ux, uy + i * fh // 7, ux + fw, uy + (i + 1) * fh // 7],
                    fill=(178, 34, 52) if i % 2 == 0 else WHITE)
    d.rectangle([ux, uy, ux + fw * 2 // 5, uy + fh * 4 // 7], fill=(28, 48, 94))
    draw_star(d, ux + fw // 5, uy + fh * 2 // 7, 5, WHITE)
    # China: red + stars
    cx0, cy0 = x + fw + 6, y + 18
    d.rectangle([cx0, cy0, cx0 + fw, cy0 + fh], fill=(222, 41, 16))
    draw_star(d, cx0 + 12, cy0 + 12, 7, (255, 222, 0))
    draw_star(d, cx0 + fw - 10, cy0 + 10, 4, (255, 222, 0))
    draw_star(d, cx0 + fw - 8, cy0 + fh - 10, 4, (255, 222, 0))
    # Russia: white / blue / red
    rx, ry = x + 2 * fw + 10, y + 18
    for i, c in enumerate((WHITE, (0, 57, 166), (213, 0, 50))):
        d.rectangle([rx, ry + i * fh // 3, rx + fw, ry + (i + 1) * fh // 3],
                    fill=c, outline=(120, 120, 120))
    # table arc
    d.arc([x + 6, y + s - 46, x + s - 6, y + s + 6], 180, 360,
          fill=GOLD, width=5)
    d.ellipse([x + s // 2 - 5, y + s - 24, x + s // 2 + 5, y + s - 14],
              fill=GOLD)


def icon_cyclone(d, x, y, s):
    """Spiral storm with rain."""
    cx, cy = x + s // 2, y + s // 2 - 6
    for k in range(4):
        r = 14 + k * 13
        d.arc([cx - r, cy - r, cx + r, cy + r],
              start=40 + k * 55, end=300 + k * 55,
              fill=(23, 120, 150) if k % 2 == 0 else (46, 170, 200), width=7)
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(23, 120, 150))
    for k in range(3):
        rx = x + 14 + k * 34
        d.line([(rx, y + s - 26), (rx - 6, y + s - 10)],
               fill=(46, 134, 193), width=4)


def icon_nvidia(d, x, y, s):
    """Green chip + rising chart arrow."""
    chip = (x + 12, y + 34, x + s - 34, y + s - 12)
    d.rounded_rectangle(chip, radius=10, fill=(118, 185, 0))
    for px in (chip[0] + 18, chip[0] + 44, chip[0] + 70):
        d.rectangle([px - 3, chip[1] - 12, px + 3, chip[1]], fill=(90, 140, 0))
        d.rectangle([px - 3, chip[3], px + 3, chip[3] + 12], fill=(90, 140, 0))
    d.rounded_rectangle([chip[0] + 16, chip[1] + 16, chip[2] - 16, chip[3] - 16],
                        radius=6, fill=(22, 60, 10))
    d.text((chip[0] + 24, chip[1] + 26), "AI", font=font(FONT_BOLD, 26),
           fill=WHITE)
    # rising arrow: diagonal shaft + arrowhead at the top right
    d.line([(x + s - 56, y + 30), (x + s - 12, y + 6)],
           fill=(22, 120, 40), width=6)
    d.polygon([(x + s - 12, y + 2), (x + s - 30, y + 4), (x + s - 14, y + 20)],
              fill=(22, 120, 40))


def icon_gaza(d, x, y, s):
    """Map pin over a small map outline with three marked areas."""
    # map outline
    d.rounded_rectangle([x + 10, y + 66, x + s - 10, y + s - 8], radius=10,
                        outline=(150, 140, 120), width=3)
    for px, py in ((x + 34, y + 92), (x + s // 2, y + 104),
                   (x + s - 34, y + 92)):
        d.ellipse([px - 7, py - 7, px + 7, py + 7],
                  outline=(178, 34, 52), width=3)
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(178, 34, 52))
    cx, cy = x + s // 2, y + 22
    d.ellipse([cx - 26, cy - 8, cx + 26, cy + 40], fill=(178, 34, 52))
    d.polygon([(cx - 20, cy + 28), (cx + 20, cy + 28), (cx, cy + 62)],
              fill=(178, 34, 52))
    d.ellipse([cx - 12, cy + 2, cx + 12, cy + 26], fill=WHITE)


def icon_measles(d, x, y, s):
    """Virus orb + crossed-out 26-year shield badge."""
    cx, cy = x + s // 2, y + s // 2 - 8
    for i in range(10):
        ang = i * math.pi / 5
        x1, y1 = cx + 26 * math.cos(ang), cy + 26 * math.sin(ang)
        x2, y2 = cx + 40 * math.cos(ang), cy + 40 * math.sin(ang)
        d.line([(x1, y1), (x2, y2)], fill=(200, 40, 40), width=5)
        d.ellipse([x2 - 5, y2 - 5, x2 + 5, y2 + 5], fill=(200, 40, 40))
    d.ellipse([cx - 28, cy - 28, cx + 28, cy + 28], fill=(220, 70, 60))
    d.ellipse([cx - 14, cy - 16, cx - 2, cy - 4], fill=(255, 150, 140))
    d.ellipse([cx + 6, cy + 6, cx + 16, cy + 16], fill=(255, 150, 140))
    d.ellipse([cx + 2, cy - 18, cx + 12, cy - 8], fill=(255, 150, 140))
    # "26 YRS" badge, struck through
    d.rounded_rectangle([x + 8, y + s - 30, x + s - 8, y + s - 6], radius=8,
                        fill=NAVY)
    d.text((x + s // 2, y + s - 18), "26 YEARS LOST",
           font=font(FONT_BOLD, 15), fill=WHITE, anchor="mm")


# ---------------------------------------------------------------- layout
STORIES = [
    ("MIDDLE EAST", (178, 34, 52), "US STRIKES IRAN",
     "Jets hit a missile site on Qeshm Island in the Strait of Hormuz. "
     "Iran hits back at US bases in Kuwait and Bahrain.",
     icon_hormuz),
    ("ASIA-PACIFIC", (28, 48, 94), "TRUMP LANDS IN CHINA",
     "First-ever trilateral with Xi and Putin set for Thursday at the "
     "APEC summit in Shenzhen.",
     icon_summit),
    ("CLIMATE", (23, 120, 150), "CYCLONE AKVAN CLOSES IN",
     "Severe storm strengthens over the Bay of Bengal. Landfall on "
     "India's east coast expected Friday.",
     icon_cyclone),
    ("MARKETS", (90, 140, 0), "NVIDIA DOUBLES REVENUE",
     "Record $115.8bn quarter, profit $65.3bn. The board rules out "
     "Jensen Huang's return as CEO.",
     icon_nvidia),
    ("MIDDLE EAST", (120, 60, 30), "NEW GAZA OPERATION",
     "Israel begins a \u201cconcentrated operation\u201d in three areas "
     "of central Gaza.",
     icon_gaza),
    ("HEALTH", (160, 40, 90), "US LOSES MEASLES-FREE STATUS",
     "Elimination status ends after 26 years as cases spread for "
     "over a year.",
     icon_measles),
]


def main():
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)

    # ---- header
    d.rectangle([0, 0, W, 168], fill=NAVY2)
    d.rectangle([0, 168, W, 174], fill=GOLD)
    d.text((32, 22), "WEDNESDAY 18 NOVEMBER 2026",
           font=font(FONT_BLACK, 54), fill=WHITE)
    d.text((32, 96), "THE WORLD IN ONE DAY  \u2014  SIX STORIES THAT DEFINED IT",
           font=font(FONT_BOLD, 25), fill=GOLD)

    # ---- story grid: 2 cols x 3 rows
    gx, gy = 16, 190
    pw, ph, gap = 488, 246, 16
    for i, (tag, color, head, sub, icon) in enumerate(STORIES):
        x = gx + (i % 2) * (pw + gap)
        y = gy + (i // 2) * (ph + gap)
        d.rounded_rectangle([x, y, x + pw, y + ph], radius=14, fill=PAPER)
        d.rounded_rectangle([x, y, x + pw, y + 10], radius=5, fill=color)
        # icon zone
        icon(d, x + 14, y + 22, 132)
        # tag
        tx = x + 162
        d.text((tx, y + 22), tag, font=font(FONT_BOLD, 19), fill=color)
        # headline
        lines = wrap(d, head, font(FONT_BOLD, 30), pw - 178)
        ly = y + 48
        for ln in lines[:2]:
            d.text((tx, ly), ln, font=font(FONT_BOLD, 30), fill=INK)
            ly += 34
        # subline
        sub_lines = wrap(d, sub, font(FONT_REG, 19), pw - 178)
        ly += 6
        for ln in sub_lines[:4]:
            d.text((tx, ly), ln, font=font(FONT_REG, 19), fill=MUTED)
            ly += 24

    # ---- footer ticker (panels end at y=960; footer is 960..1024)
    fy = 190 + 3 * ph + 2 * gap  # 960
    d.rectangle([0, fy, W, H], fill=NAVY2)
    d.rectangle([0, fy, W, fy + 4], fill=GOLD)
    d.text((32, fy + 10),
           "ALSO ON 18 NOV:  Ukraine hits the Kerch Bridge again  \u2022  Peltola wins",
           font=font(FONT_BOLD, 20), fill=WHITE)
    d.text((32, fy + 38),
           "Alaska Senate seat \u2014 Democrats 56\u201344  \u2022  Magnitude 6 quake in Papua New Guinea",
           font=font(FONT_REG, 20), fill=(200, 210, 220))

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes,", img.size)


if __name__ == "__main__":
    main()
