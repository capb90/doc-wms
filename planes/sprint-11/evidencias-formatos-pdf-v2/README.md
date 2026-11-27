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

## Fase 3 (BE) — 2026-11-27

BE en `f2/formatos-pdf-v2`, sobre la fase 2 (`bf61eac`). PDF del depósito v2 de importación, exportación e inspección (D13, D22, D28) y guía de salida v2, completa y por depósito (D14), con el encabezado y el pie comunes de D9, en carta (D24) y sin el sello «DOCUMENTO OFICIAL» (D25). Diseño de los mockups [`../qa-manual/pdf-deposito-v2/`](../qa-manual/pdf-deposito-v2/) y [`../qa-manual/formato-guia-v2/`](../qa-manual/formato-guia-v2/).

**Método.** Igual que en las fases 1 y 2: una prueba de integración temporal, que no se subió, llamó a `DepositPdfService` y `DispatchGuidePdfService` con el formato fijo en `V2` o en `LEGACY` (y, en la guía, con `GUIDE_CODE_TYPE` fijo en QR o en código de barras, con una clave de verificación de prueba generada en la corrida). En la misma corrida dibujó el legacy con una copia de los dos servicios de `bf61eac` («antes»). No se cambió ningún parámetro en la base local ni se entró al frontend (las contraseñas locales del README no sirven). El cambio por API (`PATCH` con token de Admin) lo cubre la prueba de integración que sí se sube, `PdfFormatParameterTests.DepositAndGuideFormat_V2_ChangeTheDepositPdfAndTheGuide`: con `V2` cambian el PDF del depósito de importación, exportación e inspección, la guía completa, la guía por depósito y la guía anulada, y llevan Inter y JetBrains Mono embebidas; con `LEGACY`, no.

Hubo dos fuentes:

- **Base local `wmsdb`:** el depósito de la QA `5f3749d2-…` (2026BA00013) y 2026INSP00001 (inspección, con un camión). **La base local no tiene guías de salida ni depósitos de exportación.**
- **Escenario en Testcontainers:** un depósito de exportación y uno de inspección con agencia de aduanas; dos depósitos de importación del mismo importador con un levante cada uno, una salida de los dos (guía con dos filas) y otra salida con su guía anulada.

Cada PDF v2 se guardó con su texto (`pdftotext -layout`, `.txt`) y la captura de cada página (`-N.png`, 100 ppp). El PDF del depósito ocupa una página; la guía, dos (las dos copias, como el legacy).

### QA-PV2-007: PDF del depósito de la QA en V2 (PASA)

[`fase-3/pv2-007-qa-deposito.v2.pdf`](fase-3/pv2-007-qa-deposito.v2.pdf) ([captura](fase-3/pv2-007-qa-deposito.v2-1.png)), frente a [`screen.png`](../qa-manual/pdf-deposito-v2/screen.png):

- **Encabezado y pie de D9:** montacargas, logotipo vectorial y raya oscura; abajo, «Depósito registrado el … impreso el …», la raya con «Descripción del Ingreso a Bodega», «Página 1 de 1» y la banda amarilla con los parámetros `COMPANY_*`.
- «Depósito No.» con 2026BA00013 en rojo y el Code 39 de hoy; a la derecha, «Fecha Hora Ingreso: 2026-11-26 13:36:36».
- **Bloques separados por rayas finas:** Importador COMERCIALIZADORA LUHOMAR S.A.S con «Codigo/Cedula/NIT: 874534-2 COL» y Dirección (`AJQ/` D19); Carta Porte PE000843 (2026-11-24) y Manifiesto I.C. 116575014469850 (2026-11-26); S.I.A. SURCOMEX S.A NIVEL 2 con NIT 345765-4; Transportadora.
- **Tabla:** FRIJOL EN GRANO · SACOS; los 3 pesajes PUB010, IBA2021 y XAI1204 con P. mercancía 32.020, 32.020 y 32.010 y sus tiquetes; Entrada 1.920, Ampara 1.920, Saldo 0 (`AJQ/` D19).
- **«TOTAL PESO (Kg): 96.050»** (es-CO, `DEC-082`).
- Unidad(es) de carga N/A, Observaciones, Responsable A.L. y Cuadrilla; firmas «Recibido por» (ADMINISTRADOR LOCAL, 123456789) y «Firma Conductor».

### QA-PV2-008: guía en V2 con QR (PASA, escenario)

[`fase-3/pv2-008-escenario-guia-qr.v2.pdf`](fase-3/pv2-008-escenario-guia-qr.v2.pdf) ([copia 1](fase-3/pv2-008-escenario-guia-qr.v2-1.png), [copia 2](fase-3/pv2-008-escenario-guia-qr.v2-2.png)), frente a [`screen.png`](../qa-manual/formato-guia-v2/screen.png):

