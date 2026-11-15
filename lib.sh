# Funciones comunes de edicion-horizontal (se carga con `source`). Vale para macOS y para Windows (Git Bash).
SKILL="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
# El repositorio ES la skill (github.com/lucasalvarezblancob-ux/edicion-horizontal): público para descargar; solo suben
# cambios la cuenta dueña y sus colaboradores.
REPO_DIR="$(git -C "$SKILL" rev-parse --show-toplevel 2>/dev/null || echo "$SKILL")"
NOMBRE="edicion-horizontal"
GH_REPO="lucasalvarezblancob-ux/edicion-horizontal"
GH_URL="https://github.com/$GH_REPO.git"
RELEASE="edicion-horizontal-refs"
LISTA="$SKILL/base/refs/VIDEOS.txt"   # "<sha256>  <ruta relativa a base/refs>"; vacía mientras los vídeos de referencia no estén publicados

es_windows() { case "$(uname -s)" in MINGW*|MSYS*|CYGWIN*) return 0;; *) return 1;; esac; }
limpia() { tr -d '\r'; }               # en Windows los archivos pueden llegar con retorno de carro: nunca dentro de un nombre

# Python del sistema que funciona de verdad (en Windows `python3` suele ser el acceso directo vacío de la Tienda).
py_sistema() {
  local c
  for c in python3 python py; do
    if command -v "$c" >/dev/null 2>&1 && "$c" -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)" >/dev/null 2>&1; then echo "$c"; return 0; fi
  done
  return 1
}
# Python de la .venv de una carpeta de edición (Scripts\ en Windows, bin/ en macOS y Linux).
py_venv() { if [ -x "$1/herramientas/.venv/Scripts/python.exe" ]; then echo "$1/herramientas/.venv/Scripts/python.exe"; else echo "$1/herramientas/.venv/bin/python"; fi; }

# autor = la cuenta de gh está en AUTORES o tiene permiso de escritura en el repo (dueña o colaboradora invitada).
modo() {
  local login push
  login="$(gh api user -q .login 2>/dev/null | limpia || true)"
  [ -n "$login" ] || { echo local; return; }
  if limpia < "$SKILL/AUTORES" | grep -qx "$login"; then echo autor; return; fi
  push="$(gh api "repos/$GH_REPO" -q .permissions.push 2>/dev/null | limpia || true)"
  if [ "$push" = true ]; then echo autor; else echo local; fi
}

sha() { if command -v sha256sum >/dev/null 2>&1; then sha256sum "$1" | cut -d' ' -f1; else shasum -a 256 "$1" | cut -d' ' -f1; fi; }
nombre_asset() { echo "${1:0:16}.mp4"; }   # el asset se llama por su hash: sin espacios ni rutas

# Vídeos de referencia estándar. DE MOMENTO SOLO EN LOCAL (no hay Release): la skill trae las fichas JSON y el
# CONTEXTO.md, que es lo que hace falta para editar. Cuando el autor los publique (publicar.sh), VIDEOS.txt tendrá líneas
# y esto los bajará. Baja (o repara) los que falten o no cuadren, y quita los que ya no están en la lista.
bajar_refs() {
  local h ruta destino tmp faltan=0 linea
  if [ ! -s "$LISTA" ]; then echo "Referencias estándar: fichas y CONTEXTO.md incluidos; los vídeos aún no están publicados (no hacen falta para editar)."; return 0; fi
  command -v gh >/dev/null 2>&1 || { echo "⚠️  Sin gh no puedo bajar los vídeos de referencia (opcional)."; return 0; }
  while IFS= read -r linea; do
    linea="$(printf '%s' "$linea" | limpia)"; [ -z "$linea" ] && continue
    h="${linea%%  *}"; ruta="${linea#*  }"; destino="$SKILL/base/refs/$ruta"
    if [ -f "$destino" ] && [ "$(sha "$destino")" = "$h" ]; then continue; fi
    faltan=$((faltan+1)); mkdir -p "$(dirname "$destino")"
    tmp="$(mktemp -d)"
    echo "  ↓ $ruta"
    gh release download "$RELEASE" -R "$GH_REPO" -p "$(nombre_asset "$h")" -D "$tmp" --clobber || { echo "⚠️  No se pudo bajar $ruta"; rm -rf "$tmp"; continue; }
    [ "$(sha "$tmp/$(nombre_asset "$h")")" = "$h" ] || { echo "Hash distinto en $ruta"; rm -rf "$tmp"; return 1; }
    mv "$tmp/$(nombre_asset "$h")" "$destino"; rm -rf "$tmp"
  done < "$LISTA"
  echo "Referencias estándar: al día ($faltan bajadas)."
}

