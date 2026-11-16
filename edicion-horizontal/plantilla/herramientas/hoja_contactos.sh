#!/usr/bin/env bash
# Hoja de contactos 16:9 con el tiempo impreso en cada celda.
# Uso: herramientas/hoja_contactos.sh VIDEO SALIDA.jpg [cada_s=2] [inicio_s=0] [dur_s=todo] [columnas=6] [ancho_celda=320]
# Celdas en orden, fila a fila; celda n = inicio + n*cada_s. Para intros: cada_s=0.25.
set -euo pipefail
IN="$1"; OUT="$2"; STEP="${3:-2}"; START="${4:-0}"; DUR="${5:-}"; COLS="${6:-6}"; W="${7:-320}"
TOTAL=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$IN" | tr -d '\r')
[ -z "$DUR" ] && DUR=$(awk -v t="$TOTAL" -v s="$START" 'BEGIN{print t-s}')
N=$(awk -v d="$DUR" -v s="$STEP" 'BEGIN{n=d/s; print (n==int(n))?n:int(n)+1}')
ROWS=$(( (N + COLS - 1) / COLS ))
case "$(uname -s)" in
  Darwin) FONT="/System/Library/Fonts/Helvetica.ttc" ;;
  MINGW*|MSYS*|CYGWIN*) FONT="C\:/Windows/Fonts/arial.ttf" ;;
  *) FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf" ;;
esac
FPS=$(awk -v s="$STEP" 'BEGIN{printf "%.6f", 1/s}')
ffmpeg -v error -y -ss "$START" -t "$DUR" -i "$IN" \
  -vf "fps=${FPS},scale=${W}:-2,drawtext=fontfile='${FONT}':text='%{eif\:(t+${START})/60\:d\:2}\:%{eif\:mod(t+${START}\,60)\:d\:2}.%{eif\:mod((t+${START})*100\,100)\:d\:2}':x=6:y=6:fontsize=18:fontcolor=white:box=1:boxcolor=black@0.6:boxborderw=4,tile=${COLS}x${ROWS}" \
  -frames:v 1 -q:v 3 "$OUT"
echo "$OUT  ($N celdas, ${STEP}s cada una desde ${START}s)"
