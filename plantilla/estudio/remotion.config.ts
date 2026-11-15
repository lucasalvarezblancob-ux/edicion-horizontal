/**
 * Note: When using the Node.JS APIs, the config file
 * doesn't apply. Instead, pass options directly to the APIs.
 *
 * All configuration options: https://remotion.dev/docs/config
 */

import { Config } from "@remotion/cli/config";

Config.setRspack(true);
// Color y calidad (2026-11-01): fotogramas PNG (JPEG 80 metía artefactos), matriz y etiquetas bt709 como los proxies
// (por defecto Remotion codifica bt601 sin etiquetar + curva sRGB → QuickTime/iPhone lo muestran con otro color).
Config.setVideoImageFormat("png");
Config.setColorSpace("bt709");
Config.setCrf(15);
Config.setOverwriteOutput(true);
Config.setDefaultPremountInSeconds(2);