# Archivos de la plantilla que se sincronizan (nunca: personal/ —con los recursos de cada creador—, refs/, out/, bruto*, marca.ts).
archivos_plantilla() {
  (cd "$SKILL/plantilla" && find . -type f ! -name .DS_Store ! -name .gitkeep | sed 's|^\./||' |
    grep -v -E '^(personal|refs|out|bruto|bruto terminado)/' | grep -v -x 'estudio/src/comun/marca.ts' | grep -v -x 'estudio/src/Root.tsx' | LC_ALL=C sort)
}
MANIFIESTO_REL=".claude/$NOMBRE-plantilla.sha256"   # hash de cada archivo tal como lo dejó la plantilla

# Skills de terceros (SKILLS.txt) que falten en ~/.claude/skills o en la carpeta → `npx skills add` global.
skills_que_faltan() {   # imprime "<repo> <skill…>" por cada repo con alguna que falte
  local carpeta="${1:-}" repo nombres falta n
  limpia < "$SKILL/SKILLS.txt" | grep -v -E '^\s*(#|$)' | while read -r repo nombres; do
    falta=""
    for n in $nombres; do
      [ -e "$HOME/.claude/skills/$n" ] || { [ -n "$carpeta" ] && [ -e "$carpeta/.claude/skills/$n" ]; } || falta="$falta $n"
    done
    [ -z "$falta" ] || echo "$repo$falta"
  done
  return 0
}
instalar_skills() {
  local repo resto
  command -v npx >/dev/null 2>&1 || { echo "⚠️  Sin node/npx: no puedo instalar las skills de SKILLS.txt."; return 0; }
  skills_que_faltan "${1:-}" | while read -r repo resto; do
    echo "  ↓ $repo: $resto"
    # shellcheck disable=SC2086
    npx -y skills add "$repo" -g -a claude-code -s $resto -y </dev/null >/dev/null 2>&1 \
      || echo "⚠️  No se pudieron instalar ($repo): npx -y skills add $repo -g -a claude-code -s $resto -y"
  done
  echo "Skills de apoyo: al día."
}

