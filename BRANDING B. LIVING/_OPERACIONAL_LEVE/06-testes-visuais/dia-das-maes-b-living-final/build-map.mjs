import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.dirname(fileURLToPath(import.meta.url));
const input = path.join(root, 'data', 'florianopolis-ibge-4205407.geojson');
const output = path.join(root, 'assets', 'florianopolis-ibge-map.svg');

const geojson = JSON.parse(fs.readFileSync(input, 'utf8'));
const geometry = geojson.features?.[0]?.geometry ?? geojson.geometry;

function collectRings(geom) {
  if (!geom) return [];
  if (geom.type === 'Polygon') return geom.coordinates;
  if (geom.type === 'MultiPolygon') return geom.coordinates.flat();
  throw new Error(`Unsupported geometry type: ${geom.type}`);
}

const rings = collectRings(geometry);
const points = rings.flat();
const minLon = Math.min(...points.map(([lon]) => lon));
const maxLon = Math.max(...points.map(([lon]) => lon));
const minLat = Math.min(...points.map(([, lat]) => lat));
const maxLat = Math.max(...points.map(([, lat]) => lat));

const width = 720;
const height = 940;
const pad = 34;
const lonSpan = maxLon - minLon;
const latSpan = maxLat - minLat;
const scale = Math.min((width - pad * 2) / lonSpan, (height - pad * 2) / latSpan);
const drawnWidth = lonSpan * scale;
const drawnHeight = latSpan * scale;
const offsetX = (width - drawnWidth) / 2;
const offsetY = (height - drawnHeight) / 2;

function project([lon, lat]) {
  const x = offsetX + (lon - minLon) * scale;
  const y = offsetY + (maxLat - lat) * scale;
  return [Number(x.toFixed(2)), Number(y.toFixed(2))];
}

function simplifyRing(ring) {
  const keepEvery = Math.max(1, Math.ceil(ring.length / 520));
  const simplified = ring.filter((_, index) => index % keepEvery === 0);
  if (simplified.length > 0) simplified.push(ring[ring.length - 1]);
  return simplified;
}

const pathData = rings
  .map((ring) => simplifyRing(ring).map(project))
  .map((ring) => ring.map(([x, y], index) => `${index === 0 ? 'M' : 'L'} ${x} ${y}`).join(' ') + ' Z')
  .join(' ');

const svg = `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${width} ${height}" role="img" aria-label="Contorno oficial do municipio de Florianopolis, Santa Catarina, fonte IBGE">
  <path d="${pathData}" fill="none" stroke="#b79b69" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round"/>
  <path d="${pathData}" fill="#b79b69" opacity="0.055"/>
  <g opacity="0.42" stroke="#b79b69" stroke-width="0.9" fill="none">
    <path d="M 128 628 C 218 572, 288 572, 374 598 S 526 624, 596 556"/>
    <path d="M 174 728 C 266 672, 346 666, 432 704"/>
    <path d="M 250 320 C 326 390, 370 438, 490 458"/>
  </g>
</svg>`;

fs.writeFileSync(output, svg);
console.log(output);
