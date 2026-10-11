# PANALIM · Pan de Ambato Doña Adita

Apps de control operativo (offline, instalables en Android como PWA).

| Carpeta | App |
|---|---|
| `public/app1/` | App 1 · Producción (orden y moldeado) |
| `public/app7/` | App 7 · Turno 2 (supervisor, pastelería) |
| `public/app8/` | App 8 · T3 Moldeador |

## Publicar en Vercel
1. vercel.com → *Add New → Project* → importar este repo.
2. *Framework preset:* **Other**, sin build command. `vercel.json` ya apunta a `public/`.
3. Deploy. Abrir `https://TU-PROYECTO.vercel.app/` desde Chrome en el Android y, en cada app, menú ⋮ → **Instalar aplicación**.

## Actualizar una app
```
python3 tools/build_pwa.py app1=ruta/PANALIM_App1.html app7=ruta/App7.html app8=ruta/App8.html
git add -A && git commit -m "Actualiza apps" && git push
```
Las apps se actualizan solas la siguiente vez que se abren con internet (cerrar y abrir 2 veces).

Los datos viven en el teléfono (localStorage del dominio). Hacer respaldo con el botón de cada app antes de cambiar de dominio o borrar datos del navegador.
