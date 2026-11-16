# Encargo: los TÍTULOS de UN canal de un nicho, y cómo los acompaña la miniatura

Lee antes `ENCARGO_COMUN.md`. Sirve para afinar los títulos de un tipo de vídeo concreto (animales, aventura, viaje…):
el canal, su carpeta, el nicho y el archivo de salida te los dicen en el mensaje. Se lanza un agente por canal; luego
alguien cruza los informes, así que **respeta el orden y los nombres de los apartados**. Guarda el archivo cada pocos
apartados, no al final.

El trabajo es el **texto del título**. La miniatura solo se mira para entender **qué papel tiene el título frente a
ella** (qué dice cada uno, qué calla cada uno), no para analizar su diseño.

## Qué mirar
- `titulos.tsv` entero (todos los títulos) y `videos.json` si necesitas la descripción, las etiquetas o los «me gusta».
- `hojas/NN.jpg` todas (16 por hoja, con título y ratio debajo) y `detalle/NN.jpg` (4 grandes por hoja, de mayor a
  menor ratio). Abre a tamaño completo (`miniaturas/<id>.jpg`) al menos las 8 mejores y las 8 peores.
- Corrige por época antes de comparar: si el canal crece o se apaga, compara cada vídeo con la mediana de sus 8–10
  vecinos en el tiempo y dilo. Descuenta series, invitados y temas que expliquen el ratio solos.

## Qué entregar
### 1. El canal en cinco líneas
Qué hace, idioma y variante (España, México, EE. UU., Australia…), tamaño, cuántos vídeos, si crece o se apaga, el
registro (documental, colección propia, dolor y contacto, aventura en el campo, divulgación, humor…).

### 2. Medidas del título
Longitud (caracteres y palabras: mediana y rango), mayúsculas (frase / Cada Palabra / TODO / palabras sueltas en
mayúsculas: cuáles), signos (¿ ? ¡ ! … paréntesis, barras, comillas), cifras y unidades, emojis, nombres propios
(especie científica, nombre común, nombre de un animal concreto de la casa, topónimos, personas). Recuento real.

### 3. Moldes (lo más importante)
Todos los moldes que se repiten, con huecos. De cada uno: cuántas veces, 3–5 ejemplos literales con `#n` y ratio,
mediana de ratio, **qué curiosidad abre y qué se guarda**. Clasifica TODOS los títulos en un molde (u «otros») y da el
reparto. Distingue en particular, cuando existan:
- quién es el sujeto gramatical: **el animal** («Esta Serpiente…»), **el creador** («Me mordió…», «I Found…») o
  **nadie** (nominal: «El Pez Más Raro del Río»);
- cómo se nombra al animal: nombre común, apodo, rasgo («de dos cabezas»), categoría vaga («bicho», «criatura»),
  nombre propio de un animal de la casa, nombre científico;
- qué se le atribuye: una propiedad que se ve, una conducta, un peligro, una rareza, un tamaño, un precio, una emoción.

### 4. Cómo acompaña la miniatura al título
Para las 10 mejores y las 10 peores (corregidas por época), una línea cada una: **qué dice el título**, **qué dice la
miniatura** (sujeto, instante, texto si lo hay) y **qué queda sin decir entre los dos**. Luego el recuento: en cuántas
el título nombra lo que se ve, en cuántas añade algo que no se ve, en cuántas la imagen trae algo que el título calla,
en cuántas se repiten. Si el título nombra al animal, ¿la miniatura lo enseña entero, tapado, de cerca, en acción? Si el
título lo calla, ¿cómo lo resuelve la imagen? Lo que se repita en las mejores y falte en las peores.

### 5. Qué rinde y qué no
Moldes, sujetos, formas de nombrar al animal, palancas (peligro, contacto, rareza, tamaño, ternura, rescate, compra,
obra, visita, primera vez, reto, misterio, humor…) en los de ratio alto frente a los de ratio bajo, con recuento y
cautela. Los 5 mejores y los 5 peores con una hipótesis de por qué (márcala como hipótesis). Parejas casi iguales con
resultado distinto: las más valiosas.

### 6. Cómo suena en su idioma
Lo propio de este canal y de su idioma: tiempos verbales, persona, giros, palabras de moda, cómo escribe cifras y
unidades, tuteo o ustedeo, regionalismos; lo que sonaría traducido. Si es en español, di qué sería distinto en
español de España.

### 7. Contraejemplos y malas prácticas
Títulos que no dicen nada sin la miniatura, relleno, promesas dudosas, títulos que rompen los patrones y aun así rinden.

### 8. Plantillas de este canal
8–12 plantillas con huecos, cada una con su ejemplo real (`#n`, ratio) y una línea de cuándo usarla.

### 9. Límites
Lo que no has podido ver o leer, y qué conclusiones son débiles.

Tu respuesta final: máximo 15 líneas con lo más importante y la ruta del archivo.
