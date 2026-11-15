#!/usr/bin/env bash
# SOLO AUTOR (AUTORES o cuenta con permiso de escritura en el repo), y solo cuando Lucas lo pida.
# Publica la skill como VERSIÓN nueva: commit de todo el repo, push a main, etiqueta vMAYOR.MENOR y Release en GitHub
# (github.com/lucasalvarezblancob-ux/edicion-horizontal/releases). Las instalaciones se ponen al día solas al abrir sesión.
#   publicar.sh "<qué cambió y por qué>"            versión menor nueva (v1.3 → v1.4)
#   publicar.sh "<qué cambió>" --mayor              versión mayor nueva (v1.4 → v2.0)
#   publicar.sh --volver v1.2 ["<por qué>"]         ROLLBACK: la skill vuelve a quedar como en v1.2, publicado como versión
#                                                   nueva (nada se borra del historial; se puede volver a cualquier otra)
#   publicar.sh --versiones                         lista las versiones publicadas
#   --con-videos                                    sube además los vídeos nuevos de base/refs al Release de referencias
set -euo pipefail
source "$(dirname "$0")/lib.sh"
ultima_version() { git -C "$REPO_DIR" tag -l 'v[0-9]*.[0-9]*' --sort=-v:refname | limpia | head -1; }
MSG=""; VIDEOS=0; MAYOR=0; VOLVER=""; sig=""
for a in "$@"; do
  if [ "$sig" = volver ]; then VOLVER="$a"; sig=""; continue; fi
  case "$a" in
    --con-videos) VIDEOS=1;; --mayor) MAYOR=1;; --volver) sig=volver;;
    --versiones) git -C "$REPO_DIR" fetch -q --tags origin 2>/dev/null || true
                 git -C "$REPO_DIR" tag -l 'v[0-9]*.[0-9]*' --sort=-v:refname --format='%(refname:short)  %(creatordate:short)  %(subject)'; exit 0;;
    *) MSG="$a";;
  esac
done
[ "$(modo)" = autor ] || { echo "Solo el autor (AUTORES o con permiso de escritura en $GH_REPO) puede publicar."; exit 1; }
git -C "$REPO_DIR" fetch -q --tags origin
if [ -n "$VOLVER" ]; then
  git -C "$REPO_DIR" rev-parse -q --verify "refs/tags/$VOLVER" >/dev/null || { echo "No existe la versión $VOLVER (publicar.sh --versiones)."; exit 1; }
  [ -z "$(git -C "$REPO_DIR" status --porcelain)" ] || { echo "Hay cambios sin publicar en la skill: publícalos o descártalos antes de volver a $VOLVER."; exit 1; }
  git -C "$REPO_DIR" pull -q --ff-only origin main
  git -C "$REPO_DIR" read-tree -u --reset "$VOLVER"
  MSG="Vuelta a $VOLVER${MSG:+: $MSG}"
fi
[ -n "$MSG" ] || { echo "Uso: publicar.sh \"<qué cambió y por qué>\" [--mayor] [--con-videos]  |  --volver vX.Y  |  --versiones"; exit 1; }
if [ $VIDEOS = 1 ]; then
  gh release view "$RELEASE" -R "$GH_REPO" >/dev/null 2>&1 || \
    gh release create "$RELEASE" -R "$GH_REPO" --title "$NOMBRE — vídeos de las referencias estándar" \
      --notes "Vídeos de $NOMBRE/base/refs. Cada asset se llama por su hash; la ruta está en base/refs/VIDEOS.txt. Los baja instalar.sh / actualizar.sh." --latest=false
  SUBIDOS="$(gh release view "$RELEASE" -R "$GH_REPO" --json assets -q '.assets[].name' | limpia)"
  NUEVA="$(mktemp)"
  (cd "$SKILL/base/refs" && find . -type f \( -iname '*.mp4' -o -iname '*.mov' -o -iname '*.m4v' \) | sed 's|^\./||' | limpia | LC_ALL=C sort) |
  while IFS= read -r ruta; do
    h="$(sha "$SKILL/base/refs/$ruta")"; n="$(nombre_asset "$h")"
    if ! grep -qx "$n" <<<"$SUBIDOS"; then
      tmp="$(mktemp -d)"; cp "$SKILL/base/refs/$ruta" "$tmp/$n"
      echo "  ↑ $ruta"; gh release upload "$RELEASE" -R "$GH_REPO" "$tmp/$n" --clobber; rm -rf "$tmp"
    fi
    echo "$h  $ruta" >> "$NUEVA"
  done
  mv "$NUEVA" "$LISTA"
fi
# El repo es la skill entera. Los vídeos de referencia y lo pesado de los creadores están en .gitignore.
git -C "$REPO_DIR" add -A
if git -C "$REPO_DIR" diff --cached --quiet; then echo "Nada que publicar en git."; exit 0; fi
git -C "$REPO_DIR" commit -q -m "$MSG"
git -C "$REPO_DIR" pull -q --rebase --autostash origin main
# versión nueva
ULT="$(ultima_version)"; ULT="${ULT:-v1.-1}"; MA="${ULT#v}"; MA="${MA%%.*}"; ME="${ULT##*.}"
if [ $MAYOR = 1 ]; then V="v$((MA + 1)).0"; else V="v$MA.$((ME + 1))"; fi
git -C "$REPO_DIR" tag -a "$V" -m "$MSG"
git -C "$REPO_DIR" push -q origin main "$V"
if command -v gh >/dev/null 2>&1; then
  NOTAS="$MSG"
  [ -n "${ULT#v1.-1}" ] && NOTAS="$MSG

Cambios desde $ULT:
$(git -C "$REPO_DIR" log --format='- %s' "$ULT..$V" | limpia)"
  gh release create "$V" -R "$GH_REPO" --title "$V" --notes "$NOTAS" --verify-tag >/dev/null || echo "⚠️  Versión $V etiquetada y subida, pero no se pudo crear el Release en GitHub."
fi
echo "✓ Publicada $V: $(git -C "$REPO_DIR" log --oneline -1)"
echo "  Las instalaciones se pondrán al día solas al abrir sesión (rollback: publicar.sh --volver $ULT)."
