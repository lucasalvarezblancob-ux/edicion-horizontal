# Montaje de vida — contexto

> **Estándar de `edicion-reels`** (mínimo que toda instalación tiene; solo lo cambia Lucas, autor de la skill). Los vídeos de esta tabla están junto a este archivo, en la skill. "Lucas" = el creador que edita; usa tus datos de `personal/perfil.md`. Las rutas `estudio/src/videos/<slug>/` de los edits citados están en la skill como `base/ejemplos/<slug>/` (código, sin media); las de `recursos/` son material de Lucas que no viene con la skill. Tus referencias y correcciones de este tipo van en `refs/<tipo>/CONTEXTO.md` de tu carpeta y mandan sobre esto.

Tipo de edit: **montaje rápido de momentos de vida** (deporte, viajes, amigos, familia, aventuras) sobre un **audio de discurso
motivacional**, con la frase que se oye escrita en pantalla. Sin voz en off propia, sin gancho aparte, sin zooms ni transiciones:
cortes secos y el clip tal cual. Encaja con la línea de Lucas (lifestyle + motivación física y mental).

## Referencias analizadas
| Archivo | Duración | Audio | Texto en pantalla | s/plano | Notas |
|---|---|---|---|---|---|
| `daviddelpinovidal_DfPC4CUosts.mp4` (instagram.com/p/DfPC4CUosts, caption "Miedo a que?") | 36,7 s, 1440×2560 30 fps | Discurso con acento argentino "¿A qué le vas a tener miedo, si nos vamos a morir?… haz lo que sientas… es un regalo la vida… disfrútala, siéntela, vívela… ama mucho, haz amigos, ríete mucho, porque ya va a llegar la oscuridad" | Frases cortas en **crema #FEFEBF**, sans negrita sencilla (~39 px a 1080), **centradas en mitad de la pantalla**, sin fondo; cambian casi siempre en el corte. Escrito en español de España ("haz lo que sientas", "sé tú") aunque el audio es argentino. Un solo grito en MAYÚSCULAS: "¡ES UN REGALO LA VIDA!" | 0,6–2,2 (media ~1,2) | 31 planos: selfies, POV, deportes (bici, buceo, snow, surf, calistenia, sentadilla), viajes, familia. Clips sin tocar (sin zoom, sin color), muchos a pulso. Cierre en calma (ciervos) en "La oscuridad." |

## Patrones
- **Cada plano ilustra la frase** y además **alterna escala y energía**: selfie cerca → plano general → acción → selfie… Nunca dos selfies seguidos.
- Las frases repetidas ("¿A qué le puedes tener miedo?", "sé tú", "haz lo que sientas") vuelven sobre planos distintos.
- El texto entra y sale **en el corte** (excepciones: "Disfrútala → siéntela → vívela" cambian dentro del plano siguiendo la voz, y "haz amigos" se va 0,5 s antes del corte).
- El momento emocional ("¡ES UN REGALO LA VIDA!") cae sobre planos con gente querida (madre, gente local).
- Final suave: plano tranquilo, sin CTA.

## Cómo se calca (2026-11-03, regalo-la-vida)
1. `yt-dlp` (en `herramientas/.venv/bin/`) → ref a esta carpeta.
2. Cortes: `ffmpeg -vf "scale=180:320,select='gt(scene,0.12)',metadata=print"` y revisar los dudosos (score < 0,3) a 30 fps.
3. Textos: OCR con `tesseract --psm 7` sobre la franja del texto a 10 fps (ruidoso, pero da los instantes de cambio) + hojas de contactos a 2 fps de esa franja para leerlos.
4. Audio: `ffmpeg -vn -c:a copy` de la ref.
5. Elegir un clip de `recursos/` por plano que case con la frase y con el **tipo de plano** de la ref (ver la tabla en el comentario de `estudio/src/videos/regalo-la-vida/RegaloLaVida.tsx`).

## Correcciones de Lucas
_Ninguna todavía._
