#!/usr/bin/env bash
# Revisión de color SIN QuickTime (Windows/Linux): bruto vs proxy (o render) tal como los pinta mpv (libplacebo, gestión de
# color y tone mapping HDR→SDR de verdad). Es el equivalente a las capturas de QuickTime de preferencias → COLOR.
# Uso: herramientas/comparar_color.sh BRUTO OTRO "t1 t2 t3" [desfase_s=0]
#   OTRO = proxy (mismo tiempo que el bruto) o un tramo/render: se captura OTRO en t - desfase.
#   Compara la imagen ENTERA → úsalo con el proxy (sin textos ni zoom). Para el render, pasa un instante sin textos.
# Salida: diferencia media por canal (OTRO − BRUTO, en niveles 0–255) en cada instante y capturas en $TMPDIR/comparar_color/.
# Aprobado: |media| ≤ 5 en todos los instantes. Más claro de +5 → el proxy está mal (ver proxy.sh), no se corrige con filtros.
# Necesita mpv (Windows: winget install shinchiro.mpv → "C:\Program Files\MPV Player\mpv.exe").
set -euo pipefail
B="$1"; O="$2"; TS="$3"; DES="${4:-0}"
MPV="$(command -v mpv || true)"; [ -z "$MPV" ] && [ -x "/c/Program Files/MPV Player/mpv.exe" ] && MPV="/c/Program Files/MPV Player/mpv.exe"
[ -z "$MPV" ] && { echo "Falta mpv (Windows: winget install shinchiro.mpv)" >&2; exit 1; }
DIR="$(cd "$(dirname "$0")" && pwd)"; PY="$DIR/.venv/Scripts/python.exe"; [ -x "$PY" ] || PY="$DIR/.venv/bin/python"
OUT="${TMPDIR:-/tmp}/comparar_color"; mkdir -p "$OUT"
cat > "$OUT/cap.lua" <<'LUA'
local out = mp.get_opt("cap-out"); local hecho = false
mp.register_event("playback-restart", function()
  if hecho then return end; hecho = true
  mp.add_timeout(0.8, function() mp.commandv("screenshot-to-file", out, "window"); mp.add_timeout(0.3, function() mp.command("quit") end) end)
end)
LUA
cap() { "$MPV" --no-config --vo=gpu-next --pause --mute=yes --start="$2" --geometry=432x768+0+0 --no-border --osd-level=0 \
  --script="$OUT/cap.lua" --script-opts=cap-out="$3" "$1" >/dev/null 2>&1; }
for t in $TS; do
  to=$(awk -v a="$t" -v b="$DES" 'BEGIN{print a-b}')
  cap "$B" "$t" "$OUT/bruto_$t.png"; cap "$O" "$to" "$OUT/otro_$t.png"
  "$PY" -I -c "
import numpy as np; from PIL import Image
b=np.asarray(Image.open(r'$OUT/bruto_$t.png').convert('RGB')).astype(float); o=np.asarray(Image.open(r'$OUT/otro_$t.png').convert('RGB')).astype(float)
d=o-b; m=d.reshape(-1,3).mean(0)
print(f't=$t  media {d.mean():+.1f}  |dif| {np.abs(d).mean():.1f}  R {m[0]:+.1f} G {m[1]:+.1f} B {m[2]:+.1f}  ' + ('OK' if abs(d.mean())<=5 else 'MAL'))"
done
echo "capturas: $OUT"
