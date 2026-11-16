# Posing — contexto

> **Estándar de `edicion-reels`** (mínimo que toda instalación tiene; solo lo cambia Lucas, autor de la skill). Los vídeos de esta tabla están junto a este archivo, en la skill. "Lucas" = el creador que edita; usa tus datos de `personal/perfil.md`. Las rutas `estudio/src/videos/<slug>/` de los edits citados están en la skill como `base/ejemplos/<slug>/` (código, sin media); las de `recursos/` son material de Lucas que no viene con la skill. Tus referencias y correcciones de este tipo van en `refs/<tipo>/CONTEXTO.md` de tu carpeta y mandan sobre esto.

Tipo de edit: **posados / posing (solo o en grupo) estilo David Laid**: sin voz, sin texto, solo música "slowed + reverb" y la imagen.

## Referencias analizadas
| Archivo | Duración | Texto en pantalla | Cortes | Notas |
|---|---|---|---|---|
| `davidlaid_CvTZbdNO_cz.mp4` (IG CvTZbdNO_cz) | 23,4 s | ninguno | 0 (una sola toma) | David + chica en un plató negro con foco cenital, plano entero vertical, cámara casi fija. Poses: relajado → frente → brazos detrás de la cabeza (abdominales) hasta el final. Canción con voz, lenta y con mucha reverb. |
| `davidlaid_Cwnt7-_pcZU.mp4` (IG Cwnt7-_pcZU) | 33,3 s | ninguno | 1 (a los 14,1 s) | Grupo posando en el gym, cámara en mano grabando entre cuerpos desenfocados en primer plano, tonos cálidos. Horizontal girado 90° → **eso NO lo quiere Lucas** (ver correcciones). Canción slowed + reverb. |

## Patrones
- **Nada de texto, subtítulos ni SFX.** Solo música + imagen. La gracia es el físico y la atmósfera.
- ~~Tomas largas con 0–3 cortes~~ (sustituido 2026-11-01, ver correcciones): **corte cada ~2 s, seco y en pulso** (alternando 3 y 2 pulsos: 2,43 / 1,62 s a 74 BPM), sin whips ni flashes. Duración 23–33 s.
- **Encuadres variados con zoom suave, enseñando el FÍSICO**: general (×1,0–1,2) · medio (×1,25–1,4) · como mucho ×1,5 sobre una persona o los abdominales. El punto de foco va en el tronco (pecho/abdominales/brazos), nunca en la cara; la cabeza entra entera arriba del encuadre, sin cortarla. Cada plano con zoom continuo (acercar o alejar, `Easing.inOut(sin)`) y punch-in de entrada suave (+6 %, 6 f) en la mitad de los planos. Alternar general/medio y repartir entre todos los que posan. Encuadre = zoom + punto de foco en px del proxy, con tope para que no se vean bordes (`Plano` en `src/videos/posing-gold/PosingGold.tsx`). (Sustituye a la versión con zooms ×1,8–2,15, 2026-11-01.)
- Orden que funciona: relajado/de frente → enseñar (camiseta arriba) → bíceps → **brazos arriba / abdominales al final** (como cierra la ref 1).
- Fundido a negro corto al entrar (12 f) y al salir (15 f), música que se apaga en los últimos 2 s.
- Música: si Lucas da una canción (enlace de YouTube), descárgala con `herramientas/.venv/bin/yt-dlp -x --audio-format mp3` y úsala **tal cual** (sin slowed, salvo que lo pida). Si no, synthwave/darkwave generado con ElevenLabs + `slowed-reverb.sh … 0.88`.
- **Ajustar a los ritmos**: librosa beat_track → ajuste lineal de los pulsos (periodo exacto) y RMS de graves por segundo para encontrar el drop. Recorta la canción para que empiece **4 compases antes del drop** (intro = 1 plano por compás, el último con zoom que acelera, `Easing.in`), el drop cae en la pose más fuerte (camiseta arriba) con el único destello del vídeo, y después un plano por compás con el último compás de cada frase partido en 2 + 2. Termina en final de frase. Canción a −14 LUFS (las de phonk vienen a −7: volumen ≈ 0,36).

## Formato
- **Bruto horizontal → reel vertical 1080×1920 con el vídeo horizontal a todo el ancho (1080×608 centrado, top 656) y franjas negras arriba y abajo.** Ni girado ni recortado a vertical.
- Bruto de cámara Sony (4K 25 fps, SDR bt709): proxy con ffmpeg directo a 1920×1080 (no hace falta avconvert) y **composición a 25 fps** (los del bruto) para que no haya tirones 25→30.

## Correcciones de Lucas
- 2026-11-01 — Bruto horizontal: **horizontal sin más, no girado**, a todo el ancho del reel vertical con bordes negros arriba y abajo. Por qué: "no quiero que sea un horizontal girado, quiero que sea un horizontal sin más… no me importa que haya los bordes negros arriba y abajo" / "es un reel, son verticales, simplemente que ocupe el horizontal". (posing-gold)
- 2026-11-01 — **Corte cada ~2 s y juega con zooms** (general/medio/cerrado), en vez de 4 tomas largas. Por qué: "mete cortes cada 2 segundos. Es como demasiado estático todo. Puedes también jugar con zooms". (posing-gold)
- 2026-11-01 — **Zoom máx. ~×1,5 y centrado en el cuerpo, no en la cara** (cabeza entera pero arriba; lo que manda es el físico). Por qué: "zoomeado demasiado y… enfocando la cara más que al físico, que realmente es un posing. Hay que enseñar el físico, no la cara". (posing-gold)
- 2026-11-01 — Música elegida por Lucas: **DYGO & Mxng0 – FUNK INFERNAL [Brazilian Phonk]** (YouTube A8DLRWL9_Y8), ajustada a los ritmos. Por qué: "haz el edit con esta canción, descárgatela y ajústalo a los ritmos". (posing-gold)
