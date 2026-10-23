#!/usr/bin/env python3
"""Genera docs/videos/Guiones_Video_Tutoriales_WMS.pdf desde guiones-video-tutoriales.md.

Uso (ver generar-pdf.md):
    python generar_pdf.py                 # escribe ../Guiones_Video_Tutoriales_WMS.pdf
    python generar_pdf.py --html out.html # además guarda el HTML intermedio

Requiere: markdown y weasyprint (con Pango instalado en el sistema).
"""
from __future__ import annotations

import argparse
import html
import re
from pathlib import Path

import markdown

AQUI = Path(__file__).resolve().parent
FUENTE = AQUI / "guiones-video-tutoriales.md"
SALIDA = AQUI.parent / "Guiones_Video_Tutoriales_WMS.pdf"
PIE = "Guiones de Video Tutoriales · Centro de Ayuda — Sistema WMS"

RE_GUION = re.compile(r"^(\d+\.\d+) · (.+)$")
RE_META = re.compile(r"^\*\*Duración:\*\* (.+?) · \*\*Rol:\*\* (.+)$")
RE_CAMPO = re.compile(r"^\*\*(OBJETIVO|GRABA CON|REQUISITOS)\*\* · (.+)$")
RE_CIERRE = re.compile(r"^\*\*Cierre:\*\* (.+)$")
RE_SERIE = re.compile(r"^Serie (\d+) · (.+)$")


def inline(texto: str) -> str:
    """Convierte Markdown en línea (negrita, código) a HTML sin el <p> envolvente."""
    h = markdown.markdown(texto.strip())
    h = re.sub(r"^<p>(.*)</p>$", r"\1", h, flags=re.S)
    return decorar(h)


def bloque(texto: str) -> str:
    # Python-Markdown exige una línea en blanco antes de una lista: se agrega si falta.
    lineas, previa = [], ""
    for linea in texto.splitlines():
        es_item = re.match(r"^\s*([-*]|\d+\.) ", linea) is not None
        previa_item = re.match(r"^\s*([-*]|\d+\.) ", previa) is not None
        if es_item and previa.strip() and not previa_item and not linea.startswith("  "):
            lineas.append("")
        lineas.append(linea)
        previa = linea
    return decorar(markdown.markdown("\n".join(lineas), extensions=["tables"], tab_length=2))


def decorar(h: str) -> str:
    h = h.replace("[verificar en pantalla", '<span class="verificar">[verificar en pantalla')
    h = re.sub(r'(<span class="verificar">\[verificar en pantalla[^\]]*\])', r"\1</span>", h)
    h = h.replace("<strong>Verás:</strong>", '<strong class="veras">Verás:</strong>')
    return h


def ancla(numero: str) -> str:
    return "g" + numero.replace(".", "-")


def leer_fuente() -> tuple[dict[str, str], str]:
    texto = FUENTE.read_text(encoding="utf-8")
    meta: dict[str, str] = {}
    m = re.match(r"^---\n(.*?)\n---\n", texto, flags=re.S)
    if m:
        for linea in m.group(1).splitlines():
            clave, _, valor = linea.partition(":")
            meta[clave.strip()] = valor.strip()
        texto = texto[m.end():]
    texto = re.sub(r"<!--.*?-->", "", texto, flags=re.S)
    return meta, texto


def partir(texto: str, nivel: str) -> list[tuple[str, str]]:
    """Divide por encabezados del nivel dado ('## ' o '### ')."""
    partes: list[tuple[str, str]] = []
    titulo, cuerpo = None, []
    previo: list[str] = []
    for linea in texto.splitlines():
        if linea.startswith(nivel):
            if titulo is not None:
                partes.append((titulo, "\n".join(cuerpo)))
            else:
                previo = cuerpo
            titulo, cuerpo = linea[len(nivel):].strip(), []
        else:
            cuerpo.append(linea)
    if titulo is not None:
        partes.append((titulo, "\n".join(cuerpo)))
    else:
        return [("", "\n".join(cuerpo))]
    if previo and "".join(previo).strip():
        partes.insert(0, ("", "\n".join(previo)))
    return partes


