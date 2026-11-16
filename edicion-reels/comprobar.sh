#!/usr/bin/env bash
# Hook SessionStart: avisa si faltan referencias estándar (el mínimo) o si la carpeta no está rellena. Rápido, sin red
# (en la copia pública, además, se pone al día sola: auto_actualizar en lib.sh).
source "$(dirname "$0")/lib.sh"
CARPETA="${CLAUDE_PROJECT_DIR:-$PWD}"
auto_actualizar "$CARPETA"   # solo en la copia pública (publiqo-edicion)
faltan=0
[ "$PUBLICA" = 1 ] || while IFS= read -r linea; do
  [ -z "$linea" ] && continue; [ -f "$SKILL/base/refs/${linea#*  }" ] || faltan=$((faltan+1))
done < "$LISTA"
[ "$faltan" -gt 0 ] && echo "edicion-reels: faltan $faltan vídeos de las referencias estándar → ejecuta .claude/skills/edicion-reels/actualizar.sh antes de editar."
pf="$(programas_que_faltan)"
[ -n "$pf" ] && echo "edicion-reels: faltan programas ($pf) → ejecuta .claude/skills/edicion-reels/actualizar.sh."
sf="$(skills_que_faltan "$CARPETA" | cut -d" " -f2- | tr "\n" " ")"
[ -n "$sf" ] && echo "edicion-reels: faltan skills de apoyo ($sf) → ejecuta .claude/skills/edicion-reels/actualizar.sh."
if [ -f "$CARPETA/personal/perfil.md" ] && grep -q '^- \*\*Instagram\*\*: @ ' "$CARPETA/personal/perfil.md"; then
  echo "edicion-reels: personal/perfil.md sin rellenar (nombre, Instagram…) → pídeselo al creador antes del primer edit."
fi
exit 0
