// fisico-redes — gancho hablado a cámara (Lucas se quita la camiseta) + voz en off de Lucas sobre b-roll.
// Idea: reel de otro creador ("si este físico no te parece un buen físico, las redes te han frito la cabeza"), guion propio
// (físico honesto: sin tableta, no el más fuerte; maratón + medio Ironman; respeto a los culturistas; fitness real).
// Gancho: bruto terminado/2026-11-05_fisico-redes_01-gancho-a-camara-se-quita-camiseta.MOV (era IMG_1160) (estudio de posing, camiseta compresiva azul petróleo Gymshark), 4K HDR → proxy.sh … 2160.
//   "Soy Lucas" (4,55–5,62) → salto al momento en que se saca la camiseta (8,15–9,90, lo pidió Lucas) → resto del gancho (11,25–16,08).
//   Audio (elegido por Lucas con previas): 52 % voz aislada (ElevenLabs) + 73 % del original (highpass 130 ×2) en todo el tramo,
//   + noisereduce suave (perfil 0,5–4,4 s, prop_decrease 0,55) + ruido −8 dB entre palabras; guardado a −19 LUFS en el habla.
//   Más aislado distorsionaba la voz; noisereduce al 0,9 la dejaba "enlatada".
//   Historial: aislado + 12 % (1.ª, le gustó el tono pero "distorsiona" — el render pasaba de 0 dBFS) → original + afftdn → noisereduce ("enlatada").
// Voz: bruto terminado/2026-11-05_fisico-redes_02-voz-lucas.m4a (era "Passeig de la Marina, 27 2.m4a") → SIN aislar (la nota está limpia: 37 dB de voz sobre ruido),
//   highpass 80, retoma "ayudar un pa--" quitada (63,36–65,72), pausas entre palabras recortadas a 0,4 s, sin acelerar,
//   ganancia fija a −16 LUFS (sin loudnorm dinámico ni limitador: Lucas, "la normalización es too much… me distorsiona la voz").
// Música (pedida por Lucas): "Champagne Coast – Piano Version" (Penguin Piano), el audio de Instagram 967785882675803;
//   bajada de YouTube 1tQTkf4DEgs, desde 0,8 s, −14 LUFS en el archivo y 0,13 en la mezcla.
// Recursos de Lucas: recursos/… (proxies 2160×3840 con proxy.sh; rutas en scratchpad → ver recursos/INDICE.md, "Usado en: fisico-redes"). Clips de fuera (x<id>): Pexels (licencia libre), vídeos
//   27869330, 27869331, 35585696, 38627590, 38627617, 8859327, 8861900, 30234647, 36072027, 38410499, 7877141, 39593839.
import { Audio, Video } from "@remotion/media";
import React from "react";
import { AbsoluteFill, Composition, Easing, interpolate, Sequence, staticFile, useCurrentFrame } from "remotion";
import { Bloque, CamaraVirtual, Sfx, TextoBloques } from "../../comun/hablando";
import { RotuloHandle } from "../../comun/Rotulos";
import { Palabra, Subtitulos } from "../../comun/Subtitulos";
import ganchoPalabras from "./gancho-palabras.json";
import vozPalabras from "./voz-palabras.json";

const S = "fisico-redes";
// Voz y gancho son mono a −16 LUFS (ganancia fija, sin compresor): en el render estéreo suben +3 dB → −3 dB en la mezcla (≈ −16 LUFS final).
// Toda la mezcla va 3 dB baja (MEZCLA) para que nada sature dentro del render; el volumen final (−14 LUFS) se pone después con ganancia fija.
const MEZCLA = 0.7;
const GAIN_VOZ = 0.71 * MEZCLA;
// gancho-audio.mp3 va guardado 3 dB por debajo (un transitorio pasaba de 0 dBFS y el mp3 lo recortaba) → se compensa aquí.
const GANCHO_EXTRA = 1.6; // +1,1 dB más para que el gancho suene igual que la voz en off (medido en el render)
const FPS = 30;
const f = (s: number) => Math.round(s * FPS);

// ---------------------------------------------------------------- gancho (tramos del bruto)
const TRAMOS = [
  { desde: 4.55, hasta: 5.62, nota: "Soy Lucas" }, // la "s" de Lucas dura hasta ~5,55 (energía medida)
  { desde: 8.15, hasta: 9.9, nota: "se quita la camiseta" },
  { desde: 11.25, hasta: 16.08, nota: "y déjame decirte… frito el cerebro" },
];
const INI_TRAMO: number[] = [];
TRAMOS.reduce((acc, t) => (INI_TRAMO.push(acc), acc + (t.hasta - t.desde)), 0);
const HOOK = INI_TRAMO[2] + (TRAMOS[2].hasta - TRAMOS[2].desde);
// palabras del gancho en tiempo del edit
const GANCHO: Palabra[] = (ganchoPalabras as (Palabra & { hablante?: string })[]).flatMap((p) => {
  const i = TRAMOS.findIndex((t) => p.start >= t.desde - 0.02 && p.start < t.hasta);
  if (i < 0) return [];
  const d = INI_TRAMO[i] - TRAMOS[i].desde;
  return [{ w: p.w, start: p.start + d, end: Math.min(p.end, TRAMOS[i].hasta) + d }];
});

