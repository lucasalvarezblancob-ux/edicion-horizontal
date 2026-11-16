#!/bin/bash
# proxy 4K de una VENTANA del bruto: misma receta que herramientas/proxy.sh (avconvert + hdr-pantalla.cube), con --start/--duration
# uso: herramientas/proxy_ventana.sh N INI DUR SLUG   (N = número del IMG_N.MOV de bruto/; salida en estudio/public/SLUG/N.mp4)
set -euo pipefail
cd "$(dirname "$0")/.."
IN=bruto/IMG_$1.MOV; SLUG=${4:?falta SLUG}; mkdir -p estudio/public/$SLUG; OUT=estudio/public/$SLUG/$1.mp4; INI=$2; DUR=$3
[ -f "$OUT" ] && exit 0
LUT=$PWD/herramientas/hdr-pantalla.cube
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
TR=$(ffprobe -v error -select_streams v:0 -show_entries stream=color_transfer -of default=nw=1:nk=1 "$IN" | head -1 | tr -d ', ')
if [[ ( "$TR" == "arib-std-b67" || "$TR" == "smpte2084" ) ]] && ! command -v avconvert >/dev/null; then
  # Windows/Linux: libplacebo (mismo motor que mpv), sin hdr-pantalla.cube (esa se midió contra avconvert). Ver proxy.sh.
  ffmpeg -v error -y -init_hw_device vulkan -ss $INI -t $DUR -i "$IN" -vf "libplacebo=w=2160:h=3840:colorspace=bt709:color_primaries=bt709:color_trc=bt709:range=tv:format=yuv420p,fps=30" -c:v libx264 -crf 14 -g 15 -color_primaries bt709 -color_trc bt709 -colorspace bt709 -c:a aac -b:a 192k "$TMP/o.mp4"
elif [[ "$TR" == "arib-std-b67" || "$TR" == "smpte2084" ]]; then
  avconvert -s "$IN" -p PresetHighestQuality -o "$TMP/sdr.mov" --start $INI --duration $DUR --replace >/dev/null
  VF="scale=2160:3840:in_color_matrix=bt709:in_range=tv,format=gbrp,lut3d=${LUT}:interp=tetrahedral,scale=out_color_matrix=bt709:out_range=tv,format=yuv420p,fps=30,setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv"
  ffmpeg -v error -y -i "$TMP/sdr.mov" -vf "$VF" -c:v libx264 -crf 14 -g 15 -color_primaries bt709 -color_trc bt709 -colorspace bt709 -c:a aac -b:a 192k "$TMP/o.mp4"
else
  ffmpeg -v error -y -ss $INI -t $DUR -i "$IN" -vf "scale=2160:3840,fps=30,format=yuv420p" -c:v libx264 -crf 14 -g 15 -color_primaries bt709 -color_trc bt709 -colorspace bt709 -c:a aac -b:a 192k "$TMP/o.mp4"
fi
mv "$TMP/o.mp4" "$OUT"; echo "$OUT $TR $(ffprobe -v error -show_entries format=duration -of csv=p=0 $OUT)"
