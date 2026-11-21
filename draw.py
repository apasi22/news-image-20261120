#!/usr/bin/env python3
"""Draw the 20 November 2026 world-news image (1024x1024 PNG).

Fresh composition for news-image-20261120. Deterministic: same input always
writes the same bytes (fixed palette, fixed layout, PNG with no timestamps).
Run:  python3 draw.py  ->  writes entry.png next to this file.
"""
import hashlib
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

# ---- palette ------------------------------------------------------------
PAPER   = (247, 243, 234)   # warm newsprint
INK     = (22, 22, 22)      # near-black
RED     = (178, 24, 24)     # flag red
DARKRED = (128, 16, 16)
GREY    = (96, 92, 84)
RULE    = (60, 56, 48)
NAVY    = (24, 38, 64)      # illustration sky
RIVER   = (72, 108, 148)
ORANGE  = (232, 120, 32)
YELLOW  = (244, 196, 64)
SMOKE   = (120, 116, 108)

# ---- fonts --------------------------------------------------------------
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF   = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B  = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS    = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def f(path, size):
    return ImageFont.truetype(path, size)

F_MASTHEAD = f(SERIF_B, 50)
F_KICKER   = f(SANS_B, 16)
F_FLAG     = f(SANS_B, 15)
F_HEAD     = f(SERIF_B, 38)
F_HEAD2    = f(SERIF_B, 28)
F_HEAD3    = f(SERIF_B, 27)
F_DECK     = f(SERIF, 20)
F_DECK2    = f(SERIF, 18)
F_NUM      = f(SANS_B, 19)
F_TICK     = f(SANS_B, 15)
F_CAP      = f(SANS, 13)
F_FOOT     = f(SANS, 13)

# ---- text helpers -------------------------------------------------------
def wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def para(draw, x, y, text, font, max_w, fill, leading):
    lines = wrap(draw, text, font, max_w)
    for ln in lines:
        draw.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y

def headline(draw, x, y, text, font, max_w, leading):
    return para(draw, x, y, text, font, max_w, INK, leading)

def flag(draw, x, y, text):
    draw.text((x, y), text, font=F_FLAG, fill=RED)
    return y + 22

def rule(draw, x0, y, x1, wdt=2):
    draw.line([(x0, y), (x1, y)], fill=RULE, width=wdt)

# ---- illustration: Kyiv skyline, river, three bridges, smoke -----------
def draw_kyiv(draw, x0, y0, w, h):
    # sky
    for i in range(h):
        t = i / max(h - 1, 1)
        c = tuple(int(NAVY[k] + (52 - NAVY[k]) * t) for k in range(3))
        draw.line([(x0, y0 + i), (x0 + w, y0 + i)], fill=c)
    # stars
    for sx, sy in [(18, 12), (52, 26), (96, 9), (150, 22), (205, 11),
                   (250, 28), (288, 14), (120, 38), (230, 40)]:
        draw.ellipse([x0 + sx - 1, y0 + sy - 1, x0 + sx + 1, y0 + sy + 1],
                     fill=(220, 220, 200))
    # skyline silhouettes
    base = y0 + h - 44
    blds = [(0, 38, 34), (38, 58, 30), (72, 44, 40), (116, 70, 30),
            (150, 50, 36), (190, 62, 30), (224, 42, 34), (262, 54, 30),
            (296, 36, 26)]
    for bx, bh, bw in blds:
        draw.rectangle([x0 + bx, base - bh, x0 + bx + bw, base],
                       fill=(14, 22, 40))
    # dome on the tallest block
    draw.ellipse([x0 + 116, base - 70 - 12, x0 + 146, base - 70 + 6],
                 fill=(14, 22, 40))
    draw.rectangle([x0 + 128, base - 70 - 22, x0 + 134, base - 70],
                   fill=(14, 22, 40))
    # windows
    for wx in range(8, w - 8, 16):
        for wy in range(base - 64, base - 6, 13):
            if (wx * 7 + wy * 3) % 11 < 4:
                draw.rectangle([x0 + wx, wy, x0 + wx + 4, wy + 5],
                               fill=(244, 196, 64))
    # river
    draw.rectangle([x0, y0 + h - 44, x0 + w, y0 + h], fill=RIVER)
    draw.line([(x0, y0 + h - 44), (x0 + w, y0 + h - 44)],
              fill=(150, 180, 210), width=2)
    # three bridges across the river
    for bx in (10, 118, 226):
        draw.arc([x0 + bx, y0 + h - 62, x0 + bx + 84, y0 + h - 14],
                 start=180, end=360, fill=(210, 205, 190), width=4)
        draw.line([(x0 + bx, y0 + h - 38), (x0 + bx + 84, y0 + h - 38)],
                  fill=(210, 205, 190), width=3)
    # explosion bursts + smoke columns over the bridges
    for ex, ey, r in [(60, y0 + 56, 15), (168, y0 + 48, 17), (272, y0 + 60, 13)]:
        pts = []
        for k in range(12):
            ang = k * 30 * math.pi / 180.0
            rr = r if k % 2 == 0 else r * 0.45
            pts.append((x0 + ex + rr * math.cos(ang),
                        ey + rr * math.sin(ang)))
        draw.polygon(pts, fill=ORANGE)
        draw.ellipse([x0 + ex - 7, ey - 7, x0 + ex + 7, ey + 7], fill=YELLOW)
        for s in range(3):
            draw.ellipse([x0 + ex - 8 + s * 3, ey - 24 - s * 11,
                          x0 + ex + 8 + s * 3, ey - 11 - s * 11], fill=SMOKE)