// ---------------------------------------------------------------- voz en off
const VOZ_DESDE = HOOK - 0.2; // la 1.ª palabra ("Llevo", 0,27 s en voz.mp3) cae justo después del gancho
const VOZ: Palabra[] = (vozPalabras as Palabra[]).map((p) => ({ w: p.w, start: p.start + VOZ_DESDE, end: p.end + VOZ_DESDE }));
const FIN_VOZ = VOZ[VOZ.length - 1].end;
const DUR = f(FIN_VOZ + 1.3);
const SIGUEME = VOZ.find((p) => /^Sígueme/.test(p.w))!.start;

// Planos de la voz en off: v = s de voz.mp3 en que empieza (cada uno hasta el siguiente), desde = s del clip.
type Plano = { v: number; clip: string; desde: number; nota: string; zoom?: number; origen?: string; exposicion?: number }; // exposicion >1 solo en clips de Pexels muy oscuros (no son brutos de Lucas)
const PLANOS: Plano[] = [
  { v: 0.2, clip: "cfuerza", desde: 3.0, nota: "Llevo cuatro años entrenando fuerza (curl barra Z, neón STRENGTH)" },
  { v: 2.39, clip: "ccharcos", desde: 0.3, nota: "y ahora me estoy preparando una maratón (run club, charcos)" },
  { v: 4.51, clip: "ccinta", desde: 1.0, nota: "y medio Ironman (cinta, sudado)" },
  { v: 5.86, clip: "gancho", desde: 10.0, zoom: 1.45, origen: "50% 62%", nota: "No tengo tableta (su abdomen, del gancho)" },
  { v: 7.13, clip: "cinclinado", desde: 2.0, nota: "no soy el más fuerte del gimnasio (curl inclinado)" },
  { v: 9.25, clip: "cposes", desde: 0.5, nota: "y obviamente podría estar mejor (posing, misma camiseta)" },
  { v: 11.58, clip: "cposes", desde: 10.0, nota: "Pero es un físico sano, estético (side chest)" },
  { v: 13.87, clip: "cwallballs", desde: 13.3, nota: "y funcional (wall balls)" },
  { v: 14.94, clip: "x38410499", desde: 0.5, nota: "Lo que pasa es que en redes ves a (móvil, reels) · Pexels" },
  { v: 16.82, clip: "x35585696", desde: 0.5, nota: "chavales de dieciocho años (chaval mamado) · Pexels" },
  { v: 18.35, clip: "x38627590", desde: 5.0, nota: "hipermamados (doble bíceps de espaldas, culturista) · Pexels" },
  { v: 19.33, clip: "x27869330", desde: 5.0, nota: "hasta arriba de esteroides (culturista enorme) · Pexels" },
  { v: 21.06, clip: "x8861900", desde: 2.0, nota: "con la mejor luz (luz de estudio) · Pexels" },
  { v: 22.19, clip: "x8859327", desde: 2.0, nota: "recién bombeados (espalda brillante) · Pexels" },
  { v: 23.35, clip: "x30234647", desde: 3.0, exposicion: 1.6, nota: "y con filtro (gym con filtro verde) · Pexels" },
  { v: 24.61, clip: "cespejo", desde: 2.9, nota: "Y luego te miras al espejo" },
  { v: 26.11, clip: "cespejo", desde: 12.0, nota: "y piensas que lo estás haciendo fatal" },
  { v: 29.05, clip: "cposes", desde: 19.0, zoom: 1.12, origen: "50% 35%", nota: "Pues no. (de frente, puños juntos)" },
  { v: 30.14, clip: "cducha", desde: 1.0, nota: "Si te comparas con eso, te vas a deprimir (ducha, luz roja)" },
  { v: 32.51, clip: "ccajon", desde: 8.6, nota: "y vas a acabar dejándolo (sentado, Nike Strength)" },
  { v: 34.21, clip: "x38627617", desde: 6.0, nota: "Y ojo, respeto máximo a los culturistas (escenario) · Pexels" },
  { v: 36.51, clip: "x27869331", desde: 5.0, nota: "Tienen físicos de la hostia (pose en escenario) · Pexels" },
  { v: 38.07, clip: "x36072027", desde: 2.0, exposicion: 1.6, nota: "y se lo curran muchísimo (entreno duro, gym oscuro) · Pexels" },
  { v: 39.57, clip: "cposes", desde: 8.0, nota: "pero es su deporte, no el tuyo (de lado)" },
  { v: 42.03, clip: "csonrie", desde: 16.0, nota: "Un buen físico es el que te hace verte bien (sonríe sin camiseta)" },
  { v: 44.57, clip: "clata", desde: 1.5, nota: "sentirte bien (run club, sonrisa)" },
  { v: 45.51, clip: "cskierg", desde: 4.6, nota: "y que el cuerpo te responda (SkiErg)" },
  { v: 47.83, clip: "cdunas", desde: 3.0, nota: "Correr (dunas al atardecer)" },
  { v: 48.59, clip: "x7877141", desde: 2.2, exposicion: 0.85, nota: "subir unas escaleras sin ahogarte · Pexels" },
  { v: 50.73, clip: "x39593839", desde: 0, nota: "aguantar un partido con tus amigos (fútbol de noche) · Pexels" },
  { v: 52.71, clip: "cposes", desde: 13.0, nota: "Eso es lo que tienes que buscar (de frente, posing)" },
  { v: 55.11, clip: "cfinal", desde: 1.9, nota: "Sígueme para más fitness real (se acerca y tapa la cámara)" },
];
const EN = (p: Plano) => VOZ_DESDE + p.v;
const CORTES = PLANOS.map(EN);

