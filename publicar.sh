#!/usr/bin/env bash
# SOLO AUTOR (cuenta de AUTORES o con permiso de escritura en el repo), y solo cuando Lucas lo pida.
# Publica TODAS las skills del repo como una VERSIÓN nueva: commit, push a main, etiqueta vMAYOR.MENOR y Release en
# GitHub. Quien las tenga instaladas se pone al día solo al abrir Claude Code.
#   publicar.sh "<qué cambió y por qué>"            versión menor nueva (v2.3 → v2.4)
#   publicar.sh "<qué cambió>" --mayor              versión mayor nueva (v2.4 → v3.0)
#   publicar.sh --volver v2.2 ["<por qué>"]         ROLLBACK: todo vuelve a quedar como en v2.2, publicado como versión
#                                                   nueva (nada se borra del historial; se puede volver a cualquier otra)
#   publicar.sh --versiones                         lista las versiones publicadas
#   publicar.sh --solo <skill> "<qué cambió>"       versión nueva con solo los cambios de esa carpeta (lo demás que
#                                                   haya sin publicar se queda como está; lo usa espejo_reels.sh)
# Antes del commit, cada skill puede preparar lo suyo con <skill>/antes_de_publicar.sh (edicion-horizontal copia ahí
# los perfiles de creadores desde la carpeta de edición del autor).
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
GH_REPO="lucasalvarezblancob-ux/publiqo-edicion"
limpia() { tr -d '\r'; }
ultima_version() { git -C "$REPO" tag -l 'v[0-9]*.[0-9]*' --sort=-v:refname | limpia | head -1; }
modo() {
  local login push
  login="$(gh api user -q .login 2>/dev/null | limpia || true)"
  [ -n "$login" ] || { echo local; return; }
  if limpia < "$REPO/AUTORES" | grep -qx "$login"; then echo autor; return; fi
  push="$(gh api "repos/$GH_REPO" -q .permissions.push 2>/dev/null | limpia || true)"
  [ "$push" = true ] && echo autor || echo local
}

MSG=""; MAYOR=0; VOLVER=""; SOLO=""; sig=""
for a in "$@"; do
  if [ "$sig" = volver ]; then VOLVER="$a"; sig=""; continue; fi
  if [ "$sig" = solo ]; then SOLO="${a%/}"; sig=""; continue; fi
  case "$a" in
    --mayor) MAYOR=1;; --volver) sig=volver;; --solo) sig=solo;;
    --versiones) git -C "$REPO" fetch -q --tags origin 2>/dev/null || true
                 git -C "$REPO" tag -l 'v[0-9]*.[0-9]*' --sort=-v:refname --format='%(refname:short)  %(creatordate:short)  %(subject)'; exit 0;;
    *) MSG="$a";;
  esac
done
[ "$(modo)" = autor ] || { echo "Solo el autor (AUTORES o con permiso de escritura en $GH_REPO) puede publicar."; exit 1; }
[ -z "$SOLO" ] || [ -d "$REPO/$SOLO" ] || { echo "No existe la carpeta $SOLO en el repo."; exit 1; }
[ -z "$SOLO" ] || [ -z "$VOLVER" ] || { echo "--solo y --volver no van juntos."; exit 1; }
git -C "$REPO" fetch -q --tags origin
if [ -n "$VOLVER" ]; then
  git -C "$REPO" rev-parse -q --verify "refs/tags/$VOLVER" >/dev/null || { echo "No existe la versión $VOLVER (publicar.sh --versiones)."; exit 1; }
  [ -z "$(git -C "$REPO" status --porcelain)" ] || { echo "Hay cambios sin publicar: publícalos o descártalos antes de volver a $VOLVER."; exit 1; }
  git -C "$REPO" pull -q --ff-only origin main
  git -C "$REPO" read-tree -u --reset "$VOLVER"
  MSG="Vuelta a $VOLVER${MSG:+: $MSG}"
else
  for h in "$REPO"/${SOLO:-*}/antes_de_publicar.sh; do [ -f "$h" ] && bash "$h"; done
fi
[ -n "$MSG" ] || { echo "Uso: publicar.sh \"<qué cambió y por qué>\" [--mayor]  |  --volver vX.Y  |  --versiones"; exit 1; }

RUTA="${SOLO:-.}"
git -C "$REPO" add -A -- "$RUTA"
if git -C "$REPO" diff --cached --quiet -- "$RUTA"; then echo "Nada que publicar."; exit 0; fi
git -C "$REPO" commit -q -m "$MSG" -- "$RUTA"
git -C "$REPO" pull -q --rebase --autostash origin main
ULT="$(ultima_version)"; ULT="${ULT:-v1.-1}"; MA="${ULT#v}"; MA="${MA%%.*}"; ME="${ULT##*.}"
if [ $MAYOR = 1 ]; then V="v$((MA + 1)).0"; else V="v$MA.$((ME + 1))"; fi
git -C "$REPO" tag -a "$V" -m "$MSG"
git -C "$REPO" push -q origin main "$V"
if command -v gh >/dev/null 2>&1; then
  NOTAS="$MSG"
  [ -n "${ULT#v1.-1}" ] && NOTAS="$MSG

Cambios desde $ULT:
$(git -C "$REPO" log --format='- %s' "$ULT..$V" | limpia)"
  gh release create "$V" -R "$GH_REPO" --title "$V" --notes "$NOTAS" --verify-tag >/dev/null || echo "⚠️  $V etiquetada y subida, pero no se pudo crear el Release en GitHub."
fi
echo "✓ Publicada $V: $(git -C "$REPO" log --oneline -1)"
echo "  Quien tenga las skills se pondrá al día solo al abrir Claude Code (rollback: publicar.sh --volver $ULT)."
