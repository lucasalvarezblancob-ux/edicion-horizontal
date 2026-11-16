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
import { Clave, Palabra, Subtitulos, Titulo } from "../../comun/Subtitulos";
import { NombrePegatina } from "../../comun/NombrePegatina";
import { Handle } from "../movilidad-hombro/MovilidadHombro";
import palabrasV1 from "./voz-palabras.json";
import palabrasV2 from "./voz-v2-palabras.json";
import pechoTrack from "./pecho-track.json";

// Proxies 1080×1920 a 30 fps en public/entreno-empuje/c<IMG>.mp4. Brutos en recursos/gym/{fisico,pecho,hombro,triceps}/ (ver recursos/INDICE.md):
//   c1048 espejo-sin-camiseta-moviendo-pecho · c1034 press-inclinado-maquina · c1035 press-cerrado-maquina
//   c1037 press-plano-maquina-sentado · c1038 elevaciones-laterales-maquina · c1039 triceps-polea-golds-gym
const clip = (id: string) => staticFile(`entreno-empuje/c${id}.mp4`);
const VOZ_DESDE = 3;
// V1 (programada): "Si quieres conseguir unas tetas grandes…" · V2: narrador estilo Ariana "Este es Lucas y quiere hacer crecer su pecho…"
const DURACION_V1 = 895;
const SIGUEME_V1 = 852;
const DURACION_V2 = 990;
const SIGUEME_V2 = 944;

type Plano = {
  name: string;
  c: string; // id del clip
  t: number; // segundo del clip donde empieza
  d: number; // frames
  zoom?: number;
  origen?: string;
  punch?: number;
  rate?: number;
  brillo?: boolean; // pectorales iluminados
};

// Un solo ángulo por ejercicio: tiempo continuo y cambio de encuadre (abierto/cerrado) en cada extremo de la rep.
const PLANOS_V1: Plano[] = [
  // ── Gancho: "Si quieres conseguir unas tetas grandes, apúntate este entreno de empuje."
  { name: "Intro · espejo", c: "1048", t: 2.9, d: 29, punch: 0.15 },
  { name: "Pecho · se ilumina (tetas grandes)", c: "1048", t: 13.3, d: 42, zoom: 1.35, origen: "50% 62%", brillo: true },
  { name: "Flash · press inclinado", c: "1034", t: 5.77, d: 9, zoom: 1.15 },
  { name: "Flash · elevaciones", c: "1038", t: 5.6, d: 8, zoom: 1.15, origen: "45% 30%" },
  { name: "Flash · tríceps", c: "1039", t: 3.87, d: 8, zoom: 1.25, origen: "45% 85%" },
  // ── 1 Press inclinado en máquina
  { name: "Inclinado · abierto", c: "1034", t: 0.2, d: 43 },
  { name: "Inclinado · cerrado (arriba del pecho)", c: "1034", t: 1.63, d: 35, zoom: 1.4, origen: "50% 35%" },
  { name: "Inclinado · abierto 2 (bajas controlado)", c: "1034", t: 2.8, d: 51, zoom: 1.05 },
  { name: "Inclinado · cerrado 2 (dinero)", c: "1034", t: 4.5, d: 51, zoom: 1.45, origen: "50% 38%" },
  // ── 2 Press cerrado
  { name: "Cerrado · abierto", c: "1035", t: 0.4, d: 54 },
  { name: "Cerrado · agarre estrecho (cerrado)", c: "1035", t: 2.2, d: 32, zoom: 1.45, origen: "40% 50%" },
  { name: "Cerrado · abierto 2 (a sufrir)", c: "1035", t: 3.27, d: 39, zoom: 1.1 },
  // ── 3 Press plano en máquina (sentado)
  { name: "Plano · abierto", c: "1037", t: 1.27, d: 36 },
  { name: "Plano · manos/pecho", c: "1037", t: 2.47, d: 43, zoom: 1.4, origen: "50% 42%" },
  { name: "Plano · abierto 2", c: "1037", t: 3.9, d: 41, zoom: 1.05 },
  { name: "Plano · pecho (las tetas)", c: "1037", t: 5.27, d: 28, zoom: 1.3, origen: "50% 40%" },
  { name: "Plano · cara (uf, cómo quema)", c: "1037", t: 6.2, d: 27, zoom: 1.55, origen: "50% 32%" },
  // ── 4 Elevaciones laterales en máquina
  { name: "Elevaciones · abierto", c: "1038", t: 4.27, d: 35 },
  { name: "Elevaciones · hombro cerrado", c: "1038", t: 5.43, d: 48, zoom: 1.4, origen: "40% 24%" },
  { name: "Elevaciones · abierto 2 (barca)", c: "1038", t: 7.03, d: 47, zoom: 1.1 },
  // ── 5 Tríceps en polea (encuadre hacia abajo: el cartel de Gold's Gym no tapa la etiqueta)
  { name: "Tríceps · abierto", c: "1039", t: 2.53, d: 40, zoom: 1.22, origen: "45% 82%" },
  { name: "Tríceps · brazos cerrado", c: "1039", t: 3.87, d: 42, zoom: 1.45, origen: "40% 60%" },
  { name: "Tríceps · abierto 2 (abajo del todo)", c: "1039", t: 5.27, d: 28, zoom: 1.25, origen: "45% 82%" },
  // ── Remate: "Que no todo es hacer bíceps." — vuelta al espejo
  { name: "Remate · espejo", c: "1048", t: 8.0, d: 36, zoom: 1.1 },
  // ── Cierre: "Sígueme para más." — espejo a cámara lenta
  { name: "Cierre · espejo lento", c: "1048", t: 12.0, d: DURACION_V1 - SIGUEME_V1, punch: 0.18, rate: 0.75 },
];

