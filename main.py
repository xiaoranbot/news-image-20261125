"""Draw the front page of THE WORLD TODAY for Wednesday 25 November 2026.

Pure standard library. Renders a 1024x1024 PNG newspaper front page:
Nvidia slides 7% as lawmakers question Trump's role in Huang's return,
mines hit two tankers in the Strait of Hormuz, Zelenskiy confirms the
Gulf of Finland ship strike, Pakistan's first astronaut reaches China's
space station, and Senegal gets the Africa Cup back, plus a briefs ticker.

Run:  MAKEFUN_OUTPUT_DIR=out python3 main.py
Output is deterministic: two runs produce byte-identical PNGs.
"""

import math
import os
import struct
import zlib
from binascii import crc32

WIDTH = 1024
HEIGHT = 1024

CREAM = (244, 239, 228)
NAVY = (16, 24, 64)
NAVY_SOFT = (24, 36, 84)
INK = (26, 26, 26)
RED = (178, 34, 34)
GOLD = (201, 162, 39)
GOLD_BRIGHT = (232, 184, 32)
GREEN = (34, 139, 34)
GREEN_DARK = (27, 94, 32)
TEAL = (42, 122, 120)
BLUE_EU = (0, 51, 153)
SKY = (168, 205, 230)
SEA = (16, 92, 99)
ORANGE = (232, 120, 24)
WHITE = (255, 255, 255)
GREY_LINE = (201, 196, 184)


# ---------------------------------------------------------------- PNG writer

def _png_chunk(kind, payload):
    """One PNG chunk: length, type, data, CRC."""
    body = kind + payload
    return struct.pack(">I", len(payload)) + body + struct.pack(
        ">I", crc32(body) & 0xFFFFFFFF)


def encode_png(rgb, width, height):
    """Encode raw RGB bytes (row-major, no alpha) as a PNG file.

    Filter type 0 on every scanline and a fixed zlib level keep the
    output byte-for-byte identical across runs.
    """
    raw = bytearray()
    stride = width * 3
    for y in range(height):
        raw.append(0)
        raw += rgb[y * stride:(y + 1) * stride]
    compressed = zlib.compress(bytes(raw), 9)
    header = struct.pack(">8s", b"\x89PNG\r\n\x1a\n")
    ihdr = _png_chunk(b"IHDR", struct.pack(
        ">IIBBBBB", width, height, 8, 2, 0, 0, 0))
    return header + ihdr + _png_chunk(b"IDAT", compressed) + _png_chunk(
        b"IEND", b"")


# ------------------------------------------------------------ bitmap font

# Hand-drawn 5x7 pixel glyphs. Each glyph is seven rows of five cells;
# '#' is ink, '.' is blank. Only the characters the page needs are here.
GLYPHS = {
    "A": (
        ".###.",
        "#...#",
        "#...#",
        "#####",
        "#...#",
        "#...#",
        "#...#",
    ),
    "B": (
        "####.",
        "#...#",
        "#...#",
        "####.",
        "#...#",
        "#...#",
        "####.",
    ),
    "C": (
        ".####",
        "#....",
        "#....",
        "#....",
        "#....",
        "#....",
        ".####",
    ),
    "D": (
        "####.",
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        "####.",
    ),
    "E": (
        "#####",
        "#....",
        "#....",
        "####.",
        "#....",
        "#....",
        "#####",
    ),
    "F": (
        "#####",
        "#....",
        "#....",
        "####.",
        "#....",
        "#....",
        "#....",
    ),
    "G": (
        ".####",
        "#....",
        "#....",
        "#.###",
        "#...#",
        "#...#",
        ".###.",
    ),
    "H": (
        "#...#",
        "#...#",
        "#...#",
        "#####",
        "#...#",
        "#...#",
        "#...#",
    ),
    "I": (
        ".###.",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
        ".###.",
    ),
    "J": (
        "..###",
        "...#.",
        "...#.",
        "...#.",
        "...#.",
        "#..#.",
        ".##..",
    ),
    "K": (
        "#...#",
        "#..#.",
        "#.#..",
        "##...",
        "#.#..",
        "#..#.",
        "#...#",
    ),
    "L": (
        "#....",
        "#....",
        "#....",
        "#....",
        "#....",
        "#....",
        "#####",
    ),
    "M": (
        "#...#",
        "##.##",
        "#.#.#",
        "#.#.#",
        "#...#",
        "#...#",
        "#...#",
    ),
}

