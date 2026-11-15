# creadores/ — personalizaciones que vienen con la skill

Cada carpeta es la personalización ya hecha de un creador, lista para instalar en otra carpeta de edición:

- `creadores/<n>/personal/` → se copia a `personal/<n>/` (perfil, preferencias, recursos.md, marca.json, ajustes.py, fichas de refs/).
- `creadores/<n>/estudio/` → se copia a `estudio/` (sus gráficos propios y sus recursos preparados para superponer).
- Sus `recursos/` y lo pesado de `refs/` (vídeos, fotogramas, miniaturas) **no van en git**: están en su disco duro, en
  `<disco>/Horizontal/personal/<n>/`. `recursos/` se enlaza al disco y lo pesado de `refs/` se copia.

Se instala con `instalar.sh --creador <n> "<carpeta>"` (o `instalar.ps1 -Creador <n>`). Si el disco no estaba
conectado o cambió de letra: `bash .claude/skills/edicion-horizontal/conectar_disco.sh <n>`.
Nada se pisa: si `personal/<n>/` ya existe, solo se añade lo que falte.

Lo que el creador corrija después se apunta en SU carpeta (`personal/<n>/`), no aquí. Para actualizar esta copia con
lo aprendido en una carpeta de edición, el autor la vuelve a copiar aquí y publica.
