# このリポジトリについて

3〜6さい向けの寝かしつけ朗読 YouTube 動画を作るためのリポジトリです。
動画はユーザーが Canva で手作業で作ります。Claude の担当は **ナレーション台本** と **スライド画像の生成プロンプト** です。

## 動画づくりの依頼を受けたとき

新しい動画・おはなし・台本・ナレーション・スライドの絵（画像プロンプト）の作成を頼まれたら、
**必ず `bedtime-script` スキルを呼び出して**、その手順とルールに従ってください（ユーザーは `/bedtime-script テーマ` でも呼べます）。

- 成果物: `canva/<slug>.md`（完成例: `canva/popo_moon_boat.md`）
- ナレーションでは **擬音語・擬態語（オノマトペ）を使わない**（「すー」「ふー」「ぽかぽか」「ゆらゆら」など）
- 書いたら `python3 .claude/skills/bedtime-script/scripts/check_script.py canva/<slug>.md` でチェックする

## そのほか
- `bedtime/` と `stories/*.yaml` は、台本から動画を自動生成する Python ツール（任意）。使い方は README.md。
