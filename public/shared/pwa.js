/* PANALIM · PWA: service worker + botón «atrás» controlado (no saca de la app) */
(function(){'use strict';
if('serviceWorker' in navigator){const had=!!navigator.serviceWorker.controller;let shown=false;
 addEventListener('load',()=>navigator.serviceWorker.register('sw.js').then(r=>{const chk=()=>{try{r.update()}catch(_){}};chk();document.addEventListener('visibilitychange',()=>{if(!document.hidden)chk()});setInterval(chk,10*60*1000)}).catch(()=>{}));
 navigator.serviceWorker.addEventListener('controllerchange',()=>{if(!had||shown)return;shown=true;const b=document.createElement('div');b.style.cssText='position:fixed;left:0;right:0;top:0;z-index:100000;background:#0b7c77;color:#fff;padding:10px 14px;font:600 14px system-ui;display:flex;gap:10px;justify-content:space-between;align-items:center';b.innerHTML='<span>Hay una versión nueva de la app</span><button style="border:0;border-radius:8px;padding:7px 12px;font-weight:700">Actualizar ahora</button>';b.querySelector('button').onclick=()=>location.reload();document.body.appendChild(b)})}
const G=window;let stack=[],cur=null,lastBack=0,busy=false;
const toast=m=>{try{G.toast?G.toast(m):alert(m)}catch(_){}};
/* ---- pantalla actual (módulo/pestaña) según la app ---- */
function getNav(){try{
 if(G.PANALIMPrototype&&G.PANALIMPrototype.state){const S=G.PANALIMPrototype.state;return{sig:S.module+'|'+(S.tabs&&S.tabs[S.module]),set(sig){const[m,t]=sig.split('|');S.module=m;if(S.tabs&&t&&t!=='undefined')S.tabs[m]=t;G.renderModule()}}}
 if(typeof S!=='undefined'&&S&&typeof S.tab==='string'&&typeof render==='function')return{sig:S.tab,set(sig){S.tab=sig;try{localStorage.setItem(KEY,JSON.stringify(S))}catch(_){}render()}};
}catch(_){}return null}
/* ---- ventanas abiertas: se cierran primero ---- */
function closeOverlay(){
 const dm=document.getElementById('docModal');if(dm&&dm.classList.contains('open')){dm.classList.remove('open');dm.setAttribute('aria-hidden','true');return true}
 const sh=document.getElementById('pnShare');if(sh&&sh.style.display==='flex'){sh.style.display='none';return true}
 const pc=document.getElementById('pnCons');if(pc){pc.remove();return true}
 const m=document.querySelector('.overlay.open,.modal-backdrop.open,dialog[open]');if(m){m.classList.remove('open');if(m.close)m.close();return true}
 return false}
function push(){try{history.pushState({pn:1},'')}catch(_){}}
history.replaceState({pn:0},'');push();
/* cada cambio de pantalla se recuerda para que «atrás» vuelva a la anterior */
setInterval(()=>{const n=getNav();if(!n||busy)return;if(cur===null){cur=n.sig;return}if(n.sig!==cur){stack.push(cur);cur=n.sig;if(stack.length>30)stack.shift();push()}},250);
/* el diálogo de compartir / vista previa también cuenta como «paso» */
addEventListener('popstate',()=>{
 if(closeOverlay()){push();return}
 const n=getNav();
 if(n&&stack.length){const prev=stack.pop();busy=true;cur=prev;try{n.set(prev)}catch(e){console.error(e)}setTimeout(()=>busy=false,400);push();return}
 const now=Date.now();
 if(now-lastBack<2500){history.back();return}      /* segundo «atrás» seguido: sale */
 lastBack=now;toast('Toque «atrás» otra vez para salir de la app');push()});
/* evitar recargar con deslizar-hacia-abajo y cerrar sin querer con datos sin guardar: los datos ya se guardan solos */
})();
