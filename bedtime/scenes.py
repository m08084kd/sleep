"""物語の場面ごとのイラスト。

story.yaml の `art:` に書いた名前で呼び出される。物語が進むほど
空の色を暗く・しずかにして、自然に「夜が深くなっていく」ように作っている。
"""

from __future__ import annotations

import random

from . import svgkit as k
from .svgkit import H, PAL, W, g

FONT = "Zen Maru Gothic"


def _text(x, y, s, size, color="#fffaf0", shadow="#2a2450", anchor="middle", weight="normal"):
    common = f'font-family="{FONT}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}"'
    return (f'<text x="{x}" y="{y + size * 0.06:.0f}" {common} fill="{shadow}" opacity="0.45">{s}</text>'
            f'<text x="{x}" y="{y}" {common} fill="{color}">{s}</text>')


# ---------------------------------------------------------------- 場面
def title(title: str = "", subtitle: str = "", **_):
    defs, bg = k.sky("sky", "#2c2f6b", "#6d5fa6", "#e3a8b8")
    defs += k.radial_glow("mglow", "#fff4c9", 0.7) + k.radial_glow("sglow", "#fff6c7", 0.5)
    defs += k.radial_glow("wglow", "#ffdc8a", 0.6)
    body = bg
    body += k.starfield(1, 110, 620, "sglow", 7, avoid=[(1500, 250, 260), (960, 300, 520)])
    body += k.glow(1500, 250, 380, "mglow") + g(k.moon_face(130), 1500, 250)
    body += k.hill(860, 40, "#8a7bb8", 0.4) + k.hill(930, 30, "#6b5f9e", 1.8, 1.1)
    body += g(k.house(True, "wglow"), 360, 940, 0.9)
    for x, s in [(90, 0.8), (620, 0.7), (1780, 0.9)]:
        body += g(k.pine("#4d4a86"), x, 960, s)
    body += g(k.bear_sitting("open"), 1160, 900, 0.8)
    body += g(k.cloud("#9d8fd0", 0.8), 300, 180, 0.8) + g(k.cloud("#8f82c6", 0.7), 900, 110, 0.6)
    if title:
        body += _text(W / 2, 420, title, 104)
    if subtitle:
        body += _text(W / 2, 530, subtitle, 52, color="#fff3c9")
    return k.svg_doc(body, defs)


def yawn(**_):
    """ゆうがたの おへや。ポポが おおきな あくび。"""
    defs = k.linear_gradient("wall", [(0, "#f2d9cf"), (1, "#e3c3c9")])
    defs += k.linear_gradient("dusk", [(0, "#8f7cc4"), (0.6, "#e7a6b4"), (1, "#f8cfa2")])
    defs += k.radial_glow("lg", "#ffe2a0", 0.6)
    body = f'<rect width="{W}" height="{H}" fill="url(#wall)"/>'
    body += f'<rect y="820" width="{W}" height="{H - 820}" fill="#caa38f"/>'
    inner = (f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#dusk)"/>'
             + k.hill(640, 30, "#9b7fb4", 0.3) + g(k.cloud("#fff", 0.5), 1300, 260, 0.5)
             + g(k.cloud("#fff", 0.4), 1600, 360, 0.4))
    body += k.window_frame(1120, 170, 560, 520, inner)
    body += g(k.lamp(True, "lg"), 360, 790, 0.9)
    body += '<ellipse cx="860" cy="930" rx="260" ry="40" fill="#b88d7a" opacity="0.6"/>'
    body += g(k.bear_sitting("closed", mouth="yawn"), 860, 800, 1.35)
    return k.svg_doc(body, defs)


def moon_arrives(**_):
    defs, bg = k.sky("sky", "#23285e", "#4d4b93", "#8d78b3")
    defs += k.radial_glow("bglow", "#fff2b3", 0.75) + k.radial_glow("sglow", "#fff6c7", 0.45)
    defs += k.radial_glow("wglow", "#ffdc8a", 0.55)
    body = bg + k.starfield(2, 120, 700, "sglow", 8, avoid=[(1250, 330, 320)])
    body += k.hill(880, 40, "#5c5391", 0.6)
    body += g(k.house(True, "wglow"), 520, 930, 1.0)
    for x, s in [(120, 0.9), (1780, 0.8), (1560, 0.6)]:
        body += g(k.pine("#3d3b72"), x, 960, s)
    body += k.glow(1250, 330, 360, "bglow")
    body += g(k.moon_boat(), 1250, 360, 0.95, rot=-6)
    body += g(k.bear_sitting("open"), 880, 900, 0.75)
    for i, (x, y) in enumerate([(1060, 520), (1000, 600), (1120, 610)]):
        body += g(k.star_shape(10 - i * 2), x, y, opacity=0.8)
    return k.svg_doc(body, defs)


