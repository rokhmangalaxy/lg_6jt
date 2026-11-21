// npm install --prefix .cache/logo-trace imagetracerjs pngjs @resvg/resvg-js
// Deterministic contour tracing; no AI redesign and no font substitution.
const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..');
const deps=path.join(root,'.cache/logo-trace/node_modules');
const tracer=require(path.join(deps,'imagetracerjs'));
const {PNG}=require(path.join(deps,'pngjs'));
const {Resvg}=require(path.join(deps,'@resvg/resvg-js'));
const assets=path.join(root,'android-logo/logo-assets');
const out=path.join(root,'04-desain/pilihan-client/vector');fs.mkdirSync(out,{recursive:true});
const palette=[{r:220,g:38,b:38,a:255},{r:23,g:50,b:87,a:255},{r:255,g:255,b:255,a:255},{r:0,g:0,b:0,a:0}];
function commands(p){
 if(!p.segments.length)return [];
 const a=[['M',p.segments[0].x1,p.segments[0].y1]];
 for(const s of p.segments)a.push(s.type==='Q'?['Q',s.x2,s.y2,s.x3,s.y3]:['L',s.x2,s.y2]);
 a.push(['Z']);return a;
}
for(const filename of fs.readdirSync(assets).filter(n=>n.endsWith('.png')).sort()){
 const input=PNG.sync.read(fs.readFileSync(path.join(assets,filename)));
 for(let i=0;i<input.data.length;i+=4)if(input.data[i+3]===0)input.data.fill(0,i,i+4);
 const data=tracer.imagedataToTracedata(input,{ltres:3,qtres:3,pathomit:12,rightangleenhance:true,colorquantcycles:1,layering:0,pal:palette.map(c=>({...c}))});
 const layers=[];
 const area=p=>Math.abs(p.segments.reduce((sum,s)=>sum+s.x1*(s.y3??s.y2)-(s.x3??s.x2)*s.y1,0))/2;
 for(let color=0;color<3;color++){
  if(filename==='client-attachment-01.png' && color===1)continue; // Blue fringe in source is raster noise, not part of this red/white symbol.
  const paths=data.layers[color];
  for(const p of paths){
   if(p.isholepath||!p.segments.length||area(p)<80)continue;
   let cmd=commands(p);
   for(const h of p.holechildren)if(area(paths[h])>=30)cmd=cmd.concat(commands(paths[h]));
   layers.push({color,commands:cmd});
  }
 }
 if(!layers.length)throw Error('Empty trace '+filename);
 const doc={width:input.width,height:input.height,layers};
 const stem=filename.slice(0,-4);
 fs.writeFileSync(path.join(assets,stem+'.json'),JSON.stringify(doc));
 const elements=layers.map(l=>`<path fill="${['#DC2626','#173257','#FFFFFF'][l.color]}" fill-rule="evenodd" d="${l.commands.map(c=>c.join(' ')).join(' ')}"/>`).join('');
 const svg=`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${doc.width} ${doc.height}" width="${doc.width}" height="${doc.height}">${elements}</svg>`;
 fs.writeFileSync(path.join(out,stem+'.svg'),svg);
 const preview=svg.replace('>'+elements,`><rect width="100%" height="100%" fill="#D1D5DB"/>${elements}`);
 const png=new Resvg(preview,{fitTo:{mode:'width',value:1200}}).render().asPng();
 fs.writeFileSync(path.join(out,stem+'-preview.png'),png);
 console.log(stem,layers.length,'vector shapes');
}
