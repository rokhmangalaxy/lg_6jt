// Run: node tests/test_logo_preview.cjs
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const html=fs.readFileSync('html/index.html','utf8');
const script=html.match(/<script>([\s\S]*?)<\/script>/)[1];
new vm.Script(script); // Check complete application syntax.
const funcs=script.match(/function recolor\(original,palette\)\{[\s\S]*?\n\}/)[0];
const sandbox={Uint8ClampedArray,ImageData:class {constructor(data,width,height){Object.assign(this,{data,width,height})}}};
vm.createContext(sandbox);
vm.runInContext(`const rgb=hex=>[1,3,5].map(n=>parseInt(hex.slice(n,n+2),16));${funcs};this.recolor=recolor;`,sandbox);
const src={width:3,height:1,data:new Uint8ClampedArray([220,38,38,255,23,50,87,255,255,255,255,255])};
const original=Array.from(src.data);
assert.deepEqual(Array.from(sandbox.recolor(src,['#173257','#dc2626','#ffffff']).data),[23,50,87,255,220,38,38,255,255,255,255,255]);
assert.deepEqual(Array.from(src.data),original,'original pixels unchanged');
assert.deepEqual(Array.from(sandbox.recolor(src,['#dc2626','#173257','#ffffff']).data),original,'reset restores original');
assert.deepEqual(Array.from(sandbox.recolor(src,['#000000','#000000','#000000']).data),[0,0,0,255,0,0,0,255,0,0,0,255]);
assert.equal((html.match(/data:image\/png;base64,/g)||[]).length,5);
assert(!html.includes('src="assets/'));
assert.equal(html,fs.readFileSync('preview-logo-mcm.html','utf8'));
console.log('PASS: JS syntax, simultaneous swap, source immutability, reset, custom palette, 5 embedded sources, offline parity');

const match=script.match(/const arrangements=(\[[\s\S]*?\]);/);
const arrangements=JSON.parse(match[1]);
assert.equal(arrangements.length,6);
assert.equal(new Set(arrangements.map(a=>a.join(','))).size,6);
arrangements.forEach(a=>assert.deepEqual([...a].sort(),[0,1,2]));
assert(!html.includes('type="color"'));
console.log('PASS: 6 unique base-palette permutations; no custom color controls');