# ---- page ---------------------------------------------------------------
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36                      # side margin
    X1 = W - M                  # right edge

    # masthead ------------------------------------------------------------
    y = 18
    d.text((M, y), "THE WORLD IN ONE PAGE", font=F_KICKER, fill=GREY)
    rk = d.textlength("FRIDAY  ·  SIX STORIES", font=F_KICKER)
    d.text((X1 - rk, y), "FRIDAY  ·  SIX STORIES", font=F_KICKER, fill=GREY)
    y += 26
    rule(d, M, y, X1, 3)
    y += 10
    title = "20 NOVEMBER 2026"
    tw = d.textlength(title, font=F_MASTHEAD)
    d.text(((W - tw) / 2, y), title, font=F_MASTHEAD, fill=INK)
    y += 62
    rule(d, M, y, X1, 3)
    y += 10

    # LEAD: Kyiv ----------------------------------------------------------
    ly = y
    flag(d, M, ly, "UKRAINE  —  LEAD STORY")
    # illustration, right side
    iw, ih = 322, 150
    ix, iy = X1 - iw, ly + 26
    draw_kyiv(d, ix, iy, iw, ih)
    d.text((ix, iy + ih + 5),
           "Three Dnipro bridges hit: Podilsko-Voskresenskyi,",
           font=F_CAP, fill=GREY)
    d.text((ix, iy + ih + 21), "Darnytskyi, Pivdennyi.",
           font=F_CAP, fill=GREY)
    # headline + deck, left of illustration
    hw = X1 - iw - 28 - M
    hy = headline(d, M, ly + 26,
                  "RUSSIA'S BIGGEST AIR STRIKE OF THE YEAR HITS KYIV",
                  F_HEAD, hw, 42)
    hy += 6
    hy = para(d, M, hy,
              "110+ missiles \u2014 27 ballistic \u2014 and 400+ drones "
              "overnight. Three Dnipro bridges hit; power, water and heat "
              "cut. Zelenskyy: \u201cthe biggest this year\u201d.",
              F_DECK, hw, INK, 24)
    # numbers strip
    ny = max(ly + 26 + ih + 40, hy + 8)
    rule(d, M, ny, X1, 1)
    ny += 8
    nums = "110+ MISSILES   ·   27 BALLISTIC   ·   400+ DRONES   ·   9 KILLED   ·   28 INJURED"
    nw = d.textlength(nums, font=F_NUM)
    d.text(((W - nw) / 2, ny), nums, font=F_NUM, fill=DARKRED)
    ny += 26
    rule(d, M, ny, X1, 2)
    y = ny + 10

    # two-column rows -----------------------------------------------------
    col_w = (W - 2 * M - 28) // 2
    cx2 = M + col_w + 28

    def story(x, yy, flagtext, head, deck):
        yy = flag(d, x, yy, flagtext)
        yy = headline(d, x, yy + 4, head, F_HEAD2, col_w, 32)
        yy += 4
        yy = para(d, x, yy, deck, F_DECK2, col_w, INK, 22)
        return yy

    # row 1: Poland | NATO guarantees
    r1 = y
    e1 = story(M, r1, "POLAND  ·  NATO",
               "RUSSIAN MISSILES LAND IN POLAND",
               "A Kh-101 missile, a second missile and a jet-powered drone "
               "crash in the south-east \u2014 no one hurt. Tusk: \u201cdeliberate "
              "provocation\u201d; NATO jets scramble; Rutte due in Warsaw.")
    e2 = story(cx2, r1, "DIPLOMACY",
               "MOSCOW REJECTS NATO-STYLE GUARANTEES",
               "Deputy FM Ryabkov: Ukraine\u2019s \u201cquasi-membership\u201d of "
              "NATO is \u201cunacceptable\u201d \u2014 a day after Kushner said "
              "Russia was \u201ccomfortable\u201d with Article 5 cover.")
    y = max(e1, e2) + 8
    rule(d, M, y, X1, 1)
    y += 10

    # row 2: Markets | Anthropic
    r2 = y
    e3 = story(M, r2, "MARKETS",
               "GLOBAL SELL-OFF DEEPENS",
               "Nikkei \u22125.06% \u00b7 Kospi \u22125.21% \u00b7 Taiex "
              "\u22126.2%, worst week since 1991. S&P 500 \u22123.7% \u00b7 "
              "Nasdaq \u22125.3% \u00b7 Dow \u22121.9%. SoftBank \u221214.6%.")
    e4 = story(cx2, r2, "TECH",
               "ANTHROPIC CRASHES 12% A DAY AFTER ITS RECORD IPO",
               "Shares fall to $85.16 after closing at $97.17 \u2014 up 17% "
              "\u2014 on a debut priced at $83. Retail buyers who chased the "
              "listing face steep losses.")
    y = max(e3, e4) + 8
    rule(d, M, y, X1, 1)
    y += 10

    # row 3: Trump, full width --------------------------------------------
    r3 = y
    flag(d, M, r3, "WASHINGTON")
    hy = headline(d, M, r3 + 26,
                  "TRUMP DEFENDS PUTIN AS A \u201cFRIEND\u201d IN 90-MINUTE BRIEFING",
                  F_HEAD3, X1 - M, 30)
    hy += 4
    hy = para(d, M, hy,
              "Floats Stephen Miller for president in 2028; plans a big tax on "
              "US firms building data centres abroad; claims two new trade "
              "deals, with Thailand and the Philippines.",
              F_DECK2, X1 - M, INK, 22)
    y = hy + 8
    rule(d, M, y, X1, 2)
    y += 6

    # footer ticker -------------------------------------------------------
    tick1 = ("NIKKEI 56,436.65 \u22125.06%   ·   KOSPI 4,869.96 \u22125.21%   ·   "
             "TAIEX 36,033.29 \u22126.2%")
    tick2 = ("S&P 500 6,910.39 \u22123.7%   ·   NASDAQ 22,617.73 \u22125.3%   ·   "
             "DOW 48,147.33 \u22121.9%")
    for tick in (tick1, tick2):
        tw = d.textlength(tick, font=F_TICK)
        d.text(((W - tw) / 2, y), tick, font=F_TICK, fill=DARKRED)
        y += 20
    foot = ("Friday 20 November 2026  ·  Sources: Reuters  ·  CNN  ·  AP  ·  "
            "ISW  ·  LSEG")
    fw = d.textlength(foot, font=F_FOOT)
    d.text(((W - fw) / 2, y), foot, font=F_FOOT, fill=GREY)

    return img

if __name__ == "__main__":
    image = build()
    image.save("entry.png", format="PNG", optimize=True)
    data = open("entry.png", "rb").read()
    print("entry.png", len(data), "bytes",
          "sha256", hashlib.sha256(data).hexdigest()[:16])
