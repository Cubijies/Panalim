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
HEAD='''<link rel="manifest" href="manifest.webmanifest"><meta name="theme-color" content="#75242a"><meta name="mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-title" content="%s"><link rel="apple-touch-icon" href="icons/icon-192.png"><link rel="icon" href="icons/icon-192.png"><style>html,body{overscroll-behavior-y:contain}</style>'''
SW='''/* PANALIM service worker · %(ver)s · abre sin internet; se actualiza solo cuando hay conexión */
const V='panalim-%(app)s-%(ver)s',FILES=['./','index.html','manifest.webmanifest','../shared/pwa.js','icons/icon-192.png','icons/icon-512.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(V).then(c=>c.addAll(FILES)).then(()=>self.skipWaiting()))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x.startsWith('panalim-%(app)s-')&&x!==V).map(x=>caches.delete(x)))).then(()=>self.clients.claim()))});
self.addEventListener('fetch',e=>{const r=e.request;if(r.method!=='GET')return;
 e.respondWith(caches.match(r,{ignoreSearch:true}).then(hit=>{const net=fetch(r).then(res=>{if(res&&res.ok&&new URL(r.url).origin===location.origin){const cp=res.clone();caches.open(V).then(c=>c.put(r,cp))}return res}).catch(()=>hit);return hit||net}))});
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
main()
