// regalo-la-vida — calco del reel de daviddelpinovidal (https://www.instagram.com/p/DfPC4CUosts/, ref en
// refs/montaje de vida/daviddelpinovidal_DfPC4CUosts.mp4) con clips de Lucas: montaje de "vida" (31 planos de 0,6–2,2 s,
// cortes secos sin zoom ni transiciones, como la ref) sobre el mismo audio (discurso "¿A qué le vas a tener miedo… es un
// regalo la vida", extraído de la ref → public/regalo-la-vida/audio.m4a) y el mismo texto en pantalla: frases cortas en crema
// (#FEFEBF), negrita sencilla, centradas en la pantalla, que cambian en los mismos instantes que en la ref.
// Tiempos de corte: detección de escena de la ref (ffmpeg scene > 0,25, revisados a 30 fps). Textos: OCR (tesseract a 10 fps).
// Exposición (preferencias → COLOR, excepción de Lucas): p90 de luminancia en la franja del texto ≥ 175 → 0,80; ≥ 145 → 0,85.
// Cada plano casa con la frase y con el tipo de plano de la ref (café al sol ↔ café, bici hacia cámara ↔ corre hacia cámara,
// barras de calistenia ↔ pasamanos de la playa, selfie con su madre ↔ selfie en el coche con amigos…).
// Clips: recursos/ (proxies 2160×3840 con herramientas/proxy.sh … 2160) → render con --scale=2 (hay brutos 4K).
// c07 y c19 (playa 2026-04-20, HDR exterior con sol): encima del proxy va ../monkey-branching/pasamanos-pantalla.cube (medida en QuickTime con el mismo pasamanos).
import { Audio, Video } from "@remotion/media";
import React from "react";
import { AbsoluteFill, Composition, Sequence, staticFile } from "remotion";
import { F_RELLENO } from "../../comun/hablando";

const S = "regalo-la-vida";
const FPS = 30;
const DUR = Math.round(36.7 * FPS); // misma duración que la ref
const f = (s: number) => Math.round(s * FPS);

