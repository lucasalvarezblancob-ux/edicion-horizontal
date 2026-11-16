// "Si no entrenas…" — Lucas hablando a cámara. 3 versiones para elegir estilo.
// Bruto: bruto terminado/2026-10-31_sentado-sudadera-negra_fondo-blanco.MOV (antes bruto/IMG_1021.MOV) → public/si-no-entrenas/proxy.mp4 (1080×1920, 30 fps)
// Pausas quitadas con herramientas/cortar_pausas.py (cortes.json). Tiempos por palabra: Scribe.
import { Audio, Video } from "@remotion/media";
import React from "react";
import {
  AbsoluteFill,
  Composition,
  Easing,
  interpolate,
  Series,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import {
  ACENTO,
  Bloque,
  CamaraVirtual,
  CREMA,
  Encuadre,
  F_FUERTE,
  F_SUB,
  PersonaEncima,
  Sfx,
  TextoBloques,
} from "../../comun/hablando";
import cara from "./cara.json";
import cortes from "./cortes.json";

const SRC = staticFile("si-no-entrenas/proxy.mp4");
const VOZ = staticFile("si-no-entrenas/voz.mp3");
const MUSICA = staticFile("si-no-entrenas/musica.mp3");
const CARAS = cara.caras as number[][];

// Tramos que se conservan (frames del bruto a 30 fps) — de cortes.json
const T1 = { desde: 20, dur: 528 }; // 0,67 s → 18,27 s
const T2 = { desde: 610, dur: 55 }; // 20,33 s → 22,17 s
const DUR = T1.dur + T2.dur; // 583
const bruto = (f: number) => (f < T1.dur ? f + T1.desde : f - T1.dur + T2.desde);

// Vídeo + voz con las pausas quitadas (jump cut en f528)
const Base: React.FC<{ fin?: number }> = ({ fin = 0 }) => {
  const { fps } = useVideoConfig();
  return (
    <Series>
      <Series.Sequence name="Tramo 1 (gancho → quién seas)" durationInFrames={T1.dur} premountFor={fps}>
        <Video src={SRC} trimBefore={T1.desde} muted premountFor={fps} />
        <Audio src={VOZ} trimBefore={T1.desde} />
      </Series.Sequence>
      <Series.Sequence name="Tramo 2 (sígueme)" durationInFrames={T2.dur + fin} premountFor={fps}>
        <Video src={SRC} trimBefore={T2.desde} muted premountFor={fps} />
        <Audio src={VOZ} trimBefore={T2.desde} />
      </Series.Sequence>
    </Series>
  );
};

const Grade: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <AbsoluteFill style={{ filter: "contrast(1.08) saturate(0.92) brightness(0.98)" }}>{children}</AbsoluteFill>
);

// Doble flash de sección (ref Triple Hook): 4 f blanco, 1 f imagen, 3 f blanco + whoosh y golpe grave
const DobleFlash: React.FC<{ en: number[] }> = ({ en }) => {
  const frame = useCurrentFrame();
  const blanco = en.some((c) => { const d = frame - c; return (d >= 0 && d < 4) || (d >= 5 && d < 8); });
  return blanco ? <AbsoluteFill style={{ backgroundColor: "white" }} /> : null;
};

const Musica: React.FC<{ vol?: number }> = ({ vol = 0.1 }) => <Audio src={MUSICA} volume={vol} />;

// =====================================================================================
// V1 · TIPOGRÁFICA — bloques palabra a palabra (relleno / FUERTE / remate) DETRÁS de Lucas,
// zoom de entrada + empuje lento, golpe de zoom en "Mercadona".
// =====================================================================================
const P = (texto: string, desde: number, estilo: Bloque["palabras"][number]["estilo"] = "relleno", salto = false) => ({ texto, desde, estilo, salto });

