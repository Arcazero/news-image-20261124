#!/usr/bin/env python3
"""Build the 24 November 2026 front page: 'The World Today'.

Six verified stories from Tuesday 24 November 2026, each with its own
generated illustration, set as a newspaper sheet (masthead, weather strip
with real Open-Meteo figures, 2x3 story grid, source footer) and saved as
a 1024x1024 PNG under 1 MiB.

Run from the repository root:  python3 draw.py
"""
import os

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = os.path.dirname(os.path.abspath(__file__))
PHOTO_DIR = os.path.join(ROOT, "assets")
TARGET = os.path.join(ROOT, "entry.png")

PAGE_W, PAGE_H = 1024, 1024
MARGIN = 36
GUTTER = 18
NEWSPRINT = (253, 252, 247)
BLACK = (18, 18, 18)
GREY = (90, 86, 78)
HAIRLINE = (150, 145, 132)
CARD_EDGE = (205, 200, 188)
CARD_FILL = (255, 255, 255)

DEJAVU = "/usr/share/fonts/truetype/dejavu"


def typeface(filename, points):
    return ImageFont.truetype(os.path.join(DEJAVU, filename), points)


MASTHEAD_FONT = typeface("DejaVuSerif-Bold.ttf", 64)
DATE_FONT = typeface("DejaVuSerif-Bold.ttf", 26)
HEADLINE_FONT = typeface("DejaVuSans-Bold.ttf", 21)
BODY_FONT = typeface("DejaVuSans.ttf", 19)
TAG_FONT = typeface("DejaVuSans-Bold.ttf", 15)
CITY_FONT = typeface("DejaVuSans-Bold.ttf", 17)
DETAIL_FONT = typeface("DejaVuSans.ttf", 15)
CREDIT_FONT = typeface("DejaVuSans.ttf", 14)

# tag, illustration, headline, deck — all six verified against reporting
# dated 24 November 2026 (Reuters, CNN, US National Weather Service).
STORIES = [
    dict(tag="POLAND", art="poland.webp",
         head="NATO sends radar jets to Poland after missiles land",
         deck="The alliance will deploy an AWACS early-warning aircraft "
              "after three Russian missiles landed in Poland on Friday."),
    dict(tag="WEATHER", art="storms.webp",
         head="Thanksgiving storms threaten both US coasts",
         deck="Heavy rain and 50 mph gusts threaten the East Coast into "
              "Thanksgiving, as an atmospheric river soaks the West."),
    dict(tag="USA", art="iowa.webp",
         head="Trump halts Iowa explosives blast",
         deck="Trump orders the Army to pause the blast of 68 barrels of "
              "unstable lead azide in Iowa until a court agrees."),
    dict(tag="GULF", art="iran.webp",
         head="Iran vows to defy US naval blockade",
         deck="Tehran says it will use every means to counter the "
              "blockade after Trump threatened to sink ships breaking it."),
    dict(tag="LIBYA", art="libya.webp",
         head="Ukraine sinks Russian warship in Libya",
         deck="Kyiv says maritime drones sank the corvette Merkury in "
              "Benghazi port, taking the war far beyond Europe's shores."),
    dict(tag="ASIA", art="indonesia.webp",
         head="Indonesia factory fire kills 24",
         deck="A blaze at a candy factory in Serang leaves 24 dead and "
              "about 30 missing as rescuers search the wreckage."),
]

# Real Open-Meteo daily forecast for 24 November 2026: high/low, sky, wind.
FORECAST = [
    ("Warsaw", "4° / 1°", "light snow", "24 km/h"),
    ("Tehran", "22° / 9°", "overcast", "10 km/h"),
    ("Benghazi", "22° / 18°", "partly cloudy", "20 km/h"),
    ("Jakarta", "32° / 25°", "thunderstorm", "8 km/h"),
    ("Des Moines", "2° / -3°", "overcast", "10 km/h"),
]

CREDITS = ("Sources: Reuters, CNN, US National Weather Service  •  "
           "Weather: Open-Meteo  •  Illustrations generated for this entry")


def load_photo(name, width, height):
    """Centre-crop an illustration to the card photo slot, 256 colours."""
    shot = Image.open(os.path.join(PHOTO_DIR, name)).convert("RGB")
    shot = ImageOps.fit(shot, (width, height), Image.LANCZOS)
    return shot.convert("P", palette=Image.ADAPTIVE, colors=256).convert("RGB")


