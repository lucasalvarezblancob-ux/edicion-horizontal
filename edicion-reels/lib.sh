# Funciones comunes de edicion-reels (se carga con `source`).
SKILL="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
REPO_DIR="$(cd "$SKILL/.." && pwd -P)"
# La skill vive en dos repos. El ORIGINAL es publiqo-agency/skills (privado): ahí la cambia Lucas. La COPIA PÚBLICA es
# lucasalvarezblancob-ux/publiqo-edicion: un espejo que se publica solo en cada commit que toque edicion-reels/ (hook
# post-commit del ordenador de Lucas → espejo_reels.sh de ese repo) y que se actualiza sola al abrir Claude Code.
# En la copia pública la skill es siempre de solo lectura y los vídeos de referencia no se redistribuyen (bajar_refs).
GH_REPO="publiqo-agency/skills"; PUBLICA=0
case "$(git -C "$REPO_DIR" remote get-url origin 2>/dev/null)" in
  *lucasalvarezblancob-ux/publiqo-edicion*) GH_REPO="lucasalvarezblancob-ux/publiqo-edicion"; PUBLICA=1;;
esac
RELEASE="edicion-reels-refs"
LISTA="$SKILL/base/refs/VIDEOS.txt"   # "<sha256>  <ruta relativa a base/refs>"

modo() {
  local login
  [ "$PUBLICA" = 1 ] && { echo local; return; }   # copia pública: el estándar se cambia en el original
  login="$(gh api user -q .login 2>/dev/null || true)"
  if [ -n "$login" ] && grep -qx "$login" "$SKILL/AUTORES"; then echo autor; else echo local; fi
}

sha() { shasum -a 256 "$1" | cut -d' ' -f1; }
nombre_asset() { echo "${1:0:16}.mp4"; }   # el asset se llama por su hash: sin espacios ni rutas

# Baja (o repara) los vídeos estándar que falten o no cuadren, y quita los que ya no están en la lista.
bajar_refs() {
  local h ruta destino tmp faltan=0
  [ -f "$LISTA" ] || { echo "Falta $LISTA"; return 1; }
  [ "$PUBLICA" = 1 ] && { bajar_refs_instagram; return 0; }
  while IFS= read -r linea; do
    [ -z "$linea" ] && continue
    h="${linea%%  *}"; ruta="${linea#*  }"; destino="$SKILL/base/refs/$ruta"
    if [ -f "$destino" ] && [ "$(sha "$destino")" = "$h" ]; then continue; fi
    faltan=$((faltan+1)); mkdir -p "$(dirname "$destino")"
    tmp="$(mktemp -d)"
    echo "  ↓ $ruta"
    gh release download "$RELEASE" -R "$GH_REPO" -p "$(nombre_asset "$h")" -D "$tmp" --clobber
    [ "$(sha "$tmp/$(nombre_asset "$h")")" = "$h" ] || { echo "Hash distinto en $ruta"; rm -rf "$tmp"; return 1; }
    mv "$tmp/$(nombre_asset "$h")" "$destino"; rm -rf "$tmp"
  done < "$LISTA"
  # vídeos que sobran (Lucas los quitó del estándar)
  (cd "$SKILL/base/refs" && find . -type f \( -iname '*.mp4' -o -iname '*.mov' -o -iname '*.m4v' -o -iname '*.mp3' \) | sed 's|^\./||') |
  while IFS= read -r ruta; do
    grep -qF "  $ruta" "$LISTA" || { echo "  ✕ $ruta (ya no es estándar)"; rm -f "$SKILL/base/refs/$ruta"; }
  done
  echo "Referencias estándar: al día ($faltan bajadas)."
}

