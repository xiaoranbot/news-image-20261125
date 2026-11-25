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
    size = len(payload).to_bytes(4, "big")
    check = (crc32(body) & 0xFFFFFFFF).to_bytes(4, "big")
    return size + body + check


def encode_png(rgb, width, height):
    """Encode raw RGB bytes (row-major, no alpha) as a PNG file.

    Filter type 0 on every scanline and a fixed zlib level keep the
    output byte-for-byte identical across runs.
    """
    row_bytes = width * 3
    scanlines = bytearray()
    for yy in range(height):
        scanlines.append(0)
        scanlines += rgb[yy * row_bytes:(yy + 1) * row_bytes]
    blob = zlib.compress(bytes(scanlines), 9)
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    magic = b"\x89PNG\r\n\x1a\n"
    return (magic + _png_chunk(b"IHDR", ihdr) +
            _png_chunk(b"IDAT", blob) + _png_chunk(b"IEND", b""))


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
    return scale * (len(text) * CHAR_W - 1)


class Page:
    """An RGB pixel buffer with small drawing helpers."""

    def __init__(self, width, height, background):
        self.width = width
        self.height = height
        self.pixels = bytearray(background * (width * height))

    def put(self, px, py, color):
        if not (0 <= px < self.width and 0 <= py < self.height):
            return
        off = (py * self.width + px) * 3
        self.pixels[off:off + 3] = bytes(color)

    def rect(self, rx, ry, rw, rh, color):
        for yy in range(ry, ry + rh):
            for xx in range(rx, rx + rw):
                self.put(xx, yy, color)

    def hline(self, hx, hy, hw, color, thick=1):
        self.rect(hx, hy, hw, thick, color)

    def vline(self, vx, vy, vh, color, thick=1):
        self.rect(vx, vy, thick, vh, color)

    def disc(self, cx, cy, r, color):
        """Filled circle, centre (cx, cy), radius r."""
        rr = r * r
        for yy in range(cy - r, cy + r + 1):
            dy = yy - cy
            for xx in range(cx - r, cx + r + 1):
                dx = xx - cx
                if dx * dx + dy * dy <= rr:
                    self.put(xx, yy, color)

    def ring(self, cx, cy, r, color, thick=2):
        for yy in range(cy - r - thick, cy + r + thick + 1):
            for xx in range(cx - r - thick, cx + r + thick + 1):
                dist = math.hypot(xx - cx, yy - cy)
                if r - thick <= dist <= r:
                    self.put(xx, yy, color)

    def triangle(self, x0, y0, x1, y1, x2, y2, color):
        """Filled triangle via a scanline walk."""
        corners = [(x0, y0), (x1, y1), (x2, y2)]
        top = min(c[1] for c in corners)
        bottom = max(c[1] for c in corners)
        edges = ((corners[0], corners[1]),
                 (corners[1], corners[2]),
                 (corners[2], corners[0]))
        for yy in range(top, bottom + 1):
            hits = []
            for (ax, ay), (bx, by) in edges:
                if ay == by:
                    continue
                if min(ay, by) <= yy < max(ay, by):
                    hits.append(ax + (yy - ay) * (bx - ax) / (by - ay))
            if len(hits) >= 2:
                for xx in range(int(min(hits)), int(max(hits)) + 1):
                    self.put(xx, yy, color)

    def glyph(self, gx, gy, char, scale, color):
        rows = GLYPHS.get(char)
        if rows is None:
            return
        for rnum, row in enumerate(rows):
            for cnum, cell in enumerate(row):
                if cell == "#":
                    self.rect(gx + cnum * scale, gy + rnum * scale,
                              scale, scale, color)

    def text(self, tx, ty, string, scale, color):
        """Draw a string; returns the x just past its last glyph."""
        pen = tx
        for ch in string:
            self.glyph(pen, ty, ch, scale, color)
            pen += CHAR_W * scale
        return pen - scale

    def text_centered(self, mid, ty, string, scale, color):
        start = mid - text_width(string, scale) // 2
        return self.text(start, ty, string, scale, color)

    def text_right(self, right, ty, string, scale, color):
        start = right - text_width(string, scale)
        return self.text(start, ty, string, scale, color)

    def paragraph(self, px, py, string, scale, color, max_width, leading):
        """Word-wrap a paragraph; returns the y just past its last line."""
        wrapped = []
        current = ""
        for word in string.split():
            candidate = word if not current else current + " " + word
            if text_width(candidate, scale) <= max_width or not current:
                current = candidate
            else:
                wrapped.append(current)
                current = word
        if current:
            wrapped.append(current)
        cursor = py
        for row in wrapped:
            self.text(px, cursor, row, scale, color)
            cursor += leading
        return cursor


