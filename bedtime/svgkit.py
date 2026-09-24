"""かわいい夜のイラストを SVG で組み立てるための部品集。

すべての部品は SVG 文字列を返す。座標は 1920x1080 のキャンバスを前提とし、
各キャラクターは (x, y) を中心、s を拡大率として配置する。
"""

from __future__ import annotations

import math
import random

W, H = 1920, 1080

# やさしいパステル調の配色
PAL = {
    "bear": "#c9956c",
    "bear_dark": "#a8744f",
    "bear_light": "#f5e0c6",
    "bear_ear": "#eab69a",
    "ink": "#4f3a36",
    "blush": "#f59fa0",
    "cap": "#8ea7e3",
    "cap_band": "#fdf6e3",
    "moon": "#fff1b8",
    "moon_shade": "#f6dc85",
    "star": "#fff6c7",
    "cloud": "#f4f0ff",
    "sheep": "#fffaf1",
    "sheep_face": "#8a7486",
    "tree": "#2f4f6b",
    "tree2": "#3b5f7d",
    "trunk": "#5a4a5e",
    "window": "#ffe39a",
}


# ---------------------------------------------------------------- 基本
def svg_doc(body: str, defs: str = "", w: int = W, h: int = H) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}"><defs>{defs}</defs>{body}</svg>'
    )


def g(content: str, x: float = 0, y: float = 0, s: float = 1, rot: float = 0,
      opacity: float = 1, flip: bool = False) -> str:
    sx = -s if flip else s
    t = f"translate({x:.1f} {y:.1f}) rotate({rot:.1f}) scale({sx:.3f} {s:.3f})"
    op = f' opacity="{opacity:.2f}"' if opacity < 1 else ""
    return f'<g transform="{t}"{op}>{content}</g>'


def linear_gradient(gid: str, stops: list[tuple[float, str]], vertical: bool = True,
                    opacities: list[float] | None = None) -> str:
    x2, y2 = ("0", "1") if vertical else ("1", "0")
    ss = []
    for i, (off, col) in enumerate(stops):
        op = f' stop-opacity="{opacities[i]}"' if opacities else ""
        ss.append(f'<stop offset="{off}" stop-color="{col}"{op}/>')
    return f'<linearGradient id="{gid}" x1="0" y1="0" x2="{x2}" y2="{y2}">{"".join(ss)}</linearGradient>'


def radial_glow(gid: str, color: str, strength: float = 0.8) -> str:
    """中心から外へふんわり消える光。cairosvg はぼかしフィルタが弱いのでグラデーションで表現する。"""
    return (
        f'<radialGradient id="{gid}" cx="0.5" cy="0.5" r="0.5">'
        f'<stop offset="0" stop-color="{color}" stop-opacity="{strength}"/>'
        f'<stop offset="0.35" stop-color="{color}" stop-opacity="{strength * 0.45:.3f}"/>'
        f'<stop offset="1" stop-color="{color}" stop-opacity="0"/>'
        "</radialGradient>"
    )


def glow(x: float, y: float, r: float, gid: str) -> str:
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="url(#{gid})"/>'


def sky(gid: str, top: str, mid: str, bottom: str) -> tuple[str, str]:
    defs = linear_gradient(gid, [(0, top), (0.6, mid), (1, bottom)])
    return defs, f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#{gid})"/>'


# ---------------------------------------------------------------- ほし
def star_shape(r: float = 20, color: str = PAL["star"], points: int = 5) -> str:
    pts = []
    for i in range(points * 2):
        a = -math.pi / 2 + i * math.pi / points
        rr = r if i % 2 == 0 else r * 0.5
        pts.append(f"{rr * math.cos(a):.1f},{rr * math.sin(a):.1f}")
    sw = r * 0.35
    return (f'<polygon points="{" ".join(pts)}" fill="{color}" stroke="{color}" '
            f'stroke-width="{sw:.1f}" stroke-linejoin="round"/>')


