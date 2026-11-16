#!/usr/bin/env bash
# Hook PreToolUse (Edit|Write|NotebookEdit): en modo local, la skill es de solo lectura.
source "$(dirname "$0")/lib.sh"
ruta="$(python3 -I -c 'import json,sys; d=json.load(sys.stdin).get("tool_input",{}); print(d.get("file_path") or d.get("notebook_path") or "")')"
[ -z "$ruta" ] && exit 0
real="$(python3 -I -c 'import os,sys; print(os.path.realpath(sys.argv[1]))' "$ruta")"
case "$real" in
  "$SKILL"|"$SKILL"/*)
    [ "$(modo)" = autor ] && exit 0
    [ "$PUBLICA" = 1 ] && { echo "La skill edicion-reels es de solo lectura aquí (copia pública; el original está en publiqo-agency/skills). Apunta el cambio en local: personal/preferencias.md, refs/<tipo>/CONTEXTO.md o estudio/src/comun/marca.ts." >&2; exit 2; }
    echo "La skill edicion-reels es de solo lectura (estándar de Lucas). Apunta el cambio en local: personal/preferencias.md, refs/<tipo>/CONTEXTO.md o estudio/src/comun/marca.ts." >&2
    exit 2 ;;
esac
exit 0
