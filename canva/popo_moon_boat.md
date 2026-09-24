# くまの ポポと おつきさまの ふね
## 台本 ＋ 画像用プロンプト（Canva で動画を作る用）

- 対象：3〜6さい／ねむる まえの よみきかせ
- 長さ：朗読 約 5〜6 分（ナレーションはオノマトペなし） ＋ おわりの星空 30〜60 秒
- 画面：16:9（1920×1080）、全 10 場面

---

## 0. 使いかたの流れ

1. **「1. 共通スタイル」と「2. キャラクター」** のプロンプトで、まずポポとおつきさまのふねを作り、気に入った絵を決める
2. **「4. 場面ごとの台本と画像プロンプト」** で各場面の絵を作る
3. Canva で 1 場面 = 1 ページにして、台本の文を字幕として置き、ナレーション音声を入れる
4. 各ページの長さは「目安の長さ」を参考に、ナレーションに合わせて調整する

### 絵のタッチをそろえるコツ（重要）

AI 画像生成は、同じプロンプトでも毎回キャラの見た目が変わりがちです。おすすめは次の 2 つのどちらか。

- **A. パーツ方式（Canva でいちばん確実）**
  背景は「キャラなし」で作り、ポポは「3. ポポのポーズ集」で別に作って **背景除去** → 背景の上に配置する。
  同じポポを全場面で使いまわせるので、キャラがぶれません。
- **B. 参照画像方式（ChatGPT・Midjourney などを使う場合）**
  気に入ったポポの画像を参照画像として添付し、「この くまと同じキャラクターで」と指示する。
  （Midjourney なら `--cref 画像URL` が使えます）

各プロンプトは **英語版（精度が高い）** と **日本語版（Canva のマジック生成にそのまま使える短め）** を用意しました。
Canva で文字数が多すぎると言われたら、日本語版を使ってください。

---

## 1. 共通スタイル（すべてのプロンプトの最後に付ける）

**英語**
```
soft pastel children's picture book illustration, cute kawaii style, gentle watercolor and colored pencil texture, rounded simple shapes, calm and cozy bedtime atmosphere, muted lavender, navy blue and cream color palette, soft warm glow, low contrast, no text, no letters, 16:9
```

**日本語**
```
やさしいパステル調の絵本イラスト、かわいい、水彩と色えんぴつのタッチ、まるいシンプルな形、しずかで あたたかい夜の雰囲気、ラベンダーと紺とクリーム色、やわらかい光、文字なし
```

**入れたくないもの（ネガティブプロンプト欄がある場合）**
```
text, letters, watermark, scary, dark shadows, sharp edges, high contrast, neon, oversaturated colors, realistic, photo, 3d render, extra limbs, open mouth teeth
```

> 眠りをさそう動画なので、**明るすぎる色・強いコントラスト・ギラギラした光は避ける**のがポイントです。後半の場面ほど暗めの色にしています。

---

## 2. キャラクター設定

### くまの ポポ（主人公）

**英語**
```
character design of Popo, a small round chubby teddy bear cub, light caramel-brown fur, cream colored belly and muzzle, small round ears with pink inside, tiny black button nose, rosy pink cheeks, gentle sleepy smile, wearing a soft periwinkle-blue nightcap with a white fluffy band, a white pompom and tiny yellow stars, simple and cute, full body, plain cream background
```

**日本語**
```
小さくてまるい子ぐまのキャラクター「ポポ」、キャラメル色の毛、おなかと口もとはクリーム色、ピンクのほっぺ、やさしい笑顔、白いふちと白いぽんぽんがついた水色のナイトキャップ（小さな黄色い星もよう）、全身、無地のクリーム色の背景
```

### おつきさまの ふね

**英語**
```
a small boat shaped like a crescent moon, pale butter-yellow and softly glowing, with a gentle sleeping face on its side (closed curved eyes, rosy cheeks, tiny smile), a small wooden mast with a pink pennant flag and a little star on top, cute, plain navy background
```

**日本語**
```
三日月の形をした小さなふね、うすい黄色でやさしく光っている、ふねの横にねむっている顔（とじた目、ピンクのほっぺ、小さな笑顔）、木のほばしらにピンクの小さな旗と星、かわいい、無地の紺色の背景
```

### おつきさま（まんまる）

**英語**
```
a cute full moon with a gentle smiling face, closed curved eyes, rosy cheeks, pale cream-yellow with faint soft craters, soft halo glow
```