def starfield(seed: int, n: int = 90, y_max: float = 700, glow_id: str | None = None,
              big: int = 8, color: str = PAL["star"], avoid: list[tuple[float, float, float]] | None = None) -> str:
    """ランダム（ただし毎回同じ）な星空。avoid=[(x, y, r)] の範囲には置かない。"""
    rnd = random.Random(seed)
    out = []

    def ok(x, y):
        return not any((x - ax) ** 2 + (y - ay) ** 2 < ar ** 2 for ax, ay, ar in (avoid or []))

    for _ in range(n):
        x, y = rnd.uniform(0, W), rnd.uniform(0, y_max)
        if not ok(x, y):
            continue
        r = rnd.choice([1.6, 2.0, 2.4, 3.0, 3.6])
        op = rnd.uniform(0.45, 0.95)
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{color}" opacity="{op:.2f}"/>')
    for _ in range(big):
        x, y = rnd.uniform(60, W - 60), rnd.uniform(40, y_max * 0.8)
        if not ok(x, y):
            continue
        r = rnd.uniform(12, 22)
        if glow_id:
            out.append(glow(x, y, r * 4, glow_id))
        out.append(g(star_shape(r, color), x, y, rot=rnd.uniform(-20, 20)))
    return "".join(out)


# ---------------------------------------------------------------- くも
def cloud(color: str = PAL["cloud"], opacity: float = 1.0, w: float = 1.0) -> str:
    """中心 (0,0)、幅およそ 360*w のふわふわ雲。"""
    circles = [(-110, 10, 62), (-40, -35, 80), (50, -25, 72), (120, 12, 58), (0, 20, 70)]
    body = "".join(
        f'<circle cx="{cx * w:.0f}" cy="{cy}" r="{r}" fill="{color}"/>' for cx, cy, r in circles
    )
    body += f'<rect x="{-170 * w:.0f}" y="10" width="{340 * w:.0f}" height="60" rx="30" fill="{color}"/>'
    return f'<g opacity="{opacity:.2f}">{body}</g>'


# ---------------------------------------------------------------- おつきさま
def closed_eye(x: float, y: float, w: float = 22, color: str = PAL["ink"], sw: float = 6) -> str:
    """ねむっている目（下向きの弧）。"""
    return (f'<path d="M {x - w / 2:.1f} {y:.1f} Q {x:.1f} {y + w * 0.55:.1f} {x + w / 2:.1f} {y:.1f}" '
            f'fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round"/>')


def moon_face(r: float = 120, sleepy: bool = True) -> str:
    c = PAL["moon"]
    body = f'<circle cx="0" cy="0" r="{r}" fill="{c}"/>'
    # うすいクレーター
    for cx, cy, cr in [(-0.45, -0.4, 0.14), (0.5, -0.2, 0.1), (0.35, 0.5, 0.12), (-0.55, 0.35, 0.08)]:
        body += f'<circle cx="{cx * r:.0f}" cy="{cy * r:.0f}" r="{cr * r:.0f}" fill="{PAL["moon_shade"]}" opacity="0.55"/>'
    ey = -0.05 * r
    if sleepy:
        body += closed_eye(-0.32 * r, ey, 0.26 * r, sw=r * 0.045)
        body += closed_eye(0.32 * r, ey, 0.26 * r, sw=r * 0.045)
    else:
        for ex in (-0.32, 0.32):
            body += f'<circle cx="{ex * r:.0f}" cy="{ey:.0f}" r="{0.07 * r:.0f}" fill="{PAL["ink"]}"/>'
    body += (f'<path d="M {-0.12 * r:.0f} {0.22 * r:.0f} Q 0 {0.33 * r:.0f} {0.12 * r:.0f} {0.22 * r:.0f}" '
             f'fill="none" stroke="{PAL["ink"]}" stroke-width="{r * 0.04:.1f}" stroke-linecap="round"/>')
    for ex in (-0.52, 0.52):
        body += f'<ellipse cx="{ex * r:.0f}" cy="{0.18 * r:.0f}" rx="{0.13 * r:.0f}" ry="{0.08 * r:.0f}" fill="{PAL["blush"]}" opacity="0.55"/>'
    return body


