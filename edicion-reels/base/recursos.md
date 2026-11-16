# Recursos: cómo clasificarlos, analizarlos y elegirlos

> **Estándar de `edicion-reels`** (solo lo cambia Lucas). Vale para cualquier nicho: fitness, cocina, viajes, moda,
> tech, vlog… Los ejemplos de Lucas son de fitness; cambia las categorías por las de tu contenido. Las reglas de
> cómo combinarlos en un vídeo están en `base/preferencias.md` → Recursos; tus excepciones, en `personal/preferencias.md`.

Recurso = clip o foto **tuyo** que se puede reutilizar en otros vídeos (b-roll). Viven en `recursos/` de la carpeta
(nunca en la skill) y cada uno tiene su ficha en `recursos/INDICE.md`. Sin ficha, el clip no existe: al montar se
busca en el índice, no mirando carpetas.

## 1. Carpetas: clasifica por lo que vas a buscar

- Clasifica por **el tema que ilustra**, que es lo que se busca al montar: la frase de la voz en off dice "espalda",
  "madrugar" o "comer fuera" y hay que encontrar un clip que lo enseñe. No clasifiques por fecha ni por cámara.
- **Primer nivel = los grandes temas de tu contenido** (5–8). **Segundo nivel solo cuando una carpeta pase de ~15 clips**
  o tenga subtemas claros (Lucas: `gym/<zona muscular>/`). Al partir una carpeta, actualiza las rutas del índice
  y de los comentarios de las composiciones que usan esos clips.
- Las carpetas de la plantilla son las de Lucas (fitness). Si tu nicho es otro, **crea las tuyas dentro de
  `recursos/` y borra las vacías que no apliquen**; apúntalas en la tabla de arriba del índice. Ideas:

  | Nicho | Primer nivel | Segundo nivel cuando crezca |
  |---|---|---|
  | Fitness (Lucas) | `gym/`, `running/`, `competicion/`, `aire-libre/`, `lifestyle/`, `recuperacion/` | `gym/<zona muscular>/` |
  | Cocina | `recetas/`, `ingredientes/`, `mercado/`, `emplatado/`, `comiendo/`, `cocina-casa/` | `recetas/<tipo de plato>/` |
  | Viajes | `<país o ciudad>/`, `transporte/`, `alojamiento/`, `comida/`, `paisajes/` | `<país>/<ciudad>/` |
  | Moda | `outfits/`, `prendas/`, `tiendas/`, `probador/`, `calle/` | `outfits/<estación>/` |
  | Tech / negocio | `setup/`, `pantalla/`, `producto/`, `unboxing/`, `oficina/`, `reuniones/` | `producto/<marca>/` |
  | Vlog / lifestyle | `mananas/`, `casa/`, `amigos/`, `comida/`, `deporte/`, `noche/` | por tema |

- Siempre existen: **una carpeta de "tú sin acción concreta"** (posados, mirando a cámara, andando, intros: sirven
  para ganchos y cierres; en Lucas, `gym/fisico/`), `fotos/` (recortes PNG, fotos de producto) y `sonidos/` (SFX).
- Si un clip encaja en dos carpetas, va a la del **tema principal** y el otro tema se apunta en **Temas**.
- Los brutos ya editados que no sirven como b-roll genérico van a `bruto terminado/`, no a `recursos/`.

## 2. Nombre del archivo

`AAAA-MM-DD_<que-se-ve>[_<angulo>][_<outfit o detalle>].ext`, en minúsculas y con guiones.
- La fecha es **la de grabación** (`ffprobe -v error -show_entries format_tags=creation_time`), no la de hoy.
- Que el nombre diga lo que se ve: `2026-06-09_curl-mancuerna-banco-inclinado_de-frente_conjunto-azul.MOV`.
- El nombre original (`IMG_7208`) no se pierde: va en la ficha.
- Clips de una misma sesión: `AAAA-MM-DD_<sesion>_NN-<que-se-ve>.ext` (`NN` = orden en que se grabaron).

## 3. Analizar un clip antes de apuntarlo

1. **Técnica** con `ffprobe`: duración, resolución, fps, rotación (`stream_side_data=rotation`), **HDR o SDR**
   (`color_transfer` = `arib-std-b67` o `smpte2084` → HDR, pasa por `herramientas/proxy.sh`), y si el audio sirve.
2. **Vista general**: `herramientas/hoja_contactos.sh CLIP /tmp/hoja.jpg 1` (una celda por segundo; en clips de más
   de 60 s, cada 2 s) y mírala. Así se ve qué pasa y dónde.
3. **Fino donde hay acción**: `hoja_contactos.sh CLIP /tmp/fino.jpg 0.25 <inicio> <duracion>` en los tramos
   interesantes, para dar tiempos exactos de inicio y fin de cada gesto.
