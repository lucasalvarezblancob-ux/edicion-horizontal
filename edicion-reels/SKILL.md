---
name: edicion-reels
description: Edición de reels verticales (9:16) de fitness/lifestyle en Remotion, con el estándar de Lucas (lucaselatleta) — voz en off (IA o propia), hablando a cámara con ganchos de texto animados, transiciones, posing, montajes de vida, subtítulos palabra a palabra, guiones, música y descripciones. Úsala SIEMPRE que pidan editar un vídeo de bruto/, hacer un reel, escribir un guion o gancho, generar la voz, poner subtítulos o transiciones, corregir un edit, añadir referencias o recursos, escribir la descripción, o "que aprendas" de una corrección; también para instalarla o crear la carpeta de edición ("instala la skill de reels", "monta la carpeta de edición"). No para vídeo horizontal (otra skill).
---

# Edición de reels

Reels verticales 9:16 (1080×1920, o 2160×3840 si algún bruto es 4K — ver preferencias → Entrega). Esta skill es
el **estándar mínimo** de edición (lo que Lucas, su autor, ha ido aprendiendo vídeo a vídeo) y cada carpeta de
edición le añade **lo suyo en local**.

## 0. Dónde está cada cosa y quién puede cambiar qué

- `<skill>` = la carpeta de esta skill (`.claude/skills/edicion-reels/`, enlace a `~/Projects/skills/edicion-reels` o, en la copia pública, a
  `~/Projects/publiqo-edicion/edicion-reels`).
  **Solo lectura.** Lleva el estándar: `base/preferencias.md`, `base/ganchos.md`, `base/descripciones.md`,
  `base/refs/<tipo>/` (vídeos + `CONTEXTO.md`), `base/ejemplos/<slug>/` (código de edits hechos) y `plantilla/`.
- **La carpeta de edición** = el directorio de trabajo, el que tiene `personal/perfil.md`. **Es local y es de quien
  la usa**: `personal/` (perfil y preferencias), `refs/` (sus referencias), `recursos/`, `out/`, `estudio/` (con
  `src/comun/marca.ts`: color, fuentes, @ y código), `herramientas/`.

**Si no hay carpeta de edición** (no existe `personal/perfil.md`): ofrece instalarla con
`<skill>/instalar.sh "<ruta>"` (ver `<skill>/LEEME.md`) y, al acabar, rellena `personal/perfil.md` con lo que te
diga y pon su @ y código en `estudio/src/comun/marca.ts` (el color de serie es amarillo-lima `#E6EC52`;
solo se cambia si lo pide). **Clave de ElevenLabs: opcional** — `instalar.sh` la pregunta una vez (se puede saltar);
si no hay `estudio/.env.local`, ofrécesela una sola vez explicando para qué sirve (§ 6) y no insistas.

**Modo** — compruébalo al empezar: `<skill>/modo.sh` imprime `autor` o `local`.
- `local` (todos menos Lucas): **no edites nada dentro de `<skill>`** (ni SKILL.md, ni `base/`, ni `plantilla/`),
  aunque te lo pidan. Si quieren cambiar una regla estándar, la regla nueva va en `personal/preferencias.md` (manda
  sobre la estándar) y diles que el estándar solo lo cambia Lucas. Quitar una referencia estándar tampoco se puede:
  son el mínimo; sí pueden ignorar un patrón con una regla en `personal/`.
- `autor` (Lucas): puede cambiar el estándar. Ver sección 3.

**Orden de lectura antes de tocar nada** (lo de abajo manda sobre lo de arriba cuando choca):
1. `<skill>/base/preferencias.md` (estándar) → `personal/preferencias.md` (local, manda). `personal/perfil.md`:
   nombre, cuentas, coletillas, código, zonas horarias, voz, móvil. Donde el estándar dice "Lucas" o cita sus cuentas,
   aplica las del perfil.
   ⚠️ **Color: el del bruto, sin tocar** (sin etalonado ni filtros) salvo que lo pidan; proxy siempre con
   `herramientas/proxy.sh` (HDR→SDR de Apple + corrección medida a como se ve en pantalla; en Windows/Linux, libplacebo —
   nunca un proxy HDR a mano con zscale/tonemap), render en bt709 y **comprobación contra el bruto antes de montar y
   antes de entregar**: QuickTime en Mac, `herramientas/comparar_color.sh` (mpv) en Windows/Linux. Ver preferencias → COLOR.