def moon_boat() -> str:
    """三日月のふね。中心 (0,0)、幅およそ 440。上に乗る余白は y<-20 あたり。"""
    c, sh = PAL["moon"], PAL["moon_shade"]
    hull = ("M -220 -60 C -170 120, 170 120, 220 -60 "
            "C 130 40, -130 40, -220 -60 Z")
    body = f'<path d="{hull}" fill="{c}"/>'
    body += '<path d="M -150 40 C -60 92, 60 92, 150 40 C 60 75, -60 75, -150 40 Z" fill="' + sh + '" opacity="0.6"/>'
    # ほばしらと ほしの はた
    body += '<rect x="96" y="-190" width="9" height="200" rx="4" fill="#b99a74"/>'
    body += '<path d="M 105 -186 Q 170 -160 105 -118 Z" fill="#f7b9c4"/>'
    body += g(star_shape(15, "#fff6c7"), 101, -198)
    # ふねの かお
    body += closed_eye(-40, 58, 20, sw=5) + closed_eye(14, 58, 20, sw=5)
    body += '<ellipse cx="-66" cy="70" rx="12" ry="7" fill="' + PAL["blush"] + '" opacity="0.6"/>'
    body += '<ellipse cx="40" cy="70" rx="12" ry="7" fill="' + PAL["blush"] + '" opacity="0.6"/>'
    return body


# ---------------------------------------------------------------- くまの ポポ
def _eyes(kind: str, lx: float, rx_: float, y: float) -> str:
    ink = PAL["ink"]
    if kind == "open":
        out = ""
        for x in (lx, rx_):
            out += f'<circle cx="{x}" cy="{y}" r="10" fill="{ink}"/>'
            out += f'<circle cx="{x + 3}" cy="{y - 4}" r="3.5" fill="#fff"/>'
        return out
    if kind == "sleepy":  # はんぶん とじた目
        out = ""
        for x in (lx, rx_):
            out += (f'<path d="M {x - 13} {y - 1} Q {x} {y + 11} {x + 13} {y - 1}" fill="{ink}" />')
            out += (f'<path d="M {x - 14} {y - 2} L {x + 14} {y - 2}" stroke="{ink}" stroke-width="5" stroke-linecap="round"/>')
        return out
    return closed_eye(lx, y, 26) + closed_eye(rx_, y, 26)


def bear_head(eyes: str = "open", cap: bool = True, mouth: str = "smile") -> str:
    """ポポの あたま。中心 (0,0)、はば およそ 200。"""
    b, bl, be, ink = PAL["bear"], PAL["bear_light"], PAL["bear_ear"], PAL["ink"]
    out = ""
    for ex in (-66, 66):
        out += f'<circle cx="{ex}" cy="-62" r="34" fill="{b}"/>'
        out += f'<circle cx="{ex}" cy="-60" r="19" fill="{be}"/>'
    out += f'<ellipse cx="0" cy="0" rx="100" ry="86" fill="{b}"/>'
    out += f'<ellipse cx="0" cy="30" rx="40" ry="29" fill="{bl}"/>'
    out += f'<ellipse cx="0" cy="18" rx="13" ry="9" fill="{ink}"/>'
    if mouth == "yawn":
        out += f'<ellipse cx="0" cy="44" rx="11" ry="14" fill="#8c4a4a"/>'
    else:
        out += (f'<path d="M -12 36 Q -6 44 0 36 Q 6 44 12 36" fill="none" stroke="{ink}" '
                'stroke-width="4" stroke-linecap="round"/>')
    out += _eyes(eyes, -38, 38, -8)
    for ex in (-62, 62):
        out += f'<ellipse cx="{ex}" cy="22" rx="16" ry="10" fill="{PAL["blush"]}" opacity="0.6"/>'
    if cap:
        c, band = PAL["cap"], PAL["cap_band"]
        out += (f'<path d="M -86 -40 Q -60 -118 10 -120 Q 90 -118 150 -70 Q 190 -40 176 10 '
                f'Q 150 -50 80 -58 Q 0 -66 -86 -40 Z" fill="{c}"/>')
        out += f'<path d="M -92 -34 Q 0 -74 92 -40" fill="none" stroke="{band}" stroke-width="20" stroke-linecap="round"/>'
        out += f'<circle cx="178" cy="14" r="20" fill="{band}"/>'
        out += g(star_shape(9, "#fff3a6"), 20, -88)
        out += g(star_shape(7, "#fff3a6"), 90, -80)
    return out


