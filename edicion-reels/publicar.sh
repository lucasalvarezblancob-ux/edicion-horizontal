#!/usr/bin/env bash
# SOLO AUTOR: sube vídeos nuevos de base/refs al Release, regenera VIDEOS.txt, commit de edicion-reels/ y push a main.
#   publicar.sh "edicion-reels: <qué cambió y por qué>"
#   publicar.sh --solo-videos      solo sube los vídeos y regenera VIDEOS.txt (sin commit)
set -euo pipefail
source "$(dirname "$0")/lib.sh"
[ "$PUBLICA" = 1 ] && { echo "Esta es la copia pública de edicion-reels (publiqo-edicion). El estándar se cambia en el original, publiqo-agency/skills (~/Projects/skills/edicion-reels): al hacer commit allí se copia aquí sola."; exit 1; }
[ "$(modo)" = autor ] || { echo "Solo el autor (AUTORES) puede publicar el estándar."; exit 1; }
MSG="${1:?Uso: publicar.sh \"edicion-reels: <qué y por qué>\" | --solo-videos}"
gh release view "$RELEASE" -R "$GH_REPO" >/dev/null 2>&1 || \
  gh release create "$RELEASE" -R "$GH_REPO" --title "edicion-reels — vídeos de las referencias estándar" \
    --notes "Vídeos de edicion-reels/base/refs. Cada asset se llama por su hash; la ruta está en base/refs/VIDEOS.txt. Los baja instalar.sh / actualizar.sh." --latest=false
SUBIDOS="$(gh release view "$RELEASE" -R "$GH_REPO" --json assets -q '.assets[].name')"
NUEVA="$(mktemp)"
(cd "$SKILL/base/refs" && find . -type f \( -iname '*.mp4' -o -iname '*.mov' -o -iname '*.m4v' -o -iname '*.mp3' \) | sed 's|^\./||' | LC_ALL=C sort) |
while IFS= read -r ruta; do
  h="$(sha "$SKILL/base/refs/$ruta")"; n="$(nombre_asset "$h")"
  if ! grep -qx "$n" <<<"$SUBIDOS"; then
    tmp="$(mktemp -d)"; cp "$SKILL/base/refs/$ruta" "$tmp/$n"
    echo "  ↑ $ruta"; gh release upload "$RELEASE" -R "$GH_REPO" "$tmp/$n" --clobber; rm -rf "$tmp"
  fi
  echo "$h  $ruta" >> "$NUEVA"
done
mv "$NUEVA" "$LISTA"
[ "$MSG" = --solo-videos ] && { echo "✓ Vídeos subidos; VIDEOS.txt al día."; exit 0; }
git -C "$REPO_DIR" add -A -- edicion-reels
if git -C "$REPO_DIR" diff --cached --quiet -- edicion-reels; then echo "Nada que publicar en git."; exit 0; fi
git -C "$REPO_DIR" commit -q -m "$MSG" -- edicion-reels
git -C "$REPO_DIR" pull -q --rebase --autostash origin main
git -C "$REPO_DIR" push -q origin main
echo "✓ Publicado: $(git -C "$REPO_DIR" log --oneline -1)"
