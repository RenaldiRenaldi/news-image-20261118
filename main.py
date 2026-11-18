from pathlib import Path
import os

from PIL import Image, ImageDraw, ImageFont


W = H = 1024
PAPER = (248, 246, 238)
INK = (22, 31, 39)
BLUE = (22, 58, 82)
RED = (166, 48, 35)
MUTED = (84, 83, 75)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_font(draw, text, path, start, maximum, width):
    for size in range(start, maximum - 1, -1):
        f = font(path, size)
        if draw.textbbox((0, 0), text, font=f)[2] <= width:
            return f
    return font(path, maximum)


def wrap(draw, text, f, width):
    words = text.split()
    lines, line = [], ""
    for word in words:
        candidate = word if not line else line + " " + word
        if draw.textbbox((0, 0), candidate, font=f)[2] <= width:
            line = candidate
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def centered(draw, text, y, f, fill):
    box = draw.textbbox((0, 0), text, font=f)
    draw.text(((W - (box[2] - box[0])) // 2, y), text, font=f, fill=fill)


def globe(draw, x, y, r):
    draw.ellipse((x-r, y-r, x+r, y+r), fill=(225, 232, 227), outline=BLUE, width=3)
    draw.arc((x-r*0.57, y-r, x+r*0.57, y+r), 0, 360, fill=BLUE, width=2)
    draw.arc((x-r*0.88, y-r*0.48, x+r*0.88, y+r*0.48), 0, 360, fill=BLUE, width=2)
    draw.line((x-r+4, y, x+r-4, y), fill=BLUE, width=2)
    draw.line((x, y-r+4, x, y+r-4), fill=BLUE, width=2)


def make_page():
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    d.rectangle((18, 18, 1005, 1005), outline=INK, width=2)
    centered(d, "THE WORLD TODAY", 26, font(SERIF_B, 52), INK)
    centered(d, "WEDNESDAY  •  18 NOVEMBER 2026  •  WORLD EDITION", 86, font(SANS_B, 16), BLUE)
    d.line((38, 117, 986, 117), fill=INK, width=3)
    d.line((38, 123, 986, 123), fill=INK, width=1)

    # Lead: the international summit and its diplomatic setting.
    d.text((43, 136), "DIPLOMACY  /  ASIA-PACIFIC", font=font(SANS_B, 14), fill=RED)
    d.text((42, 154), "TRUMP IN MANILA FOR QUAD TALKS", font=fit_font(d, "TRUMP IN MANILA FOR QUAD TALKS", SERIF_B, 36, 28, 938), fill=INK)
    d.text((42, 199), "AHEAD OF CHINA VISIT", font=font(SERIF_B, 34), fill=INK)
    d.text((43, 242), "Quad leaders meet on maritime security, AI and critical minerals", font=font(SANS_B, 17), fill=BLUE)
    d.text((43, 265), "as Trump arrives before the APEC summit in China, Nov. 18–19.", font=font(SANS, 16), fill=INK)

    # Original hand-drawn summit and globe illustration, with a clear caption.
    d.rounded_rectangle((43, 294, 981, 425), radius=4, fill=(232, 235, 229), outline=(171, 180, 172), width=1)
    globe(d, 105, 359, 43)
    d.text((166, 305), "MANILA  |  QUAD LEADERS' TALKS", font=font(SANS_B, 14), fill=BLUE)
    # Summit table and four delegate silhouettes.
    d.ellipse((283, 334, 547, 405), fill=(206, 214, 207), outline=BLUE, width=2)
    d.ellipse((314, 345, 516, 394), fill=(248, 246, 238), outline=(129, 145, 137), width=1)
    for px in (324, 390, 456, 522):
        d.ellipse((px-12, 316, px+12, 340), fill=BLUE)
        d.rounded_rectangle((px-15, 339, px+15, 364), radius=5, fill=BLUE)
    d.text((588, 326), "UNITED STATES  •  INDIA", font=font(SANS_B, 16), fill=INK)
    d.text((588, 353), "JAPAN  •  AUSTRALIA", font=font(SANS_B, 16), fill=INK)
    d.text((588, 385), "APEC summit in China follows Nov. 18–19", font=font(SANS, 14), fill=MUTED)
    d.line((43, 438, 981, 438), fill=INK, width=2)

    # Second major story.
    d.text((43, 451), "WAR IN UKRAINE", font=font(SANS_B, 13), fill=RED)
    d.text((43, 468), "CRIMEAN BRIDGE STRUCK AGAIN AS RUSSIA HITS KYIV", font=fit_font(d, "CRIMEAN BRIDGE STRUCK AGAIN AS RUSSIA HITS KYIV", SERIF_B, 27, 21, 936), fill=INK)
    d.text((43, 504), "Ukraine damaged the bridge for a second day; Russian strikes on Kyiv bridges", font=font(SANS, 16), fill=INK)
    d.text((43, 526), "disrupted water and electricity, officials said.", font=font(SANS, 16), fill=INK)
    d.line((43, 555, 981, 555), fill=INK, width=2)

    stories = [
        ("GULF DRONE STRIKES & ALERTS", "Iran hit a US radar in Bahrain; Kuwait reported interceptions. Bahrain later issued an all-clear."),
        ("CANADA–CHINA TRADE", "Xi met Carney; both countries extended trade cooperation ahead of APEC."),
        ("UK, AUSTRALIA SANCTION FIRMS", "Britain sanctioned eight settlement firms; Australia announced fresh West Bank sanctions."),
        ("CYCLONE AKVAN STRENGTHENS", "Andhra Pradesh and Odisha placed on high alert as the Bay of Bengal storm intensified."),
        ("TANKER ATTACK IN HORMUZ", "Panama-flagged LPG carrier MT TARA GAS was attacked; 21 of 24 Indians evacuated at Khasab."),
        ("GAZA CEASEFIRE AT RISK", "Board of Peace warned of imminent collapse; WFP serves one hot meal every two days in camps."),
    ]
    x0, x1 = 43, 521
    colw, gapx = 438, 34
    top, row_h, gapy = 570, 132, 8
    for i, (headline, summary) in enumerate(stories):
        col, row = i % 2, i // 2
        x = (x0, x1)[col]
        y = top + row * (row_h + gapy)
        d.line((x, y, x + colw, y), fill=BLUE, width=2)
        hf = fit_font(d, headline, SANS_B, 17, 14, colw)
        d.text((x, y + 9), headline, font=hf, fill=BLUE)
        sf = font(SANS, 15)
        lines = wrap(d, summary, sf, colw)
        for j, line in enumerate(lines[:3]):
            d.text((x, y + 37 + j * 20), line, font=sf, fill=INK)
    d.line((43, 990, 981, 990), fill=INK, width=1)
    return im


def main():
    out = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "out"))
    out.mkdir(parents=True, exist_ok=True)
    make_page().save(out / "entry.png", format="PNG", optimize=True, compress_level=9)


if __name__ == "__main__":
    main()