def bear_sitting(eyes: str = "open", cap: bool = True, mouth: str = "smile") -> str:
    """すわっている ポポ。中心 (0,0) は おなか。あたまの上まで およそ -230。"""
    b, bl, bd = PAL["bear"], PAL["bear_light"], PAL["bear_dark"]
    out = ""
    out += f'<ellipse cx="0" cy="40" rx="92" ry="84" fill="{b}"/>'
    out += f'<ellipse cx="0" cy="58" rx="56" ry="52" fill="{bl}"/>'
    for sx in (-1, 1):
        out += f'<ellipse cx="{sx * 84}" cy="36" rx="26" ry="44" fill="{bd}" transform="rotate({sx * -18} {sx * 84} 36)"/>'
        out += f'<ellipse cx="{sx * 48}" cy="118" rx="36" ry="24" fill="{b}"/>'
        out += f'<ellipse cx="{sx * 48}" cy="120" rx="18" ry="12" fill="{PAL["bear_ear"]}"/>'
    out += g(bear_head(eyes, cap, mouth), 0, -110)
    return out


# ---------------------------------------------------------------- ひつじ
def sheep(sleep: bool = True, lying: bool = True) -> str:
    """ふわふわの ひつじ。中心 (0,0)、はば およそ 200。"""
    wool, face = PAL["sheep"], PAL["sheep_face"]
    out = ""
    if not lying:
        for lx in (-50, -20, 25, 55):
            out += f'<rect x="{lx - 9}" y="30" width="18" height="52" rx="9" fill="{face}"/>'
    for cx, cy, r in [(-60, 0, 44), (-20, -30, 48), (30, -28, 46), (62, 4, 42), (0, 18, 50), (-40, 30, 36), (40, 30, 36)]:
        out += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{wool}"/>'
    # かお
    out += f'<ellipse cx="-92" cy="-6" rx="36" ry="42" fill="{face}"/>'
    out += f'<ellipse cx="-124" cy="-26" rx="18" ry="9" fill="{face}" transform="rotate(-25 -124 -26)"/>'
    out += f'<ellipse cx="-62" cy="-30" rx="16" ry="8" fill="{face}" transform="rotate(20 -62 -30)"/>'
    for cx, cy, r in [(-104, -44, 16), (-84, -48, 18), (-66, -40, 14)]:
        out += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{wool}"/>'
    if sleep:
        out += closed_eye(-106, -4, 16, "#fff", 4) + closed_eye(-78, -4, 16, "#fff", 4)
    else:
        out += '<circle cx="-106" cy="-6" r="5" fill="#fff"/><circle cx="-78" cy="-6" r="5" fill="#fff"/>'
    out += f'<ellipse cx="-92" cy="16" rx="9" ry="6" fill="{PAL["blush"]}" opacity="0.7"/>'
    return out


# ---------------------------------------------------------------- もりの どうぶつ
def bunny_sleeping() -> str:
    """まるくなって ねむる うさぎ。中心 (0,0)。"""
    w, pk, ink = "#fbf7f4", "#f6c3cc", PAL["ink"]
    out = f'<ellipse cx="0" cy="10" rx="90" ry="58" fill="{w}"/>'
    out += f'<circle cx="84" cy="30" r="20" fill="#ffffff"/>'
    out += f'<circle cx="-62" cy="-8" r="52" fill="{w}"/>'
    for dy, rot in [(-40, -12), (-24, 4)]:
        out += (f'<ellipse cx="10" cy="{dy}" rx="78" ry="20" fill="{w}" transform="rotate({rot} 10 {dy})"/>'
                f'<ellipse cx="14" cy="{dy}" rx="58" ry="9" fill="{pk}" transform="rotate({rot} 14 {dy})"/>')
    out += closed_eye(-78, -8, 18, ink, 4)
    out += f'<ellipse cx="-96" cy="8" rx="10" ry="6" fill="{PAL["blush"]}" opacity="0.7"/>'
    out += f'<ellipse cx="-110" cy="-2" rx="5" ry="4" fill="{pk}"/>'
    return out


def squirrel_sleeping() -> str:
    """しっぽに くるまって ねむる りす。"""
    fur, light, ink = "#d98c5f", "#f7d9bd", PAL["ink"]
    out = (f'<path d="M 40 50 C 150 40 150 -120 40 -110 C -10 -105 -20 -60 20 -50 '
           f'C 70 -40 80 20 40 50 Z" fill="#e7a176"/>')
    out += f'<path d="M 60 -70 C 100 -60 105 0 60 20" fill="none" stroke="{light}" stroke-width="10" stroke-linecap="round" opacity="0.7"/>'
    out += f'<ellipse cx="-10" cy="20" rx="62" ry="44" fill="{fur}"/>'
    out += f'<circle cx="-60" cy="-6" r="38" fill="{fur}"/>'
    out += f'<path d="M -78 -40 L -70 -70 L -54 -42 Z" fill="{fur}"/>'
    out += f'<ellipse cx="-72" cy="8" rx="18" ry="14" fill="{light}"/>'
    out += closed_eye(-66, -10, 16, ink, 4)
    out += f'<ellipse cx="-44" cy="6" rx="8" ry="5" fill="{PAL["blush"]}" opacity="0.7"/>'
    return out


