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
6. **Con muchos clips (un lote, o el material de alguien que empieza): `herramientas/inventario_recursos.py`**:
   `pendientes` (clips sin ficha, fichas que se quedan cortas y por qué, duplicados, nombres repetidos) → `preparar
   [--transcribir]` (técnica, hoja de contactos con la leyenda de segundos, audio y lo que se dice; lotes en
   `herramientas/alta_recursos/`, la misma sesión junta) → un subagente por lote con `herramientas/ENCARGO_RECURSOS.md`
   (formato, criterios y ejemplos) → `juntar [--mover]` (las fichas al índice; con `--mover`, cada clip a su carpeta y
   nombre) → `comprobar`. Es el mismo método de siempre, escrito para que salga igual en cualquier ordenador: cada
   segundo del clip con lo que pasa, para que los tiempos sean buenos al montar. Por qué (Lucas, 2026-11-17): «tiene
   que haber un buen contexto generado de cada vídeo de recursos. No puede ser un contexto pobre, porque así los
   timings son buenos a la hora de meter la edición».

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
- **La línea de tiempo de TODO el clip** (2026-11-17): cada tramo con su segundo, también lo que no sirve, como las
  mejores fichas del índice (`0–23 colocan la cámara · 24–29 de frente · **36–41 se suben la camiseta** · …`): es lo que
  da tiempos buenos al montar. En fichas nuevas puede ir en una línea **Momentos** aparte (formato y ejemplos en
  `herramientas/ENCARGO_RECURSOS.md`). Las fichas que ya hay siguen valiendo; `inventario_recursos.py pendientes` dice
  cuáles se quedan cortas, para completarlas cuando se vaya a usar ese clip o cuando el creador lo pida.
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
   entregar. Si la frase habla de algo que no tienes grabado, o `recursos/` está vacío, un clip libre de Pexels
   (`herramientas/pexels.py`; preferencias → Recursos). Lo tuyo va primero cuando casa.
6. **Duración en el montaje**: un plano de recurso suele durar 0,6–2 s (según el ritmo del tipo de vídeo). Coge el
   subtramo que cubre la frase y corta en un punto de movimiento.

Al acabar el vídeo, añade "Usado en: <slug> (tramos)" en la ficha de cada recurso usado.

## 6b. Vídeos de stock como recursos (cuando toca)

Cómo se han usado en los edits de Lucas (fisico-redes, recetas-este-es-lucas, montajes de vida); las reglas de detalle
están en `base/preferencias.md` → Recursos (2026-11-05 y 2026-11-16).

**Cuándo sí**
- La frase habla de algo que el creador **no tiene grabado** (culturistas, alguien mirando el móvil, un partido, unas
  escaleras, un animal…): un clip que lo enseñe de verdad es mejor que forzar un recurso suyo que no lo ilustra.
- `recursos/` está vacío o no hay nada en el índice que case (carpeta recién instalada).
- Formatos que se apoyan en stock por diseño (p. ej. recetas con voz en off: manos y comida de stock).

**Cuándo no**: si hay un clip propio que casa, va el propio. El stock tapa huecos, no sustituye lo grabado. En vídeos
hablando a cámara, nada de clips a pantalla completa encima de la cara salvo que lo pidan
(`refs/hablando a camara/CONTEXTO.md`).

**Cómo**
1. **Buscar** en inglés y en vertical: `herramientas/pexels.py buscar "…" --miniaturas <dir>` (con `PEXELS_API_KEY`;
   sin clave, el método del navegador de preferencias → Recursos). **Mira las portadas o el clip** antes de bajarlo:
   tiene que enseñar exactamente lo que dice la frase (la especie, el ejercicio, el sitio). Pexels: uso libre, sin
   atribución obligatoria.
2. **Que case con el resto** igual que un recurso propio (§ 6): tema de la frase primero, luego paleta, luz, sitio,
   época y energía del vídeo (si el gancho es oscuro, stock oscuro).
3. **Que siga pareciendo del creador**: él sale en el gancho, en las frases que hablan de él y en el cierre (con la
   misma ropa del gancho si se puede). Si el stock hace de él (cocinar, preparar algo), solo **manos y planos de
   detalle**, nunca la cara de otra persona como si fuera él.
4. **Bajar** a `estudio/public/<slug>/` (`pexels.py bajar <id> …`), la mejor resolución vertical. Si el vídeo es 4K y
   el clip 1080p, escálalo a 2160×3840 (lanczos + `unsharp`). Al stock **sí** se le puede tocar la exposición o el
   color para que case (no es un bruto del creador); a lo suyo, no.
5. **Apuntar el origen**: el id de Pexels (y el autor) de cada clip en el comentario de la composición, o en un
   `catalogo.json` si son muchos (recetas). Así se pueden volver a bajar para un retoque.
6. **Al entregar**, di qué planos son de stock.
7. **Al terminar el vídeo**: si el clip puede volver a servir, catalógalo en `recursos/` como uno propio (§ 1–4), con
   "Pexels <id>" en la ficha. Si no, se borra de `public/<slug>/` cuando quien edita da el vídeo por acabado (o con la
   limpieza de 30 días); los ids quedan apuntados para bajarlos otra vez.

## 7. Mantenimiento

- Al cerrar un edit, los brutos que sirvan de b-roll van a su carpeta de `recursos/` con su ficha (flujo, paso 8);
  el resto, a `bruto terminado/`.
- Antes de pedirle material nuevo al creador, busca en el índice.
- **Nunca se borran recursos** (ni a mano ni con la limpieza automática).
