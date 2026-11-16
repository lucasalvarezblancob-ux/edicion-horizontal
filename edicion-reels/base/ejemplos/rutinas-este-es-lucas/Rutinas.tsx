import { Audio, Video } from "@remotion/media";
import React from "react";
import {
  AbsoluteFill,
  Composition,
  Easing,
  interpolate,
  Sequence,
  Series,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { ACENTO, Clave, Palabra, Subtitulos, Titulo, TITLE_FONT } from "../../comun/Subtitulos";
import { NombrePegatina } from "../../comun/NombrePegatina";
import { Handle } from "../movilidad-hombro/MovilidadHombro";
import pechoTrack from "../entreno-empuje/pecho-track.json";

// Plantilla "Este es Lucas…" (narrador 3.ª persona estilo Ariana) para series de vídeos hechos con recursos.
// Cada vídeo = una entrada de versiones.json: segmentos de guion (frase → tomas que la ilustran) + bloques con etiqueta
// numerada (Clave) y tarjeta de cifra (series × reps, cantidades…). El montaje se calcula solo a partir de los tiempos
// de la voz: cada segmento ocupa lo que dura su frase y se rellena con planos de sus tomas, cortando en las paradas del
// movimiento (paradas.json, de herramientas/puntos_movimiento.py) para que los cortes caigan en los extremos de la rep.
// Primera serie: rutinas de espalda y pecho (2026-11-05). Proxies 4K en public/rutinas-este-es-lucas/ (proxy.sh … 2160);
// brutos en recursos/gym/{espalda,pecho,fisico}/ — id del proxy = c<IMG> (Gold's 2026-11-01), d<C####> (Devant, Sony),
// e8416 (jalón tirantes negra), j1031 (jalón 2026-10-31), p3989 / p7629 (press con mancuernas). Ver recursos/INDICE.md.

export type Toma = {
  c: string; // id del clip (archivo <carpeta>/<c>.mp4)
  a: number; // s del clip: desde
  b: number; // s del clip: hasta
  z?: number; // zoom
  o?: string; // transform-origin
  r?: number; // velocidad
  punch?: number;
  fijo?: boolean; // plano exacto a→b (una vez por segmento)
  brillo?: boolean; // pecho iluminado en rojo (c1048 desde 13,3 s)
  exp?: number; // exposición del plano (regla 2026-11-02: planos muy claros bajo subtítulos → brightness 0,85 / 0,80)
};
export type Seg = { txt: string; tomas: Toma[]; b?: number; dur?: number; titulo?: boolean; cierre?: boolean };
export type Bloque = { n?: string; etiqueta: string; valor?: string; texto?: string };
export type Version = {
  titulo?: [string, string];
  cabeza: { x: number; y: number };
  claves: string;
  bloques: Bloque[];
  segs: Seg[];
  brillo?: string;
  subTop?: number;
  cifraTop?: number;
  dur?: number; // duración objetivo de plano por defecto (s)
};
type Paradas = Record<string, { dur: number; paradas: number[] }>;

const FPS = 30;
const VOZ_DESDE = 3;
type Tipo = "pan" | "zoom" | "giro";
const TIPOS: Tipo[] = ["pan", "zoom", "giro"];

type Plano = Toma & { t: number; d: number; name: string };

export type Plan = {
  planos: Plano[];
  duracion: number;
  segIni: number[];
  nombre: [number, number];
  sigueme: number;
  trans: [number, Tipo][];
  bloques: { from: number; d: number }[];
  titulo?: [number, number];
  brillo?: [number, number];
  palabras: Palabra[];
};

const snapArriba = (par: number[], t: number, hasta: number) => par.find((p) => p >= t - 0.03 && p <= hasta - 0.5) ?? t;

export const planificar = (v: Version, palabras: Palabra[], paradas: Paradas): Plan => {
  const seg0: number[] = [];
  let idx = 0;
  for (const s of v.segs) {
    seg0.push(idx);
    idx += s.txt.split(/\s+/).filter(Boolean).length;
  }
  if (idx !== palabras.length) throw new Error(`palabras ${palabras.length} ≠ guion ${idx}`);
  const fin = palabras[palabras.length - 1].end;
  const duracion = Math.round((fin + VOZ_DESDE / FPS) * FPS) + 27;
  const segIni = seg0.map((w, i) => (i === 0 ? 0 : Math.round((palabras[w].start + VOZ_DESDE / FPS) * FPS) - 2));
  const segFin = segIni.map((_, i) => (i < segIni.length - 1 ? segIni[i + 1] : duracion));

  const cursor: Record<string, number> = {};
  const planos: Plano[] = [];
  let brillo: [number, number] | undefined;
  v.segs.forEach((seg, si) => {
    const e = segFin[si];
    let f = segIni[si];
    const target = seg.dur ?? v.dur ?? 1.7;
    const usados = new Set<number>();
    let k = 0;
    let vueltas = 0;
    while (f < e && vueltas < 200) {
      vueltas++;
      const ti = k % seg.tomas.length;
      k++;
      const tm = seg.tomas[ti];
      if (tm.fijo && usados.has(ti)) {
        if (seg.tomas.every((x, j) => x.fijo && usados.has(j))) usados.clear();
        continue;
      }
      const r = tm.r ?? 1;
      const info = paradas[tm.c];
      const par = info?.paradas ?? [];
      const durClip = info?.dur ?? tm.b;
      const quedan = e - f;
      let start: number;
      let df: number;
      if (tm.fijo || seg.cierre) {
        usados.add(ti);
        start = tm.a;
        df = seg.cierre ? quedan : Math.min(quedan, Math.round(((tm.b - tm.a) / r) * FPS));
      } else {
        start = cursor[tm.c] ?? tm.a;
        if (start < tm.a || start > tm.b - 0.8) start = tm.a;
        start = snapArriba(par, start, tm.b);
        let disp = (tm.b - start) / r;
        if (disp < 0.5) {
          start = snapArriba(par, tm.a, tm.b);
          disp = (tm.b - start) / r;
        }
        let d: number;
        if (quedan / FPS <= target * 1.5) d = quedan / FPS;
        else {
          const quiero = start + target * r;
          const cand = par.filter((p) => p > start + 0.6 * target * r && p < start + 1.45 * target * r && p <= tm.b);
          d = cand.length ? (cand.reduce((a, b) => (Math.abs(b - quiero) < Math.abs(a - quiero) ? b : a)) - start) / r : target;
        }
        d = Math.min(d, disp);
        df = Math.max(6, Math.round(d * FPS));
      }
      // no dejar colas de menos de 10 frames: el plano se alarga hasta el final del segmento si el clip da
      if (e - (f + df) < 10 && (durClip - start) / r >= (e - f) / FPS) df = e - f;
      df = Math.min(df, e - f);
      if (df <= 0) break;
      if (tm.brillo) brillo = [f, df];
      planos.push({ ...tm, t: start, d: df, name: `${si + 1}·${tm.c}@${start.toFixed(2)} ${seg.txt.slice(0, 28)}` });
      cursor[tm.c] = start + (df / FPS) * r;
      f += df;
    }
  });

  // transiciones: al entrar en cada bloque y en el remate
  const trans: [number, Tipo][] = [];
  const bloques: { from: number; d: number }[] = v.bloques.map(() => ({ from: -1, d: 0 }));
  let ultimoB: number | undefined;
  v.segs.forEach((s, si) => {
    if (s.b !== undefined) {
      if (s.b !== ultimoB) {
        trans.push([segIni[si], TIPOS[trans.length % 3]]);
        bloques[s.b].from = segIni[si];
      }
      bloques[s.b].d = segFin[si] - bloques[s.b].from;
    } else if (ultimoB !== undefined && !s.cierre) {
      trans.push([segIni[si], TIPOS[trans.length % 3]]);
    }
    ultimoB = s.b;
  });

  const nombreIni = Math.round((palabras[2].start + VOZ_DESDE / FPS) * FPS);
  const nombreFin = planos[0].d;
  const iSig = palabras.findIndex((p) => /^sígueme/i.test(p.w));
  const sigueme = Math.round((palabras[iSig].start + VOZ_DESDE / FPS) * FPS);
  const tSeg = v.segs.findIndex((s) => s.titulo);
  const titulo: [number, number] | undefined =
    v.titulo && tSeg >= 0 ? [segIni[tSeg], Math.max(35, segFin[tSeg] - segIni[tSeg])] : undefined;

  // subtítulos: "este es," (la pegatina dice "Lucas")
  const pal = palabras.flatMap((p, i) => (i === 2 ? [] : i === 1 ? [{ ...p, w: "es," }] : [p]));
  return {
    planos,
    duracion,
    segIni,
    nombre: [nombreIni, Math.max(20, nombreFin - nombreIni)],
    sigueme,
    trans,
    bloques,
    titulo,
    brillo,
    palabras: pal,
  };
};

const Shot: React.FC<{ children: React.ReactNode; punch?: number; zoom?: number; origen?: string; exp?: number }> = ({
  children,
  punch = 0.07,
  zoom = 1,
  origen = "50% 45%",
  exp,
}) => {
  const frame = useCurrentFrame();
  const p = interpolate(frame, [0, 7], [punch, 0], { extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const drift = frame * 0.0007;
  return (
    <AbsoluteFill style={{ transform: `scale(${zoom + p + drift})`, transformOrigin: origen, filter: exp && exp !== 1 ? `brightness(${exp})` : undefined }}>
      {children}
    </AbsoluteFill>
  );
};

// Pecho iluminado en rojo (regla 2026-11-01, entreno-empuje): sigue pecho-track.json (c1048 desde 13,3 s)
const PECTORALES = [
  { x: 395, y: 1220 },
  { x: 685, y: 1220 },
];
const ROJO = "#FF1A1A";
const BrilloPecho: React.FC<{ d: number }> = ({ d }) => {
  const frame = useCurrentFrame();
  const track = pechoTrack as number[][];
  const i = Math.min(frame, track.length - 1);
  const [dx, dy] = track[i];
  const win = track.slice(Math.max(0, i - 2), i + 3).map((r) => r[2]);
  const e = win.reduce((a, b) => a + b, 0) / win.length;
  const pulso = interpolate(e, [1.2, 2.6], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const entra = interpolate(frame, [0, 8], [0, 1], { extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const sale = interpolate(frame, [d - 9, d], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const o = entra * sale * (0.55 + 0.45 * pulso);
  return (
    <AbsoluteFill style={{ pointerEvents: "none", mixBlendMode: "overlay", opacity: o }}>
      {PECTORALES.map((p, k) => (
        <div
          key={k}
          style={{
            position: "absolute",
            left: p.x + dx - 165,
            top: p.y + dy - 120,
            width: 330,
            height: 240,
            borderRadius: "50%",
            background: `radial-gradient(ellipse at center, ${ROJO}dd 0%, ${ROJO}99 35%, ${ROJO}33 55%, ${ROJO}00 70%)`,
            filter: "blur(12px)",
            transform: `scale(${1 + 0.06 * pulso})`,
          }}
        />
      ))}
    </AbsoluteFill>
  );
};

// Tarjeta de cifra (series × reps / cantidades): número grande en el acento + qué es debajo, entra con pop suave
const Cifra: React.FC<{ valor: string; texto: string; top: number }> = ({ valor, texto, top }) => {
  const frame = useCurrentFrame();
  const s = interpolate(frame, [0, 7], [0.5, 1], { extrapolateRight: "clamp", easing: Easing.out(Easing.back(2.6)) });
  const o = interpolate(frame, [0, 4], [0, 1], { extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ alignItems: "center", paddingTop: top, opacity: o }}>
      <div style={{ transform: `scale(${s})`, textAlign: "center", fontFamily: TITLE_FONT }}>
        <div style={{ fontWeight: 700, fontSize: 130, lineHeight: 1, color: ACENTO, letterSpacing: -2, textShadow: "0 6px 30px rgba(0,0,0,0.7)" }}>
          {valor}
        </div>
        <div style={{ fontWeight: 700, fontSize: 44, color: "white", marginTop: 2, textShadow: "0 3px 16px rgba(0,0,0,0.85)" }}>{texto}</div>
      </div>
    </AbsoluteFill>
  );
};

const efectoTransicion = (frame: number, trans: [number, Tipo][]) => {
  let blur = 0;
  let scale = 0;
  let tx = 0;
  let rot = 0;
  for (const [c, tipo] of trans) {
    const d = frame - c + 0.5;
    const ad = Math.abs(d);
    const R = 5;
    if (ad >= R) continue;
    const k = 1 - ad / R;
    const k2 = k * k;
    if (tipo === "zoom") {
      blur = Math.max(blur, 16 * k);
      scale = Math.max(scale, 0.16 * k);
    } else if (tipo === "pan") {
      blur = Math.max(blur, 18 * k);
      tx = Math.sign(-d) * -170 * k2;
      scale = Math.max(scale, 0.34 * k);
    } else {
      blur = Math.max(blur, 14 * k);
      rot = Math.sign(d) * 9 * k2;
      scale = Math.max(scale, 0.3 * k);
    }
  }
  return { blur, scale, tx, rot };
};

const SERIES_RETRASO = 10;

export const VideoEsteEsLucas: React.FC<{ carpeta: string; clave: string; v: Version; plan: Plan; musica?: string }> = ({ carpeta, clave, v, plan, musica }) => {
  const { fps, durationInFrames } = useVideoConfig();
  const frame = useCurrentFrame();
  const { blur, scale, tx, rot } = efectoTransicion(frame, plan.trans);
  const { sigueme } = plan;
  const flash = interpolate(frame, [sigueme - 1, sigueme, sigueme + 6], [0, 0.85, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const fadeOut = interpolate(frame, [durationInFrames - 8, durationInFrames], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const claves = new RegExp(`^(${v.claves})$`, "i");
  const enBrillo = plan.brillo && frame >= plan.brillo[0] && frame < plan.brillo[0] + plan.brillo[1];

  return (
    <AbsoluteFill style={{ backgroundColor: "black" }}>
      {/* Color del bruto sin tocar: solo blur en las transiciones */}
      <AbsoluteFill
        style={{
          opacity: fadeOut,
          filter: blur > 0 ? `blur(${blur}px)` : undefined,
          transform: `translateX(${tx}px) rotate(${rot}deg) scale(${1 + scale})`,
        }}
      >
        <Series>
          {plan.planos.map((p, i) => (
            <Series.Sequence key={i} name={p.name} durationInFrames={p.d} premountFor={fps}>
              <Shot punch={p.punch} zoom={p.z} origen={p.o} exp={p.exp}>
                <Video
                  src={staticFile(`${carpeta}/${p.c}.mp4`)}
                  trimBefore={Math.round(p.t * fps)}
                  playbackRate={p.r ?? 1}
                  muted
                  style={{ width: "100%", height: "100%", objectFit: "cover" }}
                />
                {p.brillo ? <BrilloPecho d={p.d} /> : null}
              </Shot>
            </Series.Sequence>
          ))}
        </Series>
      </AbsoluteFill>

      <AbsoluteFill style={{ backgroundColor: "white", opacity: flash, pointerEvents: "none" }} />

      <Sequence name="Nombre a mano (Lucas)" from={plan.nombre[0]} durationInFrames={plan.nombre[1]} layout="none">
        <NombrePegatina nombre="Lucas" cabeza={v.cabeza} />
      </Sequence>
      {plan.titulo && v.titulo ? (
        <Sequence name="Título" from={plan.titulo[0]} durationInFrames={plan.titulo[1]} layout="none">
          <Titulo titulo={v.titulo[0]} sub={v.titulo[1]} top={300} />
        </Sequence>
      ) : null}
      {plan.bloques.map(({ from, d }, k) =>
        from < 0 ? null : (
          <Sequence key={k} name={`${v.bloques[k].n ?? k + 1} · ${v.bloques[k].etiqueta}`} from={from} durationInFrames={d} layout="none">
            <Clave n={v.bloques[k].n ?? k + 1} texto={v.bloques[k].etiqueta} />
          </Sequence>
        ),
      )}
      {plan.bloques.map(({ from, d }, k) =>
        from < 0 || !v.bloques[k].valor ? null : (
          <Sequence key={`s${k}`} name={`${v.bloques[k].valor} · ${v.bloques[k].texto}`} from={from + SERIES_RETRASO} durationInFrames={d - SERIES_RETRASO} layout="none">
            <Cifra valor={v.bloques[k].valor!} texto={v.bloques[k].texto ?? ""} top={v.cifraTop ?? 1290} />
          </Sequence>
        ),
      )}
      <Sequence name="@ Instagram" from={sigueme} layout="none">
        <Handle />
      </Sequence>

      <Subtitulos palabras={plan.palabras} offset={VOZ_DESDE / fps} top={enBrillo ? 1390 : (v.subTop ?? 1180)} claves={claves} />

      <Sequence name="Voz" from={VOZ_DESDE} layout="none">
        <Audio src={staticFile(`${carpeta}/voz-${clave}.mp3`)} volume={1} />
      </Sequence>
      {/* Música de fondo (pedida por Lucas para esta serie, 2026-11-05): ElevenLabs Music, −14 LUFS, a 0,22 bajo la voz; se funde en el último segundo */}
      {musica ? (
        <Audio
          name="Música"
          src={staticFile(`${carpeta}/${musica}`)}
          volume={(f) => 0.22 * interpolate(f, [durationInFrames - 30, durationInFrames - 2], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })}
        />
      ) : null}
      {plan.brillo ? (
        <Sequence name="sfx brillo" from={plan.brillo[0]} durationInFrames={55} layout="none">
          <Audio src={staticFile("sonidos/chime.mp3")} volume={0.16} />
        </Sequence>
      ) : null}
      {plan.titulo ? (
        <Sequence name="sfx título" from={plan.titulo[0] - 2} durationInFrames={55} layout="none">
          <Audio src={staticFile("sonidos/sparkle.mp3")} volume={0.22} />
        </Sequence>
      ) : null}
      <Sequence name="pop nombre" from={plan.nombre[0]} durationInFrames={20} layout="none">
        <Audio src={staticFile("sonidos/pop.mp3")} volume={0.45} />
      </Sequence>
      <Sequence name="pop @" from={sigueme} durationInFrames={20} layout="none">
        <Audio src={staticFile("sonidos/pop.mp3")} volume={0.2} />
      </Sequence>
      {plan.bloques.map(({ from }, k) =>
        from < 0 || !v.bloques[k].valor ? null : (
          <Sequence key={`pop${k}`} name={`pop cifra ${k + 1}`} from={from + SERIES_RETRASO} durationInFrames={20} layout="none">
            <Audio src={staticFile("sonidos/pop.mp3")} volume={0.2} />
          </Sequence>
        ),
      )}
      {plan.trans.map(([c]) => (
        <Sequence key={c} name={`whoosh ${c}`} from={Math.max(0, c - 7)} durationInFrames={20} layout="none">
          <Audio src={staticFile("sonidos/whoosh.mp3")} volume={0.35} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};

// Registra una composición por versión: id = <prefijo>-<clave>
export const crearComps = (
  prefijo: string,
  carpeta: string,
  versiones: Record<string, Version>,
  voces: Record<string, Palabra[]>,
  paradas: Paradas,
  musicas: string[] = [],
) =>
  Object.entries(versiones)
    .filter(([k, v]) => voces[k] && v.segs.every((s) => s.tomas?.length))
    .map(([k, v], i) => {
      const plan = planificar(v, voces[k], paradas);
      return (
        <Composition
          key={k}
          id={`${prefijo}-${k}`}
          component={VideoEsteEsLucas}
          durationInFrames={plan.duracion}
          fps={FPS}
          width={1080}
          height={1920}
          defaultProps={{ carpeta, clave: k, v, plan, musica: musicas.length ? musicas[i % musicas.length] : undefined }}
        />
      );
    });
