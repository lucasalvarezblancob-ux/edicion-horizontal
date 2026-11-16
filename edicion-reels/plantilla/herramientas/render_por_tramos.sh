#!/usr/bin/env bash
# Render de Remotion POR TRAMOS para ir liberando RAM (estándar desde 2026-11-15).
# Un render largo (sobre todo 4K con --scale=2) acumula memoria en Chrome headless + ffmpeg hasta el final.
# Aquí cada tramo es un proceso nuevo: al acabar suelta TODA su RAM. El primer tramo mide cuántos fotogramas
# se renderizan por minuto y los siguientes se dimensionan para durar ~MINUTOS (4 por defecto).
# Vídeo por tramos (sin audio) + el audio en una pasada aparte (así no hay clics en las uniones) → unión sin recodificar.
# Uso (desde la carpeta de edición o estudio/):
#   herramientas/render_por_tramos.sh <Composicion> <salida.mp4> [--scale=2 ...otros flags de remotion render]
# Variables: MINUTOS=4 (duración objetivo de cada tramo) · PRIMER=300 (fotogramas del tramo de medida).
# Nota: `sudo purge` (vaciar la caché del sistema) pide contraseña → no se usa; liberar = cerrar el proceso.
set -euo pipefail
COMP="$1"; OUT="$2"; shift 2
EXTRA=("$@")
MINUTOS="${MINUTOS:-4}"; PRIMER="${PRIMER:-300}"
RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
cd "$RAIZ/estudio"
case "$OUT" in /*) ;; *) OUT="$OLDPWD/$OUT" ;; esac
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
CACHE=(--media-cache-size-in-bytes=1000000000 --offthreadvideo-cache-size-in-bytes=1000000000)

# Fotogramas totales de la composición
TOTAL=$(npx remotion compositions 2>/dev/null | awk -v c="$COMP" '$1==c {print $4; exit}')
[ -z "$TOTAL" ] && { echo "No encuentro la composición $COMP" >&2; exit 1; }
echo "▶ $COMP: $TOTAL fotogramas · tramos de ~${MINUTOS} min"

# Audio en una pasada (rápido, no pinta fotogramas)
SOLO_AUDIO=1 npx remotion render "$COMP" "$TMP/audio.wav" --codec=wav --log=error ${EXTRA[@]+"${EXTRA[@]}"}

ini=0; n=0; LISTA="$TMP/lista.txt"; : > "$LISTA"
tramo=$PRIMER
while [ "$ini" -lt "$TOTAL" ]; do
  fin=$(( ini + tramo - 1 )); [ "$fin" -ge "$TOTAL" ] && fin=$(( TOTAL - 1 ))
  n=$((n+1)); f="$TMP/tramo_$(printf %03d $n).mp4"
  t0=$(date +%s)
  npx remotion render "$COMP" "$f" --codec=h264 --muted --frames="$ini-$fin" --log=error "${CACHE[@]}" ${EXTRA[@]+"${EXTRA[@]}"}
  t=$(( $(date +%s) - t0 )); [ "$t" -lt 1 ] && t=1
  echo "  tramo $n: fotogramas ${ini}-${fin} en ${t}s (RAM liberada al cerrar el proceso)"
  echo "file '$f'" >> "$LISTA"
  # siguiente tramo: los fotogramas que caben en MINUTOS al ritmo medido
  tramo=$(( (fin - ini + 1) * MINUTOS * 60 / t )); [ "$tramo" -lt 60 ] && tramo=60
  ini=$(( fin + 1 ))
done

ffmpeg -v error -y -f concat -safe 0 -i "$LISTA" -i "$TMP/audio.wav" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 320k -shortest -movflags +faststart "$OUT"
echo "✔ $OUT ($n tramos)"