**日本語**
```
やさしい笑顔のまんまるのおつきさま、とじた目、ピンクのほっぺ、うすいクリーム色、ふんわり光る
```

---

## 3. ポポのポーズ集（パーツ方式で使う）

背景除去しやすいよう、すべて **無地の背景** で作ります。先頭に「2. ポポ」の英語プロンプトの見た目説明を付けると、より似せやすくなります。

| No. | 使う場面 | 英語 | 日本語 |
|---|---|---|---|
| P1 | 1, 3 | `Popo the teddy bear cub sitting and smiling, facing forward, plain background` | `すわってにっこりしているポポ、正面、無地の背景` |
| P2 | 2 | `Popo the teddy bear cub sitting with eyes closed, giving a big sleepy yawn, one paw near mouth, plain background` | `目をとじて大きなあくびをしているポポ、口もとに手、無地の背景` |
| P3 | 4, 5 | `Popo the teddy bear cub sitting happily inside a crescent moon boat, plain navy background` | `三日月のふねにすわっているポポ、うれしそう、無地の紺色の背景` |
| P4 | 6, 7, 8 | `Popo the teddy bear cub sitting in a crescent moon boat with half-closed sleepy eyes, relaxed, plain navy background` | `三日月のふねで、ねむそうに目をはんぶんとじているポポ、無地の紺色の背景` |
| P5 | 9 | `Popo the teddy bear cub sleeping peacefully in a cozy bed under a blue quilt with little star pattern, eyes closed, head on a white pillow, plain background` | `星もようの水色のおふとんで、白いまくらにあたまをのせて すやすや ねむるポポ、無地の背景` |

---

## 4. 場面ごとの台本と画像プロンプト

表記のきまり
- 台本は **ひらがな中心・分かち書き**（読み聞かせる大人も読みやすく、字幕にもそのまま使えます）
- ナレーションでは **擬音語・擬態語（オノマトペ）を使いません**（「すー」「ふー」「ぽかぽか」「ゆらゆら」などは、ふつうの言葉で言いかえています）
- `（間 ○秒）` は、その文のあとに空ける時間です。**後半ほど長く**しています
- 画像プロンプトの【背景のみ】はパーツ方式用（キャラなし）、【全部入り】は 1 枚で完結させたい場合用です

---

### 場面 1　タイトル　（目安 15 秒）

**台本**
> くまの ポポと、おつきさまの ふね。（間 3秒）

**Canva メモ**：タイトル文字を大きく入れる。丸ゴシック系フォント（例：「M PLUS Rounded」「Zen Maru Gothic」など）がおすすめ。

**画像【全部入り】英語**
```
twilight scene on a gentle lavender hill, a small cozy cottage with warm glowing windows on the left, a few soft rounded pine trees, a big smiling full moon in the upper right, the sky fading from deep indigo at the top to soft pink near the horizon, twinkling little stars, Popo the small teddy bear cub with a blue nightcap sitting on the hill looking up, empty space in the upper center for a title
```
**画像【全部入り】日本語**
```
夕ぐれのラベンダー色の丘、左に窓があたたかく光る小さなおうち、まるい木、右上に笑顔のまんまるのおつきさま、空は上が紺色で地平線がピンク、小さな星、丘にすわって空を見上げる水色のナイトキャップの子ぐま、中央上にタイトル用の余白
```
**画像【背景のみ】**：上から「Popo … looking up」「子ぐま」の部分を消して使う

---

### 場面 2　おおきな あくび　（目安 30 秒）

**台本**
> もりの おくの ちいさな おうちに、くまの ポポが すんでいました。（間 1.8秒）
> おそらが、オレンジいろから、むらさきいろに かわるころ。（間 1.8秒）
> ポポは、おおきな あくびを しました。（間 2.2秒）
> きょうも いっぱい あそんだね。（間 1.8秒）
> そろそろ、ねむる じかんです。（間 2.5秒）

**画像【背景のみ】英語**
```
cozy warm bedroom interior at dusk, soft peach and dusty pink walls, a large round window showing a sunset sky fading from orange to purple with small fluffy clouds, a small bedside lamp with a warm glow, a soft round rug on a wooden floor, empty space in the center for a character
```
**画像【全部入り】英語**：上の文の最後を `Popo the teddy bear cub sitting on the rug with eyes closed, giving a big sleepy yawn` に変える

