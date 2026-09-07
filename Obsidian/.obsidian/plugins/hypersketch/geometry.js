// Shared pure geometry: tablet drawing and server-side validated SVG export.
(function(root){
const colors=['#f3f4f6','#ff5555','#50b5ff','#50fa7b','#f1fa8c','#172033'];
function paths(s){return s.paths||[s.points];}
function validate(model){
 if(!Array.isArray(model)||model.length>3000)throw Error('Invalid sketch');let count=0;
 for(const s of model){if(!s||!colors.includes(s.color)||!Number.isFinite(s.width)||s.width<1||s.width>30||!['solid','dashed','dotted',undefined].includes(s.dash))throw Error('Invalid brush');
 const lines=paths(s);if(!Array.isArray(lines)||lines.length>100)throw Error('Invalid paths');
 for(const line of lines){if(!Array.isArray(line)||!line.length)throw Error('Empty path');for(const p of line)if(++count>150000||!Array.isArray(p)||p.length!==2||!p.every(n=>Number.isFinite(n)&&Math.abs(n)<100000))throw Error('Invalid coordinates');}
 if(s.rotation!==undefined&&(!Number.isFinite(s.rotation)||Math.abs(s.rotation)>360))throw Error('Invalid rotation');
 if(s.text!==undefined&&(typeof s.text!=='string'||s.text.length>300))throw Error('Invalid label');
 }return model;
}
function distance(p,a,b){const dx=b[0]-a[0],dy=b[1]-a[1],d=dx*dx+dy*dy;const t=d?Math.max(0,Math.min(1,((p[0]-a[0])*dx+(p[1]-a[1])*dy)/d)):0;return Math.hypot(p[0]-a[0]-t*dx,p[1]-a[1]-t*dy);}
function turn(p,c,degrees){const t=degrees*Math.PI/180,co=Math.cos(t),si=Math.sin(t),x=p[0]-c[0],y=p[1]-c[1];return [c[0]+x*co-y*si,c[1]+x*si+y*co];}
function textCorners(s){const a=s.points[0];return [[a[0]-2,a[1]-28],[a[0]+s.text.length*18+2,a[1]-28],[a[0]+s.text.length*18+2,a[1]+8],[a[0]-2,a[1]+8]].map(p=>turn(p,a,s.rotation||0));}
function hit(s,p,r=12){if(s.text){const a=s.points[0],q=turn(p,a,-(s.rotation||0));return q[0]>=a[0]-r&&q[0]<=a[0]+s.text.length*18+r&&q[1]>=a[1]-28-r&&q[1]<=a[1]+8+r;}return paths(s).some(line=>line.some((a,i)=>distance(p,a,line[Math.min(i+1,line.length-1)])<r+s.width/2));}
function transformPoints(s,fn){const seen=new Set();for(const line of paths(s))for(const p of line){if(seen.has(p))continue;seen.add(p);const q=fn(p);p[0]=q[0];p[1]=q[1];}}
function shift(s,dx,dy){transformPoints(s,p=>[p[0]+dx,p[1]+dy]);}
function rotate(s,degrees){if(!Number.isFinite(degrees))throw Error('Invalid rotation');const b=bounds([s]),c=[b.x+b.width/2,b.y+b.height/2];transformPoints(s,p=>turn(p,c,degrees));if(s.text)s.rotation=((s.rotation||0)+degrees)%360;}
function shape(kind,a,b){const [x,y]=a,[u,v]=b,dx=u-x,dy=v-y;
 if(kind==='rectangle')return [[a,[u,y],b,[x,v],a]];
 if(kind==='ellipse')return [Array.from({length:65},(_,i)=>[x+dx/2+Math.cos(i*Math.PI/32)*dx/2,y+dy/2+Math.sin(i*Math.PI/32)*dy/2])];
 if(kind==='arrow'){const t=Math.atan2(dy,dx),n=Math.min(24,Math.hypot(dx,dy)/3);return [[a,b],[[u-n*Math.cos(t-.5),v-n*Math.sin(t-.5)],b,[u-n*Math.cos(t+.5),v-n*Math.sin(t+.5)]]];}
 return [[a,b]];
}
function symbol(kind,p){const [x,y]=p;let lines;
 if(kind==='resistor')lines=[[[0,0],[22,0],[29,-12],[43,12],[57,-12],[71,12],[85,-12],[92,0],[114,0]]];
 else if(kind==='capacitor')lines=[[[0,0],[45,0]],[[45,-24],[45,24]],[[60,-24],[60,24]],[[60,0],[105,0]]];
 else if(kind==='ground')lines=[[[0,-40],[0,0]],[[-30,0],[30,0]],[[-20,10],[20,10]],[[-10,20],[10,20]]];
 else lines=[[[-45,-40],[-45,40],[45,0],[-45,-40]],[[-75,-20],[-45,-20]],[[-75,20],[-45,20]],[[45,0],[75,0]],[[-36,-20],[-24,-20]],[[-36,20],[-24,20]],[[-30,14],[-30,26]]];
 return lines.map(line=>line.map(([u,v])=>[u+x,v+y]));
}
function dash(s){return s.dash==='dashed'?[s.width*5,s.width*3]:s.dash==='dotted'?[.01,s.width*3]:[];}
function bounds(model){let x=Infinity,y=Infinity,u=-Infinity,v=-Infinity;for(const s of model){const lines=s.text?[textCorners(s)]:paths(s);const margin=s.text?0:s.width/2;for(const line of lines)for(const p of line){x=Math.min(x,p[0]-margin);y=Math.min(y,p[1]-margin);u=Math.max(u,p[0]+margin);v=Math.max(v,p[1]+margin);}}return {x,y,width:u-x,height:v-y};}
const escape=s=>s.replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&apos;'}[c]));
function svg(model){validate(model);if(!model.length)throw Error('Draw something first');const b=bounds(model),x=b.x-16,y=b.y-16,w=b.width+32,h=b.height+32;let out=`<svg xmlns="http://www.w3.org/2000/svg" viewBox="${x} ${y} ${w} ${h}" width="${w}" height="${h}">`;
 for(const s of model){const color=s.color;if(s.text){out+=`<text x="${s.points[0][0]}" y="${s.points[0][1]}" fill="${color}" transform="rotate(${s.rotation||0} ${s.points[0][0]} ${s.points[0][1]})" font-size="28" font-family="monospace">${escape(s.text)}</text>`;continue;}
 for(const line of paths(s)){if(line.length===1)out+=`<circle cx="${line[0][0]}" cy="${line[0][1]}" r="${s.width/2}" fill="${color}"/>`;else out+=`<path d="M${line.map(p=>p.join(',')).join(' L')}" fill="none" stroke="${color}" stroke-width="${s.width}" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="${dash(s).join(' ')}"/>`;}}
 return {svg:out+'</svg>',width:w,height:h};}
const api={paths,validate,distance,hit,shift,rotate,shape,symbol,dash,bounds,svg};if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.HyperSketchGeometry=api;
})(typeof window!=='undefined'?window:globalThis);
