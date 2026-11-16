#!/usr/bin/env bash
# Instalador de las Publiqo Edición para macOS: todas las skills y todo lo necesario para editar y renderizar.
# Crea dos carpetas de edición: ~/Desktop/Horizontal (edicion-horizontal) y ~/Desktop/Reels (edicion-reels).
# En Terminal:
#   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/lucasalvarezblancob-ux/publiqo-edicion/main/instalar-mac.sh)"
# con creador que viene incluido y/u otra carpeta de edición (por defecto ~/Desktop/Horizontal):
#   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/lucasalvarezblancob-ux/publiqo-edicion/main/instalar-mac.sh)" _ --creador reinoselva
#
# Hace: Homebrew (te pide la contraseña del Mac) y con él git, ffmpeg, node, python, yt-dlp y gh si faltan; Claude
# Code si falta; descarga el repo en ~/Projects/publiqo-edicion (o lo actualiza); enlaza todas sus skills en
# ~/.claude/skills y deja el hook que las actualiza solas (y añade las nuevas); y lanza edicion-horizontal/instalar.sh:
# la carpeta de edición, las skills de apoyo (Remotion, HyperFrames), la .venv de Python, node_modules y el navegador
# de render. Con --creador, deja además su personalización y enlaza sus recursos a su disco duro.
set -euo pipefail
REPO="https://github.com/lucasalvarezblancob-ux/publiqo-edicion.git"
SKILLS_DIR="$HOME/Projects/publiqo-edicion"
CARPETA="$HOME/Desktop/Horizontal"; REELS="$HOME/Desktop/Reels"; EXTRA=()
while [ $# -gt 0 ]; do
  case "$1" in
    --creador) EXTRA+=(--creador "$2"); shift 2;;
    --carpeta) CARPETA="$2"; shift 2;;
    --reels) REELS="$2"; shift 2;;
    *) CARPETA="$1"; shift;;
  esac
done
[ "$(uname)" = Darwin ] || { echo "Esto es para macOS. En Windows: instalar.ps1 (ver README.md)."; exit 1; }

if ! command -v brew >/dev/null 2>&1; then
  echo "→ Homebrew (te pedirá la contraseña del Mac)"
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi
[ -x /opt/homebrew/bin/brew ] && eval "$(/opt/homebrew/bin/brew shellenv)"
[ -x /usr/local/bin/brew ] && eval "$(/usr/local/bin/brew shellenv)"

echo "→ Programas (solo los que falten)"
faltan=()
for c in git ffmpeg node python3 yt-dlp gh; do
  command -v "$c" >/dev/null 2>&1 || faltan+=("$c")
done
python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)" 2>/dev/null || faltan+=(python)
if [ ${#faltan[@]} -gt 0 ]; then
  pk=""; for c in "${faltan[@]}"; do case "$c" in python3|python) pk="$pk python@3.12";; *) pk="$pk $c";; esac; done
  # shellcheck disable=SC2086
  brew install $pk
fi

if ! command -v claude >/dev/null 2>&1; then
  echo "→ Claude Code"
  curl -fsSL https://claude.ai/install.sh | bash || echo "⚠️  No se pudo instalar Claude Code: https://claude.com/claude-code"
fi

echo "→ Publiqo Edición en $SKILLS_DIR"
if [ -d "$SKILLS_DIR/.git" ]; then git -C "$SKILLS_DIR" pull -q --ff-only origin main
else mkdir -p "$(dirname "$SKILLS_DIR")"; git clone -q "$REPO" "$SKILLS_DIR"; fi

echo "→ Todas las skills (enlazadas en ~/.claude/skills) y actualización automática"
PUBLIQO_ED_SIN_AVISOS=1 bash "$SKILLS_DIR/sincronizar.sh" --ya
python3 "$SKILLS_DIR/hook_global.py" "$SKILLS_DIR"

echo "→ edicion-horizontal: carpeta de edición"
ADOPTAR=()
[ -f "$CARPETA/personal/LEEME.md" ] && ADOPTAR=(--adoptar)
bash "$SKILLS_DIR/edicion-horizontal/instalar.sh" ${ADOPTAR[@]+"${ADOPTAR[@]}"} ${EXTRA[@]+"${EXTRA[@]}"} "$CARPETA"

echo "→ edicion-reels: carpeta de edición de reels verticales"
# siempre --adoptar: en una carpeta nueva hace lo mismo y no choca con la clave copiada justo antes
# la clave de ElevenLabs (opcional) que se diera para la horizontal vale también aquí: no se pregunta dos veces
if [ -f "$CARPETA/estudio/.env.local" ] && [ ! -f "$REELS/estudio/.env.local" ]; then
  mkdir -p "$REELS/estudio"; (umask 077; cp "$CARPETA/estudio/.env.local" "$REELS/estudio/.env.local")
fi
bash "$SKILLS_DIR/edicion-reels/instalar.sh" --adoptar "$REELS" ||
  echo "⚠️  La carpeta de reels no quedó completa: vuelve a lanzar este instalador o bash \"$SKILLS_DIR/edicion-reels/actualizar.sh\" \"$REELS\""
echo
echo "Listo. Abre la carpeta con Claude Code:"
echo "  vídeo horizontal (YouTube):  cd \"$CARPETA\" && claude"
echo "  reels verticales:            cd \"$REELS\" && claude"
