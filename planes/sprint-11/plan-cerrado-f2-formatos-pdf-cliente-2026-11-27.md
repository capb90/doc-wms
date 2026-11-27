# Plan cerrado — Fase 2 · Formatos de PDF del cliente: etiqueta, PDF del depósito y guía de salida

> **Fecha:** 27 de noviembre de 2026. **Estado:** Borrador, pendiente de la aprobación del usuario. Preguntas en §9.
> **Origen:** el cliente revisó los formatos v2 del plan [`plan-cerrado-f2-formatos-pdf-v2-2026-11-26.md`](plan-cerrado-f2-formatos-pdf-v2-2026-11-26.md) (`PV2/`), ejecutado y fusionado en `fase-2` el 2026-11-27 con los tres parámetros en `LEGACY`, y pidió cambiarlos. Sus formatos están en [`qa-manual/formatos-pdf/`](qa-manual/formatos-pdf/) (`CL/`), en cinco carpetas con una imagen (`*.png`) y el diseño (`*.dc.html`, con medidas y colores en sus `style="…"`): `etiqueta-nacionalizada/`, `etiqueta-sin-nacionalizar/`, `pdf-deposito/`, `guia-salida-qr/` y `guia-salida-cod-barras/`. Los llamó «Formato actual mejorado» y «Guía de salida – Definitiva». El usuario los entregó el 2026-11-27.
> **Base:** BE `fase-2` `996828e` (con `PV2/`, `DEC-082` y los ajustes de la QA de F05 fusionados) · FE `fase-2` `8884936` · docs `main` `f98bd7b`.
> **Alcance:** backend y docs. Se rehace el dibujo v2 de `PV2/` con los diseños del cliente, sobre los mismos registros de datos (`PV2/` D8) y los mismos parámetros (`PV2/` D6). Los legacy no cambian. Sin cambios de contrato ni de frontend, y sin migración, salvo lo que decidan P1 y P5.
> **Rutas:** relativas a `code_workspace/`. Prefijos: `B/` = `Backend/wms-api/`; `BS/` = `B/Wms.Application/ForeignTrade/Common/Services/`; `D/` = `docs/`; `PV2/` = el plan de formatos v2; `CL/` = `D/planes/sprint-11/qa-manual/formatos-pdf/`; `L/` = `bodegas-legacy/`.

---

## 0. Instrucciones para el ejecutor

1. **Lecturas mínimas:** `AGENTS.md` del backend, `D/procesos/flujo-de-trabajo-agentes.md`, `D/contexto/decisiones.md` `DEC-060` y `DEC-082`, `PV2/` completo (en especial D6 a D14, D21 a D28 y §10) y este plan. De `CL/`, las cinco imágenes y, para medidas y colores, los `*.dc.html`.
2. **Ramas y git:** `f2/formatos-pdf-cliente` en BE, desde `fase-2`. Commit y push al cerrar cada fase, con el mensaje de §7. Al cerrar la última fase, fusión en `fase-2` con `--no-ff` y push. Sin `push --force`. Para borrar, `rm`.
3. **Una fase por turno** (`AGENTS.md`): al cerrar cada una, compuertas, commit, estado en este plan (§4) y en la matriz, y reporte.
4. **Líneas citadas:** son de la base. Confírmalas con grep; si el código no coincide, pregunta en un solo mensaje.
5. **Descargas:** la fuente de D3 se descarga solo con el permiso del usuario, pedido en la sesión con el archivo, la fuente oficial y el tamaño.
6. **Verificación:** como en `PV2/`: el PDF v2 y la captura de cada página, comparados con la imagen del cliente; el legacy, idéntico antes y después con `pdftotext` y la imagen de cada página. Si las contraseñas locales no funcionan, por API con un token de las pruebas de integración o con una prueba temporal que no se sube. Evidencias en `D/planes/sprint-11/evidencias-formatos-pdf-cliente/`.

---

## 1. Decisiones

### 1.1 Del usuario y del cliente

