#!/usr/bin/env python3
"""Atlas of a Day — news-image-20261125, variant B.

Draws a 1024x1024 PNG from scratch with PIL: a world-map centrepiece with
numbered pins for 12 verified stories from Wednesday, 25 November 2026,
plus numbered story cards below. Fully deterministic — no timestamps,
no randomness, no date calls; the date string is embedded.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
DATE_STR = "Wednesday, 25 November 2026"

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


# Palette
NAVY = (15, 42, 68)
NAVY_DK = (10, 30, 50)
OCEAN = (214, 231, 242)
LAND = (232, 220, 196)
LAND_EDGE = (170, 152, 120)
INK = (22, 28, 36)
MUTED = (90, 100, 112)
HERO_RED = (192, 45, 30)
HERO_RED_DK = (150, 32, 20)
BLUE_PIN = (28, 92, 150)
CARD_BG = (255, 255, 255)
CARD_HERO_BG = (255, 244, 232)
CARD_EDGE = (200, 208, 216)
GOLD = (212, 160, 60)

# Map rect (equirectangular, lon -180..180, lat 78..-58)
MAP_X0, MAP_Y0, MAP_X1, MAP_Y1 = 10, 116, 1014, 490


def project(lon, lat):
    x = MAP_X0 + (lon + 180.0) / 360.0 * (MAP_X1 - MAP_X0)
    y = MAP_Y0 + (78.0 - lat) / 136.0 * (MAP_Y1 - MAP_Y0)
    return (x, y)


# Simplified continent outlines as (lon, lat) polygons.
CONTINENTS = [
    # North America
    [(-168, 66), (-150, 70), (-140, 70), (-130, 71), (-120, 70), (-110, 68),
     (-100, 69), (-90, 68), (-85, 66), (-80, 73), (-70, 62), (-60, 55),
     (-55, 52), (-60, 46), (-68, 44), (-74, 39), (-76, 35), (-80, 32),
     (-81, 26), (-84, 30), (-89, 29), (-91, 19), (-96, 16), (-100, 17),
     (-105, 20), (-110, 23), (-114, 28), (-120, 34), (-124, 42),
     (-124, 48), (-130, 55), (-140, 60), (-152, 58), (-162, 58),
     (-168, 60)],
    # South America
    [(-79, 9), (-77, 4), (-72, 11), (-64, 10), (-58, 8), (-52, 5),
     (-50, 0), (-44, -3), (-38, -5), (-35, -9), (-39, -15), (-40, -21),
     (-47, -26), (-51, -31), (-57, -35), (-62, -39), (-66, -43),
     (-69, -50), (-71, -53), (-73, -46), (-73, -36), (-71, -28),
     (-70, -19), (-75, -15), (-79, -8), (-81, -3), (-80, 2)],
    # Africa
    [(-17, 15), (-15, 22), (-10, 30), (-5, 35), (2, 37), (10, 37),
     (18, 33), (25, 32), (31, 31), (34, 28), (37, 22), (39, 18),
     (43, 11), (48, 11), (51, 10), (47, 3), (41, -2), (40, -8),
     (40, -15), (36, -22), (33, -27), (28, -33), (21, -35), (17, -31),
     (15, -27), (13, -19), (12, -12), (10, -3), (9, 3), (4, 6),
     (-4, 5), (-10, 5), (-15, 11)],
    # Europe
    [(-10, 36), (-9, 43), (-4, 44), (-2, 48), (0, 50), (3, 52),
     (6, 55), (8, 57), (11, 55), (16, 55), (20, 55), (23, 58),
     (26, 60), (28, 63), (30, 68), (28, 71), (22, 70), (16, 68),
     (12, 64), (7, 62), (5, 59), (2, 58), (-2, 54), (-5, 50),
     (-8, 46), (-10, 42), (-9, 38)],
    # Asia (with Arabian peninsula bulge)
    [(30, 70), (38, 68), (46, 69), (55, 69), (62, 69), (70, 72),
     (78, 73), (86, 74), (94, 76), (102, 77), (110, 76), (118, 73),
     (126, 72), (134, 71), (142, 72), (150, 70), (158, 69), (166, 66),
     (174, 66), (178, 65), (172, 62), (163, 60), (158, 53), (153, 58),
     (146, 58), (141, 50), (140, 42), (135, 43), (131, 39), (127, 35),
     (122, 31), (120, 26), (115, 22), (109, 18), (108, 11), (105, 9),
     (101, 7), (98, 10), (96, 15), (92, 21), (89, 22), (85, 19),
     (80, 13), (77, 8), (73, 16), (69, 22), (65, 25), (61, 25),
     (58, 25), (59, 22), (57, 19), (54, 17), (50, 15), (46, 13),
     (43, 15), (42, 19), (43, 24), (43, 29), (40, 31), (37, 35),
     (34, 36), (31, 36), (28, 37), (27, 40),
     (30, 42), (30, 46), (30, 52), (30, 58), (30, 64)],
    # Greenland
    [(-58, 64), (-52, 60), (-46, 60), (-40, 64), (-32, 68), (-24, 70),
     (-20, 73), (-28, 76), (-40, 77), (-52, 76), (-58, 73), (-60, 69)],
    # South-East Asian islands (Sumatra, Java, Borneo, New Guinea)
    [(95, 5), (99, 2), (102, -1), (105, -4), (109, -6), (113, -7),
     (117, -9), (121, -10), (125, -9), (129, -6), (131, -3), (135, -2),
     (140, -3), (145, -6), (149, -9), (146, -9), (141, -8), (136, -5),
     (131, -2), (126, 0), (121, 1), (116, 1), (111, 2), (106, 3),
     (101, 4), (97, 5)],
    # Australia
    [(114, -22), (114, -30), (116, -35), (122, -34), (128, -32),
     (132, -32), (136, -35), (140, -38), (146, -39), (150, -37),
     (153, -30), (153, -25), (150, -22), (146, -19), (142, -11),
     (137, -12), (132, -12), (128, -14), (124, -15), (120, -19),
     (116, -21)],
]

# (number, lon, lat, hero?)
PINS = [
    (1, 57.5, 26.5, True),    # Strait of Hormuz
    (2, 47.0, 24.0, True),    # Riyadh / Ras Tanura
    (3, 43.8, 15.0, True),    # Hodeidah
    (4, -75.5, 10.4, True),   # Cartagena
    (5, 100.3, 39.8, True),   # Jiuquan / Tiangong
    (6, 139.7, 35.7, True),   # Tokyo markets
    (7, 90.4, 23.8, False),   # Dhaka
    (8, 160.0, -9.4, False),  # Honiara
    (9, 127.0, 37.5, False),  # Seoul
    (10, 106.8, -6.6, False), # Bogor
    (11, 114.2, 22.3, False), # Hong Kong
    (12, 44.5, 33.0, False), # Baghdad / Kurdistan
]

# (number, headline, summary, source, hero?)
STORIES = [
    (1, "Two tankers hit mines in the Strait of Hormuz",
     "Tankers explode and burn; Iran keeps the strait shut.",
     "Reuters", True),
    (2, "Houthis strike Ras Tanura refinery and Riyadh",
     "Saudi defences intercept four drones at Ras Tanura.",
     "Reuters", True),
    (3, "Saudi-led coalition strikes Hodeidah port",
     "Strikes follow evacuation; Houthis threaten ports.",
     "WireMinute", True),
    (4, "All hostages freed in dawn raid in Cartagena",
     "Special forces storm supermarket; captor killed.",
     "Reuters / AFP", True),
    (5, "Pakistan's first astronaut reaches Tiangong",
     "Shenzhou-24 launches 08:18, docks 11:56.",
     "Reuters / Xinhua", True),
    (6, "Markets slide on a fresh US tariff threat",
     "Nasdaq futures -2%+, Nikkei -2.76% on US tariff plans.",
     "Reuters", True),
    (7, "Bangladesh garment wage rises 36%",
     "Minimum wage lifted after weeks of protests.",
     "WireMinute", False),
    (8, "Australia-Solomon Islands security treaty signed",
     "Wide pact excludes foreign bases; shift from China.",
     "WireMinute", False),
    (9, "Russian jets enter South Korea air defence zone",
     "Seoul reports Russian aircraft in its defence zone.",
     "SRI", False),
    (10, "Three bodies found in flooded Bogor gold mine",
     "26 miners still trapped about 100 m down in Pongkor.",
     "Reuters", False),
    (11, "Hong Kong mourns 168 dead, a year after Tai Po fire",
     "Residents mark one year since the Wang Fuk blaze.",
     "Reuters", False),
    (12, "Iraq orders federal forces to seize Kurdish oilfields",
     "PM orders the takeover of oilfields and crossings.",
     "Starlit Daily", False),
]


def fit_text(draw, text, fnt, max_w):
    """Truncate with an ellipsis so text fits max_w pixels."""
    if draw.textlength(text, font=fnt) <= max_w:
        return text
    ell = "..."
    lo, hi = 0, len(text)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if draw.textlength(text[:mid] + ell, font=fnt) <= max_w:
            lo = mid
        else:
            hi = mid - 1
    return text[:lo].rstrip() + ell


def wrap_text(draw, text, fnt, max_w, max_lines):
    """Greedy word wrap, capped at max_lines; last line gets an ellipsis."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = fit_text(draw, lines[-1], fnt, max_w)
    return lines


