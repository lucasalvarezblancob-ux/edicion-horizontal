// Genera un efecto de sonido a partir de una descripción (ElevenLabs Sound Effects).
// Para sonidos que no están en personal/<creador>/recursos/sonidos/ (beber, echar agua, báscula…). Guarda lo útil ahí.
//
// Uso (desde estudio/):
//   node --env-file=.env.local scripts/sfx.mjs "descripción en inglés" salida.mp3 [duración_s] [influencia 0-1]
import { ElevenLabsClient } from "@elevenlabs/elevenlabs-js";
import fs from "node:fs";
import { Readable } from "node:stream";
import { pipeline } from "node:stream/promises";

const [texto, salida, dur, infl] = process.argv.slice(2);
if (!texto || !salida) throw new Error('Uso: scripts/sfx.mjs "descripción" salida.mp3 [duración_s] [influencia]');

const client = new ElevenLabsClient();
const stream = await client.textToSoundEffects.convert({
  text: texto,
  durationSeconds: dur ? Number(dur) : undefined,
  promptInfluence: infl ? Number(infl) : 0.6,
});
await pipeline(Readable.fromWeb(stream), fs.createWriteStream(salida));
console.log(`ok: ${salida}`);