type Tipo = "pan" | "zoom" | "giro";
const TRANS_V1: [number, Tipo][] = [
  [96, "pan"],
  [276, "zoom"],
  [401, "giro"],
  [576, "pan"],
  [706, "zoom"],
  [816, "giro"],
];

// ── V2: narrador en 3.ª persona (estilo Ariana). Voz en voz-v2.mp3.
const PLANOS_V2: Plano[] = [
  // "Este es Lucas y quiere hacer crecer su pecho. Si tuviera que recomendarle un entreno, sería este."
  { name: "Intro · espejo (este es Lucas)", c: "1048", t: 2.9, d: 44, punch: 0.15 },
  { name: "Pecho · se ilumina (crecer su pecho)", c: "1048", t: 13.3, d: 42, zoom: 1.35, origen: "50% 62%", brillo: true },
  { name: "Espejo · recomendarle", c: "1048", t: 8.0, d: 15, zoom: 1.1 },
  { name: "Flash · press inclinado", c: "1034", t: 5.77, d: 12, zoom: 1.15 },
  { name: "Flash · elevaciones", c: "1038", t: 5.6, d: 12, zoom: 1.15, origen: "45% 30%" },
  { name: "Flash · tríceps", c: "1039", t: 3.87, d: 11, zoom: 1.25, origen: "45% 85%" },
  // ── 1 Press inclinado en máquina
  { name: "Inclinado · abierto", c: "1034", t: 0.2, d: 43 },
  { name: "Inclinado · cerrado (arriba del pecho)", c: "1034", t: 1.63, d: 35, zoom: 1.4, origen: "50% 35%" },
  { name: "Inclinado · abierto 2 (baje controlado)", c: "1034", t: 2.8, d: 51, zoom: 1.05 },
  { name: "Inclinado · cerrado 2 (con arte)", c: "1034", t: 4.5, d: 21, zoom: 1.45, origen: "50% 38%" },
  // ── 2 Press cerrado
  { name: "Cerrado · abierto", c: "1035", t: 0.4, d: 54 },
  { name: "Cerrado · agarre estrecho (cerrado)", c: "1035", t: 2.2, d: 32, zoom: 1.45, origen: "40% 50%" },
  { name: "Cerrado · abierto 2 (con confianza)", c: "1035", t: 3.27, d: 59, zoom: 1.1 },
  { name: "Cerrado · cerrado 2 (técnica)", c: "1035", t: 5.23, d: 40, zoom: 1.4, origen: "40% 50%" },
  // ── 3 Press plano en máquina (sentado)
  { name: "Plano · abierto", c: "1037", t: 1.27, d: 36 },
  { name: "Plano · manos/pecho", c: "1037", t: 2.47, d: 43, zoom: 1.4, origen: "50% 42%" },
  { name: "Plano · pecho cerrado (nuez)", c: "1037", t: 3.9, d: 25, zoom: 1.45, origen: "50% 40%" },
  // ── 4 Elevaciones laterales en máquina
  { name: "Elevaciones · abierto", c: "1038", t: 4.27, d: 35 },
  { name: "Elevaciones · hombro cerrado", c: "1038", t: 5.43, d: 48, zoom: 1.4, origen: "40% 24%" },
  { name: "Elevaciones · abierto 2 (con arte)", c: "1038", t: 7.03, d: 44, zoom: 1.1 },
  { name: "Elevaciones · hombro y cara (aparentemente el arte…)", c: "1038", t: 8.5, d: 58, zoom: 1.35, origen: "40% 24%" },
  // ── 5 Tríceps en polea
  { name: "Tríceps · abierto", c: "1039", t: 2.53, d: 40, zoom: 1.22, origen: "45% 82%" },
  { name: "Tríceps · brazos cerrado", c: "1039", t: 3.87, d: 42, zoom: 1.45, origen: "40% 60%" },
  { name: "Tríceps · abierto 2 (abajo del todo)", c: "1039", t: 5.27, d: 24, zoom: 1.25, origen: "45% 82%" },
  // ── "Y una vez más, Lucas demuestra que no todo es hacer bíceps."
  { name: "Remate · espejo", c: "1048", t: 8.0, d: 40, zoom: 1.1 },
  { name: "Remate · espejo cerca (Lucas demuestra)", c: "1048", t: 5.0, d: 38, zoom: 1.25, origen: "50% 40%" },
  // ── Cierre: "Sígueme para más."
  { name: "Cierre · espejo lento", c: "1048", t: 12.0, d: DURACION_V2 - SIGUEME_V2, punch: 0.18, rate: 0.75 },
];
const TRANS_V2: [number, Tipo][] = [
  [136, "pan"],
  [286, "zoom"],
  [471, "giro"],
  [575, "pan"],
  [760, "zoom"],
  [866, "giro"],
];

