# githubpages — páginas públicas de mis aplicaciones

Una subcarpeta por aplicación o página. Se publica tal cual con GitHub Pages.

| Carpeta | Qué es | Cómo se actualiza |
|---|---|---|
| `transitgocity/` | Política de privacidad y condiciones de uso de TransitGoCity (5 idiomas) | `transitgocity/README.md` (se genera con `generar.py` desde los textos de la app) |

`index.html` es la portada con la lista; añade una línea por cada página nueva. `.nojekyll` hace
que GitHub publique los ficheros sin procesarlos.

## Publicar en GitHub Pages (una vez)

**Recomendado: repositorio de usuario** `<tu-usuario>.github.io`. Así la web queda en la raíz
`https://<tu-usuario>.github.io/` y sirve para todas las apps; además permite poner en la raíz el
`app-ads.txt` que pide AdMob (ver `transitgocity/README.md`).

1. GitHub → **New repository** → nombre exactamente `<tu-usuario>.github.io` → **Public** →
   *Create repository*.
2. Desde esta carpeta (`C:\workspace\proyectos\githubpages`):
   ```powershell
   git init -b main
   git add .
   git commit -m "Páginas de TransitGoCity"
   git remote add origin https://github.com/<tu-usuario>/<tu-usuario>.github.io.git
   git push -u origin main
   ```
3. Repositorio → **Settings → Pages** → *Source: Deploy from a branch* → *main* / `/ (root)` →
   *Save* (en los repositorios `<usuario>.github.io` suele venir ya activado).
4. En 1-2 minutos:
   - `https://<tu-usuario>.github.io/transitgocity/privacidad.html` ← **URL para Play Console y AdMob**
   - `https://<tu-usuario>.github.io/transitgocity/condiciones.html`

Si prefieres otro nombre de repositorio (p. ej. `paginas`), las URL llevan ese nombre delante:
`https://<tu-usuario>.github.io/paginas/transitgocity/privacidad.html`.

## Para cada actualización

```powershell
cd C:\workspace\proyectos\githubpages\transitgocity
python generar.py
cd ..
git add . ; git commit -m "Actualizo textos legales" ; git push
```

El repositorio es **público**: solo textos para publicar. Nunca copies aquí `local.properties`,
`keystore.properties`, `.env` ni código del servidor.
