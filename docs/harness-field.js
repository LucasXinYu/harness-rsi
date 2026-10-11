'use strict';
// A conceptual rendering of the editable software around the model. No simulated telemetry.
(() => {
  const field = document.getElementById('harness-field');
  const canvas = document.getElementById('harness-canvas');
  const ctx = canvas?.getContext('2d');
  if (!ctx || !field) return;
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
  const toggle = document.getElementById('motion-toggle');
  const colors = {tools:[121,234,211],context:[112,183,255],memory:[184,153,255],control:[255,187,126]};
  let selected='tools', width=580, height=440, time=0, previous=0, frame=0;
  let paused=reducedMotion.matches, visible=true, pointer={x:0,y:0}, drift={x:0,y:0};
  const rgba=(color,alpha)=>`rgba(${color.join(',')},${alpha})`;
  const points=Array.from({length:230},(_,i)=>{
    const y=1-(i/229)*2,r=Math.sqrt(1-y*y),a=i*Math.PI*(3-Math.sqrt(5));
    return {x:Math.cos(a)*r,y,z:Math.sin(a)*r};
  });
  function project(p, rotation=0){
    const a=rotation+drift.x*.16, x=p.x*Math.cos(a)-p.z*Math.sin(a), z=p.x*Math.sin(a)+p.z*Math.cos(a);
    const tilt=-.17+drift.y*.1, y=p.y*Math.cos(tilt)-z*Math.sin(tilt), depth=p.y*Math.sin(tilt)+z*Math.cos(tilt);
    const size=Math.min(width*.305,height*.40), perspective=3.8/(3.8-depth);
    return {x:width*.5+x*size*perspective,y:height*.49+y*size*perspective,z:depth};
  }
  function line(a,b,color,alpha,lineWidth=1){
    ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.strokeStyle=rgba(color,alpha);ctx.lineWidth=lineWidth;ctx.stroke();
  }
  function draw(){
    ctx.clearRect(0,0,width,height);
    drift.x+=(pointer.x-drift.x)*.055;drift.y+=(pointer.y-drift.y)*.055;
    const c=colors[selected],cx=width*.5,cy=height*.49,r=Math.min(width*.305,height*.4);
    const glow=ctx.createRadialGradient(cx,cy,r*.1,cx,cy,r*1.65);
    glow.addColorStop(0,rgba(c,.10));glow.addColorStop(.55,rgba(c,.055));glow.addColorStop(1,rgba(c,0));
    ctx.fillStyle=glow;ctx.fillRect(0,0,width,height);
    // Sparse background stars are deterministic; animation never changes source data.
    for(let i=0;i<44;i++){
      const x=((i*137.5+31)%577)/577*width,y=((i*79.7+17)%431)/431*height;
      ctx.fillStyle=rgba([172,197,223],.12+(i%3)*.075);ctx.fillRect(x,y,1,1);
    }
    const projected=points.map(p=>project(p,time*.055));
    // Short mesh edges reveal the shell while keeping its center readable.
    for(let i=0;i<points.length;i++){
      for(let j=i+1;j<points.length;j++){
        const a=points[i],b=points[j],distance=(a.x-b.x)**2+(a.y-b.y)**2+(a.z-b.z)**2;
        if(distance<.075){const depth=(projected[i].z+projected[j].z)/2;line(projected[i],projected[j],c,.025+(depth+1)*.07);}
      }
    }
    projected.sort((a,b)=>a.z-b.z).forEach(p=>{
      const opacity=.12+(p.z+1)*.22;
      ctx.beginPath();ctx.arc(p.x,p.y,.6+(p.z+1)*.48,0,Math.PI*2);ctx.fillStyle=rgba(c,opacity);ctx.fill();
    });
    // Four differently tilted software layers, with a brighter selected layer.
    Object.entries(colors).forEach(([name,color],i)=>{
      const tilt=[.48,-.56,.92,-1.03][i],angle=[.2,1.6,2.2,.9][i];
      const ring=t=>{
        const x=Math.cos(t)*1.26,y=Math.sin(t)*.52,z=Math.sin(t)*.79;
        return project({x:x*Math.cos(tilt)-y*Math.sin(tilt),y:x*Math.sin(tilt)+y*Math.cos(tilt),z},angle);
      };
      let last=ring(0);
      for(let j=1;j<=150;j++){
        const next=ring(j/150*Math.PI*2);
        line(last,next,color,(name===selected ? .35 : .09)+(next.z+1)*(name===selected ? .15 : .035),name===selected?1.2:.65);last=next;
      }
      const t=time*(.18+i*.018)+i*1.5,head=ring(t);
      for(let j=15;j>0;j--){const a=ring(t-j*.021),b=ring(t-(j-1)*.021);line(a,b,color,(1-j/16)*.7,1.8);}
      ctx.shadowBlur=13;ctx.shadowColor=rgba(color,.9);ctx.fillStyle=rgba(color,1);
      ctx.beginPath();ctx.arc(head.x,head.y,name===selected?3.1:1.9,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;
    });
    // A quiet, unchanging core distinguishes the task model from editable layers.
    const core=ctx.createRadialGradient(cx,cy,12,cx,cy,r*.51);
    core.addColorStop(0,'rgba(10,18,31,.98)');core.addColorStop(.65,'rgba(10,18,31,.94)');core.addColorStop(1,'rgba(10,18,31,0)');
    ctx.fillStyle=core;ctx.beginPath();ctx.arc(cx,cy,r*.51,0,Math.PI*2);ctx.fill();
    ctx.strokeStyle=rgba(c,.34);ctx.lineWidth=.8;ctx.beginPath();
    for(let i=0;i<=6;i++){const a=Math.PI/3*i-Math.PI/2;const x=cx+Math.cos(a)*r*.37,y=cy+Math.sin(a)*r*.37;if(i===0)ctx.moveTo(x,y);else ctx.lineTo(x,y);}ctx.stroke();
  }
  function animate(now){
    frame=0;
    if(!paused&&visible&&!document.hidden){
      if(now-previous>=32){time+=Math.min((now-previous)/1000,.065);previous=now;draw();}
      frame=requestAnimationFrame(animate);
    }
  }
  function syncMotion(){
    cancelAnimationFrame(frame);frame=0;
    toggle.setAttribute('aria-pressed',String(paused));
    toggle.setAttribute('aria-label',paused?'Play diagram animation':'Pause diagram animation');
    toggle.replaceChildren(document.createTextNode(paused?'▷ ':'Ⅱ '));
    const label=document.createElement('span');label.textContent=paused?'Play motion':'Pause motion';toggle.append(label);
    draw();if(!paused&&visible&&!document.hidden){previous=performance.now();frame=requestAnimationFrame(animate);}
  }
  function resize(){
    const box=field.getBoundingClientRect();width=box.width;height=box.height;
    const dpr=Math.min(window.devicePixelRatio||1,2);canvas.width=Math.round(width*dpr);canvas.height=Math.round(height*dpr);ctx.setTransform(dpr,0,0,dpr,0,0);draw();
  }
  field.querySelector('.field-overlay').hidden=false;field.classList.add('field-ready');
  if('ResizeObserver' in window)new ResizeObserver(resize).observe(field);else window.addEventListener('resize',resize);
  field.addEventListener('pointermove',event=>{if(paused)return;const box=field.getBoundingClientRect();pointer={x:(event.clientX-box.left)/width-.5,y:(event.clientY-box.top)/height-.5};});
  field.addEventListener('pointerleave',()=>{pointer={x:0,y:0};});
  document.querySelectorAll('[data-orbit-surface]').forEach(node=>node.addEventListener('click',()=>document.getElementById(`surface-tab-${node.dataset.orbitSurface}`).click()));
  document.addEventListener('harness-surface',event=>{
    if(!colors[event.detail])return;selected=event.detail;
    document.querySelectorAll('[data-orbit-surface]').forEach(node=>node.setAttribute('aria-pressed',String(node.dataset.orbitSurface===selected)));draw();
  });
  toggle.addEventListener('click',()=>{paused=!paused;syncMotion();});
  reducedMotion.addEventListener('change',()=>{paused=reducedMotion.matches;syncMotion();});
  document.addEventListener('visibilitychange',syncMotion);
  if('IntersectionObserver' in window)new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;syncMotion();},{rootMargin:'80px'}).observe(field);
  resize();syncMotion();
})();
