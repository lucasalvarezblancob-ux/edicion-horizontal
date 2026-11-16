# Intros: gancho, ráfaga y título — ESTÁNDAR

> Estándar de `edicion-horizontal` (sustituye al `ganchos.md` de reels). Sale de lo medido en las referencias
> (`base/refs/dinamicos/CONTEXTO.md`) y de las correcciones de Lucas. Tus reglas de `personal/<creador>/preferencias.md` mandan.

En YouTube el primer medio minuto decide si se quedan. Un vídeo horizontal no abre con un texto escrito encima (eso es
el reel): abre **enseñando lo mejor del propio vídeo**.

## Estructura de serie (la que lleva `ramon`)

| Bloque | Duración | Qué es | Marca en el EDL |
|---|---|---|---|
| 1. Gancho / tráiler | 15–27 s | Lo mejor del vídeo, antes de cualquier saludo | `X("trailer")` |
| 2. Ráfaga | 2–4 s | 3–5 planos de 0,5–0,8 s, sin voz, con la música arriba | `X("rafaga")` |
| 3. Título | 2,5–4 s | Título grande sobre un plano potente, con golpe de sonido | `X("titulo")` |
| 4. Arranque | — | Saludo corto o directamente la primera sección | `X("cuerpo")` |

Reglas:
- **Se habla desde el fotograma 0.** Nada de logo, cabecera ni «hola, ¿qué tal?» antes del gancho.
- **El gancho se monta con frases y planos del propio vídeo** (no se inventa ni se graba aparte salvo que el creador lo
  traiga). Dos maneras, según el bruto:
  - *Recap con voz* (tipo Rubén Holgado): 12–22 planos de 0,35–1,5 s, **un plano por idea o por verbo**, sobre la frase
    del creador troceada o sobre su voz en off. Guion: qué es esto → por qué importa (peligro, dinero, rareza, reto) →
    promesa de lo que se va a ver.
  - *Tráiler en directo* (tipo Paul Cuffaro): 4–6 momentos con su sonido original, 2,2–2,5 s por plano; la música se
    apaga 2–3 veces para dejar una frase limpia; el último plano es el más largo y deja la sorpresa sin enseñar.
- **No destripes el clímax**: se enseña que pasa algo, no cómo acaba.
- **Cada frase del gancho va con su imagen**: si dice «tortugas», se ven tortugas desde el primer fotograma (misma regla
  que los planos de recurso). Las frases del gancho se sacan de la transcripción con `T(...)` y los planos de `BROLL`.
- **Música** desde el segundo 0 en el gancho, más alta que en el resto (ventana `trailer`→`cuerpo` del paso 6).
- **Título**: 2–5 palabras, en la fuente ancha de marca, el dato o la palabra clave en el acento. Entra de golpe (pop) y
  sale por corte. Es el título del vídeo o una versión corta; **en el idioma del vídeo**.
- **Suscripción**: no se pide en la intro. El botón animado sale cuando el creador lo dice (`BOTONES` en `plan.py`: el animado de la skill, abajo en el centro),
  normalmente tras el primer momento bueno o en el cierre.
- Si el bruto no da para tráiler (un solo plano a cámara), abre con la frase más fuerte del vídeo en punch-in y pasa al
  título: mejor 8 s buenos que 25 s de relleno.

## Capítulos
Cada sección abre con su rótulo (`S("TÍTULO", …)` en el EDL → número/total + título, ~3 s, con zoom-out de entrada y
música ~10–14 s). Los tiempos de los capítulos de la descripción salen de esas mismas marcas (`base/descripciones.md`).

## Cierre
Despedida corta (≤ 20 s), sin resumen largo. Si lo que queda abierto sirve de gancho al siguiente vídeo, dilo ahí.
Pantalla final de 8–15 s con un único CTA solo si el creador la pide (YouTube pone sus tarjetas encima: deja libre la
mitad derecha o las zonas que te diga).

## Antes de dar la intro por buena
- `ver.py` en 6–8 frames de la intro: cada texto aparece cuando se dice, nada tapa la cara.
- `hoja_recursos.py`: todos los planos del gancho enseñan su sujeto.
- Enséñale al creador la intro sola (render de los tramos 0–1) antes de renderizar el vídeo entero si es su primer edit.