const BLOQUES_V1: Bloque[] = [
  { desde: 3, hasta: 70, y: 0.235, palabras: [P("si eres un", 3), P("puto maricón", 20), P("QUE NO", 45, "fuerte", true), P("ENTRENA", 52, "fuerte", true)] },
  { desde: 70, hasta: 129, y: 0.235, palabras: [P("me puedes venir a", 71), P("chupar", 97, "fuerte", true), P("la polla", 108, "remate")] },
  { desde: 129, hasta: 164, y: 0.235, palabras: [P("¿a que", 130), P("sí,", 140, "remate"), P("oye?", 146, "fuerte", true)] },
  { desde: 164, hasta: 192, y: 0.235, palabras: [P("SÍ", 165, "fuerte"), P("SÍ", 175, "fuerte"), P("SÍ", 180, "fuerte", true), P("SÍ", 185, "fuerte"), P("SÍ", 189, "fuerte")] },
  { desde: 192, hasta: 210, y: 0.235, palabras: [P("bla,", 193, "remate"), P("bla,", 198, "remate"), P("bla.", 203, "remate")] },
  { desde: 210, hasta: 278, y: 0.235, palabras: [P("esto es lo que pasa", 211), P("cuando te", 239, "relleno", true), P("MASTURBAS", 256, "fuerte", true)] },
  { desde: 278, hasta: 342, y: 0.235, palabras: [P("en público en el", 279), P("MERCADONA", 305, "fuerte", true)] },
  { desde: 342, hasta: 461, y: 0.235, palabras: [P("yo,", 343), P("personalmente,", 353, "remate"), P("prefiero el", 381, "relleno", true), P("pasillo de", 407), P("CONGELADOS", 426, "fuerte", true)] },
  { desde: 461, hasta: 528, y: 0.235, palabras: [P("pero depende mucho", 462), P("de", 494, "relleno", true), P("quién seas", 502, "remate")] },
  { desde: 528, hasta: 600, y: 0.235, palabras: [P("sígueme para más,", 529), P("MARICÓN", 562, "fuerte", true)] },
];

const ENC_V1: Encuadre[] = [
  { desde: 0, escala: 1.0 },
  { desde: 2, escala: 1.2, suave: 27, empuje: 0.012 }, // zoom de entrada 1,00→1,20 en 27 f (ref Triple Hook)
  { desde: 129, escala: 1.32, suave: 0, empuje: 0.02 },
  { desde: 210, escala: 1.2, suave: 0, empuje: 0.025 },
  { desde: 300, escala: 1.55, suave: 9 }, // golpe en MERCADONA
  { desde: 342, escala: 1.22, suave: 0, empuje: 0.02 },
  { desde: 426, escala: 1.38, suave: 8 }, // CONGELADOS
  { desde: 461, escala: 1.25, suave: 0, empuje: 0.025 },
  { desde: 528, escala: 1.4, suave: 0, empuje: 0.02 }, // jump cut tapado con cambio de encuadre
];

export const SiNoEntrenasV1: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: "black" }}>
    <Grade>
      <CamaraVirtual encuadres={ENC_V1} cara={CARAS} frameBruto={bruto} shake={[{ desde: 305, hasta: 318, px: 10 }]}>
        <Base fin={17} />
        {/* fondo oscurecido (la persona va encima sin oscurecer) para que el texto destaque */}
        <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(0,0,0,0.62) 0%, rgba(0,0,0,0.45) 18%, rgba(0,0,0,0) 34%)" }} />
        <TextoBloques bloques={BLOQUES_V1} pop escala={0.9} />
        <PersonaEncima carpeta="si-no-entrenas/persona" frameBruto={bruto} />
      </CamaraVirtual>
    </Grade>
    <DobleFlash en={[126, 524]} />
    <Sfx en={1} src="whoosh.mp3" volumen={0.5} />
    <Sfx en={0} src="impact-bass-2.mp3" volumen={0.3} />
    <Sfx en={124} src="whoosh.mp3" volumen={0.45} />
    <Sfx en={126} src="impact-bass-1.mp3" volumen={0.35} />
    <Sfx en={303} src="impact-bass-1.mp3" volumen={0.55} />
    <Sfx en={522} src="whoosh.mp3" volumen={0.45} />
    <Sfx en={524} src="impact-bass-1.mp3" volumen={0.35} />
    <Musica />
  </AbsoluteFill>
);