- El mismo encabezado y pie del PDF del depósito; encima de la banda, «Guía generada el … impreso el …» y la línea de contacto.
- El QR a la izquierda con «Escanee para verificar esta guía»; «GUÍA DE SALIDA NO.» 2026S00001; a la derecha «FECHA HORA SALIDA». En la copia 2, el número lleva la placa con su país, como el legacy.
- Importador con identificación y dirección; Placas en su recuadro con el país; Tiquetes; Fecha ingreso de cada depósito; Conductores, Empresa de transporte y su identificación; Agencia de aduanas sin el rol repetido (`AJQ/` D20) y su identificación.
- Tabla con las 12 columnas de hoy, sin «Unidad» (`AJQ/` D7c); levante y aceptación en su píldora, uno por línea; «Cant. Sale» resaltada; «Total en esta salida 9,25».
- Unidades de carga, Observaciones, Responsable y Cuadrilla; Destino y «Vence: … en 3 días» resaltado; firmas «Firma Entrega» y la del firmante resuelto al emitir (aquí, el conductor).
- En el escenario, la salida no trae tiquetes y el «Doc / CPI» y la aceptación de prueba son más largos que los reales, así que se parten en dos líneas.

### QA-PV2-009: código de barras y PDF por depósito (PASA, escenario)

- [`pv2-009-escenario-guia-barras.v2`](fase-3/pv2-009-escenario-guia-barras.v2-1.png): con `GUIDE_CODE_TYPE = BARCODE`, el código de barras va en el lugar del QR.
- [`pv2-009-escenario-guia-por-deposito-1.v2`](fase-3/pv2-009-escenario-guia-por-deposito-1.v2-1.png): el PDF por depósito con el número 2026S00001-1, solo la fila y la fecha de ingreso de ese depósito.

### QA-PV2-010: guía anulada en V2 (PASA, escenario)

[`pv2-010-escenario-guia-anulada.v2`](fase-3/pv2-010-escenario-guia-anulada.v2-1.png): la marca de agua «ANULADA» en las dos copias, con el tamaño, el ángulo y el color del legacy.

### QA-PV2-013: PDF del depósito de exportación e inspección en V2 (PASA)

- **Exportación** (escenario): [`pv2-013-escenario-exportacion.v2`](fase-3/pv2-013-escenario-exportacion.v2-1.png), con la banda azul «MERCANCIA PARA EXPORTACION» bajo el número.
- **Inspección** (escenario): [`pv2-013-escenario-inspeccion.v2`](fase-3/pv2-013-escenario-inspeccion.v2-1.png), con la banda naranja «INSPECCION ADUANERA».
- **Inspección** (base local, 2026INSP00001): [`pv2-013-insp-2026INSP00001.v2`](fase-3/pv2-013-insp-2026INSP00001.v2-1.png), con «Sin cliente» y la banda naranja.
- La importación no lleva banda, como el mockup.
- Con sus datos de hoy: el PDF de exportación sigue rotulando «Importador:» al cliente, como el legacy.

### El legacy no cambia

Con `LEGACY` sale el mismo PDF de hoy ([`fase-3/legacy-comparacion.txt`](fase-3/legacy-comparacion.txt)). Los 8 pares «antes» (copia de los servicios de `bf61eac`) y «después» tienen el mismo texto y la misma imagen de cada página, a 100 ppp:

- el PDF del depósito de la QA;
- el de exportación e inspección del escenario;
- el de 2026INSP00001;
- y la guía en QR, en código de barras, por depósito y anulada.

Los archivos son `fase-3/pv2-*.antes.pdf` y `*.despues.pdf`. Los dibujos legacy (`Services/Pdf/Legacy*Renderer.cs`) no se tocaron.

### Decisiones de dibujo y colores

**Diferencias con el mockup, por D4 (gana el PDF de hoy):**

- El PDF del depósito conserva la columna **Embalaje** (F01 D18) y la rejilla paralela producto/pesaje del legacy (CE-1, D8). El mockup pone el embalaje entre paréntesis bajo el producto y une la celda del producto entre pesajes.
- La guía conserva **las dos copias** del legacy, con la placa en el número de la segunda.

**Otras diferencias con el mockup:**

- La banda de exportación e inspección va bajo el número y el código de barras: D13 y D22 no dicen dónde.
- Margen horizontal de 30 pt, el del legacy, para que la tabla de 12 columnas de la guía quepa en carta. En carta, los números, códigos, levantes y aceptaciones van en columnas fijas y en monoespaciada de 6 a 6,5 pt, y el producto se reparte en líneas. El mockup de la guía es A4.
- Sin cursivas: las fuentes embebidas son regular, semibold y bold (D10). El mockup pone en cursiva las placas y la línea «registrado / generado el …».
- La línea de contacto dice «guía», con tilde, como el mockup. El legacy dice «guia».

**Colores tomados de `code.html` que difieren de D10:**

