#!/usr/bin/env python3
"""寝かしつけ台本（canva/<slug>.md）のナレーションを検査する。

`> ` で始まる引用行をナレーションとみなし、次を調べる。
  エラー: 既知のオノマトペ、こわい言葉、漢字、場面に画像プロンプトがない
  警告  : オノマトペらしい形（くり返し・「〜っと」・のばし棒）、長すぎる文、間の書き忘れ

使いかた: python3 check_script.py canva/<slug>.md
終了コード: エラーがあれば 1
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# 使ってはいけない擬音語・擬態語（ひらがな・カタカナの両方を検査する）
ONOMATOPOEIA = [
    "すやすや", "すうすう", "くーくー", "ぐうぐう", "ぐっすり", "うとうと", "こっくり", "むにゃむにゃ",
    "ぽかぽか", "ぬくぬく", "ほかほか", "ほっこり", "ほんのり", "ぽわっ", "ぽわぽわ", "ほわほわ",
    "ふわふわ", "ふわっ", "ふわり", "ふかふか", "もこもこ", "もふもふ", "ふんわり",
    "ゆらゆら", "ゆらり", "ゆら、", "ぷかぷか", "そよそよ", "さらさら", "ころころ", "ごろごろ", "ごろん",
    "きらきら", "きらり", "ぴかぴか", "ちかちか", "しーん", "しいん", "ひっそり",
    "にっこり", "にこにこ", "にこっ", "くすくす", "とろとろ", "とろん", "とんとん", "ぎゅっ",
    "すーっ", "ふーっ", "すうっ", "ふうっ", "すー", "ふー", "はー", "ふわぁ", "ふぁ〜",
    "ざあざあ", "ぽつぽつ", "ちゅんちゅん", "ほーほー", "ぴょんぴょん", "ぱちぱち", "zzz",
]
# 「〜っと」で終わるが オノマトペではない ふつうの言葉
TTO_OK = {"もっと", "ずっと", "きっと", "やっと", "ちょっと", "そっと", "いっと", "ほっと"}
# くり返しの形だが オノマトペではない ふつうの言葉
REPEAT_OK = {"そろそろ", "だんだん", "ときどき", "いろいろ", "まだまだ", "ますます", "みるみる", "ひとびと", "しばしば"}
SCARY = ["おばけ", "かいぶつ", "こわい", "おおかみ", "わるもの", "まいご", "なきだ", "どろぼう", "かみなり", "けんか", "たいへん"]

KANA = str.maketrans({chr(c): chr(c - 0x60) for c in range(0x30A1, 0x30F7)})  # カタカナ→ひらがな


def check(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    warns: list[str] = []
    narration = 0

    for no, raw in enumerate(text.splitlines(), 1):
        if not raw.startswith("> "):
            continue
        line = re.sub(r"（間\s*[\d.]+\s*秒）", "", raw[2:]).strip()
        if not line or "**" in line:  # 注意書きの引用は対象外
            continue
        narration += 1
        hira = line.translate(KANA)
        where = f"{path}:{no}: {line}"

        for w in ONOMATOPOEIA:
            if w in hira:
                errors.append(f"オノマトペ「{w}」 → {where}")
        for w in SCARY:
            if w in hira:
                errors.append(f"こわい/ドキドキする言葉「{w}」 → {where}")
        if re.search(r"[一-鿿]", line):
            errors.append(f"漢字が入っています（ひらがなにする） → {where}")

        for m in re.finditer(r"([ぁ-ゖ]{2})[、 ]?\1", hira):
            if m.group(0) in REPEAT_OK:
                continue
            warns.append(f"くり返し語「{m.group(0)}」はオノマトペでは？ → {where}")
        for m in re.finditer(r"([ぁ-ゖ]{1,2})[ーぁぃぅぇぉ]*っと", hira):
            if m.group(0) not in TTO_OK:
                warns.append(f"「{m.group(0)}」はオノマトペでは？ → {where}")
        if re.search(r"[ぁ-ゖ][ー〜]", line):  # カタカナ語（オレンジーなど）ののばし棒は対象外
            warns.append(f"のばし棒（声や音のまね？） → {where}")
        if len(line.replace(" ", "")) > 32:
            warns.append(f"文が長め（字幕 2 行以内に） → {where}")
        if "（間" not in raw:
            warns.append(f"（間 ○秒）がありません → {where}")

    # 場面ごとに画像プロンプトがあるか
    scenes = re.split(r"^### 場面", text, flags=re.M)[1:]
    for sc in scenes:
        name = sc.splitlines()[0].strip()
        if "**画像" not in sc:
            errors.append(f"場面{name} に画像プロンプトがありません")
        elif "英語" not in sc or "日本語" not in sc:
            warns.append(f"場面{name} に英語版・日本語版の両方のプロンプトがありません")
    if narration == 0:
        errors.append("ナレーション（`> ` で始まる行）が見つかりません")

    for w in warns:
        print("警告:", w)
    for e in errors:
        print("エラー:", e)
    print(f"— ナレーション {narration} 行 / 場面 {len(scenes)} / エラー {len(errors)} / 警告 {len(warns)}")
    return 1 if errors else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(check(Path(sys.argv[1])))