// =====================================================================================
// V2 · ACERCAR Y ALEJAR + BUCLE — cortes secos entre 3 encuadres en cada frase,
// subtítulos gruesos en mayúsculas, SFX CapCut, el final empalma con el principio.
// =====================================================================================
const ABIERTO = 1.0, MEDIO = 1.35, CARA = 1.95;
const ENC_V2: Encuadre[] = [
  { desde: 0, escala: ABIERTO, empuje: 0.01 },
  { desde: 30, escala: CARA }, // "maricón"
  { desde: 45, escala: MEDIO }, // "que no entrena"
  { desde: 71, escala: ABIERTO }, // "me puedes venir…"
  { desde: 97, escala: CARA }, // "chupar la polla"
  { desde: 130, escala: MEDIO }, // "¿a que sí, oye?"
  { desde: 165, escala: CARA }, // sí sí sí
  { desde: 175, escala: MEDIO },
  { desde: 180, escala: CARA },
  { desde: 185, escala: MEDIO },
  { desde: 193, escala: ABIERTO }, // bla bla bla
  { desde: 211, escala: MEDIO, empuje: 0.02 }, // esto es lo que pasa…
  { desde: 256, escala: CARA }, // masturbas
  { desde: 279, escala: ABIERTO }, // en público en el
  { desde: 305, escala: CARA }, // MERCADONA
  { desde: 343, escala: MEDIO, empuje: 0.02 }, // yo personalmente
  { desde: 407, escala: ABIERTO }, // pasillo de
  { desde: 426, escala: CARA }, // congelados
  { desde: 462, escala: MEDIO, empuje: 0.02 }, // pero depende
  { desde: 502, escala: CARA }, // quién seas
  { desde: 528, escala: MEDIO }, // sígueme
  { desde: 562, escala: ABIERTO }, // maricón → bucle con el plano abierto del inicio
];

// Subtítulos: grupos cortos, palabra clave en acento
type Sub = { desde: number; texto: string; clave?: boolean };
const SUBS_V2: Sub[] = [
  { desde: 3, texto: "si eres un" }, { desde: 20, texto: "puto" }, { desde: 30, texto: "maricón", clave: true },
  { desde: 45, texto: "que no" }, { desde: 52, texto: "entrena", clave: true }, { desde: 71, texto: "me puedes" },
  { desde: 85, texto: "venir a" }, { desde: 97, texto: "chupar", clave: true }, { desde: 108, texto: "la polla" },
  { desde: 130, texto: "¿a que sí," }, { desde: 146, texto: "oye?" }, { desde: 165, texto: "sí" }, { desde: 175, texto: "sí, sí" },
  { desde: 185, texto: "sí, sí, sí" }, { desde: 193, texto: "bla" }, { desde: 198, texto: "bla, bla" }, { desde: 203, texto: "bla, bla, bla" },
  { desde: 211, texto: "esto es" }, { desde: 220, texto: "lo que pasa" }, { desde: 239, texto: "cuando te" },
  { desde: 256, texto: "masturbas", clave: true }, { desde: 279, texto: "en público" }, { desde: 297, texto: "en el" },
  { desde: 305, texto: "mercadona", clave: true }, { desde: 343, texto: "yo," }, { desde: 353, texto: "personalmente" },
  { desde: 381, texto: "prefiero el" }, { desde: 407, texto: "pasillo de" }, { desde: 426, texto: "congelados", clave: true },
  { desde: 462, texto: "pero depende" }, { desde: 482, texto: "mucho de" }, { desde: 502, texto: "quién seas", clave: true },
  { desde: 529, texto: "sígueme" }, { desde: 544, texto: "para más," }, { desde: 562, texto: "maricón", clave: true },
];

