"""Build a deterministic, compact world-news front page with Pillow."""
from pathlib import Path
import os

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
PAPER = (250, 248, 241)
INK = (25, 35, 41)
BLUE = (30, 68, 91)
RED = (166, 57, 40)
MUTED = (91, 99, 96)
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

# Concise display heads retain each R2 story's identifying event and figures.
SECTIONS = [
    ("ASIA", [
        "Trump arrives Manila for Quad talks before China visit",
        "Canada and China extend trade deals before APEC",
        "Cyclone Akvan: Andhra Pradesh, Odisha on high alert",
        "Modi proposes ASEAN e-visas and maritime cooperation",
        "India re-elected to ITU Council for 2027–2030",
        "Amazon pledges $7B for India's renewable energy",
        "India wins 10th SAFF title, beats Pakistan 2–1",
        "MS Dhoni retires from IPL, becomes CSK mentor",
        "Japan proposes Asian IEA, offers idle oil storage",
        "Baidu chief warns of AI bubble ahead of APEC",
        "Xi calls for open trade at APEC CEO Summit",
        "Xi backs efforts to ease Korean Peninsula tensions",
    ]),
    ("EUROPE", [
        "Ukraine strikes Crimean Bridge; Russia hits Kyiv bridges",
        "Britain sanctions Israeli settlement firms",
        "Cyberattack disables freezers in 7 European countries",
        "Finland approves world's first nuclear-waste repository",
        "EU proposes €45B loan to shore up Ukraine's budget",
        "Zelensky accuses US of blocking paid missile deliveries",
        "Germany's 2027 tax forecast hits record €1 trillion",
        "Hungary and Northern Ireland draw 1–1 in Nations League",
    ]),
    ("MIDDLE EAST", [
        "Iran attacks US radar in Bahrain with drones",
        "Kuwait reports drone attacks; Iran-US strikes widen",
        "Gaza ceasefire nears collapse, Board of Peace warns",
        "Houthi rocket attack kills 53 soldiers in Yemen",
        "Israel elects Eisenkot ally Matan Kahana as speaker",
        "Hormuz tanker attacked; 21 Indians evacuated",
        "Iran says tanker with 2M barrels sank in Hormuz",
        "Gaza families return to kerosene stoves amid gas shortage",
    ]),
    ("AMERICAS", [
        "Dow plunges over 1,000 points intraday as US stocks fall",
        "California bars Waymo self-driving cars from freeways",
        "Microsoft services restored after 36-hour outage",
        "Nvidia hires law firm to probe CEO-China spy allegation",
        "Amazon, Google to own nearly 30% of Anthropic after IPO",
        "Asif Merchant gets 27 years over Trump murder plot",
        "Voyager 1 nears one light-day from Earth",
        "SpaceX catches a falling Starship",
    ]),
    ("AFRICA", [
        "DR Congo peace efforts falter amid eastern violence",
        "Sudan factories struggle to recover from war",
        "UN confirms over 2,230 civilian deaths in Sudan",
        "Kenya arrests four after kidnapped girl, 4, is rescued",
        "Rwanda tightens safeguards for overseas child adoptions",
        "South Africa reprimands Nigerian envoy over broadcast dispute",
        "Guinea jails 224 over illegal gold mining",
        "Ethiopia-Eritrea fighting reignites, war fears grow",
    ]),
    ("OCEANIA", [
        "Australia sanctions Israeli settlers and organisations",
        "Trump praises 'friend' Albanese at Quad summit",
        "New Zealand accepts Penrhyn port cost overruns",
        "Fiji declares disaster state as El Niño thresholds hit",
        "Fiji backs review of Food Safety Act after violations",
        "Kadavu hospital upgraded to improve island healthcare",
    ]),
]

def font(path, size):
    return ImageFont.truetype(path, size)


def centered(draw, text, y, f, fill):
    box = draw.textbbox((0, 0), text, font=f)
    draw.text(((SIZE - box[2] + box[0]) / 2, y), text, font=f, fill=fill)