// en = s del edit (cortes de la ref) · desde = s del clip · nota = texto + qué se ve (ref ↔ nuestro)
type Plano = { en: number; clip: string; desde: number; nota: string; zoom?: number; origen?: string; exposicion?: number };
const PLANOS: Plano[] = [
  { en: 0, clip: "c01-cafe", desde: 1.5, exposicion: 0.8, nota: "01 · café al sol (ref: café con maillot) — chiringuito" },
  { en: 1.567, clip: "c02-charcos", desde: 0.3, nota: "02 · de pie, plano frío (ref: entre rocas) — corriendo de espaldas en los charcos" },
  { en: 2.733, clip: "c03-brindis", desde: 0.5, nota: "03 · plan con gente dentro (ref: póker) — brindis del run club" },
  { en: 3.6, clip: "c04-tumbado", desde: 7.2, exposicion: 0.8, nota: "04 · ¿A qué? (ref: selfie en bata de hospital) — tumbado reventado tras el WOD" },
  { en: 4.533, clip: "c05-trail", desde: 1.0, exposicion: 0.8, nota: "05 · selfie contrapicado con cielo (ref: casco de moto) — trail, gafas rojas" },
  { en: 6.0, clip: "c06-dunas-frente", desde: 3.0, exposicion: 0.85, nota: "06 · viene hacia cámara (ref: bici) — corre por el paseo de las dunas" },
  { en: 7.367, clip: "c07-fondos-playa", desde: 4.0, nota: "07 · a todo (ref: encima de una roca) — fondos en la playa" },
  { en: 8.3, clip: "c08-ducha", desde: 2.0, nota: "08 · a todo, agua (ref: nadando en el mar) — ducha del spa" },
  { en: 9.333, clip: "c09-amanecer", desde: 2.0, nota: "09 · si te vas a morir (ref: cascada) — corriendo al amanecer junto al mar" },
  { en: 10.333, clip: "c10-selfie-pinos", desde: 7.0, exposicion: 0.8, nota: "10 · selfie cerca, pinos (ref: sombrero y gafas) — selfie en Francia" },
  { en: 11.467, clip: "c11-tank-pull", desde: 1.0, exposicion: 0.8, nota: "11 · Lucha, dale para adelante (ref: buceando) — tank pull en la DEKA" },
  { en: 13.033, clip: "c12-burpee", desde: 1.0, exposicion: 0.85, nota: "12 · haz lo que sientas (ref: sin camiseta en box de OSB) — burpee + saco en Olimpia" },
  { en: 13.633, clip: "c13-atardecer", desde: 2.2, nota: "13 · haz lo que quieras (ref: nieve al atardecer) — corriendo de espaldas al atardecer" },
  { en: 15.5, clip: "c14-brazos-cruzados", desde: 2.5, nota: "14 · sé tú (ref: primer plano con gafas de esquí) — posado brazos cruzados" },
  { en: 16.367, clip: "c15-wall-balls", desde: 14.1, nota: "15 · saca la mejor versión (ref: sentadilla con barra) — wall balls" },
  { en: 17.333, clip: "c16-reveal", desde: 4.6, exposicion: 0.8, nota: "16 · de ti mismo — de frente sin camiseta (gym neón azul)" },
  { en: 18.567, clip: "c17-salto-playa", desde: 0.5, nota: "17 · sé tú (ref: salto a la poza) — sentadillas con salto en la arena" },
  { en: 19.667, clip: "c18-rio", desde: 3.0, nota: "18 · haz lo que sientas (ref: surf) — corriendo junto al río" },
  { en: 20.533, clip: "c19-pasamanos", desde: 12.0, nota: "19 · por eso viniste a este mundo (ref: barras al aire libre) — pasamanos de la playa" },
  { en: 21.933, clip: "c20-carrera", desde: 1.0, exposicion: 0.85, nota: "20 · es un regalo la vida (ref: snow) — carrera con dorsal, sol bajo" },
  { en: 22.9, clip: "c21-selfie-playa", desde: 0.2, exposicion: 0.85, nota: "21 · es un regalo la vida (ref: selfie con un amigo) — selfie en la playa con el grupo" },
  { en: 23.867, clip: "c22-coche", desde: 13.0, nota: "22 · ¡ES UN REGALO LA VIDA! (ref: selfie con su madre) — selfie en el coche con amigos" },
  { en: 25.433, clip: "c23-abrazo", desde: 0.5, exposicion: 0.8, nota: "23 · ¡ES UN REGALO LA VIDA! (ref: con gente local) — abrazo en la meta de la DEKA" },
  { en: 27.133, clip: "c24-medalla", desde: 0.5, exposicion: 0.85, nota: "24 · Disfrútala / siéntela (ref: tirado en el suelo) — mordiendo la medalla" },
  { en: 27.767, clip: "c25-celebracion", desde: 1.0, exposicion: 0.85, nota: "25 · siéntela / vívela (ref: tiro) — brazos arriba bajo la lluvia" },
  { en: 29.4, clip: "c26-pinos", desde: 1.0, nota: "26 · ama mucho (ref: caída en la nieve) — selfie corriendo entre pinos" },
  { en: 30.133, clip: "c27-grupo", desde: 0.3, exposicion: 0.8, nota: "27 · haz amigos (ref: amigos en quad) — el run club hacia cámara" },
  { en: 30.733, clip: "c28-pov-dorsal", desde: 3.6, exposicion: 0.85, nota: "28 · haz amigos (ref: POV pies entre rocas) — POV pies y dorsal" },
  { en: 31.967, clip: "c29-colgado", desde: 5.6, exposicion: 0.85, nota: "29 · ríete mucho (ref: paseo por el bosque) — colgado de las barras riéndose" },
  { en: 34.167, clip: "c30-selfie-grupo", desde: 0.2, exposicion: 0.8, nota: "30 · porque ya va a llegar… (ref: selfie con amigos) — selfie con el grupo" },
  { en: 35.6, clip: "c31-anochecer", desde: 8.9, exposicion: 0.8, nota: "31 · La oscuridad. (ref: ciervos, calma) — brazos abiertos al anochecer" },
];