def centred(draw, text, y, typeface_, colour):
    x = (PAGE_W - draw.textlength(text, font=typeface_)) / 2
    draw.text((x, y), text, font=typeface_, fill=colour)
    return y + typeface_.size


def draw_masthead(canvas, draw):
    y = 30
    centred(draw, "THE WORLD TODAY", y, MASTHEAD_FONT, BLACK)
    y += 78
    centred(draw, "Tuesday, 24 November 2026", y, DATE_FONT, GREY)
    y += 40
    draw.line([(MARGIN, y), (PAGE_W - MARGIN, y)], fill=HAIRLINE, width=2)
    return y + 12


def draw_weather(canvas, draw, top):
    span = PAGE_W - 2 * MARGIN
    cell = span // len(FORECAST)
    for index, (city, temps, sky, wind) in enumerate(FORECAST):
        left = MARGIN + index * cell
        draw.text((left + 4, top), city, font=CITY_FONT, fill=BLACK)
        draw.text((left + 4, top + 22), temps, font=DETAIL_FONT, fill=GREY)
        draw.text((left + 4, top + 42), f"{sky} · {wind}",
                  font=DETAIL_FONT, fill=GREY)
        if index:
            draw.line([(left - 6, top + 2), (left - 6, top + 58)],
                      fill=HAIRLINE, width=1)
    bottom = top + 66
    draw.line([(MARGIN, bottom), (PAGE_W - MARGIN, bottom)],
              fill=HAIRLINE, width=2)
    return bottom + 14


def draw_card(canvas, draw, story, x0, y0, width, height):
    draw.rectangle([x0, y0, x0 + width, y0 + height],
                   fill=CARD_FILL, outline=CARD_EDGE, width=1)
    photo_h = 96
    canvas.paste(load_photo(story["art"], width, photo_h), (x0, y0))
    label = story["tag"]
    chip_w = draw.textlength(label, font=TAG_FONT) + 18
    chip_top = y0 + photo_h - 30
    draw.rectangle([x0 + 8, chip_top, x0 + 8 + chip_w, chip_top + 22],
                   fill=BLACK)
    draw.text((x0 + 17, chip_top + 3), label, font=TAG_FONT,
              fill=NEWSPRINT)
    pad = 12
    text_x = x0 + pad
    text_w = width - 2 * pad
    cursor = y0 + photo_h + 8
    # Headline: wrap by pixel width using textwrap on a measured basis.
    head_lines = wrap_by_width(draw, story["head"], HEADLINE_FONT, text_w)
    for line in head_lines[:2]:
        draw.text((text_x, cursor), line, font=HEADLINE_FONT, fill=BLACK)
        cursor += 24
    cursor += 2
    deck_lines = wrap_by_width(draw, story["deck"], BODY_FONT, text_w)
    for line in deck_lines[:3]:
        draw.text((text_x, cursor), line, font=BODY_FONT, fill=GREY)
        cursor += 21


def wrap_by_width(draw, text, typeface_, max_width):
    """Split text into lines no wider than max_width pixels."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=typeface_) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_footer(draw, top):
    draw.line([(MARGIN, top), (PAGE_W - MARGIN, top)], fill=HAIRLINE, width=1)
    draw.text((MARGIN, top + 8), CREDITS, font=CREDIT_FONT, fill=GREY)


def build_sheet():
    sheet = Image.new("RGB", (PAGE_W, PAGE_H), NEWSPRINT)
    draw = ImageDraw.Draw(sheet)
    y = draw_masthead(sheet, draw)
    y = draw_weather(sheet, draw, y)
    grid_top = y
    grid_bottom = PAGE_H - 30 - 34
    card_w = (PAGE_W - 2 * MARGIN - GUTTER) // 2
    card_h = (grid_bottom - grid_top - 2 * GUTTER) // 3
    for position, story in enumerate(STORIES):
        row, col = divmod(position, 2)
        x0 = MARGIN + col * (card_w + GUTTER)
        y0 = grid_top + row * (card_h + GUTTER)
        draw_card(sheet, draw, story, x0, y0, card_w, card_h)
    draw_footer(draw, PAGE_H - 30 - 14)
    sheet.save(TARGET, "PNG", optimize=True)
    print(f"wrote {TARGET}: {os.path.getsize(TARGET)} bytes")


if __name__ == "__main__":
    build_sheet()
