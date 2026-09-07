const os=require('node:os');
const QRCode=require('./vendor/QRCode');
const level=require('./vendor/QRCode/QRErrorCorrectLevel');
function addresses(interfaces=os.networkInterfaces()){
 const out=[];for(const [name,items] of Object.entries(interfaces))for(const a of items||[]){if(a.family!=='IPv4'||a.internal)continue;const p=a.address.split('.').map(Number);const tailscale=p[0]===100&&p[1]>=64&&p[1]<=127;const local=p[0]===10||p[0]===192&&p[1]===168||p[0]===172&&p[1]>=16&&p[1]<=31;if(tailscale||local)out.push({name,address:a.address,mode:tailscale?'tailscale':'lan'});}return out;
}
function link(settings,token,interfaces){
 const list=addresses(interfaces);const mode=settings.connectionMode||'tailscale';
 let base;
 if(mode==='usb')base=`http://127.0.0.1:${settings.port}`;
 else if(mode==='tailscale'&&settings.httpsUrl){const u=new URL(settings.httpsUrl);if(u.protocol!=='https:')throw Error('PWA address must use HTTPS');base=u.origin;}
 else {const candidates=list.filter(a=>a.mode===mode);const chosen=candidates.find(a=>a.address===settings.lanAddress)||candidates[0];if(!chosen)return {url:null,list,message:mode==='tailscale'?'Connect Tailscale on this PC, or choose Local Wi-Fi.':'No private LAN address detected. Connect Wi-Fi or Ethernet.'};base=`http://${chosen.address}:${settings.port}`;}
 return {url:base+'/#'+token,list};
}
function qrData(url){const qr=new QRCode(-1,level.M);qr.addData(url);qr.make();const n=qr.getModuleCount();let svg=`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${n+8} ${n+8}"><rect width="100%" height="100%" fill="white"/>`;for(let y=0;y<n;y++)for(let x=0;x<n;x++)if(qr.isDark(y,x))svg+=`<path d="M${x+4} ${y+4}h1v1h-1z"/>`;return 'data:image/svg+xml;base64,'+Buffer.from(svg+'</svg>').toString('base64');}
module.exports={addresses,link,qrData};