# Copia pública: los vídeos de referencia (casi todos reels de otros creadores) no se publican. Se intentan bajar del
# propio Instagram con yt-dlp (el nombre del archivo acaba en el código de 11 caracteres del reel). Son OPCIONALES: la
# skill edita igual con los CONTEXTO.md, que ya traen el análisis de cada referencia.
bajar_refs_instagram() {
  local linea ruta destino base cod tmp bajadas=0 fallan=0
  command -v yt-dlp >/dev/null || { echo "Referencias: sin yt-dlp no bajo los vídeos (opcionales: se edita con los CONTEXTO.md)."; return 0; }
  while IFS= read -r linea; do
    [ -z "$linea" ] && continue
    ruta="${linea#*  }"; destino="$SKILL/base/refs/$ruta"
    [ -f "$destino" ] && continue
    base="$(basename "$ruta")"; base="${base%.*}"; cod="${base: -11}"
    mkdir -p "$(dirname "$destino")"; tmp="$(mktemp -d)"
    if yt-dlp -q --no-warnings --no-playlist --merge-output-format mp4 -o "$tmp/v.%(ext)s" \
         "https://www.instagram.com/reel/$cod/" </dev/null >/dev/null 2>&1 && [ -f "$tmp/v.mp4" ]; then
      mv "$tmp/v.mp4" "$destino"; echo "  ↓ $ruta"; bajadas=$((bajadas+1))
    else fallan=$((fallan+1)); fi
    rm -rf "$tmp"
  done < "$LISTA"
  if [ "$fallan" -gt 0 ]; then echo "Referencias: $bajadas bajadas de Instagram; $fallan no disponibles (no hacen falta: se edita con los CONTEXTO.md)."
  else echo "Referencias: al día ($bajadas bajadas de Instagram)."; fi
  return 0
}

# Archivos de la plantilla que se sincronizan (nunca: personal/, refs/, recursos/, out/, bruto*, marca.ts).
archivos_plantilla() {
  (cd "$SKILL/plantilla" && find . -type f ! -name .DS_Store ! -name .gitkeep | sed 's|^\./||' |
    grep -v -E '^(personal|refs|recursos|out|bruto|bruto terminado)/' | grep -v -x 'estudio/src/comun/marca.ts' | sort)
}
MANIFIESTO_REL=".claude/edicion-reels-plantilla.sha256"   # hash de cada archivo tal como lo dejó la plantilla

# Copia pública: al abrir sesión (hook comprobar.sh) se pone al día sola. sincronizar.sh trae la versión nueva del repo
# (como mucho cada 6 h) y, si cambió desde la última vez en esta carpeta, se actualiza la plantilla sin pisar lo tocado.
# Para que no se actualice sola: crear <carpeta>/.claude/edicion-reels-sin-auto.
auto_actualizar() {
  local dest="$1" marca="$1/.claude/edicion-reels-commit" ahora hecho
  [ "$PUBLICA" = 1 ] || return 0
  [ -f "$dest/personal/perfil.md" ] && [ ! -e "$dest/.claude/edicion-reels-sin-auto" ] || return 0
  [ -f "$REPO_DIR/sincronizar.sh" ] && bash "$REPO_DIR/sincronizar.sh"
  ahora="$(git -C "$REPO_DIR" rev-parse HEAD 2>/dev/null)" || return 0
  hecho="$(cat "$marca" 2>/dev/null || true)"
  [ "$ahora" = "$hecho" ] && return 0
  if [ -n "$hecho" ]; then
    EDICION_REELS_SIN_PULL=1 EDICION_REELS_RAPIDO=1 bash "$SKILL/actualizar.sh" "$dest" 2>&1 |
      grep -E '^  (\+|↻|·)|dependencias|versión nueva de estos' || true
  fi
  echo "$ahora" > "$marca"
}

# Skills de terceros (SKILLS.txt) que falten en ~/.claude/skills o en la carpeta → `npx skills add` global.
skills_que_faltan() {   # imprime "<repo> <skill…>" por cada repo con alguna que falte
  local carpeta="${1:-}" repo nombres falta n
  grep -v -E '^\s*(#|$)' "$SKILL/SKILLS.txt" | while read -r repo nombres; do
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
  command -v npx >/dev/null || { echo "⚠️  Sin node/npx: no puedo instalar las skills de SKILLS.txt."; return 0; }
  skills_que_faltan "${1:-}" | while read -r repo resto; do
    echo "  ↓ $repo: $resto"
    # shellcheck disable=SC2086
    npx -y skills add "$repo" -g -a claude-code -s $resto -y </dev/null >/dev/null 2>&1 \
      || echo "⚠️  No se pudieron instalar ($repo): npx -y skills add $repo -g -a claude-code -s $resto -y"
  done
  echo "Skills de apoyo: al día."
}

