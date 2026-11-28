# Evidencias — Formatos de PDF del cliente

Plan: [`../plan-cerrado-f2-formatos-pdf-cliente-2026-11-27.md`](../plan-cerrado-f2-formatos-pdf-cliente-2026-11-27.md). Diseños del cliente: [`../qa-manual/formatos-pdf/`](../qa-manual/formatos-pdf/).

## Fase 1 (BE) — 2026-11-27

BE `c764750` en `f2/formatos-pdf-cliente`, desde `fase-2` `a81b99c` (con F06 integrada).

**Método.** Un arnés temporal, que no se subió: una aplicación de consola que usa `LabelGenerationService` contra la base local `wmsdb`, con el formato fijo (`LEGACY` o `V2`) y la acción «imprimir», como el frontend. No registra la impresión. Generó la etiqueta y la tarjeta por vehículo (el primer camión) de cuatro depósitos:

- **2026BA00013**: depósito de la QA de F05, con dos levantes y 6 impresiones de la etiqueta registradas;
- **2026BA00008**: sin levantes y sin intermediario;
- **2026BA00003**: con una unidad de carga;
- **2026INSP00001**: inspección, con camión.

La base local no tiene depósitos de exportación. La etiqueta y la tarjeta de exportación se dibujaron con los datos de 2026BA00003: `GET exports/{id}/label` no valida la modalidad. La prueba de integración `PdfFormatParameterTests` cubre un depósito de exportación real.

### El legacy no cambia (PASA)

Los 14 PDF legacy de esos cuatro depósitos se generaron dos veces: con el código de `fase-2` `a81b99c`, antes de tocarlo, y con el de la fase 1. Cada par se comparó con `pdftotext -layout` y con la imagen de cada página (`pdftoppm`, 100 ppp), byte a byte. Los 14 tienen el mismo texto y la misma imagen ([`fase-1/legacy-comparacion.txt`](fase-1/legacy-comparacion.txt)).

Una prueba unitaria comprueba además que el legacy ignora los datos nuevos: el número de impresión y las filas de levantes.

### QA-PC-001: etiqueta nacionalizada (PASA)

[`fase-1/pc-001-cliente-vs-v2.png`](fase-1/pc-001-cliente-vs-v2.png): a la izquierda, el diseño del cliente; a la derecha, la etiqueta v2 de 2026BA00013.

- Carta, Barlow, el logotipo del cliente, «DEPÓSITO NO.», el número en rojo y el Code 128 con el número espaciado.
- Banda verde «MERCANCÍA NACIONALIZADA».
- La tabla No. aceptación · Fecha · Levante No. · Fecha, con una fila por levante: 372024000009520 con sus fechas y el segundo levante de la base local.
- «Impresión # 7»: las 6 impresiones registradas de la etiqueta más la actual (D16).

La prueba de integración `VehicleLabelTests.PrintNumber_CountsOnlyThePrintsOfThatLabelOrCard` comprueba el conteo por el API: dos impresiones y una descarga de la etiqueta, y una impresión de la tarjeta. Cuenta solo las impresiones de esa etiqueta o de esa tarjeta, y la descarga actual no suma.

Las diferencias con la imagen del cliente son de datos:

- Ampara y Saldo son los de la base local.
- El manifiesto no tiene fecha en la base local: el legacy imprime `116575014469850(N/A)` y el v2 no repite «N/A» debajo.

Archivos: `pc-001-qa-etiqueta.v2.pdf`, `.png` y `.txt`.

### QA-PC-002: etiqueta sin levantes (PASA)

[`fase-1/pc-002-cliente-vs-v2.png`](fase-1/pc-002-cliente-vs-v2.png): el diseño del cliente y la etiqueta v2 de 2026BA00008. Banda roja «MERCANCÍA SIN NACIONALIZAR», sin la tabla de nacionalización e «Impresión # 1».

Archivos:

- `pc-002-sin-levantes-etiqueta.v2.*`: 2026BA00008. Sin intermediario, su lugar queda en blanco y cada dato sigue en la columna del diseño.
- `pc-002-con-unidades-etiqueta.v2.*`: 2026BA00003. Con su unidad de carga en una tercera fila del recuadro.

### QA-PC-003: tarjeta por vehículo (PASA)

`pc-003-qa-tarjeta.v2.*`: la tarjeta del primer camión de 2026BA00013. Es el diseño de la etiqueta con:

- «PLACA» PUB010;
- la tabla «Cant. ingresa» · «Mercancía», sin Ampara ni Saldo;
- el manifiesto;
- la banda verde y la tabla de levantes del depósito;
- «Impresión # 7»: las 6 impresiones registradas de esa tarjeta más la actual.

### QA-PC-004: exportación e inspección (PASA)

