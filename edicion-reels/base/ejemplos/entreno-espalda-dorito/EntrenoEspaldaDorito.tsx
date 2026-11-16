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
import palabrasVoz from "./voz-palabras.json";

// Narrador 3.ª persona (estilo Ariana): "Este es Lucas y quiere tener una espalda Dorito…"
// Proxies 4K (2160×3840, proxy.sh … 2160) en public/entreno-espalda-dorito/c<IMG>.mp4. Brutos en recursos/gym/espalda/ (ver recursos/INDICE.md):
//   c1085 jalon-agarre-estrecho_sudadera-y-sin-camiseta (sudadera 0–12 · se la quita 14–15,5 · espaldas 19–33 · 3/4 33,5–40)
//   c1086 jalon-barra-ancha-sin-camiseta_lateral-y-espalda (lado 0–8 · espaldas 10–17)
//   c1092 dominadas-sin-camiseta · c1090 remo-polea-baja-agarre-cerrado-sin-camiseta_espalda (cerca)
// Render con --scale=2 → 2160×3840.
const clip = (id: string) => staticFile(`entreno-espalda-dorito/c${id}.mp4`);
const VOZ_DESDE = 3;
const SIGUEME = 818; // "Sígueme" @815 + VOZ_DESDE
const DURACION = 871;

type Plano = {
  name: string;
  c: string;
  t: number; // segundo del clip donde empieza
  d: number; // frames
  zoom?: number;
  origen?: string;
  punch?: number;
  rate?: number;
  brillo?: boolean; // dorsales iluminados
};

const PLANOS: Plano[] = [
  // ── Gancho: "Este es Lucas y quiere tener una espalda Dorito. Si tuviera que recomendarle un entreno, sería este."
  { name: "Intro · jalón con sudadera (este es Lucas)", c: "1085", t: 1.0, d: 38, punch: 0.15 },
  { name: "Se quita la sudadera (quiere tener una espalda)", c: "1085", t: 14.3, d: 14, rate: 1.6, zoom: 1.1, origen: "60% 40%" },
  { name: "Espalda · dorsales se iluminan (Dorito)", c: "1085", t: 23.5, d: 44, zoom: 1.2, origen: "50% 45%", brillo: true },
  { name: "Flash · dominadas", c: "1092", t: 3.0, d: 11, zoom: 1.15, origen: "50% 35%" },
  { name: "Flash · jalón ancho de lado", c: "1086", t: 4.4, d: 12, zoom: 1.15, origen: "55% 40%" },
  { name: "Flash · remo agarre cerrado", c: "1090", t: 4.5, d: 12, zoom: 1.25, origen: "50% 40%" },
  // ── 1 Dominadas (un ángulo: abierto/cerrado en cada extremo)
  { name: "Dominadas · abierto", c: "1092", t: 1.5, d: 45 },
  { name: "Dominadas · espalda cerrado (a lo ancho)", c: "1092", t: 3.0, d: 39, zoom: 1.45, origen: "50% 30%" },
  { name: "Dominadas · abierto 2 (pecho por delante)", c: "1092", t: 4.3, d: 30, zoom: 1.05 },
  { name: "Dominadas · cerrado 2 (baje controlado)", c: "1092", t: 5.3, d: 36, zoom: 1.4, origen: "50% 30%" },
  { name: "Dominadas · abierto 3 (columpio)", c: "1092", t: 6.5, d: 26, zoom: 1.1, origen: "50% 35%" },
  // ── 2 Jalón barra ancha (espaldas ↔ lado, cortes en los extremos)
  { name: "Jalón ancho · espaldas (sube a arriba)", c: "1086", t: 11.6, d: 42, zoom: 1.1, origen: "50% 35%" },
  { name: "Jalón ancho · lado arriba → abajo (codos)", c: "1086", t: 6.5, d: 38, zoom: 1.1, origen: "60% 40%" },
  { name: "Jalón ancho · espaldas abajo (la barra no le ha hecho nada)", c: "1086", t: 14.75, d: 46, zoom: 1.25, origen: "50% 35%" },
  // ── 3 Jalón agarre estrecho (espaldas ↔ 3/4)
  { name: "Estrecho · espaldas → abajo", c: "1085", t: 26.9, d: 45, zoom: 1.05 },
  { name: "Estrecho · 3/4 abajo → arriba (estirar el dorsal)", c: "1085", t: 36.0, d: 39, zoom: 1.15, origen: "45% 40%" },
  { name: "Estrecho · espaldas cerrado (aguante abajo)", c: "1085", t: 31.6, d: 48, zoom: 1.4, origen: "50% 40%" },
  { name: "Estrecho · 3/4 (autobús)", c: "1085", t: 35.6, d: 28, zoom: 1.1, origen: "45% 40%" },
  // ── 4 Remo en polea baja con AGARRE CERRADO (c1090: triángulo, codos pegados → más dorsal = más V; corrección de Lucas 2026-11-02:
  //    el agarre abierto (c1089) carga más la parte alta de la espalda y no se mezcla con el cerrado). Un ángulo: abierto/cerrado
  //    en cada extremo (codos atrás ≈4,5 · 6,6; brazos estirados ≈5,85)
  { name: "Remo cerrado · abierto → codos atrás", c: "1090", t: 3.6, d: 27, zoom: 1.1, origen: "50% 40%" },
  { name: "Remo cerrado · espalda cerrado (polea baja)", c: "1090", t: 4.5, d: 40, zoom: 1.4, origen: "50% 38%" },
  { name: "Remo cerrado · abierto 2 (pecho fuera)", c: "1090", t: 5.85, d: 23 },
  { name: "Remo cerrado · espalda cerrado 2 (escápulas, lápiz)", c: "1090", t: 6.6, d: 57, zoom: 1.35, origen: "50% 38%" },
  // ── Remate (2026-11-02, pedido de Lucas): "Y una vez más, Lucas demuestra que si él puede, tú también."
  { name: "Remate · espalda en V, jalón estrecho abajo (Lucas demuestra)", c: "1085", t: 27.8, d: 38, zoom: 1.15, origen: "50% 40%" },
  { name: "Remate · dominadas (si él puede, tú también)", c: "1092", t: 7.6, d: 40, zoom: 1.2, origen: "50% 35%" },
  // ── Cierre: "Sígueme para más." — se gira a cámara al acabar las dominadas, a cámara lenta
  { name: "Cierre · se gira a cámara (lento)", c: "1092", t: 9.9, d: DURACION - SIGUEME, punch: 0.18, rate: 0.6 },
];