def owl_sleeping() -> str:
    body, belly, ink = "#9d8aa8", "#e9dff0", PAL["ink"]
    out = f'<ellipse cx="0" cy="0" rx="62" ry="76" fill="{body}"/>'
    out += f'<path d="M -52 -58 L -44 -96 L -20 -66 Z" fill="{body}"/><path d="M 52 -58 L 44 -96 L 20 -66 Z" fill="{body}"/>'
    out += f'<ellipse cx="0" cy="22" rx="40" ry="46" fill="{belly}"/>'
    for ex in (-24, 24):
        out += f'<circle cx="{ex}" cy="-26" r="24" fill="#f4eef8"/>'
        out += closed_eye(ex, -26, 22, ink, 4)
    out += '<path d="M -7 -8 L 7 -8 L 0 6 Z" fill="#f3b457"/>'
    out += f'<ellipse cx="-54" cy="10" rx="18" ry="44" fill="#86739a"/><ellipse cx="54" cy="10" rx="18" ry="44" fill="#86739a"/>'
    out += '<path d="M -20 74 l -6 10 M -14 74 l 0 12 M 14 74 l 0 12 M 20 74 l 6 10" stroke="#f3b457" stroke-width="5" stroke-linecap="round"/>'
    return out


def zzz(color: str = "#fdf6e3", size: float = 1) -> str:
    out = ""
    for i, (dx, dy, fs) in enumerate([(0, 0, 34), (34, -40, 44), (76, -92, 56)]):
        out += (f'<text x="{dx * size:.0f}" y="{dy * size:.0f}" font-family="Zen Maru Gothic" '
                f'font-size="{fs * size:.0f}" fill="{color}" opacity="{0.55 + i * 0.15:.2f}">z</text>')
    return out


# ---------------------------------------------------------------- けしき
def tree(h: float = 1.0, color: str = PAL["tree"]) -> str:
    """まあるい木。根元が (0,0)。"""
    out = f'<rect x="-14" y="{-120 * h:.0f}" width="28" height="{120 * h:.0f}" rx="12" fill="{PAL["trunk"]}"/>'
    for cx, cy, r in [(0, -220, 90), (-60, -150, 70), (60, -150, 70), (0, -130, 70)]:
        out += f'<circle cx="{cx}" cy="{cy * h:.0f}" r="{r}" fill="{color}"/>'
    return out


def pine(color: str = PAL["tree"]) -> str:
    out = f'<rect x="-10" y="-50" width="20" height="50" rx="6" fill="{PAL["trunk"]}"/>'
    for i, (wid, y) in enumerate([(110, -40), (90, -110), (66, -170)]):
        out += (f'<path d="M {-wid} {y} Q 0 {y - 110} {wid} {y} Q 0 {y + 18} {-wid} {y} Z" fill="{color}"/>')
    return out


def hill(y: float, amp: float, color: str, phase: float = 0.0, waves: float = 1.3) -> str:
    pts = []
    for i in range(0, 41):
        x = i * W / 40
        yy = y - amp * math.sin(phase + waves * math.pi * i / 40)
        pts.append(f"{x:.0f},{yy:.0f}")
    return f'<path d="M 0 {H} L {" L ".join(pts)} L {W} {H} Z" fill="{color}"/>'