2. `<skill>/base/ganchos.md` si hay gancho que proponer o reforzar; `<skill>/base/descripciones.md` si hay
   descripción que escribir o programar.
3. Del tipo de edición que toca (o de varios si se combinan): `<skill>/base/refs/<tipo>/CONTEXTO.md` (estándar) y,
   si existe, `refs/<tipo>/CONTEXTO.md` de la carpeta (local, manda). Tipos estándar:
   - `voice en off` — guion + voz en off (IA estilo Blair, o la voz propia) sobre el bruto.
   - `transiciones edit` — gancho de texto escrito + transiciones entre planos.
   - `hablando a camara` — habla a cámara en primera persona: gancho de texto animado palabra a palabra, zoom de entrada con sonido, dinamismo sobre plano fijo.
   - `posing` — posados estilo David Laid: sin texto ni voz, tomas largas, música slowed + reverb; brutos horizontales a todo el ancho con bordes negros.
   - `montaje de vida` — montaje rápido de momentos de vida sobre un audio de discurso motivacional, con la frase en pantalla; cortes secos, clips de `recursos/`.
   - Un tipo nuevo local = una carpeta en `refs/` con su `CONTEXTO.md`.
4. `recursos/INDICE.md` (material propio con tiempos útiles) y `out/REGISTRO.md` (vídeos hechos: reutilizar
   estructura/código, no repetir ganchos).

Si el tipo no está claro, pregunta solo eso. Si en `refs/<tipo>/` (local) hay vídeos que no aparecen en
"Referencias analizadas" de su `CONTEXTO.md`, **analízalos primero** (sección 4). Si `<skill>/comprobar.sh` (lo lanza
el hook al abrir la sesión) avisa de que faltan referencias estándar, ejecuta `<skill>/actualizar.sh` antes de editar.

## 1. Estructura de la carpeta de edición (no la cambies sin preguntar)

```
<carpeta>/
├── personal/     perfil.md + preferencias.md (lo de quien edita; manda sobre el estándar)
├── bruto/        entrada: vídeos en bruto pendientes de editar
├── bruto terminado/  brutos ya editados que NO son clips de entreno (para repasos)
├── refs/<tipo>/  referencias LOCALES + CONTEXTO.md (las estándar están en <skill>/base/refs/)
├── recursos/     material propio por temas + INDICE.md (cómo clasificar: <skill>/base/recursos.md; las carpetas de serie son de fitness: gym/<zona>/, running/, competicion/, aire-libre/, lifestyle/, recuperacion/, fotos/, sonidos/)
├── out/          vídeos terminados (AAAA-MM-DD_slug.mp4) + REGISTRO.md
├── estudio/      proyecto Remotion
│   ├── src/comun/marca.ts    color de acento, crema, fuentes, HANDLE y CODIGO (local)
│   ├── src/comun/            componentes reutilizables (Subtitulos, Titulo, Clave, Rotulos, NombrePegatina, hablando)
│   ├── src/videos/<slug>/    composición de cada vídeo + guion.json + voz-palabras.json
│   ├── public/<slug>/        proxy.mp4, voz.mp3, musica.mp3 de cada vídeo; public/sonidos/ = SFX estándar
│   ├── scripts/voz.mjs       voz IA con ElevenLabs (solo si la piden; clave en estudio/.env.local, no la imprimas)
│   └── src/Root.tsx          registra cada composición
└── herramientas/ scripts de análisis/audio, .venv de Python y modelos/ggml-small.bin (Whisper)
```

Python: usa siempre `herramientas/.venv/bin/python` (si falta: `python3 -m venv herramientas/.venv && herramientas/.venv/bin/pip install -r herramientas/requirements.txt`).

