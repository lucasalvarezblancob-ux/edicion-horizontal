#!/usr/bin/env bash
# Crea una carpeta de edición de reels desde la plantilla y la deja lista.
#   instalar.sh "<ruta>"              carpeta nueva (o vacía)
#   instalar.sh --adoptar "<ruta>"    carpeta que ya existe: solo añade lo que falte, no pisa nada
#   --ligero                          sin modelo Whisper, .venv ni node_modules (para probar)
# Todo lo que ya tengas (programas, skills, modelo…) se deja como está: solo se instala lo que falte.
set -euo pipefail
source "$(dirname "$0")/lib.sh"
ADOPTAR=0; LIGERO=0; DEST=""
for a in "$@"; do case "$a" in --adoptar) ADOPTAR=1;; --ligero) LIGERO=1;; *) DEST="$a";; esac; done
[ -n "$DEST" ] || { echo "Uso: instalar.sh [--adoptar] [--ligero] \"<ruta de la carpeta de edición>\""; exit 1; }
[ "$(uname)" = Darwin ] || echo "⚠️  Pensada para macOS (avconvert, QuickTime, Edits). En otro sistema faltarán piezas."

# 1. Programas (Homebrew, gh, ffmpeg, whisper.cpp, yt-dlp, node, python): solo los que falten
echo "→ Programas"; instalar_programas
[ "$PUBLICA" = 1 ] || gh api "repos/$GH_REPO" -q .full_name >/dev/null || { echo "Tu cuenta de GitHub no tiene acceso a $GH_REPO: pídeselo a Lucas."; exit 1; }

# 2. Carpeta
mkdir -p "$DEST"; DEST="$(cd "$DEST" && pwd -P)"
if [ $ADOPTAR = 0 ] && [ -n "$(ls -A "$DEST" 2>/dev/null | grep -v .DS_Store || true)" ]; then
  echo "$DEST no está vacía. Para convertir una carpeta que ya usas: instalar.sh --adoptar \"$DEST\""; exit 1
fi
echo "→ Carpeta: $DEST"
(cd "$SKILL/plantilla" && find . -type f ! -name .DS_Store | sed 's|^\./||') | while IFS= read -r f; do
  d="$DEST/$f"
  [ -e "$d" ] && continue
  if [ "$(basename "$f")" = .gitkeep ] && [ -d "$(dirname "$d")" ]; then continue; fi
  mkdir -p "$(dirname "$d")"; cp -p "$SKILL/plantilla/$f" "$d"
done
mkdir -p "$DEST/.claude/skills"
[ -e "$DEST/.claude/skills/edicion-reels" ] || ln -s "$SKILL" "$DEST/.claude/skills/edicion-reels"
# manifiesto: hash de cada archivo tal como viene de la plantilla (actualizar.sh solo pisa lo que no hayas tocado)
archivos_plantilla | while IFS= read -r f; do echo "$(sha "$SKILL/plantilla/$f")  $f"; done > "$DEST/$MANIFIESTO_REL"

# 3. it-reelsmaker (skill de terceros que usa el flujo, en la carpeta)
echo "→ it-reelsmaker"; instalar_reelsmaker "$DEST"

# 3b. Skills de apoyo (Remotion, HyperFrames, media-use…; lista en SKILLS.txt)
echo "→ Skills de apoyo"; instalar_skills "$DEST"

# 4. Referencias estándar (vídeos del Release)
echo "→ Referencias estándar"; bajar_refs

# 5. Pesados (modelo Whisper, .venv, node_modules)
[ $LIGERO = 0 ] && { echo "→ Modelo, Python y Remotion"; instalar_pesados "$DEST"; }

# 6. Clave de ElevenLabs (opcional)
pedir_clave_elevenlabs "$DEST"

cat <<FIN

✓ Carpeta de edición lista: $DEST
Falta (lo hace Claude contigo la primera vez que abras la carpeta):
  1. personal/perfil.md — nombre, cuentas, coletillas, código, voz…
  2. estudio/src/comun/marca.ts — HANDLE y CODIGO (el color por defecto es amarillo-lima; cámbialo si quieres).
La clave de ElevenLabs es opcional: si la saltaste, se puede añadir más adelante.
Abre Claude Code en esa carpeta: cd "$DEST" && claude
Actualizar el estándar más adelante: .claude/skills/edicion-reels/actualizar.sh
FIN
