# Índice de recursos del creador

**Todo** el material de este creador está en esta carpeta (no viene con la skill y no hay otra carpeta de recursos),
**ordenado por carpetas**: aquí suelto solo va este índice. Al añadir o usar un archivo: analízalo, ponlo en su carpeta
y apúntalo en su sección (qué se ve, tramos útiles, en qué vídeos se ha usado). Sin ficha, el clip no existe: al montar
se busca aquí, no mirando carpetas. Rutas relativas a esta carpeta; tiempos en segundos del archivo original.

**Cómo clasificar, analizar y elegir** (vale para cualquier nicho): skill → `base/recursos.md`. Las carpetas de tema
son las de SU contenido (5–8 grandes temas; un segundo nivel cuando una pase de ~15 clips o tenga subtemas claros): se
crean al dar de alta al creador y se apuntan en esta tabla.

**Al usar recursos en un vídeo**: cada plano tiene que enseñar aquello de lo que se habla **desde su primer
fotograma** (manda) y casar con el outfit, los colores y el vibe del resto. Por eso cada clip apunta **Tramos
útiles**, **Outfit**, **Vibe** y **Temas**. Un clip de aquí se pide en `edl.py` y `plan.py` como un bruto, por su
nombre de archivo sin extensión, esté en la carpeta que esté: no repitas nombres entre carpetas.

| Carpeta | Qué va |
|---|---|
| `marca/` | sus archivos fijos ORIGINALES: intro, outro, cortinillas, logos, mascota. Cuándo va cada uno: `../recursos.md` |
| `<tema>/` | clips de archivo y b-roll, por lo que ilustran (una carpeta por cada gran tema de su contenido) |
| `creador/` | él sin acción concreta: a cámara, andando, posados (para ganchos y cierres) |
| `fotos/` | fotos y recortes PNG (tarjetas, capturas) |
| `mapas/` | bases de satélite para mapas animados (`herramientas/mapa_satelite.py`), con su `.json` |
| `musica/` | pistas con licencia + `CATALOGO.md` (BPM, mood, energía, duración, id, dónde se usó) |
| `sonidos/` | efectos propios (los SFX base ya están en `estudio/public/sonidos/`) |

<!-- Formato de cada clip (una línea, en la sección de su carpeta; los de una misma sesión, bajo una cabecera con lo común):
- `<tema>/AAAA-MM-DD_que-se-ve.MP4` (C0123, 4K 25 fps, 42 s): qué se ve. Tramos útiles 2–5 · 8–10 (cámara quieta, sujeto ya en imagen). **Outfit**: … **Vibe**: … **Temas**: … Usado en: <slug>.
-->

## marca/

## creador/

## fotos/

## mapas/

## bruto terminado/
Brutos ya editados (para repasos): `AAAA-MM-DD_<slug-del-edit>_<nn>-<que-se-ve>.ext`.