## 2. Flujo de un vídeo

1. **Analiza el bruto** (`bruto/…`): `ffprobe` (duración, fps, orientación — los del iPhone vienen HEVC 4K 60 fps girados; los de la Sony ZV-E10 II (`C####.MP4`, 4K 25 fps SDR) son 3840×2160 con rotación ±90° → se ven verticales: mira `stream_side_data=rotation` antes de suponer que son horizontales), `herramientas/hoja_contactos.sh` cada 1–2 s y luego más fino donde haya acción, `herramientas/transcribir.sh` para saber qué dice. Si habla a cámara: tiempos por palabra con **Scribe** (`estudio/scripts/transcribir-scribe.mjs`, preciso; necesita clave de ElevenLabs, ver § 6: si no hay, Whisper local con `transcribir.sh` y afina los cortes con la energía del audio) y jump cuts con `herramientas/cortar_pausas.py` (ver `refs/hablando a camara/CONTEXTO.md` → Flujo técnico). Identifica ángulos, reps, planos útiles (intro, cara a cámara para el cierre…). **Si hay ruido de fondo o varias personas**: `scripts/aislar-voz.mjs` + `herramientas/mezclar_voces.py` (ver `refs/hablando a camara/CONTEXTO.md` → Flujo técnico, punto 10).
   Decide qué técnicas tienen sentido para ESTE bruto (tabla de criterio en el CONTEXTO del tipo) antes de montar.
2. **Puntos de corte**: en ejercicios, `herramientas/puntos_movimiento.py VIDEO INI FIN` da las paradas (arriba/abajo de cada rep). Confírmalas con hoja de contactos a 4 fps. Corta siempre en los extremos del movimiento (match cut entre ángulos).
3. **Guion** (si lleva voz en off): sigue la plantilla del `CONTEXTO.md` de voice en off. El gancho normalmente lo da el creador — **úsalo literal**. Enséñale el guion si lo ha pedido revisar; si no, sigue.
4. **Voz**:
   - **Voz del creador (lo normal)**: me manda su audio → `herramientas/transcribir.sh AUDIO salida` (o Scribe si hay clave) para tiempos por palabra, y quita silencios igual (el script corta por energía, no se come letras). Procesado mínimo: ver `refs/voice en off/CONTEXTO.md` → variante A.
   - **Voz IA (solo si la pide)**: si quiere la voz generada en vez de grabarla él. Necesita su clave de ElevenLabs: si `estudio/.env.local` no existe, pídesela, créalo desde `.env.local.example` y no la imprimas. Luego `cd estudio && node --env-file=.env.local scripts/voz.mjs src/videos/<slug>/guion.json public/<slug>/voz-original` → luego `herramientas/.venv/bin/python herramientas/apretar_voz.py public/<slug>/voz-original.mp3 public/<slug>/voz-original-palabras.json public/<slug>/voz.mp3 src/videos/<slug>/voz-palabras.json 1.25`.
   - Para cambiar solo una frase: genera esa frase con `PREV="frase anterior"` y empálmala en un silencio real (mide la energía; nunca cortes encima de una consonante).
