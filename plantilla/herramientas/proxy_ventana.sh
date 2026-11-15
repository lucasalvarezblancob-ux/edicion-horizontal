#!/usr/bin/env bash
# Proxy SDR de una VENTANA de un bruto HDR largo: misma receta que herramientas/proxy.sh, pero solo de INI a INI+DUR.
# Para brutos 4K HDR largos (convertir el bruto entero tarda ~5 s por segundo de vídeo). Ojo: el proxy empieza en 0, así
# que los tiempos del EDL/plan que apunten a él van desplazados INI segundos; lo cómodo es convertir el bruto entero y
# dejar esto para pruebas o para planos de recurso sueltos.
# Uso: herramientas/proxy_ventana.sh BRUTO INI_S DUR_S SALIDA.mp4 [ALTO]
set -euo pipefail
IN="$1"; INI="$2"; DUR="$3"; OUT="$4"; ALTO="${5:-}"
AN="iw"; [ -n "$ALTO" ] && AN="trunc(iw*${ALTO}/ih/2)*2"     # ancho que conserva la proporción
[ -f "$OUT" ] && { echo "$OUT ya existe (bórralo si es de un intento anterior)"; exit 0; }
DIR="$(cd "$(dirname "$0")" && pwd)"; LUT="$DIR/hdr-pantalla.cube"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
TR=$(ffprobe -v error -select_streams v:0 -show_entries stream=color_transfer -of default=nw=1:nk=1 "$IN" | head -1 | tr -d ', \r')
COD=(-c:v libx264 -preset fast -crf 14 -g 25 -color_primaries bt709 -color_trc bt709 -colorspace bt709 -color_range tv -c:a aac -b:a 256k)
if [[ "$TR" == "arib-std-b67" || "$TR" == "smpte2084" ]] && command -v avconvert >/dev/null 2>&1; then
  avconvert -s "$IN" -p PresetHighestQuality -o "$TMP/sdr.mov" --start "$INI" --duration "$DUR" --replace >/dev/null
  VF="scale=${AN}:${ALTO:-ih}:in_color_matrix=bt709:in_range=tv,format=gbrp,lut3d=${LUT}:interp=tetrahedral,scale=out_color_matrix=bt709:out_range=tv,format=yuv420p,setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv"
  ffmpeg -nostdin -v error -y -i "$TMP/sdr.mov" -vf "$VF" "${COD[@]}" "$TMP/o.mp4"
elif [[ "$TR" == "arib-std-b67" || "$TR" == "smpte2084" ]]; then
  ffmpeg -nostdin -v error -y -init_hw_device vulkan -ss "$INI" -t "$DUR" -i "$IN" -vf "libplacebo=w=${AN}:h=${ALTO:-ih}:colorspace=bt709:color_primaries=bt709:color_trc=bt709:range=tv:format=yuv420p" "${COD[@]}" "$TMP/o.mp4"
else
  ffmpeg -nostdin -v error -y -ss "$INI" -t "$DUR" -i "$IN" -vf "scale=${AN}:${ALTO:-ih},format=yuv420p,setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv" "${COD[@]}" "$TMP/o.mp4"
fi
mv "$TMP/o.mp4" "$OUT"; echo "$OUT ($TR, desde $INI s, $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT" | tr -d '\r') s)"
