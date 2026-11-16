// MARCA de esta carpeta de edición (LOCAL): color, fuentes, @ y código de descuento.
// Cámbialo a tu gusto: la skill edicion-reels no lo pisa al actualizarse.
// Las fuentes son de Google Fonts vía @remotion/google-fonts (cambia el import y el loadFont).
import { loadFont as loadMontserrat } from "@remotion/google-fonts/Montserrat";
import { loadFont as loadQuicksand } from "@remotion/google-fonts/Quicksand";
import { loadFont as loadInter } from "@remotion/google-fonts/Inter";
import { loadFont as loadAnton } from "@remotion/google-fonts/Anton";
import { loadFont as loadInstrument } from "@remotion/google-fonts/InstrumentSerif";
import { loadFont as loadCaveat } from "@remotion/google-fonts/Caveat";

// Color de acento: subtítulos clave, títulos, rótulos, pegatina del nombre. Uno solo por vídeo.
// Por defecto, amarillo-lima (el estándar). Nada de rosa salvo que tú lo cambies aquí.
export const ACENTO = "#E6EC52";
// Crema: línea pequeña de los rótulos y relleno del texto a cámara.
export const CREMA = "#F1E7D6";

// Tu @ de Instagram (rótulo de "Sígueme") y tu código de descuento ("" si no tienes).
export const HANDLE = "@tuusuario";
export const CODIGO = "";

// Fuentes
export const SUB_FONT = loadMontserrat("normal", { weights: ["800"], subsets: ["latin", "latin-ext"] }).fontFamily; // subtítulos palabra a palabra
export const TITLE_FONT = loadQuicksand("normal", { weights: ["500", "700"], subsets: ["latin", "latin-ext"] }).fontFamily; // Titulo / Clave
export const F_RELLENO = loadInter("normal", { weights: ["600", "800"], subsets: ["latin", "latin-ext"] }).fontFamily; // texto de relleno / línea pequeña
export const F_FUERTE = loadAnton("normal", { weights: ["400"], subsets: ["latin", "latin-ext"] }).fontFamily; // rótulos y palabra fuerte (mayúsculas)
export const F_REMATE = loadInstrument("italic", { weights: ["400"], subsets: ["latin", "latin-ext"] }).fontFamily; // remate en cursiva
export const F_SUB = loadMontserrat("normal", { weights: ["900"], subsets: ["latin", "latin-ext"] }).fontFamily;
export const F_MANO = loadCaveat("normal", { weights: ["700"], subsets: ["latin"] }).fontFamily; // pegatina del nombre
