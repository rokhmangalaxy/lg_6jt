#!/usr/bin/env bash
# ImageMagick; normalize generated symbols and add an exact, consistent nameplate.
set -euo pipefail
cd "$(dirname "$0")/.."
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
convert -size 3x1 xc:white -fill '#dc2626' -draw 'point 0,0' -fill '#173257' -draw 'point 1,0' "$tmp/palette.png"
for n in 06 07 08 09 10; do
  convert "03-konsep/tambahan/source-$n.png" -shave 3x3 -background white -alpha remove +dither -remap "$tmp/palette.png" -trim +repage -resize 920x500 "$tmp/symbol.png"
  convert -size 1200x800 xc:white "$tmp/symbol.png" -gravity north -geometry +0+76 -composite \
    -font DejaVu-Sans-Bold -fill '#173257' -pointsize 42 -gravity north \
    -annotate +0+660 'PT. MENARA CIPTA METALINDO' \
    +dither -remap "$tmp/palette.png" -strip PNG24:"html/assets/variasi-$n-native.png"
done