def sailing(**_):
    defs, bg = k.sky("sky", "#1f2458", "#3b3f84", "#6c64a6")
    defs += k.radial_glow("bglow", "#fff2b3", 0.5) + k.radial_glow("sglow", "#fff6c7", 0.45)
    body = bg + k.starfield(3, 140, 760, "sglow", 9, avoid=[(960, 560, 280)])
    body += g(k.cloud("#b9b3e6", 0.9, 1.4), 300, 900, 1.3) + g(k.cloud("#b9b3e6", 0.9, 1.4), 1650, 920, 1.3)
    body += k.glow(960, 600, 360, "bglow")
    boat = g(k.bear_sitting("open"), -10, -120, 0.62) + k.moon_boat()
    body += g(boat, 960, 680, 1.1, rot=3)
    body += g(k.cloud("#d6d1f5", 1.0, 1.8), 960, 960, 1.5) + g(k.cloud("#c9c3ee", 1.0, 1.4), 400, 1010, 1.4)
    body += g(k.cloud("#c9c3ee", 1.0, 1.4), 1540, 1010, 1.4)
    return k.svg_doc(body, defs)


def sheep_hill(**_):
    defs, bg = k.sky("sky", "#1d2154", "#353a7b", "#5a5699")
    defs += k.radial_glow("sglow", "#fff6c7", 0.4) + k.radial_glow("bglow", "#fff2b3", 0.45)
    body = bg + k.starfield(4, 130, 600, "sglow", 7, avoid=[(1560, 300, 250)])
    body += k.glow(1560, 300, 280, "bglow")
    body += g(k.bear_sitting("sleepy"), 1540, 240, 0.45) + g(k.moon_boat(), 1560, 300, 0.7, rot=-4)
    body += k.hill(760, 60, "#d9d4f3", 0.2, 1.0)
    body += k.hill(860, 40, "#c7c1ea", 1.2, 1.6)
    for x, y, s, flip in [(250, 760, 0.8, False), (560, 720, 0.9, True), (880, 780, 1.0, False),
                          (1230, 800, 0.85, True), (1560, 860, 0.8, False)]:
        body += g(k.sheep(True, True), x, y, s, flip=flip)
    body += g(k.zzz("#fff8e7", 0.9), 900, 640)
    return k.svg_doc(body, defs)


def star_pond(**_):
    defs, bg = k.sky("sky", "#181c4a", "#2b3070", "#3f4488")
    defs += k.radial_glow("sglow", "#fff6c7", 0.45) + k.radial_glow("bglow", "#fff2b3", 0.45)
    body = bg + k.starfield(5, 150, 560, "sglow", 9)
    body += k.water(600, "#27306a", "#9fa8e8")
    # みずに うつる ほし
    rnd = random.Random(11)
    for _ in range(14):
        x, y = rnd.uniform(80, W - 80), rnd.uniform(660, 1040)
        body += k.glow(x, y, 44, "sglow") + g(k.star_shape(rnd.uniform(8, 14)), x, y, opacity=0.8)
    body += k.glow(960, 640, 300, "bglow")
    boat = g(k.bear_sitting("sleepy"), -10, -120, 0.62) + k.moon_boat()
    body += g(boat, 960, 700, 1.0)
    body += '<ellipse cx="960" cy="780" rx="300" ry="26" fill="#fff2b3" opacity="0.15"/>'
    return k.svg_doc(body, defs)


def sleepy_forest(**_):
    defs, bg = k.sky("sky", "#151a44", "#252a62", "#343a78")
    defs += k.radial_glow("sglow", "#fff6c7", 0.4) + k.radial_glow("bglow", "#fff2b3", 0.35)
    body = bg + k.starfield(6, 110, 520, "sglow", 6)
    body += k.hill(840, 30, "#2c355f", 0.3)
    for x, s, c in [(120, 1.1, "#27425d"), (520, 1.25, "#2f4f6b"), (1380, 1.2, "#2f4f6b"), (1800, 1.05, "#27425d")]:
        body += g(k.tree(1.0, c), x, 900, s)
    body += '<rect x="1270" y="560" width="300" height="22" rx="11" fill="#5a4a5e"/>'
    body += g(k.owl_sleeping(), 1380, 480, 0.9)
    body += f'<rect x="0" y="880" width="{W}" height="{H - 880}" fill="#26304f"/>'
    body += g(k.bunny_sleeping(), 700, 920, 1.1)
    body += g(k.squirrel_sleeping(), 1120, 930, 1.0)
    body += k.glow(1000, 280, 220, "bglow")
    body += g(k.bear_sitting("sleepy"), 990, 220, 0.4) + g(k.moon_boat(), 1000, 280, 0.6, rot=2)
    body += g(k.zzz("#fff8e7", 0.8), 610, 810) + g(k.zzz("#fff8e7", 0.7), 1440, 380)
    return k.svg_doc(body, defs)