**日本語**
```
夕方のあたたかいお部屋、ピーチ色とうすいピンクのかべ、大きな丸い窓から見えるオレンジから紫にかわる夕焼け空と小さな雲、あたたかく光る小さなランプ、木の床にまるいラグ、ラグの上で目をとじて大きなあくびをする子ぐま
```

---

### 場面 3　おつきさまが むかえに くる　（目安 35 秒）

**台本**
> そのとき、まどの そとが、やさしく ひかりました。（間 1.8秒）
> おつきさまが、ちいさな ふねに なって、おりてきたのです。（間 1.8秒）
> 「ポポ、こんばんは。」（間 1.8秒）
> 「ねむる まえに、いっしょに よるの おさんぽを しようよ。」（間 1.8秒）
> ポポは、うれしそうに うなずいて、ふねに のりました。（間 2.5秒）

**読みかたメモ**：おつきさまのセリフは、ひそひそ声に近いくらい、やさしく。

**画像 英語**
```
early night scene outside a small cozy cottage with warm glowing windows, soft indigo and violet sky full of little twinkling stars, a glowing crescent moon boat with a sleeping face gently floating down from the sky, a trail of tiny sparkles behind it, soft rounded dark-blue pine trees, Popo the teddy bear cub standing near the cottage looking up happily
```
**日本語**
```
夜のはじまり、窓があたたかく光る小さなおうちの前、紺と紫の空に小さな星がいっぱい、ねむった顔の三日月のふねが光りながら空からゆっくりおりてくる、うしろに小さなきらきら、まるい紺色の木、おうちの前で空を見上げてにっこりする子ぐま
```

---

### 場面 4　くもの うみ　（目安 35 秒）

**台本**
> ふねは、かぜに のって、しずかに うかびました。（間 1.8秒）
> くもの うみを、ゆっくり ゆっくり すすみます。（間 1.8秒）
> ふねが、みぎへ、ひだりへ、やさしく ゆれています。（間 2秒）
> みぎへ、ひだりへ。（間 2.5秒）
> からだの ちからを ぬいて、ふねに ゆられて みようね。（間 3秒）

**Canva メモ**：この場面から、絵をゆっくり左右に動かす（アニメーション「パン」や、ゆっくりズーム）と、ゆられている感じが出ます。

**画像 英語**
```
Popo the teddy bear cub sitting in a glowing crescent moon boat, sailing slowly over a soft sea of fluffy lavender and pale lilac clouds, deep navy night sky with many small twinkling stars, gentle glow around the boat, dreamy and peaceful, wide view
```
**日本語**
```
光る三日月のふねにのった子ぐまが、ふわふわのラベンダー色の雲の海をゆっくり進む、紺色の夜空に小さな星がたくさん、ふねのまわりにやさしい光、夢のようにしずか、ひろい景色
```

---

### 場面 5　ひつじの おか　（目安 45 秒）

**台本**
> しばらく いくと、まっしろな ひつじの おかが みえてきました。（間 1.8秒）
> ひつじさんたちが、やわらかな くもの うえで、まるく なっています。（間 1.8秒）
> いっしょに かぞえて みようか。（間 1.8秒）
> ひつじさんが、ひとり。（間 2.2秒）
> ひつじさんが、ふたり。（間 2.2秒）
> ひつじさんが、さんにん。（間 2.4秒）
> ひつじさんが、よにん。（間 2.6秒）
> ひつじさんが、ごにん。（間 2.8秒）
> みんな、なかよく、おやすみなさい。（間 3秒）

**読みかたメモ**：数えるところは、1 回ごとに少しずつ声を小さく・ゆっくりにしていく。
**Canva メモ**：数えるのに合わせて、ひつじを 1 ぴきずつ「フェード」で出すと子どもが一緒に数えやすいです（ひつじをパーツで作る場合は下の「ひつじ単体」を使用）。

**画像 英語**
```
a soft rolling hill made of fluffy pale lavender clouds under a deep blue starry night sky, five round fluffy white sheep curled up and sleeping peacefully on the hill with closed eyes and rosy cheeks, small "zzz" feeling, a tiny glowing crescent moon boat with a teddy bear cub floating in the sky in the upper right
```
**日本語**
```
ふわふわのラベンダー色の雲でできたなだらかな丘、紺色の星空、まるくてふわふわの白いひつじが5ひき、目をとじてすやすやねむっている、ピンクのほっぺ、右上の空に子ぐまがのった小さな三日月のふね
```
**ひつじ単体（パーツ）**
```
英語: one round fluffy white sheep curled up and sleeping, closed eyes, rosy cheeks, soft grey-mauve face, plain background
日本語: まるくなってねむる ふわふわの白いひつじ1ぴき、とじた目、ピンクのほっぺ、無地の背景
```

