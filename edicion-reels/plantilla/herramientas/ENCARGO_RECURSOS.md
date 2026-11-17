# Encargo: ficha con CONTEXTO RICO de cada clip de recursos (un lote)

> De la skill (igual en `edicion-horizontal` y `edicion-reels`). Lo prepara `herramientas/inventario_recursos.py preparar`:
> te pasan un `lote_NN.md` con los clips, su técnica, su hoja de contactos (con la leyenda de segundos) y, si hablan, lo
> que se dice. Un agente por lote; hasta 4–5 a la vez en Mac, de dos en dos en Windows con 16 GB.

Eres quien cataloga el archivo de vídeo de un creador. Tu ficha es lo ÚNICO que se leerá al editar: nadie volverá a
mirar el clip para decidir si sirve, qué tramo usar ni dónde cortar. Si la ficha es pobre, el clip no se usa o se usa
mal (el tramo equivocado, un corte en mitad del gesto, un recurso que no casa con la frase). Por eso: **cada segundo del
clip con lo que pasa, y para qué frase de voz sirve.**

Por qué (Lucas, 2026-11-17): «tiene que haber un buen contexto generado de cada vídeo de recursos. No puede ser un
contexto pobre, porque así los timings son buenos a la hora de meter la edición».

Todo en español de España. No ves movimiento ni oyes: trabajas con fotogramas y con los datos de audio. Lo que no
puedas comprobar, dilo («no comprobado»); no lo inventes.

## Cómo trabajar cada clip

1. **Lee la técnica** del lote (duración, resolución, orientación, fps, HDR, fecha de grabación, audio).
2. **Mira la hoja de contactos entera** con su leyenda (`hoja.txt`: qué segundo es cada celda). Haz la línea de tiempo
   de TODO el clip: qué pasa en cada tramo, también lo que no sirve (colocar la cámara, se va de plano, desenfocado).
3. **Afina donde hay algo bueno**: hoja fina del tramo para dar inicio y final exactos del gesto
   (`<python> herramientas/inventario_recursos.py hoja "<archivo>" <inicio> <duración> 0.25` desde la carpeta de
   edición, con `<python>` = `python3`, o el de la carpeta: `herramientas/.venv/bin/python`, en Windows
   `herramientas/.venv/Scripts/python.exe`; mira su leyenda). Un gesto
   se corta en un punto limpio: el extremo del movimiento, el gesto completo. Movimientos que se repiten (repeticiones,
   pasos, saltos): da las paradas (los extremos) con su segundo.
4. **Si hablan** (`dice.txt`), apunta lo que se dice con su segundo (frases citables) y si el audio sirve o hay que
   quitarlo (viento, conversación de fondo, música con derechos).
5. **Escribe la ficha** con el formato de abajo. Si te dan una ficha vieja (POBRE), rehazla entera conservando lo que
   esté bien medido.
6. **Comprueba antes de entregar** (la herramienta lo comprobará igual y devolverá la ficha si no pasa):
   - la línea de tiempo cubre al menos el 70 % del clip (50 % en clips de más de 3 min), con un tramo cada 10–15 s como
     mucho, en orden y dentro de la duración;
   - hay **Útil** con los mejores tramos en negrita;
   - **Vibe**, **Temas** (3–5 frases), **Audio** y, si sale una persona, **Outfit**;
   - al menos 35 palabras de descripción.

## Dónde va y cómo se llama

- **Carpeta**: la del TEMA que ilustra (lo que la voz dirá cuando se use), no la fecha ni la cámara. Usa las carpetas que
  ya tiene el índice (`INDICE.md`, la tabla de arriba); si de verdad no encaja en ninguna, propón una en tu respuesta.
- **Nombre**: `AAAA-MM-DD_<que-se-ve>[_<detalle>].ext`, minúsculas con guiones (fecha de grabación de la técnica). Clips
  de una misma sesión: `AAAA-MM-DD_<sesion>_NN-<que-se-ve>.ext`. Ningún nombre repetido entre carpetas.
- Si propones otra carpeta o nombre que el actual, añade la línea `Original: \`<ruta actual>\`` (relativa a la carpeta de
  recursos): `inventario_recursos.py juntar --mover` lo moverá.

## Formato de la ficha (en `lote_NN.fichas.md`, una tras otra)