def draw_map(draw):
    draw.rectangle([MAP_X0, MAP_Y0, MAP_X1, MAP_Y1], fill=OCEAN)
    # faint graticule
    for lon in range(-150, 181, 30):
        x, _ = project(lon, 0)
        draw.line([(x, MAP_Y0), (x, MAP_Y1)], fill=(190, 208, 222), width=1)
    for lat in (60, 30, 0, -30):
        _, y = project(0, lat)
        draw.line([(MAP_X0, y), (MAP_X1, y)], fill=(190, 208, 222), width=1)
    for poly in CONTINENTS:
        pts = [project(lon, lat) for lon, lat in poly]
        draw.polygon(pts, fill=LAND, outline=LAND_EDGE)
    # ocean labels
    f_lab = font(SANS_B, 15)
    draw.text(project(-130, -28), "PACIFIC", font=f_lab, fill=(150, 172, 190))
    draw.text(project(-35, -32), "ATLANTIC", font=f_lab, fill=(150, 172, 190))
    draw.text(project(85, -38), "INDIAN OCEAN", font=f_lab, fill=(150, 172, 190))
    # pins
    for num, lon, lat, hero in PINS:
        x, y = project(lon, lat)
        r = 13 if hero else 11
        col = HERO_RED if hero else BLUE_PIN
        draw.ellipse([x - r, y - r, x + r, y + r], fill=col,
                     outline=(255, 255, 255), width=3)
        f_num = font(SANS_B, 15 if hero else 13)
        tw = draw.textlength(str(num), font=f_num)
        th = f_num.getbbox(str(num))[3]
        draw.text((x - tw / 2, y - th / 2 - 1), str(num), font=f_num,
                  fill=(255, 255, 255))


