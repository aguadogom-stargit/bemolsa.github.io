#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera las páginas públicas de la política de privacidad y las condiciones de uso de
TransitGoCity para GitHub Pages, a partir de los MISMOS textos que muestra la app
(app/src/main/res/values*/strings.xml), para que la web y la app nunca digan cosas distintas.

Uso (desde esta carpeta):   python generar.py
Datos que no están en la app (titular, correo, fecha): config.json.
Ver README.md (en tuscity: docs/plan-publicacion-google-play-1.md §3.3).
"""
import html
import json
import re
import sys
from datetime import date
from pathlib import Path

AQUI = Path(__file__).resolve().parent
# Recursos de la app: config.json "res_app" (relativo a esta carpeta o absoluto). Por defecto, el
# proyecto tuscity junto a githubpages: C:\\workspace\\proyectos\\{githubpages,tuscity}.
_CFG = json.loads((AQUI / "config.json").read_text(encoding="utf-8"))
RES = (AQUI / _CFG.get("res_app", "../../tuscity/app/src/main/res")).resolve()

IDIOMAS = [  # (código, carpeta de recursos, nombre propio, locale html)
    ("es", "values-es", "Español", "es"),
    ("en", "values", "English", "en"),
    ("fr", "values-fr", "Français", "fr"),
    ("de", "values-de", "Deutsch", "de"),
    ("it", "values-it", "Italiano", "it"),
]
MESES = {
    "es": "enero febrero marzo abril mayo junio julio agosto septiembre octubre noviembre diciembre",
    "en": "January February March April May June July August September October November December",
    "fr": "janvier février mars avril mai juin juillet août septembre octobre novembre décembre",
    "de": "Januar Februar März April Mai Juni Juli August September Oktober November Dezember",
    "it": "gennaio febbraio marzo aprile maggio giugno luglio agosto settembre ottobre novembre dicembre",
}
TEXTOS_WEB = {  # textos propios de la web (no existen en la app)
    "es": {"privacidad": "Política de privacidad", "condiciones": "Condiciones de uso", "idioma": "Idioma",
           "intro": "Información legal de la aplicación", "pie": "Este texto es el mismo que se muestra dentro de la aplicación (Perfil).",
           "pendiente": "PENDIENTE: nombre del titular"},
    "en": {"privacidad": "Privacy policy", "condiciones": "Terms of use", "idioma": "Language",
           "intro": "Legal information for the app", "pie": "This text is the same one shown inside the app (Profile).",
           "pendiente": "PENDING: owner's name"},
    "fr": {"privacidad": "Politique de confidentialité", "condiciones": "Conditions d'utilisation", "idioma": "Langue",
           "intro": "Informations légales de l'application", "pie": "Ce texte est identique à celui affiché dans l'application (Profil).",
           "pendiente": "EN ATTENTE : nom du titulaire"},
    "de": {"privacidad": "Datenschutzrichtlinie", "condiciones": "Nutzungsbedingungen", "idioma": "Sprache",
           "intro": "Rechtliche Informationen zur App", "pie": "Dieser Text ist derselbe, der in der App angezeigt wird (Profil).",
           "pendiente": "AUSSTEHEND: Name des Inhabers"},
    "it": {"privacidad": "Informativa sulla privacy", "condiciones": "Termini di utilizzo", "idioma": "Lingua",
           "intro": "Informazioni legali dell'app", "pie": "Questo testo è lo stesso mostrato nell'app (Profilo).",
           "pendiente": "IN SOSPESO: nome del titolare"},
}
ORDEN_PRIVACIDAD = ["privacidad_1", "privacidad_2", "privacidad_3", "privacidad_4", "privacidad_formulario",
                    "privacidad_5", "privacidad_6", "privacidad_7", "privacidad_8"]
ORDEN_CONDICIONES = [f"condiciones_{i}" for i in range(1, 12)]


def leer_strings(carpeta):
    xml = (RES / carpeta / "strings.xml").read_text(encoding="utf-8")
    out = {}
    for m in re.finditer(r'<string name="([^"]+)"[^>]*>(.*?)</string>', xml, re.S):
        v = m.group(2)
        v = v.replace("\\'", "'").replace('\\"', '"').replace("\\n", "\n")
        v = v.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
        out[m.group(1)] = v
    return out


def fecha_larga(lang, f):
    mes = MESES[lang].split()[f.month - 1]
    return {"es": f"{f.day} de {mes} de {f.year}", "en": f"{f.day} {mes} {f.year}",
            "fr": f"{f.day} {mes} {f.year}", "de": f"{f.day}. {mes} {f.year}",
            "it": f"{f.day} {mes} {f.year}"}[lang]


def enlazar(texto_html, correo):
    texto_html = re.sub(r"(policies\.google\.com/[\w/\-]+)", r'<a href="https://\1">\1</a>', texto_html)
    if correo:
        c = html.escape(correo)
        texto_html = texto_html.replace(c, f'<a href="mailto:{c}">{c}</a>')
    return texto_html


def parrafo(texto, correo):
    texto = texto.replace("%1$s", correo)
    m = re.match(r"^(\d+\.\s+[^.]+\.)\s*(.*)$", texto, re.S)  # "1. Responsable. resto"
    if m:
        return (f'<section><h2>{html.escape(m.group(1))}</h2>'
                f'<p>{enlazar(html.escape(m.group(2)), correo)}</p></section>')
    return f"<p>{enlazar(html.escape(texto), correo)}</p>"


CSS = """
:root{--bg:#f7f7f5;--fg:#1b1d21;--muted:#5d636d;--card:#fff;--line:#e3e4e6;--accent:#0b6bcb}
@media (prefers-color-scheme:dark){:root{--bg:#121417;--fg:#e9eaec;--muted:#a3a8b1;--card:#1b1e23;--line:#2c3038;--accent:#6aa8ff}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
header{border-bottom:1px solid var(--line);background:var(--card)}
.wrap{max-width:760px;margin:0 auto;padding:0 16px}
.top{display:flex;flex-wrap:wrap;gap:8px 16px;align-items:center;justify-content:space-between;padding:14px 0}
.marca{font-weight:700;font-size:18px;color:var(--fg);text-decoration:none}
nav.idiomas{display:flex;flex-wrap:wrap;gap:4px}
nav.idiomas a{padding:4px 10px;border-radius:999px;color:var(--muted);text-decoration:none;font-size:14px}
nav.idiomas a[aria-current]{background:var(--accent);color:#fff}
nav.docs{display:flex;gap:16px;padding-bottom:12px;font-size:15px}
nav.docs a{color:var(--muted);text-decoration:none;padding-bottom:4px;border-bottom:2px solid transparent}
nav.docs a[aria-current]{color:var(--fg);border-color:var(--accent)}
main.wrap{padding:28px 16px 48px}
h1{font-size:28px;line-height:1.25;margin:0 0 4px}
.fecha{color:var(--muted);margin:0 0 24px}
h2{font-size:17px;margin:24px 0 4px}
p{margin:0 0 8px}
a{color:var(--accent)}
.pendiente{background:#fff3c4;color:#5b4500;padding:0 4px;border-radius:4px}
footer{border-top:1px solid var(--line);color:var(--muted);font-size:14px;padding:16px 0 32px}
ul.lista{padding-left:20px}
"""


ACTUAL = ' aria-current="page"'


def pagina(lang, titulo, cuerpo, actual, enlaces_idioma, cfg, t):
    idiomas = "".join(
        f'<a href="{href}" lang="{c}" hreflang="{c}"{ACTUAL if c == lang else ""}>{html.escape(n)}</a>'
        for c, n, href in enlaces_idioma)
    docs = (f'<a href="privacidad.html"{ACTUAL if actual == "privacidad" else ""}>{html.escape(t["privacidad"])}</a>'
            f'<a href="condiciones.html"{ACTUAL if actual == "condiciones" else ""}>{html.escape(t["condiciones"])}</a>')
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(titulo)} · {html.escape(cfg["app"])}</title>
<meta name="description" content="{html.escape(titulo)} — {html.escape(cfg["app"])}">
<style>{CSS}</style>
</head>
<body>
<header><div class="wrap">
<div class="top"><a class="marca" href="../index.html">{html.escape(cfg["app"])}</a>
<nav class="idiomas" aria-label="{html.escape(t["idioma"])}">{idiomas}</nav></div>
<nav class="docs">{docs}</nav>
</div></header>
<main class="wrap">
{cuerpo}
</main>
<footer><div class="wrap">{html.escape(t["pie"])}</div></footer>
</body>
</html>
"""


def main():
    cfg = json.loads((AQUI / "config.json").read_text(encoding="utf-8"))
    f = date.fromisoformat(cfg["fecha"]) if cfg.get("fecha") else date.today()
    avisos = []
    if not cfg.get("titular"):
        avisos.append("config.json: 'titular' vacío -> la política sale con el aviso PENDIENTE en el punto 1.")
    for lang, carpeta, nombre, _ in IDIOMAS:
        s = leer_strings(carpeta)
        t = TEXTOS_WEB[lang]
        titular = cfg.get("titular") or ""
        correo = cfg.get("correo", "")
        fecha_txt = re.sub(r"\[[^\]]*\]", fecha_larga(lang, f), s["legal_ultima_actualizacion"])
        for doc, clave_titulo, orden in (("privacidad", "privacidad_titulo_largo", ORDEN_PRIVACIDAD),
                                         ("condiciones", "condiciones_titulo_largo", ORDEN_CONDICIONES)):
            partes = []
            for k in orden:
                texto = s[k]
                marca = None
                if k == "privacidad_1":
                    marca = "@@TITULAR@@"
                    texto = re.sub(r"\[[^\]]*\]", marca, texto)
                if "[" in texto:
                    avisos.append(f"{lang}/{k}: queda un texto entre corchetes: {texto[:80]}")
                h = parrafo(texto, correo)
                if marca:
                    h = h.replace(marca, html.escape(titular) if titular
                                  else f'<span class="pendiente">{html.escape(t["pendiente"])}</span>')
                partes.append(h)
            cuerpo = ("<h1>" + html.escape(s[clave_titulo]) + "</h1>\n<p class=\"fecha\">" + html.escape(fecha_txt) + "</p>\n"
                      + "\n".join(partes))
            enlaces = [(c, n, f"../{c}/{doc}.html") for c, _, n, _ in IDIOMAS]
            destino = AQUI / lang / f"{doc}.html"
            destino.parent.mkdir(exist_ok=True)
            destino.write_text(pagina(lang, s[clave_titulo], cuerpo, doc, enlaces, cfg, t), encoding="utf-8")

    # Páginas raíz: índice y accesos directos que eligen idioma (las URL para Play Console).
    filas = "".join(
        f'<li lang="{c}"><strong>{html.escape(n)}</strong> — '
        f'<a href="{c}/privacidad.html">{html.escape(TEXTOS_WEB[c]["privacidad"])}</a> · '
        f'<a href="{c}/condiciones.html">{html.escape(TEXTOS_WEB[c]["condiciones"])}</a></li>'
        for c, _, n, _ in IDIOMAS)
    indice = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(cfg["app"])}</title><style>{CSS}</style></head>
<body><header><div class="wrap"><div class="top"><span class="marca">{html.escape(cfg["app"])}</span></div></div></header>
<main class="wrap"><h1>{html.escape(cfg["app"])}</h1><p class="fecha">{html.escape(TEXTOS_WEB["es"]["intro"])} · {html.escape(TEXTOS_WEB["en"]["intro"])}</p>
<ul class="lista">{filas}</ul>
<p>Contacto / Contact: <a href="mailto:{html.escape(cfg["correo"])}">{html.escape(cfg["correo"])}</a></p></main></body></html>
"""
    (AQUI / "index.html").write_text(indice, encoding="utf-8")

    codigos = [c for c, *_ in IDIOMAS]
    for doc in ("privacidad", "condiciones"):
        # Sin JavaScript (p. ej. el revisor de Google) se ve el enlace a cada idioma; con JS se
        # redirige al idioma del navegador (español si no está entre los cinco).
        lista = "".join(f'<li><a href="{c}/{doc}.html">{html.escape(n)}</a></li>' for c, _, n, _ in IDIOMAS)
        (AQUI / f"{doc}.html").write_text(f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(TEXTOS_WEB["es"][doc])} · {html.escape(cfg["app"])}</title>
<link rel="canonical" href="es/{doc}.html">
<script>(function(){{var s={json.dumps(codigos)},l=(navigator.languages||[navigator.language||"es"]);
for(var i=0;i<l.length;i++){{var c=(l[i]||"").slice(0,2).toLowerCase();if(s.indexOf(c)>=0){{location.replace(c+"/{doc}.html");return;}}}}
location.replace("es/{doc}.html");}})();</script>
<style>{CSS}</style></head>
<body><main class="wrap"><h1>{html.escape(cfg["app"])}</h1><ul class="lista">{lista}</ul></main></body></html>
""", encoding="utf-8")

    print("Generado en", AQUI)
    for a in avisos:
        print("AVISO:", a)
    return 0


if __name__ == "__main__":
    sys.exit(main())