def house(lit: bool = True, window_glow: str | None = None) -> str:
    """ちいさな おうち。床の中心が (0,0)、はば およそ 300。"""
    wall, roof, door = "#e9d6c6", "#b2677a", "#8e6b5f"
    win = PAL["window"] if lit else "#4a4f7a"
    out = f'<rect x="-140" y="-220" width="280" height="220" rx="18" fill="{wall}"/>'
    out += f'<rect x="70" y="-340" width="40" height="90" rx="6" fill="{roof}"/>'
    out += f'<path d="M -180 -200 L 0 -350 L 180 -200 Q 0 -225 -180 -200 Z" fill="{roof}" stroke="{roof}" stroke-width="18" stroke-linejoin="round"/>'
    out += f'<rect x="-40" y="-120" width="80" height="120" rx="36" fill="{door}"/>'
    out += '<circle cx="24" cy="-58" r="6" fill="#f7d67d"/>'
    for wx in (-100, 60):
        if lit and window_glow:
            out += glow(wx + 20, -150, 120, window_glow)
        out += f'<rect x="{wx}" y="-180" width="42" height="56" rx="10" fill="{win}"/>'
        out += f'<path d="M {wx + 21} -180 L {wx + 21} -124 M {wx} -152 L {wx + 42} -152" stroke="{wall}" stroke-width="5"/>'
    return out


def water(y: float, color: str, highlight: str) -> str:
    out = f'<rect x="0" y="{y}" width="{W}" height="{H - y}" fill="{color}"/>'
    rnd = random.Random(7)
    for _ in range(26):
        x = rnd.uniform(0, W)
        yy = rnd.uniform(y + 20, H - 20)
        w = rnd.uniform(60, 180)
        out += (f'<path d="M {x - w / 2:.0f} {yy:.0f} Q {x:.0f} {yy - 8:.0f} {x + w / 2:.0f} {yy:.0f}" '
                f'fill="none" stroke="{highlight}" stroke-width="4" stroke-linecap="round" opacity="0.35"/>')
    return out


def bed(quilt: str = "#9fb6ea", quilt_dot: str = "#fdf6e3") -> str:
    """ベッド（中心 (0,0) が まくらの あたり）。ポポの あたまは別途重ねる。"""
    wood = "#b98a6e"
    out = f'<rect x="-330" y="-190" width="90" height="360" rx="40" fill="{wood}"/>'
    out += f'<rect x="-300" y="60" width="760" height="110" rx="20" fill="#a67a60"/>'
    out += '<ellipse cx="-150" cy="10" rx="130" ry="62" fill="#fffaf2"/>'
    return out


def quilt(color: str = "#9fb6ea", dot: str = "#fdf6e3") -> str:
    out = (f'<path d="M -250 40 Q -150 0 -40 30 Q 200 10 440 30 L 460 130 Q 100 160 -260 130 Z" '
           f'fill="{color}"/>')
    rnd = random.Random(3)
    for _ in range(18):
        x, y = rnd.uniform(-220, 420), rnd.uniform(55, 120)
        out += g(star_shape(9, dot), x, y, rot=rnd.uniform(-30, 30), opacity=0.8)
    out += (f'<path d="M -250 40 Q -150 0 -40 30 Q 200 10 440 30" fill="none" stroke="#fdf6e3" '
            'stroke-width="14" stroke-linecap="round" opacity="0.8"/>')
    return out


def window_frame(x: float, y: float, w: float, h: float, inner: str, frame: str = "#c9a88c") -> str:
    """窓。inner には窓の中に描く SVG（クリップされる）を渡す。"""
    cid = f"win{int(x)}{int(y)}"
    out = (f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{min(w, h) * 0.5}"/></clipPath>')
    out += f'<g clip-path="url(#{cid})">{inner}</g>'
    out += (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{min(w, h) * 0.5}" fill="none" '
            f'stroke="{frame}" stroke-width="22"/>')
    out += (f'<path d="M {x + w / 2} {y + 10} L {x + w / 2} {y + h - 10} M {x + 10} {y + h * 0.55} '
            f'L {x + w - 10} {y + h * 0.55}" stroke="{frame}" stroke-width="14"/>')
    return out


def lamp(on: bool = True, glow_id: str | None = None) -> str:
    out = ""
    if on and glow_id:
        out += glow(0, -120, 200, glow_id)
    out += '<rect x="-60" y="-10" width="120" height="120" rx="16" fill="#c49c80"/>'
    out += '<rect x="-8" y="-100" width="16" height="92" fill="#e8d5c4"/>'
    shade = "#ffd98a" if on else "#bda6b4"
    out += f'<path d="M -60 -100 L -40 -170 L 40 -170 L 60 -100 Q 0 -90 -60 -100 Z" fill="{shade}"/>'
    return out