4. **Si hablan o hay voces**: `herramientas/transcribir.sh` → qué se dice (frases que se pueden citar) y si hay que
   quitar el audio (voces de fondo, música, conversación).
5. **Movimientos que se repiten** (repeticiones, saltos, pasos, cortes de cuchillo…):
   `herramientas/puntos_movimiento.py CLIP INICIO FIN` da las paradas; confírmalas con una hoja a 4 fps.
6. Con muchos clips, reparte el análisis en subagentes en paralelo (un lote por sesión) y junta las fichas.

## 4. La ficha en `recursos/INDICE.md`

Una línea por clip, dentro de la sección de su carpeta:

```
- `carpeta/AAAA-MM-DD_que-se-ve.MOV` (IMG_XXXX, 12,3 s[, 4K HDR | 1080p | horizontal]): qué se ve (acción; de frente,
  de lado o de espaldas; fijo o a pulso; cerca o lejos; quién sale). **Útil 2–5 · 8–10** (en negrita lo mejor;
  apunta también lo que no sirve: "0–1,5 el dedo tapa", "15+ se va de plano"). **Outfit**: prenda, color, marca.
  **Vibe**: sitio, luz, energía, época del año, tono. **Temas**: 2–4 frases de voz en off en las que encaja.
  Audio: sirve / quitar (por qué). Usado en: <slug> (tramos).
```

- **Outfit, Vibe y Temas son obligatorios**: sin ellos no se puede elegir bien (ver § 6).
- Clips de la misma sesión: una **cabecera de sesión** con lo común (fecha, sitio, luz, outfit, técnica) y debajo
  una línea por clip con lo que cambia. Mantener la sesión junta ayuda a casar outfits.
- Tiempos en segundos del archivo original, con coma decimal.
- Si el clip lleva marca o colaboración visible (logo, producto), apúntalo: sirve para vídeos con esa marca y hay
  que evitarlo en vídeos de la competencia.

## 5. Cómo elegir los tramos útiles (los fotogramas buenos)

Un tramo es útil si:
- **La acción se entiende en menos de 1 s** y está entera: empieza y acaba en un punto limpio (el extremo de un
  movimiento, un gesto completo). Se apunta el tramo, no el clip entero.
- **Imagen limpia**: estable o a pulso controlado, enfocada, bien expuesta, sin dedos ni objetos tapando y sin gente
  cruzando por delante (salvo que eso sea la gracia).
- **Aguanta el vertical**: el sujeto cabe en 9:16 con aire para los textos (zonas de UI de Instagram: y 0–220 y
  1500–1920 en 1080×1920). Si el clip es horizontal, apunta si el sujeto queda centrado al recortar.
- **Se ve la cara cuando importa** (ganchos, cierres, reacciones). Apunta los picos de expresión: risa, esfuerzo,
  sorpresa, cara de fallo.
- **Remates**: gestos únicos que cierran una idea (se quita la camiseta, brinda, salta, gesto de victoria, prueba el
  plato y pone cara). Van en negrita: son los que más se reutilizan.

Descarta: los segundos de colocar o coger el móvil, los tramos movidos, desenfocados o quemados, y lo que tape el
sujeto.

## 6. Elegir recursos para un vídeo

1. **Tema**: busca en el índice (Temas y "qué se ve") lo que ilustra **la frase que suena en ese momento**. Manda
   sobre todo lo demás.
2. **Outfit y vibe**: de lo que encaja, quédate con lo que case con el bruto principal y con el resto de planos:
   misma paleta (o que no choque), misma luz y tipo de sitio, misma energía y época del año (detalle en
   `base/preferencias.md` → Recursos).
3. **Técnica**: la mejor resolución que haya. Si se mezclan HDR y SDR, todos por `proxy.sh` para que casen de color.
4. **Variedad**: no repitas el mismo tramo en un vídeo y mira "Usado en" para no repetir el mismo clip en vídeos
   seguidos.
5. **Si nada encaja**: el más cercano o quédate en el plano principal (zoom, texto), lo que quede mejor, y dilo al
   entregar. Si la frase habla de algo que no tienes grabado, un clip libre de Pexels (preferencias → Recursos).
6. **Duración en el montaje**: un plano de recurso suele durar 0,6–2 s (según el ritmo del tipo de vídeo). Coge el
   subtramo que cubre la frase y corta en un punto de movimiento.

Al acabar el vídeo, añade "Usado en: <slug> (tramos)" en la ficha de cada recurso usado.

## 7. Mantenimiento

- Al cerrar un edit, los brutos que sirvan de b-roll van a su carpeta de `recursos/` con su ficha (flujo, paso 8);
  el resto, a `bruto terminado/`.
- Antes de pedirle material nuevo al creador, busca en el índice.
- **Nunca se borran recursos** (ni a mano ni con la limpieza automática).