5. **Montaje en Remotion**: crea `src/videos/<slug>/` copiando la estructura de un edit parecido: los de esta carpeta (`estudio/src/videos/`) o los ejemplos de la skill (`<skill>/base/ejemplos/<slug>/`, p. ej. `jalon-espalda-dorito/` para voz en off) (Series de planos con `name` descriptivo, `Shot` con punch-in + drift, whips, subtítulos, claves, audio). Registra en `Root.tsx`. Proxy del bruto con **`herramientas/proxy.sh BRUTO proxy.mp4`** (1440×2560; **si el bruto es 4K: `proxy.sh BRUTO proxy.mp4 2160`** → 2160×3840; `<Video style={{width:"100%",height:"100%"}}>`; ver preferencias → COLOR). Los planos se ajustan a la voz: cada frase cae sobre el plano que la ilustra.
6. **Comprueba antes de renderizar**: fotogramas de cada corte (último antes / primero después) en una hoja → la posición debe casar; stills de 6–8 momentos con textos. Revisa que ningún texto tape la cara ni caiga en las zonas de UI (y 0–220 y 1500–1920).
7. **Render** (⛔ **si en el bruto alguien dicta, antes `herramientas/verificar_hablante.py`**: el apuntador no puede oírse nunca; ver `refs/hablando a camara/CONTEXTO.md` → 8b. ⛔ **Con voz real cortada por tomas, antes `revisar_cortes.py` y `revisar_finales.py`, sin dejar ningún aviso sin resolver**: la última palabra de cada toma se oye entera, ver punto 2 del mismo CONTEXTO): `cd estudio && npx remotion render <Comp> ../out/AAAA-MM-DD_<slug>.mp4 --codec h264` (+ **`--scale=2` si algún bruto es 4K** → sale 2160×3840; resolución = la del mejor clip, ver preferencias → Entrega). Si hay variantes para comparar, renderízalas con sufijo y, cuando elija, deja solo la elegida en `out/`.
   **Renders largos o en 4K → por tramos para ir liberando RAM** (estándar desde 2026-11-15): `herramientas/render_por_tramos.sh <Comp> ../out/AAAA-MM-DD_<slug>.mp4 --scale=2` — cada tramo dura ~4 min de render (`MINUTOS=4`) y es un proceso nuevo que suelta toda su memoria al acabar; el audio va en una pasada aparte y los tramos se unen sin recodificar (misma imagen y fluidez que un render de una vez, ~5–10 % más de tiempo por arrancar Chrome en cada tramo). `sudo purge` no se usa: pide contraseña.
   **Después del render, comprueba que el color se ha mantenido (obligatorio, no se entrega sin esto)**: bruto y render abiertos en **QuickTime** en el mismo instante, capturas de pantalla y comparación de zonas fijas (techo, suelo, pared) en 3–4 momentos; diferencia media ≤ 5 niveles. **En Windows/Linux (sin QuickTime): mpv** con `herramientas/comparar_color.sh` (bruto vs proxy en 4 instantes antes de montar; el render, en un instante sin textos o por zonas fijas). Fotogramas sacados con ffmpeg **no** valen (no aplican la gestión de color de Apple). Si no cuadra, revisa el proxy (preferencias → COLOR) y vuelve a renderizar. Al entregar, di el resultado (p. ej. "color comprobado en QuickTime: dif. media 3 niveles").
   **Después, el paso por Edits (obligatorio en todo ordenador que tenga Edits; estándar desde 2026-11-17)**: si existe
   `/Applications/Edits.app` (la app Edits de Meta; en Windows/Linux no existe y el paso se salta, dilo al entregar), el
   render pasa por Edits **sin que haga falta pedirlo**: se importa, se le hace el cambio invisible (PNG transparente
   encima; la música comercial, desde Edits) y se exporta (cómo, paso a paso: preferencias → Entrega). **El archivo de
   `out/` es el de Edits**: el export comprobado (misma resolución, fps, duración ±1 fotograma, color y sonoridad que el
   render) se copia como `out/AAAA-MM-DD_<slug>.mp4`, el nombre normal, que es el que se sube y se programa; el render
   de Remotion se queda como `out/AAAA-MM-DD_<slug>_sin-edits.mp4` solo hasta que quien edita confirme que no hay más
   retoques (paso 9: entonces se borra con lo descargado) y el proyecto de Edits se borra al acabar. Edits toma la
   pantalla: **avisa en una línea antes** (si quien edita ha pedido trabajar sin preguntas, no esperes respuesta). Si
   Edits falla, se entrega el render de Remotion y se dice que falta el paso por Edits. Por qué: Lucas, «para que
   cualquier persona que se descargue la skill y tenga Edits en el ordenador, al acabar de renderizar el vídeo se le
   pase por Edits y en el out ya tenga el vídeo pasado por Edits» (Instagram da más alcance a lo hecho con Edits).
