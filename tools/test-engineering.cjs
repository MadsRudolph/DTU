const {test}=require('node:test');const assert=require('node:assert/strict');const fs=require('node:fs');const vm=require('node:vm');const {createRequire}=require('node:module');const path=require('node:path');
const dir=path.resolve('Obsidian/.obsidian/plugins/hypersketch');const G=require(path.join(dir,'geometry'));const C=require(path.join(dir,'connections'));
const stroke={color:'#f3f4f6',isAdaptive:true,width:3,dash:'dashed',points:[[0,0],[100,100]]};
test('shapes, symbols, dashes and labels export validated portable SVG',()=>{
 for(const kind of ['line','rectangle','ellipse','arrow']){const paths=G.shape(kind,[0,0],[100,60]);const s={...stroke,points:paths[0],paths};assert.match(G.svg([s]).svg,/stroke-dasharray="15 9"/);G.shift(s,10,20);assert(G.bounds([s]).x>=8.5);}
 for(const kind of ['resistor','capacitor','ground','opamp']){const paths=G.symbol(kind,[100,100]);assert.match(G.svg([{...stroke,points:paths[0],paths}]).svg,/<path/);}
 assert(!G.svg([stroke]).svg.includes('<rect'), 'SVG export must have no background rectangle');
 assert.match(G.svg([{...stroke,text:'<R & L>'}]).svg,/&lt;R &amp; L&gt;/);
 assert.throws(()=>G.svg([{...stroke,color:'red" onload="evil'}]));assert.throws(()=>G.svg([{...stroke,points:[[Infinity,0]]}]));
});
test('network detection distinguishes Tailscale CGNAT range, LAN and machine choice',()=>{
 const n={wifi:[{family:'IPv4',address:'192.168.1.9'}],vpn:[{family:'IPv4',address:'100.100.2.3'}],public:[{family:'IPv4',address:'100.1.2.3'}]};
 assert.equal(C.addresses(n).length,2);assert.match(C.link({connectionMode:'tailscale',port:27123},'token',n).url,/100.100.2.3/);assert.match(C.link({connectionMode:'lan',port:27123},'token',n).url,/192.168.1.9/);assert.match(C.qrData('http://192.168.1.9:27123/#token'),/^data:image\/svg\+xml;base64,/);
});
class MarkdownView{}
const obsidian={Plugin:class{},MarkdownView,Modal:class{},PluginSettingTab:class{},Notice:class{},normalizePath:s=>s.replace(/\\/g,'/')};
const mockModule={exports:{}};const nativeRequire=createRequire(path.join(dir,'main.js'));
vm.runInNewContext(fs.readFileSync(path.join(dir,'main.js'),'utf8'),{module:mockModule,require:n=>n==='obsidian'?obsidian:nativeRequire(n),Buffer,URL,console});
function fixture(){const files=new Map(),views=['A.md','B.md'].map(name=>{const v=new MarkdownView();v.file={path:name,basename:name};v.content='Notes\n';v.editor={getValue:()=>v.content,getCursor:()=>({line:0,ch:0}),replaceRange:s=>{v.content+=s;},setCursor(){}};v.getMode=()=> 'source';return v;});let active=views[0];const p=new mockModule.exports();p.settings={port:0,assetFolder:'assets/sketches',token:'test-secret'};p.receipts={};p.queue=Promise.resolve();p.saveData=async()=>{};p.status={setText(){}};p.app={workspace:{getLeavesOfType:()=>views.map(view=>({view})),getActiveViewOfType:()=>active},vault:{getName:()=> 'DTU',getAbstractFileByPath:n=>files.has(n)?{path:n}:null,createFolder:async n=>files.set(n,''),create:async(n,s)=>{assert(!files.has(n));files.set(n,s);},read:async f=>files.get(f.path)}};return {p,files,views,setActive:v=>active=v};}
test('plugin inserts into arbitrary open notes, pins requested target, retries once',async()=>{const {p,files,views,setActive}=fixture();setActive(views[1]);const d={sketchId:'abc123456789000000',notePath:'A.md',strokes:[stroke]};await p.saveAndInjectSketch(d);await p.saveAndInjectSketch(d);assert.equal(views[0].content.split('![[').length-1,1);assert.equal(views[1].content,'Notes\n');assert.equal([...files.keys()].filter(x=>x.endsWith('.svg')).length,1);await p.saveAndInjectSketch({...d,sketchId:'abc123456789000001',notePath:'B.md'});assert.match(views[1].content,/!\[\[/);await assert.rejects(p.saveAndInjectSketch({...d,strokes:[{...stroke,width:5}]}),/already used/);});
test('plugin HTTP serves PWA and requires paired model submissions',async t=>{const {p,views}=fixture();p.startServer();await new Promise(r=>p.server.once('listening',r));t.after(()=>p.onunload());const base='http://127.0.0.1:'+p.server.address().port;
 assert.equal((await fetch(base+'/api/status')).status,401);const manifest=await(await fetch(base+'/manifest.webmanifest')).json();assert.equal(manifest.display,'standalone');
 const headers={Authorization:'Bearer test-secret','Content-Type':'application/json'};const res=await fetch(base+'/api/inject',{method:'POST',headers,body:JSON.stringify({sketchId:'http1234567890000',notePath:'A.md',strokes:[stroke]})});assert.equal(res.status,200);assert.match(views[0].content,/!\[\[/);
 assert.equal((await fetch(base+'/api/inject',{method:'POST',headers,body:JSON.stringify({svgData:'<svg/>'})})).status,400);
});