def going_home(**_):
    defs, bg = k.sky("sky", "#12163d", "#1f2457", "#2d3269")
    defs += k.radial_glow("sglow", "#fff6c7", 0.4) + k.radial_glow("bglow", "#fff2b3", 0.35)
    defs += k.radial_glow("wglow", "#ffdc8a", 0.5)
    body = bg + k.starfield(7, 150, 700, "sglow", 8, avoid=[(700, 360, 220)])
    body += k.hill(880, 50, "#262c5a", 0.8, 1.2)
    body += g(k.house(True, "wglow"), 1300, 900, 0.7)
    for x, s in [(1000, 0.6), (1600, 0.7), (200, 0.8)]:
        body += g(k.pine("#1f2550"), x, 920, s)
    # ほしの みち
    for i in range(9):
        x = 800 + i * 58
        y = 420 + i * 44 - (i * i) * 1.6
        body += g(k.star_shape(6), x, y, opacity=0.25 + 0.06 * i)
    body += k.glow(700, 360, 260, "bglow")
    body += g(k.bear_sitting("sleepy"), 690, 300, 0.45) + g(k.moon_boat(), 700, 360, 0.7, rot=8)
    return k.svg_doc(body, defs)


def in_bed(**_):
    defs = k.linear_gradient("wall", [(0, "#3d3d72"), (1, "#56508a")])
    defs += k.linear_gradient("night", [(0, "#151a44"), (1, "#2d3269")])
    defs += k.radial_glow("lg", "#ffe2a0", 0.35) + k.radial_glow("mglow", "#fff4c9", 0.6)
    body = f'<rect width="{W}" height="{H}" fill="url(#wall)"/>'
    body += f'<rect y="860" width="{W}" height="{H - 860}" fill="#463f73"/>'
    inner = (f'<rect width="{W}" height="{H}" fill="url(#night)"/>'
             + k.starfield(8, 60, 700, None, 0) + k.glow(1480, 380, 200, "mglow")
             + g(k.moon_face(90), 1480, 380))
    body += k.window_frame(1240, 150, 480, 460, inner, "#8b7aa0")
    body += g(k.lamp(True, "lg"), 1660, 860, 0.8)
    body += g(k.bed(), 700, 640, 1.2)
    body += g(k.bear_head("closed"), 530, 600, 0.9, rot=-8)
    body += g(k.quilt(), 700, 640, 1.2)
    body += g(k.zzz("#fff8e7", 0.9), 700, 470)
    return k.svg_doc(body, defs)


def goodnight(**_):
    defs, bg = k.sky("sky", "#0e1233", "#181d4b", "#242a5e")
    defs += k.radial_glow("sglow", "#fff6c7", 0.35) + k.radial_glow("mglow", "#fff4c9", 0.5)
    body = bg + k.starfield(9, 170, 760, "sglow", 9, avoid=[(960, 360, 240)])
    body += k.glow(960, 360, 340, "mglow") + g(k.moon_face(140), 960, 360)
    body += k.hill(900, 40, "#1c2150", 0.5, 1.4)
    body += g(k.house(False), 960, 940, 0.6)
    for x, s in [(560, 0.6), (1360, 0.65), (160, 0.8), (1760, 0.75)]:
        body += g(k.pine("#161a42"), x, 950, s)
    return k.svg_doc(body, defs)


REGISTRY = {
    "title": title,
    "yawn": yawn,
    "moon_arrives": moon_arrives,
    "sailing": sailing,
    "sheep_hill": sheep_hill,
    "star_pond": star_pond,
    "sleepy_forest": sleepy_forest,
    "going_home": going_home,
    "in_bed": in_bed,
    "goodnight": goodnight,
}


def render_scene(name: str, **opts) -> str:
    if name not in REGISTRY:
        raise KeyError(f"未知の art です: {name}（使えるもの: {', '.join(REGISTRY)}）")
    return REGISTRY[name](**opts)
