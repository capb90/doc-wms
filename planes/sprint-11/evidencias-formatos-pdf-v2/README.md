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

## Fase 2 (BE) — 2026-11-27

BE en `f2/formatos-pdf-v2`, sobre la fase 1 (`0612773`). Etiqueta del depósito y tarjeta por vehículo v2 de importación, exportación e inspección (D11, D12 con D27, D22), con el encabezado compacto de D9, las fuentes embebidas de D10 (Inter 4.1 y JetBrains Mono, SIL OFL) y el diseño del mockup [`../qa-manual/formato-etiqueta-v2/`](../qa-manual/formato-etiqueta-v2/).

**Método.** Igual que en la fase 1: una prueba de integración temporal, que no se subió, llamó a `LabelGenerationService` con el formato fijo en `V2` o en `LEGACY`. Así no hizo falta cambiar `LABEL_FORMAT` en la base local. Las contraseñas locales del README no sirven, así que no se entró al frontend. El cambio del parámetro por API (`PATCH` con token de Admin) lo cubre la prueba de integración que sí se sube, `PdfFormatParameterTests.LabelFormat_V2_ChangesTheLabelsAndVehicleCards`: con `V2`, las seis descargas (etiqueta y tarjeta de importación, exportación e inspección) cambian y llevan Inter y JetBrains Mono embebidas; con `LEGACY`, no.

Hubo dos fuentes:

- **Base local `wmsdb`:** el depósito de la QA `5f3749d2-…` (2026BA00013) con sus 3 tarjetas; 2026BA00012 (sin levantes); 2026BA00003 (con unidad de carga y levante); 2026INSP00007 (inspección). La base local no tiene depósitos de exportación.
- **Escenario en Testcontainers:** importación sin levantes con un tanquero (unidad de carga); exportación e inspección con agencia de aduanas y dos documentos adicionales del servicio (con y sin fecha).

Cada PDF se guardó con su texto (`pdftotext -layout`, `.txt`) y la captura de su página (`-1.png`, 110 ppp). Todos caben en una página A5.

### QA-PV2-004: etiqueta del depósito de la QA en V2 (PASA)

[`fase-2/pv2-004-qa-etiqueta.v2.pdf`](fase-2/pv2-004-qa-etiqueta.v2.pdf) ([captura](fase-2/pv2-004-qa-etiqueta.v2-1.png)), frente a [`screen.png`](../qa-manual/formato-etiqueta-v2/screen.png):

- **Encabezado:** el montacargas en su recuadro, el logotipo vectorial (nombre, NIT y «DEPÓSITO HABILITADO COD. 22080», D23) y, a la derecha, «Deposito No.» con 2026BA00013 en rojo y el Code 128 de hoy, con el número legible debajo.
- **Partes:** recuadro con Importador (COMERCIALIZADORA LUHOMAR S.A.S), Intermediario (SURCOMEX S.A NIVEL 2) y Fecha Ingreso 2026-11-26 13:36:36.
- **Tabla:** Ampara 640,13 · Saldo 1.920 · FRIJOL EN GRANO (SACOS), en es-CO (`DEC-082`).
- **Documentos:** Carta Porte PE000843 (2026-11-24), Manifiesto No. 116575014469850 (2026-11-26) y Placa(s) IBA2021, PUB010, XAI1204. Sin «Unidad(es) de carga», porque el depósito no tiene (`AJQ/` D17; el mockup pinta «N/A», D4).
- **Banda y nacionalización:** banda verde «MERCANCIA NACIONALIZADA»; «DATOS DE NACIONALIZACION» con Levantes 372024000009520 (26/11/2026) y N Aceptacion 372024000009905 (26/11/2026).

### QA-PV2-005: sin levantes y con unidades de carga (PASA)

