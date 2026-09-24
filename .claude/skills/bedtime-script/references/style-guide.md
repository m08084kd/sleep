# スライド画像プロンプトのスタイルガイド

## 基本方針
- 画面は 16:9。**文字は絵に入れない**（タイトルや字幕は Canva で入れる）。
- やさしいパステル調の絵本風。コントラスト低め、ギラギラした光やネオン色は使わない。
- 物語が進むほど、空や部屋の色を暗く（夕方のピンク・ラベンダー → 紺 → 深い藍色）。
- 各場面に **英語版（精度重視・詳しめ）** と **日本語版（Canva のマジック生成用・短め）** を書く。
- 英語版は「場面の説明」＋ 共通スタイル（毎回末尾に付ける前提なので本文には重ねて書かない）。
- キャラクターは、キャラ設定で決めた **同じ言葉** で毎回説明する（見た目のぶれを防ぐ）。
- パーツ方式のために、主人公の **ポーズ集（無地背景）** を 4〜6 個つくる。背景プロンプトは主人公を消しても成り立つように書く。

## 共通スタイル（そのまま使う）

英語
```
soft pastel children's picture book illustration, cute kawaii style, gentle watercolor and colored pencil texture, rounded simple shapes, calm and cozy bedtime atmosphere, muted lavender, navy blue and cream color palette, soft warm glow, low contrast, no text, no letters, 16:9
```

日本語
```
やさしいパステル調の絵本イラスト、かわいい、水彩と色えんぴつのタッチ、まるいシンプルな形、しずかで あたたかい夜の雰囲気、ラベンダーと紺とクリーム色、やわらかい光、文字なし
```

ネガティブ
```
text, letters, watermark, scary, dark shadows, sharp edges, high contrast, neon, oversaturated colors, realistic, photo, 3d render, extra limbs, open mouth teeth
```

## 色の進み方（場面の位置ごと）
| 位置 | 空・部屋の色（英語で書くとき） |
|---|---|
| はじめ（夕方・おうち） | sky fading from deep indigo to soft pink, peach and dusty pink walls |
| なかほど（夜のおさんぽ） | soft indigo and violet sky, deep navy night sky with many small stars |
| 後半（深い夜） | dark indigo sky, dim and calm colors |
| おふとん | cozy dim bedroom, muted lavender-blue walls, very soft dim lamp glow |
| さいご | very calm deep night sky, dark navy, minimal |

## 主人公キャラの作り方
新しいキャラを作るときは、次の要素を英語 1 文で決めて、以後すべての場面で同じ文を使う。
- 動物の種類・大きさ・体型（small round chubby …）
- 毛の色・おなかや口もとの色
- 顔（rosy pink cheeks, gentle sleepy smile など）
- 目印の小物を 1 つ（ナイトキャップ、スカーフ、パジャマなど。色も固定）

## 既存シリーズのキャラクター

### くまの ポポ
```
Popo, a small round chubby teddy bear cub, light caramel-brown fur, cream colored belly and muzzle, small round ears with pink inside, tiny black button nose, rosy pink cheeks, gentle sleepy smile, wearing a soft periwinkle-blue nightcap with a white fluffy band, a white pompom and tiny yellow stars
```
日本語：小さくてまるい子ぐま「ポポ」、キャラメル色の毛、おなかと口もとはクリーム色、ピンクのほっぺ、白いふちと白いぽんぽんがついた水色のナイトキャップ（小さな黄色い星もよう）

### おつきさまの ふね
```
a small boat shaped like a crescent moon, pale butter-yellow and softly glowing, with a gentle sleeping face on its side (closed curved eyes, rosy cheeks, tiny smile), a small wooden mast with a pink pennant flag and a little star on top
```

### おつきさま（まんまる）
```
a cute full moon with a gentle smiling face, closed curved eyes, rosy cheeks, pale cream-yellow with faint soft craters, soft halo glow
```

## よいプロンプトの例（場面：ほしの いけ）
英語
```
a calm quiet pond at night reflecting the starry sky, small glowing stars floating gently on the dark blue water surface, soft ripples, Popo the teddy bear cub sitting with sleepy half-closed eyes in a softly glowing crescent moon boat in the center of the pond, deep navy sky full of tiny stars, very peaceful and still
```
日本語
```
夜のしずかな池に星空がうつっている、紺色の水面に小さな光る星が浮かぶ、やさしい波もよう、池のまんなかで光る三日月のふねにのって ねむそうに目をはんぶんとじた子ぐま、小さな星がいっぱいの紺色の空、とてもしずか
```
