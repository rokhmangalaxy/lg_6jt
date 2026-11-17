// Run: node tests/test_logo_preview.cjs
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const html=fs.readFileSync('html/index.html','utf8');
const script=html.match(/<script>([\s\S]*?)<\/script>/)[1];
new vm.Script(script); // Check complete application syntax.
const maskFunction=script.match(/function backgroundMask\(original\)\{[\s\S]*?\n\}/)[0];
const funcs=script.match(/function recolor\(original,palette\)\{[\s\S]*?\n\}/)[0];
const sandbox={Uint8ClampedArray,Uint8Array,Int32Array,ImageData:class {constructor(data,width,height){Object.assign(this,{data,width,height})}}};
vm.createContext(sandbox);
vm.runInContext(`const rgb=hex=>[1,3,5].map(n=>parseInt(hex.slice(n,n+2),16));${maskFunction};${funcs};this.recolor=recolor;this.backgroundMask=backgroundMask;`,sandbox);
const src={width:3,height:1,data:new Uint8ClampedArray([220,38,38,255,23,50,87,255,255,255,255,255])};
const original=Array.from(src.data);
assert.deepEqual(Array.from(sandbox.recolor(src,['#173257','#dc2626','#ffffff']).data),[23,50,87,255,220,38,38,255,255,255,255,255]);
assert.deepEqual(Array.from(src.data),original,'original pixels unchanged');
assert.deepEqual(Array.from(sandbox.recolor(src,['#dc2626','#173257','#ffffff']).data),original,'reset restores original');
assert.deepEqual(Array.from(sandbox.recolor(src,['#000000','#000000','#000000']).data),[0,0,0,255,0,0,0,255,255,255,255,255]);
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

// 5x5 image: white exterior, closed red 3x3 ring, white center.
const fixture={width:5,height:5,data:new Uint8ClampedArray(100).fill(255)};
for(let y=1;y<4;y++)for(let x=1;x<4;x++)if(x!==2||y!==2){const p=(y*5+x)*4;fixture.data.set([220,38,38,255],p)}
const bg=sandbox.backgroundMask(fixture);
assert.equal(Array.from(bg).reduce((a,b)=>a+b,0),16);
assert.equal(bg[12],0,'enclosed white is not background');
for(const order of arrangements){
 const palette=order.map(i=>['#dc2626','#173257','#ffffff'][i]);
 const output=sandbox.recolor(fixture,palette).data;
 for(let p=0;p<25;p++)if(bg[p])assert.deepEqual(Array.from(output.slice(p*4,p*4+4)),[255,255,255,255]);
 const whiteColor=palette[2].slice(1).match(/../g).map(h=>parseInt(h,16));
 assert.deepEqual(Array.from(output.slice(48,51)),whiteColor);
}
console.log('PASS: exterior white locked across all 6 palettes; enclosed white remains editable');
