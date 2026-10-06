# TransitGoCity — política de privacidad y condiciones de uso

Generadas con `generar.py` desde los **mismos textos que muestra la app**
(`tuscity/app/src/main/res/values*/strings.xml`), en es, en, fr, de, it. Plan de publicación:
`tuscity/docs/plan-publicacion-google-play-1.md` §3.3.

| Fichero | Para qué |
|---|---|
| `privacidad.html` | **URL para Play Console y AdMob.** Abre el idioma del navegador (español por defecto); sin JavaScript muestra los enlaces a los 5 idiomas |
| `condiciones.html` | igual, para las condiciones de uso |
| `es/ en/ fr/ de/ it/` | páginas de cada idioma |
| `index.html` | portada de la app con todos los enlaces |
| `config.json` | lo que no está en la app: `titular`, `correo`, `fecha` y `res_app` (ruta a los textos de la app, por defecto `../../tuscity/app/src/main/res`) |
| `generar.py` | regenera todo (Python 3.8+). **No edites los `.html` a mano**: se sobrescriben |

## Actualizar

El titular (Oscar Aguado Gómez) y la fecha de «Última actualización» están en los textos de la app
(`strings.xml`, 5 idiomas). Cuando cambien los textos legales de la app (y su fecha):
`python generar.py`, revisar los AVISOS y subir.

## app-ads.txt (AdMob)

AdMob lo busca en la raíz del dominio del «sitio web del desarrollador» de la ficha de Play. Con el
repositorio `<usuario>.github.io` la raíz es `https://<usuario>.github.io/`: cuando tengas el ID de
editor de AdMob, crea `githubpages/app-ads.txt` (en la raíz, no aquí) con la línea que te da AdMob
(`google.com, pub-XXXXXXXXXXXXXXXX, DIRECT, f08c47fec0942fa0`) y pon `https://<usuario>.github.io`
como sitio web en Play Console.