- **Sin levantes:** [`pv2-005-local-sin-levantes-etiqueta.v2`](fase-2/pv2-005-local-sin-levantes-etiqueta.v2-1.png) (2026BA00012) y [`pv2-005-imp-sin-levantes-unidades-etiqueta.v2`](fase-2/pv2-005-imp-sin-levantes-unidades-etiqueta.v2-1.png) (escenario): banda roja «MERCANCIA SIN NACIONALIZAR» y sin el bloque de nacionalización.
- **Con unidades de carga:** la del escenario muestra «Unidad(es) de carga: TANQUERO …», y su tarjeta por vehículo también ([`pv2-005-imp-sin-levantes-unidades-tarjeta.v2`](fase-2/pv2-005-imp-sin-levantes-unidades-tarjeta.v2-1.png)). [`pv2-005-local-con-unidades-etiqueta.v2`](fase-2/pv2-005-local-con-unidades-etiqueta.v2-1.png) (2026BA00003) muestra «CONTENEDOR QAIC05», dos productos con su Ampara por fila, banda verde y su levante.

### QA-PV2-006: tarjetas por vehículo del depósito de la QA en V2 (PASA)

[`pv2-006-qa-tarjeta-1.v2`](fase-2/pv2-006-qa-tarjeta-1.v2-1.png), [`-2`](fase-2/pv2-006-qa-tarjeta-2.v2-1.png) y [`-3`](fase-2/pv2-006-qa-tarjeta-3.v2-1.png): el diseño de la etiqueta con la placa de cada camión destacada, la tabla con solo «Cant. ingresa» y «Mercancia» de sus filas (sin Ampara ni Saldo, D27), el manifiesto DIAN con su fecha, banda verde y el bloque de nacionalización.

### QA-PV2-012: exportación e inspección en V2 (PASA)

- **Exportación** (escenario): [etiqueta](fase-2/pv2-012-exp-etiqueta.v2-1.png) y [tarjeta](fase-2/pv2-012-exp-tarjeta.v2-1.png) con banda azul «MERCANCIA PARA EXPORTACION», Exportador e Intermediario, la línea del documento, los documentos adicionales y Placa(s).
- **Inspección** (escenario): [etiqueta](fase-2/pv2-012-insp-etiqueta.v2-1.png) y [tarjeta](fase-2/pv2-012-insp-tarjeta.v2-1.png) con banda naranja «INSPECCION ADUANERA», Importador, Exportador e Intermediario.
- **Inspección** (base local, 2026INSP00007, sin partes ni productos): [etiqueta](fase-2/pv2-012-local-insp-etiqueta.v2-1.png) y [tarjeta](fase-2/pv2-012-local-insp-tarjeta.v2-1.png), con los «N/A» y la fila vacía de hoy.

### El legacy no cambia

En la fase 2, la etiqueta de exportación e inspección pasó a su registro de datos (`DepositLabelData`), y su dibujo pasó, sin cambios, a `Services/Pdf/LegacyDepositLabelRenderer.cs`. Con `LEGACY`, sale igual que antes ([`fase-2/legacy-comparacion.txt`](fase-2/legacy-comparacion.txt)):

- **Exportación e inspección:** se comparó cada etiqueta dibujada con una copia del servicio de `0612773` y con el código nuevo. El texto y la imagen salen iguales: [`pv2-012-exp-etiqueta.antes.pdf`](fase-2/pv2-012-exp-etiqueta.antes.pdf) contra [`.despues.pdf`](fase-2/pv2-012-exp-etiqueta.despues.pdf), y lo mismo con `insp`.
- **Importación:** la etiqueta y la tarjeta 1 legacy del depósito de la QA salen iguales a las de la fase 1 (`fase-1/pv2-001-qa-*.despues.pdf`).

### Compuertas (BE `bf61eac`)

| Compuerta | Antes (`0612773`) | Después |
| --- | --- | --- |
| `dotnet build Wms.sln` | Sin errores | Sin errores |
| `Wms.Tests` | 2447 | 2465, con la guardia `NumberCultureGuardTests` (29) en verde |
| `Wms.IntegrationTests` | 891 | 892 |
| `has-pending-model-changes` | — | Limpio |

Las dos suites de antes corrieron en la misma sesión, sobre un worktree de `0612773`.
