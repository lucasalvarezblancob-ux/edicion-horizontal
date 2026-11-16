# edicion-reels — instalación

Skill de edición de **reels verticales** con el estándar de Lucas. Al instalarla se crea una **carpeta de edición**
(bruto, refs, recursos, out, estudio Remotion, herramientas) en tu ordenador.

| Viene con la skill (estándar, igual para todos) | Es tuyo (local, no sale de tu ordenador) |
|---|---|
| Reglas: `base/preferencias.md`, `ganchos.md`, `descripciones.md` | `personal/perfil.md` y `personal/preferencias.md` (mandan sobre el estándar) |
| Referencias estándar: `base/refs/<tipo>/` (vídeos + `CONTEXTO.md`) — **el mínimo, no se quitan** | `refs/<tipo>/`: añade o quita las tuyas |
| Código de edits de ejemplo: `base/ejemplos/` | `estudio/src/videos/`: tus edits |
| Herramientas y componentes (`plantilla/`) | `estudio/src/comun/marca.ts`: color, fuentes, @, código |
| — | `recursos/`: tu material (la skill **no** trae recursos) |

**Solo Lucas cambia el estándar.** En cualquier otra instalación la skill es de solo lectura: Claude apunta tus
correcciones en tu carpeta (y un hook le impide editar la skill). `modo.sh` dice si eres `autor` o `local`.

## Instalar

**Sin acceso al repo de Publiqo**: la skill tiene una copia pública en
[publiqo-edicion](https://github.com/lucasalvarezblancob-ux/publiqo-edicion). Su instalador de un solo comando (macOS)
deja la carpeta de edición en `~/Desktop/Reels` y se actualiza sola. En esa copia los vídeos de referencia se bajan de
Instagram cuando se puede; si no, se edita igual con los `CONTEXTO.md`.

**Con acceso al repo de Publiqo**: necesitas: macOS, acceso de lectura a `publiqo-agency/skills` (pídeselo a Lucas), `gh` con sesión, Homebrew.

```sh
git clone https://github.com/publiqo-agency/skills.git ~/Projects/skills   # si no lo tienes
~/Projects/skills/edicion-reels/instalar.sh "$HOME/Documents/edicion-reels"
```

Instala **solo lo que falte** (Homebrew, `gh`, `ffmpeg`, `whisper.cpp`, `yt-dlp`, `node`, `python`; lo que ya tengas no lo toca), crea la carpeta, enlaza la skill en su
`.claude/skills/`, baja las referencias estándar (~600 MB, del Release `edicion-reels-refs`), el modelo Whisper
(465 MB), la `.venv` de Python, `node_modules`, `it-reelsmaker` y las skills de apoyo que falten (Remotion,
HyperFrames, `media-use`: lista en `SKILLS.txt`, globales en `~/.claude/skills`). Luego abre Claude Code en la
carpeta y te ayuda a rellenar `personal/perfil.md` y `marca.ts` (el color por defecto es amarillo-lima `#E6EC52`).

Al final pregunta tu clave de ElevenLabs, **opcional** (Intro para saltar): con ella los subtítulos de los vídeos
hablando a cámara salen más precisos y puedes usar voz en off con IA; sin ella todo funciona en local.
`actualizar.sh` repone lo que falte (programas, skills, modelo, `.venv`, `node_modules`). Opcional: app **Edits** de Meta (la entrega estándar exporta desde Edits).

¿Ya tienes una carpeta de edición? `instalar.sh --adoptar "<ruta>"` añade lo que falte sin pisar nada.

## Actualizar

```sh
.claude/skills/edicion-reels/actualizar.sh      # desde la carpeta de edición
```

`git pull` del repo, referencias estándar nuevas (y repone las que falten), y herramientas/componentes nuevos **solo
si no los has tocado** (los que sí, te los lista). No toca `personal/`, `refs/`, `recursos/`, `out/` ni `marca.ts`.

## Autor (Lucas)

`publicar.sh "edicion-reels: <qué y por qué>"`: sube los vídeos nuevos de `base/refs/` al Release, regenera
`base/refs/VIDEOS.txt`, commit de `edicion-reels/` y push a `main`. Mejoras generales de herramientas o componentes
de tu carpeta: cópialas antes a `plantilla/` (sin tus datos).
