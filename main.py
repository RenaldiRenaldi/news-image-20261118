"""Draw a compact, deterministic world newspaper front page."""
from pathlib import Path
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (250, 248, 241)
INK = (25, 35, 41)
BLUE = (30, 68, 91)
RED = (166, 57, 40)
MUTED = (91, 99, 96)
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

# Each entry is a concise headline preserving the supplied story's identifying facts.
SECTIONS = [
    ("ASIA", [
        "Trump arrives in Manila for Quad talks ahead of China visit",
        "Canada and China extend trade deals as Xi meets Carney before APEC",
        "Cyclone Akvan intensifies over the Bay of Bengal (Andhra Pradesh, Odisha on high alert)",
        "PM Modi proposes free e-visas and maritime cooperation at ASEAN",
        "India re-elected to ITU Council for 2027–2030",
        "Amazon announces $7B investment in India's renewable energy",
        "India clinches 10th SAFF title, beat Pakistan 2–1",
        "MS Dhoni retires from IPL, becomes CSK mentor",
        "Japan proposes Asian IEA, offers idle oil storage",
        "Baidu chief warns of AI ‘bubble’ ahead of APEC",
    ]),
    ("EUROPE", [
        "Ukraine strikes Crimean Bridge for a 2nd day as Russia hits Kyiv bridges",
        "Britain sanctions Israeli settlement firms",
        "Cyber-attack disables supermarket freezers in 7 European countries",
        "Finland approves world's first nuclear waste repository",
        "EU wants to borrow €45B to shore up Ukraine's budget",
        "Zelensky accuses US of blocking paid missile deliveries",
        "Germany's 2027 tax forecast hits record €1 trillion",
        "Hungary 1–1 Northern Ireland in Nations League",
    ]),
    ("MIDDLE EAST", [
        "Iran attacks US military radar in Bahrain with drones",
        "Kuwait reports drone attacks; Iran, US trade attacks on Qeshm and Bahrain",
        "Gaza ceasefire faces imminent collapse, Board of Peace warns",
        "Houthi rocket attack kills 53 soldiers in Yemen",
        "Israel parliament elects Eisenkot ally Matan Kahana as speaker",
        "Hormuz tanker MT TARA GAS attacked; 21 Indians evacuated",
        "Iran claims tanker with 2M barrels of oil sank in Hormuz",
        "Gaza families return to kerosene stoves amid gas shortage",
    ]),
    ("AMERICAS", [
        "US stocks fall as Dow plunges over 1,000 points intraday",
        "California bans Waymo self-driving cars from freeways",
        "Microsoft services restored after 36-hour outage",
        "Nvidia hires law firm to probe CEO's alleged link to Chinese spy",
        "Amazon + Google to own nearly 30% of Anthropic after IPO",
        "Asif Merchant sentenced to 27 years over Trump murder plot",
        "NASA's Voyager 1 nears one light-day from Earth",
        "SpaceX catches a falling Starship",
    ]),
    ("AFRICA", [
        "DR Congo rival peace efforts fail, violence in east",
        "Sudan's factories struggle to recover after wartime destruction",
        "UN confirms over 2,230 civilian deaths in Sudan",
    ]),
    ("OCEANIA", [
        "Australia targets Israeli settlements with fresh sanctions",
        "Trump praises 'friend' Albanese at Quad summit",
        "New Zealand accepts liability for Penrhyn port cost overruns",
    ]),
]


def font(path, size):
    return ImageFont.truetype(path, size)


def centered(draw, text, y, f, fill):
    box = draw.textbbox((0, 0), text, font=f)
    draw.text(((W - box[2] + box[0]) / 2, y), text, font=f, fill=fill)


