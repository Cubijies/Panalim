/* PANALIM service worker · 20261025001326 · abre sin internet; se actualiza solo cuando hay conexión */
const V='panalim-app8-20261025001326',FILES=['./','index.html','manifest.webmanifest','../shared/pwa.js','icons/icon-192.png','icons/icon-512.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(V).then(c=>c.addAll(FILES)).then(()=>self.skipWaiting()))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x.startsWith('panalim-app8-')&&x!==V).map(x=>caches.delete(x)))).then(()=>self.clients.claim()))});
self.addEventListener('fetch',e=>{const r=e.request;if(r.method!=='GET'||new URL(r.url).origin!==location.origin)return;
 /* red primero (siempre la versión más nueva); si no hay internet o tarda más de 4 s, usa lo guardado */
 e.respondWith(new Promise(res=>{let done=false;const fromCache=()=>caches.match(r,{ignoreSearch:true}).then(h=>h||caches.match('index.html'));
  const t=setTimeout(()=>{if(!done)fromCache().then(h=>{if(h&&!done){done=true;res(h)}})},4000);
  fetch(r,{cache:'no-cache'}).then(x=>{if(x&&x.ok){const cp=x.clone();caches.open(V).then(c=>c.put(r,cp))}if(!done){done=true;clearTimeout(t);res(x)}}).catch(()=>{clearTimeout(t);if(!done)fromCache().then(h=>{done=true;res(h||Response.error())})})}))});
