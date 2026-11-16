#!/usr/bin/env bash
# Transcribe un vídeo/audio en español con whisper.cpp (local, sin internet).
# Uso: herramientas/transcribir.sh MEDIA [salida_sin_extension]
#   Sin salida: imprime la transcripción con tiempos por frase.
#   Con salida: además escribe <salida>.json con tiempos POR PALABRA (para voz propia
#   del usuario: cortar silencios y sincronizar subtítulos).
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
MODEL="$DIR/modelos/ggml-small.bin"
IN="$1"; OUT="${2:-}"
TMP="$(mktemp -d)"
ffmpeg -v error -y -i "$IN" -ar 16000 -ac 1 "$TMP/a.wav"
if [ -z "$OUT" ]; then
  whisper-cli -m "$MODEL" -l es -f "$TMP/a.wav" 2>/dev/null
else
  whisper-cli -m "$MODEL" -l es -f "$TMP/a.wav" -ml 1 -sow -ojf -of "$OUT" 2>/dev/null
  echo "Tiempos por palabra: $OUT.json"
fi
rm -rf "$TMP"