- **Tabla del PDF del depósito:** bordes negros y raya entre filas `#b3b3b3` (`border-black` y `border-black/30`), no los grises de D10. Cabecera de «Pesajes» y «Cantidades» `#f8fafc` (`bg-slate-50/50`).
- **Tabla de la guía:** bordes `#1f2937` (`.doc-table`), cabecera `#f1f5f9`, Levante y Aceptación `#f8fafc`. «Cant. Sale» en `#fffbeb` (cabecera) y `#fef8dd` (celda). «Vence» en `#fef5d2` con borde `#fcd34d`. El ámbar no está en la paleta de D10.
- **Rótulos secundarios de la guía** («GUÍA DE SALIDA NO.», «FECHA HORA SALIDA:», el texto bajo el QR, la línea «Guía generada …»): `#475569` (slate-600), que no está en D10.
- **Banda del pie:** el mockup del depósito usa `#FDE047` (yellow-300) y el de la guía `#FACC15`. El pie es común (D9), así que se queda `#facc15`, el de D10 y la guía.
- El número del depósito `#e11d48` y la raya del encabezado `#0f172a` coinciden con D10.

### Compuertas (BE `190f56f`)

| Compuerta | Antes (`bf61eac`) | Después |
| --- | --- | --- |
| `dotnet build Wms.sln` | Sin errores | Sin errores |
| `Wms.Tests` | 2465 | 2475, con la guardia `NumberCultureGuardTests` (29) en verde |
| `Wms.IntegrationTests` | 892 | 893 |
| `has-pending-model-changes` | — | Limpio |

Las dos suites de antes corrieron en la misma sesión, sobre un worktree de `bf61eac`. No hubo fallas que dependan de la hora.

## Fase 4 (BE y docs) — 2026-11-27

BE en `f2/formatos-pdf-v2`, sobre la fase 3 (`190f56f`), y después fusionado en `fase-2` (`996828e`).

### QA-PV2-011: de vuelta a LEGACY, sin desplegar (PASA, por API)

**Método.** Una prueba de integración temporal, que no se subió, usó el API de las pruebas de integración con un token de Admin para los parámetros y uno de Comercio Exterior para las descargas. Las contraseñas locales del README no sirven, así que no se entró al frontend. El escenario de Testcontainers tenía:

- un depósito de importación con un levante, una salida y su guía;
- un depósito de exportación y uno de inspección.

Los pasos fueron tres, sin reiniciar el API:

1. Los tres parámetros en `LEGACY` (el valor de la semilla): se descargaron los documentos («legacy-antes»).
2. Los tres en `V2` por `PATCH`: se descargaron otra vez («v2»).
3. Los tres de vuelta en `LEGACY` por `PATCH`: se descargaron otra vez («legacy-despues»).

En cada paso se descargaron la etiqueta, la tarjeta por vehículo, el PDF del depósito y la guía de importación, más el PDF del depósito de exportación y la etiqueta de inspección. Cada `PATCH` respondió 200 y cada descarga, 200 `application/pdf` ([`fase-4/pv2-011-api.log`](fase-4/pv2-011-api.log)).

**Resultado** ([`fase-4/pv2-011-comparacion.txt`](fase-4/pv2-011-comparacion.txt)):

- En `V2`, los seis PDF llevan las fuentes v2 y su texto es otro.
- De vuelta en `LEGACY`, ninguno las lleva. Salen con el mismo texto (`pdftotext -layout`) y la misma imagen de cada página (100 ppp) que en el paso 1.
- La única diferencia es el último dígito de los segundos de «impreso el …» en el PDF del depósito, el de exportación y las dos copias de la guía: una zona de 7 × 10 píxeles.

**Archivos.** En `fase-4/`, `pv2-011-<documento>.<paso>.pdf` con su texto (`.txt`), y la captura de la primera página de «legacy-despues» y de «v2» (`-1.png`). Los documentos son `etiqueta`, `tarjeta`, `deposito`, `guia`, `exp-deposito` e `insp-etiqueta`.

**Base local.** Al cerrar, `wmsdb` tiene los tres parámetros en `LEGACY`, activos, y la migración `20261127060211_AddPdfFormatParameters` aplicada. Ninguna fase cambió los parámetros de la base local.

### Compuertas (BE `fase-2` `996828e`, después de la fusión)

| Compuerta | Antes (`190f56f`, fase 3) | Después (`fase-2` `996828e`) |
| --- | --- | --- |
| `dotnet build Wms.sln` | Sin errores | Sin errores |
| `Wms.Tests` | 2475 | 2475, con la guardia `NumberCultureGuardTests` (29) en verde |
| `Wms.IntegrationTests` | 893 | 893 |
| `has-pending-model-changes` | Limpio | Limpio; `20261127060211_AddPdfFormatParameters` aplicada en la base local |

La fase 4 no agrega pruebas: la prueba temporal de QA-PV2-011 se borró antes de fusionar.
