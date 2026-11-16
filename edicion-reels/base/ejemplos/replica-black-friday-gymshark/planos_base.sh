#!/usr/bin/env bash
# Plano base N (SDR bt709, 2160x3840, 30 fps, duración del plano + 0,3 s) desde seleccion.json. Copia de la-repeticion.
# HDR: avconvert (tone mapping de Apple) + hdr-pantalla.cube, igual que herramientas/proxy.sh. SDR (Sony): solo escala.
# Uso: planos_base.sh N   (desde edits/)
set -euo pipefail
N="$1"; DIR=estudio/src/videos/replica-black-friday-gymshark; OUT=estudio/public/replica-black-friday-gymshark/planos/$(printf %02d $N).mp4
mkdir -p "$(dirname "$OUT")"
IFS=$'\t' read -r CLIP IN DUR < <(python3 -I -c "
import json;d=[x for x in json.load(open('$DIR/seleccion.json')) if x['n']==$N][0];print(d['clip'],d['in'],round((d['a']-d['de'])/30+0.3,3),sep='\t')")
LUT="$PWD/herramientas/hdr-pantalla.cube"
TR=$(ffprobe -v error -select_streams v:0 -show_entries stream=color_transfer -of default=nw=1:nk=1 "$CLIP" | head -1 | tr -d ', ')
TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
if [[ "$TR" == "arib-std-b67" || "$TR" == "smpte2084" ]]; then
  avconvert -s "$CLIP" -p PresetHighestQuality -o "$TMP/sdr.mov" --start "$IN" --duration "$(echo "$DUR+0.5"|bc)" --replace >/dev/null
  ffmpeg -v error -y -i "$TMP/sdr.mov" -t "$DUR" -vf "scale=2160:3840:in_color_matrix=bt709:in_range=tv,format=gbrp,lut3d=${LUT}:interp=tetrahedral,scale=out_color_matrix=bt709:out_range=tv,format=yuv420p,fps=30,setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv" \
    -an -c:v libx264 -crf 14 -g 10 -color_primaries bt709 -color_trc bt709 -colorspace bt709 "$OUT"
else
  ffmpeg -v error -y -ss "$IN" -i "$CLIP" -t "$DUR" -vf "scale=2160:3840:flags=lanczos,fps=30,format=yuv420p,setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv" \
    -an -c:v libx264 -crf 14 -g 10 -color_primaries bt709 -color_trc bt709 -colorspace bt709 "$OUT"
fi
echo "$N $TR $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT")"
