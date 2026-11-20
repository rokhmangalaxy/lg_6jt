// Run: node tests/test_logo_preview.cjs
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const assert = require('node:assert/strict');

const html = fs.readFileSync('html/index.html', 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];
new vm.Script(script); // Check complete application syntax.

// --- Mesin warna: disimpan utuh untuk fitur susunan palet yang ditunda. ---
const funcs = script.match(/function recolor\(original,palette\)\{[\s\S]*?\n\}/)[0];
const sandbox = { Uint8ClampedArray, ImageData: class { constructor(data, width, height) { Object.assign(this, { data, width, height }); } } };
vm.createContext(sandbox);
vm.runInContext(`const rgb=hex=>[1,3,5].map(n=>parseInt(hex.slice(n,n+2),16));${funcs};this.recolor=recolor;`, sandbox);
const src = { width: 3, height: 1, data: new Uint8ClampedArray([220, 38, 38, 255, 23, 50, 87, 255, 255, 255, 255, 255]) };
const original = Array.from(src.data);
assert.deepEqual(Array.from(sandbox.recolor(src, ['#173257', '#dc2626', '#ffffff']).data), [23, 50, 87, 255, 220, 38, 38, 255, 255, 255, 255, 255]);
assert.deepEqual(Array.from(src.data), original, 'original pixels unchanged');
assert.deepEqual(Array.from(sandbox.recolor(src, ['#dc2626', '#173257', '#ffffff']).data), original, 'reset restores original');
assert.deepEqual(Array.from(sandbox.recolor(src, ['#000000', '#000000', '#000000']).data), [0, 0, 0, 255, 0, 0, 0, 255, 0, 0, 0, 255]);
console.log('PASS: JS syntax, simultaneous swap, source immutability, reset, custom palette');

const arrangements = JSON.parse(script.match(/const arrangements=(\[[\s\S]*?\]);/)[1]);
assert.equal(arrangements.length, 6);
assert.equal(new Set(arrangements.map((a) => a.join(','))).size, 6);
arrangements.forEach((a) => assert.deepEqual([...a].sort(), [0, 1, 2]));
console.log('PASS: 6 unique base-palette permutations kept for the postponed feature');

// --- Kontrak halaman: pustaka eksternal, tanpa base64, palet belum aktif. ---
assert.equal((html.match(/data:image\//g) || []).length, 0, 'no inlined base64 artwork');
assert(!html.includes('type="color"'), 'no custom color inputs');
assert(html.includes("const ASSET_BASE='';"), 'asset base marker for the root copy');
assert(!html.includes('id="presets"'), 'palette controls stay hidden until the feature is decided');
assert(html.includes('assets/manifest.js'), 'manifest loaded at runtime');
console.log('PASS: no inlined artwork, palette controls absent, manifest driven');

// Salinan root hanya berbeda pada awalan aset.
const rootPreview = fs.readFileSync('preview-logo-mcm.html', 'utf8');
assert.equal(rootPreview, html.replace("const ASSET_BASE='';", "const ASSET_BASE='html/';"), 'root copy parity');
console.log('PASS: preview-logo-mcm.html matches html/index.html with html/ asset prefix');

// --- Manifest dan aset di disk. ---
function webpSize(buffer) {
  assert.equal(buffer.toString('ascii', 0, 4), 'RIFF');
  assert.equal(buffer.toString('ascii', 8, 12), 'WEBP');
  let offset = 12;
  while (offset + 8 <= buffer.length) {
    const id = buffer.toString('ascii', offset, offset + 4);
    const size = buffer.readUInt32LE(offset + 4);
    const payload = offset + 8;
    if (id === 'VP8X') {
      return { w: 1 + buffer.readUIntLE(payload + 4, 3), h: 1 + buffer.readUIntLE(payload + 7, 3) };
    }
    if (id === 'VP8 ') {
      return { w: buffer.readUInt16LE(payload + 6) & 0x3fff, h: buffer.readUInt16LE(payload + 8) & 0x3fff };
    }
    if (id === 'VP8L') {
      const bits = buffer.readUInt32LE(payload + 1);
      return { w: 1 + (bits & 0x3fff), h: 1 + ((bits >> 14) & 0x3fff) };
    }
    offset += 8 + size + (size % 2);
  }
  throw new Error('ukuran WebP tidak terbaca');
}

const manifestPath = 'html/assets/manifest.js';
const librarySandbox = { window: {} };
vm.createContext(librarySandbox);
vm.runInContext(fs.readFileSync(manifestPath, 'utf8'), librarySandbox);
const library = librarySandbox.window.LOGO_LIBRARY;

assert.ok(Array.isArray(library), 'manifest exposes an array');
const bySet = library.reduce((acc, item) => ({ ...acc, [item.set]: (acc[item.set] || 0) + 1 }), {});
assert.deepEqual(bySet, { legacy: 5, kotak: 171, rasio: 171 }, 'set composition');
assert.equal(library.length, 347, 'total library size');
assert.equal(new Set(library.map((item) => item.id)).size, library.length, 'unique ids');
assert.equal(new Set(library.map((item) => item.label)).size, library.length, 'unique labels');

for (const item of library) {
  assert.match(item.src, /^assets\/logos\/[a-z0-9-]+\.webp$/, `src pattern: ${item.src}`);
  assert.match(item.thumb, /^assets\/thumbs\/[a-z0-9-]+\.webp$/, `thumb pattern: ${item.thumb}`);
  const full = path.join('html', item.src);
  const thumb = path.join('html', item.thumb);
  assert.ok(fs.existsSync(full), `missing ${full}`);
  assert.ok(fs.existsSync(thumb), `missing ${thumb}`);
  assert.deepEqual(webpSize(fs.readFileSync(full)), { w: item.w, h: item.h }, `full size ${item.id}`);
  const thumbSize = webpSize(fs.readFileSync(thumb));
  assert.ok(thumbSize.w <= 160 && thumbSize.h <= 160, `thumb bounds ${item.id}`);
}

const logoFiles = fs.readdirSync('html/assets/logos').filter((name) => name.endsWith('.webp'));
const thumbFiles = fs.readdirSync('html/assets/thumbs').filter((name) => name.endsWith('.webp'));
assert.equal(logoFiles.length, library.length, 'no orphan full images');
assert.equal(thumbFiles.length, library.length, 'no orphan thumbnails');

const totalBytes = library.reduce((sum, item) => sum + fs.statSync(path.join('html', item.src)).size + fs.statSync(path.join('html', item.thumb)).size, 0);
assert.ok(totalBytes < 5 * 1024 * 1024, `asset budget, got ${(totalBytes / 1048576).toFixed(2)} MB`);
console.log(`PASS: manifest ${library.length} item (${bySet.legacy}/${bySet.kotak}/${bySet.rasio}), WebP sizes match, assets ${(totalBytes / 1048576).toFixed(2)} MB`);