# ── Programas: se instala solo lo que falte (lo usan instalar.sh y actualizar.sh) ──
# Imprescindibles: ffmpeg/ffprobe, node/npx, python. Recomendados: yt-dlp (bajar referencias), gh (modo autor y vídeos de
# referencia), mpv (comprobar el color sin QuickTime en Windows/Linux).
programas_que_faltan() {
  local c
  for c in ffmpeg ffprobe node npx; do command -v "$c" >/dev/null 2>&1 || printf '%s ' "$c"; done
  py_sistema >/dev/null || printf 'python '
}
recomendados_que_faltan() {
  local c
  for c in yt-dlp gh; do command -v "$c" >/dev/null 2>&1 || printf '%s ' "$c"; done
  if [ "$(uname)" != Darwin ] && ! command -v mpv >/dev/null 2>&1 && [ ! -x "/c/Program Files/MPV Player/mpv.exe" ]; then printf 'mpv '; fi
}
# Windows: tras instalar con winget, el PATH nuevo está en el registro pero no en esta terminal → se relee.
refrescar_path() {
  es_windows || return 0
  local p d extra=""
  p="$(powershell.exe -NoProfile -Command '[Environment]::GetEnvironmentVariable("Path","Machine")+";"+[Environment]::GetEnvironmentVariable("Path","User")' 2>/dev/null | limpia)"
  local IFS=';'
  for d in $p; do [ -n "$d" ] && extra="$extra:$(cygpath -u "$d" 2>/dev/null)"; done
  for d in "$LOCALAPPDATA/Microsoft/WinGet/Links" "/c/Program Files/nodejs" "/c/Program Files/MPV Player" "/c/Program Files/GitHub CLI"; do
    extra="$extra:$(cygpath -u "$d" 2>/dev/null)"; done
  PATH="$PATH$extra"; export PATH
}
paquete() {   # nombre del paquete de un programa: paquete <programa> winget|brew
  case "$2:$1" in
    winget:ffmpeg|winget:ffprobe) echo Gyan.FFmpeg;; winget:node|winget:npx) echo OpenJS.NodeJS.LTS;; winget:python) echo Python.Python.3.12;;
    winget:yt-dlp) echo yt-dlp.yt-dlp;; winget:gh) echo GitHub.cli;; winget:mpv) echo shinchiro.mpv;;
    brew:ffprobe) echo ffmpeg;; brew:npx) echo node;; brew:*) echo "$1";;
  esac
}
instalar_programas() {
  local falta rec pk c
  falta="$(programas_que_faltan)"; rec="$(recomendados_que_faltan)"
  if [ -z "$falta$rec" ]; then echo "Programas: al día."; return 0; fi
  [ -n "$falta" ] && echo "  Faltan (imprescindibles): $falta"
  [ -n "$rec" ] && echo "  Faltan (recomendados): $rec"
  if es_windows; then
    command -v winget >/dev/null 2>&1 || { echo "  Falta winget (Instalador de aplicaciones de Microsoft Store). Instálalo y vuelve a lanzar."; return 1; }
    pk="$(for c in $falta $rec; do paquete "$c" winget; done | sort -u | tr '
' ' ')"
    for c in $pk; do
      echo "  → winget install $c"
      winget install -e --id "$c" --silent --accept-package-agreements --accept-source-agreements </dev/null >/dev/null 2>&1         || echo "  ⚠️  winget no pudo instalar $c (lánzalo tú: winget install -e --id $c)"
    done
    refrescar_path
    falta="$(programas_que_faltan)"
    [ -z "$falta" ] && { echo "Programas: al día."; return 0; }
    echo "  Siguen faltando: $falta. Cierra y abre la terminal (para que coja el PATH nuevo) y vuelve a lanzar."; return 1
  fi
  if ! command -v brew >/dev/null 2>&1; then
    echo "  → Homebrew (te pedirá la contraseña del Mac)"
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" || { echo "No se pudo instalar Homebrew: https://brew.sh"; return 1; }
    [ -x /opt/homebrew/bin/brew ] && eval "$(/opt/homebrew/bin/brew shellenv)"
    [ -x /usr/local/bin/brew ] && eval "$(/usr/local/bin/brew shellenv)"
  fi
  pk="$(for c in $falta $rec; do paquete "$c" brew; done | sort -u | tr '\n' ' ')"
  # shellcheck disable=SC2086
  brew install $pk || { echo "⚠️  brew install $pk falló."; return 1; }
  echo "Programas: al día."
}

