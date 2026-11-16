#!/usr/bin/env bash
# SOLO AUTOR, en el ordenador de Lucas. edicion-reels tiene su ORIGINAL en publiqo-agency/skills (~/Projects/skills):
# allí se cambia, y sigue igual que siempre. Este script la copia a este repo y la publica como versión nueva (solo esa
# carpeta), y quien tenga Publiqo Edición la recibe sola al abrir Claude Code.
# No hace falta lanzarlo: lo lanza en segundo plano el hook post-commit de ~/Projects/skills en cada commit que toque
# edicion-reels/ (log en .git/espejo-reels.log; si falla, sale un aviso de macOS). A mano también vale (sin cambios no
# publica nada), por ejemplo tras hacer commits de edicion-reels desde otro ordenador.
#   espejo_reels.sh [<commit del original>]     copia y publica (por defecto, HEAD del original)
#   espejo_reels.sh --instalar-hook             deja puesto el hook post-commit en el original
# Lo que la copia pública no lleva: los vídeos de base/refs (reels de otros creadores; ver bajar_refs en lib.sh).
# Lo que añade: .solo-carpeta (no se enlaza global: se usa desde su carpeta de edición), .solo-mac y .aviso-nueva (a
# quien ya tenía el repo se le avisa una vez de que puede crear su carpeta; ver sincronizar.sh).
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
ORIGEN="${PUBLIQO_SKILLS:-$HOME/Projects/skills}"
N="edicion-reels"
LOG="$REPO/.git/espejo-reels.log"

if [ "${1:-}" = --instalar-hook ]; then
  hook="$(git -C "$ORIGEN" rev-parse --path-format=absolute --git-path hooks)/post-commit"
  if [ -e "$hook" ] && ! grep -q espejo_reels "$hook"; then
    echo "Ya hay un hook post-commit en $hook que no es este: añade a mano la llamada a $REPO/espejo_reels.sh."; exit 1
  fi
  cat > "$hook" <<HOOK
#!/bin/sh
# Publiqo Edición: cada commit que toque $N/ se copia a la copia pública (lucasalvarezblancob-ux/publiqo-edicion)
# y se publica como versión nueva. Lo dejó puesto $REPO/espejo_reels.sh --instalar-hook.
git diff-tree --no-commit-id --name-only -r HEAD | grep -q '^$N/' || exit 0
E="$REPO/espejo_reels.sh"
[ -f "\$E" ] || exit 0
c="\$(git rev-parse HEAD)"
( bash "\$E" "\$c" || osascript -e 'display notification "No se pudo copiar $N a publiqo-edicion. Mira $LOG" with title "Publiqo Edición"' ) >> "$LOG" 2>&1 </dev/null &
echo "$N: copiándose a publiqo-edicion en segundo plano (log: $LOG)"
HOOK
  chmod +x "$hook"; echo "✓ Hook puesto: $hook"; exit 0
fi

COMMIT="$(git -C "$ORIGEN" rev-parse "${1:-HEAD}")"
git -C "$ORIGEN" cat-file -e "$COMMIT:$N" 2>/dev/null || { echo "El commit $COMMIT del original no tiene $N/."; exit 1; }

# Un espejo cada vez (dos commits seguidos lanzan dos)
cerrojo="$REPO/.git/espejo-reels.lock"; t=0
until mkdir "$cerrojo" 2>/dev/null; do
  t=$((t + 1)); [ $t -lt 600 ] || { echo "Otro espejo lleva 10 min sin acabar ($cerrojo): bórralo si no hay ninguno en marcha."; exit 1; }
  sleep 1
done
tmp="$(mktemp -d)"
trap 'rmdir "$cerrojo" 2>/dev/null; rm -rf "$tmp"' EXIT

echo "── $(date '+%F %T') espejo de $N desde ${COMMIT:0:7}"
git -C "$ORIGEN" archive "$COMMIT" "$N" | tar -x -C "$tmp"
: > "$tmp/$N/.solo-carpeta"; : > "$tmp/$N/.solo-mac"; : > "$tmp/$N/.aviso-nueva"
# --delete deja la carpeta igual que el original; los vídeos de referencia (no van en git) no se tocan
rsync -a --delete --exclude .DS_Store \
  --exclude '/base/refs/**.mp4' --exclude '/base/refs/**.MP4' --exclude '/base/refs/**.mov' \
  --exclude '/base/refs/**.MOV' --exclude '/base/refs/**.m4v' --exclude '/base/refs/**.mp3' \
  "$tmp/$N/" "$REPO/$N/"

MSG="$(git -C "$ORIGEN" log -1 --format=%s "$COMMIT" -- "$N")"
case "$MSG" in "$N"*) ;; *) MSG="$N: $MSG";; esac
bash "$REPO/publicar.sh" --solo "$N" "$MSG"
