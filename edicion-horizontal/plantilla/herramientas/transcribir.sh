#!/usr/bin/env bash
# Transcribe un vídeo o audio en local (faster-whisper) con tiempos por palabra. El IDIOMA se detecta solo: no lo
# fuerces sin haber comprobado en qué idioma se habla (un vídeo en inglés transcrito como español sale inservible).
# Uso: herramientas/transcribir.sh MEDIA SALIDA.json [idioma=auto|es|en…]
#   Escribe SALIDA.json (frases con confianza y palabras con tiempo) y SALIDA.txt (una línea por frase, para leer).
# Ojo: los tiempos por palabra de Whisper van ~0,2 s adelantados; para cortar o colgar textos de palabras, alinea
# (herramientas/montaje/paso1_alinear.py o herramientas/alinear_palabras.py).
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
PY="$DIR/.venv/Scripts/python.exe"; [ -x "$PY" ] || PY="$DIR/.venv/bin/python"
PYTHONIOENCODING=utf-8 "$PY" "$DIR/transcribir.py" "$1" "$2" --idioma "${3:-auto}"
