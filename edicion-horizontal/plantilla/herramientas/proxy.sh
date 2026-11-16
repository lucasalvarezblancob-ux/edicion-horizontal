#!/usr/bin/env bash
# Copia SDR (bt709) de un bruto HDR con los COLORES DEL BRUTO tal como se ven en pantalla, a su misma resolución y fps.
# Cuándo hace falta: el montaje horizontal lee los brutos directamente con ffmpeg (paso4_render.py) y NO convierte HDR.
#   · Sony ZV-E10 II y cualquier bruto SDR: NO hace falta proxy; se monta desde el original.
#   · iPhone (HLG, BT.2020, 10 bits) u otro HDR: haz antes este proxy y úsalo como bruto (BRUTOS de proyecto.py apuntando
#     a la carpeta de los proxies, con el mismo nombre de clip).
# Conversión HDR → SDR:
#   · Mac: conversor de Apple (avconvert, el mismo tone mapping que Fotos/QuickTime) + herramientas/hdr-pantalla.cube
#     (corrección MEDIDA con un iPhone: avconvert solo sale ~16 niveles más claro y plano que el bruto en QuickTime).
#   · Windows/Linux: ffmpeg + libplacebo (GPU, Vulkan), el motor de mpv. Validado en reels el 2026-11-11: 2,7 niveles de
#     media frente al bruto. ⚠️ NO uses zscale+tonemap (mobius salió ~20 niveles más claro y más cálido).
# Uso: herramientas/proxy.sh BRUTO SALIDA.mp4 [ALTO]      (ALTO por defecto = el del bruto; nunca lo bajes para el vídeo final)
# Después, SIEMPRE: comprueba el color contra el bruto antes de montar (QuickTime en Mac; herramientas/comparar_color.sh
# con mpv en Windows/Linux). Con otro móvil o exteriores con sol fuerte la corrección puede no cuadrar: ver preferencias → COLOR.
set -euo pipefail
IN="$1"; OUT="$2"; ALTO="${3:-}"
AN="iw"; [ -n "$ALTO" ] && AN="trunc(iw*${ALTO}/ih/2)*2"     # ancho que conserva la proporción
LUT="$(cd "$(dirname "$0")" && pwd)/hdr-pantalla.cube"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
# ojo: con csv=p=0 ffprobe devuelve "arib-std-b67," (coma final) y la comparación fallaba; y en Windows llega con \r
TR=$(ffprobe -v error -select_streams v:0 -show_entries stream=color_transfer -of default=nw=1:nk=1 "$IN" | head -1 | tr -d ', \r')
ESC="scale=${AN}:${ALTO:-ih}"; PRE=(); SRC="$IN"
if [[ "$TR" == "arib-std-b67" || "$TR" == "smpte2084" ]]; then
  if command -v avconvert >/dev/null 2>&1; then
    avconvert -s "$IN" -p PresetHighestQuality -o "$TMP/sdr.mov" --replace >/dev/null
    SRC="$TMP/sdr.mov"
    VF="${ESC}:in_color_matrix=bt709:in_range=tv,format=gbrp,lut3d=${LUT}:interp=tetrahedral,scale=out_color_matrix=bt709:out_range=tv,format=yuv420p,setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv"
  else
    if ! ffmpeg -hide_banner -filters 2>/dev/null | grep -q libplacebo; then
      echo "ERROR: bruto HDR sin avconvert y este ffmpeg no tiene libplacebo. Instala un ffmpeg «full» (Windows: winget install -e --id Gyan.FFmpeg)." >&2; exit 1
    fi
    PRE=(-init_hw_device vulkan)
    VF="libplacebo=w=${AN}:h=${ALTO:-ih}:colorspace=bt709:color_primaries=bt709:color_trc=bt709:range=tv:format=yuv420p"
  fi
else
  echo "Aviso: $IN no es HDR ($TR): no hace falta proxy para montar; se hace una copia SDR igualmente." >&2
  VF="${ESC},format=yuv420p,setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv"
fi
ffmpeg -nostdin -v error -y ${PRE[@]+"${PRE[@]}"} -i "$SRC" -vf "$VF" -c:v libx264 -preset fast -crf 14 -g 25 \
  -color_primaries bt709 -color_trc bt709 -colorspace bt709 -color_range tv -c:a aac -b:a 256k "$OUT"
# comprobación: tiene que salir en SDR bt709
TR_OUT=$(ffprobe -v error -select_streams v:0 -show_entries stream=color_transfer -of default=nw=1:nk=1 "$OUT" | head -1 | tr -d ', \r')
if [[ "$TR_OUT" != "bt709" ]]; then echo "ERROR: el proxy ha salido con color_transfer=$TR_OUT (esperado bt709)" >&2; exit 1; fi
echo "$OUT ($TR → $TR_OUT, $(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0:s=x "$OUT" | tr -d '\r'))"
