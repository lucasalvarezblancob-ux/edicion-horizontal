# Publiqo Edición

Skills de edición de vídeo de Publiqo para Claude Code. Un solo repositorio: al instalarlo se instalan **todas** las skills
que contiene, y las que se vayan añadiendo después **se instalan y se actualizan solas**.

| Skill | Qué hace |
|---|---|
| [`edicion-horizontal`](edicion-horizontal/) | Edición de vídeo horizontal 16:9 para YouTube a partir de brutos largos: montaje, dinamismo, recursos, intro, rótulos, mapas, música, render 4K y el paquete de YouTube (títulos, miniaturas, descripción). Trae ya hecho el perfil de Reino Selva. |

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
automática y crea la carpeta de edición de vídeo en `~/Desktop/Horizontal` con todo lo que necesita para renderizar.

**Reino Selva** (con su disco duro conectado), para que quede ya su perfil y sus recursos enlazados:

```sh
# Mac
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/lucasalvarezblancob-ux/publiqo-edicion/main/instalar-mac.sh)" _ --creador reinoselva
```
```powershell
# Windows
& ([scriptblock]::Create((irm https://raw.githubusercontent.com/lucasalvarezblancob-ux/publiqo-edicion/main/instalar.ps1))) -Creador reinoselva
```

Luego: `cd ~/Desktop/Horizontal && claude` y pedirle el vídeo.

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
| `sincronizar.sh` | lo lanza el hook al abrir Claude Code: trae la versión nueva y enlaza las skills nuevas |

Se puede publicar desde cualquier ordenador con una cuenta de `AUTORES` o colaboradora del repo: `publicar.sh` junta
antes lo que se haya publicado desde otro ordenador.