8. **Cierre**: al acabar el edit, mueve cada bruto de `bruto/` con nombre descriptivo (`AAAA-MM-DD_que-se-ve.ext`): **los clips que sirvan de b-roll a su carpeta de `recursos/`** con su ficha (`base/recursos.md`; en fitness, los ejercicios a `recursos/gym/<zona muscular>/`, cada clip a su zona, y posados/espejo a `gym/fisico/`; crea la carpeta si no existe) y el resto a **`bruto terminado/`** renombrados con **el vídeo final al que pertenecen**: `AAAA-MM-DD_<slug-del-edit>_<nn>-<que-se-ve>.ext` (mismo `<slug>` que `out/AAAA-MM-DD_<slug>.mp4`; `nn` = orden en el montaje, 01, 02…), p. ej. `2026-11-01_prenda-fav-gymshark_01-intro.MOV`, `…_02-susie.MOV`. Así, cuando un edit usa varios brutos, se sabe de qué vídeo final es cada uno. Apúntalo en `recursos/INDICE.md` (sección "gym" o "bruto terminado", con sus tiempos útiles), actualiza la ruta en el comentario de la composición y apunta el vídeo en `out/REGISTRO.md`. Para repasos o correcciones de un vídeo ya hecho, el bruto está en `bruto terminado/` (el proxy sigue en `estudio/public/<slug>/`).
9. **Descargas del vídeo**: si bajaste material solo para este vídeo (clips de películas, memes, canciones de YouTube…), al acabar pregunta "¿Hemos acabado o quieres un retoque más?" y, si ha acabado, "¿Borro lo descargado para este vídeo?" con la lista (ver preferencias → Entrega). En esa lista va también el `out/AAAA-MM-DD_<slug>_sin-edits.mp4` (el render antes de Edits), si lo hay.
10. **Limpieza automática (estándar desde 2026-11-03)**: a los **30 días** del render de un edit en `out/` se borra sola **la carpeta entera `estudio/public/<slug>/`** (proxies, clips, voz, música, audio de la ref, LUTs…) para liberar espacio. **Si se borra el render de `out/`, la regla es la misma**: los 30 días cuentan desde que el script ve por primera vez que ya no está (fecha en `herramientas/limpieza-estado.json`), y pasado ese plazo se borra aunque no exista en `out/`. Se salta el edit si se ha tocado algo suyo en los últimos 30 días. Lo hace `herramientas/limpiar_renders.py`, lanzado por el hook `SessionStart` de `.claude/settings.json` al abrir cada sesión. Lo borrado queda en `herramientas/limpieza.log`; si el hook avisa de que ha borrado algo, avísalo en una línea. Para ver qué borraría: `python3 -I herramientas/limpiar_renders.py --simular`. **Nunca se borra** (ni este script ni a mano): `recursos/` (sus clips grabados de gym, running, competición…), `bruto terminado/`, `refs/`, la skill y lo aprendido (`personal/`, los `CONTEXTO.md`), el código de cada edit (`estudio/src/videos/<slug>/`, sirve de plantilla) y los renders de `out/` (esos solo los borra el creador). **Para retocar un edit limpiado** hay que rehacer `public/<slug>/`: proxies con `herramientas/proxy.sh` desde `recursos/` o `bruto terminado/` (rutas en el comentario de la composición), y la voz, música o audio que hagan falta.

Remotion: carga la skill `remotion-best-practices` antes de escribir código. Studio: `cd estudio && npx remotion studio`.

## 3. Aprender de las correcciones (obligatorio)

