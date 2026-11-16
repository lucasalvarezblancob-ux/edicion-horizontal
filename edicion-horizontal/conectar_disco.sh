#!/usr/bin/env bash
# Enlaza personal/<creador>/recursos a su disco duro (busca <disco>/Horizontal/personal/<creador>/recursos en todas las
# unidades) y copia los vídeos y fotogramas de refs/ que falten. Desde la carpeta de edición:
#   bash .claude/skills/edicion-horizontal/conectar_disco.sh <creador>
# Si la letra del disco cambia (D:, E:…), se vuelve a lanzar y se rehace el enlace.
set -uo pipefail
source "$(dirname "$0")/lib.sh"
N="${1:?Uso: conectar_disco.sh <creador>  (p. ej. reinoselva)}"
DEST="${CLAUDE_PROJECT_DIR:-$PWD}"; DEST="$(cd "$DEST" && pwd -P)"
[ -f "$DEST/personal/LEEME.md" ] || { echo "$DEST no es una carpeta de edición (falta personal/LEEME.md)."; exit 1; }
if [ ! -d "$DEST/personal/$N" ] && [ -d "$SKILL/creadores/$N" ]; then instalar_creador "$DEST" "$N"; else conectar_disco "$DEST" "$N"; fi
