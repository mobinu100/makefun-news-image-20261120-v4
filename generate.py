#!/usr/bin/env python3
"""V4: THE WORLD TODAY — one-image front page of Friday 20 November 2026.

Draws entry.png (1024x1024, deterministic, no network, no external images).
Design: newspaper front page. Masthead + date, drawn dusk-Shenzhen hero scene
with the three-leader summit lead, 9 featured stories in a 3x3 grid (every
kicker dated "20 NOV"), and a MORE strip of 8 concrete items. Total 18 stories.
Plain, attributed wording throughout; no hype words; every number appears in
exactly one place on the page (Anthropic's three prices live in a single
consistent line only).
"""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (246, 240, 220)
INK = (26, 26, 26)
RED = (163, 30, 34)
GREY = (84, 78, 66)
RULE = (26, 26, 26)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
COND_B = "/usr/share/fonts/truetype/noto/NotoSans-CondensedBold.ttf"
COND = "/usr/share/fonts/truetype/noto/NotoSans-Condensed.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines, each fitting max_w."""
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
    return lines


def draw_rule(draw, x0, x1, y, width=2):
    draw.line([(x0, y), (x1, y)], fill=RULE, width=width)


# ---------------------------------------------------------------- data
HERO_KICKER = "SHENZHEN, CHINA \u2022 20 NOV \u2022 THE THREE-WAY SUMMIT"
HERO_HEADLINE = "THREE LEADERS SIGN PEACE DECLARATION"
HERO_DECK = "Declaration: \u2018A nuclear war cannot be won and must never be fought.\u2019"

# (place, icon, headline, deck) — decks at most 5 words, except the Anthropic
# line, which must carry all three prices in one consistent place.
FEATURED = [
    ("THE HAGUE", "scales", "MYANMAR IS GUILTY", "ICJ: genocide, 9\u20136."),
    ("WALL ST", "bars", "ANTHROPIC DEBUTS", "IPO $83, opens $111.50, closes $97.17"),
    ("INDIA", "cloud", "CYCLONE AKVAN HITS ODISHA", "300,000 evacuated."),
    ("WASHINGTON", "dome", "SENATE BACKS TRUMP ON IRAN", "Curb fails 51\u201348."),
    ("RIYADH", "tower", "HOUTHI STRIKE HITS RIYADH", "Tower hit; none hurt."),
    ("MARKETS", "arrow", "STOCKS SLIDE ON AI FEARS", "Nvidia \u22123.3%."),
    ("SPACE", "star", "VOYAGER 1, ONE LIGHT-DAY", "Signals take a full day."),
    ("TOKYO", "probe", "HAYABUSA2 LANDING OFF", "2031 landing called off."),
    ("CULTURE", "pad", "GTA VI SELLS 24.6M COPIES", "Sensor Tower: $2.36bn."),
]

MORE = [
    "69 trains halted",
    "Dow drops 1,101",
    "GTA VI: 75% on PS5",
    "Dems take Congress",
    "ICJ: 10,000 killed",
    "Voyager 2 in 2035",
    "9,341 shelters ready",
    "Fuel output to rise",
]

FOOTER_LEFT = "All stories reported Friday, 20 November 2026"
FOOTER_RIGHT = "Sources: Reuters \u2022 AP \u2022 BBC \u2022 IMD"

BANNED = ["first-ever", "largest ever", "record", "smashes",
          "Bigger than Yalta", "historic"]

TOTAL_STORIES = 1 + len(FEATURED) + len(MORE)
assert TOTAL_STORIES == 18, TOTAL_STORIES
ALL_TEXT = [HERO_KICKER, HERO_HEADLINE, HERO_DECK, FOOTER_LEFT, FOOTER_RIGHT]
for _p, _i, _h, _d in FEATURED:
    ALL_TEXT += [_h, _d]
ALL_TEXT += MORE
for _t in ALL_TEXT:
    for _b in BANNED:
        assert _b.lower() not in _t.lower(), ("hype word in text:", _t)


