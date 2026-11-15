#!/usr/bin/env bash
# uso: hoja.sh SALIDA INICIO DUR FPS COLS FILAS ANCHO [crop]
cd "C:/Users/Lucas/Desktop/Horizontal/personal/reinoselva/refs"
C=_analisis/2026-09-26_78wavVq4ymI/creador
CROP=""; [ -n "${8:-}" ] && CROP="crop=$8,"
ffmpeg -nostdin -v error -y -ss "$2" -t "$3" -i 2026-09-26_78wavVq4ymI.mp4 -vf "fps=$4,${CROP}scale=$7:-2,tile=$5x$6" -frames:v 1 -q:v 3 "$C/$1"
