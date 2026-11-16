#!/usr/bin/env bash
# Precálculo ligero de una referencia: cortes, transcripción (idioma detectado) y hojas de contactos.
# Uso: herramientas/precalcular_ref.sh <video>.mp4 [carpeta de salida]   (sin demucs: no separa música)
# Por defecto deja el análisis en refs/dinamicos/_analisis/<video>/; para un creador: personal/<creador>/refs/_analisis/<video>
# Además de la intro y el vídeo entero, saca los últimos 40 s cada 0,5 s (hojas/final_NN.jpg) para ver la outro y el cierre.
set -euo pipefail
V="$1"; N=$(basename "$V" .mp4); D="${2:-refs/dinamicos/_analisis/$N}"; mkdir -p "$D/hojas" "$D/rotulos" "$D/detalle"
case "$(uname -s)" in MINGW*|MSYS*|CYGWIN*) PY=herramientas/.venv/Scripts/python.exe ;; *) PY=herramientas/.venv/bin/python ;; esac
[ -f "$D/cortes.json" ] || $PY herramientas/detectar_cortes.py "$V" "$D/cortes.json" >/dev/null
[ -f "$D/transcripcion.json" ] || PYTHONIOENCODING=utf-8 $PY herramientas/transcribir.py "$V" "$D/transcripcion.json" --idioma auto >/dev/null
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$V" | tr -d '\r' | cut -d. -f1)
for i in 0 1 2 3 4 5 6 7; do o="$D/hojas/intro_0$i.jpg"; [ -f "$o" ] || bash herramientas/hoja_contactos.sh "$V" "$o" 0.25 $(awk -v i=$i 'BEGIN{print i*7.5}') 7.5 6 320 >/dev/null </dev/null; done
m=0; while [ $((m*60)) -lt "$DUR" ]; do o=$(printf "%s/hojas/min_%02d.jpg" "$D" $m); r=$((DUR-m*60)); [ $r -gt 60 ] && r=60
  [ -f "$o" ] || bash herramientas/hoja_contactos.sh "$V" "$o" 2 $((m*60)) $r 6 320 >/dev/null </dev/null; m=$((m+1)); done
for i in 0 1; do o="$D/hojas/final_0$i.jpg"; [ -f "$o" ] || bash herramientas/hoja_contactos.sh "$V" "$o" 0.5 $((DUR-40+i*20)) 20 8 320 >/dev/null </dev/null; done
echo "$N listo: $(ls "$D/hojas" | wc -l) hojas"
