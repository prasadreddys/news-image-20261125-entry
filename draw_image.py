#!/usr/bin/env python3
"""Draw the 25 November 2026 front page: one 1024x1024 PNG.

Everything here is fixed: fixed text, fixed colours, fixed geometry. No
network, no clock, no randomness, so the picture is the same every run.
Run: python3 draw_image.py  ->  writes entry.png next to this file.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE / "entry.png"
W, H = 1024, 1024

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

NAVY = (16, 36, 62)
NAVY2 = (13, 27, 51)
GOLD = (201, 162, 39)
PAPER = (255, 253, 247)
INK = (24, 24, 24)
GREY = (90, 90, 90)
RUST = (178, 84, 30)
CREAM = (242, 237, 227)
RED = (178, 34, 34)
GREEN = (31, 122, 60)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
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


def para(draw, x, y, text, fnt, max_w, fill=INK, leading=24):
    lines = wrap(draw, text, fnt, max_w)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def panel(draw, box, kicker, kicker_fill, headline, headline_size, body,
          scene):
    """A bordered panel: kicker, headline, drawn scene, body text."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(255, 255, 255), outline=NAVY, width=2)
    pad = 14
    tx = x0 + pad
    tw = x1 - x0 - 2 * pad
    y = y0 + 10
    draw.text((tx, y), kicker, font=font(SANS_B, 14), fill=kicker_fill)
    y += 22
    hf = font(SERIF_B, headline_size)
    for line in wrap(draw, headline, hf, tw):
        draw.text((tx, y), line, font=hf, fill=INK)
        y += headline_size + 4
    y += 4
    scene_h = 96
    scene(draw, tx, y, tw, scene_h)
    y += scene_h + 10
    para(draw, tx, y, body, font(SANS, 16), tw, leading=20)


def rocket_scene(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=NAVY2)
    stars = [(x + 30, y + 18), (x + 90, y + 44), (x + 150, y + 14),
             (x + 210, y + 52), (x + 260, y + 20), (x + 320, y + 40),
             (x + 380, y + 16), (x + 430, y + 48), (x + 480, y + 24),
             (x + 530, y + 44), (x + 60, y + 90), (x + 500, y + 90)]
    for sx, sy in stars:
        draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 255))
    # ground
    draw.rectangle([x, y + h - 26, x + w, y + h], fill=(38, 74, 52))
    # station, upper right: two solar panels and a central module
    sx, sy = x + w - 170, y + 30
    draw.rectangle([sx, sy, sx + 44, sy + 14], fill=(90, 130, 200))
    draw.rectangle([sx + 58, sy - 6, sx + 96, sy + 20], fill=(220, 225, 230))
    draw.rectangle([sx + 110, sy, sx + 154, sy + 14], fill=(90, 130, 200))
    draw.text((sx + 48, sy + 26), "TIANGONG", font=font(SANS_B, 13),
              fill=(255, 255, 255))
    draw.text((x + 14, y + h - 22), "JIUQUAN  •  LONG MARCH 2F",
              font=font(SANS_B, 13), fill=(255, 255, 255))
    # rocket, centre-left, rising
    rx, ry = x + 150, y + 60
    draw.polygon([(rx + 22, ry), (rx + 44, ry + 34), (rx + 44, ry + 120),
                  (rx, ry + 120), (rx, ry + 34)], fill=(235, 235, 235))
    draw.polygon([(rx + 22, ry), (rx + 44, ry + 34), (rx, ry + 34)],
                 fill=RED)
    draw.rectangle([rx + 12, ry + 96, rx + 32, ry + 120], fill=(255, 255, 255))
    draw.ellipse([rx + 14, ry + 58, rx + 30, ry + 74], fill=(120, 180, 230))
    # flame
    draw.polygon([(rx + 8, ry + 122), (rx + 36, ry + 122), (rx + 22, ry + 168)],
                 fill=(255, 140, 0))
    draw.polygon([(rx + 14, ry + 122), (rx + 30, ry + 122), (rx + 22, ry + 150)],
                 fill=(255, 220, 0))
    # small smoke puffs at the pad, clear of the flame
    for cx, cy, r in [(rx - 28, y + h - 44, 12), (rx + 72, y + h - 44, 12)]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(200, 200, 200))


