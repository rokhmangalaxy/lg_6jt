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
assert.equal((html.match(/data:image\/png;base64,/g)||[]).length,10);
assert(!html.includes('src="assets/'));
assert.equal(html,fs.readFileSync('preview-logo-mcm.html','utf8'));
console.log('PASS: JS syntax, simultaneous swap, source immutability, reset, custom palette, 10 embedded sources, offline parity');

const presets=JSON.parse(script.match(/const presets=(\[[\s\S]*?\]);/)[1].replace(/(name|colors|background):/g,'"$1":').replace(/'/g,'"'));
assert.equal(presets.length,4);
assert.deepEqual(presets[0].colors,['#dc2626','#173257','#ffffff']);
assert.deepEqual(presets[1].colors,['#173257','#dc2626','#ffffff']);
assert.equal(presets[2].background,'#d1d5db');
assert.equal(presets[3].background,'#d1d5db');
assert(!html.includes('type="color"'));

// 5x5 image: white exterior, closed red 3x3 ring, white center.
const fixture={width:5,height:5,data:new Uint8ClampedArray(100).fill(255)};
for(let y=1;y<4;y++)for(let x=1;x<4;x++)if(x!==2||y!==2){const p=(y*5+x)*4;fixture.data.set([220,38,38,255],p)}
const bg=sandbox.backgroundMask(fixture);
assert.equal(Array.from(bg).reduce((a,b)=>a+b,0),16);
assert.equal(bg[12],0,'enclosed white is not background');
for(const preset of presets){
 const palette=[...preset.colors,preset.background];
 const background=preset.background.slice(1).match(/../g).map(h=>parseInt(h,16));
 const output=sandbox.recolor(fixture,palette).data;
 for(let p=0;p<25;p++)if(bg[p])assert.deepEqual(Array.from(output.slice(p*4,p*4+4)),[...background,255]);
 const whiteColor=palette[2].slice(1).match(/../g).map(h=>parseInt(h,16));
 assert.deepEqual(Array.from(output.slice(48,51)),whiteColor);
}
console.log('PASS: 4 presets, fixed white/gray exterior, enclosed white remains editable');

// Closed white counters in the nameplate must use the actual background.
fixture.textRegion=[0,0,1,1];delete fixture.backgroundMask;
for(const preset of presets){
 const out=sandbox.recolor(fixture,[...preset.colors,preset.background]).data;
 const bg=preset.background.slice(1).match(/../g).map(h=>parseInt(h,16));
 assert.deepEqual(Array.from(out.slice(48,51)),bg);
}
const swipe=script.match(/function swipeDirection\(dx,dy,elapsed\)\{[\s\S]*?\n\}/)[0];
vm.runInContext(`${swipe};this.swipeDirection=swipeDirection;`,sandbox);
assert.equal(sandbox.swipeDirection(-100,5,200),1);
assert.equal(sandbox.swipeDirection(100,5,200),-1);
assert.equal(sandbox.swipeDirection(20,0,200),0);
assert.equal(sandbox.swipeDirection(60,100,200),0);
assert.equal(sandbox.swipeDirection(100,0,1500),0);
console.log('PASS: nameplate counters match background, swipe thresholds and direction');
