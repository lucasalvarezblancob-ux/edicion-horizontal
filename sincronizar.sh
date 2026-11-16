#!/usr/bin/env bash
# Publiqo Edición: pone al día el repo y enlaza en ~/.claude/skills cada skill que tenga (las nuevas también).
# Lo lanza un hook global al abrir Claude Code (lo deja puesto el instalador) y el hook de edicion-horizontal.
#   sincronizar.sh            como mucho cada 6 h mira GitHub (sin red ni espera si no toca)
#   sincronizar.sh --ya       mira ahora
# Nunca pisa cambios locales: si la copia tiene cambios sin publicar (el autor trabajando), solo avisa.
# Una skill con el archivo .solo-carpeta (edicion-horizontal) no se enlaza global: se instala en su carpeta de trabajo.
set -uo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"

# git no puede sustituir en Windows un script que se está ejecutando: este se ejecuta desde una copia temporal.
if [ -z "${PUBLIQO_ED_COPIA:-}" ]; then
  tmp="$(mktemp)"; cp "$REPO/sincronizar.sh" "$tmp"
  PUBLIQO_ED_COPIA="$tmp" PUBLIQO_ED_REPO="$REPO" exec bash "$tmp" "$@"
fi
REPO="$PUBLIQO_ED_REPO"; trap 'rm -f "$PUBLIQO_ED_COPIA"' EXIT
limpia() { tr -d '\r'; }
es_windows() { case "$(uname -s)" in MINGW*|MSYS*|CYGWIN*) return 0;; *) return 1;; esac; }

# 1. Versión nueva en GitHub (fast-forward; nada se pisa)
marca="$REPO/.git/ultima-sincronizacion"
ahora="$(date +%s)"; antes="$(cat "$marca" 2>/dev/null | limpia || true)"
if [ "${1:-}" = --ya ] || [ $((ahora - ${antes:-0})) -ge 21600 ]; then
  echo "$ahora" > "$marca"
  if git -C "$REPO" -c http.lowSpeedLimit=1000 -c http.lowSpeedTime=15 fetch -q --tags origin main 2>/dev/null; then
    viejo="$(git -C "$REPO" rev-parse HEAD)"; nuevo="$(git -C "$REPO" rev-parse origin/main)"
    if [ "$viejo" != "$nuevo" ]; then
      if git -C "$REPO" merge-base --is-ancestor origin/main HEAD; then :          # vas por delante (autor sin publicar)
      elif ! git -C "$REPO" merge-base --is-ancestor HEAD origin/main; then
        echo "Publiqo Edición: hay versión nueva, pero esta copia tiene commits propios sin publicar (publicar.sh)."
      elif [ -n "$(git -C "$REPO" status --porcelain)" ]; then
        echo "Publiqo Edición: hay versión nueva, pero hay cambios sin publicar en el repo: no la actualizo sola (publicar.sh primero)."
      elif git -C "$REPO" merge -q --ff-only origin/main; then
        v="$(git -C "$REPO" describe --tags --abbrev=0 2>/dev/null | limpia)"
        echo "Publiqo Edición: actualizadas solas a ${v:-la última versión} ($(git -C "$REPO" rev-list --count "$viejo..HEAD") cambios). Novedades: git -C \"$REPO\" log --oneline ${viejo:0:7}..HEAD"
      fi
    fi
  fi
fi

# 2. Cada skill del repo, enlazada en ~/.claude/skills (solo las que falten)
mkdir -p "$HOME/.claude/skills"
for d in "$REPO"/*/; do
  d="${d%/}"; n="$(basename "$d")"
  [ -f "$d/SKILL.md" ] || continue
  [ -e "$d/.solo-carpeta" ] && continue
  enlace="$HOME/.claude/skills/$n"
  [ -e "$enlace" ] && continue
  if es_windows; then cmd //c mklink //J "$(cygpath -w "$enlace")" "$(cygpath -w "$d")" >/dev/null || { echo "⚠️  No se pudo enlazar la skill $n"; continue; }
  else ln -s "$d" "$enlace"; fi
  echo "Publiqo Edición: skill nueva instalada → $n"
done
exit 0
