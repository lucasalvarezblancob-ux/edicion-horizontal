import React, { useMemo } from "react";
import {
  AbsoluteFill,
  Easing,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { ACENTO, SUB_FONT, TITLE_FONT } from "./marca";

// Color y fuentes en ./marca.ts (local de cada carpeta). Se reexportan para los vídeos que los importan de aquí.
export { ACENTO, TITLE_FONT };

// clave: resalta ESA palabra en el acento (sin depender del regex). mayus: se escribe en mayúsculas (códigos: ALVAREZ10).
export type Palabra = { w: string; start: number; end: number; clave?: boolean; mayus?: boolean };

// Palabras que se resaltan en el color de acento
const CLAVE = /^(dorito|truco|espalda|codos|clavícula|dinero|estrella|estiras|dorsal|balanceo|barca|quema|bíceps)$/i;

const limpia = (w: string) => w.replace(/[¿?¡!.,:]/g, "");

type Pagina = { palabras: Palabra[]; start: number; end: number };

const paginar = (palabras: Palabra[], maxHueco = Infinity, maxPalabras = 3, minDur = 0): Pagina[] => {
  const paginas: Pagina[] = [];
  let cur: Palabra[] = [];
  const cerrar = () => {
    if (cur.length) paginas.push({ palabras: cur, start: cur[0].start, end: 0 });
    cur = [];
  };
  palabras.forEach((p, i) => {
    cur.push(p);
    const chars = cur.map((x) => x.w).join(" ").length;
    // minDur: el bloque no se cierra por número de palabras hasta durar ≥ minDur s (evita palabras de 2–3 frames que parpadean)
    const sig = palabras[i + 1];
    const durOk = !sig || sig.start - cur[0].start >= minDur;
    // Fin de frase (. ? !) siempre cierra; la coma, solo si el bloque ya dura lo suficiente (con minDur 0 = como antes)
    if (/[.?!]$/.test(p.w) || (/[,:]$/.test(p.w) && durOk) || (cur.length >= maxPalabras && durOk) || chars > 15) cerrar();
  });
  cerrar();
  // Sin huecos: cada página dura hasta que empieza la siguiente
  paginas.forEach((pg, i) => {
    const fin = pg.palabras[pg.palabras.length - 1].end;
    pg.end = i < paginas.length - 1 ? Math.min(paginas[i + 1].start, fin + maxHueco) : fin + 0.5;
  });
  return paginas;
};

// maxHueco: s máximos que un subtítulo sigue en pantalla tras su última palabra (útil si hay tramos mudos)
// size: px de la letra. SIEMPRE 52 desde 2026-11-01 (bicep-fah: "algo más pequeños"; antes 62, y antes 76)
// fuente: cambia la letra solo en ese vídeo (por defecto Montserrat 800). Ej. bicep-fah: Inter 600 tipo "Classic" de Instagram
// maxPalabras: palabras por bloque. SIEMPRE 1 (palabra a palabra) desde 2026-11-01 (bicep-fah: "acuérdate de que vaya palabra a palabra"); antes 3
// minDur: junta palabras rápidas hasta que el bloque dure ≥ minDur s. NO usar por defecto: Lucas quiere palabra a palabra estricto
// cortes: s (en tiempo de `palabras`) donde ningún subtítulo puede seguir en pantalla (cambios de plano/persona)
export const Subtitulos: React.FC<{ palabras: Palabra[]; offset: number; claves?: RegExp; top?: number; maxHueco?: number; size?: number; cortes?: number[]; maxPalabras?: number; minDur?: number; fuente?: { family: string; weight: number; tracking?: number } }> = ({
  palabras,
  offset,
  claves = CLAVE,
  top = 1180,
  maxHueco,
  size = 52,
  cortes,
  maxPalabras = 1,
  minDur = 0,
  fuente,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps - offset;
  const paginas = useMemo(() => {
    const pgs = paginar(palabras, maxHueco, maxPalabras, minDur);
    if (cortes) for (const pg of pgs) { const c = cortes.find((x) => x > pg.start + 0.01); if (c !== undefined) pg.end = Math.min(pg.end, c); }
    return pgs;
  }, [palabras, maxHueco, cortes, maxPalabras, minDur]);
  const pg = paginas.find((p) => t >= p.start && t < p.end);
  if (!pg) return null;

  const entrada = interpolate(t - pg.start, [0, 0.12], [0.85, 1], {
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.back(2)),
  });

  return (
    <AbsoluteFill
      style={{ justifyContent: "flex-start", alignItems: "center", paddingTop: top }}
    >
      <div
        style={{
          fontFamily: fuente?.family ?? SUB_FONT,
          fontWeight: fuente?.weight ?? 800,
          fontSize: size,
          lineHeight: 1.1,
          textAlign: "center",
          maxWidth: 900,
          transform: `scale(${entrada})`,
          textTransform: "lowercase",
          letterSpacing: fuente?.tracking ?? -1,
        }}
      >
        {pg.palabras.map((p, i) => {
          const activa = t >= p.start;
          return (
            <span
              key={i}
              style={{
                color: p.clave || claves.test(limpia(p.w)) ? ACENTO : "white",
                textTransform: p.mayus ? "uppercase" : undefined,
                opacity: activa ? 1 : 0.55,
                textShadow: "0 4px 18px rgba(0,0,0,0.75), 0 2px 4px rgba(0,0,0,0.9)",
                marginRight: Math.round(size * 0.24),
                display: "inline-block",
              }}
            >
              {limpia(p.w)}
            </span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

// Título estilo "receta saludable" + subtítulo fino
export const Titulo: React.FC<{ titulo: string; sub: string; top?: number }> = ({ titulo, sub, top = 430 }) => {
  const frame = useCurrentFrame();
  const o = interpolate(frame, [0, 8], [0, 1], { extrapolateRight: "clamp" });
  const y = interpolate(frame, [0, 10], [20, 0], {
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });
  return (
    <AbsoluteFill
      style={{ alignItems: "center", paddingTop: top, opacity: o, transform: `translateY(${y}px)` }}
    >
      <div
        style={{
          fontFamily: TITLE_FONT,
          fontWeight: 700,
          fontSize: 92,
          color: ACENTO,
          textShadow: "0 4px 24px rgba(0,0,0,0.55)",
          letterSpacing: -1,
        }}
      >
        {titulo}
      </div>
      <div
        style={{
          fontFamily: TITLE_FONT,
          fontWeight: 500,
          fontSize: 40,
          color: "white",
          fontStyle: "italic",
          marginTop: 6,
          textShadow: "0 2px 12px rgba(0,0,0,0.8)",
        }}
      >
        {sub}
      </div>
    </AbsoluteFill>
  );
};

// Etiqueta de cada clave: "1 · agarre ancho"
export const Clave: React.FC<{ n: number | string; texto: string }> = ({ n, texto }) => {
  const frame = useCurrentFrame();
  const s = interpolate(frame, [0, 6], [0.6, 1], {
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.back(2.5)),
  });
  const o = interpolate(frame, [0, 4], [0, 1], { extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ alignItems: "center", paddingTop: 300 }}>
      <div
        style={{
          fontFamily: TITLE_FONT,
          fontWeight: 700,
          fontSize: 54,
          color: "white",
          opacity: o,
          transform: `scale(${s})`,
          display: "flex",
          alignItems: "center",
          gap: 18,
          textShadow: "0 3px 16px rgba(0,0,0,0.8)",
        }}
      >
        <span
          style={{
            background: ACENTO,
            color: "#1a1a1a",
            width: 70,
            height: 70,
            borderRadius: 35,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            textShadow: "none",
            fontSize: typeof n === "string" ? 30 : undefined,
          }}
        >
          {n}
        </span>
        {texto}
      </div>
    </AbsoluteFill>
  );
};
