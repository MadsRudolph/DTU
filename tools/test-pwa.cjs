const {spawn}=require('node:child_process');const fs=require('node:fs');const os=require('node:os');const path=require('node:path');const assert=require('node:assert/strict');
const base=(process.env.HYPERSKETCH_TEST_URL||'http://127.0.0.1:27123').replace(/\/$/,'');
(async()=>{
const child=spawn('chromium',['--headless','--no-sandbox','--disable-dev-shm-usage','--remote-debugging-port=0','--user-data-dir='+fs.mkdtempSync(path.join(os.tmpdir(),'hypersketch-pwa-test-')),'about:blank']);
let socket;
try{
const endpoint=await new Promise((resolve,reject)=>{let output='';child.stderr.on('data',d=>{output+=d;const m=output.match(/DevTools listening on (ws:\/\/[^\s]+)/);if(m)resolve(m[1]);});child.on('error',reject);});
socket=new WebSocket(endpoint);await new Promise(r=>socket.onopen=r);
let id=0;const pending=new Map();socket.onmessage=e=>{const m=JSON.parse(e.data);if(m.id){const p=pending.get(m.id);pending.delete(m.id);m.error?p.reject(Error(JSON.stringify(m.error))):p.resolve(m.result);}};
const send=(method,params={},sessionId)=>new Promise((resolve,reject)=>{const n=++id;pending.set(n,{resolve,reject});socket.send(JSON.stringify({id:n,method,params,sessionId}));});
const {targetId}=await send('Target.createTarget',{url:'about:blank'});const {sessionId}=await send('Target.attachToTarget',{targetId,flatten:true});
const call=(m,p)=>send(m,p,sessionId);const evaluate=async expression=>{const r=await call('Runtime.evaluate',{expression,awaitPromise:true,returnByValue:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result.value;};
await call('Page.enable');await call('Network.enable');await call('Page.navigate',{url:base+'/'});
await new Promise(r=>setTimeout(r,700));
const setup=await evaluate(`(async()=>{await navigator.serviceWorker.ready;const m=await (await fetch('/manifest.webmanifest')).json();localStorage.setItem('pwa-test','retained');return {secure:isSecureContext,display:m.display,cached:!!(await caches.match('/')),icons:m.icons.length};})()`);
assert.equal(setup.secure,true);assert.equal(setup.display,'standalone');assert.equal(setup.cached,true);assert.equal(setup.icons,2);
await call('Network.emulateNetworkConditions',{offline:true,latency:0,downloadThroughput:0,uploadThroughput:0});
await call('Page.navigate',{url:base+'/?offline-test=1'});await new Promise(r=>setTimeout(r,700));
const offline=await evaluate(`({url:location.search,pad:!!document.getElementById('pad'),stored:localStorage.getItem('pwa-test'),height:document.documentElement.scrollHeight,viewport:innerHeight})`);
assert.equal(offline.url,'?offline-test=1');assert.equal(offline.pad,true);assert.equal(offline.stored,'retained');assert(offline.height<=offline.viewport);
console.log('PASS: HTTPS secure context, standalone manifest, icons, cached app shell, offline navigation, local storage and viewport fit.');
}finally{socket?.close();child.kill();}
})().catch(e=>{console.error(e);process.exitCode=1;});