// Texto en pantalla (mismas frases e instantes que la ref; "de ti misma" → "de ti mismo" y con tildes)
type Texto = { en: number; hasta?: number; t: string };
const TEXTOS: Texto[] = [
  { en: 0, t: "¿A qué le vas a tener miedo?" },
  { en: 1.567, t: "si nos vamos a morir..." },
  { en: 3.6, t: "¿A qué?" },
  { en: 4.533, t: "¿A qué le puedes tener miedo?" },
  { en: 6.0, t: "La gente tiene miedo a todo" },
  { en: 7.367, t: "a todo" },
  { en: 9.333, t: "si te vas a morir..." },
  { en: 10.333, t: "¿A qué le puedes tener miedo?" },
  { en: 11.467, t: "Lucha, dale para adelante" },
  { en: 13.033, t: "haz lo que sientas" },
  { en: 13.633, t: "haz lo que quieras" },
  { en: 15.5, t: "sé tú" },
  { en: 16.367, t: "saca la mejor versión" },
  { en: 17.333, t: "de ti mismo" },
  { en: 18.567, t: "sé tú" },
  { en: 19.667, t: "haz lo que sientas" },
  { en: 20.533, t: "por eso viniste a este mundo" },
  { en: 21.933, t: "es un regalo la vida" },
  { en: 23.867, t: "¡ES UN REGALO LA VIDA!" },
  { en: 27.133, t: "Disfrútala" },
  { en: 27.6, t: "siéntela" },
  { en: 28.5, t: "vívela" },
  { en: 29.4, t: "ama mucho" },
  { en: 30.133, hasta: 31.5, t: "haz amigos" },
  { en: 31.967, t: "ríete mucho" },
  { en: 34.167, t: "porque ya va a llegar..." },
  { en: 35.6, t: "La oscuridad." },
];

const Planos: React.FC = () => (
  <>
    {PLANOS.map((p, i) => {
      const ini = f(p.en);
      const fin = i < PLANOS.length - 1 ? f(PLANOS[i + 1].en) : DUR;
      return (
        <Sequence key={i} name={p.nota} from={ini} durationInFrames={fin - ini} premountFor={FPS}>
          <AbsoluteFill
            style={{
              transform: `scale(${p.zoom ?? 1})`,
              transformOrigin: p.origen ?? "50% 50%",
              filter: p.exposicion ? `brightness(${p.exposicion})` : undefined,
            }}
          >
            <Video src={staticFile(`${S}/${p.clip}.mp4`)} trimBefore={f(p.desde)} muted style={{ width: "100%", height: "100%" }} />
          </AbsoluteFill>
        </Sequence>
      );
    })}
  </>
);

// Letra de la ref: sans negrita sencilla, crema, sin fondo, centrada (centro ≈ y 964 de 1920), ~620 px de ancho la frase larga
const Frase: React.FC<{ t: string }> = ({ t }) => (
  <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
    <div
      style={{
        fontFamily: F_RELLENO,
        fontWeight: 700,
        fontSize: 39,
        color: "#FEFEBF",
        textAlign: "center",
        letterSpacing: -0.2,
        textShadow: "0 1px 6px rgba(0,0,0,0.35)",
        marginTop: 8,
      }}
    >
      {t}
    </div>
  </AbsoluteFill>
);

const Textos: React.FC = () => (
  <>
    {TEXTOS.map((x, i) => {
      const ini = f(x.en);
      const fin = f(x.hasta ?? (i < TEXTOS.length - 1 ? TEXTOS[i + 1].en : DUR / FPS));
      return (
        <Sequence key={i} name={`texto · ${x.t}`} from={ini} durationInFrames={fin - ini}>
          <Frase t={x.t} />
        </Sequence>
      );
    })}
  </>
);

const RegaloLaVida: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: "black" }}>
    <Planos />
    <Textos />
    <Audio src={staticFile(`${S}/audio.m4a`)} />
  </AbsoluteFill>
);

export const RegaloLaVidaComp: React.FC = () => (
  <Composition id="RegaloLaVida" component={RegaloLaVida} durationInFrames={DUR} fps={FPS} width={1080} height={1920} />
);
