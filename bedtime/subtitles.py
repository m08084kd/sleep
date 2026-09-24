"""字幕の画像・SRT とサムネイルを作る。"""

from __future__ import annotations

import unicodedata

from . import svgkit as k
from .scenes import FONT, render_scene


def _text_width(s: str, size: float) -> float:
    return sum(size if unicodedata.east_asian_width(c) in "WFA" else size * 0.55 for c in s)


def wrap(text: str, max_chars: int = 20) -> list[str]:
    """分かち書き（空白）の位置で折り返す。改行（\\n）はそのまま使う。"""
    lines: list[str] = []
    for para in text.split("\n"):
        cur = ""
        for word in para.split(" "):
            cand = f"{cur} {word}" if cur else word
            if cur and len(cand) > max_chars:
                lines.append(cur)
                cur = word
            else:
                cur = cand
        if cur:
            lines.append(cur)
    return lines


def subtitle_svg(text: str, w: int = k.W, h: int = k.H, size: int = 54) -> str:
    lines = wrap(text)
    lh = size * 1.45
    box_w = max(_text_width(line, size) for line in lines) + size * 1.6
    box_h = lh * len(lines) + size * 0.7
    x0 = (w - box_w) / 2
    y0 = h - box_h - 56
    body = (f'<rect x="{x0:.0f}" y="{y0:.0f}" width="{box_w:.0f}" height="{box_h:.0f}" '
            f'rx="{box_h / 2 if len(lines) == 1 else 40:.0f}" fill="#1b1840" opacity="0.42"/>')
    for i, line in enumerate(lines):
        y = y0 + size * 0.35 + lh * (i + 0.5) + size * 0.35
        body += (f'<text x="{w / 2:.0f}" y="{y:.0f}" font-family="{FONT}" font-size="{size}" '
                 f'text-anchor="middle" fill="#fff8e6">{_esc(line)}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{body}</svg>'


def thumbnail_svg(title: str, subtitle: str = "") -> str:
    """YouTube 用サムネイル（タイトル画面の絵に、大きめの文字をのせる）。"""
    svg = render_scene("title")
    lines = wrap(title, 10)
    size = 128
    body = ""
    top = 250 if len(lines) > 1 else 330
    for i, line in enumerate(lines):
        y = top + i * size * 1.3
        for dx, dy in [(-5, 0), (5, 0), (0, -5), (0, 5), (4, 4), (-4, 4), (4, -4), (-4, -4)]:
            body += (f'<text x="{960 + dx}" y="{y + dy:.0f}" font-family="{FONT}" font-size="{size}" '
                     f'text-anchor="middle" fill="#3a2f6b">{_esc(line)}</text>')
        body += (f'<text x="960" y="{y:.0f}" font-family="{FONT}" font-size="{size}" '
                 f'text-anchor="middle" fill="#fff6d2">{_esc(line)}</text>')
    if subtitle:
        y = top + len(lines) * size * 1.3 + 10
        body += (f'<rect x="{960 - _text_width(subtitle, 64) / 2 - 40:.0f}" y="{y - 70:.0f}" '
                 f'width="{_text_width(subtitle, 64) + 80:.0f}" height="100" rx="50" fill="#f59fa0"/>')
        body += (f'<text x="960" y="{y:.0f}" font-family="{FONT}" font-size="64" text-anchor="middle" '
                 f'fill="#fffaf0">{_esc(subtitle)}</text>')
    return svg.replace("</svg>", body + "</svg>")


def srt_time(t: float) -> str:
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def _esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