def draw_map(draw):
    """Draw a simplified world map and six locators in the map band."""
    draw.rounded_rectangle((32, 105, 992, 220), radius=8,
                           fill=(233, 239, 234), outline=(190, 201, 195))
    shapes = [
        [(67,147),(98,123),(151,122),(183,137),(171,155),(146,159),(133,180),(112,191),(96,173),(76,166)],
        [(149,181),(176,184),(191,204),(183,217),(166,210),(158,195)],
        [(406,137),(435,123),(464,127),(472,140),(455,148),(439,157),(419,153)],
        [(432,159),(461,159),(475,176),(466,198),(449,211),(435,187)],
        [(474,137),(508,125),(559,130),(595,140),(629,138),(656,151),(632,164),(596,159),(582,176),(555,169),(531,178),(505,159),(477,158)],
        [(545,177),(571,176),(586,192),(569,205),(553,195)],
        [(654,188),(689,189),(702,200),(689,210),(664,204)],
    ]
    for points in shapes:
        draw.polygon(points, fill=(123, 155, 136), outline=(80, 116, 99))
    # Approximate markers: Manila, Europe, Gulf, Americas, Africa and Fiji.
    for px, py in [(641,157),(451,148),(530,176),(123,153),(455,185),(690,198)]:
        draw.ellipse((px-4, py-4, px+4, py+4), fill=RED, outline=PAPER, width=1)
    draw.text((736, 122), "THE DAY, ACROSS SIX CONTINENTS", font=font(SANS_B, 12), fill=BLUE)
    draw.text((736, 145), "47 dispatches • one world map", font=font(SANS, 12), fill=INK)
    draw.text((736, 166), "Manila · Kyiv · Gulf · Suva", font=font(SANS, 12), fill=INK)


def draw_section(draw, title, stories, x, y, width=310):
    """One-line heads in compact columns; variable rows prevent clipping."""
    draw.rectangle((x, y, x + width, y + 19), fill=BLUE)
    draw.text((x + 7, y + 2), title, font=font(SANS_B, 11), fill=(255, 255, 255))
    f = font(SANS_B, 10)
    yy = y + 23
    for story in stories:
        # Fit every head inside its column and wrap only when necessary.
        words = story.split()
        lines, line = [], ""
        for word in words:
            candidate = word if not line else line + " " + word
            if draw.textbbox((0, 0), candidate, font=f)[2] <= width - 4:
                line = candidate
            else:
                lines.append(line)
                line = word
        if line:
            lines.append(line)
        for headline_line in lines:
            draw.text((x + 1, yy), headline_line, font=f, fill=INK)
            yy += 11
    return yy


def draw_sections(draw):
    # Each vertical column has two region blocks; Africa/Oceania have room to breathe.
    columns = [((0, 12), (4, 8)), ((1, 8), (5, 6)), ((2, 8), (3, 8))]
    for col, blocks in enumerate(columns):
        x = 34 + col * 322
        y = 330
        for section_index, count in blocks:
            title, stories = SECTIONS[section_index]
            y = draw_section(draw, title, stories[:count], x, y)
            y += 5


def draw_market(draw):
    draw.rounded_rectangle((32, 681, 992, 738), radius=5,
                           fill=(235, 239, 233), outline=(190, 201, 195))
    draw.text((44, 688), "MARKET PULSE", font=font(SANS_B, 12), fill=RED)
    draw.text((176, 688), "DOW CLOSE 50,759  −849  •  AMBER 04:00 GMT: GOLD $3,787  •  BTC $64,401",
              font=font(SANS_B, 11), fill=INK)
    draw.text((176, 713), "AMBER EUR/USD 1.09895  •  SMIFS BRENT $92.80/bbl (08:35 IST)  |  18 Nov",
              font=font(SANS, 10), fill=BLUE)


