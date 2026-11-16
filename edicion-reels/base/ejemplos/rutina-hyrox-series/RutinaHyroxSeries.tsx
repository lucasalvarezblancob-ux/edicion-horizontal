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
import { ACENTO, Palabra, Subtitulos, Titulo, TITLE_FONT } from "../../comun/Subtitulos";
import palabras from "./voz-palabras.json";

// 3.ª versión (series y repeticiones) de rutina-hibrida: mismos clips (proxies en public/rutina-hibrida/c<IMG>.mp4,
// brutos en recursos/gym/{fisico,cardio,piernas,funcional}/2026-11-01_hibrido_…). 3 rondas: 1 km + SkiErg 500 m + granjero 100 m +
// 20 zancadas por pierna + 25 wall balls, 2 min de descanso. Cifras propuestas por Claude (Lucas no dio las suyas).
const clip = (id: string) => staticFile(`rutina-hibrida/c${id}.mp4`);
const VOZ = staticFile("rutina-hyrox-series/voz.mp3"); // Alberto Rodríguez ×1,25 sin silencios
const VOZ_DESDE = 3;
const DURACION = 845;

type Plano = {
  name: string;
  c: string;
  t: number;
  d: number;
  zoom?: number;
  origen?: string;
  punch?: number;
  rate?: number;
};

const PLANOS: Plano[] = [
  // ── Gancho: "¿Qué pasa, perra? Esta es la rutina exacta para preparar un Hyrox, con series y repeticiones."
  { name: "Intro · sentado", c: "6116", t: 4.05, d: 26, punch: 0.15 },
  { name: "Intro · sentado (jump cut)", c: "6116", t: 8.8, d: 45, zoom: 1.25, origen: "50% 50%", punch: 0.1 },
  { name: "Gancho · lanza", c: "6123", t: 4.1, d: 16 },
  { name: "Gancho · ski", c: "6370", t: 5.0, d: 13, zoom: 1.2 },
  { name: "Gancho · granjero", c: "6120", t: 22.6, d: 22, zoom: 1.1 },
  // "Son tres rondas."
  { name: "3 rondas · zancadas", c: "6369", t: 42.0, d: 26, zoom: 1.3, origen: "50% 58%" },
  // ── 1 km corriendo
  { name: "Correr · abierto", c: "6128", t: 20.0, d: 28 },
  { name: "Correr · piernas", c: "6128", t: 21.0, d: 27, zoom: 1.6, origen: "50% 82%" },
  { name: "Correr · abierto 2", c: "6128", t: 12.0, d: 28, zoom: 1.1, origen: "50% 60%" },
  // ── SkiErg 500 m (tiempo continuo, cambia el encuadre en los extremos)
  { name: "Ski · abierto", c: "6370", t: 4.8, d: 29 },
  { name: "Ski · brazos", c: "6370", t: 5.77, d: 17, zoom: 1.45, origen: "58% 30%" },
  { name: "Ski · cadera", c: "6370", t: 6.33, d: 29, zoom: 1.5, origen: "58% 55%" },
  // ── Granjero 100 m
  { name: "Granjero · de frente", c: "6120", t: 22.57, d: 32, zoom: 1.1 },
  { name: "Granjero · mancuernas (espalda)", c: "6120", t: 1.37, d: 24 },
  { name: "Granjero · de frente cerrado", c: "6120", t: 24.3, d: 25, zoom: 1.35, origen: "50% 58%" },
  { name: "Granjero · se aleja (pasos cortos)", c: "6120", t: 9.0, d: 26, zoom: 1.15, origen: "50% 60%" },
  // ── 20 zancadas por pierna
  { name: "Zancadas · de espaldas", c: "6369", t: 4.83, d: 24, zoom: 1.05 },
  { name: "Zancadas · de frente cerrado", c: "6369", t: 39.77, d: 45, zoom: 1.5, origen: "60% 62%" },
  { name: "Zancadas · rodilla al suelo", c: "6369", t: 41.27, d: 31, zoom: 1.3, origen: "50% 58%" },
  // ── 25 wall balls (lateral = sentadilla, contrapicado = lanzamiento)
  { name: "WB contrapicado · lanza", c: "6123", t: 3.95, d: 35 },
  { name: "WB lateral · arriba", c: "6125", t: 13.4, d: 19 },
  { name: "WB lateral · bajando en sentadilla", c: "6125", t: 15.83, d: 34 },
  { name: "WB contrapicado · lanzando con las piernas", c: "6123", t: 7.6, d: 27 },
  { name: "WB · cara (uf, cómo quema)", c: "6123", t: 36.3, d: 27 },
  // ── "Descansas dos minutos y repites." — bebe agua en el cajón
  { name: "Descanso · bebe agua", c: "6116", t: 13.2, d: 43, zoom: 1.2, origen: "50% 50%" },
  // ── Repaso ×3: "Tres rondas así y el día de la carrera vas sobrado."
  { name: "Repaso · corre", c: "6128", t: 30.0, d: 13 },
  { name: "Repaso · ski", c: "6370", t: 10.0, d: 13, zoom: 1.2 },
  { name: "Repaso · granjero", c: "6120", t: 25.0, d: 13, zoom: 1.2 },
  { name: "Repaso · zancadas", c: "6369", t: 43.0, d: 13, zoom: 1.2 },
  { name: "Repaso · wall ball", c: "6125", t: 18.95, d: 14 },
  // ── Cierre: "Guárdatela. Sígueme para más, perra."
  { name: "Se levanta del cajón", c: "6116", t: 16.9, d: 20 },
  { name: "Cierre · a cámara", c: "6116", t: 18.6, d: DURACION - 784, punch: 0.18, rate: 0.75 },
];