| # | Decisión | Fuente |
| --- | --- | --- |
| D1 | **Los formatos del cliente reemplazan los diseños v2 de `PV2/`.** Se replican fielmente las cinco imágenes de `CL/` (medidas, colores, tipografía y orden de los bloques), con los datos reales de cada documento | Usuario, 2026-11-27 («El cliente revisó los formatos nuevos V2, y pidieron cambiarlos») |
| D2 | **Lo que no cambia de `PV2/`:** los parámetros `LABEL_FORMAT`, `DEPOSIT_PDF_FORMAT` y `DISPATCH_GUIDE_FORMAT` y su valor inicial `LEGACY` (`PV2/` D6, D21); los legacy; los registros de datos (`PV2/` D8); los números en es-CO (`DEC-082`): la imagen del cliente muestra `26000` y `13000`, el PDF imprime `26.000` y `13.000`; la marca de agua «ANULADA» de la guía (`PV2/` D14), que la imagen no muestra | `PV2/`; `DEC-082` |

### 1.2 Elementos comunes

| # | Decisión | Base |
| --- | --- | --- |
| D3 | **Tipografía Barlow** (licencia SIL OFL), la de los diseños del cliente (`font-family: Barlow`, pesos 400, 500, 700 y 800 en las etiquetas). Sus `.ttf` se embeben en `B/Wms.Application/Common/Resources/Fonts/` con su licencia y se registran al iniciar, como Inter y JetBrains Mono (`PV2/` D10). Inter y JetBrains Mono se retiran si ningún v2 las usa | `CL/*.dc.html`; P6 |
| D4 | **Logotipo:** la imagen única del cliente (`CL/*/assets/3f43311559d5bac477856b68e3ac9088.png`, 1187 × 210, montacargas y «BODEGAS ASOCIADAS LTDA.» con NIT y «DEPÓSITO HABILITADO COD. 22080»), dibujada a 260 × 46 px, reemplaza el montacargas y el SVG de `PV2/` D9. Se copia a `B/Wms.Application/Common/Resources/Pdf/` con un nombre legible | `CL/` |
| D5 | **Encabezado:** logotipo a la izquierda; a la derecha, el rótulo del documento («DEPÓSITO NO.» o «GUÍA DE SALIDA NO.»), el número en rojo (`#DC2626`) y el código (barras debajo del número en la etiqueta, el depósito y la guía con barras; QR a la derecha del número en la guía con QR). Debajo, una raya `#CBD5E1` de ancho completo | `CL/` |
| D6 | **Pie del PDF del depósito y de la guía:** una línea gris con «Depósito registrado el … , impreso el …» o «Guía generada el … , impreso el …» a la izquierda y, a la derecha, «Página X de Y» (depósito) o la línea de contacto (guía); debajo, la banda naranja `#FFA500` de ancho completo con `CompanyInfo.FooterAddressLine` y `FooterEmailLine` (CHG-84), como hoy. La etiqueta no lleva pie | `CL/`; `PV2/` D9 |
| D7 | **Estilo:** paleta pizarra de los diseños (títulos `#0F172A`, texto `#334155`, rótulos `#475569`, bordes `#CBD5E1`, divisiones `#E2E8F0`), bloques de borde fino con esquinas redondeadas, rótulos en mayúscula y negrita, fechas `yyyy-MM-dd` y horas `HH:mm:ss`. Página carta en el depósito y la guía (816 × 1056 px de los diseños) | `CL/` |

### 1.3 Contenido de cada formato