def draw_cards(draw):
    f_head = font(SANS_B, 18)
    f_sum = font(SANS, 13)
    f_src = font(SANS_B, 12)
    f_badge = font(SANS_B, 16)
    x0, y0 = 10, 500
    cw, ch, gap = 496, 76, 6
    for i, (num, head, summ, src, hero) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x = x0 + col * (cw + gap)
        y = y0 + row * (ch + gap)
        bg = CARD_HERO_BG if hero else CARD_BG
        draw.rounded_rectangle([x, y, x + cw, y + ch], radius=8,
                               fill=bg, outline=CARD_EDGE, width=1)
        if hero:
            draw.rectangle([x, y + 6, x + 5, y + ch - 6], fill=HERO_RED)
        # number badge
        bx, by, br = x + 14, y + ch // 2, 15
        col_pin = HERO_RED if hero else BLUE_PIN
        draw.ellipse([bx - br, by - br, bx + br, by + br], fill=col_pin)
        tw = draw.textlength(str(num), font=f_badge)
        th = f_badge.getbbox(str(num))[3]
        draw.text((bx - tw / 2, by - th / 2 - 1), str(num), font=f_badge,
                  fill=(255, 255, 255))
        tx = x + 40
        tw_max = cw - 40 - 10
        lines = wrap_text(draw, head, f_head, tw_max, 2)
        ly = y + 8
        for ln in lines:
            draw.text((tx, ly), ln, font=f_head, fill=INK)
            ly += 21
        summ_y = y + 8 + 21 * len(lines)
        sw = draw.textlength(src, font=f_src)
        s = fit_text(draw, summ, f_sum, tw_max - sw - 10)
        draw.text((tx, summ_y), s, font=f_sum, fill=MUTED)
        # source tag, right-aligned on the summary line
        draw.text((x + cw - 10 - sw, summ_y), src, font=f_src, fill=(150, 105, 20))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    img = Image.new("RGB", (W, H), (248, 247, 243))
    draw = ImageDraw.Draw(img)

    # Header banner
    draw.rectangle([0, 0, W, 104], fill=NAVY)
    draw.rectangle([0, 104, W, 108], fill=GOLD)
    f_date = font(SERIF_B, 46)
    dw = draw.textlength(DATE_STR, font=f_date)
    draw.text(((W - dw) / 2, 12), DATE_STR, font=f_date, fill=(255, 255, 255))
    f_sub = font(SANS_B, 17)
    sub = "A T L A S   O F   A   D A Y   \u00b7   1 2   S T O R I E S   F R O M   A R O U N D   T H E   W O R L D"
    sw = draw.textlength(sub, font=f_sub)
    draw.text(((W - sw) / 2, 68), sub, font=f_sub, fill=(212, 160, 60))

    draw_map(draw)
    draw_cards(draw)

    # Footer
    f_foot = font(SANS, 13)
    foot = "Sources: Reuters \u00b7 AFP \u00b7 Xinhua \u00b7 WireMinute \u00b7 SRI \u00b7 Starlit Daily  \u2014  All events reported Wednesday, 25 November 2026"
    fw = draw.textlength(foot, font=f_foot)
    draw.text(((W - fw) / 2, 994), foot, font=f_foot, fill=MUTED)

    os.makedirs(out_dir, exist_ok=True)
    img.save(os.path.join(out_dir, "entry.png"), format="PNG")


if __name__ == "__main__":
    main()