const SubtitulosGruesos: React.FC<{ subs: Sub[]; y?: number }> = ({ subs, y = 0.64 }) => {
  const frame = useCurrentFrame();
  let s: Sub | undefined;
  for (const x of subs) if (frame >= x.desde) s = x;
  if (!s) return null;
  const k = interpolate(frame - s.desde, [0, 4], [0.7, 1], { extrapolateRight: "clamp", easing: Easing.out(Easing.back(2.2)) });
  return (
    <AbsoluteFill>
      <div
        style={{
          position: "absolute", top: `${y * 100}%`, width: "100%", textAlign: "center", transform: `translateY(-50%) scale(${k})`,
          fontFamily: F_SUB, fontWeight: 900, fontSize: s.clave ? 112 : 92, textTransform: "uppercase", letterSpacing: -1,
          color: s.clave ? ACENTO : "white", WebkitTextStroke: "3px black", paintOrder: "stroke fill",
          textShadow: "0 6px 0 rgba(0,0,0,0.85), 0 10px 24px rgba(0,0,0,0.5)",
        }}
      >
        {s.texto}
      </div>
    </AbsoluteFill>
  );
};

export const SiNoEntrenasV2: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: "black" }}>
    <Grade>
      <CamaraVirtual encuadres={ENC_V2} cara={CARAS} frameBruto={bruto}>
        <Base />
      </CamaraVirtual>
    </Grade>
    <SubtitulosGruesos subs={SUBS_V2} />
    {/* SFX estilo CapCut: whoosh en zooms grandes, pop en palabras clave, ding al enumerar */}
    <Sfx en={29} src="whoosh-short.mp3" volumen={0.35} />
    <Sfx en={96} src="whoosh-short.mp3" volumen={0.35} />
    <Sfx en={165} src="ping.mp3" volumen={0.18} />
    <Sfx en={175} src="ping.mp3" volumen={0.18} />
    <Sfx en={180} src="ping.mp3" volumen={0.18} />
    <Sfx en={185} src="ping.mp3" volumen={0.18} />
    <Sfx en={255} src="pop.mp3" volumen={0.35} />
    <Sfx en={304} src="whoosh.mp3" volumen={0.45} />
    <Sfx en={425} src="pop.mp3" volumen={0.35} />
    <Sfx en={501} src="whoosh-short.mp3" volumen={0.35} />
    <Musica vol={0.08} />
  </AbsoluteFill>
);

// =====================================================================================
// V3 · ZOOMS A LOS REMATES (modelo Aayush B, para plano fijo) — subtítulo de una palabra al
// centro, empuje lento continuo, zooms largos que aterrizan en cada remate, bloques solo en
// gancho y remate, la música se corta justo antes del chiste.
// (El texto que sigue la cabeza NO se usa: Lucas está sentado casi quieto.)
// =====================================================================================
const CLAVES_V3 = /^(entrena|chupar|masturbas|mercadona|congelados|seas|maricón)$/i;
const limpia = (w: string) => w.replace(/[¿?¡!.,]/g, "");

const PalabraSuelta: React.FC<{ ocultar: [number, number][] }> = ({ ocultar }) => {
  const frame = useCurrentFrame();
  if (ocultar.some(([a, b]) => frame >= a && frame < b)) return null;
  let w: { w: string; start: number; end: number } | undefined;
  for (const p of cortes.palabras) if (frame >= Math.round(p.start * 30) - 1) w = p;
  if (!w || frame > Math.round(w.end * 30) + 12) return null;
  const clave = CLAVES_V3.test(limpia(w.w));
  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
      <div style={{ position: "absolute", top: "60%", transform: "translateY(-50%)", fontFamily: clave ? F_FUERTE : F_SUB, fontWeight: clave ? 400 : 900,
        fontSize: clave ? 150 : 96, color: clave ? ACENTO : CREMA, textTransform: clave ? "uppercase" : "lowercase", letterSpacing: clave ? 0 : -2,
        textShadow: "0 4px 22px rgba(0,0,0,0.6), 0 2px 4px rgba(0,0,0,0.6)" }}>
        {limpia(w.w)}
      </div>
    </AbsoluteFill>
  );
};