Cada vez que corrigen algo ("esto no", "más rápido", "no uses rosa", "la voz tiene que ser de hombre"…):
1. Arréglalo en el vídeo.
2. **Apúntalo en el mismo turno**, según el modo:
   - **`local`** — todo en la carpeta, nunca en `<skill>`:
     - Regla que vale para cualquier vídeo → `personal/preferencias.md`.
     - Regla de un tipo (guion, voz, gancho, transición) → `refs/<tipo>/CONTEXTO.md` (créalo si no existe), sección "Correcciones".
     - Descripciones → `personal/preferencias.md` → "Entrega y publicación".
     - Color, fuentes, @, código → `estudio/src/comun/marca.ts`.
   - **`autor`** (Lucas) — decide dónde va:
     - **Regla de estilo que debería tener todo el mundo** → el estándar: `<skill>/base/preferencias.md`, `<skill>/base/refs/<tipo>/CONTEXTO.md`, `ganchos.md` o `descripciones.md`.
     - **Dato o gusto solo suyo** (su marca, sus cuentas, su físico, su código, sus colaboraciones) → `personal/` o `marca.ts`, igual que en local.
     - Si no está claro, pregúntale en una línea: "¿estándar para todos o solo tuyo?".
     - Cambios en el estándar → commit y push en el mismo turno (`<skill>/publicar.sh "edicion-reels: <qué y por qué>"`, ver sección 7).
   - Formato: `- AAAA-MM-DD — <regla en imperativo>. Por qué: <lo que dijo / el motivo>. (vídeo: <slug>)`
3. Si una corrección contradice una regla anterior del mismo archivo, **sustituye** la vieja (no acumules contradicciones) y anota la fecha. Si contradice una regla estándar en modo local, la local la tapa: no hace falta tocar la estándar.
4. Cuando algo funcione a la primera y lo aprueben ("dejamos este"), apúntalo también como "lo que funciona".
5. Si una decisión es de gusto y no hay regla, ofrece 2 variantes rápidas en vez de adivinar (ej.: dos cierres renderizados).

## 4. Analizar referencias (cuando añaden vídeos a refs/)

Las referencias nuevas van a `refs/<tipo>/` de la carpeta (local). En modo `autor`, si Lucas dice que una referencia es
para el estándar, va a `<skill>/base/refs/<tipo>/` y se publica con `<skill>/publicar.sh` (sube los vídeos nuevos).

Por cada vídeo nuevo: transcripción con tiempos (`herramientas/transcribir.sh`), cortes (`ffmpeg -vf "select='gt(scene,0.28)',showinfo"`), los 3 primeros segundos fotograma a fotograma (cada 0,25 s) y el resto con hojas de contactos cada ~1 s. Extrae: gancho literal + texto en pantalla, estructura por bloques con tiempos, chistes/coletillas literales, CTA, ritmo (s/plano), tipo de planos, estilo de texto/subtítulos, música, voz (IA o real; para IA compara con `herramientas/comparar_voces.py` generando el mismo texto). Resúmelo en el `CONTEXTO.md` del tipo (tabla de referencias analizadas + patrones). Con muchos vídeos, reparte el análisis en subagentes en paralelo.

## 5. Recursos

**Guía completa en `<skill>/base/recursos.md`** (léela antes de catalogar o elegir recursos): cómo crear las
carpetas para cualquier nicho, cómo nombrar los archivos, cómo analizar un clip (hojas de contactos, tiempos finos,
transcripción, puntos de movimiento), la ficha de `recursos/INDICE.md` (qué se ve, **tramos útiles, outfit, vibe y
temas**), cómo elegir los fotogramas buenos y cómo elegir recursos para un vídeo.
Cuando el creador suba material a `recursos/` (o lo deje en `bruto/` diciendo que son recursos) o se use uno en un
edit: analízalo y apúntalo en el índice. Al meterlos en un vídeo, cada clip casa con **lo que se dice en ese
momento** y con **el outfit, los colores y el vibe del resto** (preferencias → Recursos). Antes de pedir material
nuevo, busca en el índice. Si no hay nada que sirva (o `recursos/` está vacío), clips libres de Pexels con
`herramientas/pexels.py` (preferencias → Recursos, 2026-11-16); lo del creador va primero cuando casa.

## 6. Otras skills y servicios