def cyber_scene(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(28, 34, 44))
    # laptop screen
    draw.rectangle([x + 40, y + 12, x + w - 40, y + h - 26], fill=(16, 36, 62),
                   outline=(150, 160, 175), width=2)
    draw.ellipse([x + w // 2 - 26, y + 20, x + w // 2 + 26, y + 72],
                 outline=GOLD, width=3)
    draw.text((x + w // 2 - 14, y + 38), "CIA", font=font(SANS_B, 18),
              fill=(255, 255, 255))
    # warning triangle
    tx, ty = x + w - 78, y + 14
    draw.polygon([(tx, ty + 30), (tx + 34, ty + 30), (tx + 17, ty)],
                 fill=(255, 200, 0))
    draw.text((tx + 13, ty + 10), "!", font=font(SANS_B, 16), fill=(0, 0, 0))
    draw.text((x + 14, y + h - 20), "UNCLASSIFIED NETWORK",
              font=font(SANS_B, 13), fill=(255, 200, 0))


def tower_scene(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(214, 228, 240))
    # skyline
    for bx, bw, bh in [(x + 8, 44, 52), (x + 58, 36, 38), (x + 210, 40, 60),
                       (x + 256, 34, 44)]:
        draw.rectangle([bx, y + h - bh, bx + bw, y + h], fill=(120, 135, 150))
    # the tall tower, centre
    tx = x + w // 2 - 32
    draw.polygon([(tx, y + 12), (tx + 64, y + 12), (tx + 56, y + h),
                  (tx + 8, y + h)], fill=(70, 110, 150))
    for i in range(5):
        yy = y + 22 + i * 14
        draw.line([tx + 6, yy, tx + 58, yy], fill=(200, 220, 235), width=2)
    # smoke from the top
    for cx, cy, r in [(tx + 32, y + 4, 14), (tx + 48, y - 2, 10),
                      (tx + 16, y - 4, 9)]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 120, 120))
    draw.text((x + 14, y + h - 20), "RIYADH", font=font(SANS_B, 13),
              fill=(255, 255, 255))


def gaza_scene(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(232, 176, 120))
    draw.ellipse([x + w - 52, y + 10, x + w - 16, y + 46], fill=(255, 220, 150))
    # ruined silhouettes
    draw.polygon([(x + 10, y + h), (x + 10, y + 46), (x + 44, y + 46),
                  (x + 44, y + 30), (x + 78, y + 30), (x + 78, y + h)],
                 fill=(90, 70, 60))
    draw.polygon([(x + 96, y + h), (x + 96, y + 58), (x + 130, y + 58),
                  (x + 130, y + 40), (x + 168, y + 40), (x + 168, y + h)],
                 fill=(70, 55, 48))
    draw.polygon([(x + 190, y + h), (x + 190, y + 66), (x + 224, y + 66),
                  (x + 224, y + 52), (x + 258, y + 52), (x + 258, y + h)],
                 fill=(90, 70, 60))
    draw.text((x + 14, y + h - 20), "GAZA", font=font(SANS_B, 13),
              fill=(255, 255, 255))


