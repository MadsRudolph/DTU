function getPWAHtml(port) {
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <meta name="mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="theme-color" content="#121214">
  <title>HyperSketch Pad</title>
  <link rel="manifest" href="/manifest.webmanifest">
  <link rel="icon" href="/icon-192.png">
  <link rel="apple-touch-icon" href="/icon-192.png">
  <style>
    * {
      box-sizing: border-box;
      -webkit-tap-highlight-color: transparent;
      user-select: none;
      -webkit-user-select: none;
    }
    html, body {
      margin: 0;
      padding: 0;
      width: 100vw;
      height: 100vh;
      overflow: hidden;
      background: #121214;
      color: #f3f4f6;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      touch-action: none;
      overscroll-behavior: none;
    }
    canvas {
      position: absolute;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      touch-action: none;
      display: block;
      background: #121214;
      z-index: 1;
    }
    /* Minimal header */
    header {
      position: fixed;
      top: 10px;
      left: 12px;
      right: 12px;
      height: 38px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      z-index: 10;
      pointer-events: none;
    }
    .pill {
      pointer-events: auto;
      background: #1c1f26;
      border: 1px solid #2e3440;
      border-radius: 18px;
      padding: 4px 12px;
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 0.85rem;
    }
    .dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #10b981;
      box-shadow: 0 0 6px #10b981;
    }
    .note-name {
      max-width: 260px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      font-weight: 500;
      color: #e5e7eb;
    }

    /* Floating Toolbar */
    .toolbar-wrap {
      position: fixed;
      bottom: 16px;
      left: 50%;
      transform: translateX(-50%);
      z-index: 10;
      display: flex;
      align-items: center;
      gap: 10px;
      pointer-events: none;
    }
    .toolbar {
      pointer-events: auto;
      background: #1c1f26;
      border: 1px solid #2e3440;
      border-radius: 26px;
      padding: 4px 10px;
      display: flex;
      align-items: center;
      gap: 6px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.6);
    }
    .tool-btn {
      background: transparent;
      border: none;
      outline: none;
      color: #9ca3af;
      width: 36px;
      height: 36px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      font-size: 1.1rem;
    }
    .tool-btn.active {
      color: #ffffff;
      background: #2e3440;
    }
    .divider {
      width: 1px;
      height: 20px;
      background: #2e3440;
      margin: 0 2px;
    }

    .color-dot {
      width: 20px;
      height: 20px;
      border-radius: 50%;
      border: 2px solid transparent;
      cursor: pointer;
    }
    .color-dot.active {
      border-color: #ffffff;
      transform: scale(1.2);
    }

    .insert-btn {
      pointer-events: auto;
      background: #2563eb;
      color: white;
      border: none;
      border-radius: 26px;
      padding: 0 20px;
      height: 46px;
      font-weight: 700;
      font-size: 0.95rem;
      display: flex;
      align-items: center;
      gap: 8px;
      cursor: pointer;
      box-shadow: 0 4px 16px rgba(37, 99, 235, 0.4);
    }
    .insert-btn:active { transform: scale(0.96); }
    .insert-btn.sending {
      opacity: 0.6;
      pointer-events: none;
    }

    #toast {
      position: fixed;
      top: 56px;
      left: 50%;
      transform: translateX(-50%) translateY(-10px);
      background: #10b981;
      color: #ffffff;
      padding: 6px 16px;
      border-radius: 16px;
      font-weight: 600;
      font-size: 0.85rem;
      opacity: 0;
      pointer-events: none;
      transition: all 0.2s ease;
      z-index: 100;
    }
    #toast.show {
      opacity: 1;
      transform: translateX(-50%) translateY(0);
    }
    #toast.err { background: #ef4444; }

    .engineering-select {background:#1c1f26;color:#e5e7eb;border:1px solid #3b4354;border-radius:8px;height:32px;max-width:125px;font-size:12px;}
    [hidden] { display: none !important; }
    /* Keep DOM controls outside the ink rectangle. */
    html { height: 100%; overflow: hidden; }
    body { height: 100dvh; min-height: 0; overflow: hidden; display: flex; flex-direction: column; padding: env(safe-area-inset-top) 2% env(safe-area-inset-bottom); }
    #stage { order: 3; flex: 1 1 0; min-height: 0; min-width: 0; display: flex; align-items: center; justify-content: center; }
    header { order: 1; position: static; grid-row: 1; height: auto; min-height: 54px; padding: 8px 12px; gap: 8px; flex-wrap: wrap; z-index: auto; }
    #surface { order: 3; flex-shrink: 0; width: 100%; max-width: 100%; margin: 0 auto; aspect-ratio: 1400 / 850; position: relative; overflow: hidden; border: 1px solid #2e3440; border-radius: 13px; }
    #pad { background: transparent; position: absolute; inset: 0; width: 100%; height: 100%; z-index: auto; }
    .toolbar-wrap { order: 2; flex-shrink: 0; position: static; grid-row: 3; transform: none; padding: 8px 12px; justify-content: center; flex-wrap: wrap; z-index: auto; }
    .toolbar { flex-wrap: wrap; box-shadow: none; }
    .insert-btn { box-shadow: none; }
    #toast { order: 4; position: static; grid-row: 4; transform: none; height: 28px; flex-shrink: 0; padding: 0; overflow: hidden; transition: none; text-align: center; }
    #toast.show { transform: none; height: 28px; }
  </style>
</head>
<body>
  <!-- Local ink; no network in the pointer path. -->
  <div id="stage"><div id="surface"><canvas id="pad"></canvas></div></div>

  <header>
    <div class="pill">
      <div id="status-dot" class="dot"></div>
      <span style="color: #9ca3af;">Target:</span>
      <span id="active-note-title" class="note-name">Original ink · HyperSketch</span>
    </div>

    <div class="pill">
      <button id="grid-btn" class="tool-btn" style="width: auto; padding: 0 8px; font-size: 0.8rem; border-radius: 10px;" title="Toggle Grid">
        Grid: Dots
      </button>
      <div class="divider"></div>
      <button id="pen-lock-btn" class="tool-btn active" style="width: auto; padding: 0 8px; font-size: 0.8rem; border-radius: 10px;" title="Reject Touch Palm Interference">
        ✍️ Pen Only: ON
      </button>
    </div>
  </header>

  <div class="toolbar-wrap">
    <div class="toolbar">
      <button id="install-btn" class="tool-btn" style="width:auto;padding:0 10px;font-size:.8rem" hidden>Install app</button>
      <!-- Colors -->
      <div class="color-dot active" data-color="adaptive" style="background: #ffffff;" title="White ink"></div>
      <div class="color-dot" data-color="#ff5555" style="background: #ff5555;" title="VCC/Signal Red"></div>
      <div class="color-dot" data-color="#50b5ff" style="background: #50b5ff;" title="GND/Wire Blue"></div>
      <div class="color-dot" data-color="#50fa7b" style="background: #50fa7b;" title="Logic Green"></div>
      <div class="color-dot" data-color="#f1fa8c" style="background: #f1fa8c;" title="Note Yellow"></div>

      <div class="divider"></div>

      <!-- Stroke Width -->
      <button id="width-btn" class="tool-btn" title="Toggle Stroke Width" style="font-size: 0.85rem; font-weight: 700;">
        3px
      </button>

      <div class="divider"></div>

      <select id="shape-tool" aria-label="Drawing tool" class="engineering-select">
        <option value="pen">Freehand</option><option value="line">Line</option><option value="arrow">Arrow</option><option value="rectangle">Rectangle</option><option value="ellipse">Ellipse</option><option value="select">Select / move</option><option value="text">Text label</option>
      </select>
      <select id="dash-tool" aria-label="Line pattern" class="engineering-select"><option value="solid">Solid</option><option value="dashed">Dashed</option><option value="dotted">Dotted</option></select>
      <select id="symbol-tool" aria-label="Insert engineering symbol" class="engineering-select"><option value="">Symbols…</option><option value="resistor">Resistor</option><option value="capacitor">Capacitor</option><option value="ground">Ground</option><option value="opamp">Op-amp</option></select>
      <button id="hold-btn" class="tool-btn active" style="width:auto;font-size:.75rem" title="Hold pen still to straighten">Hold: ON</button>
      <button id="redo-btn" class="tool-btn" title="Redo">↪</button>
      <button id="delete-btn" class="tool-btn" title="Delete selected figure">✕</button>
      <button id="save-btn" class="tool-btn" title="Download editable drawing">💾</button>
      <button id="load-btn" class="tool-btn" title="Open editable drawing">📂</button>
      <input id="load-file" type="file" accept=".json,.hypersketch,application/json" hidden>
      <!-- Tools -->
      <button id="pen-btn" class="tool-btn active" title="Pen Mode">✏️</button>
      <button id="eraser-btn" class="tool-btn" title="Eraser">🧹</button>
      <button id="undo-btn" class="tool-btn" title="Undo">↩️</button>
      <button id="clear-btn" class="tool-btn" title="Clear Canvas">🗑️</button>
    </div>

    <!-- The Primary Insert Action -->
    <button id="insert-btn" class="insert-btn">
      <span>Insert</span>
      <span style="font-size: 1.15rem;">➔</span>
    </button>
  </div>

  <div id="toast" role="status">Inserted into Obsidian! ✓</div>

  <script>
    ${require('./geometry-source')}
    (function() {
      const G=window.HyperSketchGeometry;
      const authKey='hypersketch-token';
      if(location.hash.length>1)localStorage.setItem(authKey,location.hash.slice(1));
      const token=localStorage.getItem(authKey)||'';
      let targetPath=null,sendId=localStorage.getItem('hypersketch-send-id')||null;
      const newId=()=>Array.from(crypto.getRandomValues(new Uint8Array(16)),b=>b.toString(16).padStart(2,'0')).join('');
      const canvas = document.getElementById('pad');
      // Direct local 2D context with hardware desynchronization hint
      const ctx = canvas.getContext('2d', { desynchronized: true });

      const statusDot = document.getElementById('status-dot');
      const noteTitleEl = document.getElementById('active-note-title');
      const gridBtn = document.getElementById('grid-btn');
      const penLockBtn = document.getElementById('pen-lock-btn');
      const penBtn = document.getElementById('pen-btn');
      const eraserBtn = document.getElementById('eraser-btn');
      const undoBtn = document.getElementById('undo-btn');
      const clearBtn = document.getElementById('clear-btn');
      const insertBtn = document.getElementById('insert-btn');
      const widthBtn = document.getElementById('width-btn');
      const colorDots = document.querySelectorAll('.color-dot');
      const toast = document.getElementById('toast');

      // State - stored strictly in memory, zero network during drawing
      let strokes = []; // { points: [[x, y]], color, isAdaptive, width, isEraser }
      let isDrawing = false;
      let currentStroke = null;
      let activeTool = 'pen'; // 'pen' or 'eraser'
      let selectedColor = '#f3f4f6';
      let isAdaptive = true;
      let strokeWidth = 3;
      let penOnly = true;
      let gridStyles = ['dots', 'lines', 'blank'];
      let gridIndex = 0;
      let activePointerId = null;
      let sending = false;
      let history = [],redoHistory=[];
      let pattern='solid',selected=-1,startPoint=null,dragPoint=null,holdTimer=null,holdEnabled=true,holdAnchor=null;
      function checkpoint(){history.push(JSON.stringify(strokes));if(history.length>40)history.shift();redoHistory=[];sendId=null;}
      function stopHold(){clearTimeout(holdTimer);holdTimer=null;}
      function armHold(p){
        if(!holdEnabled||activeTool!=='pen'||!currentStroke||currentStroke.points.length<3)return;
        if(holdAnchor&&Math.hypot(p[0]-holdAnchor[0],p[1]-holdAnchor[1])<4)return;
        stopHold();holdAnchor=p.slice();
        holdTimer=setTimeout(()=>{if(!currentStroke||activeTool!=='pen')return;const points=currentStroke.points;const a=points[0],b=points[points.length-1];if(Math.hypot(a[0]-b[0],a[1]-b[1])<35)return;currentStroke.points=[a,b];redrawAll();},550);
      }
      const logicalWidth = 1400, logicalHeight = 850;
      let dpr = 1;
      let scrollTouch = null;
      const gridCanvas=document.createElement('canvas');
      gridCanvas.width=1400;gridCanvas.height=850;
      const gridCtx=gridCanvas.getContext('2d');
      // Original Lecture Pad renderer: fixed logical surface, transparent context,
      // CSS grid, complete immediate redraw on each pointer event. No rAF/network.
      window.hyperSketchInkDiagnostics = () => ({version:'lecture-pad-original-v1',
        context:ctx.getContextAttributes?.(), backingWidth:canvas.width,
        backingHeight:canvas.height, dpr, activePointerId, strokes:strokes.length});
      function drawStroke(s) {
        ctx.strokeStyle=s.color;ctx.fillStyle=s.color;ctx.lineWidth=s.width;
        ctx.lineCap='round';ctx.lineJoin='round';ctx.setLineDash(G.dash(s));
        if(s.text){ctx.font='28px monospace';ctx.fillText(s.text,...s.points[0]);return;}
        for(const line of G.paths(s)){ctx.beginPath();if(line.length===1){ctx.arc(...line[0],s.width/2,0,Math.PI*2);ctx.fill();}else{line.forEach((p,i)=>i?ctx.lineTo(...p):ctx.moveTo(...p));ctx.stroke();}}
        ctx.setLineDash([]);
      }
      function redrawAll() {
        ctx.clearRect(0,0,1400,850);
        ctx.drawImage(gridCanvas,0,0,1400,850);
        strokes.forEach(drawStroke);
        if(currentStroke) drawStroke(currentStroke);
        if(selected>=0&&strokes[selected]){const b=G.bounds([strokes[selected]]);ctx.strokeStyle='#60a5fa';ctx.lineWidth=1;ctx.setLineDash([6,5]);ctx.strokeRect(b.x-6,b.y-6,b.width+12,b.height+12);ctx.setLineDash([]);}
      }
      function resizeCanvas() {
        dpr=Math.min(devicePixelRatio||1,2);
        canvas.width=1400*dpr; canvas.height=850*dpr;
        ctx.setTransform(dpr,0,0,dpr,0,0); redrawAll();
      }
      function drawGrid() {
        gridCtx.fillStyle='#121214';gridCtx.fillRect(0,0,1400,850);
        gridCtx.fillStyle='#465064';
        if(gridIndex===0){
          for(let x=22;x<1400;x+=22)for(let y=22;y<850;y+=22)gridCtx.fillRect(x-1,y-1,2,2);
        }else if(gridIndex===1){
          for(let x=28;x<1400;x+=28)gridCtx.fillRect(x,0,1,850);
          for(let y=28;y<850;y+=28)gridCtx.fillRect(0,y,1400,1);
        }
        // Rebuild only on grid changes; ordinary ink events copy the cached bitmap.
        redrawAll();
      }
      function saveDraft() {
        try {localStorage.setItem('hypersketch-original-draft-v1',JSON.stringify(strokes));if(sendId)localStorage.setItem('hypersketch-send-id',sendId);else localStorage.removeItem('hypersketch-send-id');}catch(_){}
      }
      try {const saved=JSON.parse(localStorage.getItem('hypersketch-original-draft-v1')||'[]');
        if(Array.isArray(saved)) strokes=G.validate(saved);
      } catch(_) {}
      function point(e) {
        const r=canvas.getBoundingClientRect();
        return [(e.clientX-r.left)*1400/r.width,(e.clientY-r.top)*850/r.height];
      }
      function erase(p) { strokes=strokes.filter(s=>!G.hit(s,p));selected=-1;redrawAll(); }
      canvas.addEventListener('pointerdown',e=>{
        if(penOnly&&e.pointerType==='touch'){
          if(activePointerId===null&&!scrollTouch){scrollTouch={id:e.pointerId,y:e.clientY};canvas.setPointerCapture(e.pointerId);}
          return;
        }
        if(sending || activePointerId!==null)return;
        scrollTouch=null;
        e.preventDefault(); activePointerId=e.pointerId; isDrawing=true;
        canvas.setPointerCapture(activePointerId);
        stopHold();holdAnchor=null;checkpoint();startPoint=point(e);dragPoint=startPoint;
        if(activeTool==='select'){selected=strokes.findLastIndex(s=>G.hit(s,startPoint));currentStroke=null;redrawAll();return;}
        selected=-1;
        if(activeTool==='text'){
          const text=prompt('Label (for example: Vout, R = 10 kΩ, ω₀):','');
          if(text)strokes.push({points:[startPoint],text:text.slice(0,300),color:selectedColor,isAdaptive,width:strokeWidth});
          activePointerId=null;isDrawing=false;saveDraft();redrawAll();return;
        }
        if(activeTool.startsWith('symbol:')){
          const paths=G.symbol(activeTool.slice(7),startPoint);
          strokes.push({points:paths[0],paths,color:selectedColor,isAdaptive,width:strokeWidth,dash:pattern});
          activePointerId=null;isDrawing=false;saveDraft();redrawAll();return;
        }
        const erasing=activeTool==='eraser'||!!(e.buttons&2)||!!(e.buttons&32);
        if(erasing){currentStroke=null;erase(point(e));}
        else currentStroke={color:selectedColor,width:strokeWidth,isAdaptive,dash:pattern,points:[point(e)]};
        redrawAll();
      },{passive:false});
      canvas.addEventListener('pointermove',e=>{
        if(scrollTouch&&e.pointerId===scrollTouch.id){
          e.preventDefault();
          const delta=scrollTouch.y-e.clientY;scrollTouch.y=e.clientY;
          if(activePointerId===null)window.scrollBy(0,delta);
          return;
        }
        if(e.pointerId!==activePointerId)return;
        e.preventDefault();
        if(activeTool==='select'){if(selected>=0){const p=point(e);G.shift(strokes[selected],p[0]-dragPoint[0],p[1]-dragPoint[1]);dragPoint=p;redrawAll();}return;}
        if(currentStroke&&['line','arrow','rectangle','ellipse'].includes(activeTool)){currentStroke.paths=G.shape(activeTool,startPoint,point(e));currentStroke.points=currentStroke.paths[0];redrawAll();return;}
        if(currentStroke){
          const samples=e.getCoalescedEvents?.();
          for(const sample of samples?.length?samples:[e])currentStroke.points.push(point(sample));
          armHold(point(e));redrawAll();
        }else erase(point(e));
      },{passive:false});
      function endStroke(e) {
        if(scrollTouch&&e.pointerId===scrollTouch.id)scrollTouch=null;
        if(e.pointerId!==activePointerId)return;
        stopHold();holdAnchor=null;
        if(currentStroke)strokes.push(currentStroke);
        currentStroke=null;activePointerId=null;isDrawing=false;
        saveDraft();redrawAll();
      }
      canvas.addEventListener('pointerup',endStroke);
      canvas.addEventListener('pointercancel',endStroke);
      canvas.addEventListener('lostpointercapture',endStroke);
      window.addEventListener('pointerup',endStroke);
      window.addEventListener('pointercancel',endStroke);
      canvas.addEventListener('contextmenu',e=>e.preventDefault());
      resizeCanvas();drawGrid();
      // Resize CSS paper only. Backing bitmap, points and pen renderer stay fixed.
      const stage=document.getElementById('stage'), paper=document.getElementById('surface');
      function fitPaper(){
        const w=Math.max(1,Math.min(stage.clientWidth,stage.clientHeight*1400/850));
        paper.style.width=w+'px';paper.style.height=(w*850/1400)+'px';
      }
      new ResizeObserver(fitPaper).observe(stage);fitPaper();
      const installButton=document.getElementById('install-btn');
      let installPrompt=null;
      window.addEventListener('beforeinstallprompt',e=>{
        e.preventDefault();installPrompt=e;installButton.hidden=false;
      });
      installButton.addEventListener('click',async()=>{
        if(!installPrompt)return;
        await installPrompt.prompt();await installPrompt.userChoice;
        installPrompt=null;installButton.hidden=true;
      });
      window.addEventListener('appinstalled',()=>{installButton.hidden=true;});
      if('serviceWorker' in navigator && window.isSecureContext){
        navigator.serviceWorker.register('/sw.js').catch(()=>{});
      }


      // Tools
      penBtn.addEventListener('click', () => {
        activeTool = 'pen';document.getElementById('shape-tool').value='pen';
        penBtn.classList.add('active');
        eraserBtn.classList.remove('active');
      });

      eraserBtn.addEventListener('click', () => {
        activeTool = 'eraser';
        eraserBtn.classList.add('active');
        penBtn.classList.remove('active');
      });

      undoBtn.addEventListener('click', () => {
        if (isDrawing || sending) return;
        if (history.length > 0) {
          redoHistory.push(JSON.stringify(strokes));sendId=null;selected=-1;strokes=JSON.parse(history.pop());
          saveDraft();redrawAll();
        }
      });

      clearBtn.addEventListener('click', () => {
        if (isDrawing || sending) return;
        if (strokes.length === 0) return;
        checkpoint();selected=-1;
        strokes = [];
        saveDraft();redrawAll();
        showToast('Pad cleared');
      });

      // Color selection
      colorDots.forEach(dot => {
        dot.addEventListener('click', () => {
          colorDots.forEach(d => d.classList.remove('active'));
          dot.classList.add('active');
          const col = dot.dataset.color;
          if (col === 'adaptive') {
            selectedColor = '#f3f4f6';
            isAdaptive = true;
          } else {
            selectedColor = col;
            isAdaptive = false;
          }
          activeTool = 'pen';document.getElementById('shape-tool').value='pen';
          penBtn.classList.add('active');
          eraserBtn.classList.remove('active');
        });
      });

      // Stroke width toggle
      const widths = [2, 3, 5];
      let widthIdx = 1;
      widthBtn.addEventListener('click', () => {
        widthIdx = (widthIdx + 1) % widths.length;
        strokeWidth = widths[widthIdx];
        widthBtn.textContent = strokeWidth + 'px';
      });

      // Grid toggle
      let lastGridPointer = -Infinity;
      function toggleGrid() {
        gridIndex = (gridIndex + 1) % gridStyles.length;
        const names = ['Dots', 'Lines', 'Blank'];
        gridBtn.textContent = 'Grid: ' + names[gridIndex];
        drawGrid();
      }
      gridBtn.style.touchAction='manipulation';
      gridBtn.addEventListener('pointerup', e => {
        e.preventDefault();
        lastGridPointer=performance.now();
        toggleGrid();
      });
      gridBtn.addEventListener('click', () => {
        if(performance.now()-lastGridPointer>500)toggleGrid();
      });

      // Pen-only palm rejection toggle
      penLockBtn.addEventListener('click', () => {
        penOnly = !penOnly;
        if (penOnly) {
          penLockBtn.classList.add('active');
          penLockBtn.textContent = '✍️ Pen Only: ON';
        } else {
          penLockBtn.classList.remove('active');
          penLockBtn.textContent = '🖐️ Touch: ALLOW';
        }
      });

      document.getElementById('shape-tool').onchange=e=>{activeTool=e.target.value;document.getElementById('symbol-tool').value='';selected=-1;stopHold();redrawAll();};
      document.getElementById('dash-tool').onchange=e=>{pattern=e.target.value;};
      document.getElementById('symbol-tool').onchange=e=>{if(e.target.value)activeTool='symbol:'+e.target.value;};
      document.getElementById('hold-btn').onclick=e=>{holdEnabled=!holdEnabled;e.currentTarget.textContent='Hold: '+(holdEnabled?'ON':'OFF');stopHold();};
      document.getElementById('redo-btn').onclick=()=>{if(isDrawing||sending||!redoHistory.length)return;history.push(JSON.stringify(strokes));strokes=JSON.parse(redoHistory.pop());selected=-1;sendId=null;saveDraft();redrawAll();};
      document.getElementById('delete-btn').onclick=()=>{if(isDrawing||sending||selected<0)return;checkpoint();strokes.splice(selected,1);selected=-1;saveDraft();redrawAll();};
      document.getElementById('save-btn').onclick=()=>{
        const url=URL.createObjectURL(new Blob([JSON.stringify({version:1,strokes})],{type:'application/json'}));
        const a=document.createElement('a');a.href=url;a.download='drawing.hypersketch';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
      };
      document.getElementById('load-btn').onclick=()=>document.getElementById('load-file').click();
      document.getElementById('load-file').onchange=async e=>{
        const file=e.target.files[0];if(!file||isDrawing||sending)return;
        try{if(file.size>4*1024*1024)throw Error('Drawing too large');const model=G.validate(JSON.parse(await file.text()).strokes);if(strokes.length&&!confirm('Replace this drawing? You can Undo.'))return;checkpoint();strokes=model;selected=-1;saveDraft();redrawAll();}catch(err){showToast(err.message,'err');}finally{e.target.value='';}
      };
      function exportSvg(){return strokes.length?G.svg(strokes):null;}

      // DELIVERY PATH: Tap Insert -> send to laptop -> inject into note
      async function insertSketch() {
        if (isDrawing || sending) return;
        const crop = exportSvg(16);
        if (!crop) {
          showToast('Draw something first!', 'err');
          return;
        }

        sendId ||= newId();saveDraft();
        sending = true;
        insertBtn.classList.add('sending');
        insertBtn.innerHTML = '<span>Sending...</span>';

        try {
          const res = await fetch('/api/inject', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Authorization':'Bearer '+token },
            body: JSON.stringify({ sketchId:sendId||(sendId=newId()), notePath:targetPath, strokes, svgData:crop.svg, width:crop.width,height:crop.height })
          });
          const data = await res.json();
          if (res.ok && data.status === 'ok') {
            if (navigator.vibrate) navigator.vibrate([40, 60, 40]);
            showToast(data.injected ? 'Inserted into note! ✓' : 'Saved to vault! ✓');
            strokes = []; history=[];redoHistory=[];selected=-1;sendId=null;
            saveDraft();redrawAll();
          } else {
            showToast('Failed: ' + (data.error || 'Error'), 'err');
          }
        } catch (err) {
          showToast('Connection error: ' + err.message, 'err');
        } finally {
          sending = false;
          insertBtn.classList.remove('sending');
          insertBtn.innerHTML = '<span>Insert</span><span style="font-size: 1.15rem;">➔</span>';
        }
      }

      insertBtn.addEventListener('click', insertSketch);

      // Keyboard shortcut (Ctrl+Enter)
      window.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') insertSketch();
      });

      function showToast(msg, type = 'ok') {
        toast.textContent = msg;
        toast.className = (type === 'err') ? 'err' : '';
        toast.classList.add('show');
        setTimeout(() => toast.classList.remove('show'), 2000);
      }

      // Passive status check (only when user is idle)
      async function checkStatus() {
        if (isDrawing) return; // Never do network fetch while drawing!
        try {
          const res = await fetch('/api/status',{headers:{Authorization:'Bearer '+token}});
          if (!res.ok) {noteTitleEl.textContent='Scan the QR in Obsidian settings';return;}
          if (res.ok) {
            const data = await res.json();
            if (isDrawing) return;
            targetPath=data.notePath||null;
            statusDot.classList.add('online');
            noteTitleEl.textContent = data.activeNote || 'No active note (will save to vault)';
            noteTitleEl.style.color = data.activeNote ? '#e5e7eb' : '#fbbf24';
          }
        } catch (_) {}
      }
      checkStatus();setInterval(checkStatus, 4000);
    })();
  </script>
</body>
</html>`;
}

module.exports = getPWAHtml;