def render_guion(numero: str, titulo: str, cuerpo: str) -> str:
    duracion = rol = cierre = ""
    campos: list[tuple[str, str]] = []
    filas: list[list[str]] = []
    for linea in cuerpo.splitlines():
        linea = linea.rstrip()
        if not linea:
            continue
        if m := RE_META.match(linea):
            duracion, rol = m.group(1), m.group(2)
        elif m := RE_CAMPO.match(linea):
            campos.append((m.group(1), m.group(2)))
        elif m := RE_CIERRE.match(linea):
            cierre = m.group(1)
        elif linea.startswith("|"):
            celdas = [c.strip() for c in linea.strip().strip("|").split("|")]
            if celdas and set(celdas[0]) <= {"-", ":"}:
                continue
            if celdas[0] == "#":
                continue
            if len(celdas) != 3:
                raise ValueError(f"Guion {numero}: fila con {len(celdas)} celdas: {linea[:80]}")
            filas.append(celdas)
        else:
            raise ValueError(f"Guion {numero}: línea no reconocida: {linea[:80]}")
    if not (duracion and campos and filas and cierre):
        raise ValueError(f"Guion {numero}: faltan partes obligatorias")

    campos_html = "".join(
        f'<div class="campo"><span class="etq">{html.escape(k)}</span><span class="val">{inline(v)}</span></div>'
        for k, v in campos
    )
    filas_html = "".join(
        f'<tr><td class="n">{html.escape(n)}</td><td class="accion">{inline(a)}</td>'
        f'<td class="narr">{inline(t)}</td></tr>'
        for n, a, t in filas
    )
    return f"""
<section class="guion" id="{ancla(numero)}">
  <div class="cabeza">
    <div class="barra"><span class="num">{numero}</span><span class="tit">{inline(titulo)}</span>
      <span class="dur">{html.escape(duracion)} · {html.escape(rol)}</span></div>
    <div class="campos">{campos_html}</div>
  </div>
  <table class="tabla-guion">
    <thead><tr><th class="n">#</th><th>En pantalla (lo que haces)</th><th>Narración sugerida (lo que dices)</th></tr></thead>
    <tbody>{filas_html}</tbody>
  </table>
  <div class="cierre"><strong>Cierre:</strong> {inline(cierre)}</div>
</section>"""


def render_capitulo(titulo: str, cuerpo: str, indice: list[tuple[str, str, str]]) -> str:
    if m := RE_SERIE.match(titulo):
        badge, clase = m.group(1), "serie"
        serie_txt = titulo
    elif titulo.startswith("A ·"):
        badge, clase, serie_txt = "A", "seccion", titulo
    else:
        badge, clase, serie_txt = "v2", "seccion", titulo
    partes = partir(cuerpo, "### ")
    html_partes = []
    for sub, texto in partes:
        if not sub:
            html_partes.append(f'<div class="intro">{bloque(texto)}</div>')
        elif g := RE_GUION.match(sub):
            indice.append((g.group(1), g.group(2), serie_txt))
            html_partes.append(render_guion(g.group(1), g.group(2), texto))
        else:
            html_partes.append(f"<h3>{inline(sub)}</h3>{bloque(texto)}")
    return f"""
<section class="capitulo {clase}">
  <h2><span class="badge">{badge}</span>{inline(titulo)}</h2>
  {''.join(html_partes)}
</section>"""


def render_indice(indice: list[tuple[str, str, str]]) -> str:
    def clave(item):
        s, n = item[0].split(".")
        return (int(s), int(n))

    filas, serie_actual = [], None
    for numero, titulo, serie in sorted(indice, key=clave):
        if serie != serie_actual:
            filas.append(f'<li class="serie-idx">{html.escape(serie)}</li>')
            serie_actual = serie
        filas.append(
            f'<li><a href="#{ancla(numero)}"><span class="inum">{numero}</span>'
            f'<span class="itit">{inline(titulo)}</span></a></li>'
        )
    return f"""
<section class="capitulo seccion indice">
  <h2><span class="badge">≡</span>Índice de videos</h2>
  <p class="nota-idx">En orden de publicación (series 0 a 7). El orden de grabación está en la sección A.3.</p>
  <ul class="lista-idx">{''.join(filas)}</ul>
</section>"""


def render_portada(meta: dict[str, str]) -> str:
    titulo = meta.get("titulo", "Guiones de Video Tutoriales").split()
    t1 = " ".join(titulo[:2])
    t2 = " ".join(titulo[2:-1])
    t3 = titulo[-1]
    return f"""
<section class="portada">
  <div class="chip">BODEGAS ASOCIADAS · CENTRO DE AYUDA</div>
  <h1>{html.escape(t1)}<br>{html.escape(t2)}<br><span>{html.escape(t3)}</span></h1>
  <p class="sub">{html.escape(meta.get('subtitulo', ''))}</p>
  <div class="raya"></div>
  <p class="dato"><b>Alcance:</b> {html.escape(meta.get('alcance', ''))}</p>
  <p class="dato"><b>Orden:</b> {html.escape(meta.get('orden', ''))}</p>
  <p class="dato"><b>Incluye:</b> {html.escape(meta.get('incluye', ''))}</p>
  <p class="dato"><b>Versión:</b> {html.escape(meta.get('version', ''))} · <b>Fecha:</b> {html.escape(meta.get('fecha', ''))}</p>
  <div class="pie-portada"><span>{html.escape(meta.get('pie_portada', ''))}</span><span>Uso interno</span></div>
</section>"""