Las instala `instalar.sh` y `actualizar.sh` repone cualquier cosa que falte (programas, skills, it-reelsmaker, modelo Whisper, `.venv`, `node_modules`); lo que ya esté instalado no se toca. Lista en `<skill>/SKILLS.txt`: globales en
`~/.claude/skills`, con `npx skills add`.
- `remotion-best-practices` (+ `remotion-captions`, `remotion-render`, `remotion-multimedia`…): siempre que se escriba código Remotion.
- `it-reelsmaker` (en `.claude/skills/` de la carpeta): técnicas probadas para reels a cámara (talking head): cortar pausas y retomas, cámara virtual, subtítulos palabra a palabra, masterizado −14 LUFS, checklist. Úsala como **caja de herramientas y criterio**, pero respeta nuestra estructura de carpetas y las preferencias (si pide `brands/` o configuración propia, guárdala en `estudio/reelsmaker/`).
- `hyperframes` = la antigua **Embedded Captions**: subtítulos "detrás del sujeto" y tarjetas sobre metraje a cámara (versiones nuevas: `references/captions.md` → "Text behind the speaker"; antiguas: `references/routes/embedded-captions.md`); `hyperframes-registry`: animaciones de texto y bloques listos (transiciones, títulos) si el gancho o la transición lo piden.
- `media-use`: SFX/BGM/imágenes (la música del catálogo necesita `heygen` CLI con sesión iniciada; si no, `herramientas/synth_music.py` o `herramientas/slowed-reverb.sh` con una canción suya).
- Para mirar vídeos (brutos, referencias, recursos) no hace falta ninguna skill: `herramientas/hoja_contactos.sh`, `ffprobe`/`ffmpeg`, `transcribir.sh` (Whisper local) y `puntos_movimiento.py`.
- **ElevenLabs: opcional.** `instalar.sh` pregunta la clave una vez y se puede saltar. Es imprescindible solo para **voz en off generada con IA** (lo normal es que la voz sea un audio suyo): si la pide y no hay clave, pídesela y guárdala en `estudio/.env.local` (desde `.env.local.example`; no la abras ni la imprimas; `npx -y @elevenlabs/cli@latest onboard check --env-path .env.local` la verifica). Con la clave también van Scribe (tiempos por palabra precisos), aislar voz, SFX y música generados. Sin clave: Whisper local para tiempos, los SFX de `estudio/public/sonidos/`, música con `synth_music.py` o una canción suya, y para el ruido `highpass`/`afftdn` de ffmpeg.
- **Pexels: opcional.** `PEXELS_API_KEY` en `estudio/.env.local` (gratis en pexels.com/api) hace que `herramientas/pexels.py` busque y baje clips verticales sin navegador. Sin clave, el método del navegador (preferencias → Recursos).

## 7. Instalar, actualizar, publicar

- `<skill>/instalar.sh "<ruta>"` — crea la carpeta de edición desde `plantilla/` (sin recursos), enlaza la skill,
  baja las referencias estándar, el modelo Whisper, la `.venv` y `node_modules`. Detalle en `<skill>/LEEME.md`.
- `<skill>/actualizar.sh` — `git pull` del repo de skills + referencias estándar que falten + archivos de
  `plantilla/` (herramientas, componentes) que no se hayan tocado en local. **Nunca pisa** `personal/`, `refs/`,
  `recursos/`, `out/`, `marca.ts` ni nada cambiado en local (lo lista).
- `<skill>/publicar.sh "<mensaje>"` — **solo modo autor**: sube los vídeos nuevos de `base/refs/` al Release,
  hace commit de `edicion-reels/` y push a `main`. Si Lucas mejora un componente o herramienta de su carpeta de forma
  general, cópialo antes a `<skill>/plantilla/` (sin sus datos: `marca.ts` y `personal/` nunca van).
- **Copia pública** (`lucasalvarezblancob-ux/publiqo-edicion`, instalada con su instalador de un comando): espejo del
  original, que sigue en `publiqo-agency/skills`. Cada commit de Lucas que toque `edicion-reels/` se copia allí solo
  como versión nueva, y cada instalación se pone al día sola al abrir Claude Code. En la copia, `modo.sh` dice siempre
  `local` y `publicar.sh` no publica. Los vídeos de referencia no van en la copia: se bajan de Instagram si se puede
  y, si no, se edita igual con los `CONTEXTO.md`.