# ---------------------------------------------------------------- icons
def draw_icon(draw, kind, x, y, s=22, color=RED):
    """Small beat icon, drawn with primitives, inside a s x s box at (x, y)."""
    if kind == "scales":
        draw.line([(x + s // 2, y + 2), (x + s // 2, y + s - 4)], fill=color, width=2)
        draw.line([(x + 2, y + 5), (x + s - 2, y + 5)], fill=color, width=2)
        draw.polygon([(x + 1, y + s - 3), (x + 7, y + s - 3), (x + 4, y + 8)], fill=color)
        draw.polygon([(x + s - 7, y + s - 3), (x + s - 1, y + s - 3), (x + s - 4, y + 8)], fill=color)
    elif kind == "bars":
        for i, h in enumerate((8, 13, 18)):
            bx = x + 2 + i * 7
            draw.rectangle([bx, y + s - 2 - h, bx + 5, y + s - 2], fill=color)
    elif kind == "cloud":
        draw.ellipse([x + 2, y + 6, x + 12, y + 14], fill=color)
        draw.ellipse([x + 9, y + 3, x + 20, y + 13], fill=color)
        for dx in (5, 11, 17):
            draw.line([(x + dx, y + 16), (x + dx, y + 20)], fill=color, width=2)
    elif kind == "dome":
        draw.pieslice([x + 3, y + 2, x + s - 3, y + 14], 180, 360, fill=color)
        draw.rectangle([x + 2, y + 13, x + s - 2, y + s - 3], fill=color)
    elif kind == "tower":
        draw.rectangle([x + 7, y + 4, x + s - 7, y + s - 2], fill=color)
        draw.polygon([(x + 7, y + 4), (x + s - 7, y + 4), (x + s // 2, y)], fill=color)
    elif kind == "arrow":
        draw.polygon([(x + s // 2, y + s - 2), (x + 2, y + 8), (x + 8, y + 8),
                      (x + 8, y + 2), (x + s - 8, y + 2), (x + s - 8, y + 8),
                      (x + s - 2, y + 8)], fill=color)
    elif kind == "star":
        cx, cy = x + s // 2, y + s // 2
        draw.polygon([(cx, cy - 10), (cx + 3, cy - 3), (cx + 10, cy), (cx + 3, cy + 3),
                      (cx, cy + 10), (cx - 3, cy + 3), (cx - 10, cy), (cx - 3, cy - 3)],
                     fill=color)
    elif kind == "probe":
        draw.ellipse([x + 5, y + 4, x + s - 5, y + s - 6], outline=color, width=2)
        draw.ellipse([x + 9, y + 8, x + s - 9, y + s - 10], fill=color)
        draw.line([(x + 2, y + s - 4), (x + s - 2, y + 4)], fill=color, width=2)
    elif kind == "pad":
        draw.rounded_rectangle([x + 1, y + 5, x + s - 1, y + s - 5], radius=4,
                               outline=color, width=2)
        draw.line([(x + 6, y + s // 2), (x + 11, y + s // 2)], fill=color, width=2)
        draw.line([(x + 8, y + s // 2 - 2), (x + 8, y + s // 2 + 3)], fill=color, width=2)
        draw.ellipse([x + 14, y + 9, x + 17, y + 12], fill=color)
        draw.ellipse([x + 17, y + 12, x + 20, y + 15], fill=color)


# ---------------------------------------------------------------- hero scene
def draw_hero_scene(draw, x0, x1, y0, y1):
    """Dusk Shenzhen skyline: gradient sky, stars, moon, lit towers, three
    flags and three leaders at a table. All shapes are fixed primitives."""
    # gradient sky, dark blue-violet to warm orange at the horizon
    top = (31, 42, 77)
    bot = (232, 147, 90)
    for yy in range(y0, y1):
        t = (yy - y0) / max(1, (y1 - y0))
        c = tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3))
        draw.line([(x0, yy), (x1, yy)], fill=c)
    # stars (fixed)
    for sx, sy in [(60, 8), (150, 20), (260, 6), (400, 16), (520, 8), (660, 18),
                   (780, 6), (900, 14), (330, 26), (590, 26), (850, 26)]:
        draw.ellipse([x0 + sx - 1, y0 + sy - 1, x0 + sx + 1, y0 + sy + 1], fill=(245, 240, 220))
    # moon
    draw.ellipse([x1 - 70, y0 + 8, x1 - 38, y0 + 40], fill=(245, 238, 210))
    # skyline: (left offset, width, height fraction of scene) — heights must
    # stay inside the scene so nothing pokes into the dateline band above.
    sh = y1 - y0
    buildings = [(0, 70, .62), (78, 52, .84), (138, 64, .58), (210, 46, .78),
                 (264, 72, .66), (344, 50, .88), (402, 60, .56), (470, 48, .80),
                 (526, 66, .62), (600, 54, .86), (662, 60, .58), (730, 48, .82),
                 (786, 66, .64), (860, 52, .88), (920, 60, .60)]
    for bx, bw, bf in buildings:
        bh = int(sh * bf)
        draw.rectangle([x0 + bx, y1 - bh, x0 + bx + bw, y1], fill=(20, 24, 36))
        for wy in range(y1 - bh + 8, y1 - 6, 12):
            for wx in range(x0 + bx + 7, x0 + bx + bw - 6, 12):
                if (wx * 7 + wy * 13) % 5 < 3:
                    draw.rectangle([wx, wy, wx + 4, wy + 5], fill=(245, 197, 66))
    # table
    draw.rectangle([x0 + 300, y1 - 14, x1 - 300, y1 - 7], fill=(90, 52, 32))
    # three leaders: (centre x, suit colour) with a flag on a pole behind each
    leaders = [(x0 + 380, (38, 48, 96)), (x0 + 490, (122, 28, 32)), (x0 + 600, (30, 30, 30))]
    flags = ["us", "cn", "ru"]
    for (cx, suit), flag in zip(leaders, flags):
        # flag pole + flag
        draw.line([(cx - 46, y1 - 64), (cx - 46, y1 - 40)], fill=(220, 220, 210), width=2)
        if flag == "us":
            for s in range(3):
                draw.rectangle([cx - 44, y1 - 64 + s * 7, cx - 14, y1 - 58 + s * 7],
                               fill=(178, 34, 52) if s % 2 == 0 else (240, 240, 235))
            draw.rectangle([cx - 44, y1 - 64, cx - 30, y1 - 53], fill=(38, 48, 96))
        elif flag == "cn":
            draw.rectangle([cx - 44, y1 - 64, cx - 14, y1 - 43], fill=(222, 41, 16))
            draw.ellipse([cx - 41, y1 - 61, cx - 35, y1 - 55], fill=(255, 222, 0))
        else:
            draw.rectangle([cx - 44, y1 - 64, cx - 14, y1 - 57], fill=(240, 240, 235))
            draw.rectangle([cx - 44, y1 - 57, cx - 14, y1 - 50], fill=(0, 57, 166))
            draw.rectangle([cx - 44, y1 - 50, cx - 14, y1 - 43], fill=(213, 0, 50))
        # figure: head + shoulders behind the table
        draw.ellipse([cx - 12, y1 - 40, cx + 12, y1 - 16], fill=(232, 196, 160))
        draw.polygon([(cx - 22, y1 - 7), (cx - 18, y1 - 24), (cx - 7, y1 - 20),
                      (cx, y1 - 27), (cx + 7, y1 - 20), (cx + 18, y1 - 24),
                      (cx + 22, y1 - 7)], fill=suit)
        draw.polygon([(cx - 4, y1 - 22), (cx, y1 - 16), (cx + 4, y1 - 22),
                      (cx, y1 - 27)], fill=(240, 240, 235))


# ---------------------------------------------------------------- build
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 22                      # side margin
    cx0, cx1 = mx, W - mx
    # outer frame
    d.rectangle([10, 10, W - 11, H - 11], outline=INK, width=3)

    y = 20
    # masthead
    f_mast = font(SERIF_B, 84)
    d.text(((W - d.textlength("THE WORLD TODAY", font=f_mast)) / 2, y),
           "THE WORLD TODAY", font=f_mast, fill=INK)
    y += 92
    draw_rule(d, cx0, cx1, y, 3)
    y += 8
    # dateline band
    f_date = font(COND_B, 34)
    d.text((cx0, y), "FRIDAY, 20 NOVEMBER 2026", font=f_date, fill=RED)
    f_sec = font(SANS_B, 25)
    sec = "WORLD \u2022 BUSINESS \u2022 SCIENCE"
    d.text((cx1 - d.textlength(sec, font=f_sec), y + 3), sec, font=f_sec, fill=INK)
    y += 40
    draw_rule(d, cx0, cx1, y, 2)
    y += 6
    # hero scene
    scene_y0, scene_y1 = y, y + 72
    draw_hero_scene(d, cx0, cx1, scene_y0, scene_y1)
    y = scene_y1 + 8
    # hero kicker
    f_hkick = font(COND_B, 26)
    d.text((cx0, y), HERO_KICKER, font=f_hkick, fill=RED)
    assert d.textlength(HERO_KICKER, font=f_hkick) <= cx1 - cx0
    y += 30
    # hero headline, 2 lines
    f_hhead = font(SERIF_B, 58)
    head_lines = wrap(d, HERO_HEADLINE, f_hhead, cx1 - cx0)
    assert len(head_lines) <= 2, head_lines
    for ln in head_lines:
        d.text((cx0, y), ln, font=f_hhead, fill=INK)
        y += 60
    # hero deck, wrapped
    f_hdeck = font(SERIF, 26)
    deck_lines = wrap(d, HERO_DECK, f_hdeck, cx1 - cx0)
    assert len(deck_lines) <= 2, deck_lines
    for ln in deck_lines:
        d.text((cx0, y), ln, font=f_hdeck, fill=INK)
        y += 30
    y += 4
    draw_rule(d, cx0, cx1, y, 2)
    y += 8

    # grid 3x3
    gutter = 14
    col_w = (cx1 - cx0 - 2 * gutter) // 3
    col_x = [cx0, cx0 + col_w + gutter, cx0 + 2 * (col_w + gutter)]
    f_kick = font(COND_B, 26)
    f_head = font(SERIF_B, 26)
    f_deck = font(SERIF, 26)
    grid_y = y
    # measure row heights first: headline lines + deck lines per cell
    cells = []
    for i, (place, icon, headline, deck) in enumerate(FEATURED):
        hl = wrap(d, headline, f_head, col_w)
        assert len(hl) <= 2, (headline, hl)
        dl = wrap(d, deck, f_deck, col_w)
        assert len(dl) <= 2, (deck, dl)
        kicker = place + " \u2022 20 NOV"
        assert d.textlength(kicker, font=f_kick) + 28 <= col_w, (kicker, col_w)
        cells.append((place, icon, hl, dl, kicker))
    row_h = []
    for r in range(3):
        hlines = max(len(cells[r * 3 + c][2]) for c in range(3))
        dlines = max(len(cells[r * 3 + c][3]) for c in range(3))
        row_h.append(28 + hlines * 30 + dlines * 28 + 6)
    for r in range(3):
        ry = grid_y + sum(row_h[:r])
        for c in range(3):
            place, icon, hl, dl, kicker = cells[r * 3 + c]
            x = col_x[c]
            draw_icon(d, icon, x, ry + 2, 22, RED)
            d.text((x + 28, ry), kicker, font=f_kick, fill=RED)
            hy = ry + 28
            for ln in hl:
                d.text((x, hy), ln, font=f_head, fill=INK)
                hy += 30
            dy = ry + 28 + len(hl) * 30
            for ln in dl:
                d.text((x, dy), ln, font=f_deck, fill=GREY)
                dy += 28
        if r < 2:
            draw_rule(d, cx0, cx1, ry + row_h[r] - 4, 1)
    y = grid_y + sum(row_h) + 6
    draw_rule(d, cx0, cx1, y, 2)
    y += 8

    # MORE strip: heading + 8 items in 2 rows x 4 columns
    f_more_h = font(SANS_B, 27)
    more_head = "MORE TODAY \u2022 18 STORIES"
    d.text((cx0, y), more_head, font=f_more_h, fill=INK)
    y += 32
    f_more = font(COND_B, 26)
    mcol_w = (cx1 - cx0 - 3 * 10) // 4
    mcol_x = [cx0 + i * (mcol_w + 10) for i in range(4)]
    for i, item in enumerate(MORE):
        assert d.textlength("\u2022 " + item, font=f_more) <= mcol_w, (item, mcol_w)
        mx0 = mcol_x[i % 4]
        my0 = y + (i // 4) * 30
        d.text((mx0, my0), "\u2022 " + item, font=f_more, fill=INK)
    y += 60
    y += 6
    draw_rule(d, cx0, cx1, y, 2)
    y += 8
    # footer
    f_foot = font(SERIF, 20)
    d.text((cx0, y), FOOTER_LEFT, font=f_foot, fill=INK)
    fw = d.textlength(FOOTER_RIGHT, font=f_foot)
    assert d.textlength(FOOTER_LEFT, font=f_foot) + fw + 20 <= cx1 - cx0
    d.text((cx1 - fw, y), FOOTER_RIGHT, font=f_foot, fill=GREY)
    y += 30
    assert y <= 1012, ("layout overflow, bottom y =", y)
    return img


def main():
    img = build()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG")
    print("wrote", out, img.size)


if __name__ == "__main__":
    main()
