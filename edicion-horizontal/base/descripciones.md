# Descripción, capítulos y etiquetas de YouTube — ESTÁNDAR

> Estándar de `edicion-horizontal`. **Títulos y miniaturas: `base/titulos-miniaturas.md`** (se hacen antes: la
> descripción completa lo que el título calla). Los datos del creador (canal, redes, enlaces fijos, código) están en
> `personal/<creador>/perfil.md`; sus reglas de `personal/<creador>/preferencias.md` → «Entrega y publicación» mandan.
> Base: las 631 descripciones de diez canales (`base/refs/_youtube/descripciones.md`). Aún no hay correcciones de Lucas
> sobre descripciones.

Con cada vídeo terminado se entrega el **paquete de YouTube** (`base/titulos-miniaturas.md` § 8): en
`out/<slug>/youtube/PAQUETE.md` va todo, y en `out/AAAA-MM-DD_<slug>.txt` lo que se pega tal cual (títulos, descripción
con capítulos, etiquetas). **Todo en el idioma del vídeo** (el hablado, detectado), no en el idioma en que te escriben;
si el creador quiere además traducción, se añade debajo. Claude **no sube ni publica nada**: lo copia el creador.

## Para qué sirve (y para qué no)
- **No trae clics.** En ninguno de los diez canales se ve relación entre la descripción y las visitas: no se lee antes
  de pulsar. Tres de los diez mejores vídeos de su canal llevan debajo una plantilla sin una sola línea propia.
- **Sí sirve para que te encuentren y para quien ya está dentro**: el nombre exacto del sitio, la especie o la persona
  (lo que el título calló a propósito), los capítulos, el enlace a la serie, a quien ayudó, y lo obligatorio
  (patrocinio, licencias). Los canales de «contenido que se busca» (un destino, una especie) escriben resumen casi
  siempre: Nico Villa 62 de 64, Brave 46 de 46, Paul Cuffaro 148 de 150. Los de personaje o reto, no. Un creador
  mediano de animales, viajes o visitas está en el primer grupo: **se escribe**.
- Por eso: corta, útil y sin relleno. 900–1400 caracteres sin contar la letra pequeña. Más no ayuda.

## Bloques, en este orden
1. **Primera línea (120–200 caracteres): qué pasa, dónde o con qué animal, y algo sin resolver.** Con el **nombre
   propio que el título no dice**. Es lo único que se ve antes de «…más». Las buenas tienen un nombre propio, una cifra
   o una condición, y un final abierto («…», una pregunta, «El problema es que…»). Prohibido «Hoy os traigo un vídeo…»,
   «In today's video, we…», «¡Hola a todos!» y copiar el gancho hablado.
   - «Hoy nos encontramos en Dandong, la ciudad frontera entre China y Corea del Norte, parece una ciudad normal pero…»
   - «While in the Amazon Rainforest, Mark Vins comes face to face with the Assassin Hawk, an Assassin Bug that mimics…»
   - Si hay patrocinador y su contrato pide la primera línea, él va en la 1 y el resumen en la 2 (lo decide el creador).
     Indicio de un solo canal: en Nico Villa, los 11 vídeos con el patrocinio en la primera línea rinden x0,58 frente a
     x1,27 (puede ser que los patrocinados ya fueran más flojos).
2. **Un párrafo de contenido (250–450 caracteres)**: lo que se ve, con lugares, especies y personas **por su nombre**
   (el científico también, si se dice en el vídeo), y una o dos preguntas de las que la gente teclea («¿Se puede soltar
   un lobo criado por humanos?»). Frases, no listas de palabras clave.
3. **Patrocinio** (si lo hay), con la palabra de aviso delante, enlace y código: en español «Publi.»; en inglés
   «Thanks to X for sponsoring this video!». Lo declara el creador también con la casilla de YouTube.
4. **Capítulos**, escritos siempre (abajo). En español YouTube no los pone solo (0 de 279 vídeos); en inglés a veces
   sí, pero los escritos son mejores.
5. **Serie**: lista de reproducción y episodio anterior, si es seriado.
6. **Gracias y enlaces** de quien sale, presta o acoge.
7. **Bloque fijo del creador** (3–5 líneas): redes, contacto, tienda. Sale de su `perfil.md`; si falta un dato, se deja
   marcado `[falta: Instagram]`, no se inventa.
8. **Tres hashtags** al final (YouTube muestra los tres primeros sobre el título): especie o país, lugar, tema. Nunca
   `#viral`, `#fyp`.
9. **Letra pequeña** (condiciones del patrocinador, licencias de música), al fondo.