// Exposición del gancho (pedida por Lucas, 2026-11-05: "sube un poco la exposición en la intro para que se me vea un poquito más moreno")
// → un poco más de exposición + algo más cálido (solo exposición aclaraba la piel, lo contrario de "más moreno"). También en el plano de "No tengo tableta".
const FILTRO_GANCHO = "brightness(1.07) saturate(1.12) sepia(0.06)";
const Planos: React.FC = () => (
  <>
    {PLANOS.map((p, i) => {
      const ini = f(EN(p));
      const fin = i < PLANOS.length - 1 ? f(EN(PLANOS[i + 1])) : DUR;
      return (
        <Sequence key={i} name={p.nota} from={ini} durationInFrames={fin - ini} premountFor={FPS}>
          <AbsoluteFill style={{ transform: `scale(${p.zoom ?? 1})`, transformOrigin: p.origen ?? "50% 50%", filter: p.clip === "gancho" ? FILTRO_GANCHO : p.exposicion ? `brightness(${p.exposicion})` : undefined }}>
            <Video src={staticFile(`${S}/${p.clip}.mp4`)} trimBefore={f(p.desde)} muted style={{ width: "100%", height: "100%" }} />
          </AbsoluteFill>
        </Sequence>
      );
    })}
  </>
);

// Gancho: zoom de entrada 1→1,12 con whoosh (siempre en hablando a cámara), plano abierto al quitarse la camiseta, empuje lento después
// y golpe corto hacia "frito el cerebro".
const FRITO = GANCHO.find((p) => /^frito/.test(p.w))!.start;
const ENCUADRES = [
  // centro por encima de la cara (cy 300) para que al hacer zoom la cabeza BAJE y no pise el texto de arriba (CONTEXTO hablando, punto 17)
  { desde: 0, escala: 1.0, cx: 540, cy: 300 },
  { desde: 1, escala: 1.12, cx: 540, cy: 300, suave: 26 },
  { desde: f(INI_TRAMO[1]), escala: 1.0, cx: 540, cy: 900 },
  { desde: f(INI_TRAMO[2]), escala: 1.03, cx: 540, cy: 300, empuje: 0.015 },
  { desde: f(FRITO) - 10, escala: 1.06, cx: 540, cy: 300, suave: 10 }, // golpe suave: aquí ya se acerca a cámara y la cabeza sube hacia el texto
];

const Gancho: React.FC = () => (
  <AbsoluteFill style={{ filter: FILTRO_GANCHO }}>
  <CamaraVirtual encuadres={ENCUADRES}>
    {TRAMOS.map((t, i) => (
      <Sequence key={i} name={`Gancho · ${t.nota}`} from={f(INI_TRAMO[i])} durationInFrames={f(INI_TRAMO[i] + t.hasta - t.desde) - f(INI_TRAMO[i])}>
        <Video src={staticFile(`${S}/gancho.mp4`)} trimBefore={f(t.desde)} muted style={{ width: "100%", height: "100%" }} />
      </Sequence>
    ))}
  </CamaraVirtual>
  </AbsoluteFill>
);