// Transiciones en cada cambio de ejercicio (todas con whoosh: cambia el sitio)
type Tipo = "pan" | "zoom" | "giro";
const TRANS: [number, Tipo, boolean][] = [
  [148, "pan", true],
  [231, "zoom", true],
  [306, "giro", true],
  [413, "pan", true],
  [513, "zoom", true],
  [698, "pan", true],
  [784, "zoom", true],
];
const FLASH = 784;

// Tarjeta de cifra: número grande en el acento + qué es
const CIFRAS: [number, number, string, string, number?][] = [
  [122, 26, "3", "rondas"],
  [148, 83, "1 km", "corriendo", 600], // más abajo: en la cinta la cara queda arriba
  [231, 75, "500 m", "ski erg"],
  [306, 107, "100 m", "paseo del granjero"],
  [413, 100, "20", "zancadas por pierna"],
  [513, 142, "25", "wall balls"],
  [655, 43, "2 min", "descanso", 540], // debajo del logo de Nike
  [698, 66, "×3", "rondas"],
];

const Cifra: React.FC<{ valor: string; texto: string; top?: number }> = ({ valor, texto, top = 250 }) => {
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
            fontSize: 150,
            lineHeight: 1,
            color: ACENTO,
            letterSpacing: -3,
            textShadow: "0 6px 30px rgba(0,0,0,0.7)",
          }}
        >
          {valor}
        </div>
        <div
          style={{
            fontWeight: 700,
            fontSize: 56,
            color: "white",
            marginTop: 4,
            textShadow: "0 3px 16px rgba(0,0,0,0.85)",
          }}
        >
          {texto}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// Cada plano entra con punch-in y sigue empujando despacio: nunca está quieto.
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

// Efecto global alrededor de cada corte marcado
const efectoTransicion = (frame: number) => {
  let blur = 0;
  let scale = 0;
  let tx = 0;
  let rot = 0;
  for (const [c, tipo] of TRANS) {
    const d = frame - c + 0.5; // <0 antes del corte, >0 después
    const ad = Math.abs(d);
    const R = 5;
    if (ad >= R) continue;
    const k = 1 - ad / R; // 0→1→0
    const k2 = k * k;
    if (tipo === "zoom") {
      blur = Math.max(blur, 16 * k);
      scale = Math.max(scale, 0.16 * k);
    } else if (tipo === "pan") {
      // barrido lateral: lo de antes sale a la izquierda, lo nuevo entra desde la derecha
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

export const RutinaHyroxSeries: React.FC = () => {
  const { fps, durationInFrames } = useVideoConfig();
  const frame = useCurrentFrame();
  const { blur, scale, tx, rot } = efectoTransicion(frame);

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
          {PLANOS.map((p) => (
            <Series.Sequence key={p.name} name={p.name} durationInFrames={p.d} premountFor={fps}>
              <Shot punch={p.punch} zoom={p.zoom} origen={p.origen}>
                <Video
                  src={clip(p.c)}
                  trimBefore={Math.round(p.t * fps)}
                  playbackRate={p.rate ?? 1}
                  muted
                />
              </Shot>
            </Series.Sequence>
          ))}
        </Series>
      </AbsoluteFill>

      {/* Viñeta */}
      <AbsoluteFill
        style={{
          pointerEvents: "none",
          background: "radial-gradient(ellipse at center, rgba(0,0,0,0) 55%, rgba(0,0,0,0.55) 100%)",
        }}
      />
      <AbsoluteFill style={{ backgroundColor: "white", opacity: flash, pointerEvents: "none" }} />

      {/* Textos */}
      <Sequence name="Título" from={30} durationInFrames={92} layout="none">
        <Titulo titulo="rutina hyrox" sub="series y repeticiones" top={500} />
      </Sequence>
      {CIFRAS.map(([from, d, valor, texto, top]) => (
        <Sequence key={from} name={`${valor} · ${texto}`} from={from} durationInFrames={d} layout="none">
          <Cifra valor={valor} texto={texto} top={top} />
        </Sequence>
      ))}

      <Subtitulos
        palabras={palabras as Palabra[]}
        offset={VOZ_DESDE / fps}
        claves={/^(hyrox|exacta|3|1|km|500|100|20|25|2|cadera|granjero|rodilla|quema|sobrado)$/i}
      />

      {/* Audio: voz + whoosh solo en los cambios de ejercicio */}
      <Sequence name="Voz" from={VOZ_DESDE} layout="none">
        <Audio src={VOZ} volume={1} />
      </Sequence>
      {/* Título: brillo suave al aparecer */}
      <Sequence name="sfx título" from={28} durationInFrames={55} layout="none">
        <Audio src={staticFile("sonidos/sparkle.mp3")} volume={0.22} />
      </Sequence>
      {CIFRAS.map(([from]) => (
        <Sequence key={`pop${from}`} name={`pop ${from}`} from={from} durationInFrames={20} layout="none">
          <Audio src={staticFile("sonidos/pop.mp3")} volume={0.2} />
        </Sequence>
      ))}
      {TRANS.filter(([, , sfx]) => sfx).map(([c]) => (
        <Sequence key={c} name={`whoosh ${c}`} from={c - 7} durationInFrames={20} layout="none">
          <Audio src={staticFile("sonidos/whoosh.mp3")} volume={0.35} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};

export const RutinaHyroxSeriesComp = () => (
  <Composition
    id="RutinaHyroxSeries"
    component={RutinaHyroxSeries}
    durationInFrames={DURACION}
    fps={30}
    width={1080}
    height={1920}
  />
);
