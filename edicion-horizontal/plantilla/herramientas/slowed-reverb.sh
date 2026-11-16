#!/usr/bin/env bash
# Convierte una canción en versión "slowed + reverb" para usarla de fondo.
# Uso: herramientas/slowed-reverb.sh cancion.mp3 salida.mp3 [duracion_s] [inicio_s] [velocidad]
#   duracion_s: largo del trozo final (por defecto 30)
#   inicio_s:   desde dónde empieza el trozo de la canción (por defecto 0)
#   velocidad:  0.85 = más lento y grave (por defecto)
set -euo pipefail
IN="$1"; OUT="$2"; DUR="${3:-30}"; START="${4:-0}"; SPEED="${5:-0.85}"
FADE_OUT=$(echo "$DUR - 2.5" | bc)
ffmpeg -v error -y -ss "$START" -i "$IN" -t $(echo "$DUR / $SPEED + 2" | bc) -af "\
asetrate=44100*${SPEED},aresample=44100,\
aecho=0.8:0.85:70|140|280|560:0.35|0.28|0.2|0.14,\
lowpass=f=9000,\
atrim=0:${DUR},afade=t=in:d=1,afade=t=out:st=${FADE_OUT}:d=2.5,\
loudnorm=I=-14:TP=-1.5" -ar 44100 -b:a 256k "$OUT"
echo "Listo: $OUT"
