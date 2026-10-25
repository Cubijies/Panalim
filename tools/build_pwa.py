#!/usr/bin/env python3
"""Genera public/appN/ (PWA instalable) a partir de los HTML de PANALIM.
Uso:  python3 tools/build_pwa.py app1=ruta/App1.html app7=ruta/App7.html app8=ruta/App8.html
Cada app queda en su carpeta con index.html, manifest, sw.js e iconos (se instala como app aparte en Android)."""
import sys,os,json,time,re
ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','public')
META={'app1':('PANALIM · Producción','Producción','Orden y moldeado del turno 1'),
      'app7':('PANALIM · Turno 2','Turno 2','Supervisor: local principal, pastelería, T3'),
      'app8':('PANALIM · T3 Moldeador','T3 Moldeador','Registro del moldeador del turno tarde')}
VER=time.strftime('%Y%m%d%H%M%S')
HEAD='''<link rel="manifest" href="manifest.webmanifest"><meta name="theme-color" content="#75242a"><meta name="mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-title" content="%s"><link rel="apple-touch-icon" href="icons/icon-192.png"><link rel="icon" href="icons/icon-192.png">'''
SW='''/* PANALIM service worker · %(ver)s · abre sin internet; se actualiza solo cuando hay conexión */
const V='panalim-%(app)s-%(ver)s',FILES=['./','index.html','manifest.webmanifest','../shared/pwa.js','icons/icon-192.png','icons/icon-512.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(V).then(c=>c.addAll(FILES)).then(()=>self.skipWaiting()))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x.startsWith('panalim-%(app)s-')&&x!==V).map(x=>caches.delete(x)))).then(()=>self.clients.claim()))});
self.addEventListener('fetch',e=>{const r=e.request;if(r.method!=='GET'||new URL(r.url).origin!==location.origin)return;
 /* red primero (siempre la versión más nueva); si no hay internet o tarda más de 4 s, usa lo guardado */
 e.respondWith(new Promise(res=>{let done=false;const fromCache=()=>caches.match(r,{ignoreSearch:true}).then(h=>h||caches.match('index.html'));
  const t=setTimeout(()=>{if(!done)fromCache().then(h=>{if(h&&!done){done=true;res(h)}})},4000);
  fetch(r,{cache:'no-cache'}).then(x=>{if(x&&x.ok){const cp=x.clone();caches.open(V).then(c=>c.put(r,cp))}if(!done){done=true;clearTimeout(t);res(x)}}).catch(()=>{clearTimeout(t);if(!done)fromCache().then(h=>{done=true;res(h||Response.error())})})}))});
'''
def main():
    for a in sys.argv[1:]:
        app,src=a.split('=',1);name,short,desc=META[app]
        h=open(src,encoding='utf8').read()
        h=re.sub(r'<link rel="manifest"[^>]*>','',h)
        assert '</head>' in h and '</body>' in h
        h=h.replace('</head>',HEAD%short+'</head>',1)
        h=h.replace('</body>','<script src="../shared/pwa.js"></script></body>',1)
        d=os.path.join(ROOT,app);os.makedirs(d,exist_ok=True)
        open(os.path.join(d,'index.html'),'w',encoding='utf8').write(h)
        man={'name':name,'short_name':short,'description':desc,'id':'/%s/'%app,'start_url':'./','scope':'./','display':'standalone','orientation':'any','lang':'es','background_color':'#f4f0ea','theme_color':'#75242a',
         'icons':[{'src':'icons/icon-192.png','sizes':'192x192','type':'image/png','purpose':'any'},{'src':'icons/icon-512.png','sizes':'512x512','type':'image/png','purpose':'any'},{'src':'icons/maskable-192.png','sizes':'192x192','type':'image/png','purpose':'maskable'},{'src':'icons/maskable-512.png','sizes':'512x512','type':'image/png','purpose':'maskable'}]}
        json.dump(man,open(os.path.join(d,'manifest.webmanifest'),'w'),indent=2,ensure_ascii=False)
        open(os.path.join(d,'sw.js'),'w').write(SW%{'app':app,'ver':VER})
        print('OK',app,round(os.path.getsize(os.path.join(d,'index.html'))/1024),'KB')
SHELL_SW=SW.replace("'../shared/pwa.js'","'shared/pwa.js','app1/','app7/','app8/'").replace("panalim-%(app)s-","panalim-shell-")
def shell():
    ip=os.path.join(ROOT,'index.html');h=open(ip,encoding='utf8').read();import re as _r;h=_r.sub(r'v(__BUILD__|\d{14})','v'+VER,h);open(ip,'w',encoding='utf8').write(h)
    open(os.path.join(ROOT,'sw.js'),'w').write(SHELL_SW%{'app':'shell','ver':VER});print('OK shell sw')
main();shell()
