#!/usr/bin/env bash
# フォントと音声データをダウンロードして、Python ライブラリを入れます。
set -euo pipefail
cd "$(dirname "$0")/.."

pip install -r requirements.txt

mkdir -p assets/fonts assets/voices
if [ ! -f assets/fonts/ZenMaruGothic-Medium.ttf ]; then
  echo "▶ フォント Zen Maru Gothic（SIL OFL 1.1）をダウンロード"
  curl -fsSL -o assets/fonts/ZenMaruGothic-Medium.ttf \
    https://raw.githubusercontent.com/google/fonts/main/ofl/zenmarugothic/ZenMaruGothic-Medium.ttf
fi
if [ ! -f assets/voices/tohoku-f01-neutral.htsvoice ]; then
  echo "▶ 音声 tohoku-f01（CC BY 4.0）をダウンロード"
  base=https://raw.githubusercontent.com/icn-lab/htsvoice-tohoku-f01/master
  curl -fsSL -o assets/voices/tohoku-f01-neutral.htsvoice "$base/tohoku-f01-neutral.htsvoice"
  curl -fsSL -o assets/voices/COPYRIGHT.txt "$base/COPYRIGHT.txt"
fi

# cairosvg がフォントを見つけられるように登録する
case "$(uname)" in
  Darwin) mkdir -p ~/Library/Fonts && cp assets/fonts/*.ttf ~/Library/Fonts/ ;;
  *)      mkdir -p ~/.fonts && cp assets/fonts/*.ttf ~/.fonts/ && (fc-cache -f >/dev/null 2>&1 || true) ;;
esac
echo "✓ 準備できました"
