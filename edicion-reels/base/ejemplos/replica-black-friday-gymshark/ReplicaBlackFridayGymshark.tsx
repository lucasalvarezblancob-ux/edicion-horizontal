// replica-black-friday-gymshark — calco del reel de marti.cops (https://www.instagram.com/p/DffdMKag6i1/,
// refs/transiciones edit/marticops_DffdMKag6i1.mp4) con clips de Lucas vestido de Gymshark.
// Pedido de Lucas (2026-11-09): mismas transiciones, logos y textos; solo cambia el código (ALVAREZ10) y la hora
// (España, México y Argentina en vez de Italia/EST). Los posados de abdomen, con la camiseta azul petróleo.
// Música: la del original (Calvin Harris – Outside). El render de Remotion sale sin audio y después se le mete el audio
// del reel de la ref tal cual (ffmpeg -map 0:v -map 1:a -c copy -t 22.6): casa porque los cortes son los mismos fotogramas.
//
// Planos: seleccion.json (clip de recursos/ + instante de entrada) → planos_base.sh N → public/<slug>/planos/NN.mp4
// (2160×3840 30 fps bt709; HDR del iPhone con avconvert + hdr-pantalla.cube; Sony Devant SDR solo escalado).
// Coordenadas = las de la ref (720×1280) × 1,5. Fotogramas = los de la ref a 30 fps.
import { Video } from "@remotion/media";
import { loadFont as loadRoboto } from "@remotion/google-fonts/Roboto";
import { loadFont as loadCond } from "@remotion/google-fonts/RobotoCondensed";
import { loadFont as loadMont } from "@remotion/google-fonts/Montserrat";
import { loadFont as loadPoppins } from "@remotion/google-fonts/Poppins";
import React from "react";
import {
  AbsoluteFill,
  Composition,
  Img,
  interpolate,
  random,
  Sequence,
  staticFile,
  useCurrentFrame,
} from "remotion";

const roboto = loadRoboto("normal", { weights: ["400", "700"], subsets: ["latin"] }).fontFamily;
const cond = loadCond("normal", { weights: ["700"], subsets: ["latin"] }).fontFamily;
const mont = loadMont("normal", { weights: ["300", "600"], subsets: ["latin"] }).fontFamily;
const poppins = loadPoppins("normal", { weights: ["500"], subsets: ["latin"] }).fontFamily;

const S = "replica-black-friday-gymshark";
const FPS = 30;
const DURACION = 678; // 22,6 s como la ref
const LOGO = staticFile(`${S}/gymshark-tiburon.svg`); // copia en recursos/fotos/gymshark/ (public/<slug>/ se borró el 2026-11-09: para retocar, copiar el logo ahí y rehacer los planos con planos_base.sh)
const CODIGO = "ALVAREZ10";