def draw_timeline(draw):
    draw.rounded_rectangle((32, 744, 992, 837), radius=5,
                           fill=(247, 243, 233), outline=(216, 207, 188))
    draw.text((44, 751), "TIMELINE OF THE DAY", font=font(SANS_B, 12), fill=RED)
    draw.text((44, 777), "REPORTS FILED", font=font(SANS_B, 8), fill=MUTED)
    draw.text((44, 789), "UTC", font=font(SANS_B, 8), fill=MUTED)
    items = [
        ("17 NOV · 18:05Z", "Kadavu hospital upgrade reported"),
        ("17 NOV · 23:42Z", "Fiji declares a disaster state"),
        ("17 NOV · 23:57Z", "Australia announces settler sanctions"),
        ("18 NOV · 00:10Z", "Trump's Manila meeting reported"),
        ("18 NOV · 03:03Z", "Fiji council backs food-law review"),
        ("18 NOV · 04:00Z", "Xi opens APEC CEO Summit"),
    ]
    positions = [(204, 752), (470, 752), (736, 752),
                 (204, 797), (470, 797), (736, 797)]
    for (stamp, event), (x, y) in zip(items, positions):
        draw.text((x, y), stamp, font=font(SANS_B, 9), fill=BLUE)
        draw.text((x, y + 14), event, font=font(SANS, 8), fill=INK)


def draw_numbers(draw):
    draw.rounded_rectangle((32, 844, 992, 936), radius=5,
                           fill=(229, 235, 230), outline=BLUE)
    draw.text((44, 852), "DAY IN NUMBERS", font=font(SANS_B, 12), fill=RED)
    draw.text((44, 878),
              "Dow −1,000 pts intraday  •  21 Indians evacuated  •  53 soldiers killed  •  36h Microsoft outage",
              font=font(SANS_B, 9), fill=INK)
    draw.text((44, 900),
              "€45B Ukraine loan  •  $7B India renewables  •  2M tanker barrels  •  2–1 SAFF final  •  €1T German tax forecast",
              font=font(SANS_B, 9), fill=INK)
    draw.text((44, 921),
              "27-year sentence  •  14 infants  •  2,230+ Sudan civilian deaths  •  Cyberattack spans 7 European countries",
              font=font(SANS_B, 9), fill=INK)


def make_page():
    image = Image.new("RGB", (SIZE, SIZE), PAPER)
    draw = ImageDraw.Draw(image)
    draw.rectangle((14, 14, 1009, 1010), outline=INK, width=2)
    centered(draw, "THE WORLD TODAY", 21, font(SERIF_B, 42), INK)
    centered(draw, "WEDNESDAY, 18 NOVEMBER 2026     •     WORLD EDITION", 68,
             font(SANS_B, 12), BLUE)
    centered(draw, "50 STORIES  •  6 CONTINENTS", 86, font(SANS_B, 12), RED)
    draw.line((32, 102, 992, 102), fill=INK, width=2)
    draw_map(draw)

    draw.text((36, 229), "LEAD STORY  /  MANILA", font=font(SANS_B, 11), fill=RED)
    draw.text((35, 244), "TRUMP ARRIVES FOR QUAD TALKS AHEAD OF CHINA VISIT",
              font=font(SERIF_B, 22), fill=INK)
    draw.text((36, 273), "US, India, Japan and Australia put maritime security, AI and critical minerals",
              font=font(SANS, 12), fill=BLUE)
    draw.text((36, 292), "on the agenda as APEC's leaders meet in Shenzhen, Nov. 18–19.",
              font=font(SANS, 12), fill=BLUE)
    draw.line((32, 318, 992, 318), fill=INK, width=2)

    draw_sections(draw)
    draw_market(draw)
    draw_timeline(draw)
    draw_numbers(draw)
    return image


def main():
    output = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "out"))
    output.mkdir(parents=True, exist_ok=True)
    make_page().save(output / "entry.png", format="PNG", optimize=True, compress_level=9)


if __name__ == "__main__":
    main()