# ------------------------------------------------------------ masthead

def draw_masthead(page):
    page.rect(24, 24, 976, 88, NAVY)
    page.text(48, 48, "THE WORLD TODAY", 6, WHITE)
    page.text_right(976, 38, "WEDNESDAY", 3, GOLD_BRIGHT)
    page.text_right(976, 70, "25 NOVEMBER 2026", 3, WHITE)
    page.hline(24, 120, 976, RED, 6)


# ------------------------------------------------------------ top story

def draw_chip(page, ox, oy):
    """A green processor with pins, labelled NVDA, on the navy panel."""
    page.text(ox, oy, "THE CHIP GIANT", 2, GOLD_BRIGHT)
    px, py, pw, ph = ox, oy + 34, 210, 130
    # pins around the package
    for i in range(5):
        page.rect(px + 18 + i * 38, py - 10, 12, 10, CREAM)
        page.rect(px + 18 + i * 38, py + ph, 12, 10, CREAM)
    for i in range(3):
        page.rect(px - 10, py + 18 + i * 38, 10, 12, CREAM)
        page.rect(px + pw, py + 18 + i * 38, 10, 12, CREAM)
    page.rect(px, py, pw, ph, GREEN)
    page.rect(px + 10, py + 10, pw - 20, ph - 20, GREEN_DARK)
    page.text_centered(px + pw // 2, py + 44, "NVDA", 5, WHITE)
    page.text_centered(px + pw // 2, py + 96, "NVIDIA", 2, CREAM)


def draw_bars(page, ox, oy):
    """Five falling bars for the share-price slide, last one in red."""
    heights = [100, 80, 62, 44, 26]
    colors = [GREEN, GREEN, TEAL, TEAL, RED]
    for i, tall in enumerate(heights):
        page.rect(ox + i * 42, oy + 100 - tall, 30, tall, colors[i])


def draw_top_story(page):
    top = 136
    # left: navy illustration panel
    page.rect(24, top, 476, 500 - top, NAVY)
    draw_chip(page, 84, top + 22)
    draw_bars(page, 84, top + 226)
    page.text(312, top + 262, "-7%", 6, RED)
    page.text(316, top + 306, "IN ONE DAY", 2, CREAM)
    # right: headline column
    col = 524
    page.text(col, top + 6, "TECH - MARKETS", 2, RED)
    page.text(col, top + 34, "THE RALLY FADES", 5, INK)
    page.paragraph(col, top + 108, "NVDA SLIDES 7% AS CONGRESS QUESTIONS "
                   "HUANG RETURN",
                   3, INK, 476, 34)
    page.paragraph(
        col, top + 196,
        "NVIDIA SHARES FELL ABOUT 7% ON TUESDAY AS THE RALLY FROM "
        "JENSEN HUANG'S RETURN FADED AND LAWMAKERS QUESTIONED "
        "PRESIDENT TRUMP'S ROLE IN BRINGING HIM BACK. ASIAN TECH "
        "STOCKS FELL WITH IT.",
        2, INK, 476, 22)
    page.rect(col, top + 316, 200, 34, RED)
    page.text_centered(col + 100, top + 326, "NVDA -7%", 2, WHITE)
    page.rect(col + 220, top + 316, 220, 34, NAVY)
    page.text_centered(col + 330, top + 326, "NIKKEI -2.76%", 2, WHITE)
    page.hline(24, 514, 976, GREY_LINE, 2)


# ------------------------------------------------------------ middle row

def draw_mine(page, mx, my, mr, color):
    """A spiked naval mine: dark disc with eight spikes."""
    page.disc(mx, my, mr, color)
    for k in range(8):
        ang = k * math.pi / 4
        sx = mx + int((mr + 5) * math.cos(ang))
        sy = my + int((mr + 5) * math.sin(ang))
        page.disc(sx, sy, 2, color)


def draw_hormuz(page, ox, oy, ow, oh):
    """Strait of Hormuz: sky and sea, a tanker, mines and a blast."""
    page.rect(ox, oy, ow, oh // 2, SKY)
    page.rect(ox, oy + oh // 2, ow, oh - oh // 2, SEA)
    page.disc(ox + ow - 52, oy + 26, 16, (240, 214, 130))  # low sun
    # tanker silhouette
    hx, hy = ox + 60, oy + oh // 2 + 8
    page.rect(hx, hy, 150, 26, INK)
    page.rect(hx + 110, hy - 22, 26, 22, INK)
    page.rect(hx + 116, hy - 34, 14, 12, INK)
    page.triangle(hx - 24, hy + 26, hx, hy, hx, hy + 26, INK)
    # mines floating in the strait
    draw_mine(page, ox + 268, oy + oh - 26, 9, INK)
    draw_mine(page, ox + 330, oy + oh - 18, 7, INK)
    # blast where a mine struck
    page.disc(hx + 196, hy - 8, 14, ORANGE)
    page.disc(hx + 212, hy - 20, 8, GOLD_BRIGHT)
    page.disc(hx + 186, hy - 22, 5, RED)
    # wake lines
    for i, wy in enumerate((oy + oh - 30, oy + oh - 20, oy + oh - 10)):
        page.hline(ox + 40 + i * 40, wy, ow - 100 - i * 40, CREAM, 2)


def draw_gulf_strike(page, ox, oy, ow, oh):
    """Gulf of Finland: sky and sea, a cargo ship, a drone overhead."""
    page.rect(ox, oy, ow, oh // 2, SKY)
    page.rect(ox, oy + oh // 2, ow, oh - oh // 2, SEA)
    page.disc(ox + 52, oy + 26, 16, (240, 214, 130))  # low sun
    # cargo ship silhouette
    hx, hy = ox + 96, oy + oh // 2 - 6
    page.rect(hx, hy - 30, 128, 30, INK)
    page.rect(hx + 20, hy - 52, 30, 22, INK)
    page.rect(hx + 62, hy - 44, 22, 14, INK)
    page.vline(hx + 34, hy - 70, 18, INK, 3)
    page.triangle(hx - 26, hy, hx, hy - 30, hx, hy, INK)
    # drone above the ship, with spinning rotors
    dx, dy = hx + 150, oy + 22
    page.disc(dx, dy, 6, INK)
    page.rect(dx - 22, dy - 2, 44, 3, INK)
    page.disc(dx - 24, dy, 5, INK)
    page.disc(dx + 24, dy, 5, INK)
    page.rect(dx - 3, dy + 6, 6, 8, RED)
    # wake lines
    for i, wy in enumerate((oy + oh - 30, oy + oh - 20, oy + oh - 10)):
        page.hline(ox + 60 + i * 40, wy, ow - 120 - i * 40, CREAM, 2)


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


def draw_trophy(page, ox, oy, ow, oh):
    """Navy panel with a gold Africa Cup trophy under a star."""
    page.rect(ox, oy, ow, oh, NAVY)
    page.disc(ox + ow - 26, oy + 22, 4, GOLD_BRIGHT)
    page.disc(ox + 24, oy + 18, 3, WHITE)
    page.disc(ox + 40, oy + 30, 2, WHITE)
    cx = ox + ow // 2
    # star above the cup
    page.disc(cx, oy + 18, 4, GOLD_BRIGHT)
    page.rect(cx - 9, oy + 17, 18, 2, GOLD_BRIGHT)
    page.rect(cx - 1, oy + 9, 2, 18, GOLD_BRIGHT)
    # cup
    page.rect(cx - 24, oy + 30, 48, 34, GOLD)
    page.rect(cx - 24, oy + 30, 48, 8, GOLD_BRIGHT)
    # handles
    page.ring(cx - 30, oy + 46, 10, GOLD, 3)
    page.ring(cx + 30, oy + 46, 10, GOLD, 3)
    # stem and base
    page.rect(cx - 5, oy + 64, 10, 22, GOLD)
    page.rect(cx - 22, oy + 86, 44, 8, GOLD_BRIGHT)
    page.rect(cx - 28, oy + 94, 56, 8, GOLD)


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
    for edge in ("top", "bottom", "left", "right"):
        if edge == "top":
            page.rect(0, 0, WIDTH, 8, NAVY)
        elif edge == "bottom":
            page.rect(0, HEIGHT - 8, WIDTH, 8, NAVY)
        elif edge == "left":
            page.rect(0, 0, 8, HEIGHT, NAVY)
        else:
            page.rect(WIDTH - 8, 0, 8, HEIGHT, NAVY)
    for section in (draw_masthead, draw_top_story, draw_middle_row,
                    draw_bottom_row, draw_footer):
        section(page)
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