El diseño de la etiqueta con sus datos de hoy:

- `pc-004-exportacion-etiqueta.v2.*` y `pc-004-exportacion-tarjeta.v2.*`: banda azul «MERCANCÍA PARA EXPORTACIÓN» y «EXPORTADOR». El depósito no tiene documentos adicionales; las pruebas unitarias dibujan dos. La tarjeta lleva la unidad de carga del camión.
- `pc-004-inspeccion-etiqueta.v2.*` y `pc-004-inspeccion-tarjeta.v2.*`: banda naranja «INSPECCIÓN ADUANERA», con importador y exportador.

### Decisiones de dibujo

Para que el usuario las revise:

- **Medidas.** Las de los `*.dc.html`, a 0,75 pt por px (816 px = 612 pt, el ancho de la carta).
- **Código de barras.** Deja en blanco 10 de los 165 módulos del diseño a cada lado (`viewBox="-10 0 165 1"`).
- **Filas.** Con varias filas, las tablas llevan una raya `#E2E8F0` entre ellas. El diseño solo tiene una fila.
- **Lugar del intermediario.** Sin intermediario y con una sola parte, su lugar queda en blanco. El legacy no escribe nada.
- **Unidades de carga.** El diseño no las trae. Salen en el recuadro solo con valor, como en el legacy (`AJQ/` D17).
- **Textos de la banda.** Llevan tildes, como el diseño. El legacy conserva los suyos, sin tildes.
- **Descargas.** Una descarga (`action=download`) muestra las impresiones ya registradas, sin sumar la actual (usuario, 2026-11-27).

### Compuertas

Sobre `f2/formatos-pdf-cliente` `c764750`, antes y después (la base se midió en `fase-2` `a81b99c`, en otro checkout):

- `dotnet build Wms.sln`: sin errores, antes y después.
- `Wms.Tests`: 2547 → 2563, todo en verde. La guardia `NumberCultureGuardTests` pasa con 29 en los dos.
- `Wms.IntegrationTests`: 916 → 917, todo en verde. La prueba nueva es la del número de impresión.
- `dotnet ef migrations has-pending-model-changes`: sin cambios (no hay migración).

## Fase 2 (BE) — 2026-11-28

BE `471aefe` en `f2/formatos-pdf-cliente`, sobre la fase 1 (`c764750`).

**Método.** Un arnés temporal, que no se subió: una aplicación de consola que usa `DepositPdfService` contra la base local `wmsdb`, con el formato fijo (`LEGACY` o `V2`). Generó el PDF de diez depósitos:

- **2026BA00013**: el depósito de la QA de F05, con tres camiones de un producto;
- **2026BA00001** y **2026BA00003**: un camión con dos productos;
- **2026BA00002**, **2026BA00008** y **2026BA00009**: de importación, uno sin P. mercancía;
- **2026EXP00001**: exportación (la base local ya tiene uno);
- **2026INSP00001** y **2026INSP00006**: inspección;
- **2026INSP00007**: inspección con un camión que no declara productos.

### El legacy no cambia (PASA)

Los 10 PDF legacy se generaron con el código de la fase 1, antes de tocarlo, y con el de la fase 2. Cada par se comparó con `pdftotext -layout` y con la imagen de cada página (`pdftoppm`, 100 ppp), píxel a píxel: los 10 tienen el mismo texto y la misma imagen ([`fase-2/legacy-comparacion.txt`](fase-2/legacy-comparacion.txt)).

- La línea «Depósito registrado el …, impreso el …» se enmascara: la hora de impresión cambia en cada corrida y, como la línea va centrada, se corre con el ancho de sus dígitos. Por eso el texto se compara también con los espacios normalizados.
- Una prueba negativa (el PDF legacy frente al v2) da «texto distinto, imagen distinta».
- Una prueba unitaria comprueba además que el legacy ignora los datos nuevos: los pesajes de cada producto y los camiones sin productos.

### QA-PC-005: PDF del depósito de la QA (PASA)

[`fase-2/pc-005-cliente-vs-v2.png`](fase-2/pc-005-cliente-vs-v2.png): a la izquierda, el diseño del cliente; a la derecha, el PDF v2 de 2026BA00013.

- Carta, Barlow, el logotipo, «DEPÓSITO NO.», el número en rojo, el código de barras y «FECHA HORA INGRESO».
- El recuadro Importador · S.I.A. / Intermediario · Transportadora, con Carta porte, Manifiesto I.C. y sus fechas.
- La tabla Producto · Pesajes · Cantidades: FRIJOL EN GRANO (SACOS) con sus tres camiones, cada uno con Cant. 640, su P. mercancía (32.020, 32.020 y 32.010) y su tiquete; Entrada 1.920, Ampara 1.920 y Saldo 0, unidos a lo alto de los camiones.
- «TOTAL PESO (KG)» 96.050 (es-CO, D18).
- Observaciones en su recuadro y Responsable, sin Cuadrilla (D19).
- «RECIBIDO POR» con el nombre y la identificación del responsable, y «FIRMA CONDUCTOR», al pie de la hoja.
- El pie del cliente: «Depósito registrado el …, impreso el …», «Página 1 de 1» y la banda naranja.