instalar_pesados() {      # .venv de Python y node_modules (solo lo que falte). Los modelos de voz se bajan solos al primer uso.
  local dest="$1" py pv
  pv="$(py_venv "$dest")"
  if [ ! -x "$pv" ]; then
    py="$(py_sistema)" || { echo "⚠️  No hay Python 3.10 o superior."; return 1; }
    echo "  → Python (.venv)"; "$py" -m venv "$dest/herramientas/.venv" || return 1
    pv="$(py_venv "$dest")"
    # Con gráfica NVIDIA (Windows/Linux), torch con CUDA: transcribir y alinear van ~10 veces más rápido.
    if [ "$(uname)" != Darwin ] && command -v nvidia-smi >/dev/null 2>&1; then
      "$pv" -m pip install -q torch torchaudio --index-url https://download.pytorch.org/whl/cu126 || echo "⚠️  torch con CUDA no se instaló; irá por CPU."
    fi
    "$pv" -m pip install -q -r "$dest/herramientas/requirements.txt" || { echo "⚠️  pip install falló."; return 1; }
  fi
  [ -d "$dest/estudio/node_modules" ] || { echo "  → Remotion (npm)"; (cd "$dest/estudio" && npm ci --no-audit --no-fund) || return 1; }
  # el navegador con el que Remotion renderiza las capas (si no, se bajaría en el primer render)
  (cd "$dest/estudio" && npx --no-install remotion browser ensure >/dev/null 2>&1) || echo "  ⚠️  No se pudo preparar el navegador de Remotion (se bajará solo en el primer render)."
  echo "Python y Remotion: al día. (La primera transcripción baja el modelo de Whisper, ~1,6 GB, y la primera alineación el de MMS, ~1,2 GB.)"
}

# Enlace de la skill dentro de la carpeta de edición: enlace simbólico en macOS/Linux, «junction» en Windows.
enlazar_skill() {
  local dest="$1" enlace="$1/.claude/skills/$NOMBRE"
  mkdir -p "$dest/.claude/skills"
  [ -e "$enlace" ] && return 0
  if es_windows; then cmd //c mklink //J "$(cygpath -w "$enlace")" "$(cygpath -w "$SKILL")" >/dev/null || { echo "⚠️  No se pudo crear el enlace a la skill."; return 1; }
  else ln -s "$SKILL" "$enlace"; fi
}

# Clave de ElevenLabs: OPCIONAL. Se pregunta una vez al instalar (Intro = saltar). Nunca se imprime.
pedir_clave_elevenlabs() {
  local dest="$1" clave
  [ -f "$dest/estudio/.env.local" ] && return 0
  [ -t 0 ] || { echo "  (Clave de ElevenLabs: opcional, sin preguntar porque no hay terminal.)"; return 0; }
  echo
  echo "  Clave de ElevenLabs (OPCIONAL). Con ella: transcripción Scribe, voz en off con IA, aislar voz y efectos generados."
  echo "  Sin ella todo funciona en local (Whisper + alineación forzada)."
  printf "  Pégala y pulsa Intro (o solo Intro para saltar): "
  read -r -s clave || clave=""; echo
  if [ -n "$clave" ]; then
    umask 077; printf 'ELEVENLABS_API_KEY=%s\n' "$clave" > "$dest/estudio/.env.local"; echo "  ✓ Guardada en estudio/.env.local"
  else echo "  Saltada. Puedes añadirla cuando quieras (Claude te ayuda)."; fi
}

