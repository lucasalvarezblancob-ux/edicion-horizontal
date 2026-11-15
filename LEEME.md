# edicion-horizontal — instalación

Skill de edición de **vídeo horizontal 16:9 para YouTube** (vlogs, viajes, retos, visitas). Al instalarla se crea una
**carpeta de edición** en tu ordenador. Hermana de `edicion-reels` (vertical).

La skill son **las bases** de edición y efectos; lo tuyo va en una **carpeta de personalización** local:

| Bases (vienen con la skill, iguales para todos) | Personalización (tuya, local, no sale de tu ordenador) |
|---|---|
| Reglas: `base/preferencias.md`, `intros.md`, `recursos.md`, `titulos-miniaturas.md`, `descripciones.md` | `personal/<creador>/perfil.md`, `personal/<creador>/preferencias.md` (mandan sobre las bases) |
| Referencias medidas: `base/refs/<tipo>/` (fichas + `CONTEXTO.md`) | `refs/<tipo>/`: tus referencias y tus correcciones por tipo |
| Números de la base (zooms, efectos, música): `plantilla/herramientas/montaje/` | `personal/<creador>/ajustes.py`: esos números, a tu gusto |
| Gráficos de serie: `plantilla/estudio/src/comun/`; botones de YouTube: `plantilla/estudio/public/botones/` | `personal/<creador>/marca.json` (color, canal, @), fuentes en `estudio/src/comun/marca.ts`, gráficos propios en `estudio/src/personal/<creador>/` |
| Código de un edit de ejemplo: `base/ejemplos/ramon/` | `out/<slug>/`: tus montajes |
| — | `personal/<creador>/recursos/`: **todo tu material** (tu intro, tu outro, tu logo, tu mascota; tus clips de archivo y b-roll por temas; tus fotos, mapas y música) + `recursos.md` (cuándo va cada uno) |

`personal/` se crea al instalar, **no está en git** y ninguna actualización la toca. Dentro hay una carpeta **por
creador** (`personal/<creador>/`; lo normal es uno): se crea con `herramientas/montaje/nuevo_creador.py <nombre>`. Para personalizar no hace falta
editar archivos: díselo a Claude («los zooms más suaves», «mi color es el naranja», «pon siempre mi cabecera») y lo
apunta donde toca. Qué es cada archivo: `personal/LEEME.md`.

**Solo Lucas cambia las bases.** El repositorio es público (cualquiera lo descarga) pero solo pueden subir cambios
la cuenta dueña (`lucasalvarezblancob-ux`) y las cuentas que invite como colaboradoras. En cualquier otra instalación la
skill es de solo lectura (un hook impide que Claude la edite). `modo.sh` dice si eres `autor` o `local`.

## Instalar

### Windows (un solo comando)

En **PowerShell** (no hace falta ser administrador):

```powershell
irm https://raw.githubusercontent.com/lucasalvarezblancob-ux/edicion-horizontal/main/instalar.ps1 | iex
```

Instala **todo lo que falte** para editar y renderizar: Git, ffmpeg completo (con libplacebo, para HDR del iPhone),
Node LTS, Python 3.12, yt-dlp, GitHub CLI, mpv y Claude Code; descarga la skill en `~\Projects\edicion-horizontal`
y crea la carpeta de edición en `~\Desktop\Horizontal` con las skills de apoyo (Remotion, HyperFrames, media-use),
la `.venv` de Python (con PyTorch para tu gráfica si hay NVIDIA), `node_modules` y el navegador de render de Remotion.
Lo que ya tengas instalado no se toca. Varios GB y un buen rato la primera vez.

Con opciones (otra carpeta, o un creador que viene con la skill):

```powershell
& ([scriptblock]::Create((irm https://raw.githubusercontent.com/lucasalvarezblancob-ux/edicion-horizontal/main/instalar.ps1))) -Carpeta "$HOME\Desktop\Horizontal" -Creador reinoselva
```

### macOS (un solo comando)

En **Terminal**:

```sh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/lucasalvarezblancob-ux/edicion-horizontal/main/instalar-mac.sh)"
```

Instala Homebrew si falta (te pide la contraseña del Mac) y con él git, ffmpeg, node, python, yt-dlp y gh; Claude Code
si falta; descarga la skill en `~/Projects/edicion-horizontal` y crea la carpeta de edición en `~/Desktop/Horizontal`
con todo lo demás, igual que en Windows. Con creador u otra carpeta, añade al final `_ --creador reinoselva` (y/o
`--carpeta "<ruta>"`).

### Opciones de `instalar.sh`
- `--creador <n>`: deja ya hecha la personalización de un creador que viene con la skill (`creadores/<n>/`) y enlaza sus
  recursos a su disco duro (ver abajo).
