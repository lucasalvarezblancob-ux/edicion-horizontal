#!/usr/bin/env bash
# SOLO AUTOR, y solo cuando Lucas lo pida. Publica TODAS las skills del repo como versión nueva: lo hace publicar.sh de
# la raíz del repo (mismas opciones: "<mensaje>", --mayor, --volver vX.Y, --versiones).
# Con --con-videos sube además los vídeos nuevos de base/refs al Release de referencias y regenera base/refs/VIDEOS.txt.
set -euo pipefail
source "$(dirname "$0")/lib.sh"
VIDEOS=0; ARGS=()
for a in "$@"; do [ "$a" = --con-videos ] && VIDEOS=1 || ARGS+=("$a"); done
[ "$(modo)" = autor ] || { echo "Solo el autor puede publicar."; exit 1; }
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
exec bash "$REPO_DIR/publicar.sh" ${ARGS[@]+"${ARGS[@]}"}
