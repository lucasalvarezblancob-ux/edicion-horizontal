#!/usr/bin/env bash
# Hook PreToolUse (Edit|Write|NotebookEdit): en modo local, la skill es de solo lectura.
# Las rutas se comparan NORMALIZADAS dentro de Python (realpath + normcase): en Windows la herramienta manda
# C:\Users\…, bash ve /c/Users/… y la skill cuelga de un «junction»; comparadas como texto no coinciden nunca
# (por eso el hook de edicion-reels no bloqueaba en Windows).
source "$(dirname "$0")/lib.sh"
PY="$(py_sistema)" || exit 0
RAIZ="$SKILL"; es_windows && RAIZ="$(cygpath -w "$SKILL")"
dentro="$("$PY" -I -c '
import json, os, sys
d = json.load(sys.stdin).get("tool_input", {}); ruta = d.get("file_path") or d.get("notebook_path") or ""
if not ruta: print("no"); sys.exit()
n = lambda p: os.path.normcase(os.path.realpath(p))
r, s = n(ruta), n(sys.argv[1])
print("si" if r == s or r.startswith(s + os.sep) else "no")' "$RAIZ" | limpia)"
[ "$dentro" = si ] || exit 0
[ "$(modo)" = autor ] && exit 0
echo "La skill $NOMBRE es de solo lectura (estándar de Lucas). Apunta el cambio en la carpeta de personalización (personal/<creador>/: preferencias.md, recursos.md, ajustes.py, marca.json) o en refs/<tipo>/CONTEXTO.md." >&2
exit 2
