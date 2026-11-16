# Proyecto del vídeo "__SLUG__". Lo leen todos los pasos de herramientas/montaje/ (se ejecutan desde esta carpeta).
SLUG = "__SLUG__"
COMP = "__COMP__"                    # id de la composición de capas en estudio/src/Root.tsx
BRUTOS = "__BRUTOS__"                # carpeta (o lista de carpetas) con los brutos; un clip = nombre del archivo sin extensión
FPS = __FPS__                        # los del bruto principal (Sony: 25; iPhone: 30)
ANCHO, ALTO = __ANCHO__, __ALTO__    # lienzo = el del MEJOR bruto, nunca menos
IDIOMA = None                        # idioma HABLADO ("es", "en"…). Lo detecta paso0_preparar.py: ponlo aquí después de comprobarlo.
NUMEROS = {}                         # cifras tal como se dicen, para alinear: {"100": "cien", "15": "quince"} / {"100": "onehundred"}
# Opcionales: ANALISIS (por defecto ../../bruto/<slug>-analisis), ESTUDIO (../../estudio), MUSICA (personal/<creador>/recursos/musica).
CREADOR = "__CREADOR__"       # carpeta de personal/ con la personalización de quien firma el vídeo ("" = solo las bases)
