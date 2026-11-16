#!/usr/bin/env bash
# Hoja de contactos de un vídeo (para mirar un bruto o una referencia de un vistazo).
# Uso: herramientas/hoja_contactos.sh VIDEO SALIDA.jpg [cada_s=2] [inicio_s=0] [dur_s=todo] [columnas=10]
# Las celdas van en orden: fila a fila; celda n = inicio + n*cada_s.
set -euo pipefail
IN="$1"; OUT="$2"; STEP="${3:-2}"; START="${4:-0}"; DUR="${5:-}"; COLS="${6:-10}"
TOTAL=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$IN")
[ -z "$DUR" ] && DUR=$(echo "$TOTAL - $START" | bc)
N=$(echo "($DUR / $STEP + 0.999)/1" | bc)
ROWS=$(( (N + COLS - 1) / COLS ))
ffmpeg -v error -y -ss "$START" -t "$DUR" -i "$IN" \
  -vf "fps=1/${STEP},scale=135:240,tile=${COLS}x${ROWS}" -frames:v 1 "$OUT"
echo "$OUT  ($N celdas, ${STEP}s cada una desde ${START}s)"