GLYPHS.update({
    "N": (
        "#...#",
        "##..#",
        "#.#.#",
        "#..##",
        "#...#",
        "#...#",
        "#...#",
    ),
    "O": (
        ".###.",
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        ".###.",
    ),
    "P": (
        "####.",
        "#...#",
        "#...#",
        "####.",
        "#....",
        "#....",
        "#....",
    ),
    "Q": (
        ".###.",
        "#...#",
        "#...#",
        "#...#",
        "#.#.#",
        "#..#.",
        ".##.#",
    ),
    "R": (
        "####.",
        "#...#",
        "#...#",
        "####.",
        "#.#..",
        "#..#.",
        "#...#",
    ),
    "S": (
        ".####",
        "#....",
        "#....",
        ".###.",
        "....#",
        "....#",
        "####.",
    ),
    "T": (
        "#####",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
    ),
    "U": (
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        ".###.",
    ),
    "V": (
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        ".#.#.",
        "..#..",
    ),
    "W": (
        "#...#",
        "#...#",
        "#...#",
        "#.#.#",
        "#.#.#",
        "##.##",
        "#...#",
    ),
    "X": (
        "#...#",
        "#...#",
        ".#.#.",
        "..#..",
        ".#.#.",
        "#...#",
        "#...#",
    ),
    "Y": (
        "#...#",
        "#...#",
        ".#.#.",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
    ),
    "Z": (
        "#####",
        "....#",
        "...#.",
        "..#..",
        ".#...",
        "#....",
        "#####",
    ),
    "0": (
        ".###.",
        "#...#",
        "#..##",
        "#.#.#",
        "##..#",
        "#...#",
        ".###.",
    ),
    "1": (
        "..#..",
        ".##..",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
        ".###.",
    ),
    "2": (
        ".###.",
        "#...#",
        "....#",
        "...#.",
        "..#..",
        ".#...",
        "#####",
    ),
    "3": (
        "####.",
        "....#",
        "....#",
        ".###.",
        "....#",
        "....#",
        "####.",
    ),
    "4": (
        "...#.",
        "..##.",
        ".#.#.",
        "#..#.",
        "#####",
        "...#.",
        "...#.",
    ),
    "5": (
        "#####",
        "#....",
        "####.",
        "....#",
        "....#",
        "#...#",
        ".###.",
    ),
    "6": (
        ".###.",
        "#....",
        "#....",
        "####.",
        "#...#",
        "#...#",
        ".###.",
    ),
    "7": (
        "#####",
        "....#",
        "...#.",
        "...#.",
        "..#..",
        "..#..",
        "..#..",
    ),
    "8": (
        ".###.",
        "#...#",
        "#...#",
        ".###.",
        "#...#",
        "#...#",
        ".###.",
    ),
    "9": (
        ".###.",
        "#...#",
        "#...#",
        ".####",
        "....#",
        "....#",
        ".###.",
    ),
    ".": (
        ".....",
        ".....",
        ".....",
        ".....",
        ".....",
        ".##..",
        ".##..",
    ),
    ",": (
        ".....",
        ".....",
        ".....",
        ".....",
        ".##..",
        ".##..",
        ".#...",
    ),
    "-": (
        ".....",
        ".....",
        ".....",
        ".###.",
        ".....",
        ".....",
        ".....",
    ),
    "+": (
        ".....",
        "..#..",
        "..#..",
        ".###.",
        "..#..",
        "..#..",
        ".....",
    ),
    "%": (
        "##..#",
        "##.#.",
        "...#.",
        "..#..",
        ".#...",
        "#.##.",
        "#..##",
    ),
    ":": (
        ".....",
        ".##..",
        ".##..",
        ".....",
        ".##..",
        ".##..",
        ".....",
    ),
    "/": (
        "....#",
        "....#",
        "...#.",
        "..#..",
        ".#...",
        "#....",
        "#....",
    ),
    "(": (
        "...##",
        "..#..",
        ".#...",
        ".#...",
        ".#...",
        "..#..",
        "...##",
    ),
    ")": (
        "##...",
        "..#..",
        "...#.",
        "...#.",
        "...#.",
        "..#..",
        "##...",
    ),
    "'": (
        "..#..",
        "..#..",
        "..#..",
        ".....",
        ".....",
        ".....",
        ".....",
    ),
    "&": (
        ".###.",
        "#...#",
        "#.#..",
        ".#...",
        "#.#.#",
        "#..#.",
        ".##.#",
    ),
    " ": (
        ".....",
        ".....",
        ".....",
        ".....",
        ".....",
        ".....",
        ".....",
    ),
})


