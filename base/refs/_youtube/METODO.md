# Cómo estudiar los títulos, miniaturas y descripciones de un canal

Sirve para tres cosas: **el canal del propio creador** (qué le funciona a él: es la referencia que más vale), un
**canal de referencia de un nicho nuevo**, o **repetir el estudio** dentro de un año. Se hace desde la raíz de la
carpeta de edición. Solo se leen datos públicos; no se sube nada.

## 1. Bajar los datos
```
PY herramientas/canal_youtube.py @canal --meses 12            → refs/_youtube/<canal>/
PY herramientas/canal_youtube.py @canal --salida personal/<creador>/refs/canal     (el canal del creador)
```
- Necesita `yt-dlp` (`winget install yt-dlp`, `brew install yt-dlp` o `pip install yt-dlp` en la `.venv`).
- Baja solo la pestaña de vídeos largos, en su **idioma original** (yt-dlp pide el título original, no la traducción
  automática de YouTube) y la miniatura por defecto, que es la original.
- Si el canal publica poco (menos de ~40 vídeos al año), `--meses 24`.
- Unos 3 s por vídeo. Varios canales a la vez van bien (10 en paralelo sin bloqueo el 2026-11-13).
- Deja `titulos.tsv`, `descripciones.txt`, `videos.json`, `resumen.json`, `miniaturas/`, `hojas/` (16 por hoja,
  pequeñas y en orden cronológico, + `extremos.jpg`) y `detalle/` (4 miniaturas grandes por hoja, **de mayor a menor
  ratio**; las de menos de 21 días, con `*`, al final; pie `#n · xRatio · fecha · visitas · título`). Mira una hoja
  antes de seguir: que se lean los títulos y los ratios.

## 2. Analizar (agentes, cada uno con su contexto)
Un agente no puede mirar bien 600 miniaturas; uno por canal, sí. Reparto que funcionó:

| Agente | Encargo | Qué mira |
|---|---|---|
| uno por canal | `ENCARGO_CANAL.md` | todas las hojas + 10 o más miniaturas a tamaño completo; tabla de TODAS; recetas |
| uno por canal (fino) | `ENCARGO_DETALLE.md` | todas las hojas `detalle/` y `hojas/` + 12 o más a tamaño completo; vídeo a vídeo: recorrido del ojo, cara, manos, instante, texto, encaje y segunda lectura, mecanismos, parejas casi iguales; contraste con la guía al final |
| uno por idioma | `ENCARGO_TITULOS.md` | todos los títulos de los canales de ese idioma; moldes con recuento |
| uno para todos | `ENCARGO_DESCRIPCIONES.md` | todas las descripciones |
| uno por canal (nicho) | `ENCARGO_TITULOS_NICHO.md` | para afinar los títulos de UN tipo de vídeo (animales, aventura…): todos los títulos de ese canal, sus moldes, el sujeto, cómo nombra al tema, y qué papel hace el título frente a su miniatura en las 10 mejores y peores. Se usó el 2026-11-14 con cinco canales de animales (`animales_titulos_2026-11-14.md`) |

Todos leen antes `ENCARGO_COMUN.md` (qué es el ratio, reglas, formato). Se lanzan a la vez: son ligeros (leen texto e
imágenes, no vídeo). Cada uno escribe su `.md` y devuelve 15 líneas. Para un solo canal (el del creador) basta
`ENCARGO_CANAL.md`, pidiéndole además los moldes de sus títulos; para saber por qué le funciona lo que le funciona,
`ENCARGO_DETALLE.md` (más largo y más fino: es el que se usó el 2026-11-14 con los 15 canales).

**Si un agente se corta** (límite de uso, error): otro sigue **el mismo archivo a medias**, sin rehacer lo que ya
está escrito; dile por qué hoja o por qué vídeo iba. Pide a todos que guarden el archivo cada pocas hojas, no al final.

**No les des tus hipótesis**: el encargo pide recuentos y contraejemplos, no confirmar una idea. Y que digan lo que no
han podido ver.

## 3. Leer con cautela
El ratio no es el CTR. Antes de sacar una regla, mira qué más cambia entre los vídeos que comparas: la serie, el
invitado, el tema, el país, la época. Compara empaquetados solo dentro del mismo tema o serie, y corrige:
- **Por época**: si el canal crece o se apaga (los vídeos viejos acumulan visitas; un canal que crece, al revés),
  compara cada vídeo con la mediana de sus 8–10 vecinos en el tiempo.
- **Por posición en la serie**: cada episodio suele caer un 2–3 % respecto al anterior; un episodio que cae menos que
  esa tendencia tiene buen empaquetado.
- **Estrenos pegados** (≤ 8 días entre dos vídeos), el primero tras un parón y las rachas: descuéntalos.
- **«Me gusta» por visita**: ratio alto con pocos «me gusta» = llegó a gente de fuera (el empaquetado funcionó, o
  decepcionó: míralo con los comentarios); muchos «me gusta» con ratio bajo = solo lo vieron los suscriptores. En 11
  de los 15 canales estudiados van al revés que el ratio.
Vale más una **pareja casi igual con resultado distinto** que una mediana. Una regla se apunta cuando se repite en
varios canales o cuando la confirma un test del propio creador.

## 4. Dónde va lo aprendido
- **De un creador** (su canal): `personal/<creador>/preferencias.md` → «Títulos y miniaturas»; los datos, en
  `personal/<creador>/refs/canal/`.
- **De un nicho o un idioma nuevo** (local): `refs/_youtube/<canal>/` y un `refs/_youtube/CONTEXTO.md` propio.
- **Para todos** (solo modo autor): los análisis a `base/refs/_youtube/`, las reglas a `base/titulos-miniaturas.md` o
  `base/descripciones.md`, y la tabla de `CONTEXTO.md` al día.

## 5. Lo que cierra el círculo
Los resultados de «Probar y comparar» de YouTube del propio creador (qué pareja ganó y con qué porcentaje) valen más
que cualquier estudio de otros canales. Pídeselos y apúntalos con el vídeo, la pareja ganadora y la perdedora.
