# Publiqo Edición

Skills de edición de vídeo de Publiqo para Claude Code. Un solo repositorio: al instalarlo se instalan **todas** las skills
que contiene, y las que se vayan añadiendo después **se instalan y se actualizan solas**.

| Skill | Qué hace |
|---|---|
| [`edicion-horizontal`](edicion-horizontal/) | Edición de vídeo horizontal 16:9 para YouTube a partir de brutos largos: montaje, dinamismo, recursos, intro, rótulos, mapas, música, render 4K y el paquete de YouTube (títulos, miniaturas, descripción). Trae ya hecho el perfil de Reino Selva. |
| [`edicion-reels`](edicion-reels/) | Edición de reels verticales 9:16 en Remotion: voz en off (propia o con IA), hablando a cámara con ganchos de texto, transiciones, posing, montajes de vida, subtítulos palabra a palabra, guiones, música y descripciones. **Solo macOS.** Es una copia de la skill de Publiqo que se actualiza sola (ver «Para el autor»). |

Es público para descargar; **solo el autor sube cambios**. Funciona en **macOS y Windows**.

## Instalar (un solo comando)

**Mac**, en Terminal:

```sh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/lucasalvarezblancob-ux/publiqo-edicion/main/instalar-mac.sh)"
```

**Windows**, en PowerShell:

```powershell
irm https://raw.githubusercontent.com/lucasalvarezblancob-ux/publiqo-edicion/main/instalar.ps1 | iex
```

Instala lo que falte (Homebrew o winget, Git, ffmpeg, Node, Python, yt-dlp, GitHub CLI, Claude Code), descarga el
repo en `~/Projects/publiqo-edicion`, enlaza todas las skills en `~/.claude/skills`, deja puesta la actualización
automática y crea las carpetas de edición con todo lo que necesitan para renderizar: `~/Desktop/Horizontal` (vídeo
horizontal) y, en Mac, `~/Desktop/Reels` (reels verticales). En Windows solo se crea la horizontal.

**Reino Selva** (con su disco duro conectado), para que quede ya su perfil y sus recursos enlazados:

```sh
# Mac
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/lucasalvarezblancob-ux/publiqo-edicion/main/instalar-mac.sh)" _ --creador reinoselva
```
```powershell
# Windows
& ([scriptblock]::Create((irm https://raw.githubusercontent.com/lucasalvarezblancob-ux/publiqo-edicion/main/instalar.ps1))) -Creador reinoselva
```

Luego: `cd ~/Desktop/Horizontal && claude` (o `cd ~/Desktop/Reels && claude`) y pedirle el vídeo.

¿Ya lo tenías instalado de antes? La skill de reels te llega sola. Para crear su carpeta, en Terminal:
`bash ~/Projects/publiqo-edicion/edicion-reels/instalar.sh ~/Desktop/Reels`

En `edicion-reels`, los vídeos de referencia no van en este repo (casi todos son reels de otros creadores). El
instalador los baja de Instagram cuando puede. Si no puede, se edita igual: el análisis de cada referencia está en los
`CONTEXTO.md` de la skill.

## Actualizaciones

Al abrir Claude Code (como mucho cada 6 h) se mira si hay versión nueva y, si la hay, se pone al día sola: las skills,
las skills nuevas (quedan instaladas) y, en la carpeta de edición, las herramientas y el perfil del creador que haya
cambiado el autor. Cada publicación es una versión (`v2.0`, `v2.1`…) en
[Releases](https://github.com/lucasalvarezblancob-ux/publiqo-edicion/releases).

## Para el autor

| | |
|---|---|
| `publicar.sh "<qué cambió>"` | publica todo como versión nueva (`--mayor` para saltar de versión mayor) |
| `publicar.sh --versiones` | lista las versiones |
| `publicar.sh --volver v2.1` | rollback para todos (se publica como versión nueva; no se borra historial) |
| skill nueva | una carpeta con su `SKILL.md`; al publicar, a todos se les instala sola. Con un archivo `.solo-carpeta` no se enlaza global (se instala en su carpeta de trabajo, como `edicion-horizontal`) |
| `publicar.sh --solo <skill> "<qué cambió>"` | versión nueva con solo esa carpeta; lo demás que haya sin publicar se queda como está |
| `espejo_reels.sh` | copia `edicion-reels` desde `~/Projects/skills` y la publica; lo lanza solo el hook `post-commit` |
| `sincronizar.sh` | lo lanza el hook al abrir Claude Code: trae la versión nueva y enlaza las skills nuevas (de las que se usan desde su carpeta, avisa una vez) |

**`edicion-reels` no se edita aquí.** Su original está en el repo de skills de Publiqo (`publiqo-agency/skills`,
`~/Projects/skills/edicion-reels`), que sigue funcionando igual que siempre. Cada commit que toque `edicion-reels/`
allí se copia aquí y se publica como versión nueva, sin hacer nada. Lo hace el hook `post-commit` de
`~/Projects/skills`, que deja puesto `espejo_reels.sh --instalar-hook`, y deja un log en `.git/espejo-reels.log`. Si
falla, sale un aviso de macOS. Si hiciste commits de `edicion-reels` desde otro ordenador, `espejo_reels.sh` los pone
al día a mano (sin cambios no publica nada). En esta copia la skill es siempre de solo lectura (`modo.sh` → `local`).

Se puede publicar desde cualquier ordenador con una cuenta de `AUTORES` o colaboradora del repo: `publicar.sh` junta
antes lo que se haya publicado desde otro ordenador.