# ── Programas, skills y piezas pesadas: se instala solo lo que falte (lo usan instalar.sh y actualizar.sh) ──
PROGRAMAS="gh ffmpeg ffprobe whisper-cli yt-dlp node npx python3"
programas_que_faltan() { local c; for c in $PROGRAMAS; do command -v "$c" >/dev/null || printf '%s ' "$c"; done; }
instalar_programas() {
  local falta pk=() c
  falta="$(programas_que_faltan)"
  if [ -n "$falta" ]; then
    echo "  Faltan: $falta"
    if ! command -v brew >/dev/null; then
      echo "  → Homebrew (te pedirá la contraseña del Mac)"
      /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" || { echo "No se pudo instalar Homebrew: https://brew.sh"; return 1; }
      [ -x /opt/homebrew/bin/brew ] && eval "$(/opt/homebrew/bin/brew shellenv)"
      [ -x /usr/local/bin/brew ] && eval "$(/usr/local/bin/brew shellenv)"
    fi
    for c in $falta; do case $c in whisper-cli) pk+=(whisper.cpp);; python3) pk+=(python);; ffprobe) pk+=(ffmpeg);; npx) pk+=(node);; *) pk+=("$c");; esac; done
    # shellcheck disable=SC2207
    pk=($(printf '%s\n' "${pk[@]}" | sort -u))
    brew install "${pk[@]}" || { echo "⚠️  brew install ${pk[*]} falló."; return 1; }
  fi
  if [ "$PUBLICA" = 0 ] && ! gh auth status >/dev/null 2>&1; then
    if [ -t 0 ]; then echo "  → Inicia sesión en GitHub"; gh auth login || return 1
    else echo "Falta iniciar sesión en GitHub: gh auth login"; return 1; fi
  fi
  echo "Programas: al día."
}

instalar_reelsmaker() {   # skill it-reelsmaker dentro de la carpeta de edición
  local dest="$1" tmp
  [ -e "$dest/.claude/skills/it-reelsmaker" ] && return 0
  tmp="$(mktemp -d)"; mkdir -p "$dest/.claude/skills"
  if git clone -q --depth 1 https://github.com/itpartypattaya/reels-montage "$tmp/r" 2>/dev/null; then
    cp -R "$tmp/r/plugins/it-reelsmaker/skills/it-reelsmaker" "$dest/.claude/skills/it-reelsmaker" && echo "  ↓ it-reelsmaker"
  else echo "⚠️  No se pudo bajar it-reelsmaker."; fi
  rm -rf "$tmp"
}

instalar_pesados() {      # modelo Whisper, .venv de Python y node_modules (solo lo que falte)
  local dest="$1" m="$1/herramientas/modelos/ggml-small.bin"
  mkdir -p "$(dirname "$m")"
  [ -f "$m" ] || { echo "  ↓ Modelo Whisper (465 MB)"; curl -fL --progress-bar -o "$m" https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.bin; }
  if [ ! -x "$dest/herramientas/.venv/bin/python" ]; then
    echo "  → Python (.venv)"; python3 -m venv "$dest/herramientas/.venv" &&
    "$dest/herramientas/.venv/bin/pip" install -q -r "$dest/herramientas/requirements.txt"
  fi
  [ -d "$dest/estudio/node_modules" ] || { echo "  → Remotion (npm)"; (cd "$dest/estudio" && npm ci --no-audit --no-fund); }
  echo "Modelo, Python y Remotion: al día."
}

# Clave de ElevenLabs: OPCIONAL. Se pregunta una vez al instalar (Intro = saltar). Nunca se imprime.
pedir_clave_elevenlabs() {
  local dest="$1" clave
  [ -f "$dest/estudio/.env.local" ] && return 0
  [ -t 0 ] || { echo "  (Clave de ElevenLabs: opcional, sin preguntar porque no hay terminal.)"; return 0; }
  echo
  echo "  Clave de ElevenLabs (OPCIONAL). Con ella: subtítulos palabra a palabra más precisos en vídeos hablando a"
  echo "  cámara (Scribe), voz en off con IA, aislar voz y efectos/música generados. Sin ella todo funciona en local."
  printf "  Pégala y pulsa Intro (o solo Intro para saltar): "
  read -r -s clave || clave=""; echo
  if [ -n "$clave" ]; then
    umask 077; printf 'ELEVENLABS_API_KEY=%s\n' "$clave" > "$dest/estudio/.env.local"; echo "  ✓ Guardada en estudio/.env.local"
  else echo "  Saltada. Puedes añadirla cuando quieras (Claude te ayuda)."; fi
}
