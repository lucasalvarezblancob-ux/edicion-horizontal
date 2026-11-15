#!/usr/bin/env bash
# Crea una carpeta de edición de vídeo horizontal desde la plantilla y la deja lista. macOS y Windows (Git Bash).
#   instalar.sh "<ruta>"              carpeta nueva (o vacía)
#   instalar.sh --adoptar "<ruta>"    carpeta que ya existe: solo añade lo que falte, no pisa nada
#   --ligero                          sin skills de apoyo, .venv ni node_modules (para probar la estructura)
#   --creador <nombre>                instala además la personalización de un creador que viene con la skill
#                                     (creadores/<nombre>/, p. ej. reinoselva) y enlaza sus recursos a su disco duro
# Todo lo que ya tengas (programas, skills…) se deja como está: solo se instala lo que falte.
set -euo pipefail
source "$(dirname "$0")/lib.sh"
ADOPTAR=0; LIGERO=0; DEST=""; CREADOR=""; sig=""
for a in "$@"; do
  if [ "$sig" = creador ]; then CREADOR="$a"; sig=""; continue; fi
  case "$a" in --adoptar) ADOPTAR=1;; --ligero) LIGERO=1;; --creador) sig=creador;; --creador=*) CREADOR="${a#--creador=}";; *) DEST="$a";; esac
done
[ -n "$DEST" ] || { echo "Uso: instalar.sh [--adoptar] [--ligero] [--creador <nombre>] \"<ruta de la carpeta de edición>\""; exit 1; }

# 1. Programas (ffmpeg, node, python; recomendados: yt-dlp, gh, mpv): solo los que falten
echo "→ Programas"; instalar_programas || { echo "Faltan programas imprescindibles: instálalos y vuelve a lanzar."; exit 1; }

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
enlazar_skill "$DEST"
# la carpeta es local: si algún día se mete en un repositorio, lo personal y el material no entran
[ -e "$DEST/.gitignore" ] || printf "%s
" "# Carpeta de edición: local. Nada de esto va a git." personal/ bruto/ "bruto terminado/" refs/ out/ estudio/node_modules/ estudio/public/ estudio/.env.local herramientas/.venv/ herramientas/modelos/ .DS_Store __pycache__/ > "$DEST/.gitignore"
# manifiesto: hash de cada archivo tal como viene de la plantilla (actualizar.sh solo pisa lo que no hayas tocado)
archivos_plantilla | while IFS= read -r f; do echo "$(sha "$SKILL/plantilla/$f")  $f"; done > "$DEST/$MANIFIESTO_REL"

# 3. Skills de apoyo (Remotion con remotion-maps, HyperFrames, media-use; lista en SKILLS.txt)
if [ $LIGERO = 0 ]; then echo "→ Skills de apoyo"; instalar_skills "$DEST"; fi

# 4. Referencias estándar (fichas y CONTEXTO.md vienen con la skill; los vídeos, cuando estén publicados)
echo "→ Referencias estándar"; bajar_refs || true

# 5. Pesados (.venv, node_modules)
if [ $LIGERO = 0 ]; then echo "→ Python y Remotion"; instalar_pesados "$DEST" || echo "⚠️  Revisa lo de arriba y lanza actualizar.sh."; fi

# 6. Creador que viene con la skill (su personalización ya hecha + sus recursos en el disco duro)
if [ -n "$CREADOR" ]; then echo "→ Creador: $CREADOR"; instalar_creador "$DEST" "$CREADOR" || true; fi

# 7. Clave de ElevenLabs (opcional)
pedir_clave_elevenlabs "$DEST"

if [ -n "$CREADOR" ]; then cat <<FIN

✓ Carpeta de edición lista: $DEST, con la personalización de «$CREADOR» ya hecha (personal/$CREADOR/).
Sus recursos están en su disco duro: si arriba no salió «personal/$CREADOR/recursos → …», conecta el disco y lanza
  bash .claude/skills/$NOMBRE/conectar_disco.sh $CREADOR   (desde la carpeta de edición)
Abre Claude Code en esa carpeta: cd "$DEST" && claude
Actualizar el estándar más adelante: bash .claude/skills/$NOMBRE/actualizar.sh
FIN
exit 0
fi
cat <<FIN

✓ Carpeta de edición lista: $DEST
Falta (lo hace Claude contigo la primera vez que abras la carpeta):
  1. crear tu personalización: personal/<tu nombre>/ (herramientas/montaje/nuevo_creador.py <nombre>)
  2. personal/<nombre>/perfil.md — nombre, canal, idioma, cámara…
  3. personal/<nombre>/marca.json — canal y @ (el color de serie es amarillo-lima; cámbialo si quieres).
La personalización de cada creador (reglas, marca, números de la base y TODOS sus recursos: intro, logos, clips, música) vive en personal/<creador>/: es local y la skill no la pisa.
La clave de ElevenLabs es opcional: si la saltaste, se puede añadir más adelante.
Abre Claude Code en esa carpeta: cd "$DEST" && claude
Actualizar el estándar más adelante: bash .claude/skills/$NOMBRE/actualizar.sh
FIN