def shop_scene(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(245, 222, 120))
    draw.rectangle([x + 20, y + 18, x + w - 20, y + 58], fill=(255, 255, 255),
                   outline=NAVY, width=2)
    draw.text((x + w // 2, y + 26), "EXITO", font=font(SANS_B, 20),
              fill=NAVY, anchor="ma")
    draw.rectangle([x + 20, y + 58, x + w - 20, y + h - 18], fill=(200, 210, 225))
    for i in range(3):
        sx = x + 28 + i * 48
        draw.rectangle([sx, y + 66, sx + 36, y + h - 26], fill=(120, 140, 165))
    draw.rectangle([x, y + h - 14, x + w, y + h], fill=(30, 80, 160))
    draw.text((x + 14, y + h - 12), "POLICE CORDON",
              font=font(SANS_B, 11), fill=(255, 255, 255))


def chart_scene(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    draw.line([x + 10, y + 10, x + 10, y + h - 10], fill=GREY, width=2)
    draw.line([x + 10, y + h - 10, x + w - 10, y + h - 10], fill=GREY, width=2)
    pts = [(x + 16, y + 22), (x + 48, y + 30), (x + 80, y + 26),
           (x + 112, y + 50), (x + 144, y + 64), (x + 168, y + 76)]
    draw.line(pts, fill=RED, width=4)
    for px, py in pts:
        draw.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED)
    draw.text((x + w - 70, y + 8), "-5.9%", font=font(SANS_B, 20), fill=RED)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    d.rectangle([0, 0, W, 84], fill=NAVY)
    d.text((W // 2, 16), "THE WORLD IN ONE PAGE",
           font=font(SERIF_B, 52), fill=(255, 255, 255), anchor="ma")
    d.rectangle([0, 84, W, 90], fill=GOLD)
    # date bar
    d.text((W // 2, 98), "WEDNESDAY  •  25 NOVEMBER 2026",
           font=font(SANS_B, 30), fill=NAVY, anchor="ma")
    d.text((W // 2, 130), "THE DAY'S WORLD NEWS — IN ONE IMAGE",
           font=font(SANS, 15), fill=GREY, anchor="ma")

    # lead panel: space
    x0, y0, x1, y1 = 24, 162, 1000, 458
    d.rectangle([x0, y0, x1, y1], fill=(255, 255, 255), outline=NAVY, width=2)
    rocket_scene(d, x0 + 12, y0 + 12, 560, y1 - y0 - 24)
    tx = x0 + 584
    tw = x1 - tx - 14
    y = y0 + 14
    d.text((tx, y), "SPACE  •  SHENZHOU-24", font=font(SANS_B, 16), fill=RUST)
    y += 26
    hf = font(SERIF_B, 44)
    for line in ["FIRST PAKISTANI", "IN ORBIT"]:
        d.text((tx, y), line, font=hf, fill=INK)
        y += 48
    y += 6
    y = para(d, tx, y,
             "Shenzhou-24 lifts off from Jiuquan at 00:18 UTC with Tang "
             "Hongbo, Wu Yi and Muhammad Zeeshan Ali, 40 — the first "
             "Pakistani in orbit and the first foreign astronaut to board "
             "China's Tiangong station.",
             font(SANS, 19), tw, leading=25)
    y += 8
    d.text((tx, y), "Stay: 5 to 10 days  •  Long March 2F",
           font=font(SANS_B, 16), fill=NAVY)

    # row 2: three panels
    pw = 317
    panel(d, (24, 470, 24 + pw, 722), "USA  •  CYBER", NAVY,
          "CIA HIT BY CYBER BREACH", 22,
          "NYT: the CIA and ODNI found a breach of an unclassified "
          "open-source network. No classified data was hit.", cyber_scene)
    panel(d, (353, 470, 353 + pw, 722), "MIDDLE EAST  •  RIYADH", RED,
          "TOWER HIT IN RIYADH — 11 HURT", 22,
          "A Houthi strike hits a tower in Riyadh's financial district. "
          "Saudi Arabia calls it a terrorist attack.", tower_scene)
    panel(d, (682, 470, 682 + 318, 722), "GAZA", RUST,
          "NINE KILLED IN GAZA IN 24 HOURS", 22,
          "Israeli strikes kill at least nine, including Hamas security "
          "chief Naeem Abu Nahel. The fragile ceasefire is under strain.",
          gaza_scene)

    # row 3: two panels, scene left, text right
    for (bx0, bx1, kicker, kfill, headline, body, scene) in [
            (24, 506, "COLOMBIA", NAVY, "20 STILL HELD IN CARTAGENA SHOP",
             "Gunmen hold ~20 hostages in a Cartagena supermarket; 10 "
             "freed. A Villavicencio car bomb injures 22.", shop_scene),
            (518, 1000, "MARKETS  •  TRADE", RED,
             "TARIFF THREAT SINKS ASIAN STOCKS",
             "Washington may unveil new tariffs after a probe of 16 "
             "partners. Nvidia falls 5.9% after its 31% surge.",
             chart_scene)]:
        d.rectangle([bx0, 734, bx1, 902], fill=(255, 255, 255), outline=NAVY,
                    width=2)
        scene(d, bx0 + 12, 746, 180, 144)
        tx = bx0 + 204
        tw = bx1 - tx - 14
        y = 746
        d.text((tx, y), kicker, font=font(SANS_B, 14), fill=kfill)
        y += 22
        hf = font(SERIF_B, 21)
        for line in wrap(d, headline, hf, tw):
            d.text((tx, y), line, font=hf, fill=INK)
            y += 25
        y += 4
        para(d, tx, y, body, font(SANS, 15), tw, leading=19)

    # also-today strip
    d.rectangle([24, 912, 1000, 984], fill=CREAM, outline=NAVY, width=2)
    d.text((W // 2, 918), "ALSO TODAY", font=font(SANS_B, 15), fill=NAVY,
           anchor="ma")
    d.text((W // 2, 938),
           "CHINA: Politburo member Chen Jining under investigation  •  "
           "INDONESIA: rescuers search for dozens trapped in a mine",
           font=font(SANS, 15), fill=INK, anchor="ma")
    d.text((W // 2, 958),
           "USA: inflation data due ahead of an expected Fed hike  •  "
           "OIL: Brent $90.97 as Middle East fears lift prices",
           font=font(SANS, 15), fill=INK, anchor="ma")

    # footer
    d.rectangle([0, 984, W, H], fill=NAVY)
    d.text((W // 2, 997),
           "As reported on 25 Nov 2026 — Reuters • AP • Al Jazeera • Dawn "
           "• Channel News Asia • NYT",
           font=font(SANS, 14), fill=(255, 255, 255), anchor="ma")

    img.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT} ({W}x{H})")


if __name__ == "__main__":
    main()