CSS = """
@page {
  size: letter;
  margin: 20mm 17mm 19mm 17mm;
  @top-left { content: "Bodegas Asociadas · Centro de Ayuda"; font: 7.5pt "Helvetica Neue", Helvetica, Arial, sans-serif; color: #8a97ad; }
  @top-right { content: "Versión VERSION · FECHA"; font: 7.5pt "Helvetica Neue", Helvetica, Arial, sans-serif; color: #8a97ad; }
  @bottom-left { content: "PIE"; font: 7.5pt "Helvetica Neue", Helvetica, Arial, sans-serif; color: #8a97ad; }
  @bottom-right { content: "Página " counter(page) " de " counter(pages); font: 600 7.5pt "Helvetica Neue", Helvetica, Arial, sans-serif; color: #1e3a6e; }
}
@page portada { margin: 0; @top-left { content: none; } @top-right { content: none; } @bottom-left { content: none; } @bottom-right { content: none; } }

html { font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; font-size: 8.6pt; color: #1f2937; line-height: 1.38; }
body { margin: 0; }
b, strong { font-weight: 600; }
code { font-family: Menlo, "DejaVu Sans Mono", monospace; font-size: 7.4pt; background: #e8eefb; color: #1e3a6e; padding: 0.2pt 2.5pt; border-radius: 2pt; white-space: normal; }
.verificar { background: #fff4d6; color: #8a5a00; font-style: normal; font-weight: 600; font-size: 7.4pt; padding: 0 2pt; border-radius: 2pt; }
strong.veras { color: #0f766e; }

/* Portada */
.portada { page: portada; height: 279.4mm; box-sizing: border-box; padding: 34mm 26mm 18mm 26mm; position: relative;
  background: linear-gradient(160deg, #11284f 0%, #1b3f7a 55%, #2563a8 100%); color: #e8eefb; }
.portada .chip { display: inline-block; border: 0.8pt solid #9cc1f5; border-radius: 12pt; padding: 3pt 12pt; font-size: 8pt; letter-spacing: 2.2pt; font-weight: 600; color: #ffffff; }
.portada h1 { font-size: 40pt; line-height: 1.05; margin: 22mm 0 7mm 0; color: #ffffff; font-weight: 700; }
.portada h1 span { color: #93c5fd; }
.portada .sub { font-size: 12pt; max-width: 135mm; color: #dbe7fb; margin: 0 0 9mm 0; }
.portada .raya { width: 48mm; height: 2.4pt; background: #93c5fd; border-radius: 2pt; margin-bottom: 9mm; }
.portada .dato { font-size: 9pt; margin: 1.6mm 0; color: #dbe7fb; }
.portada .dato b { color: #ffffff; }
.portada .pie-portada { position: absolute; left: 26mm; right: 26mm; bottom: 16mm; border-top: 0.6pt solid #6f93c9; padding-top: 3mm;
  font-size: 8pt; color: #c7d7f0; display: flex; justify-content: space-between; }

/* Capítulos */
.capitulo { break-before: page; }
h2 { font-size: 17pt; color: #11284f; margin: 0 0 3mm 0; font-weight: 700; display: flex; align-items: center; }
h2 .badge { display: inline-block; min-width: 9mm; height: 9mm; line-height: 9mm; text-align: center; background: #1e3a6e; color: #fff;
  border-radius: 2mm; font-size: 11pt; margin-right: 4mm; padding: 0 1.5mm; }
.intro p { font-size: 9.2pt; color: #4b5563; margin: 0 0 4mm 0; }
h3 { font-size: 11pt; color: #1e3a6e; margin: 6mm 0 2mm 0; break-after: avoid; }
p { margin: 0 0 2.5mm 0; }
ul { margin: 0 0 3mm 0; padding-left: 5mm; }
li { margin-bottom: 0.8mm; }

/* Tablas genéricas (registro de cambios, sección A) */
table { width: 100%; border-collapse: collapse; margin: 0 0 4mm 0; }
th { background: #1e3a6e; color: #fff; text-align: left; font-weight: 600; font-size: 8pt; padding: 1.8mm 2mm; }
td { border-bottom: 0.5pt solid #dfe4ec; padding: 1.6mm 2mm; vertical-align: top; }
tr { break-inside: avoid; }
thead { display: table-header-group; }
.seccion td { font-size: 8.2pt; }

/* Guion */
.guion { margin: 0 0 7mm 0; break-inside: avoid; }
.cabeza { break-inside: avoid; break-after: avoid; }
.barra { background: #1e3a6e; color: #fff; border-radius: 2mm 2mm 0 0; padding: 2.4mm 3mm; display: flex; align-items: center; }
.barra .num { background: #93c5fd; color: #11284f; font-weight: 700; border-radius: 1.4mm; padding: 0.6mm 2mm; margin-right: 3mm; font-size: 9pt; }
.barra .tit { font-weight: 600; font-size: 10.5pt; flex: 1; }
.barra .tit code { background: #2d4f8a; color: #e8eefb; }
.barra .dur { font-size: 7.8pt; color: #c7d7f0; margin-left: 3mm; text-align: right; }
.campos { background: #f3f6fb; border: 0.5pt solid #d5dbe5; border-top: none; padding: 2mm 3mm 1.2mm 3mm; margin-bottom: 1.6mm; }
.campo { display: flex; margin-bottom: 1mm; }
.campo .etq { width: 24mm; flex: none; font-size: 7pt; font-weight: 700; letter-spacing: 0.7pt; color: #2563a8; padding-top: 0.6mm; }
.campo .val { flex: 1; }
.tabla-guion { margin-bottom: 1.6mm; }
.tabla-guion th { background: #2b4c86; }
.tabla-guion th.n, .tabla-guion td.n { width: 5mm; text-align: center; }
.tabla-guion td.n { font-weight: 700; color: #1e3a6e; }
.tabla-guion td.accion { width: 47%; }
.tabla-guion td.narr { font-style: italic; color: #374151; }
.tabla-guion tbody tr:nth-child(even) td { background: #fafbfd; }
.cierre { background: #e9f7ef; border: 0.5pt solid #b7e2c8; border-radius: 0 0 2mm 2mm; padding: 2mm 3mm; color: #14532d; font-style: italic; break-inside: avoid; break-before: avoid; }
.cierre strong { font-style: normal; color: #166534; }

/* Índice */
.nota-idx { color: #6b7280; font-size: 8.4pt; }
.lista-idx { list-style: none; padding: 0; columns: 2; column-gap: 8mm; }
.lista-idx li { break-inside: avoid; margin: 0 0 0.9mm 0; font-size: 8.2pt; }
.lista-idx li.serie-idx { font-weight: 700; color: #11284f; margin-top: 2.4mm; border-bottom: 0.5pt solid #d5dbe5; padding-bottom: 0.6mm; break-after: avoid; }
.lista-idx a { color: #1f2937; text-decoration: none; display: flex; }
.lista-idx a::after { content: target-counter(attr(href), page); color: #6b7280; margin-left: auto; padding-left: 2mm; }
.lista-idx .inum { width: 9mm; flex: none; font-weight: 700; color: #1e3a6e; }
.lista-idx .itit { flex: 1; }
"""


