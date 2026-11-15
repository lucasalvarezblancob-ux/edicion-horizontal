#!/usr/bin/env bash
# SOLO AUTOR (AUTORES o cuenta con permiso de escritura en el repo), y solo cuando Lucas lo pida.
# Hace commit de todo el repo de la skill y push a main (github.com/lucasalvarezblancob-ux/edicion-horizontal). Con --con-videos sube además los vídeos nuevos de base/refs al Release
# y regenera base/refs/VIDEOS.txt (sin esa opción, los vídeos de referencia se quedan en local y VIDEOS.txt no se toca).
#   publicar.sh "edicion-horizontal: <qué cambió y por qué>" [--con-videos]
set -euo pipefail
source "$(dirname "$0")/lib.sh"
[ "$(modo)" = autor ] || { echo "Solo el autor (AUTORES) puede publicar el estándar."; exit 1; }
MSG="${1:?Uso: publicar.sh \"$NOMBRE: <qué y por qué>\" [--con-videos]}"
if [ "${2:-}" = --con-videos ]; then
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
git -C "$REPO_DIR" push -q origin main
echo "✓ Publicado: $(git -C "$REPO_DIR" log --oneline -1)"
