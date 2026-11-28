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
