#!/usr/bin/env bash
# Hook SessionStart: limpieza automática de intermedios viejos + avisos (programas, skills, perfil). Rápido, sin red.
source "$(dirname "$0")/lib.sh"
CARPETA="${CLAUDE_PROJECT_DIR:-$PWD}"
PY="$(py_venv "$CARPETA")"; [ -x "$PY" ] || PY="$(py_sistema || true)"
if [ -n "$PY" ] && [ -f "$CARPETA/herramientas/limpiar_renders.py" ]; then "$PY" -I "$CARPETA/herramientas/limpiar_renders.py" --dias 30 || true; fi
faltan=0
if [ -s "$LISTA" ]; then
  while IFS= read -r linea; do
    linea="$(printf '%s' "$linea" | limpia)"; [ -z "$linea" ] && continue; [ -f "$SKILL/base/refs/${linea#*  }" ] || faltan=$((faltan+1))
  done < "$LISTA"
fi
[ "$faltan" -gt 0 ] && echo "$NOMBRE: faltan $faltan vídeos de las referencias estándar (opcionales: las fichas y el CONTEXTO.md bastan para editar) → actualizar.sh los baja."
pf="$(programas_que_faltan)"
[ -n "$pf" ] && echo "$NOMBRE: faltan programas ($pf) → ejecuta bash .claude/skills/$NOMBRE/actualizar.sh."
sf="$(skills_que_faltan "$CARPETA" | cut -d" " -f2- | tr "\n" " ")"
[ -n "$sf" ] && echo "$NOMBRE: faltan skills de apoyo ($sf) → ejecuta bash .claude/skills/$NOMBRE/actualizar.sh."
hay=0
for d in "$CARPETA"/personal/*/; do
  c="$(basename "$d")"; case "$c" in _*|.*|'*') continue;; esac; hay=1
  [ -d "$d/recursos" ] || echo "$NOMBRE: no se puede abrir personal/$c/recursos/ (si está enlazada a otro disco, ¿está conectado?) → sin ella no hay intro, outro, música ni archivo de ese creador. Con el disco conectado: bash .claude/skills/$NOMBRE/conectar_disco.sh $c"
  if [ -f "$d/perfil.md" ] && limpia < "$d/perfil.md" | grep -q '^- \*\*Nombre\*\*: *$'; then
    echo "$NOMBRE: personal/$c/perfil.md sin rellenar (nombre, canal…) → pídeselo al creador antes del primer edit."
  fi
done
[ -d "$CARPETA/recursos" ] && echo "$NOMBRE: queda una carpeta recursos/ en la raíz; los recursos van ahora dentro de cada creador → herramientas/montaje/mover_recursos.py <creador> (no borra nada tuyo)."
[ "$hay" = 0 ] && echo "$NOMBRE: aún no hay ningún creador en personal/ → antes del primer edit: herramientas/montaje/nuevo_creador.py <nombre> y rellenar su perfil."
# Actualización automática: se lanza con exec desde una copia, así este archivo queda libre para que git lo sustituya.
if [ -z "${EDICION_HORIZONTAL_SIN_AUTO:-}" ]; then
  tmp="$(mktemp)"; cat > "$tmp" <<FIN
source "$SKILL/lib.sh"; auto_actualizar "$CARPETA"; rm -f "$tmp"
FIN
  exec bash "$tmp"
fi
exit 0
