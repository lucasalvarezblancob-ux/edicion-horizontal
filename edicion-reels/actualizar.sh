#!/usr/bin/env bash
# Trae la última versión del estándar sin tocar lo local.
#   actualizar.sh ["<carpeta de edición>"]   (por defecto, la carpeta actual)
set -uo pipefail
source "$(dirname "$0")/lib.sh"
DEST="${1:-${CLAUDE_PROJECT_DIR:-$PWD}}"; DEST="$(cd "$DEST" && pwd -P)"
[ -f "$DEST/personal/perfil.md" ] || { echo "$DEST no es una carpeta de edición (falta personal/perfil.md)."; exit 1; }

if [ -z "${EDICION_REELS_SIN_PULL:-}" ]; then echo "→ Skill (git pull de $GH_REPO)"
git -C "$REPO_DIR" pull -q --ff-only --autostash origin main || echo "⚠️  No se pudo hacer pull (¿cambios locales en el repo de skills?). Sigo con lo que hay."
fi

# RAPIDO (actualización automática al abrir sesión, copia pública): solo la plantilla; lo lento, en un actualizar.sh normal.
RAPIDO="${EDICION_REELS_RAPIDO:-}"
if [ -z "$RAPIDO" ]; then
echo "→ Referencias estándar"; bajar_refs || echo "⚠️  No se pudieron bajar todas las referencias."

echo "→ Programas"; instalar_programas || echo "⚠️  Faltan programas (mira arriba)."
echo "→ it-reelsmaker"; instalar_reelsmaker "$DEST"
echo "→ Skills de apoyo"; instalar_skills "$DEST"
echo "→ Modelo, Python y Remotion"; instalar_pesados "$DEST" || true
fi

echo "→ Plantilla (herramientas, componentes, config)"
MAN="$DEST/$MANIFIESTO_REL"; touch "$MAN"; NUEVO="$(mktemp)"; tocados=(); cambio_pkg=0; cambio_req=0
while IFS= read -r f; do
  nuevo="$(sha "$SKILL/plantilla/$f")"; d="$DEST/$f"
  viejo="$(awk -v f="$f" 'substr($0,67)==f {print substr($0,1,64)}' "$MAN")"
  if [ ! -e "$d" ]; then
    # nuevo en la plantilla → se añade; si ya estaba en el manifiesto, lo borraste tú: no se repone
    if [ -z "$viejo" ]; then mkdir -p "$(dirname "$d")"; cp -p "$SKILL/plantilla/$f" "$d"; echo "  + $f"; viejo="$nuevo"; fi
  else
    local_h="$(sha "$d")"
    if [ "$local_h" = "$nuevo" ]; then viejo="$nuevo"                       # ya al día
    elif [ "$local_h" = "$viejo" ]; then                                    # sin tocar en local → se actualiza
      cp -p "$SKILL/plantilla/$f" "$d"; echo "  ↻ $f"; viejo="$nuevo"
      case "$f" in estudio/package*.json) cambio_pkg=1;; herramientas/requirements.txt) cambio_req=1;; esac
    elif [ "$nuevo" != "$viejo" ]; then tocados+=("$f")                      # cambiado en local y hay versión nueva
    fi
  fi
  echo "${viejo:-$nuevo}  $f" >> "$NUEVO"
done < <(archivos_plantilla)
mv "$NUEVO" "$MAN"
if [ -n "$RAPIDO" ] && [ $((cambio_pkg + cambio_req)) -gt 0 ]; then
  echo "  La versión nueva cambia dependencias (npm/pip): lanza bash .claude/skills/edicion-reels/actualizar.sh antes de renderizar."
else
[ $cambio_pkg = 1 ] && (cd "$DEST/estudio" && npm install --no-audit --no-fund -q)
[ $cambio_req = 1 ] && { instalar_pesados "$DEST" || true; }
fi
if [ ${#tocados[@]} -gt 0 ]; then
  echo "Hay versión nueva de estos archivos, pero los has cambiado en local y no los toco:"
  printf '  · %s\n' "${tocados[@]}"; echo "  (la versión estándar está en .claude/skills/edicion-reels/plantilla/<ruta>: compárala y decide)"
fi
echo "✓ Al día. Lo tuyo (personal/, refs/, recursos/, out/, marca.ts) no se ha tocado."