# ------------------------------------------------------------ canvas

CHAR_W = 6  # 5 glyph columns + 1 column of tracking, in font units


def text_width(text, scale):
    """Pixel width of a string at a given scale."""
    return len(text) * CHAR_W * scale - scale


class Page:
    """An RGB pixel buffer with small drawing helpers."""

    def __init__(self, width, height, background):
        self.width = width
        self.height = height
        self.pixels = bytearray(background * (width * height))

    def put(self, x, y, color):
        if 0 <= x < self.width and 0 <= y < self.height:
            i = (y * self.width + x) * 3
            self.pixels[i:i + 3] = bytes(color)

    def rect(self, x, y, w, h, color):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.put(xx, yy, color)

    def hline(self, x, y, w, color, thick=1):
        self.rect(x, y, w, thick, color)

    def vline(self, x, y, h, color, thick=1):
        self.rect(x, y, thick, h, color)

    def disc(self, cx, cy, r, color):
        """Filled circle, centre (cx, cy), radius r."""
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                    self.put(xx, yy, color)

    def ring(self, cx, cy, r, color, thick=2):
        for yy in range(cy - r - thick, cy + r + thick + 1):
            for xx in range(cx - r - thick, cx + r + thick + 1):
                d = math.hypot(xx - cx, yy - cy)
                if r - thick <= d <= r:
                    self.put(xx, yy, color)

    def triangle(self, x0, y0, x1, y1, x2, y2, color):
        """Filled triangle via a scanline walk."""
        top = min(y0, y1, y2)
        bottom = max(y0, y1, y2)
        pts = [(x0, y0), (x1, y1), (x2, y2)]
        for yy in range(top, bottom + 1):
            xs = []
            for (ax, ay), (bx, by) in ((pts[0], pts[1]),
                                       (pts[1], pts[2]),
                                       (pts[2], pts[0])):
                if ay == by:
                    continue
                if min(ay, by) <= yy < max(ay, by):
                    xs.append(ax + (yy - ay) * (bx - ax) / (by - ay))
            if len(xs) >= 2:
                for xx in range(int(min(xs)), int(max(xs)) + 1):
                    self.put(xx, yy, color)

    def glyph(self, x, y, char, scale, color):
        rows = GLYPHS.get(char)
        if rows is None:
            return
        for ry, row in enumerate(rows):
            for rx, cell in enumerate(row):
                if cell == "#":
                    self.rect(x + rx * scale, y + ry * scale,
                              scale, scale, color)

    def text(self, x, y, string, scale, color):
        """Draw a string; returns the x just past its last glyph."""
        cx = x
        for char in string:
            self.glyph(cx, y, char, scale, color)
            cx += CHAR_W * scale
        return cx - scale

    def text_centered(self, cx, y, string, scale, color):
        x = cx - text_width(string, scale) // 2
        return self.text(x, y, string, scale, color)

    def text_right(self, right, y, string, scale, color):
        x = right - text_width(string, scale)
        return self.text(x, y, string, scale, color)

    def paragraph(self, x, y, string, scale, color, max_width, leading):
        """Word-wrap a paragraph; returns the y just past its last line."""
        words = string.split()
        lines = []
        line = ""
        for word in words:
            trial = word if not line else line + " " + word
            if text_width(trial, scale) <= max_width or not line:
                line = trial
            else:
                lines.append(line)
                line = word
        if line:
            lines.append(line)
        for row in lines:
            self.text(x, y, row, scale, color)
            y += leading
        return y


# ------------------------------------------------------------ masthead

def draw_masthead(page):
    page.rect(24, 24, 976, 88, NAVY)
    page.text(48, 48, "THE WORLD TODAY", 6, WHITE)
    page.text_right(976, 38, "WEDNESDAY", 3, GOLD_BRIGHT)
    page.text_right(976, 70, "25 NOVEMBER 2026", 3, WHITE)
    page.hline(24, 120, 976, RED, 6)