```
- `<carpeta>/<nombre>.<ext>` (<nombre de cámara>, <dur> s, <ancho>×<alto> <fps> fps <SDR|HDR>, <trípode|a pulso|gimbal>)
  **Qué se ve**: sujeto y acción, quién sale (y si mira a cámara), dónde, encuadre (plano, ángulo, de frente/lado/espaldas).
  **Momentos**: 0–1,8 coloca la cámara (no sirve) · 1,8–6,2 **<lo que pasa, con detalle>** · 6,2–9,5 <…> · … · 41+ se va de plano.
  **Útil**: **1,8–6,2** (el mejor: por qué) · 12–15,5 (sujeto pequeño: zoom ×1,3 hacia <dónde>) · paradas ≈ 3,1 · 4,6 · 6,0.
  **Vibe**: sitio, luz (hora, sol/sombra/interior), época del año, energía, tono.
  **Temas**: «<frase de voz en la que encaja>» · «<otra>» · «<otra>» (3–5, como las diría el creador).
  **Outfit**: prenda, color, marca visible (si sale una persona).
  **Audio**: sirve (<qué se oye>) / quitar (<por qué>). Lo que se dice: 3,2 «…».
  **Ojo**: matrículas, caras de terceros o menores, marcas o logos, pantallas con datos, la casa o la ubicación.
  Usado en: —
```

**Lienzo** (lo dice el lote):
- **Horizontal 16:9 (YouTube)**: el sujeto ocupa una parte clara del cuadro; si queda pequeño, di dónde está para
  cerrarle zoom (hasta ×1,4 sin que se note en 4K). Un tramo útil dura al menos 2,5 s.
- **Vertical 9:16 (reel)**: ¿cabe el sujeto en 9:16 con aire para los textos (fuera de y 0–220 y 1500–1920 en 1080×1920)?
  Si el clip es horizontal, di si el sujeto queda centrado al recortar. Apunta los picos de expresión (risa, esfuerzo,
  sorpresa, cara de fallo) y los **remates** (gestos que cierran una idea), en negrita.

## Ejemplos

**Pobre (no vale)**: «`gym/espalda/2026-11-01_jalon.MOV` (IMG_1085, 41 s): jalón en polea, gym oscuro. Reps 2–40.»
→ No dice quién sale ni cómo va vestido, ni el ángulo; una sola franja para 41 s; no hay lo mejor ni para qué frase sirve.

**Rico (así)**:
```
- `gym/espalda/2026-11-01_jalon-agarre-estrecho_sudadera-y-sin-camiseta.MOV` (IMG_1085, 41 s, 2160×3840 60 fps HDR, trípode)
  **Qué se ve**: Lucas hace jalón en polea alta con agarre estrecho en Gold's Gym (nave oscura, vigas negras, foco del
  techo detrás); primero con sudadera gris de 3/4 desde atrás y desde abajo, luego sin camiseta de espaldas y centrado.
  **Momentos**: 0–12 jalón con sudadera, 3/4 trasero contrapicado · 12–16 se levanta y cambia de máquina · 16–17 **se
  quita la sudadera** · 17–20 se sienta y coge la barra · 20–31 **jalón sin camiseta, de espaldas y centrado: la espalda
  se abre muy bien** · 32–40 mismo ejercicio en 3/4 trasero · 40–41 se levanta (no sirve).
  **Útil**: **20–31** (la espalda, el mejor plano) · **16–17** (remate: se quita la sudadera) · 2–12 · paradas ≈ 21,4 ·
  23,0 · 24,7 · 26,3 · 28,0 · 29,6.
  **Vibe**: gimnasio oscuro con focos cálidos, tarde de otoño, energía alta y seria.
  **Temas**: «para una espalda ancha» · «el jalón es el ejercicio que más me ha funcionado» · «quítate la sudadera
  cuando calientes» · «día de espalda».
  **Outfit**: sudadera gris Gymshark con logo en la espalda y pantalón de chándal negro ancho; luego sin camiseta.
  **Audio**: quitar (música del gym y conversaciones de fondo).
  **Ojo**: gente al fondo a 0–12 (sin caras reconocibles).
  Usado en: —
```

## Al acabar

Responde en pocas líneas: cuántas fichas has escrito, qué clips no has podido mirar bien (y por qué), qué carpeta nueva
propones (si alguna) y qué hay que decidir (caras de terceros, marcas, matrículas). No toques `INDICE.md`: lo junta
`inventario_recursos.py juntar`.