# ── Creadores que vienen con la skill (creadores/<nombre>/): su personalización ya hecha ──
# creadores/<n>/personal/ → personal/<n>/   ·   creadores/<n>/estudio/ → estudio/   (nunca pisa nada que exista)
# Su recursos/ (y los vídeos y fotogramas pesados de refs/) NO van en git: están en un disco duro, en
# <disco>/Horizontal/personal/<n>/. recursos/ se enlaza al disco; lo pesado de refs/ se copia.
creadores_incluidos() { (cd "$SKILL/creadores" 2>/dev/null && for d in */; do [ -d "$d/personal" ] && echo "${d%/}"; done) || true; }
buscar_disco() {   # imprime la carpeta <disco>/Horizontal/personal/<n> que tenga recursos/
  local n="$1" c
  if es_windows; then   # en Git Bash las unidades (/c, /d…) no salen en un glob de /: se prueban letra a letra
    for c in d e f g h i j k l m n o p q r s t u v w x y z c; do [ -d "/$c/Horizontal/personal/$n/recursos" ] && { echo "/$c/Horizontal/personal/$n"; return 0; }; done
  else for c in /Volumes/*/Horizontal/personal/"$n" /media/*/*/Horizontal/personal/"$n" /mnt/*/Horizontal/personal/"$n"; do [ -d "$c/recursos" ] && { echo "$c"; return 0; }; done; fi
  return 1
}
instalar_creador() {
  local dest="$1" n="$2" src="$SKILL/creadores/$2" f d disco enlace
  [ -d "$src/personal" ] || { echo "No hay creador «$n» en la skill (hay: $(creadores_incluidos | tr '
' ' '))."; return 1; }
  (cd "$src" && find personal estudio -type f 2>/dev/null) | while IFS= read -r f; do
    case "$f" in personal/*) d="$dest/personal/$n/${f#personal/}";; *) d="$dest/$f";; esac
    [ -e "$d" ] && continue; mkdir -p "$(dirname "$d")"; cp -p "$src/$f" "$d"
  done
  echo "  ✓ personal/$n/ (perfil, preferencias, recursos.md, marca, ajustes, fichas de refs) y sus gráficos de estudio/"
  conectar_disco "$dest" "$n"
}
conectar_disco() {   # enlaza personal/<n>/recursos al disco y copia lo pesado de refs/ que falte
  local dest="$1" n="$2" disco enlace="$1/personal/$2/recursos"
  disco="$(buscar_disco "$n")" || { echo "  ⚠️  No encuentro el disco con Horizontal/personal/$n/recursos. Conéctalo y lanza: bash .claude/skills/$NOMBRE/conectar_disco.sh $n"; return 0; }
  if [ -L "$enlace" ] || { es_windows && [ -d "$enlace" ] && fsutil reparsepoint query "$(cygpath -w "$enlace")" >/dev/null 2>&1; }; then
    rm -f "$enlace" 2>/dev/null || cmd //c rmdir "$(cygpath -w "$enlace")" >/dev/null
  elif [ -d "$enlace" ]; then
    if [ -n "$(ls -A "$enlace" 2>/dev/null | grep -v -E '^(INDICE\.md|\.gitkeep)$' || true)" ]; then
      echo "  ⚠️  personal/$n/recursos/ ya tiene archivos: no lo enlazo al disco ($disco/recursos). Muévelos tú y vuelve a lanzar."; return 0
    fi
    rm -rf "$enlace"
  fi
  mkdir -p "$(dirname "$enlace")"
  if es_windows; then cmd //c mklink //J "$(cygpath -w "$enlace")" "$(cygpath -w "$disco/recursos")" >/dev/null
  else ln -s "$disco/recursos" "$enlace"; fi
  echo "  ✓ personal/$n/recursos → $disco/recursos"
  if ! ( : > "$disco/recursos/.prueba_escritura" ) 2>/dev/null; then
    echo "  ⚠️  El disco es de SOLO LECTURA en este ordenador (en Mac pasa con discos NTFS): se pueden usar sus recursos, pero"
    echo "     no guardar nada nuevo en él (clips de archivo, música, INDICE.md). Para escribir: formatearlo en exFAT o un driver NTFS."
  else rm -f "$disco/recursos/.prueba_escritura"; fi
  if [ -d "$disco/refs" ]; then
    (cd "$disco/refs" && find . -type f | sed 's|^\./||') | while IFS= read -r f; do
      [ -e "$dest/personal/$n/refs/$f" ] && continue; mkdir -p "$(dirname "$dest/personal/$n/refs/$f")"; cp -p "$disco/refs/$f" "$dest/personal/$n/refs/$f"
    done
    echo "  ✓ personal/$n/refs: vídeos y fotogramas copiados del disco"
  fi
}