def draw_map(d):
    """A deliberately simple, recognizable world map silhouette with location dots."""
    x0, y0, x1, y1 = 34, 106, 990, 229
    d.rounded_rectangle((x0, y0, x1, y1), radius=7, fill=(233, 239, 234), outline=(190, 201, 195), width=1)
    # Blocky, hand-drawn continent silhouettes, simplified for small-scale legibility.
    shapes = [
        [(82,145),(110,125),(166,123),(197,138),(184,154),(155,157),(143,178),(121,188),(106,171),(87,166)],
        [(165,180),(190,184),(204,205),(195,221),(181,211),(173,196)],
        [(424,138),(457,124),(486,128),(494,141),(476,149),(459,158),(437,153)],
        [(451,159),(480,159),(493,176),(484,199),(467,212),(452,188)],
        [(494,137),(527,126),(580,130),(615,142),(650,139),(675,151),(651,164),(612,159),(597,177),(570,169),(544,177),(520,160),(493,159)],
        [(564,176),(590,176),(604,192),(588,204),(572,194)],
        [(672,187),(706,189),(719,199),(706,209),(681,204)],
    ]
    for pts in shapes:
        d.polygon(pts, fill=(123, 155, 136), outline=(80, 116, 99))
    # Manila, Kyiv, Gulf, Americas, Africa, and Australia.
    for px, py in [(656,157),(467,148),(558,176),(146,153),(475,184),(699,199)]:
        d.ellipse((px-4,py-4,px+4,py+4), fill=RED, outline=PAPER, width=1)
    d.text((750, 115), "TODAY, ACROSS SIX CONTINENTS", font=font(SANS_B, 12), fill=BLUE)
    d.text((750, 137), "Stories from Manila to Kyiv", font=font(SANS, 12), fill=INK)
    d.text((750, 155), "and the Gulf to the Americas", font=font(SANS, 12), fill=INK)


def draw_section(d, section, idx):
    title, stories = section
    # Two tiers, three editorial columns. Dynamic height fits all lines without clipping.
    col = idx % 3
    row = idx // 3
    x = 36 + col * 322
    y = 340 + row * 290
    width = 300
    d.rectangle((x, y, x + width, y + 25), fill=BLUE)
    d.text((x + 9, y + 4), title, font=font(SANS_B, 14), fill=(255,255,255))
    f = font(SANS_B, 11)
    for n, headline in enumerate(stories):
        words = headline.split()
        lines, line = [], ""
        for word in words:
            candidate = word if not line else line + " " + word
            if d.textbbox((0, 0), candidate, font=f)[2] <= width - 2:
                line = candidate
            else:
                lines.append(line)
                line = word
        if line:
            lines.append(line)
        yy = y + 31 + n * 25
        for j, text in enumerate(lines[:2]):
            d.text((x + 1, yy + j * 11), text, font=f, fill=INK)
        if n != len(stories) - 1:
            d.line((x, yy + 22, x + width, yy + 22), fill=(218, 218, 208), width=1)


def make_page():
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    d.rectangle((14, 14, 1009, 1010), outline=INK, width=2)
    centered(d, "THE WORLD TODAY", 22, font(SERIF_B, 43), INK)
    centered(d, "WEDNESDAY, 18 NOVEMBER 2026     •     WORLD EDITION", 71, font(SANS_B, 13), BLUE)
    centered(d, "40 STORIES  •  6 CONTINENTS", 88, font(SANS_B, 13), RED)
    d.line((32, 107, 992, 107), fill=INK, width=2)
    draw_map(d)

    d.text((36, 242), "LEAD STORY  /  MANILA", font=font(SANS_B, 12), fill=RED)
    d.text((35, 257), "TRUMP ARRIVES IN MANILA FOR QUAD TALKS", font=font(SERIF_B, 25), fill=INK)
    d.text((36, 289), "Ahead of China visit, US, India, Japan and Australia put maritime security, AI", font=font(SANS, 14), fill=BLUE)
    d.text((36, 309), "and critical minerals on the agenda as APEC meets Nov. 18–19.", font=font(SANS, 14), fill=BLUE)
    d.line((32, 333, 992, 333), fill=INK, width=2)

    # One balanced grid keeps the headline collection scannable at native size.
    for i, section in enumerate(SECTIONS):
        draw_section(d, section, i)

    d.rectangle((32, 925, 992, 987), fill=(229, 235, 230), outline=BLUE, width=1)
    d.text((45, 934), "DAY IN NUMBERS", font=font(SANS_B, 14), fill=RED)
    d.text((45, 956), "Dow −1,000 pts  •  21 evacuated  •  53 soldiers killed  •  €45B  •  $7B  •  2M barrels  •  27 years  •  14 infants",
           font=font(SANS_B, 12), fill=INK)
    return im


def main():
    out = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "out"))
    out.mkdir(parents=True, exist_ok=True)
    make_page().save(out / "entry.png", format="PNG", optimize=True, compress_level=9)


if __name__ == "__main__":
    main()
