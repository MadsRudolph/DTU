const icons=require('./icons-base64');
const manifest = {
  id:'/',name:'HyperSketch',short_name:'HyperSketch',description:'S-Pen sketches delivered to Obsidian.',
  start_url:'/',scope:'/',display:'standalone',background_color:'#121214',theme_color:'#121214',
  icons:[192,512].map(size=>({src:`/icon-${size}.png`,sizes:`${size}x${size}`,type:'image/png',purpose:'any maskable'}))
};
const sw = `
const CACHE='hypersketch-shell-v2';
const FILES=['/','/manifest.webmanifest','/icon-192.png','/icon-512.png'];
self.addEventListener('install',e=>e.waitUntil(caches.open(CACHE).then(c=>c.addAll(FILES))));
// Do not force-reload an open drawing to activate an update.
self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k.startsWith('hypersketch-shell-')&&k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',e=>{
 const url=new URL(e.request.url);
 if(e.request.method!=='GET'||url.origin!==self.location.origin||url.pathname.startsWith('/api/'))return;
 if(e.request.mode==='navigate'){
   e.respondWith(fetch(e.request).then(response=>{
     if(response.ok){const copy=response.clone();e.waitUntil(caches.open(CACHE).then(c=>c.put('/',copy)));}
     return response;
   }).catch(()=>caches.match('/')));return;
 }
 if(FILES.includes(url.pathname))e.respondWith(caches.match(e.request).then(cached=>cached||fetch(e.request)));
});`;
module.exports=function servePwa(req,res,pathname){
 if(req.method!=='GET')return false;
 let body,type;
 if(pathname==='/manifest.webmanifest'){body=JSON.stringify(manifest);type='application/manifest+json';}
 else if(pathname==='/sw.js'){body=sw;type='text/javascript';res.setHeader('Service-Worker-Allowed','/');}
 else if(['/icon-192.png','/icon-512.png'].includes(pathname)){body=Buffer.from(icons[pathname.slice(1)],'base64');type='image/png';}
 else return false;
 res.writeHead(200,{'Content-Type':type,'Cache-Control':'no-cache','X-Content-Type-Options':'nosniff'});res.end(body);return true;
};