| # | Decisión | Base |
| --- | --- | --- |
| D8 | **Etiqueta del depósito** (`CL/etiqueta-nacionalizada/`, `CL/etiqueta-sin-nacionalizar/`): <br>• encabezado de D5 con código de barras y el texto del número espaciado debajo; <br>• recuadro de tres columnas: Importador, Intermediario, Fecha ingreso (fecha y hora); Carta porte con su fecha debajo, Manifiesto No. con su fecha debajo, Placa(s) separadas por coma; <br>• tabla Ampara · Saldo · Mercancía (la de hoy, `BS/Pdf/LabelAmparaTable.cs`), con la mercancía y su embalaje entre paréntesis; <br>• banda de estado: verde `#047857` «MERCANCÍA NACIONALIZADA» o roja `#B91C1C` «MERCANCÍA SIN NACIONALIZAR» (con tilde, como el diseño); <br>• con levantes, tabla No. aceptación · Fecha · Levante No. · Fecha, una fila por levante (hoy el texto corrido de `BS/Pdf/LabelNationalizationText.cs`); <br>• «Impresión # N» a la derecha, al final (P5). <br>Tamaño: P2 | `CL/` |
| D9 | **Tarjeta por vehículo, etiqueta y tarjeta de exportación e inspección:** no tienen diseño del cliente (P3, P4) | `PV2/` D12, D22, D27 |
| D10 | **PDF del depósito** (`CL/pdf-deposito/`): <br>• encabezado de D5 con código de barras y, debajo, «FECHA HORA INGRESO»; <br>• recuadro de tres columnas: **Importador** (nombre, Código/Cédula/NIT con país, Dirección); **S.I.A. / Intermediario** (nombre, Identificación SIA); **Transportadora** (nombre; Carta porte y Fecha carta porte; Manifiesto I.C. # y Fecha del M.I.C.); <br>• «DESCRIPCIÓN DEL INGRESO A BODEGA»: tabla Producto · Pesajes (Placa, Cant., Peso kg, Tiquete) · Cantidades (Entrada, Ampara, Saldo), con la celda del producto y la de sus cantidades unidas a lo alto de sus pesajes (P7); <br>• «TOTAL PESO (KG)» a la derecha; <br>• Observaciones en un recuadro; Responsable y Cuadrilla (P8); <br>• dos firmas: «RECIBIDO POR» con nombre e identificación del responsable, y «FIRMA CONDUCTOR»; <br>• pie de D6. <br>Exportación e inspección: P4 | `CL/`; `PV2/` D13 |
| D11 | **Guía de salida** (`CL/guia-salida-qr/`, `CL/guia-salida-cod-barras/`): <br>• encabezado de D5 con «FECHA HORA SALIDA»; QR o código de barras según `GUIDE_CODE_TYPE` (`DEC-060`); <br>• recuadro de tres columnas: **Importador** (nombre, Código/Cédula/NIT, Dirección); **S.I.A. / Intermediario** (nombre, Identificación SIA); **Empresa transporte** (nombre; Placas con país y Tiquetes; Conductores con identificación); <br>• tabla No. · Producto (embalaje debajo, en gris) · Doc / CPI · Depósito · Manifiesto · Levante · Aceptación · Cantidades; levantes y aceptaciones de un producto, uno debajo de otro; cantidades apiladas: Entrada, Saldo ante., Sale, Nvo. saldo; <br>• «TOTAL EN ESTA SALIDA» a la derecha; <br>• recuadro: Contenedor(es) como etiquetas, Observaciones, Responsable, Cuadrilla, Destino y Vence («fecha en N días»); <br>• dos firmas: «FIRMA ENTREGA» con nombre e identificación de quien la generó, y «FIRMA IMPORTADOR» con el firmante de hoy (`DispatchGuidePdfData.SignerName`); <br>• pie de D6, con la línea «Para mayor información de esta guía favor llamar al …» de hoy. <br>• Guía por depósito: el mismo diseño con el número con sufijo. Copias: P9 | `CL/`; `PV2/` D14 |

---

## 2. Contrato

Ningún contrato cambia. Si P5 se resuelve contando impresiones, el número sale de `WarehouseStorageLabelPrints` (`BS/LabelGenerationService.cs:415`), sin migración.

---

## 3. Archivos que se tocan

**Backend:**
- `BS/Pdf/V2/*` (dibujo v2): `V2LabelRenderer.cs`, `V2DepositPdfRenderer.cs`, `V2DispatchGuidePdfRenderer.cs`, `V2DocumentHeader.cs`, `V2DocumentFooter.cs`, `V2DocumentParts.cs`, `V2Style.cs`, `V2Fonts.cs` y `V2PdfAssets.cs`.
- Los registros de datos de `BS/Pdf/` solo donde D8, D10 y D11 piden un dato que hoy no traen: levantes y aceptaciones por fila con su fecha (D8), cantidad del producto por pesaje (D10) y, según P5, el número de impresión. Su relleno en `BS/LabelGenerationService.cs`, `BS/DepositPdfService.cs` y `BS/DispatchGuidePdfService.cs`. El legacy no lee los datos nuevos.
- `B/Wms.Application/Common/Resources/Fonts/` (Barlow y su licencia) y `Resources/Pdf/` (logotipo de D4).
- Pruebas: `PdfV2LabelTests`, `PdfV2DocumentTests` y `PdfFormatParameterTests`, ajustadas a los diseños nuevos.

**Docs:** este plan, `DEC-060` (descripción del v2), `D/contexto/estado.md`, `D/planes/README.md`, la matriz y los casos en `D/qa/`.

---

## 4. Fases

| Fase | Repo | Contenido | Cierre | Estado |
| --- | --- | --- | --- | --- |
| 1 | BE | D3 a D9: fuente, logotipo, encabezado y pie; etiqueta del depósito, tarjeta por vehículo y las de exportación e inspección | Compuertas BE; QA-PC-001 a 004 en PASA | Pendiente |
| 2 | BE | D10: PDF del depósito (importación, exportación e inspección) | Compuertas BE; QA-PC-005 y 006 en PASA | Pendiente |
| 3 | BE | D11: guía de salida (QR, barras, por depósito y anulada) | Compuertas BE; QA-PC-007 a 009 en PASA | Pendiente |
| 4 | BE y docs | Casos a `D/qa/`; `DEC-060`, estado; fusión de `f2/formatos-pdf-cliente` en `fase-2` | QA-PC-010 en PASA; fusión con push | Pendiente |

---

## 5. Pruebas y casos QA

**Backend:** las pruebas de `PV2/` §5 siguen y se ajustan a los textos nuevos; además, una prueba pura por cada dato nuevo de los registros (levantes por fila, cantidad por pesaje y, si aplica, número de impresión), y que el legacy no cambie con ellos.

| Caso | Pasos | Resultado esperado |
| --- | --- | --- |
| QA-PC-001 | `LABEL_FORMAT` = `V2`: etiqueta del depósito de la QA de F05 (2026BA00013) | Como `CL/etiqueta-nacionalizada/`: banda verde y la tabla de aceptación y levante 372024000009520 con sus fechas |
| QA-PC-002 | Lo mismo con un depósito sin levantes | Como `CL/etiqueta-sin-nacionalizar/`: banda roja, sin tabla de nacionalización |
| QA-PC-003 | Tarjeta por vehículo de un camión del depósito de la QA | Según P3 |
| QA-PC-004 | Etiqueta y tarjeta de exportación y de inspección | Según P4 |
| QA-PC-005 | `DEPOSIT_PDF_FORMAT` = `V2`: PDF del depósito de la QA | Como `CL/pdf-deposito/`; total de peso 96.050 (es-CO) |
| QA-PC-006 | PDF de un depósito de exportación y de uno de inspección | Según P4 |
| QA-PC-007 | `DISPATCH_GUIDE_FORMAT` = `V2`, `GUIDE_CODE_TYPE` = `QR`: guía de una salida con dos o más productos | Como `CL/guia-salida-qr/` |
| QA-PC-008 | La misma guía con `GUIDE_CODE_TYPE` = `BARCODE`, y su PDF por depósito | Como `CL/guia-salida-cod-barras/`; número con sufijo en la guía por depósito |
| QA-PC-009 | Una guía anulada en `V2` | Marca de agua «ANULADA» |
| QA-PC-010 | Los tres parámetros en `LEGACY` | Los legacy, idénticos a los de antes del plan |

---

## 6. Compuertas de cada fase

- `dotnet build Wms.sln` sin errores; `dotnet test Wms.Tests` (con `NumberCultureGuardTests`) y `dotnet test Wms.IntegrationTests` en verde, con las cifras antes y después; `dotnet ef migrations has-pending-model-changes` limpio.
- PDF y capturas de los casos de la fase, junto a la imagen del cliente.

---

## 7. Commits

| Fase | Repo | Mensaje |
| --- | --- | --- |
| 1 | BE | `feat(pdf): etiqueta y tarjeta con el formato del cliente (DEC-060, formatos v2)` |
| 2 | BE | `feat(pdf): PDF del depósito con el formato del cliente (DEC-060, formatos v2)` |
| 3 | BE | `feat(pdf): guía de salida con el formato del cliente (DEC-060, formatos v2)` |
| 4 | docs | `docs(pdf): formatos del cliente en el v2; DEC-060` |

Fusión: `f2/formatos-pdf-cliente` en `fase-2`, con `--no-ff`, al cerrar la fase 4.

---

## 8. Riesgos

| # | Riesgo | Mitigación |
| --- | --- | --- |
| R1 | La tabla de la guía no cabe en carta con productos de nombres largos o varios levantes | El diseño ya parte el texto en varias líneas; QA-PC-007 con tres productos |
| R2 | Un camión con varios productos repite su peso en la tabla del depósito | P7 |
| R3 | El cambio de la tabla de levantes de la etiqueta toca datos que también lee el legacy | Los datos nuevos son aditivos y el legacy se compara antes y después (QA-PC-010) |
| R4 | Un dato del diseño no existe en el sistema | P8 (cuadrilla del depósito); cualquier otro, se pregunta antes de inventarlo |

---

## 9. Preguntas pendientes

| # | Pregunta | Recomendación |
| --- | --- | --- |
| P1 | **¿Los formatos del cliente reemplazan el v2 o se agregan como un tercer formato (`V3`)?** | **Reemplazar el v2.** Nunca se activó (los tres parámetros siguen en `LEGACY`) y el cliente lo descartó; sumar `V3` deja un formato muerto y obliga a otra migración |
| P2 | **Tamaño de la etiqueta:** el diseño del cliente es carta; la etiqueta de hoy (legacy y v2) es A5 vertical (`PV2/` D24) | **A5, como hoy**, con el diseño escalado: el contenido ocupa menos de la mitad de la hoja carta y cabe en A5, y no obliga a cambiar el papel de las etiquetas. Si el cliente la imprime en carta, carta |
| P3 | **Tarjeta por vehículo:** no tiene diseño | **El diseño de la etiqueta (D8)** con la placa del vehículo, «Cant. ingresa» y «Mercancía» de sus filas sin Ampara ni Saldo (`PV2/` D27), el manifiesto DIAN y la tabla de nacionalización |
| P4 | **Exportación e inspección** (etiqueta, tarjeta y PDF del depósito): no tienen diseño | **Los diseños de D8 y D10 con sus datos de hoy** y su banda: azul «MERCANCÍA PARA EXPORTACIÓN» y naranja «INSPECCIÓN ADUANERA» (`PV2/` D22, D28) |
| P5 | **«Impresión # N» de la etiqueta:** es un dato nuevo. Hoy cada impresión o descarga de una etiqueta queda en `WarehouseStorageLabelPrints` con su acción | **N = las veces que se imprimió esa etiqueta, contando la actual** (registros de esa etiqueta, o de esa tarjeta por vehículo, con la acción de imprimir). Si las descargas también deben contar, se cuentan todos los registros |
| P6 | **Fuente:** Barlow no está en el equipo; hay que descargarla (Google Fonts, `github.com/google/fonts`, licencia OFL). La banda naranja del diseño usa Arial, que no se puede embeber | **Descargar Barlow** (con tu permiso al ejecutar) **y usarla también en la banda naranja**, para no depender de las fuentes del servidor |
| P7 | **Pesajes con varios productos en un camión:** la tabla agrupa los pesajes por producto, pero el peso es del camión | **Cant. = la cantidad de ese producto en el camión; Peso kg = el peso del camión en cada fila donde aparece; el total cuenta cada camión una vez** (96.050 en el depósito de la QA) |
| P8 | **Cuadrilla del PDF del depósito:** el diseño la muestra («Sin Cuadrilla»), pero el ingreso no guarda cuadrilla (solo la salida, `B/Wms.Domain/Entities/Warehouse/GoodsExit.cs:47`) | **Quitar «Cuadrilla» del PDF del depósito**: sin dato, siempre diría «Sin cuadrilla». Registrarla en el ingreso sería otro cambio, con pantalla y migración |
| P9 | **Copias de la guía:** la guía de hoy (legacy y v2) imprime dos copias en la hoja; el diseño del cliente, una | **Una copia, como el diseño del cliente** («Definitiva»), con las dos firmas; si hace falta otra, se imprime dos veces |
