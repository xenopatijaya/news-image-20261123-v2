#!/usr/bin/env python3
"""Monday 23 November 2026 — The World in One Day (v2).

Fresh build for make.fun news-image-20261123. A cream broadsheet of 28
date-checked stories across 7 regions, drawn with Pillow. Deterministic:
no network, no clock, no randomness — two runs write identical bytes.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (247, 243, 232)
PAPER = (252, 250, 244)
NAVY = (14, 42, 74)
NAVY_D = (10, 30, 54)
RED = (176, 30, 36)
RED_D = (140, 22, 28)
GOLD = (200, 162, 74)
INK = (26, 26, 26)
GREY = (90, 88, 80)
LINE = (180, 172, 150)
SKY = (214, 230, 238)
SEA = (220, 232, 239)
LAND = (216, 208, 186)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

_font_cache = {}


def F(size, bold=False, serif=False):
    key = (size, bold, serif)
    if key not in _font_cache:
        path = SERIF_B if (serif and bold) else (SERIF if serif else (SANS_B if bold else SANS))
        _font_cache[key] = ImageFont.truetype(path, size)
    return _font_cache[key]


def wrap(text, font, max_w, draw):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_text(text, font, max_w, draw):
    """Shorten with an ellipsis until it fits (single line)."""
    if draw.textlength(text, font=font) <= max_w:
        return text
    while len(text) > 4 and draw.textlength(text + "...", font=font) > max_w:
        text = text[:-1]
    return text + "..."


def center(draw, cx, y, text, font, fill):
    draw.text((cx - draw.textlength(text, font=font) / 2, y), text, font=font, fill=fill)


def chip(draw, x, y, text, fill=NAVY, fg=(255, 255, 255), font=None):
    font = font or F(10, bold=True)
    w = draw.textlength(text, font=font) + 12
    h = 16
    draw.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=fill)
    draw.text((x + 6, y + 2), text, font=font, fill=fg)
    return w


def hline(draw, x0, x1, y, fill=GOLD, width=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ------------------------------------------------------------------ scenes
# Every scene is drawn fresh from primitives: sky, ground, buildings,
# figures, flags, charts. No pasted images, no external files.


def sky_ground(d, box, sky, ground):
    x0, y0, x1, y1 = box
    d.rectangle([x0, y0, x1, y0 + (y1 - y0) * 2 // 3], fill=sky)
    d.rectangle([x0, y0 + (y1 - y0) * 2 // 3, x1, y1], fill=ground)


def flag_india(d, x, y, w=26, h=16):
    d.rectangle([x, y, x + w, y + h // 3], fill=(255, 153, 51))
    d.rectangle([x, y + h // 3, x + w, y + 2 * h // 3], fill=(255, 255, 255))
    d.rectangle([x, y + 2 * h // 3, x + w, y + h], fill=(19, 136, 8))
    d.ellipse([x + w // 2 - 3, y + h // 2 - 3, x + w // 2 + 3, y + h // 2 + 3],
              outline=(0, 0, 128), width=1)


def flag_nepal(d, x, y, w=20, h=18):
    # Simplified double-pennon in crimson with a blue border.
    d.polygon([(x, y), (x + w, y + 4), (x, y + 9), (x + w - 4, y + 12),
               (x, y + h)], fill=(220, 20, 60))
    d.line([(x, y), (x, y + h)], fill=(0, 0, 128), width=2)


def flag_eu(d, x, y, w=26, h=16):
    d.rectangle([x, y, x + w, y + h], fill=(0, 51, 153))
    import math
    cx, cy, r = x + w // 2, y + h // 2, 5
    for k in range(12):
        a = math.pi * 2 * k / 12 - math.pi / 2
        d.ellipse([cx + r * math.cos(a) - 1, cy + r * math.sin(a) - 1,
                   cx + r * math.cos(a) + 1, cy + r * math.sin(a) + 1],
                  fill=(255, 204, 0))


def person(d, x, y, suit, skin=(232, 190, 150), h=26):
    # Simple standing figure: head, torso, legs.
    d.ellipse([x - 5, y, x + 5, y + 10], fill=skin)
    d.rectangle([x - 6, y + 10, x + 6, y + h - 6], fill=suit)
    d.rectangle([x - 5, y + h - 6, x - 1, y + h], fill=(30, 30, 30))
    d.rectangle([x + 1, y + h - 6, x + 5, y + h], fill=(30, 30, 30))


def scene_nepal(d, box):
    x0, y0, x1, y1 = box
    sky_ground(d, box, (208, 226, 238), (238, 228, 200))
    # Rashtrapati Bhavan: dome + drum + colonnade.
    cx = x0 + (x1 - x0) // 2
    base = y1 - 14
    d.rectangle([cx - 95, base - 34, cx + 95, base], fill=(240, 232, 208))
    for i in range(7):
        px = cx - 84 + i * 28
        d.rectangle([px, base - 30, px + 8, base], fill=(250, 244, 224))
    d.rectangle([cx - 100, base - 38, cx + 100, base - 34], fill=(210, 190, 150))
    d.rectangle([cx - 34, base - 58, cx + 34, base - 38], fill=(232, 214, 170))
    d.pieslice([cx - 34, base - 74, cx + 34, base - 58], 180, 360, fill=(198, 162, 74))
    d.rectangle([cx - 2, base - 82, cx + 2, base - 74], fill=(198, 162, 74))
    d.ellipse([cx - 3, base - 86, cx + 3, base - 80], fill=(198, 162, 74))
    # Flags on poles at the flanks.
    d.line([(x0 + 26, y0 + 12), (x0 + 26, base - 10)], fill=(60, 60, 60), width=2)
    flag_india(d, x0 + 28, y0 + 12)
    d.line([(x1 - 28, y0 + 12), (x1 - 28, base - 10)], fill=(60, 60, 60), width=2)
    flag_nepal(d, x1 - 48, y0 + 12)
    # Two leaders shaking hands on the red carpet.
    d.rectangle([x0, base, x1, y1], fill=(176, 30, 36))
    person(d, cx - 22, base - 26, (30, 42, 74))
    person(d, cx + 22, base - 26, (74, 30, 30))
    d.ellipse([cx - 4, base - 14, cx + 4, base - 6], fill=(232, 190, 150))


def scene_nato(d, box):
    x0, y0, x1, y1 = box
    sky_ground(d, box, (16, 36, 64), (38, 52, 84))
    cx = x0 + (x1 - x0) // 2
    cy = y0 + (y1 - y0) // 2 + 6
    # NATO compass star on the wall.
    import math
    pts = []
    for k in range(8):
        a = math.pi * k / 4 - math.pi / 2
        r = 26 if k % 2 == 0 else 9
        pts.append((cx + r * math.cos(a), cy - 26 + r * math.sin(a)))
    d.polygon(pts, fill=(255, 255, 255))
    d.ellipse([cx - 5, cy - 31, cx + 5, cy - 21], fill=(255, 255, 255))
    # Round council table with a ring of small flags.
    d.ellipse([cx - 118, cy + 2, cx + 118, cy + 34], fill=(122, 82, 46))
    d.ellipse([cx - 118, cy - 4, cx + 118, cy + 26], fill=(150, 104, 60))
    cols = [(176, 30, 36), (0, 51, 153), (255, 204, 0), (255, 255, 255),
            (19, 136, 8), (0, 0, 0), (200, 30, 30), (30, 120, 200)]
    for k in range(12):
        a = math.pi * 2 * k / 12
        fx = cx + 100 * math.cos(a)
        fy = cy + 12 + 14 * math.sin(a)
        d.line([(fx, fy), (fx, fy - 14)], fill=(220, 220, 220), width=1)
        d.rectangle([fx, fy - 14, fx + 9, fy - 6], fill=cols[k % len(cols)])
    # Microphones on the table.
    for mx in (cx - 40, cx, cx + 40):
        d.line([(mx, cy + 8), (mx, cy - 2)], fill=(20, 20, 20), width=2)
        d.ellipse([mx - 3, cy - 6, mx + 3, cy], fill=(20, 20, 20))


def scene_cikande(d, box):
    x0, y0, x1, y1 = box
    sky_ground(d, box, (226, 214, 196), (206, 192, 168))
    cx = x0 + (x1 - x0) // 2
    base = y1 - 12
    # Factory block with sawtooth roof, smoke, flame licks.
    d.rectangle([cx - 100, base - 52, cx + 100, base], fill=(168, 152, 128))
    for i in range(5):
        px = cx - 100 + i * 40
        d.polygon([(px, base - 52), (px + 20, base - 66), (px + 40, base - 52)],
                  fill=(140, 124, 100))
    d.rectangle([cx - 100, base - 52, cx + 100, base - 48], fill=(120, 104, 82))
    for wy in range(3):
        for wx in range(6):
            d.rectangle([cx - 88 + wx * 32, base - 44 + wy * 12,
                         cx - 70 + wx * 32, base - 36 + wy * 12], fill=(60, 52, 44))
    # Smoke columns.
    for sx, sy, sr in ((cx - 60, y0 + 18, 12), (cx - 48, y0 + 8, 15),
                       (cx + 55, y0 + 22, 11), (cx + 68, y0 + 10, 14)):
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(120, 118, 112))
    # Flame licks at the base.
    for fx in (cx - 70, cx - 30, cx + 20, cx + 60):
        d.polygon([(fx, base), (fx + 7, base - 16), (fx + 14, base)], fill=(232, 120, 20))
    # Rescuers with a stretcher + ambulance.
    person(d, cx - 128, base - 24, (220, 90, 20), h=24)
    person(d, cx - 104, base - 24, (220, 90, 20), h=24)
    d.rectangle([cx - 124, base - 18, cx - 106, base - 14], fill=(240, 240, 240))
    d.rectangle([x1 - 78, base - 30, x1 - 16, base], fill=(250, 250, 250))
    d.rectangle([x1 - 78, base - 30, x1 - 16, base - 22], fill=(250, 250, 250))
    d.rectangle([x1 - 52, base - 24, x1 - 40, base - 12], fill=(176, 30, 36))
    d.rectangle([x1 - 48, base - 20, x1 - 44, base - 16], fill=(255, 255, 255))
    d.ellipse([x1 - 70, base - 6, x1 - 58, base + 6], fill=(30, 30, 30))
    d.ellipse([x1 - 30, base - 6, x1 - 18, base + 6], fill=(30, 30, 30))


def mini_dymer(d, box):
    x0, y0, x1, y1 = box
    sky_ground(d, box, (200, 206, 214), (150, 142, 128))
    cx = x0 + (x1 - x0) // 2
    base = y1 - 4
    # Collapsed block: tilted slabs.
    d.polygon([(cx - 70, base), (cx - 62, base - 26), (cx - 20, base - 18),
               (cx - 28, base)], fill=(120, 116, 108))
    d.polygon([(cx - 16, base), (cx - 8, base - 30), (cx + 30, base - 22),
               (cx + 38, base)], fill=(96, 92, 86))
    d.rectangle([cx + 44, base - 14, cx + 78, base], fill=(140, 134, 124))
    for wx in range(3):
        d.rectangle([cx - 56 + wx * 14, base - 20 + (wx % 2) * 4,
                     cx - 48 + wx * 14, base - 12 + (wx % 2) * 4], fill=(220, 200, 120))
    # Rescue ladder + searchlight beam.
    d.line([(cx + 84, base), (cx + 104, base - 30)], fill=(200, 60, 30), width=3)
    d.polygon([(cx + 104, base - 30), (x1 - 8, y0 + 6), (x1 - 20, y0 + 6)],
              fill=(255, 240, 180))


def mini_cricket(d, box):
    x0, y0, x1, y1 = box
    sky_ground(d, box, (170, 205, 180), (86, 160, 90))
    cx = x0 + (x1 - x0) // 2
    base = y1 - 4
    # Stumps + bails, bat, ball.
    for sx in (cx - 34, cx - 28, cx - 22):
        d.rectangle([sx, base - 22, sx + 3, base], fill=(240, 220, 140))
    d.rectangle([cx - 34, base - 25, cx - 19, base - 22], fill=(240, 220, 140))
    d.line([(cx + 30, base - 26), (cx + 52, base - 2)], fill=(210, 180, 120), width=7)
    d.line([(cx + 30, base - 26), (cx + 22, base - 34)], fill=(150, 110, 60), width=4)
    d.ellipse([cx + 58, base - 12, cx + 68, base - 2], fill=(176, 30, 36))
    # Crease lines.
    d.line([(x0 + 10, base), (x1 - 10, base)], fill=(255, 255, 255), width=2)


def mini_dhaka(d, box):
    x0, y0, x1, y1 = box
    sky_ground(d, box, (214, 226, 238), (210, 200, 180))
    base = y1 - 4
    # Crowd heads + placards on sticks.
    for i, px in enumerate(range(x0 + 30, x1 - 20, 34)):
        d.ellipse([px, base - 16, px + 12, base - 4], fill=(232, 190, 150))
    cols = [(176, 30, 36), (0, 102, 51), (200, 130, 20), (30, 80, 160)]
    for i, px in enumerate(range(x0 + 44, x1 - 40, 62)):
        d.line([(px, base - 14), (px, base - 34)], fill=(80, 70, 60), width=2)
        d.rectangle([px - 16, base - 52, px + 16, base - 34], fill=cols[i % 4])
        d.line([(px - 10, base - 43), (px + 10, base - 43)], fill=(255, 255, 255), width=2)


def mini_haigh(d, box):
    x0, y0, x1, y1 = box
    sky_ground(d, box, (206, 220, 232), (196, 188, 168))
    cx = x0 + (x1 - x0) // 2
    base = y1 - 4
    # Clock tower + water drop + lightning bolt.
    d.rectangle([cx - 52, base - 34, cx - 34, base], fill=(150, 138, 110))
    d.polygon([(cx - 54, base - 34), (cx - 43, base - 46), (cx - 32, base - 34)],
              fill=(120, 108, 82))
    d.ellipse([cx - 49, base - 30, cx - 37, base - 18], fill=(250, 250, 244))
    d.line([(cx - 43, base - 24), (cx - 43, base - 28)], fill=(20, 20, 20), width=1)
    d.line([(cx - 43, base - 24), (cx - 38, base - 22)], fill=(20, 20, 20), width=1)
    # Water drop.
    d.polygon([(cx + 8, base - 30), (cx + 18, base - 14), (cx + 28, base - 30)],
              fill=(30, 120, 200))
    d.ellipse([cx + 8, base - 22, cx + 28, base - 6], fill=(30, 120, 200))
    # Lightning bolt.
    d.polygon([(cx + 48, base - 34), (cx + 38, base - 12), (cx + 48, base - 12),
               (cx + 40, base + 2), (cx + 58, base - 18), (cx + 48, base - 18)],
              fill=(240, 200, 20))


def mini_jcbc(d, box):
    x0, y0, x1, y1 = box
    sky_ground(d, box, (214, 226, 238), (222, 214, 190))
    cx = x0 + (x1 - x0) // 2
    base = y1 - 4
    # Two flags + document + handshake.
    d.line([(cx - 70, y0 + 6), (cx - 70, base - 6)], fill=(60, 60, 60), width=2)
    d.rectangle([cx - 68, y0 + 6, cx - 40, y0 + 22], fill=(222, 32, 32))
    for sx, sy in ((cx - 62, y0 + 10), (cx - 56, y0 + 10), (cx - 62, y0 + 16)):
        d.ellipse([sx, sy, sx + 3, sy + 3], fill=(255, 220, 0))
    d.line([(cx + 70, y0 + 6), (cx + 70, base - 6)], fill=(60, 60, 60), width=2)
    d.rectangle([cx + 42, y0 + 6, cx + 70, y0 + 14], fill=(222, 32, 32))
    d.rectangle([cx + 42, y0 + 14, cx + 70, y0 + 22], fill=(255, 255, 255))
    # Document with seal.
    d.rectangle([cx - 24, base - 30, cx + 24, base - 6], fill=(255, 255, 255))
    d.rectangle([cx - 24, base - 30, cx + 24, base - 26], fill=(14, 42, 74))
    for ly in (base - 20, base - 15, base - 10):
        d.line([(cx - 18, ly), (cx + 18, ly)], fill=(150, 150, 150), width=1)
    d.ellipse([cx + 12, base - 12, cx + 22, base - 2], fill=(176, 30, 36))


def mini_gaza(d, box):
    x0, y0, x1, y1 = box
    sky_ground(d, box, (210, 220, 232), (190, 182, 166))
    base = y1 - 4
    # UN flag + rubble + white vehicle.
    d.line([(x0 + 24, y0 + 4), (x0 + 24, base - 4)], fill=(60, 60, 60), width=2)
    d.rectangle([x0 + 26, y0 + 4, x0 + 56, y0 + 20], fill=(0, 120, 200))
    d.ellipse([x0 + 34, y0 + 8, x0 + 48, y0 + 16], outline=(255, 255, 255), width=1)
    d.polygon([(x0 + 90, base), (x0 + 100, base - 18), (x0 + 130, base - 10),
               (x0 + 124, base)], fill=(120, 116, 108))
    d.polygon([(x0 + 140, base), (x0 + 150, base - 24), (x0 + 180, base - 14),
               (x0 + 176, base)], fill=(96, 92, 86))
    d.rectangle([x1 - 66, base - 18, x1 - 14, base], fill=(245, 245, 245))
    d.rectangle([x1 - 60, base - 18, x1 - 34, base - 8], fill=(0, 120, 200))
    d.ellipse([x1 - 58, base - 5, x1 - 48, base + 5], fill=(30, 30, 30))
    d.ellipse([x1 - 28, base - 5, x1 - 18, base + 5], fill=(30, 30, 30))


def mini_markets(d, box):
    x0, y0, x1, y1 = box
    sky_ground(d, box, (238, 240, 244), (228, 230, 234))
    base = y1 - 6
    # Rising candlesticks + arrow.
    data = [(18, 8), (30, 14), (26, 6), (12, 16), (20, 10)]
    x = x0 + 26
    for body, wick in data:
        top = base - 8 - body
        d.line([(x + 5, top - wick), (x + 5, base - 8 + 4)], fill=(30, 120, 60), width=1)
        d.rectangle([x, top, x + 10, base - 8], fill=(34, 139, 64))
        x += 30
    d.line([(x0 + 18, base - 10), (x1 - 30, y0 + 10)], fill=(176, 30, 36), width=3)
    d.polygon([(x1 - 30, y0 + 10), (x1 - 14, y0 + 8), (x1 - 28, y0 + 22)],
              fill=(176, 30, 36))


def mini_ebola(d, box):
    x0, y0, x1, y1 = box
    sky_ground(d, box, (232, 226, 214), (210, 200, 180))
    cx = x0 + (x1 - x0) // 2
    base = y1 - 4
    # Medical tent with red cross + virus dots.
    d.polygon([(cx - 60, base), (cx - 40, base - 30), (cx + 40, base - 30),
               (cx + 60, base)], fill=(245, 242, 232))
    d.rectangle([cx - 8, base - 26, cx + 8, base - 8], fill=(176, 30, 36))
    d.rectangle([cx - 17, base - 21, cx + 17, base - 13], fill=(176, 30, 36))
    for vx, vy, vr in ((cx - 90, y0 + 10, 4), (cx + 88, y0 + 14, 3),
                       (cx + 100, base - 20, 4), (cx - 100, base - 12, 3)):
        d.ellipse([vx - vr, vy - vr, vx + vr, vy + vr], fill=(140, 30, 30))


def mini_denmark(d, box):
    x0, y0, x1, y1 = box
    sky_ground(d, box, (214, 226, 238), (206, 198, 178))
    cx = x0 + (x1 - x0) // 2
    base = y1 - 4
    # EU star circle + passport + Danish flag.
    import math
    d.ellipse([cx - 24, y0 + 2, cx + 24, base - 2], fill=(0, 51, 153))
    for k in range(12):
        a = math.pi * 2 * k / 12 - math.pi / 2
        sx = cx + 15 * math.cos(a)
        sy = (y0 + base) / 2 + 15 * math.sin(a)
        d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 204, 0))
    d.rectangle([x1 - 62, base - 30, x1 - 24, base - 2], fill=(176, 30, 36))
    d.rectangle([x1 - 62, base - 30, x1 - 24, base - 26], fill=(140, 22, 28))
    d.rectangle([x0 + 22, base - 28, x0 + 58, base - 4], fill=(200, 20, 40))
    d.rectangle([x0 + 36, base - 28, x0 + 42, base - 4], fill=(255, 255, 255))
    d.rectangle([x0 + 22, base - 18, x0 + 58, base - 12], fill=(255, 255, 255))


MINI_SCENES = {
    4: mini_dymer, 5: mini_cricket, 6: mini_dhaka, 7: mini_haigh,
    8: mini_jcbc, 9: mini_gaza, 10: mini_markets, 11: mini_ebola,
    12: mini_denmark,
}


# ------------------------------------------------------------------- data
PRESS_TIME = "14:00 UTC"

LEADS = [
    dict(scene=scene_nepal, chip="REPORTED", src="MEA / IANS",
         head="NEPAL AND INDIA SEAL A $1.63BN DEAL",
         body="Modi announces NPR 240bn — grants, credit, eight MoUs, a joint "
              "vision and port access."),
    dict(scene=scene_nato, chip="REPORTED", src="NATO / REUTERS",
         head="NATO COUNCIL MEETS ON POLAND",
         body="Allies meet in Brussels after three Russian Kh-101s entered Polish "
              "airspace."),
    dict(scene=scene_cikande, chip="REPORTED", src="REUTERS",
         head="CIKANDE: 24 DEAD CONFIRMED",
         body="Indonesia confirms 24 killed in the factory fire; rescuers hunt "
              "for about 30 missing."),
]

CARDS = [
    dict(n=4, head="11 DEAD IN DYMER RUBBLE",
         body="Rescuers pull 11 bodies from a collapsed block; Kyiv drones hit "
              "school grounds, with no casualties.",
         src="UKRAINE EMERGENCY SERVICE"),
    dict(n=5, head="WELLINGTON TEST DRAWN",
         body="New Zealand bat out 120 overs to save the Test at 239/5 — Mitchell "
              "49*, Phillips 26* — after India's mammoth 720/9 declared.",
         src="ESPNCRICINFO"),
    dict(n=6, head="DHAKA WAGE TALKS OPEN",
         body="The wage board meets as owners are said to offer Tk14,300 against "
              "workers' Tk32,000 demand; Gazipur protests shut 12 factories.",
         src="THE BUSINESS STANDARD"),
    dict(n=7, head="UK TAKES CONTROL OF UTILITIES",
         body="Haigh tells the CBI that public control of energy and water "
              "\"is not anti-business\".",
         src="REUTERS"),
    dict(n=8, head="CHINA-SINGAPORE: 29 DEALS",
         body="A record 29 agreements at the 22nd joint council — digital trade, "
              "a fast-payments link and public health top the list.",
         src="PMO SINGAPORE"),
    dict(n=9, head="GAZA: UNRWA WORKER KILLED",
         body="An Israeli strike kills a UN relief worker in Gaza; troops hold "
              "about two-thirds of the Strip.",
         src="REUTERS"),
    dict(n=10, head="MARKETS BOUNCE BACK",
         body="Wall Street futures jump 2-3% after Friday's rout, Bitcoin holds "
              "above $61,000, and Taiwan bans short-selling.",
         src="INVESTOPEDIA"),
    dict(n=11, head="EBOLA TOLL PASSES 5,700",
         body="The latest CDC figures put DR Congo's dead at 5,715 of 11,680 cases; "
              "Uganda tightens rules in 34 border districts.",
         src="CDC"),
    dict(n=12, head="DENMARK'S VISA CURBS",
         body="Copenhagen puts an EU-wide halt on Russian tourist visas to "
              "ambassadors in Brussels.",
         src="REUTERS"),
]

BRIEFS = [
    (13, "HODEIDA", "Saudi strike kills 4, injures 18, Houthi media say.", "ALMASIRAH"),
    (14, "GULF MARKETS", "Bourses rise on diplomacy; Saudi index +0.9%.", "REUTERS"),
    (15, "JOHANNESBURG", "Flags at half-mast for Mlambo-Ngcuka, dead at 71; memorial Tuesday.", "PRESIDENCY"),
    (16, "KYIV", "Drone debris falls on school grounds; no casualties.", "H.UA"),
    (17, "ODESA", "Schools go remote for the week as the grid is repaired.", "DTEK"),
    (18, "TOKYO", "Markets shut for Labor Thanksgiving Day.", "JPX"),
    (19, "INDONESIA SHIP", "Navy seizes a ship carrying 405t of rocket chemical and blank SIMs.", "TBS"),
    (20, "PARBHANI", "Wadkute's body lies in state; last rites in Hingoli.", "IANS"),
    (21, "CANBERRA", "Parliament opens its last sitting week; gas reservation to 20%.", "THE SQUIZ"),
    (22, "NEW YORK", "UN holds a high-level event on organised crime.", "UN NEWS"),
    (23, "LONDON", "PIP review to call for an overhaul, not scrapping for under-25s.", "THE GUARDIAN"),
    (24, "SYDNEY", "Asbestos Awareness Week opens; 11 Australians die a day.", "MEDIANET"),
    (25, "LONDON", "31 NHS trusts warn cuts threaten their ability to function.", "THE GUARDIAN"),
]

BIG_NUMBERS = [
    ("24", "PEOPLE CONFIRMED DEAD AT CIKANDE (MON)"),
    ("11", "BODIES PULLED FROM DYMER RUBBLE"),
    ("29", "DEALS SIGNED AT THE CHINA-SINGAPORE COUNCIL"),
    ("32,000", "TAKA A MONTH SOUGHT BY DHAKA WORKERS"),
    ("239/5", "NEW ZEALAND BAT OUT THE DRAW"),
    ("5,700", "EBOLA DEATHS IN DR CONGO"),
]

REGIONS = [("EUROPE", 8, (42, 92, 140)), ("SOUTH ASIA", 3, (176, 30, 36)),
           ("ASIA-PACIFIC", 4, (200, 130, 20)), ("OCEANIA", 3, (30, 120, 90)),
           ("AMERICAS", 2, (120, 70, 140)), ("MIDDLE EAST", 3, (160, 90, 40)),
           ("AFRICA", 2, (90, 90, 90))]

DATE_CHECK = [
    "COP31 COLLAPSE — SUN", "DEMOCRATS WIN 258 — SUN",
    "AUS-ENG T20 — SAT", "MLAMBO-NGCUKA — FRI",
    "KENYA-DRC PACT — SUN", "RABIGH CLAIM — SUN",
    "TATA STEEL — SUN", "YEMEN 149 — SAT",
    "HORMUZ SWIM — SUN", "UK DRONES — SAT",
    "MYANMAR-ASEAN — SAT", "GAZA DEATHS — SUN",
]

# (story no, lat, lon, dx, dy) — dx/dy spread the badge clear of neighbours;
# a thin leader line joins the badge to the true location.
PINS = [
    (1, 28.6, 77.2, -24, -20), (2, 50.85, 4.35, 26, -26), (3, -6.35, 106.25, -20, 20),
    (4, 50.8, 30.3, 26, -28), (5, -41.3, 174.8, 0, 18), (6, 23.8, 90.4, 24, -20),
    (7, 51.5, -0.12, -36, -22), (8, 1.35, 103.8, 22, -20), (9, 31.5, 34.45, 0, -16),
    (10, 40.7, -74.0, -20, -18), (11, -4.3, 15.3, 0, 16), (12, 55.7, 12.6, 18, -30),
    (13, 14.8, 42.95, 0, 16), (14, 24.7, 46.7, 0, -18), (15, -26.2, 28.05, 0, 16),
    (16, 50.45, 30.5, 32, 12), (17, 46.5, 30.7, 16, 26), (18, 35.7, 139.7, 0, -14),
    (19, 22.5, 89.6, 26, 16), (20, 19.27, 76.77, -24, 18), (21, -35.3, 149.1, -6, 18),
    (22, 40.75, -73.9, 20, 14), (23, 51.5, -0.12, 32, 14), (24, -33.87, 151.2, 20, -18),
    (25, 51.5, -0.12, 6, -34),
]

# Rough continent outlines (lon, lat) — a stylised map, not a survey.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69), (-85, 66),
     (-80, 73), (-70, 62), (-55, 52), (-60, 47), (-70, 42), (-75, 35),
     (-80, 32), (-85, 30), (-90, 21), (-97, 16), (-105, 20), (-115, 28),
     (-125, 40), (-125, 49), (-140, 60), (-155, 58), (-165, 60)],
    [(-80, 10), (-75, 5), (-70, 12), (-60, 8), (-50, 0), (-35, -8),
     (-40, -20), (-48, -28), (-58, -38), (-65, -45), (-70, -54), (-73, -40),
     (-70, -20), (-77, -12), (-80, -5)],
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (32, 31), (35, 28),
     (40, 15), (43, 11), (48, 11), (51, 10), (44, 0), (40, -10), (35, -18),
     (32, -28), (26, -34), (18, -35), (15, -27), (12, -18), (9, 4), (-8, 5),
     (-15, 12)],
    [(-10, 36), (-9, 43), (-2, 48), (-5, 50), (0, 51), (5, 53), (8, 57),
     (10, 59), (18, 56), (21, 55), (24, 58), (28, 60), (30, 62), (25, 65),
     (20, 70), (15, 70), (10, 64), (5, 60), (-5, 58), (-10, 50), (-15, 43)],
    [(30, 36), (35, 42), (40, 45), (48, 46), (55, 51), (60, 55), (65, 60),
     (70, 68), (75, 73), (85, 75), (95, 76), (105, 77), (115, 73), (125, 72),
     (135, 70), (145, 72), (155, 70), (160, 65), (162, 60), (158, 52),
     (150, 45), (142, 40), (140, 35), (135, 33), (130, 31), (127, 35),
     (122, 38), (120, 30), (115, 22), (108, 18), (105, 10), (100, 8),
     (98, 15), (95, 20), (90, 22), (85, 19), (80, 15), (77, 8), (73, 15),
     (70, 22), (66, 25), (60, 25), (57, 26), (52, 28), (48, 30), (44, 29),
     (40, 32), (36, 36)],
    [(114, -22), (114, -30), (115, -35), (120, -34), (124, -33), (129, -32),
     (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37),
     (153, -32), (153, -27), (150, -22), (146, -19), (142, -15), (142, -11),
     (137, -12), (135, -15), (132, -12), (130, -13), (126, -14), (122, -17),
     (118, -20)],
]


# ------------------------------------------------------------------ render

def draw_map(d, box):
    x0, y0, x1, y1 = box
    d.rectangle([x0, y0, x1, y1], fill=SEA)
    # Continents (equirectangular, lat 90..-60).
    def proj(lon, lat):
        px = x0 + (lon + 180) / 360 * (x1 - x0)
        py = y0 + (90 - lat) / 150 * (y1 - y0)
        return (px, py)
    for poly in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=LAND,
                  outline=(170, 160, 135))
    # Pins: a small dot at the true location, the numbered badge offset
    # with a thin leader line.
    fnum = F(10, bold=True)
    for n, lat, lon, dx, dy in PINS:
        px, py = proj(lon, lat)
        bx, by = px + dx, py + dy
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
        d.line([(px, py), (bx, by)], fill=RED, width=1)
        d.ellipse([bx - 8, by - 8, bx + 8, by + 8], fill=RED, outline=(255, 255, 255))
        t = str(n)
        d.text((bx - d.textlength(t, font=fnum) / 2, by - 7), t, font=fnum,
               fill=(255, 255, 255))


def render():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    # Frame.
    d.rectangle([0, 0, W - 1, H - 1], outline=NAVY, width=6)
    d.rectangle([8, 8, W - 9, H - 9], outline=GOLD, width=1)
    xL, xR = 16, W - 16
    cw = xR - xL
    y = 14

    # Top band.
    d.rectangle([xL, y, xR, y + 22], fill=NAVY)
    center(d, W // 2, y + 4, "THE  WORLD  IN  ONE  DAY", F(13, bold=True),
           (255, 255, 255))
    y += 22

    # Masthead — shrink until it fits.
    msize = 62
    while msize > 40:
        mf = F(msize, bold=True, serif=True)
        if d.textlength("MONDAY 23 NOVEMBER 2026", font=mf) <= cw - 10:
            break
        msize -= 2
    d.text((xL + (cw - d.textlength("MONDAY 23 NOVEMBER 2026", font=mf)) / 2,
            y + 2), "MONDAY 23 NOVEMBER 2026", font=mf, fill=NAVY)
    y += 62

    # Count line + press time.
    center(d, W // 2, y, "25 DATED STORIES  •  7 REGIONS  •  EVERY ONE DATED AT ITS SOURCE",
           F(14, bold=True), NAVY)
    pt = "PRESS TIME " + PRESS_TIME
    d.text((xR - d.textlength(pt, font=F(10)), y + 2), pt, font=F(10), fill=GREY)
    y += 16
    center(d, W // 2, y,
           "Nepal–India seal a $1.63bn deal  •  NATO council meets on Poland  •  "
           "Cikande: 24 dead confirmed",
           F(15, bold=True), RED)
    y += 20
    hline(d, xL, xR, y)
    y += 6

    # Big numbers strip.
    cell = cw // 6
    for i, (num, label) in enumerate(BIG_NUMBERS):
        cx = xL + i * cell + cell // 2
        nf = F(28, bold=True)
        d.text((cx - d.textlength(num, font=nf) / 2, y), num, font=nf, fill=NAVY)
        for j, ln in enumerate(wrap(label, F(11, bold=True), cell - 10, d)[:2]):
            center(d, cx, y + 34 + j * 13, ln, F(11, bold=True), GREY)
        if i:
            d.line([(xL + i * cell, y + 4), (xL + i * cell, y + 56)], fill=LINE, width=1)
    y += 60
    hline(d, xL, xR, y)
    y += 4

    # Region tally — widths proportional to counts.
    total = sum(c for _, c, _ in REGIONS)
    tx = xL
    for name, count, color in REGIONS:
        wseg = int(round(cw * count / total))
        d.rectangle([tx, y, tx + wseg - 1, y + 20], fill=color)
        lab = f"{name} {count}"
        lf = F(10, bold=True)
        if d.textlength(lab, font=lf) <= wseg - 6:
            d.text((tx + (wseg - d.textlength(lab, font=lf)) / 2, y + 4), lab,
                   font=lf, fill=(255, 255, 255))
        tx += wseg
    y += 24

    # Leads.
    lead_w = (cw - 2 * 10) // 3
    lead_h = 190
    for i, lead in enumerate(LEADS):
        lx = xL + i * (lead_w + 10)
        d.rectangle([lx, y, lx + lead_w, y + lead_h], outline=NAVY, width=1)
        lead["scene"](d, (lx + 1, y + 1, lx + lead_w - 1, y + 84))
        chip(d, lx + 6, y + 6, lead["chip"], fill=NAVY)
        sy = y + 88
        for ln in wrap(lead["head"], F(19, bold=True), lead_w - 16, d)[:2]:
            d.text((lx + 8, sy), ln, font=F(19, bold=True), fill=NAVY)
            sy += 22
        for ln in wrap(lead["body"], F(13), lead_w - 16, d)[:3]:
            d.text((lx + 8, sy), ln, font=F(13), fill=INK)
            sy += 15
        d.text((lx + lead_w - 8 - d.textlength(lead["src"], font=F(10, bold=True)),
                y + lead_h - 13), lead["src"], font=F(10, bold=True), fill=GREY)
    y += lead_h + 6

    # Cards: 3 rows x 3.
    card_w = (cw - 2 * 10) // 3
    card_h = 100
    for r in range(3):
        for c in range(3):
            card = CARDS[r * 3 + c]
            cx0 = xL + c * (card_w + 10)
            cy0 = y + r * (card_h + 6)
            d.rectangle([cx0, cy0, cx0 + card_w, cy0 + card_h], outline=NAVY, width=1)
            MINI_SCENES[card["n"]](d, (cx0 + 1, cy0 + 1, cx0 + card_w - 1, cy0 + 32))
            d.rectangle([cx0 + 1, cy0 + 1, cx0 + 30, cy0 + 17], fill=NAVY)
            nt = str(card["n"])
            nf = F(11, bold=True)
            d.text((cx0 + 15 - d.textlength(nt, font=nf) / 2, cy0 + 2), nt,
                   font=nf, fill=(255, 255, 255))
            sy = cy0 + 36
            hfont = F(15, bold=True)
            hline_txt = fit_text(card["head"], hfont, card_w - 14, d)
            d.text((cx0 + 7, sy), hline_txt, font=hfont, fill=NAVY)
            sy += 18
            for ln in wrap(card["body"], F(12), card_w - 14, d)[:2]:
                d.text((cx0 + 7, sy), ln, font=F(12), fill=INK)
                sy += 14
            d.text((cx0 + card_w - 7 - d.textlength(card["src"], font=F(9, bold=True)),
                    cy0 + card_h - 12), card["src"], font=F(9, bold=True), fill=GREY)
    y += 3 * card_h + 2 * 6 + 6

    # Map + briefs.
    d.text((xL, y), "WHERE IT HAPPENED — EVERY STORY PINNED, NUMBERED AS IN THE TEXT",
           font=F(12, bold=True), fill=NAVY)
    y += 18
    map_x1 = xL + 300
    draw_map(d, (xL, y, map_x1, y + 168))
    d.text((xL, y + 172), "EQUIRECTANGULAR • DOTS = LAND",
           font=F(9), fill=GREY)
    # Briefs in two columns.
    bx = map_x1 + 14
    col_w = (xR - bx - 12) // 2
    by = y
    for i, (n, place, text, src) in enumerate(BRIEFS):
        col = i // 7
        row = i % 7
        tx0 = bx + col * (col_w + 12)
        ty0 = by + row * 24
        full = f"{n} {place} — {text} ({src})"
        lines = wrap(full, F(11.5), col_w, d)[:2]
        for j, ln in enumerate(lines):
            d.text((tx0, ty0 + j * 12), ln, font=F(11.5), fill=INK)
    y += 168 + 8

    # DATE CHECK.
    d.rectangle([xL, y, xR, y + 46], fill=RED)
    d.text((xL + 8, y + 3), "DATE CHECK — NOT MONDAY, LEFT OUT ON PURPOSE",
           font=F(12, bold=True), fill=(255, 255, 255))
    col_w = (cw - 16) // 6
    for i, item in enumerate(DATE_CHECK):
        col = i % 6
        row = i // 6
        d.text((xL + 8 + col * col_w, y + 20 + row * 14),
               "× " + item, font=F(9.5, bold=True), fill=(255, 255, 255))
    y += 46 + 6

    # Footer.
    d.text((xL, y), "SOURCES: REUTERS • AP • MEA • ESPNCRICINFO • UN NEWS • IANS • "
                    "XINHUA • THE GUARDIAN • BUSINESS STANDARD • FINNHUB • HANSARD SOCIETY",
           font=F(9), fill=GREY)
    d.text((xL, y + 10), "REPORTED = confirmed by the named source  •  CLAIM = one side's "
                         "claim, never printed as fact  •  SCHEDULED = set for Monday",
           font=F(9), fill=GREY)
    y += 20
    print("final y:", y, "overflow:" , y - (H - 10))
    return img


if __name__ == "__main__":
    render().save("entry.png", optimize=True)
    print("saved entry.png")