# ------------------------------------------------------------ top story

def draw_chip(page, x, y):
    """A green processor with pins, labelled NVDA, on the navy panel."""
    page.text(x, y, "THE CHIP GIANT", 2, GOLD_BRIGHT)
    bx, by, bw, bh = x, y + 34, 210, 130
    # pins around the package
    for i in range(5):
        page.rect(bx + 18 + i * 38, by - 10, 12, 10, CREAM)
        page.rect(bx + 18 + i * 38, by + bh, 12, 10, CREAM)
    for i in range(3):
        page.rect(bx - 10, by + 18 + i * 38, 10, 12, CREAM)
        page.rect(bx + bw, by + 18 + i * 38, 10, 12, CREAM)
    page.rect(bx, by, bw, bh, GREEN)
    page.rect(bx + 10, by + 10, bw - 20, bh - 20, GREEN_DARK)
    page.text_centered(bx + bw // 2, by + 44, "NVDA", 5, WHITE)
    page.text_centered(bx + bw // 2, by + 96, "NVIDIA", 2, CREAM)


def draw_bars(page, x, y):
    """Five falling bars for the share-price slide, last one in red."""
    heights = [100, 80, 62, 44, 26]
    colors = [GREEN, GREEN, TEAL, TEAL, RED]
    for i, h in enumerate(heights):
        page.rect(x + i * 42, y + 100 - h, 30, h, colors[i])


def draw_top_story(page):
    top = 136
    bottom = 500
    # left: navy illustration panel
    page.rect(24, top, 476, bottom - top, NAVY)
    draw_chip(page, 84, top + 22)
    draw_bars(page, 84, top + 226)
    page.text(312, top + 262, "-7%", 6, RED)
    page.text(316, top + 306, "IN ONE DAY", 2, CREAM)
    # right: headline column
    x = 524
    page.text(x, top + 6, "TECH - MARKETS", 2, RED)
    page.text(x, top + 34, "THE RALLY FADES", 5, INK)
    page.paragraph(x, top + 108, "NVDA SLIDES 7% AS CONGRESS QUESTIONS "
                   "HUANG RETURN",
                   3, INK, 476, 34)
    page.paragraph(
        x, top + 196,
        "NVIDIA SHARES FELL ABOUT 7% ON TUESDAY AS THE RALLY FROM "
        "JENSEN HUANG'S RETURN FADED AND LAWMAKERS QUESTIONED "
        "PRESIDENT TRUMP'S ROLE IN BRINGING HIM BACK. ASIAN TECH "
        "STOCKS FELL WITH IT.",
        2, INK, 476, 22)
    page.rect(x, top + 316, 200, 34, RED)
    page.text_centered(x + 100, top + 326, "NVDA -7%", 2, WHITE)
    page.rect(x + 220, top + 316, 220, 34, NAVY)
    page.text_centered(x + 330, top + 326, "NIKKEI -2.76%", 2, WHITE)
    page.hline(24, 514, 976, GREY_LINE, 2)


# ------------------------------------------------------------ middle row

def draw_mine(page, cx, cy, r, color):
    """A spiked naval mine: dark disc with eight spikes."""
    page.disc(cx, cy, r, color)
    for i in range(8):
        angle = i * math.pi / 4
        sx = cx + int((r + 5) * math.cos(angle))
        sy = cy + int((r + 5) * math.sin(angle))
        page.disc(sx, sy, 2, color)


def draw_hormuz(page, x, y, w, h):
    """Strait of Hormuz: sky and sea, a tanker, mines and a blast."""
    page.rect(x, y, w, h // 2, SKY)
    page.rect(x, y + h // 2, w, h - h // 2, SEA)
    page.disc(x + w - 52, y + 26, 16, (240, 214, 130))  # low sun
    # tanker silhouette
    sx, sy = x + 60, y + h // 2 + 8
    page.rect(sx, sy, 150, 26, INK)
    page.rect(sx + 110, sy - 22, 26, 22, INK)
    page.rect(sx + 116, sy - 34, 14, 12, INK)
    page.triangle(sx - 24, sy + 26, sx, sy, sx, sy + 26, INK)
    # mines floating in the strait
    draw_mine(page, x + 268, y + h - 26, 9, INK)
    draw_mine(page, x + 330, y + h - 18, 7, INK)
    # blast where a mine struck
    page.disc(sx + 196, sy - 8, 14, ORANGE)
    page.disc(sx + 212, sy - 20, 8, GOLD_BRIGHT)
    page.disc(sx + 186, sy - 22, 5, RED)
    # wake lines
    for i, wy in enumerate((y + h - 30, y + h - 20, y + h - 10)):
        page.hline(x + 40 + i * 40, wy, w - 100 - i * 40, CREAM, 2)


def draw_gulf_strike(page, x, y, w, h):
    """Gulf of Finland: sky and sea, a cargo ship, a drone overhead."""
    page.rect(x, y, w, h // 2, SKY)
    page.rect(x, y + h // 2, w, h - h // 2, SEA)
    page.disc(x + 52, y + 26, 16, (240, 214, 130))  # low sun
    # cargo ship silhouette
    sx, sy = x + 96, y + h // 2 - 6
    page.rect(sx, sy - 30, 128, 30, INK)
    page.rect(sx + 20, sy - 52, 30, 22, INK)
    page.rect(sx + 62, sy - 44, 22, 14, INK)
    page.vline(sx + 34, sy - 70, 18, INK, 3)
    page.triangle(sx - 26, sy, sx, sy - 30, sx, sy, INK)
    # drone above the ship, with spinning rotors
    dx, dy = sx + 150, y + 22
    page.disc(dx, dy, 6, INK)
    page.rect(dx - 22, dy - 2, 44, 3, INK)
    page.disc(dx - 24, dy, 5, INK)
    page.disc(dx + 24, dy, 5, INK)
    page.rect(dx - 3, dy + 6, 6, 8, RED)
    # wake lines
    for i, wy in enumerate((y + h - 30, y + h - 20, y + h - 10)):
        page.hline(x + 60 + i * 40, wy, w - 120 - i * 40, CREAM, 2)


def draw_middle_row(page):
    top = 528
    panel_h = 100
    left_x, right_x = 24, 524
    col_w = 476
    draw_hormuz(page, left_x, top, col_w, panel_h)
    draw_gulf_strike(page, right_x, top, col_w, panel_h)

    ty = top + panel_h + 10
    page.text(left_x, ty, "IRAN WAR", 2, RED)
    page.paragraph(left_x, ty + 24, "TWO TANKERS HIT BY MINES IN HORMUZ",
                   3, INK, col_w, 28)
    page.paragraph(left_x, ty + 82,
                   "IRAN GUARDS SAY MINES STRUCK THE SHIPS IN THE STRAIT. "
                   "HOUTHIS HIT RIYADH TOWER, 11 HURT.",
                   2, INK, col_w, 18)

    page.text(right_x, ty, "UKRAINE", 2, RED)
    page.paragraph(right_x, ty + 24, "KYIV CONFIRMS GULF SHIP STRIKE",
                   3, INK, col_w, 28)
    page.paragraph(right_x, ty + 82,
                   "ZELENSKIY OWNS THE DRONE HIT ON A RUSSIAN CARGO SHIP "
                   "IN THE GULF OF FINLAND. NORWAY URGES CAUTION.",
                   2, INK, col_w, 18)
    page.hline(24, 754, 976, GREY_LINE, 2)


# ------------------------------------------------------------ bottom row

def draw_rocket(page, cx, cy, r):
    """Gold disc carrying a small rocket climbing to the stars."""
    page.disc(cx, cy, r, GOLD)
    # stars
    page.disc(cx - 34, cy - 34, 3, WHITE)
    page.disc(cx + 32, cy - 38, 3, WHITE)
    page.disc(cx + 38, cy + 30, 3, WHITE)
    # rocket body, nose up
    page.rect(cx - 9, cy - 22, 18, 40, WHITE)
    page.triangle(cx - 9, cy - 22, cx + 9, cy - 22, cx, cy - 40, RED)
    page.disc(cx, cy - 6, 5, TEAL)
    page.triangle(cx - 9, cy + 18, cx - 20, cy + 32, cx - 9, cy + 30, RED)
    page.triangle(cx + 9, cy + 18, cx + 20, cy + 32, cx + 9, cy + 30, RED)
    # flame
    page.triangle(cx - 6, cy + 18, cx + 6, cy + 18, cx, cy + 38, ORANGE)
    page.triangle(cx - 3, cy + 18, cx + 3, cy + 18, cx, cy + 30,
                  GOLD_BRIGHT)


def draw_trophy(page, x, y, w, h):
    """Navy panel with a gold Africa Cup trophy under a star."""
    page.rect(x, y, w, h, NAVY)
    page.disc(x + w - 26, y + 22, 4, GOLD_BRIGHT)
    page.disc(x + 24, y + 18, 3, WHITE)
    page.disc(x + 40, y + 30, 2, WHITE)
    cx = x + w // 2
    # star above the cup
    page.disc(cx, y + 18, 4, GOLD_BRIGHT)
    page.rect(cx - 9, y + 17, 18, 2, GOLD_BRIGHT)
    page.rect(cx - 1, y + 9, 2, 18, GOLD_BRIGHT)
    # cup
    page.rect(cx - 24, y + 30, 48, 34, GOLD)
    page.rect(cx - 24, y + 30, 48, 8, GOLD_BRIGHT)
    # handles
    page.ring(cx - 30, y + 46, 10, GOLD, 3)
    page.ring(cx + 30, y + 46, 10, GOLD, 3)
    # stem and base
    page.rect(cx - 5, y + 64, 10, 22, GOLD)
    page.rect(cx - 22, y + 86, 44, 8, GOLD_BRIGHT)
    page.rect(cx - 28, y + 94, 56, 8, GOLD)


def draw_bottom_row(page):
    top = 770
    left_x, right_x = 24, 524
    col_w = 476

    draw_rocket(page, left_x + 52, top + 66, 52)
    page.text(left_x + 122, top + 6, "SPACE", 2, RED)
    page.paragraph(left_x + 122, top + 30,
                   "PAKISTAN FIRST ASTRONAUT IN ORBIT",
                   3, INK, col_w - 122, 30)
    page.paragraph(left_x + 122, top + 96,
                   "PAKISTAN FIRST ASTRONAUT REACHED CHINA SPACE "
                   "STATION ABOARD SHENZHOU.",
                   2, INK, col_w - 122, 20)

    draw_trophy(page, right_x, top, 118, 132)
    page.text(right_x + 134, top + 6, "SPORT", 2, RED)
    page.paragraph(right_x + 134, top + 30, "SENEGAL GETS THE CUP BACK",
                   3, INK, col_w - 134, 30)
    page.paragraph(right_x + 134, top + 96,
                   "THE COURT HANDED SENEGAL THE AFRICA CUP, 10 MONTHS "
                   "AFTER THE CHAOTIC FINAL.",
                   2, INK, col_w - 134, 20)


# ------------------------------------------------------------ footer ticker

def draw_footer(page):
    page.hline(24, 934, 976, RED, 4)
    page.text_centered(
        512, 950,
        "ALSO TODAY: ESTONIA TO SHUT RUSSIA BORDER DEC 1 - COP31 COLLAPSES",
        2, INK)
    page.text_centered(
        512, 972,
        "HUAWEI GUILTY IN U.S. - CIA SYSTEM BREACHED - HOSTAGES FREED",
        2, INK)
    page.text_centered(
        512, 1002, "25 NOVEMBER 2026 - ONE DAY. ONE PAGE. THE WHOLE WORLD",
        1, (110, 105, 95))


# ------------------------------------------------------------ entry point

def build_page():
    page = Page(WIDTH, HEIGHT, CREAM)
    page.rect(0, 0, WIDTH, 8, NAVY)
    page.rect(0, HEIGHT - 8, WIDTH, 8, NAVY)
    page.rect(0, 0, 8, HEIGHT, NAVY)
    page.rect(WIDTH - 8, 0, 8, HEIGHT, NAVY)
    draw_masthead(page)
    draw_top_story(page)
    draw_middle_row(page)
    draw_bottom_row(page)
    draw_footer(page)
    return page


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    page = build_page()
    data = encode_png(bytes(page.pixels), WIDTH, HEIGHT)
    path = os.path.join(out_dir, "entry.png")
    with open(path, "wb") as handle:
        handle.write(data)
    os.chmod(path, 0o644)
    print("wrote {} ({} bytes)".format(path, len(data)))


if __name__ == "__main__":
    main()
