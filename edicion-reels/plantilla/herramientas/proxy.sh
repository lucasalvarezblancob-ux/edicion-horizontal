#!/usr/bin/env bash
# Proxy 1440×2560 30 fps SDR con los COLORES DEL BRUTO tal como se ven en pantalla (iPhone / QuickTime).
# Los brutos del iPhone vienen en HDR (HLG, BT.2020, 10 bits). Se pasan a SDR con:
#   · Mac: el conversor de Apple (avconvert, mismo tone mapping que Fotos/QuickTime) + herramientas/hdr-pantalla.cube.
#   · Windows/Linux (no hay avconvert): ffmpeg + libplacebo (GPU, Vulkan) — el mismo motor de mpv. Validado 2026-11-11
#     (lagarto-caiman-nido): bruto vs proxy capturados en mpv → 2,7 niveles de media. ⚠️ NO uses zscale+tonemap
#     (mobius/hable/clip): mobius salió ~20 niveles más claro y más cálido que el bruto ("mucho más brillante").
#     hdr-pantalla.cube NO se aplica aquí: está medida contra la salida de avconvert.
# NO usar el truco antiguo de `setparams=…bt709` sin convertir: deja la imagen lavada, menos saturada y con la piel quemada.
# Uso: herramientas/proxy.sh BRUTO.MOV SALIDA.mp4 [ANCHO=1440]
# Salida 1440×2560 por defecto (los zooms/punch-in del montaje no pierden nitidez); en Remotion el <Video> va a 100%×100%.
# CORRECCIÓN HDR→PANTALLA (2026-11-01, solo Mac): la conversión SDR de Apple (avconvert) sale ~16 niveles más clara y plana que como
# QuickTime/iPhone muestran el bruto HDR. herramientas/hdr-pantalla.cube (medida comparando capturas de QuickTime bruto vs proxy
# en 4 clips y validada en un 5.º: dif. media 16 → <4 niveles) devuelve el contraste y los negros del bruto. Solo para brutos HDR.
# Comprobación de color: en QuickTime contra el bruto (Mac) o con herramientas/comparar_color.sh (mpv, Windows/Linux);
# ffmpeg suelto no aplica la gestión de color de un reproductor y engaña (ver preferencias → COLOR).
set -euo pipefail
IN="$1"; OUT="$2"; ANCHO="${3:-1440}"; ALTO=$(( ANCHO * 16 / 9 ))
LUT="$(cd "$(dirname "$0")" && pwd)/hdr-pantalla.cube"
VF="scale=${ANCHO}:${ALTO},fps=30,format=yuv420p"
PRE=()
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
# ojo: con csv=p=0 ffprobe 9 devuelve "arib-std-b67," (coma final) y la comparación fallaba → proxy en HLG sin convertir (2026-11-01)
TR=$(ffprobe -v error -select_streams v:0 -show_entries stream=color_transfer -of default=nw=1:nk=1 "$IN" | head -1 | tr -d ', \r')
SRC="$IN"
if [[ "$TR" == "arib-std-b67" || "$TR" == "smpte2084" ]]; then
  if command -v avconvert >/dev/null; then
    avconvert -s "$IN" -p PresetHighestQuality -o "$TMP/sdr.mov" --replace >/dev/null
    SRC="$TMP/sdr.mov"
    VF="scale=${ANCHO}:${ALTO}:in_color_matrix=bt709:in_range=tv,format=gbrp,lut3d=${LUT}:interp=tetrahedral,scale=out_color_matrix=bt709:out_range=tv,format=yuv420p,fps=30,setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv"
  else
    if ! ffmpeg -hide_banner -filters 2>/dev/null | grep -q libplacebo; then
      echo "ERROR: bruto HDR sin avconvert y este ffmpeg no tiene libplacebo. Instala un ffmpeg 'full' (Windows: winget install Gyan.FFmpeg)." >&2; exit 1
    fi
    PRE=(-init_hw_device vulkan)
    VF="libplacebo=w=${ANCHO}:h=${ALTO}:colorspace=bt709:color_primaries=bt709:color_trc=bt709:range=tv:format=yuv420p,fps=30"
  fi
fi
ffmpeg -v error -y "${PRE[@]}" -i "$SRC" -vf "$VF" -c:v libx264 -crf 14 -g 15 \
  -color_primaries bt709 -color_trc bt709 -colorspace bt709 -c:a aac -b:a 192k "$OUT"
# comprobación: el proxy tiene que salir en SDR bt709 (si sale HLG, Chrome/Remotion lo oscurece)
TR_OUT=$(ffprobe -v error -select_streams v:0 -show_entries stream=color_transfer -of default=nw=1:nk=1 "$OUT" | head -1 | tr -d ', \r')
if [[ "$TR_OUT" != "bt709" ]]; then echo "ERROR: el proxy ha salido con color_transfer=$TR_OUT (esperado bt709)" >&2; exit 1; fi
echo "$OUT ($TR → $TR_OUT)"