---

### 場面 6　ほしの いけ（しんこきゅう）　（目安 55 秒）

**台本**
> つぎに ついたのは、ほしの いけ。（間 1.8秒）
> みずの なかで、ちいさな ほしが、ひかりながら ゆれています。（間 1.8秒）
> おつきさまが、しずかに いいました。（間 1.8秒）
> 「ポポ、ここで、ゆっくり いきを してみよう。」（間 1.8秒）
> はなから、ゆっくり、いきを すって。（間 2.5秒）
> くちから、ゆっくり、いきを はいて。（間 3秒）
> もういちど。ゆっくり すって。（間 2.5秒）
> ゆっくり、はいて。（間 3秒）
> からだが、あたたかく なってきたね。（間 3秒）

**読みかたメモ**：「すって」「はいて」のあとは、読む人も実際に息をすって・はきながら間をとる。子どもも自然にまねします。
**Canva メモ**：呼吸に合わせて、ふねの絵を少しだけ大きく→小さく（ゆっくりズームイン・アウト）すると、呼吸のガイドになります。

**画像 英語**
```
a calm quiet pond at night reflecting the starry sky, small glowing stars floating gently on the dark blue water surface, soft ripples, Popo the teddy bear cub sitting with sleepy half-closed eyes in a softly glowing crescent moon boat in the center of the pond, deep navy sky full of tiny stars, very peaceful and still
```
**日本語**
```
夜のしずかな池に星空がうつっている、紺色の水面に小さな光る星がぷかぷか浮かぶ、やさしい波もよう、池のまんなかで光る三日月のふねにのって ねむそうに目をはんぶんとじた子ぐま、小さな星がいっぱいの紺色の空、とてもしずか
```

---

### 場面 7　ねむりの もり　（目安 45 秒）

**台本**
> ふねは、ねむりの もりの うえを とおります。（間 1.8秒）
> もりの どうぶつたちも、もう、ねむっていました。（間 1.8秒）
> うさぎさんも、まるく なって、おやすみ。（間 2.4秒）
> りすさんも、やわらかい しっぽに くるまって、おやすみ。（間 2.4秒）
> ふくろうさんも、きょうは えだの うえで、おやすみ。（間 2.8秒）
> もりは、とても しずかです。（間 3秒）

**画像 英語**
```
a quiet sleepy forest at night, soft rounded dark teal trees, a small white bunny curled up sleeping on the grass, a little orange squirrel sleeping wrapped in its fluffy tail, a round lavender owl sleeping with closed eyes on a tree branch, all animals with closed eyes and rosy cheeks, deep navy sky with a few stars, a small glowing crescent moon boat with a teddy bear cub passing high in the sky
```
**日本語**
```
夜のしずかな森、まるい形の深い青緑の木、草の上でまるくなってねむる白いうさぎ、ふわふわのしっぽにくるまってねむるオレンジ色のりす、木のえだの上で目をとじてねむるラベンダー色のふくろう、みんな目をとじてピンクのほっぺ、紺色の空に少しの星、空の高いところを子ぐまがのった小さな三日月のふねが通る
```

---

### 場面 8　おうちへ かえろう　（目安 35 秒）

**台本**
> ポポの まぶたが、だんだん、おもたく なってきました。（間 1.8秒）
> 「そろそろ、おうちに かえろうね。」（間 1.8秒）
> おつきさまの ふねは、ほしの みちを とおって、（間 1.2秒）
> ゆっくり、ゆっくり、ポポの おうちへ もどります。（間 3秒）

**画像 英語**
```
deep quiet night landscape, dark indigo sky full of small soft stars, a gentle curving path of tiny glowing stars leading down to a small cozy cottage with one warm glowing window far away on a dark hill, a small glowing crescent moon boat with a sleepy teddy bear cub following the star path, dim and calm colors
```
**日本語**
```
しずかな深い夜、こい藍色の空に小さな星がいっぱい、小さく光る星がならんだ道がカーブしながら、遠くの丘の上の窓が1つだけ光る小さなおうちへつづいている、ねむそうな子ぐまをのせた三日月のふねが星の道をすすむ、暗めでおだやかな色
```

