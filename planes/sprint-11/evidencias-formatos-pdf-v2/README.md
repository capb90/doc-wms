# Evidencias — Formatos v2 de PDF

Plan: [`../plan-cerrado-f2-formatos-pdf-v2-2026-11-26.md`](../plan-cerrado-f2-formatos-pdf-v2-2026-11-26.md).

## Fase 1 (BE) — 2026-11-27

BE en `f2/formatos-pdf-v2`, desde `fase-2` `6ccff7b`.

### QA-PV2-001: el legacy no cambia (PASA)

**Método.** Una prueba de integración temporal, que no se subió, dibujó los mismos datos dos veces en la misma corrida:

- con el código de antes: una copia de los tres servicios de `fase-2` `6ccff7b`;
- con el de después: los servicios con el registro de datos y el dibujo legacy movido a `Services/Pdf/`.

Hubo dos fuentes:

- **Base local `wmsdb`:** el depósito de la QA `5f3749d2-…` (2026BA00013), con su etiqueta, sus 3 tarjetas por vehículo y su PDF del depósito. La base local no tiene guías.
- **Escenario en Testcontainers:**
  - un depósito de importación nacionalizado con salida y guía;
  - uno de importación sin levantes, con unidad de carga;
  - uno de exportación, con su etiqueta y su tarjeta;
  - la guía en QR, por depósito (con sufijo `-1`), con código de barras y anulada (marca de agua).

Cada par se comparó con `pdftotext -layout` y con una imagen de cada página (`pdftoppm`, 100 ppp), byte a byte.

**Resultado.** Los 18 pares tienen el mismo texto y la misma imagen. La única diferencia es un segundo en «impreso el …» de un PDF del depósito, que cambió de segundo entre los dos dibujos ([`fase-1/pv2-001-comparacion.txt`](fase-1/pv2-001-comparacion.txt)).

**Archivos.** En `fase-1/`, los PDF `pv2-001-*.antes.pdf` y `*.despues.pdf`, su texto (`.txt`) y la captura de la primera página del de después (`*.despues-1.png`):

- `qa-etiqueta`, `qa-tarjeta-1` y `qa-deposito`: depósito de la QA, base local;
- `vigente-guia` y `anulada-guia`: guía de salida, escenario;
- `exp-deposito`: PDF del depósito de exportación;
- `imp-unidad-carga-etiqueta`: etiqueta sin levantes (banda roja) y con la línea de unidades de carga.

### QA-PV2-002 y 003 (PASA, por API)

Las contraseñas locales del README no sirven, así que no se entró como Administrador al frontend. Los dos casos se probaron por API: `PATCH administration/system-parameters/{id}` con un token de Admin, sobre el API de las pruebas de integración (`Wms.IntegrationTests/ForeignTrade/PdfFormatParameterTests.cs`).

- **QA-PV2-002:** `value = "otro"` en cada uno de los tres parámetros responde 400 «El parámetro {código} solo admite LEGACY o V2.» y el valor sigue en `LEGACY`. Con `v2`, en minúsculas, responde 200.
- **QA-PV2-003:** `DEPOSIT_PDF_FORMAT` con `V2` e inactivo: el proveedor devuelve `Legacy`. Al reactivarlo devuelve `V2`. En la fase 1, con `V2` salen todavía los cuatro documentos legacy (200, `application/pdf`).

En la base local, la migración `20261127060211_AddPdfFormatParameters` creó los tres parámetros en `LEGACY`.
