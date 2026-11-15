# personal/ — la PERSONALIZACIÓN de cada creador (local)

La skill `edicion-horizontal` trae unas **bases de edición y efectos** iguales para todos. Esta carpeta es donde se
guarda lo **propio de cada creador**: su intro y su outro, su mascota, sus coletillas, su gusto de música y de ritmo,
y **todos sus recursos** (clips de archivo, b-roll, fotos, mapas, música).
Es local: no está en git, no se sube a ningún sitio y la skill **nunca** la pisa al actualizarse. Lo que hay aquí
**manda sobre las bases** cuando chocan.

Orden (lo de la derecha manda):  **bases de la skill → `personal/<creador>/` → lo que se pida para un vídeo concreto**

Lo normal es **un creador** por carpeta de edición. Si se edita para varios, cada uno tiene la suya:

```
personal/
├── LEEME.md            este archivo
├── _plantilla/         de lo que parte un creador nuevo: cinco archivos vacíos y recursos/ con su índice
└── <creador>/          p. ej. reinoselva/   (se crea con: herramientas/montaje/nuevo_creador.py <creador>)
    ├── perfil.md        quién es: nombre, canal, idioma, nicho, coletillas, cámaras, de dónde saca la música
    ├── preferencias.md  SUS reglas de estilo en palabras (estructura, ritmo, textos, música…). Cada corrección suya, con fecha
    ├── recursos.md      SUS recursos fijos (intro, outro, logo, mascota, botones que usa) y cuándo va cada uno
    ├── marca.json       color de acento, canal, @, código de descuento y logo (lo leen los gráficos). Si tiene una
    │                    marca por idioma (un canal en español y otro en inglés): "idiomas": {"en": {"canal": …,
    │                    "handle": …, "logo": …}}; los campos del idioma del vídeo tapan a los generales
    ├── ajustes.py       los números de la base a su gusto (zooms, efectos de sonido, niveles de música)
    ├── recursos/        TODO su material, ordenado por carpetas (no hay recursos/ en la raíz; nada suelto):
    │   ├── INDICE.md       la ficha de cada archivo: qué se ve, tramos útiles, en qué vídeos se ha usado
    │   ├── marca/          sus archivos fijos ORIGINALES: intro, outro, logos, mascota
    │   ├── <tema>/         sus clips de archivo y b-roll: una carpeta por tema (un recinto, una especie, un viaje…)
    │   ├── creador/        él sin acción concreta: a cámara, andando (para ganchos y cierres)
    │   ├── fotos/  mapas/  sonidos/
    │   └── musica/         sus pistas con licencia + CATALOGO.md
    └── refs/            vídeos suyos de ejemplo y sus fichas: cómo edita él (se analizan con ENCARGO_CREADOR.md)
```

Dos sitios más son del creador, fuera de aquí porque los necesita Remotion:
- `estudio/src/personal/<creador>/Graficos.tsx` — sus **gráficos propios** (la mascota con su burbuja, el logo sobre la
  intro). En `plan.py` se piden con `PROPIOS = [(ancla, segundos, "tipo", {datos})]`.
- `estudio/public/personal/<creador>/` — sus recursos **ya preparados** para superponer (animaciones sin fondo en
  `.webm`, logos en `.png`). Los originales se quedan en `personal/<creador>/recursos/marca/`.

`recursos/` puede estar en **otro disco** si pesa mucho: se mueve allí y en su sitio se deja un enlace a la carpeta
(Windows: `New-Item -ItemType Junction`; macOS: `ln -s`). Todo sigue funcionando igual mientras el disco esté conectado;
si no lo está, se avisa al abrir la sesión.

El vídeo dice de quién es en `out/<slug>/proyecto.py`: `CREADOR = "<creador>"` (si solo hay uno, no hace falta).
Los clips de `personal/<creador>/recursos/` (estén en la carpeta que estén) se usan en el EDL y en el plan como
cualquier bruto, por su nombre sin extensión: `V("intro", 0, 4.8, vol=0)`.

## Qué va aquí y qué no
- **Aquí**: lo que distingue a este creador de otro. «Su intro va tras el gancho», «la tortuga comenta un dato cada
  3 min», «música en todo el vídeo», «no le gustan los efectos en las cifras».
- **En la skill (bases)**: lo que vale para cualquiera. Cómo se corta, cómo se eligen los recursos, que las matrículas
  se difuminan, los botones de YouTube de serie. Solo el autor de la skill cambia las bases.
- Los **recursos de serie** (botones de suscripción, efectos de sonido) vienen con la skill; todo lo demás
  (clips de archivo, b-roll, fotos, mapas, música) es de cada creador y está en su `recursos/`.

## Cómo se usa
No hace falta editar nada a mano: díselo a Claude con tus palabras («los zooms más suaves», «mi color es el naranja»,
«pon siempre mi cabecera después del gancho») y lo apunta en el archivo que toca del creador. Para volver a la base
en algo, se borra esa línea.