const c = (x: number) => Math.min(1, Math.max(0, x));
const lin = (f: number, xs: number[], ys: number[]) =>
  interpolate(f, xs, ys, { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

// ---------- Planos ----------
type Plano = {
  n: number;
  de: number;
  a: number;
  zoom?: number;
  origen?: string; // transform-origin
  oscuro?: Record<number, number>; // fotograma absoluto → opacidad de negro encima (fotogramas "apagados" de la ref)
  // 2026-11-09 — Lucas: "bajarle un poco la exposición porque los textos blancos no se acaban de leer bien".
  // Medido con revisar_contraste.py (ratio WCAG ≥ 3): solo los planos con texto encima que no llegaban.
  exposicion?: number;
};

const PLANOS: Plano[] = [
  { n: 1, de: 0, a: 7, oscuro: { 0: 1, 1: 0.87, 2: 0.74, 3: 0.6, 4: 0.46, 5: 0.2, 6: 0.06 } },
  { n: 2, de: 7, a: 12 },
  { n: 3, de: 12, a: 16, oscuro: { 12: 0.86 } },
  { n: 4, de: 17, a: 21, zoom: 2.2, origen: "50% 70%" },
  { n: 5, de: 22, a: 26 },
  { n: 6, de: 26, a: 31, oscuro: { 26: 0.8 } },
  { n: 7, de: 32, a: 36 },
  { n: 8, de: 36, a: 38, oscuro: { 36: 0.76 } },
  { n: 9, de: 38, a: 41 },
  { n: 10, de: 42, a: 46 },
  { n: 11, de: 74, a: 217, zoom: 1.12, origen: "50% 35%", exposicion: 0.76 },
  { n: 12, de: 218, a: 232 },
  { n: 13, de: 240, a: 297, zoom: 1.4, origen: "50% 30%" },
  { n: 14, de: 294, a: 340, exposicion: 0.77 },
  { n: 15, de: 340, a: 349 },
  { n: 16, de: 349, a: 393 },
  { n: 17, de: 393, a: 416 },
  { n: 18, de: 416, a: 457, zoom: 1.8, origen: "50% 62%" },
  { n: 19, de: 457, a: 503 },
  { n: 20, de: 503, a: 568, zoom: 1.3, origen: "50% 30%" },
];

const src = (n: number) => staticFile(`${S}/planos/${String(n).padStart(2, "0")}.mp4`);

// Recorte vertical de la franja que se abre (74–105): altura en px de la ref (de 1280), centrada.
const franja = (f: number) =>
  lin(f, [73, 74, 76, 78, 86, 90, 93, 96, 100, 103, 105], [0, 21, 207, 301, 315, 485, 688, 696, 753, 991, 1280]) / 1280;

// Estilo por fotograma (transiciones que tocan la imagen: whip, apagados, glitch, desenfoques).
const estilo = (p: Plano, f: number): React.CSSProperties => {
  const t: string[] = [];
  const fl: string[] = [];
  if (p.zoom) t.push(`scale(${p.zoom})`);
  if (p.exposicion) fl.push(`brightness(${p.exposicion})`);
  if (p.n === 12) {
    // barrido con desenfoque de movimiento 227–231
    const x = lin(f, [226, 227, 228, 229, 230, 231], [0, -60, -180, -320, -420, -460]);
    const b = lin(f, [226, 227, 229, 231], [0, 14, 30, 34]);
    if (x) t.push(`scale(${1 + Math.abs(x) / 540}) translateX(${x / (1 + Math.abs(x) / 540)}px)`); // amplía para que no asome el negro
    if (b) fl.push(`blur(${b}px)`);
    if (f >= 231) fl.push("brightness(0.85)");
  }
  if (p.n === 20) {
    // entrada con zoom de golpe 503–504 y salida en desenfoque radial a negro 548–568
    const z = lin(f, [503, 505], [1.25, 1]);
    t.push(`scale(${z})`);
    const b = lin(f, [503, 504, 505], [18, 8, 0]) + lin(f, [548, 568], [0, 22]);
    if (b) fl.push(`blur(${b}px)`);
    const out = lin(f, [548, 568], [1, 1.12]);
    t.push(`scale(${out})`);
  }
  if (p.n === 19 && f >= 499) {
    const z = lin(f, [499, 503], [1, 1.18]);
    t.push(`scale(${z})`);
    fl.push(`blur(${lin(f, [500, 503], [0, 16])}px)`);
  }
  return { transform: t.join(" ") || undefined, filter: fl.join(" ") || undefined, transformOrigin: p.origen ?? "50% 50%" };
};

const VideoPlano: React.FC<{ p: Plano; f: number }> = ({ p, f }) => (
  <AbsoluteFill style={{ overflow: "hidden" }}>
    <AbsoluteFill style={estilo(p, f)}>
      <Video src={src(p.n)} muted style={{ width: "100%", height: "100%", objectFit: "cover" }} />
    </AbsoluteFill>
  </AbsoluteFill>
);

const CapaPlano: React.FC<{ p: Plano }> = ({ p }) => {
  const f = useCurrentFrame() + p.de; // fotograma absoluto
  const negro = p.oscuro?.[f] ?? 0;
  let clip: string | undefined;
  if (p.n === 11 && f < 105) {
    const h = franja(f);
    const m = ((1 - h) / 2) * 100;
    clip = `inset(${m}% 0 ${m}% 0)`;
  }
  if (p.n === 13 && f < 245) {
    // cortinilla de arriba abajo con borde naranja (240–244)
    const y = lin(f, [239, 240, 241, 242, 243, 244, 245], [0, 25, 34, 50, 66, 78, 100]);
    clip = `inset(0 0 ${100 - y}% 0)`;
  }
  let opacidad = 1;
  if (p.n === 14) opacidad = lin(f, [293, 294, 295, 296, 297], [0, 0.35, 0.65, 0.9, 1]);
  if (p.n === 20) opacidad = lin(f, [502, 503], [0, 1]);
  const glitch = p.n === 18 || p.n === 19 ? glitchDe(f) : 0;
  return (
    <AbsoluteFill style={{ clipPath: clip, opacity: opacidad }}>
      <VideoPlano p={p} f={f} />
      {glitch > 0 && <Glitch p={p} f={f} fuerza={glitch} />}
      {negro > 0 && <AbsoluteFill style={{ backgroundColor: `rgba(0,0,0,${negro})` }} />}
      {p.n === 20 && <AbsoluteFill style={{ backgroundColor: `rgba(0,0,0,${lin(f, [548, 552, 555, 558, 560, 562, 564, 566, 567], [0, 0.1, 0.26, 0.5, 0.65, 0.8, 0.88, 0.975, 1])})` }} />}
    </AbsoluteFill>
  );
};

// ---------- Glitch (452–461) ----------
const glitchDe = (f: number) => (f >= 452 && f <= 461 ? (f >= 455 && f <= 458 ? 1 : 0.6) : 0);

const Glitch: React.FC<{ p: Plano; f: number; fuerza: number }> = ({ p, f, fuerza }) => {
  const bandas = Array.from({ length: 6 }, (_, i) => {
    const y = random(`gy${f}-${i}`) * 92;
    const h = 1 + random(`gh${f}-${i}`) * 7;
    const dx = (random(`gx${f}-${i}`) - 0.5) * 140 * fuerza;
    return { y, h, dx };
  });
  const lineas = Array.from({ length: 5 }, (_, i) => ({ y: random(`ly${f}-${i}`) * 100, h: 2 + random(`lh${f}-${i}`) * 5 }));
  return (
    <>
      {bandas.map((b, i) => (
        <AbsoluteFill key={i} style={{ clipPath: `inset(${b.y}% 0 ${100 - b.y - b.h}% 0)`, transform: `translateX(${b.dx}px)` }}>
          <VideoPlano p={p} f={f} />
        </AbsoluteFill>
      ))}
      {/* desdoblamiento de color */}
      <AbsoluteFill style={{ mixBlendMode: "screen", opacity: 0.45 * fuerza, transform: `translateX(${14 * fuerza}px)`, filter: "sepia(1) saturate(6) hue-rotate(-50deg)" }}>
        <VideoPlano p={p} f={f} />
      </AbsoluteFill>
      <AbsoluteFill style={{ mixBlendMode: "screen", opacity: 0.4 * fuerza, transform: `translateX(${-14 * fuerza}px)`, filter: "sepia(1) saturate(6) hue-rotate(160deg)" }}>
        <VideoPlano p={p} f={f} />
      </AbsoluteFill>
      {lineas.map((l, i) => (
        <div key={`l${i}`} style={{ position: "absolute", left: 0, right: 0, top: `${l.y}%`, height: l.h, background: "rgba(255,255,255,0.92)", boxShadow: "0 0 8px rgba(255,255,255,0.8)" }} />
      ))}
    </>
  );
};

// ---------- Grano y rayas de película ----------
const Grano: React.FC<{ f: number; opacidad: number }> = ({ f, opacidad }) => (
  <AbsoluteFill style={{ opacity: opacidad, mixBlendMode: "overlay" }}>
    <svg width="1080" height="1920">
      <filter id={`g${f}`}>
        <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves={2} seed={f} />
        <feColorMatrix type="saturate" values="0" />
      </filter>
      <rect width="1080" height="1920" filter={`url(#g${f})`} />
    </svg>
  </AbsoluteFill>
);

const Rayas: React.FC<{ f: number; n?: number; color?: string }> = ({ f, n = 3, color = "rgba(255,240,220,0.85)" }) => (
  <AbsoluteFill>
    <svg width="1080" height="1920">
      {Array.from({ length: n }, (_, i) => {
        const x = random(`rx${f}-${i}`) * 1080;
        const y = random(`ry${f}-${i}`) * 1700;
        const l = 120 + random(`rl${f}-${i}`) * 420;
        const cx = (random(`rc${f}-${i}`) - 0.5) * 260;
        return <path key={i} d={`M ${x} ${y} q ${cx} ${l / 2} ${cx / 3} ${l}`} stroke={color} strokeWidth={2 + random(`rw${f}-${i}`) * 2} fill="none" />;
      })}
    </svg>
  </AbsoluteFill>
);

// ---------- Quemados / luces (encima de todo, como en la ref) ----------
const Luz: React.FC<{ fondo: string; modo?: React.CSSProperties["mixBlendMode"]; opacidad: number }> = ({ fondo, modo = "screen", opacidad }) =>
  opacidad > 0 ? <AbsoluteFill style={{ background: fondo, mixBlendMode: modo, opacity: c(opacidad) }} /> : null;

const AMARILLO = "linear-gradient(180deg, #ffe066 0%, #ffd23f 45%, #ffb21e 100%)";

const Quemados: React.FC = () => {
  const f = useCurrentFrame();
  const capas: React.ReactNode[] = [];
  // destello 132–134
  capas.push(<Luz key="d1" fondo="radial-gradient(ellipse at 50% 40%, #fff3c4 0%, #ffcf6b 60%, #ff9a3c 100%)" opacidad={lin(f, [131, 132, 133, 134], [0, 0.55, 0.75, 0])} />);
  // gran quemado amarillo 138–148 (pinceladas)
  const q1 = lin(f, [137, 138, 139, 142, 143, 146, 147, 148], [0, 0.45, 0.95, 0.95, 0.75, 0.6, 0.3, 0]);
  if (q1 > 0) {
    capas.push(<Luz key="q1" fondo={AMARILLO} opacidad={q1} />);
    capas.push(
      <AbsoluteFill key="q1b" style={{ opacity: c(q1 * 1.1), mixBlendMode: "multiply" }}>
        <svg width="1080" height="1920">
          <path d={`M -40 ${1400 + (f - 138) * 6} C 300 1100, 500 1700, 1120 1350`} stroke="#e8432a" strokeWidth={14} fill="none" opacity={0.8} />
          <path d={`M 180 ${700 - (f - 138) * 8} c 140 -220 420 -40 300 160 s -320 260 -120 420`} stroke="#d63a1c" strokeWidth={9} fill="none" opacity={0.7} />
          <rect x={0} y={1640} width={1080} height={40} fill="#e8432a" opacity={0.55} />
        </svg>
      </AbsoluteFill>,
    );
  }
  // fuga roja abajo 162–164 y naranja a la derecha 169–174
  capas.push(<Luz key="l1" fondo="radial-gradient(ellipse 70% 30% at 25% 100%, #ff3b1f 0%, rgba(255,90,30,0.6) 45%, transparent 75%)" opacidad={lin(f, [161, 162, 164, 165], [0, 0.9, 0.7, 0])} />);
  capas.push(<Luz key="l2" fondo="radial-gradient(ellipse 45% 60% at 100% 55%, #ff7a1a 0%, rgba(255,60,20,0.7) 40%, transparent 75%)" opacidad={lin(f, [168, 169, 171, 173, 175], [0, 0.6, 0.95, 0.7, 0])} />);
  // quemado amarillo 188–193
  capas.push(<Luz key="q2" fondo={`linear-gradient(200deg, #fff2a8 0%, #ffd13b 50%, #ff8a1f 100%)`} opacidad={lin(f, [187, 188, 189, 191, 192, 193, 194], [0, 0.7, 0.95, 0.85, 0.15, 0.05, 0])} />);
  capas.push(<Luz key="l3" fondo="radial-gradient(ellipse 60% 25% at 50% 100%, #ff4a1a 0%, transparent 70%)" opacidad={lin(f, [199, 200, 202, 203], [0, 0.8, 0.5, 0])} />);
  // quemado amarillo con pincelada 215–216 (justo antes del negro)
  const q3 = f === 215 || f === 216 ? 0.97 : 0;
  if (q3) {
    capas.push(<Luz key="q3" fondo="linear-gradient(180deg, #ffe58a 0%, #ffd04a 100%)" opacidad={q3} />);
    capas.push(
      <AbsoluteFill key="q3b" style={{ mixBlendMode: "multiply", opacity: 0.55 }}>
        <svg width="1080" height="1920">
          <path d={`M ${80 + (f - 215) * 40} 1520 C 300 1150, 520 1500, 700 1080 S 980 800, 1100 760`} stroke="#d9862a" strokeWidth={90} fill="none" strokeLinecap="round" />
        </svg>
      </AbsoluteFill>,
    );
  }
  // tintes tras la cortinilla 245–254
  const rojo = lin(f, [244, 245, 246, 247], [0, 0.75, 0.7, 0]) + lin(f, [249, 250, 251, 252], [0, 0.75, 0.75, 0]) + lin(f, [252, 253, 254], [0, 0.35, 0]);
  capas.push(<Luz key="t1" fondo="#ff2814" modo="overlay" opacidad={rojo} />);
  capas.push(<Luz key="t1b" fondo="#ff3a1a" modo="screen" opacidad={rojo * 0.35} />);
  const azul = lin(f, [246, 247, 248, 249, 250], [0, 0.55, 0.5, 0.35, 0]);
  capas.push(<Luz key="t2" fondo="radial-gradient(ellipse at 60% 30%, #9fe3ff 0%, #2a8cff 60%, #123a8a 100%)" opacidad={azul} />);
  capas.push(<Luz key="t3" fondo="linear-gradient(180deg, #ffffff 0%, #fff1c2 40%, #ff9b2e 100%)" opacidad={lin(f, [251, 252, 253], [0, 0.9, 0])} />);
  // paso a la sudadera 289–297: rojo → naranja → blanco → funde
  capas.push(<Luz key="p1" fondo="#ff2a14" modo="overlay" opacidad={lin(f, [288, 289, 290, 291], [0, 0.5, 0.6, 0])} />);
  capas.push(<Luz key="p2" fondo="linear-gradient(180deg, #fff6d8 0%, #ffd25e 45%, #ff7a1e 100%)" opacidad={lin(f, [289, 290, 291, 292, 293, 294, 295, 296, 297, 298], [0, 0.3, 0.55, 0.8, 0.95, 0.65, 0.5, 0.5, 0.1, 0])} />);
  // antes del glitch 446–454 se calienta; 455–456 quemado blanco; 462–470 fuga cálida que se apaga
  capas.push(<Luz key="g1" fondo="linear-gradient(180deg, #ffd8a8 0%, #ff8c4a 100%)" opacidad={lin(f, [445, 450, 454, 455], [0, 0.12, 0.18, 0])} />);
  capas.push(<Luz key="g2" fondo="#ffffff" opacidad={lin(f, [454, 455, 456, 457], [0, 0.45, 0.4, 0])} />);
  capas.push(<Luz key="g3" fondo="radial-gradient(ellipse at 30% 50%, #ffb38a 0%, #ff6a3a 55%, rgba(255,80,40,0.2) 100%)" opacidad={lin(f, [461, 462, 464, 470], [0, 0.55, 0.45, 0])} />);
  // destello y paso al posado final 500–509
  capas.push(<Luz key="f1" fondo="radial-gradient(ellipse at 50% 40%, #ffffff 0%, #fff0d0 60%, #ffcf9a 100%)" opacidad={lin(f, [499, 501, 502, 503, 504, 505], [0, 0.3, 0.6, 0.12, 0.03, 0])} />);
  capas.push(<Luz key="f2" fondo="linear-gradient(180deg, #ffcf9e 0%, #ff8f5a 100%)" modo="soft-light" opacidad={lin(f, [504, 505, 509, 511], [0, 0.5, 0.25, 0])} />);
  return <>{capas}</>;
};

// ---------- Secuencia "película con logo" 230–244 ----------
const FONDOS_PELICULA: Record<number, { fondo: string; logo: boolean; raya?: boolean }> = {
  230: { fondo: "linear-gradient(180deg, rgba(120,20,10,0) 0%, rgba(255,60,20,0.85) 38%, #ffb21e 50%, rgba(255,60,20,0.85) 62%, rgba(120,20,10,0) 100%)", logo: true },
  231: { fondo: "transparent", logo: true },
  232: { fondo: "linear-gradient(180deg, #ff3d0a 0%, #ff7a1a 40%, #ffe27a 50%, #ff5a1a 58%, #5a3a6a 100%)", logo: false, raya: true },
  233: { fondo: "linear-gradient(180deg, #e2231a 0%, #ff6a1a 35%, #ffc61e 75%, #fff04a 100%)", logo: true },
  234: { fondo: "radial-gradient(ellipse at 40% 30%, #4a2a8a 0%, #2a1458 55%, #140a2a 100%)", logo: false, raya: true },
  235: { fondo: "linear-gradient(180deg, #3a1a08 0%, #9a4a10 38%, #ffb03a 46%, #7a3a10 54%, #1a0a04 100%)", logo: true },
  236: { fondo: "linear-gradient(180deg, #2a1206 0%, #8a4010 38%, #f7a336 46%, #6a3410 54%, #140804 100%)", logo: true },
  237: { fondo: "linear-gradient(180deg, #0a0a14 0%, #5a0a0a 30%, #c2201a 42%, #3a0606 55%, #c2201a 66%, #0a0a14 100%)", logo: false },
  238: { fondo: "radial-gradient(ellipse at 30% 20%, #9cc0dc 0%, #4a7aa6 45%, #102a52 100%)", logo: true, raya: true },
  239: { fondo: "#000", logo: true },
};

const Pelicula: React.FC = () => {
  const f = useCurrentFrame() + 230;
  const d = FONDOS_PELICULA[Math.min(f, 239)];
  const fondoOpaco = f >= 232 && f <= 239;
  return (
    <AbsoluteFill>
      {f <= 239 && <AbsoluteFill style={{ background: d.fondo, mixBlendMode: fondoOpaco ? "normal" : "screen" }} />}
      {f <= 238 && f >= 232 && <Grano f={f} opacidad={0.55} />}
      {d.raya && f <= 239 && <Rayas f={f} n={2} />}
      {(d.logo || f >= 240) && (
        // a partir de 240 el logo se queda en la parte negra, por debajo de la cortinilla
        <AbsoluteFill style={{ clipPath: f >= 240 ? `inset(${lin(f, [240, 241, 242, 243, 244], [25, 34, 50, 66, 78])}% 0 0 0)` : undefined }}>
          <Img
            src={LOGO}
            style={{ position: "absolute", width: 230, left: 540 - 115 + 12, top: 960 - 88, opacity: f === 230 ? 0.9 : 1, filter: "drop-shadow(0 0 2px rgba(255,255,255,0.4))" }}
          />
        </AbsoluteFill>
      )}
      {f >= 239 && f <= 244 && (
        // borde naranja de la cortinilla
        <div
          style={{
            position: "absolute",
            left: 0,
            right: 0,
            top: `${lin(f, [239, 240, 241, 242, 243, 244], [3, 25, 34, 50, 66, 78])}%`,
            height: 6,
            transform: "translateY(-3px)",
            background: "linear-gradient(90deg, rgba(255,120,30,0.2), #ffb347, #ff7a1a, rgba(255,120,30,0.4))",
            boxShadow: "0 0 18px 6px rgba(255,130,40,0.75)",
          }}
        />
      )}
    </AbsoluteFill>
  );
};

// ---------- Textos ----------
const BLANCO_ROTO = "rgba(236,231,228,0.93)";

const TituloBF: React.FC = () => (
  <AbsoluteFill>
    {[
      { t: "GYMSHARK", y: 858 },
      { t: "BLACK FRIDAY", y: 983 },
    ].map((l) => (
      <div
        key={l.t}
        style={{ position: "absolute", left: 0, right: 0, top: l.y, transform: "translateY(-50%)", textAlign: "center", fontFamily: roboto, fontWeight: 700, fontSize: 112, lineHeight: 1, letterSpacing: "-0.005em", color: BLANCO_ROTO }}
      >
        {l.t}
      </div>
    ))}
  </AbsoluteFill>
);

const StayTuned: React.FC = () => (
  <AbsoluteFill>
    <div style={{ position: "absolute", left: 0, right: 0, top: 215, transform: "translateY(-50%)", textAlign: "center", fontFamily: mont, fontWeight: 600, fontSize: 30, letterSpacing: "0.14em", color: "rgba(255,255,255,0.92)" }}>
      STAY TUNED
    </div>
    <div style={{ position: "absolute", left: 0, right: 0, top: 1062, transform: "translateY(-50%)", textAlign: "center", fontFamily: poppins, fontWeight: 500, fontSize: 47, color: "#fff" }}>
      15/11/2026
    </div>
  </AbsoluteFill>
);

// Cada letra aparece con fundido + desenfoque, del centro hacia fuera (como la ref, 268–281).
const Letras: React.FC<{ t: string; f: number; inicio: number; estilo: React.CSSProperties }> = ({ t, f, inicio, estilo }) => {
  const ls = [...t];
  const centro = (ls.length - 1) / 2;
  return (
    <div style={{ ...estilo, whiteSpace: "pre" }}>
      {ls.map((ch, i) => {
        const d = inicio + (Math.abs(i - centro) / Math.max(1, centro)) * 7 + random(`l${t}${i}`) * 2;
        const o = lin(f, [d, d + 4], [0, 1]);
        const b = lin(f, [d, d + 4], [10, 0]);
        return (
          <span key={i} style={{ opacity: o, filter: b ? `blur(${b}px)` : undefined }}>
            {ch}
          </span>
        );
      })}
    </div>
  );
};

const Descuento: React.FC = () => {
  const f = useCurrentFrame() + 268;
  const base: React.CSSProperties = { position: "absolute", left: 0, right: 0, transform: "translateY(-50%)", textAlign: "center", color: "#fff", lineHeight: 1, textShadow: "0 0 10px rgba(0,0,0,0.25)" };
  return (
    <AbsoluteFill>
      <Letras t="-50% off" f={f} inicio={268} estilo={{ ...base, top: 930, fontFamily: roboto, fontWeight: 700, fontSize: 76 }} />
      <Letras t={`+ ${CODIGO}`} f={f} inicio={269} estilo={{ ...base, top: 1008, fontFamily: roboto, fontWeight: 700, fontSize: 76 }} />
      <Letras t="for an extra -10%" f={f} inicio={268} estilo={{ ...base, top: 1070, fontFamily: roboto, fontWeight: 400, fontSize: 66, letterSpacing: "0.02em" }} />
    </AbsoluteFill>
  );
};

// ---------- Tarjeta final 572–678 ----------
// Hora: 15/11 17:00 en España (CET, UTC+1) = 10:00 en Ciudad de México (UTC−6, sin horario de verano desde 2022)
// = 13:00 en Argentina (UTC−3).
const HORAS = [
  { t: "17:00 ESP time", bandera: "🇪🇸" },
  { t: "10:00 MEX time", bandera: "🇲🇽" },
  { t: "13:00 ARG time", bandera: "🇦🇷" },
];
const SUBE = 31; // la ref tiene 2 horas; con 3 se sube el bloque media línea para que siga centrado

const Humo: React.FC<{ f: number }> = ({ f }) => {
  const t = f - 575;
  const op = lin(f, [575, 580, 592, 603, 616], [0, 0.9, 0.8, 0.35, 0]);
  if (op <= 0) return null;
  const nubes = Array.from({ length: 9 }, (_, i) => {
    const x = -200 + i * 150 + t * (9 + random(`hx${i}`) * 6);
    const y = 1420 - SUBE + (random(`hy${i}`) - 0.5) * 160 - t * (1.5 + random(`hv${i}`) * 2.5);
    const rx = 150 + random(`hr${i}`) * 120 + t * 4;
    const ry = 70 + random(`hs${i}`) * 50 + t * 1.6;
    return { x, y, rx, ry };
  });
  return (
    <AbsoluteFill style={{ opacity: op }}>
      <svg width="1080" height="1920">
        <filter id="humo" x="-30%" y="-30%" width="160%" height="160%">
          <feTurbulence type="fractalNoise" baseFrequency="0.006 0.018" numOctaves={4} seed={7} />
          <feDisplacementMap in="SourceGraphic" scale={170} xChannelSelector="R" yChannelSelector="G" />
          <feGaussianBlur stdDeviation={6} />
        </filter>
        <g filter="url(#humo)">
          {nubes.map((n, i) => (
            <ellipse key={i} cx={n.x} cy={n.y} rx={n.rx} ry={n.ry} fill="rgba(222,208,190,0.55)" />
          ))}
        </g>
      </svg>
    </AbsoluteFill>
  );
};

const Tarjeta: React.FC = () => {
  const f = useCurrentFrame() + 572;
  const centrado: React.CSSProperties = { position: "absolute", left: 0, right: 0, transform: "translateY(-50%)", textAlign: "center", color: "#fff", lineHeight: 1 };
  // el código se descubre de izquierda a derecha detrás del humo (577–600)
  const barrido = lin(f, [577, 600], [-10, 110]);
  const desenfoque = lin(f, [577, 598, 606], [10, 3, 0]);
  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      <div style={{ ...centrado, top: 735 - SUBE, fontFamily: cond, fontWeight: 700, fontSize: 80 }}>15 November</div>
      <Img src={LOGO} style={{ position: "absolute", width: 240, left: 548 - 120, top: 838 - SUBE }} />
      <div style={{ ...centrado, top: 1065 - SUBE, fontFamily: cond, fontWeight: 700, fontSize: 68 }}>GYMSHARK</div>
      {HORAS.map((h, i) => (
        <div key={h.t} style={{ ...centrado, top: 1180 - SUBE + i * 62, fontFamily: mont, fontWeight: 300, fontSize: 52 }}>
          {h.t}
          <span style={{ fontSize: 46, marginLeft: 6 }}>{h.bandera}</span>
        </div>
      ))}
      <div
        style={{
          ...centrado,
          top: 1380 + 62 - SUBE,
          fontFamily: cond,
          fontWeight: 700,
          fontSize: 92,
          filter: desenfoque ? `blur(${desenfoque}px)` : undefined,
          WebkitMaskImage: `linear-gradient(90deg, #000 ${barrido - 12}%, transparent ${barrido + 12}%)`,
          maskImage: `linear-gradient(90deg, #000 ${barrido - 12}%, transparent ${barrido + 12}%)`,
        }}
      >
        cod: {CODIGO}
      </div>
      <Humo f={f} />
    </AbsoluteFill>
  );
};

// ---------- Composición ----------
export const ReplicaBlackFridayGymshark: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: "black" }}>
    {PLANOS.map((p) => (
      <Sequence key={p.n} name={`plano ${p.n}`} from={p.de} durationInFrames={p.a - p.de} premountFor={30}>
        <CapaPlano p={p} />
      </Sequence>
    ))}
    <Sequence name="película + logo" from={230} durationInFrames={15}>
      <Pelicula />
    </Sequence>
    <Sequence name="GYMSHARK BLACK FRIDAY" from={49} durationInFrames={169} layout="none">
      <TituloBF />
    </Sequence>
    <Sequence name="STAY TUNED + fecha" from={118} durationInFrames={97} layout="none">
      <StayTuned />
    </Sequence>
    <Sequence name="-50% + código" from={268} durationInFrames={147} layout="none">
      <Descuento />
    </Sequence>
    <Quemados />
    <Sequence name="tarjeta final" from={572} durationInFrames={DURACION - 572}>
      <Tarjeta />
    </Sequence>
  </AbsoluteFill>
);

export const ReplicaBlackFridayGymsharkComp: React.FC = () => (
  <Composition id="ReplicaBlackFridayGymshark" component={ReplicaBlackFridayGymshark} durationInFrames={DURACION} fps={FPS} width={1080} height={1920} />
);