- `--adoptar "<ruta>"`: para una carpeta que ya usas; solo añade lo que falte, no pisa nada.
- `--ligero`: sin skills de apoyo, `.venv` ni `node_modules` (para probar la estructura).
- **ElevenLabs es opcional**: pregunta la clave una vez y se puede saltar.
- Los modelos de voz (Whisper ~1,6 GB, MMS ~1,2 GB) se bajan solos en la primera transcripción.

Luego abre Claude Code en la carpeta (`cd "<ruta>"; claude`) y pídele el primer vídeo. Si no viene tu creador con la
skill, la primera vez te preguntará lo del perfil (`personal/<creador>/perfil.md`) y tu canal y color (`marca.json`).

## Creadores que vienen con la skill

| Creador | Qué trae | Dónde están sus recursos |
|---|---|---|
| `reinoselva` (Reino Selva / RayWild) | perfil, preferencias, recursos.md, marca (ES y EN), ajustes, fichas de sus vídeos (`refs/`), sus gráficos propios (la tortuga, logos) | su disco duro externo: `<disco>\Horizontal\personal
einoselva
ecursos` (archivo de especies, intro, outro, música…) y `…
efs` (sus vídeos y fotogramas) |

Para **Reino Selva**: conecta su disco duro y lanza el instalador con su creador:

```sh
# Mac (Terminal)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/lucasalvarezblancob-ux/edicion-horizontal/main/instalar-mac.sh)" _ --creador reinoselva
```
```powershell
# Windows (PowerShell)
& ([scriptblock]::Create((irm https://raw.githubusercontent.com/lucasalvarezblancob-ux/edicion-horizontal/main/instalar.ps1))) -Creador reinoselva
```

Queda `personal/reinoselva/` con todo, y `personal/reinoselva/recursos` enlazado al disco (en Mac lo busca en
`/Volumes/<disco>/Horizontal/…`; en Windows, en cualquier letra). Si el disco no estaba conectado al instalar o cambia de
letra: `bash .claude/skills/edicion-horizontal/conectar_disco.sh reinoselva` desde la carpeta de edición. Al abrir
Claude Code se avisa si el disco no está conectado.

> El disco de Reino Selva está en **NTFS**: en Mac se lee pero **no se puede escribir** en él (sus recursos se usan
> igual; lo que no se puede es guardar en el disco clips nuevos, música o el `INDICE.md`). Para escribir desde Mac hay
> que pasarlo a **exFAT** (vale para Mac y Windows; hay que vaciarlo antes) o instalar un driver NTFS para Mac.

## Usar

1. Deja los brutos de un vídeo en `bruto/<nombre-del-video>/`.
2. «Edita el vídeo de `bruto/<nombre>`» (di de qué va y cualquier cosa que quieras: duración, tono, qué no puede faltar).
3. Claude estudia los brutos, te enseña la escaleta, monta, comprueba y deja el vídeo en `out/`, con el paquete de
   YouTube: 5 títulos con su prompt de miniatura (para ChatGPT) y su fotograma de referencia, descripción y capítulos. Cada corrección que le hagas se queda apuntada para los siguientes vídeos.

La música la pones tú (tu banco, tu licencia) en `personal/<creador>/recursos/musica/`. Claude no sube nada a ningún sitio.

## Actualizar

```sh
bash .claude/skills/edicion-horizontal/actualizar.sh      # desde tu carpeta de edición (hace git pull de la skill)
```
Pone al día las herramientas y los gráficos de serie que no hayas tocado. **Nunca pisa** `personal/` (con tus recursos), `refs/`,
`out/`, `marca.ts`, tus gráficos propios ni nada que hayas cambiado (te lo lista).

## Qué hace cada script de la skill

| Script | Para qué |
|---|---|
| `instalar.sh` | crear (o adoptar) una carpeta de edición |
| `actualizar.sh` | poner al día herramientas y gráficos de serie |
| `comprobar.sh` | avisos al abrir la sesión (lo lanza un hook): programas, perfil sin rellenar, limpieza a 30 días |
| `proteger.sh` | hook que impide editar la skill si no eres el autor |
| `modo.sh` | imprime `autor` o `local` |
| `conectar_disco.sh` | enlazar los recursos de un creador a su disco duro |
| `instalar.ps1` / `instalar-mac.sh` | instalador de un solo comando para Windows / macOS (programas + skill + carpeta) |
| `publicar.sh` | solo el autor: commit y push al repo |

## Estado de las pruebas (2026-11-12)

- Probado en **Windows 11** (Git Bash, ffmpeg 8.1, Node 24, Python 3.14, RTX 4060): un vídeo de 16 min en 4K completo.
- **macOS: escrito pero sin probar** (rutas `.venv/bin`, `avconvert` para HDR, `videotoolbox`, Homebrew).
- Brutos **HDR de iPhone**: probado en un edit real en Windows (`1311`, 15 clips HLG 4K 60 fps) con `sdr.py`; `proxy.sh` y macOS, solo con material sintético.
- Tipo `estudio` (a cámara en interior): sin referencias todavía.