const GanchoAudio: React.FC = () => (
  <>
    {TRAMOS.map((t, i) => (
      <Sequence key={i} name={`Audio gancho · ${t.nota}`} from={f(INI_TRAMO[i])} durationInFrames={f(INI_TRAMO[i] + t.hasta - t.desde) - f(INI_TRAMO[i])}>
        <Audio src={staticFile(`${S}/gancho-audio.mp3`)} trimBefore={f(t.desde)} volume={GAIN_VOZ * GANCHO_EXTRA} />
      </Sequence>
    ))}
  </>
);

// Texto del gancho (pedido por Lucas): "La realidad del fitness está totalmente alterada", palabra a palabra, encima de la cabeza.
const T = [0.12, 0.32, 0.5, 0.68, 0.95, 1.35, 1.85];
const BLOQUES: Bloque[] = [
  {
    desde: f(T[0]),
    hasta: f(HOOK),
    y: 0.158,
    palabras: [
      { texto: "La", desde: f(T[0]), estilo: "relleno" },
      { texto: "realidad", desde: f(T[1]), estilo: "relleno" },
      { texto: "del", desde: f(T[2]), estilo: "relleno" },
      { texto: "fitness", desde: f(T[3]), estilo: "relleno" },
      { texto: "está", desde: f(T[4]), estilo: "relleno" },
      { texto: "totalmente", desde: f(T[5]), estilo: "fuerte", salto: true },
      { texto: "alterada", desde: f(T[6]), estilo: "remate" },
    ],
  },
];

// CTA: en "Sígueme" sale el @ (regla de Lucas), con pop suave
const Handle: React.FC = () => {
  const frame = useCurrentFrame();
  const o = interpolate(frame, [0, 5], [0, 1], { extrapolateRight: "clamp" });
  const sc = interpolate(frame, [0, 8], [0.8, 1], { extrapolateRight: "clamp", easing: Easing.out(Easing.back(2)) });
  return (
    <AbsoluteFill style={{ alignItems: "center", paddingTop: 1300 }}>
      <div style={{ opacity: o, transform: `scale(${sc})` }}>
        <RotuloHandle size={84} />
      </div>
    </AbsoluteFill>
  );
};

const CLAVES = /^(hipermamados|esteroides|filtro|deprimir|culturistas|sano|estético|funcional|real|tableta|maratón|ironman)$/i;

const FisicoRedes: React.FC = () => {
  const frame = useCurrentFrame();
  const musica = interpolate(frame, [0, DUR - 30, DUR], [0.13 * MEZCLA, 0.13 * MEZCLA, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ backgroundColor: "black" }}>
      <Sequence name="GANCHO" durationInFrames={f(HOOK)}>
        <Gancho />
        <TextoBloques bloques={BLOQUES} pop escala={0.68} interlinea={14} />
      </Sequence>
      <Sequence name="VOZ EN OFF · planos" from={0}>
        <Planos />
      </Sequence>
      {/* Subtítulos del gancho más abajo (sobre el pantalón) para no tapar el físico ni el texto de arriba */}
      <Subtitulos palabras={GANCHO} offset={0} top={1390} claves={/^(frito|cerebro|físico)$/i} cortes={[INI_TRAMO[1], INI_TRAMO[2], HOOK]} maxHueco={0.4} />
      <Subtitulos palabras={VOZ} offset={0} claves={CLAVES} cortes={CORTES} maxHueco={0.5} />
      <Sequence name="CTA · @lucasalvarez.x" from={f(SIGUEME)}>
        <Handle />
      </Sequence>
      {/* Sonido */}
      <Sfx en={0} src="whoosh.mp3" volumen={0.45 * MEZCLA} />
      <Sfx en={0} src="impact-bass-1.mp3" volumen={0.25 * MEZCLA} />
      <Sfx en={f(T[0])} src="sparkle.mp3" volumen={0.22 * MEZCLA} />
      <Sfx en={f(HOOK) - 4} src="whoosh.mp3" volumen={0.35 * MEZCLA} />
      <Sfx en={f(EN(PLANOS[17]))} src="impact-bass-2.mp3" volumen={0.3 * MEZCLA} />
      <Sfx en={f(SIGUEME)} src="pop.mp3" volumen={0.35 * MEZCLA} />
      <GanchoAudio />
      <Sequence from={f(VOZ_DESDE)} name="Voz en off">
        <Audio src={staticFile(`${S}/voz.mp3`)} volume={GAIN_VOZ} />
      </Sequence>
      <Audio src={staticFile(`${S}/musica.mp3`)} volume={() => musica} />
    </AbsoluteFill>
  );
};

export const FisicoRedesComp: React.FC = () => (
  <Composition id="FisicoRedes" component={FisicoRedes} durationInFrames={DUR} fps={FPS} width={1080} height={1920} />
);