type Version = {
  voz: string;
  palabras: Palabra[];
  planos: Plano[];
  trans: [number, Tipo][];
  bloques: [number, number][]; // [desde, duración] de las 5 etiquetas
  titulo: [number, number];
  pecho: [number, number]; // plano del pecho iluminado: [desde, hasta]
  sigueme: number;
  claves: RegExp;
  subSize?: number; // tamaño de los subtítulos
  nombre?: [number, number]; // nombre a mano tipo Ariana: [desde, duración]
};
const V1: Version = {
  voz: "entreno-empuje/voz.mp3",
  palabras: palabrasV1 as Palabra[],
  planos: PLANOS_V1,
  trans: TRANS_V1,
  bloques: [[96, 180], [276, 125], [401, 175], [576, 130], [706, 110]],
  titulo: [52, 44],
  pecho: [29, 71],
  sigueme: SIGUEME_V1,
  claves: /^(tetas|grandes|empuje|inclinado|arriba|dinero|cerrado|estrecho|sufrir|plano|nuez|quema|hombro|laterales|barca|tríceps|abajo|bíceps)$/i,
};
const V2: Version = {
  voz: "entreno-empuje/voz-v2.mp3",
  // Subtítulos: "este es" y la pegatina dice "Lucas" (se quita esa palabra; "es," cierra el bloque para que "y" no se junte)
  palabras: (palabrasV2 as Palabra[]).flatMap((p, i) => (i === 2 ? [] : i === 1 ? [{ ...p, w: "es," }] : [p])),
  planos: PLANOS_V2,
  trans: TRANS_V2,
  bloques: [[136, 150], [286, 185], [471, 104], [575, 185], [760, 106]],
  titulo: [99, 37],
  pecho: [44, 86],
  sigueme: SIGUEME_V2,
  subSize: 62, // "subtítulos un poco más pequeños"
  nombre: [14, 30], // entra justo cuando dice "Lucas" (frame 14,4) → se va con el corte al pecho (44)
  claves: /^(pecho|crecer|entreno|inclinado|arriba|arte|cerrado|estrecho|técnica|plano|nuez|hombro|laterales|fundamental|tríceps|abajo|bíceps)$/i,
};
const ETIQUETAS = ["press inclinado en máquina", "press cerrado", "press plano en máquina", "elevaciones laterales", "tríceps en polea"];

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