Las diferencias con la imagen son de datos: la dirección del importador y la fecha del manifiesto están vacías en la base local.

Archivos: `pc-005-qa-deposito.v2.pdf`, `.png` y `.txt`.

### QA-PC-011: un camión con dos productos (PASA)

[`fase-2/pc-011-cliente-vs-v2.png`](fase-2/pc-011-cliente-vs-v2.png): el diseño del cliente y el PDF v2 de 2026BA00003.

- El camión QAI051 aparece bajo LENTEJA QA I05 (CAJAS) con Cant. 5 y bajo ARROZ con Cant. 12, con el mismo Peso kg (20.000) y el mismo tiquete (2026T00003).
- «TOTAL PESO (KG)» 20.000: cuenta el camión una vez, como el legacy del mismo depósito (`TOTAL PESO (Kg): 20.000`) y como el legacy de 2024BA1443 (D18).
- `pc-011-camion-dos-productos-2.v2.*`: 2026BA00001, el camión ABC122 con 8 y 2, 17.700 kg en cada fila y total 17.700, igual al legacy.

### QA-PC-006: exportación e inspección (PASA)

- [`fase-2/pc-006-cliente-vs-exportacion.png`](fase-2/pc-006-cliente-vs-exportacion.png) y `pc-006-exportacion.v2.*`: 2026EXP00001, con la banda azul «MERCANCÍA PARA EXPORTACIÓN» sobre el recuadro.
- [`fase-2/pc-006-cliente-vs-inspeccion.png`](fase-2/pc-006-cliente-vs-inspeccion.png) y `pc-006-inspeccion.v2.*`: 2026INSP00001, con la banda naranja «INSPECCIÓN ADUANERA». En la inspección, Ampara y Saldo van en blanco, como hoy.
- `pc-006-inspeccion-camion-sin-producto.v2.*`: 2026INSP00007, sin productos; su camión QAF407 va al final de la tabla, sin producto.

### Decisiones de dibujo

Para que el usuario las revise:

- **Medidas.** Las del `*.dc.html`, a 0,75 pt por px, con una excepción: «Peso Kg.» pasa de 96 a 88 px y «Tiquete» de 84 a 92 px, para que los tiquetes de 10 caracteres (`2026T00020`) quepan en una línea.
- **Código de barras.** Sigue siendo el Code 39 del PDF del depósito (el legacy y el v2 imprimen la misma imagen). Ocupa el recuadro de 170 × 30 px del diseño, estirado como su SVG. El diseño trae un Code 128, más corto: en ese ancho, las barras finas del Code 39 quedan de unos 0,19 mm.
- **Pesajes de cada producto (D18).** Una fila por camión no anulado que declara el producto, en el orden de las entradas. Si un camión no trae la cantidad de ese producto, Cant. va en blanco.
- **Camiones sin productos.** Van al final de la tabla, sin producto y sin cantidades, para que la tabla muestre todos los pesos que suma el total. El legacy no los muestra.
- **Entre productos**, una raya `#CBD5E1`; entre los camiones de un producto, una `#E2E8F0`. El diseño solo tiene un producto.
- **Unidades de carga.** El diseño no las trae. Salen junto a Responsable solo con valor, como en la etiqueta de la fase 1.
- **Firmas.** Al pie de la última hoja, como el `margin-top: auto` del diseño. Si no caben, pasan a una hoja nueva.
- **Banda de exportación e inspección.** Encima del recuadro de las partes, con los textos con tilde de la etiqueta.

### Compuertas

Sobre `f2/formatos-pdf-cliente` `471aefe`, antes (sobre `c764750`) y después:

- `dotnet build Wms.sln`: sin errores, antes y después.
- `Wms.Tests`: 2563 → 2568, todo en verde. La guardia `NumberCultureGuardTests` pasa con 29 en los dos. Las nuevas prueban los pesajes de cada producto (con el caso de 2024BA1443), el dibujo con un camión bajo dos productos y en varias hojas, y que el legacy ignora los datos nuevos.
- `Wms.IntegrationTests`: 917 → 917, todo en verde. `PdfFormatParameterTests` espera ahora Barlow en el PDF del depósito v2 (las guías siguen en Inter hasta la fase 3).
- `dotnet ef migrations has-pending-model-changes`: sin cambios (no hay migración).