---

### 場面 9　おふとんで おやすみ　（目安 45 秒）

**台本**
> ポポは、あたたかい おふとんに もぐりこみました。（間 1.8秒）
> てのさきも、あしのさきも、あたたかい。（間 2.5秒）
> おなかも、あたたかい。（間 2.5秒）
> おつきさまが、まどから やさしく いいました。（間 1.8秒）
> 「きょうも いちにち、よく がんばったね。」（間 2.4秒）
> 「おやすみ、ポポ。」（間 3.5秒）

**読みかたメモ**：「てのさきも、あしのさきも」で、聞いている子の手や足にも意識が向くように、ゆっくり区切って。

**画像 英語**
```
cozy dim bedroom at night, soft muted lavender-blue walls, Popo the teddy bear cub sleeping peacefully in a wooden bed under a blue quilt with little star pattern, eyes closed, head on a white pillow, wearing the blue nightcap, a round window showing the smiling full moon and stars, a small bedside lamp with a very soft dim glow, calm and warm
```
**日本語**
```
夜の少し暗いお部屋、落ちついたラベンダーブルーのかべ、木のベッドで星もようの水色のおふとんをかけて すやすやねむる子ぐま、白いまくら、水色のナイトキャップ、丸い窓から笑顔のまんまるのおつきさまと星、小さなランプがほんのり光る、しずかであたたかい
```

---

### 場面 10　おやすみなさい　（目安 20 秒 ＋ おわりの星空 30〜60 秒）

**台本**
> そして、これを きいている、あなたも。（間 2.5秒）
> きょうも いちにち、ありがとう。（間 3秒）
> おやすみなさい。（間 4秒）

**読みかたメモ**：いちばん小さく、いちばんゆっくり。最後の「おやすみなさい」は、ささやくように。
**Canva メモ**：読み終わったら、この絵のまま音楽だけを 30〜60 秒流し、最後の 10〜15 秒で画面を黒へフェードアウト（黒いページを最後に置いて「ディゾルブ」でつなぐ）。

**画像 英語**
```
very calm deep night sky, dark navy with many tiny soft stars, a gentle smiling full moon with closed eyes in the center with a soft halo, far below a tiny cottage with dark windows (everyone is asleep) on a dark rounded hill with small silhouette pine trees, very dim and peaceful, minimal
```
**日本語**
```
とてもしずかな深い夜空、こい紺色に小さな星がたくさん、まんなかに目をとじてほほえむまんまるのおつきさま、やさしい光の輪、下のほうに暗い丘と、窓の明かりが消えた小さなおうち（みんなねむっている）、小さな木のシルエット、とても暗くおだやか、シンプル
```

---

## 5. Canva で仕上げるときのおすすめ設定

| 項目 | おすすめ |
|---|---|
| ページの切りかえ | 「ディゾルブ」、1.5〜2.5 秒くらいの ゆっくりしたもの |
| 絵の動き | 「パン」や ゆっくりズーム程度。ぴょんぴょん動くアニメーションは使わない |
| 字幕 | 画面下に、半透明の紺色の帯＋クリーム色の丸ゴシック。1 行 20 文字くらいまで |
| BGM | オルゴールやピアノのゆっくりした曲を、声よりずっと小さい音量で（Canva の音楽素材の「子守唄」「lullaby」など） |
| 全体の明るさ | 後半ほど暗めに。最後は黒へフェードアウト |
| 最初と最後 | 最初は 2〜3 秒の静かな絵だけの時間、最後は 30〜60 秒の星空と音楽 |

## 6. ナレーションを録音するときのコツ

- **ふだんの半分くらいの速さ**で。「、」でひと呼吸、「。」でふた呼吸
- 声は**少し低め・小さめ**に。後半ほど、さらに小さく
- 台本の「（間 ○秒）」は、心の中でゆっくり数える
- 録音した音声は Canva に取り込み、各ページの長さを音声に合わせる

## 7. YouTube 投稿メモ

- アップロード時に **「子ども向け」** を選ぶ
- AI で作った画像を使う場合、各サービスの利用規約（商用利用・YouTube の収益化の可否）を確認しておく
- Canva の音楽素材を使う場合は、Canva のライセンスの範囲で使う