const BLOQUES_V3: Bloque[] = [
  { desde: 3, hasta: 70, y: 0.66, palabras: [P("si eres un puto maricón", 3), P("QUE NO", 45, "fuerte", true), P("entrena", 52, "remate")] },
  { desde: 300, hasta: 342, y: 0.66, palabras: [P("en el", 300), P("MERCADONA", 305, "fuerte", true)] },
  { desde: 495, hasta: 528, y: 0.66, palabras: [P("depende de", 495), P("quién seas", 502, "remate", true)] },
];

const ENC_V3: Encuadre[] = [
  { desde: 0, escala: 1.0 },
  { desde: 2, escala: 1.15, suave: 5, empuje: 0.04 }, // golpe de entrada +15 % en 5 f
  { desde: 70, escala: 1.1, suave: 0, empuje: 0.045 },
  { desde: 97, escala: 1.32, suave: 12 }, // "chupar"
  { desde: 129, escala: 1.08, suave: 0, empuje: 0.045 },
  { desde: 210, escala: 1.08, suave: 0, empuje: 0.045 },
  { desde: 279, escala: 1.6, suave: 28 }, // zoom largo hacia el remate MERCADONA
  { desde: 342, escala: 1.1, suave: 0, empuje: 0.045 },
  { desde: 426, escala: 1.3, suave: 10 }, // congelados
  { desde: 462, escala: 1.12, suave: 0, empuje: 0.045 },
  { desde: 480, escala: 1.55, suave: 26 }, // zoom largo hacia "quién seas"
  { desde: 528, escala: 1.15, suave: 0, empuje: 0.04 },
];

// Música con hueco de 0,35 s antes de los dos remates
const MusicaConHuecos: React.FC = () => {
  const frame = useCurrentFrame();
  const v = (h: number) => interpolate(frame, [h - 11, h - 9, h, h + 3], [1, 0, 0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return <Audio src={MUSICA} volume={() => 0.1 * Math.min(v(305), v(502))} />;
};

export const SiNoEntrenasV3: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: "black" }}>
    <Grade>
      <CamaraVirtual encuadres={ENC_V3} cara={CARAS} frameBruto={bruto} shake={[{ desde: 305, hasta: 315, px: 8 }]}>
        <Base fin={17} />
        <TextoBloques bloques={BLOQUES_V3} pop escala={0.85} />
      </CamaraVirtual>
    </Grade>
    <PalabraSuelta ocultar={BLOQUES_V3.map((b) => [b.desde, b.hasta] as [number, number])} />
    <Sfx en={1} src="whoosh-short.mp3" volumen={0.4} />
    <Sfx en={304} src="impact-bass-2.mp3" volumen={0.55} />
    <Sfx en={501} src="impact-bass-1.mp3" volumen={0.4} />
    <MusicaConHuecos />
  </AbsoluteFill>
);

const comp = { fps: 30, width: 1080, height: 1920 };
export const SiNoEntrenasComps = () => (
  <>
    <Composition id="SiNoEntrenasV1" component={SiNoEntrenasV1} durationInFrames={DUR + 17} {...comp} />
    <Composition id="SiNoEntrenasV2" component={SiNoEntrenasV2} durationInFrames={DUR} {...comp} />
    <Composition id="SiNoEntrenasV3" component={SiNoEntrenasV3} durationInFrames={DUR + 17} {...comp} />
  </>
);