type Tipo = "pan" | "zoom" | "giro";
// cambio de ejercicio: transición + whoosh (solo ahí)
const TRANS: [number, Tipo][] = [
  [131, "pan"],
  [307, "zoom"],
  [433, "giro"],
  [593, "pan"],
  [740, "zoom"],
];
const BLOQUES: [number, number][] = [
  [131, 176],
  [307, 126],
  [433, 160],
  [593, 147],
];
const ETIQUETAS = ["dominadas", "jalón con barra ancha", "jalón con agarre estrecho", "remo en polea · agarre cerrado"];
// Series × reps por bloque (2026-11-03, pedido de Lucas; cifras propuestas por Claude, pendientes de que las confirme).
// Van en tarjeta bajo la etiqueta; la voz no las dice.
const SERIES = ["4 × 8", "4 × 10", "3 × 12", "3 × 12"];
const SERIES_TOP = [1290, 1290, 1290, 1290]; // bajo los subtítulos: arriba tapaba la cabeza (remo) y el cartel blanco del Gold's (jalón ancho)
const SERIES_RETRASO = 10; // entra justo después de la etiqueta
const TITULO: [number, number] = [96, 35]; // en "entreno"
const BRILLO: [number, number] = [52, 96]; // plano de los dorsales iluminados
const NOMBRE: [number, number] = [13, 25]; // entra cuando dice "Lucas" (@10 + VOZ_DESDE) y se va con el corte
const CLAVES =
  /^(dorito|espalda|entreno|dominadas|ancho|pecho|columpio|ancha|codos|nada|estrecho|dorsal|abajo|autobús|remo|escápulas|lápiz|puede|también)$/i;