def construir_html() -> str:
    meta, texto = leer_fuente()
    indice: list[tuple[str, str, str]] = []
    capitulos = [render_capitulo(t, c, indice) for t, c in partir(texto, "## ") if t]
    # El índice va después del registro de cambios.
    cuerpo = capitulos[0] + render_indice(indice) + "".join(capitulos[1:])
    css = (CSS.replace("VERSION", meta.get("version", "")).replace("FECHA", meta.get("fecha", "")).replace("PIE", PIE))
    titulo = f"{meta.get('titulo', '')} — Centro de Ayuda WMS"
    return f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><title>{html.escape(titulo)}</title>
<meta name="author" content="Bodegas Asociadas">
<meta name="description" content="Plan de producción de las 8 series de video tutoriales">
<meta name="keywords" content="WMS, tutoriales, guiones, centro de ayuda, capacitación">
<style>{css}</style></head>
<body>{render_portada(meta)}{cuerpo}</body></html>"""


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--html", type=Path, help="Guarda también el HTML intermedio")
    p.add_argument("--salida", type=Path, default=SALIDA)
    args = p.parse_args()
    documento = construir_html()
    if args.html:
        args.html.write_text(documento, encoding="utf-8")
    from weasyprint import HTML  # import tardío: el HTML se puede generar sin WeasyPrint

    HTML(string=documento, base_url=str(AQUI)).write_pdf(args.salida)
    print(f"PDF generado: {args.salida}")


if __name__ == "__main__":
    main()
