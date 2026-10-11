/* PANALIM · PWA: service worker + botón «atrás» controlado (no saca de la app) */
(function(){'use strict';
if('serviceWorker' in navigator)addEventListener('load',()=>navigator.serviceWorker.register('sw.js').catch(()=>{}));
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