// Subtítulos: "este es," (la pegatina dice "Lucas"); "es," cierra el bloque para que "y" no se junte
const PALABRAS = (palabrasVoz as Palabra[]).flatMap((p, i) => (i === 2 ? [] : i === 1 ? [{ ...p, w: "es," }] : [p]));

const Shot: React.FC<{ children: React.ReactNode; punch?: number; zoom?: number; origen?: string }> = ({
  children,
  punch = 0.07,
  zoom = 1,
  origen = "50% 45%",
}) => {
  const frame = useCurrentFrame();
  const p = interpolate(frame, [0, 7], [punch, 0], {
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });
  const drift = frame * 0.0007;
  return (
    <AbsoluteFill style={{ transform: `scale(${zoom + p + drift})`, transformOrigin: origen }}>{children}</AbsoluteFill>
  );
};

// Brillo rojo en los dorsales (regla: zona que se trabaja en rojo #FF1A1A, overlay). Cámara fija y sentado:
// la espalda apenas se mueve, así que va fijo y late con la rep (máximo con la barra abajo, t≈24,0–24,5 del clip).
const DORSALES = [
  { x: 498, y: 1035 },
  { x: 742, y: 1035 },
];
const ROJO = "#FF1A1A";
const BrilloDorsales: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = 23.5 + frame / fps;
  const pulso = interpolate(t, [23.6, 24.0, 24.5, 24.9], [0.2, 1, 1, 0.45], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const entra = interpolate(frame, [0, 8], [0, 1], { extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const sale = interpolate(frame, [36, 44], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const o = entra * sale * (0.55 + 0.45 * pulso);
  return (
    <AbsoluteFill style={{ pointerEvents: "none", mixBlendMode: "overlay", opacity: o }}>
      {DORSALES.map((p, k) => (
        <div
          key={k}
          style={{
            position: "absolute",
            left: p.x - 100,
            top: p.y - 165,
            width: 200,
            height: 330,
            borderRadius: "50%",
            background: `radial-gradient(ellipse at center, ${ROJO}dd 0%, ${ROJO}99 35%, ${ROJO}33 55%, ${ROJO}00 70%)`,
            filter: "blur(12px)",
            transform: `rotate(${k === 0 ? -16 : 16}deg) scale(${1 + 0.06 * pulso})`,
          }}
        />
      ))}
    </AbsoluteFill>
  );
};

// Tarjeta de cifra (como rutina-hyrox-series, algo más pequeña porque va bajo la etiqueta)
const Cifra: React.FC<{ valor: string; texto: string; top: number }> = ({ valor, texto, top }) => {
  const frame = useCurrentFrame();
  const s = interpolate(frame, [0, 7], [0.5, 1], {
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.back(2.6)),
  });
  const o = interpolate(frame, [0, 4], [0, 1], { extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ alignItems: "center", paddingTop: top, opacity: o }}>
      <div style={{ transform: `scale(${s})`, textAlign: "center", fontFamily: TITLE_FONT }}>
        <div
          style={{
            fontWeight: 700,
            fontSize: 130,
            lineHeight: 1,
            color: ACENTO,
            letterSpacing: -2,
            textShadow: "0 6px 30px rgba(0,0,0,0.7)",
          }}
        >
          {valor}
        </div>
        <div
          style={{
            fontWeight: 700,
            fontSize: 44,
            color: "white",
            marginTop: 2,
            textShadow: "0 3px 16px rgba(0,0,0,0.85)",
          }}
        >
          {texto}
        </div>
      </div>
    </AbsoluteFill>
  );
};

const efectoTransicion = (frame: number) => {
  let blur = 0;
  let scale = 0;
  let tx = 0;
  let rot = 0;
  for (const [c, tipo] of TRANS) {
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

export const EntrenoEspaldaDorito: React.FC = () => {
  const { fps, durationInFrames } = useVideoConfig();
  const frame = useCurrentFrame();
  const { blur, scale, tx, rot } = efectoTransicion(frame);

  const flash = interpolate(frame, [SIGUEME - 1, SIGUEME, SIGUEME + 6], [0, 0.85, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const fadeOut = interpolate(frame, [durationInFrames - 8, durationInFrames], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

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
          {PLANOS.map((p) => (
            <Series.Sequence key={p.name} name={p.name} durationInFrames={p.d} premountFor={fps}>
              <Shot punch={p.punch} zoom={p.zoom} origen={p.origen}>
                <Video
                  src={clip(p.c)}
                  trimBefore={Math.round(p.t * fps)}
                  playbackRate={p.rate ?? 1}
                  muted
                  style={{ width: "100%", height: "100%" }}
                />
                {p.brillo ? <BrilloDorsales /> : null}
              </Shot>
            </Series.Sequence>
          ))}
        </Series>
      </AbsoluteFill>

      <AbsoluteFill style={{ backgroundColor: "white", opacity: flash, pointerEvents: "none" }} />

      {/* Textos */}
      <Sequence name="Nombre a mano (Lucas)" from={NOMBRE[0]} durationInFrames={NOMBRE[1]} layout="none">
        <NombrePegatina nombre="Lucas" cabeza={{ x: 810, y: 640 }} />
      </Sequence>
      <Sequence name="Título" from={TITULO[0]} durationInFrames={TITULO[1]} layout="none">
        <Titulo titulo="espalda dorito" sub="4 ejercicios" top={300} />
      </Sequence>
      {BLOQUES.map(([from, d], k) => (
        <Sequence key={k} name={`${k + 1} · ${ETIQUETAS[k]}`} from={from} durationInFrames={d} layout="none">
          <Clave n={k + 1} texto={ETIQUETAS[k]} />
        </Sequence>
      ))}
      {BLOQUES.map(([from, d], k) => (
        <Sequence
          key={`s${k}`}
          name={`${SERIES[k]} · series × reps`}
          from={from + SERIES_RETRASO}
          durationInFrames={d - SERIES_RETRASO}
          layout="none"
        >
          <Cifra valor={SERIES[k]} texto="series × repeticiones" top={SERIES_TOP[k]} />
        </Sequence>
      ))}
      <Sequence name="@ Instagram" from={SIGUEME} layout="none">
        <Handle />
      </Sequence>

      <Subtitulos
        palabras={PALABRAS}
        offset={VOZ_DESDE / fps}
        top={frame >= BRILLO[0] && frame < BRILLO[1] ? 1390 : 1180} // con los dorsales iluminados, por debajo de la espalda
        claves={CLAVES}
      />

      {/* Audio */}
      <Sequence name="Voz" from={VOZ_DESDE} layout="none">
        <Audio src={staticFile("entreno-espalda-dorito/voz.mp3")} volume={1} />
      </Sequence>
      <Sequence name="sfx brillo dorsales" from={BRILLO[0]} durationInFrames={55} layout="none">
        <Audio src={staticFile("sonidos/chime.mp3")} volume={0.16} />
      </Sequence>
      <Sequence name="sfx título" from={TITULO[0] - 2} durationInFrames={55} layout="none">
        <Audio src={staticFile("sonidos/sparkle.mp3")} volume={0.22} />
      </Sequence>
      <Sequence name="pop nombre" from={NOMBRE[0]} durationInFrames={20} layout="none">
        <Audio src={staticFile("sonidos/pop.mp3")} volume={0.45} />
      </Sequence>
      <Sequence name="pop @" from={SIGUEME} durationInFrames={20} layout="none">
        <Audio src={staticFile("sonidos/pop.mp3")} volume={0.2} />
      </Sequence>
      {BLOQUES.map(([from], k) => (
        <Sequence key={`pop${k}`} name={`pop series ${k + 1}`} from={from + SERIES_RETRASO} durationInFrames={20} layout="none">
          <Audio src={staticFile("sonidos/pop.mp3")} volume={0.2} />
        </Sequence>
      ))}
      {TRANS.map(([c]) => (
        <Sequence key={c} name={`whoosh ${c}`} from={c - 7} durationInFrames={20} layout="none">
          <Audio src={staticFile("sonidos/whoosh.mp3")} volume={0.35} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};

export const EntrenoEspaldaDoritoComp = () => (
  <Composition
    id="EntrenoEspaldaDorito"
    component={EntrenoEspaldaDorito}
    durationInFrames={DURACION}
    fps={30}
    width={1080}
    height={1920}
  />
);
