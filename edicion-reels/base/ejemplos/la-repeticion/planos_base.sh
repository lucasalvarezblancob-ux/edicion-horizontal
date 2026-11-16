#!/usr/bin/env bash
# Plano base N (SDR bt709, 2160x3840, 30 fps, duración del plano de la ref + 0,1 s) desde seleccion.json.
# HDR: avconvert (tone mapping de Apple) con --start/--duration + hdr-pantalla.cube, igual que herramientas/proxy.sh.
# Uso: planos_base.sh N   (desde edits/)
set -euo pipefail
N="$1"; DIR=estudio/src/videos/la-repeticion; OUT=estudio/public/la-repeticion/base/$(printf %02d $N).mp4
read CLIP IN DUR < <(python3 -I -c "
import json;d=json.load(open('$DIR/seleccion.json'))[$N-1];print(d['clip'],d['in'],round(d['dur']+0.1,3))")
LUT="$PWD/herramientas/hdr-pantalla.cube"
TR=$(ffprobe -v error -select_streams v:0 -show_entries stream=color_transfer -of default=nw=1:nk=1 "$CLIP" | head -1 | tr -d ', ')
TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
if [[ "$TR" == "arib-std-b67" || "$TR" == "smpte2084" ]]; then
  avconvert -s "$CLIP" -p PresetHighestQuality -o "$TMP/sdr.mov" --start "$IN" --duration "$(echo "$DUR+0.5"|bc)" --replace >/dev/null
  ffmpeg -v error -y -i "$TMP/sdr.mov" -t "$DUR" -vf "scale=2160:3840:in_color_matrix=bt709:in_range=tv,format=gbrp,lut3d=${LUT}:interp=tetrahedral,scale=out_color_matrix=bt709:out_range=tv,format=yuv420p,fps=30,setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv" \
    -an -c:v libx264 -crf 14 -g 10 -color_primaries bt709 -color_trc bt709 -colorspace bt709 "$OUT"
else
  ffmpeg -v error -y -ss "$IN" -i "$CLIP" -t "$DUR" -vf "scale=2160:3840,fps=30,format=yuv420p,setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv" \
    -an -c:v libx264 -crf 14 -g 10 -color_primaries bt709 -color_trc bt709 -colorspace bt709 "$OUT"
fi
echo "$N $TR $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT")"