// Brillo en los pectorales: sigue el pecho (seguimiento por plantilla, pecho-track.json = [dx, dy, energía])
// y late con su movimiento. Va dentro del Shot, así acompaña al zoom.
const PECTORALES = [
  { x: 395, y: 1220 },
  { x: 685, y: 1220 },
];
const ROJO = "#FF1A1A"; // el brillo del pecho es rojo (pedido de Lucas), no el acento
const BrilloPecho: React.FC = () => {
  const frame = useCurrentFrame();
  const track = pechoTrack as number[][];
  const i = Math.min(frame, track.length - 1);
  const [dx, dy] = track[i];
  // energía suavizada (media de ±2 frames) → 0..1
  const win = track.slice(Math.max(0, i - 2), i + 3).map((r) => r[2]);
  const e = win.reduce((a, b) => a + b, 0) / win.length;
  const pulso = interpolate(e, [1.2, 2.6], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const entra = interpolate(frame, [0, 8], [0, 1], { extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const sale = interpolate(frame, [33, 42], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
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

const efectoTransicion = (frame: number, TRANS: [number, Tipo][]) => {
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

const EntrenoEmpujeBase: React.FC<{ v: Version }> = ({ v }) => {
  const { fps, durationInFrames } = useVideoConfig();
  const frame = useCurrentFrame();
  const { blur, scale, tx, rot } = efectoTransicion(frame, v.trans);
  const FLASH = v.sigueme;

  const flash = interpolate(frame, [FLASH - 1, FLASH, FLASH + 6], [0, 0.85, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const fadeOut = interpolate(frame, [durationInFrames - 8, durationInFrames], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ backgroundColor: "black" }}>
      <AbsoluteFill
        style={{
          opacity: fadeOut,
          filter: `contrast(1.12) saturate(0.82) brightness(0.96) blur(${blur}px)`,
          transform: `translateX(${tx}px) rotate(${rot}deg) scale(${1 + scale})`,
        }}
      >
        <Series>
          {v.planos.map((p) => (
            <Series.Sequence key={p.name} name={p.name} durationInFrames={p.d} premountFor={fps}>
              <Shot punch={p.punch} zoom={p.zoom} origen={p.origen}>
                <Video src={clip(p.c)} trimBefore={Math.round(p.t * fps)} playbackRate={p.rate ?? 1} muted />
                {p.brillo ? <BrilloPecho /> : null}
              </Shot>
            </Series.Sequence>
          ))}
        </Series>
      </AbsoluteFill>

      <AbsoluteFill
        style={{
          pointerEvents: "none",
          background: "radial-gradient(ellipse at center, rgba(0,0,0,0) 55%, rgba(0,0,0,0.55) 100%)",
        }}
      />
      <AbsoluteFill style={{ backgroundColor: "white", opacity: flash, pointerEvents: "none" }} />

      {/* Textos */}
      {v.nombre ? (
        <Sequence name="Nombre a mano (Lucas)" from={v.nombre[0]} durationInFrames={v.nombre[1]} layout="none">
          <NombrePegatina nombre="Lucas" cabeza={{ x: 550, y: 590 }} />
        </Sequence>
      ) : null}
      <Sequence name="Título" from={v.titulo[0]} durationInFrames={v.titulo[1]} layout="none">
        <Titulo titulo="entreno de empuje" sub="pecho · hombro · tríceps" top={300} />
      </Sequence>
      {v.bloques.map(([from, d], k) => (
        <Sequence key={k} name={`${k + 1} · ${ETIQUETAS[k]}`} from={from} durationInFrames={d} layout="none">
          <Clave n={k + 1} texto={ETIQUETAS[k]} />
        </Sequence>
      ))}
      <Sequence name="@ Instagram" from={v.sigueme} layout="none">
        <Handle />
      </Sequence>

      <Subtitulos
        palabras={v.palabras}
        offset={VOZ_DESDE / fps}
        top={frame >= v.pecho[0] && frame < v.pecho[1] ? 1390 : 1180} // en el plano del pecho iluminado, bajo los pectorales
        claves={v.claves}
        size={v.subSize}
      />

      {/* Audio */}
      <Sequence name="Voz" from={VOZ_DESDE} layout="none">
        <Audio src={staticFile(v.voz)} volume={1} />
      </Sequence>
      <Sequence name="sfx brillo pecho" from={v.pecho[0]} durationInFrames={55} layout="none">
        <Audio src={staticFile("sonidos/chime.mp3")} volume={0.16} />
      </Sequence>
      <Sequence name="sfx título" from={v.titulo[0] - 2} durationInFrames={55} layout="none">
        <Audio src={staticFile("sonidos/sparkle.mp3")} volume={0.22} />
      </Sequence>
      {v.nombre ? (
        <Sequence name="pop nombre" from={v.nombre[0]} durationInFrames={20} layout="none">
          <Audio src={staticFile("sonidos/pop.mp3")} volume={0.45} /> {/* "un poco más presente" */}
        </Sequence>
      ) : null}
      <Sequence name="pop @" from={v.sigueme} durationInFrames={20} layout="none">
        <Audio src={staticFile("sonidos/pop.mp3")} volume={0.2} />
      </Sequence>
      {v.trans.map(([c]) => (
        <Sequence key={c} name={`whoosh ${c}`} from={c - 7} durationInFrames={20} layout="none">
          <Audio src={staticFile("sonidos/whoosh.mp3")} volume={0.35} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};

export const EntrenoEmpuje: React.FC = () => <EntrenoEmpujeBase v={V1} />;
export const EntrenoEmpujeV2: React.FC = () => <EntrenoEmpujeBase v={V2} />;

export const EntrenoEmpujeComp = () => (
  <>
    <Composition id="EntrenoEmpuje" component={EntrenoEmpuje} durationInFrames={DURACION_V1} fps={30} width={1080} height={1920} />
    <Composition id="EntrenoEmpujeV2" component={EntrenoEmpujeV2} durationInFrames={DURACION_V2} fps={30} width={1080} height={1920} />
  </>
);
