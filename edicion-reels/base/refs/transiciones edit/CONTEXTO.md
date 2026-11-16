# Transiciones edit — contexto

> **Estándar de `edicion-reels`** (mínimo que toda instalación tiene; solo lo cambia Lucas, autor de la skill). Los vídeos de esta tabla están junto a este archivo, en la skill. "Lucas" = el creador que edita; usa tus datos de `personal/perfil.md`. Las rutas `estudio/src/videos/<slug>/` de los edits citados están en la skill como `base/ejemplos/<slug>/` (código, sin media); las de `recursos/` son material de Lucas que no viene con la skill. Tus referencias y correcciones de este tipo van en `refs/<tipo>/CONTEXTO.md` de tu carpeta y mandan sobre esto.

Tipo de edit: **gancho de texto escrito al inicio + transiciones entre planos** (sin voz en off o con ella como secundaria).

## Referencias analizadas
| Archivo | Duración | Gancho (texto literal) | Transiciones usadas | s/plano | Notas |
|---|---|---|---|---|---|
| `marticops_DffdMKag6i1.mp4` (marti.cops, anuncio Black Friday Gymshark, 2026-11) | 22,6 s, 720×1280 30 fps | "GYMSHARK / BLACK FRIDAY" (Roboto Bold gris claro, sobre negro) | ráfaga de 10 planos de 4–5 fotogramas separados por 1 fotograma negro/apagado; franja que se abre a saltos desde el centro; quemados de película amarillos/naranjas y fugas de luz; barrido con desenfoque → secuencia de "película" (fondos de colores con grano y rayas + logo del tiburón) → cortinilla de arriba abajo con borde naranja; tintes rojo/azul; fundido a blanco cálido; glitch (bandas + líneas blancas + RGB); destello + zoom; desenfoque radial a negro; tarjeta final con el código que aparece con humo | intro 0,15 s; luego 1,2–4,7 s | Música: Calvin Harris – Outside. Textos: STAY TUNED + fecha, "-50% off / + CÓDIGO / for an extra -10%" (letras con fundido+desenfoque del centro a fuera), tarjeta "15 November / logo / GYMSHARK / horas / cod: CÓDIGO". Calcado en `replica-black-friday-gymshark` (fotogramas exactos en el .tsx). |

## Patrones aprendidos
- Anuncio de marca (marti.cops): **intro en ráfaga** (10 planos de detalle de la ropa/logos en 1,5 s, cada uno 4–5 fotogramas con un fotograma negro o apagado entre medias) → título de campaña sobre negro → el plano principal aparece en una franja horizontal que se abre a saltos → luces/quemados de película cada ~1 s sin cortar el plano → los cortes se tapan con transiciones de "película" (grano, rayas, colores saturados) y el logo de la marca → tarjeta final negra con fecha, logo, horas por país y código.
- Código en pantalla con aparición por letras (fundido + desenfoque, del centro hacia fuera), sin fondo.
- Logo del tiburón de Gymshark en vectorial: `recursos/fotos/gymshark/gymshark-tiburon.svg` (sacado del `mask-icon` de eu.gymshark.com).

## Caja de herramientas ya implementada (estudio/src/videos/jalon-espalda-dorito)
- **Punch-in** al entrar cada plano: escala +7 % → 0 en 7 frames, `Easing.out(cubic)`.
- **Drift**: acercamiento continuo `+0,0006 × frame` para que ningún plano esté quieto.
- **Whip** (zoom + desenfoque): ±4 frames alrededor del corte, blur hasta 14 px y escala +12 %.
- **Destello blanco**: 0 → 0,85 → 0 en 6 frames, para un corte clave (p. ej. el cierre).
- **Temblor de cámara**: 23 frames, amplitud 16 → 2 px, en una frase de intensidad ("uf, cómo quema").
- **Corte a plano cerrado** dentro de la misma toma (zoom ×1,22) para partir planos largos.
- **Match cut** entre ángulos en los extremos del movimiento (`herramientas/puntos_movimiento.py`).

## Edit "cambio en cada rep" (camisetas-flash, 2026-11-01)
Mismo ejercicio grabado con trípode fijo y varias prendas → en cada subida/bajada cambia la prenda con flash blanco + disparo de cámara. Montaje: media rep = medio pulso de la canción (0,444 s), cortes en los extremos (arriba↔arriba, abajo↔abajo), 2 vueltas a todas las prendas para que cada una salga subiendo y bajando, termina abajo → bucle limpio. 1.er flash en el drop. Texto de marca **fijo encima de la cabeza** (GYMSHARK pequeño espaciado + BLACK FRIDAY en Anton blanco), acabando por encima del punto más alto que alcanza la cabeza (mídelo); sin recorte.

## Correcciones de Lucas
- 2026-11-01 — Corta cada media rep justo en sus extremos, sin la pausa de arriba ni el balanceo de abajo (marcado frame a frame). Por qué: "hay unos frames que sobran en alguna subida o bajada". (camisetas-flash)
- 2026-11-01 — Texto fijo arriba de la cabeza en vez de detrás (sin recorte) y "Black Friday" (no "Black Day"). Por qué: "ponlo en estático arriba sin que esté detrás mío… así mejor que tener recorte". (camisetas-flash)
- 2026-11-01 — Colores del bruto tal cual, sin etalonado (se probaron contraste y gamma 0,78/0,9/1,3: ninguno). Proxy HDR con `avconvert` (ver preferencias.md). Por qué: "mantén los colores originales de los vídeos en bruto, sin tocar colores". (camisetas-flash)
- 2026-11-09 — En la hora de un lanzamiento/campaña pon **España, México y Argentina** (no la hora de otro país de la referencia): 17:00 ESP = 10:00 MEX (CDMX, UTC−6 todo el año) = 13:00 ARG (UTC−3) en horario de invierno español; en verano (CEST) 17:00 ESP = 9:00 MEX = 12:00 ARG. Por qué: "y la hora tienes que poner españa, mejico y argentina". (replica-black-friday-gymshark)
- 2026-11-09 — **Al calcar un anuncio con textos blancos encima, mide el contraste de cada línea con su fondo** (`estudio/src/videos/replica-black-friday-gymshark/revisar_contraste.py`, ratio WCAG ≥ 3) y baja la exposición SOLO de los planos que no llegan (`exposicion` del plano → `brightness()`; aquí oliva ×0,76 y sudadera de la gárgola ×0,77), sin sombras que la ref no tiene. Por qué: "a lo mejor hay que bajarle un poco la exposición porque los textos blancos no se acaban de leer bien". (replica-black-friday-gymshark)
- 2026-11-09 — **Lo que funciona**: calco "idéntico, las fuentes también" (Roboto Bold para el título y el descuento, Roboto Condensed Bold en la tarjeta, Montserrat para STAY TUNED y horas, Poppins para la fecha; posiciones = ref × 1,5). Para revisar que "todo sea igual": comparar con la ref el perfil de luminancia fotograma a fotograma (cortes, negros, destellos) y ajustar los quemados donde difieran > 45 niveles. (replica-black-friday-gymshark)
- 2026-11-09 — **En un calco, el vídeo se entrega CON la música de la referencia** (su audio tal cual, ya va sincronizado si los cortes son los mismos fotogramas; mide LUFS y pico, si está a ≈ −14 no se toca). No lo dejes "para añadir en Instagram". Por qué: entregué sin música y Lucas preguntó "¿y la música?". (replica-black-friday-gymshark)