**Petición de suscripción**: opcional y en una línea con el tema concreto («Suscríbete para ver crecer estos recintos»).
La mitad de los canales no la escribe; no es lo que mueve nada.

## Reglas
- **No inventar**: cifras, nombres científicos, marcas y sitios solo si salen en el vídeo o los ha dado el creador. Lo
  dudoso, entre corchetes `[confirmar]`. Los nombres que Whisper transcribe mal (especies, topónimos) se comprueban
  contra los rótulos del vídeo y el perfil del creador antes de escribirlos.
- **Tono del creador** (míralo en la transcripción), frases cortas, primera persona. En inglés vale también la
  tercera persona de sinopsis si es su estilo. Sin tacos ni coletillas del vídeo.
- **Repásala entera**: erratas en la palabra que importa («POSCHE 911»), marcadores sin rellenar («[Giveaway End
  Date]»), promociones caducadas, enlaces que no son enlaces, la misma línea de otro vídeo. Todo eso está en canales grandes.
- **No rellenar con palabras clave** («busan, gamcheon, corea del sur, south korea, 4k»), ni etiquetas que no describen
  el vídeo.

## Capítulos
- Salen de las secciones del EDL: `herramientas/montaje/capitulos.py` (desde `out/<slug>/`) imprime `m:ss Título` con
  los tiempos del **vídeo final**. Si se vuelve a montar, se vuelven a sacar.
- El primero es `0:00`; mínimo 3 capítulos y 10 s cada uno; en orden. Formato `0:00 Texto`, uno por línea. De 6 a 12
  es lo normal en un vídeo de 15–30 min.
- Título de capítulo: 2–5 palabras, frase normal (no las mayúsculas del rótulo), con **el nombre del sitio, la especie
  o la pregunta** («Castillo Neuschwanstein», «Cuánto se gana en Alemania») o un gancho («Time to Enter the Sting
  Zone»). `capitulos.py` da «Intro» y «Cierre»: tradúcelos al idioma del vídeo o cámbialos por algo que diga más.

## Etiquetas (el campo «Etiquetas» de YouTube)
De 10 a 20, propias de ese vídeo: lugar y especie con sus variantes de escritura (nombre común y científico, con y sin
tilde), el nombre del canal, la pregunta. Dos o tres fijas del canal. Pesan poco (MrBeast no usa ninguna), así que sin
esfuerzo de más y nunca genéricas (`TRENDING`, `VIRAL`).

## Plantilla en español
```
<Qué pasa, dónde o con qué animal (con su nombre) y algo sin resolver. 120–200 caracteres.>

<Párrafo: lo que se ve, con nombres propios, y una o dos preguntas que la gente busca. 250–450 caracteres.>

Publi. <marca>: <oferta> con el código <CÓDIGO> en <enlace>          (solo si hay)

Capítulos
0:00 <Arranque>
1:02 <Capítulo 1>
…

Serie «<nombre>»: <enlace a la lista>                                 (solo si hay)
Gracias a <quién> <enlace>                                            (solo si hay)

Instagram: <enlace>
Contacto: <correo>

#especieolugar #lugar #tema
```

## Plantilla en inglés
```
<What happens, where or with which animal (named), and something left unresolved. 120–200 characters.>

<Paragraph: what you see, with proper names, and one or two questions people search for. 250–450 characters.>

Thanks to <brand> for sponsoring this video! <offer> with code <CODE> at <link>      (only if any)

Chapters
0:00 <Opening>
1:02 <Chapter 1>
…

Watch the full "<series>" series: <playlist link>                     (only if any)
Huge thanks to <who> <link>                                           (only if any)

Instagram: <link>
Business: <email>

#speciesorplace #place #topic
```

Diferencias reales entre idiomas: la fórmula del patrocinio; en inglés las descripciones son más largas y con más
enlaces (mediana 1492 caracteres frente a 351) y en vídeos de animales es habitual un aviso de seguridad al final
(«Never attempt to handle wild animals…»: Brave, 43 de 46); en español no aparece en ningún canal.

## Antes de entregar
- ¿La primera línea se entiende sola, lleva el nombre que el título calla y deja algo abierto?
- ¿Los tiempos de los capítulos son los del archivo final (compruébalo en dos de ellos con un fotograma)?
- ¿Todo lo que pone sale en el vídeo o lo ha dicho el creador? ¿Nombres de especies y sitios bien escritos?
- ¿Está en el idioma del vídeo, con el canal y las redes de ESE idioma (`marca.json` → `idiomas`)?
- ¿Queda algún corchete sin resolver? Dilo en «por confirmar».
