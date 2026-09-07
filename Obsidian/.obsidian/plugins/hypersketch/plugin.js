const obsidian=require('obsidian');
const http=require('node:http');
const crypto=require('node:crypto');
const G=require('./geometry');
const connection=require('./connections');
const servePwa=require('./pwa');
const getPWAHtml=require('./pad');
const DEFAULTS={port:27123,assetFolder:'assets/sketches',embedWidth:'',autoAdvanceCursor:true,connectionMode:'tailscale',httpsUrl:'',lanAddress:''};
class HyperSketchPlugin extends obsidian.Plugin {
 async onload(){
  const saved=await this.loadData()||{};this.settings={...DEFAULTS,...saved};
  this.settings.token ||= crypto.randomBytes(24).toString('hex');
  this.receipts=this.settings.receipts||{};this.queue=Promise.resolve();this.lastMarkdownView=null;
  await this.saveSettings();
  this.registerEvent(this.app.workspace.on('active-leaf-change',leaf=>{if(leaf?.view instanceof obsidian.MarkdownView)this.lastMarkdownView=leaf.view;}));
  this.addRibbonIcon('pencil','HyperSketch: Connect tablet',()=>new ConnectionModal(this.app,this).open());
  this.addCommand({id:'show-hypersketch-info',name:'Connect tablet (QR code)',callback:()=>new ConnectionModal(this.app,this).open()});
  this.addSettingTab(new HyperSketchSettings(this.app,this));
  this.status=this.addStatusBarItem();this.status.onclick=()=>new ConnectionModal(this.app,this).open();
  this.startServer();
 }
 async saveSettings(){this.settings.receipts=this.receipts||{};await this.saveData(this.settings);}
 getTargetMarkdownView(notePath){
  const views=this.app.workspace.getLeavesOfType('markdown').map(l=>l.view).filter(v=>v instanceof obsidian.MarkdownView&&v.file);
  if(notePath)return views.find(v=>v.file.path===notePath)||null;
  const active=this.app.workspace.getActiveViewOfType(obsidian.MarkdownView);
  return active?.file?active:views.includes(this.lastMarkdownView)?this.lastMarkdownView:null;
 }
 startServer(){
  this.server=http.createServer(async(req,res)=>{
   const reply=(code,data)=>{if(res.writableEnded)return;res.writeHead(code,{'Content-Type':'application/json','Cache-Control':'no-store'});res.end(JSON.stringify(data));};
   try{
    const url=new URL(req.url,'http://127.0.0.1');
    if(servePwa(req,res,url.pathname))return;
    if(req.method==='GET'&&['/','/pad'].includes(url.pathname)){res.writeHead(200,{'Content-Type':'text/html; charset=utf-8','Cache-Control':'no-store','X-HyperSketch-Ink':'engineering-v1'});res.end(getPWAHtml(this.settings.port));return;}
    if(req.headers.authorization!==`Bearer ${this.settings.token}`){reply(401,{error:'Scan the QR code in Obsidian → HyperSketch settings to pair this tablet.'});return;}
    if(req.method==='GET'&&url.pathname==='/api/status'){
     const view=this.getTargetMarkdownView();reply(200,{status:'ok',activeNote:view?.file.basename||null,notePath:view?.file.path||null,vault:this.app.vault.getName()});return;
    }
    if(req.method==='POST'&&url.pathname==='/api/inject'){
     let body='',size=0;for await(const chunk of req){size+=chunk.length;if(size>4*1024*1024){reply(413,{error:'Sketch exceeds 4 MB'});return;}body+=chunk;}
     const data=JSON.parse(body);
     const work=this.queue.then(()=>this.saveAndInjectSketch(data));this.queue=work.catch(()=>{});
     reply(200,{status:'ok',...await work});return;
    }
    reply(404,{error:'Not found'});
   }catch(err){reply(400,{error:err.message});}
  });
  this.server.on('error',e=>{this.serverError=e.message;this.status.setText('HyperSketch: connection error');new obsidian.Notice(`HyperSketch: ${e.code==='EADDRINUSE'?'Port is already used. Stop the standalone demo or select a different port in settings.':e.message}`,8000);});
  this.server.listen(this.settings.port,'0.0.0.0',()=>{this.serverError=null;this.status.setText('HyperSketch :'+this.settings.port);});
 }
 async restartServer(){if(this.server){this.server.closeAllConnections?.();await new Promise(r=>this.server.close(r));}this.startServer();}
 async saveAndInjectSketch(data){
  if(!/^[a-zA-Z0-9-]{16,80}$/.test(data.sketchId||''))throw Error('Invalid sketch ID');
  const model=G.validate(data.strokes),exported=G.svg(model);
  const hash=crypto.createHash('sha256').update(JSON.stringify(model)).digest('hex');
  const receipt=this.receipts[data.sketchId];if(receipt){if(receipt.hash!==hash)throw Error('Sketch ID already used');return receipt;}
  const target=this.getTargetMarkdownView(data.notePath);
  if(!target?.editor||target.getMode?.()==='preview')throw Error('Open the destination Markdown note in editing mode, then retry.');
  const file=target.file;const folder=obsidian.normalizePath(this.settings.assetFolder||'assets/sketches');
  if(folder.startsWith('/')||folder.split('/').some(x=>x==='..'||x.startsWith('.')))throw Error('Attachment folder must be a normal path inside the vault');
  let cur='';for(const part of folder.split('/')){cur=cur?cur+'/'+part:part;if(!this.app.vault.getAbstractFileByPath(cur))await this.app.vault.createFolder(cur);}
  const svgPath=`${folder}/sketch-${data.sketchId}.svg`,sourcePath=`${folder}/sketch-${data.sketchId}.hypersketch.json`;
  const prior=this.app.vault.getAbstractFileByPath(svgPath);
  if(prior&&await this.app.vault.read(prior)!==exported.svg)throw Error('Sketch ID collision');
  if(!this.app.vault.getAbstractFileByPath(sourcePath))await this.app.vault.create(sourcePath,JSON.stringify({version:1,strokes:model}));
  if(!prior)await this.app.vault.create(svgPath,exported.svg);
  if(target.file?.path!==file.path)throw Error('Destination changed while saving. Open the intended note and retry.');
  const editor=target.editor;
  if(!editor.getValue().includes(`![[${svgPath}`)){
   const width=/^\d{1,4}$/.test(this.settings.embedWidth)?`|${this.settings.embedWidth}`:'';
   const cursor=editor.getCursor(),embed=`\n\n![[${svgPath}${width}]]\n\n`;
   editor.replaceRange(embed,cursor);
   if(this.settings.autoAdvanceCursor)editor.setCursor({line:cursor.line+4,ch:0});
  }
  const result={file:svgPath,injected:true,note:file.basename,hash};this.receipts[data.sketchId]=result;
  const keys=Object.keys(this.receipts);for(const k of keys.slice(0,Math.max(0,keys.length-1000)))delete this.receipts[k];
  await this.saveSettings();new obsidian.Notice('HyperSketch inserted into '+file.basename);return result;
 }
 onunload(){this.server?.closeAllConnections?.();this.server?.close();}
}
function renderConnection(container,plugin){
 container.empty();
 if(plugin.serverError)container.createEl('p',{text:'Server error: '+plugin.serverError});
 let result;try{result=connection.link(plugin.settings,plugin.settings.token);}catch(e){container.createEl('p',{text:e.message});return;}
 if(!result.url){container.createEl('p',{text:result.message});return;}
 container.createEl('img',{attr:{src:connection.qrData(result.url),width:'240',height:'240',alt:'Scan to pair HyperSketch on your tablet',style:'display:block;background:white;border-radius:8px;'}});
 container.createEl('p',{text:'Scan with the tablet camera. Open any Markdown note in editing mode on this PC, then tap Insert on the tablet.'});
 const row=container.createDiv();row.createEl('a',{text:result.url.split('#')[0],href:result.url});
 row.createEl('button',{text:'Copy pairing URL'}).onclick=()=>navigator.clipboard.writeText(result.url);
 if(plugin.settings.connectionMode==='usb')container.createEl('pre',{text:`adb reverse tcp:${plugin.settings.port} tcp:${plugin.settings.port}`});
 else container.createEl('p',{text:plugin.settings.connectionMode==='tailscale'?'Keep Tailscale connected on both devices.':'Use the same private Wi-Fi/LAN. Isolated campus Wi-Fi needs Tailscale.'});
 container.createEl('small',{text:result.url.startsWith('https:')?'HTTPS enabled: Chrome can install this as an app.':'Browser drawing works over HTTP. PWA installation needs an HTTPS address; configure Tailscale Serve on this PC if desired.'});
}
class ConnectionModal extends obsidian.Modal{
 constructor(app,plugin){super(app);this.plugin=plugin;}
 onOpen(){this.contentEl.createEl('h2',{text:'HyperSketch · Connect tablet'});const box=this.contentEl.createDiv();renderConnection(box,this.plugin);}
 onClose(){this.contentEl.empty();}
}
class HyperSketchSettings extends obsidian.PluginSettingTab{
 constructor(app,plugin){super(app,plugin);this.plugin=plugin;}
 display(){const el=this.containerEl,p=this.plugin;el.empty();el.createEl('h2',{text:'HyperSketch · Tablet connection'});
 new obsidian.Setting(el).setName('Connection').setDesc('Addresses are detected on this PC; connection settings are not synced by Git.').addDropdown(d=>d.addOption('tailscale','Tailscale').addOption('lan','Local Wi-Fi / LAN').addOption('usb','USB').setValue(p.settings.connectionMode).onChange(async v=>{p.settings.connectionMode=v;await p.saveSettings();this.display();}));
 if(p.settings.connectionMode==='lan'){const items=connection.addresses().filter(a=>a.mode==='lan');new obsidian.Setting(el).setName('Network interface').addDropdown(d=>{d.addOption('','Automatic');for(const a of items)d.addOption(a.address,`${a.name}: ${a.address}`);d.setValue(p.settings.lanAddress).onChange(async v=>{p.settings.lanAddress=v;await p.saveSettings();this.display();});});}
 const box=el.createDiv();renderConnection(box,p);
 new obsidian.Setting(el).setName('Refresh addresses / QR').addButton(b=>b.setButtonText('Refresh').onClick(()=>this.display()));
 new obsidian.Setting(el).setName('Tailscale HTTPS URL (optional)').setDesc('This PC’s Tailscale Serve address, e.g. https://laptop.your-tailnet.ts.net. Leave blank for automatic Tailscale IP.').addText(t=>t.setValue(p.settings.httpsUrl).onChange(async v=>{p.settings.httpsUrl=v.trim();await p.saveSettings();renderConnection(box,p);}));
 el.createEl('p',{text:`For PWA installation, run on this PC: tailscale serve --bg http://127.0.0.1:${p.settings.port}, then paste its HTTPS URL above.`});
 new obsidian.Setting(el).setName('Server port').setDesc('Apply restarts this plugin server.').addText(t=>t.setValue(String(p.settings.port)).onChange(v=>{const n=Number(v);if(Number.isInteger(n)&&n>=1024&&n<=65535)p.settings.port=n;})).addButton(b=>b.setButtonText('Apply').onClick(async()=>{await p.saveSettings();await p.restartServer();this.display();}));
 new obsidian.Setting(el).setName('Attachment folder').setDesc('Relative to this vault. SVG previews and editable source files are both saved.').addText(t=>t.setValue(p.settings.assetFolder).onChange(async v=>{p.settings.assetFolder=v.trim()||DEFAULTS.assetFolder;await p.saveSettings();}));
 new obsidian.Setting(el).setName('Embed width').setDesc('Optional width in pixels.').addText(t=>t.setValue(p.settings.embedWidth).onChange(async v=>{p.settings.embedWidth=v.trim();await p.saveSettings();}));
 new obsidian.Setting(el).setName('Move cursor after insertion').addToggle(t=>t.setValue(p.settings.autoAdvanceCursor).onChange(async v=>{p.settings.autoAdvanceCursor=v;await p.saveSettings();}));
 new obsidian.Setting(el).setName('Reset tablet pairing').setDesc('Invalidates this PC’s old pairing URLs.').addButton(b=>b.setButtonText('New QR key').onClick(async()=>{p.settings.token=crypto.randomBytes(24).toString('hex');await p.saveSettings();this.display();}));
 }
}
module.exports=HyperSketchPlugin;
