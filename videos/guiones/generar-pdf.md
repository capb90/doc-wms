# Cómo generar el PDF de los guiones

La fuente de los guiones es `guiones-video-tutoriales.md` (esta carpeta). El PDF `docs/videos/Guiones_Video_Tutoriales_WMS.pdf` se genera desde ahí con `generar_pdf.py`: Markdown → HTML con CSS de impresión → PDF con WeasyPrint.

**No edites el PDF a mano.** Cambia el Markdown y vuelve a generarlo.

## Requisitos (una sola vez)

- Python 3.9 o superior.
- Pango, la librería de texto que usa WeasyPrint. En macOS: `brew install pango`.
- Un entorno virtual con `markdown` y `weasyprint`:

```bash
python3 -m venv ~/.venvs/guiones-wms
```

```bash
~/.venvs/guiones-wms/bin/pip install markdown weasyprint
```

## Generar

Desde `docs/videos/guiones`:

```bash
DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib ~/.venvs/guiones-wms/bin/python generar_pdf.py
```

- `DYLD_FALLBACK_LIBRARY_PATH` solo hace falta en macOS con Homebrew, para que WeasyPrint encuentre Pango. En Linux se omite.
- El script escribe `../Guiones_Video_Tutoriales_WMS.pdf` y muestra «PDF generado: …».
- Opciones:
  - `--html ruta.html` guarda también el HTML intermedio, útil para revisar el diseño en el navegador;
  - `--salida ruta.pdf` escribe el PDF en otro lugar (para borradores).

## Qué produce

- Tamaño carta, con portada, «Registro de cambios», «Índice de videos» (con números de página), la sección A y las series en orden de grabación por bloques (1, 2, 4, 5, 6, 7, 3 y 0).
- Encabezado: «Bodegas Asociadas · Centro de Ayuda» y «Versión … · …».
- Pie: «Guiones de Video Tutoriales · Centro de Ayuda — Sistema WMS» y «Página N de M».
- **Cada guion se mantiene entero en una página** (`break-inside: avoid`). Las tablas largas de la sección A repiten su encabezado y no cortan filas.

## Reglas del Markdown que el script exige

El script falla con un mensaje claro si un guion no cumple el formato:

- `## Serie N · Nombre` abre una serie; `### N.M · Título` abre un guion.
- Debajo del título del guion van, en este orden:
  - `**Duración:** … · **Rol:** …`;
  - `**OBJETIVO** · …`, `**GRABA CON** · …` y `**REQUISITOS** · …`;
  - la tabla `| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |`, con una fila por paso y sin el carácter `|` dentro de las celdas;
  - `**Cierre:** …`.
- Las rutas de menú van entre comillas invertidas y se ven como etiqueta. `**Verás:**` se resalta en verde y `[verificar en pantalla]`, en ámbar.
- La portada se arma con el bloque `---` del inicio del archivo (título, subtítulo, alcance, versión y fecha).

## Al publicar una versión nueva

1. Actualiza `version` y `fecha` en el bloque inicial y el «Registro de cambios».
2. Si cambian guiones, actualiza `inventario-cambios-guiones.md` y, si cambian datos, `dataset-grabacion.md`.
3. Genera el PDF y revisa que cada guion quede en su página.
4. Haz commit del Markdown y del PDF juntos.
