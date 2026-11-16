#!/usr/bin/env bash
# Lo lanza publicar.sh (raíz) antes del commit: copia a creadores/<n>/ el perfil de cada creador incluido desde la
# carpeta de edición del autor (la del Claude Code abierto, o la actual), que es el original. Sin recursos/ ni lo pesado
# de refs/ (vídeos, fotogramas: van en el disco del creador). No borra nada de creadores/<n>/.
set -uo pipefail
source "$(dirname "$0")/lib.sh"
ED="${CLAUDE_PROJECT_DIR:-$PWD}"
[ -f "$ED/personal/LEEME.md" ] || { echo "  (perfiles de creadores: no estoy en una carpeta de edición; se publican como estén en creadores/)"; exit 0; }
for n in $(creadores_incluidos); do
  [ -d "$ED/personal/$n" ] || continue
  c=0
  copiar() {   # copiar <origen> <destino>
    if [ ! -f "$2" ] || [ "$(sha "$1")" != "$(sha "$2")" ]; then mkdir -p "$(dirname "$2")"; cp -p "$1" "$2"; c=$((c+1)); fi
  }
  while IFS= read -r f; do copiar "$ED/personal/$n/$f" "$SKILL/creadores/$n/personal/$f"
  done < <(cd "$ED/personal/$n" && find . -path ./recursos -prune -o -type f -print | sed 's|^\./||' |
           grep -v -i -E '\.(mp4|mov|png|jpe?g|pdf|webp)$|__pycache__|\.pyc$')
  for sub in src public; do
    [ -d "$ED/estudio/$sub/personal/$n" ] || continue
    while IFS= read -r f; do copiar "$ED/estudio/$sub/personal/$n/$f" "$SKILL/creadores/$n/estudio/$sub/personal/$n/$f"
    done < <(cd "$ED/estudio/$sub/personal/$n" && find . -type f | sed 's|^\./||')
  done
  echo "  perfil de $n: $c archivos al día en creadores/$n/"
done
