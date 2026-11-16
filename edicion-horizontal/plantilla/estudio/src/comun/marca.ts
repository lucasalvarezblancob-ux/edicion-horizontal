// MARCA: color de acento, cuentas y fuentes de los gráficos de serie.
// El color y las cuentas son de cada CREADOR: están en personal/<creador>/marca.json; paso3_plan.py los copia a
// capas.json y CapasBase los activa con usarMarca() al pintar. Aquí solo queda el estándar (amarillo-lima, sin rosa).
// Las fuentes sí se cambian aquí (Google Fonts vía @remotion/google-fonts): este archivo es LOCAL, la skill no lo pisa.
import { loadFont as loadUnbounded } from "@remotion/google-fonts/Unbounded";
import { loadFont as loadLexend } from "@remotion/google-fonts/Lexend";
import { loadFont as loadInter } from "@remotion/google-fonts/Inter";

export type Marca = { acento?: string; canal?: string; handle?: string; codigo?: string };
const SERIE = "#E6EC52";
// Color de acento: datos, cifras, palabra-golpe, número de capítulo, flechas. Uno solo por vídeo.
export let ACENTO: string = SERIE;
// Cuentas (rótulos de suscripción / sígueme) y código de descuento ("" si no hay).
export let CANAL = "";
export let HANDLE = "";
export let CODIGO = "";
export const usarMarca = (m?: Marca) => {
  ACENTO = (m && m.acento) || SERIE;
  CANAL = (m && m.canal) || "";
  HANDLE = (m && m.handle) || "";
  CODIGO = (m && m.codigo) || "";
};

// Fuentes (refs/dinamicos/CONTEXTO.md → Textos y títulos):
// F_ANCHA: familia ancha y negra para TODO lo grande (título, capítulo, cifra, palabra-golpe, nombre del animal).
// F_TXT: línea pequeña, subtítulos y comentarios del editor.   F_RELLENO: texto de relleno (píldoras, créditos).
export const F_ANCHA = loadUnbounded("normal", { weights: ["700", "900"], subsets: ["latin", "latin-ext"] }).fontFamily;
export const F_TXT = loadLexend("normal", { weights: ["600", "800"], subsets: ["latin", "latin-ext"] }).fontFamily;
export const F_RELLENO = loadInter("normal", { weights: ["600", "800"], subsets: ["latin", "latin-ext"] }).fontFamily;
