# Plan cerrado — Fase 2 · F05 Comercio Exterior · Ajustes de la QA manual de la integración

> **Fecha:** 26 de noviembre de 2026. **Estado:** Ejecutado el 2026-11-26. Aprobado por el usuario el 2026-11-26 («Apruebo y ejecuta F1 en una nueva sesión»). Fase 1 (BE `f076b2c`), fase 2 (BE `7733035`), fase 3 (FE `3cae866`) y fase 4 (FE `e707ae9`), hechas el 2026-11-26; fusionadas en `fase-2`: BE `dcb7b8f`, FE `4ed9400`. Casos en [`D/qa/casos-qa2-f05-ajustes-qa-2026-11-26.md`](../../../qa/casos-qa2-f05-ajustes-qa-2026-11-26.md).
> **Origen:** la prueba manual del usuario sobre F05 integrada (I-05, contra el backend local, con un flujo completo desde Vigilancia y datos tomados del legacy): [`../qa-manual/hallazgos-int-F05.md`](../qa-manual/hallazgos-int-F05.md). Las respuestas del usuario del 2026-11-26 están en D1 a D7c.
> **Base:** BE `fase-2` `348ab15` · FE `fase-2` `00d15e5` · docs `main` `6a7984b`.
> **Alcance:** backend y frontend. Backend: un endpoint de producto rápido para Báscula, la regla del estado aduanero del depósito y las correcciones de los PDF actuales (etiqueta por depósito, tarjeta por vehículo, PDF del depósito y guía de salida). Frontend: el producto nuevo en Báscula, el pesaje en un drawer desde la etapa Entradas, la edición del ingreso, el encabezado del depósito y la tabla de Levantes. Sin migraciones. Cambia decisiones del plan de F05 (D39 y D40) y del plan de ajustes de UI de F05 (D22 y D31). Donde chocan, gana este plan.
> **Fuera de este plan** (D1): el cambio de separadores del hallazgo 7 («1,234.56» en toda la app y los PDF) y los tres formatos nuevos de PDF del hallazgo 8 (etiqueta, PDF del depósito y guía de salida, elegibles por parámetro). Cada uno tendrá su propio plan.
> **Rutas:** relativas a `code_workspace/`. Prefijos: `B/` = `Backend/wms-api/`; `F/` = `Frontend/wms/app/`; `FT/` = `Frontend/wms/test/`; `D/` = `docs/`; `P05/` = `D/planes/sprint-11/f05-comercio-exterior/plan-cerrado-f2-f05-comercio-exterior-2026-11-25.md`; `AUI/` = `D/planes/sprint-11/f05-comercio-exterior/plan-cerrado-f2-f05-ajustes-ui-2026-11-26.md`; `H/` = el archivo de hallazgos. El archivo numera dos veces el 7: aquí, `H/` 7a es la tabla de Levantes y `H/` 7b los separadores.

---

## 0. Instrucciones para el ejecutor

1. **Lecturas mínimas:** los dos `AGENTS.md` de los repos, `D/procesos/flujo-de-trabajo-agentes.md`, `P05/` D39 y D40, `AUI/` D2, D22 y D31, `H/` y este plan completo.
2. **Ramas y git:** `f2/f05-ajustes-qa` en BE y en FE, desde `fase-2`. Commit y push al cerrar cada fase, con el mensaje de §7. Al cerrar la fase 4, fusión en `fase-2` con `--no-ff` en los dos repos y push. Sin `push --force`. Para borrar, `rm`. `test/.nuxtrc` está sin seguimiento: no se sube.
3. **Una fase por turno** (`AGENTS.md`): al cerrar cada una, compuertas, commit, estado en este plan (§4) y en la matriz, y reporte.
4. **Líneas citadas:** son de la base. Confírmalas con grep; si el código no coincide, pregunta en un solo mensaje.
5. **Verificación:** `yarn dev` sin sesión simulada contra el API local (`dotnet run --project B/Wms.Api --launch-profile http`, puerto 5281), con Administrador, Báscula y Comercio Exterior. El depósito de la QA es el `5f3749d2-6058-4f58-91e9-45d53f832b41` (2026BA…, legacy BA1452). Capturas en `D/planes/sprint-11/f05-comercio-exterior/evidencias/ajq-*`.
6. **Los PDF se comparan con el legacy** (`bodegas-legacy/`, base local `legacy-mariadb`). Si una regla del legacy no se puede leer del código ni de la base, pregunta.

---

## 1. Decisiones

### 1.1 Respuestas del usuario (2026-11-26)

| # | Decisión | Fuente |
| --- | --- | --- |
| D1 | **Tres planes.** Este cubre los hallazgos 1 a 6, 7a, 8 (correcciones de los PDF actuales) y 9. El cambio de separadores (`H/` 7b) y los formatos nuevos de PDF (`H/` 8, rediseños) van en planes propios | Usuario: «Plan F05 + 2 planes aparte» |
| D2 | **Formato de PDF por parámetro de sistema, uno por documento** (etiqueta, PDF del depósito y guía de salida), como `GUIDE_CODE_TYPE`. Lo aplica el plan de los formatos nuevos; aquí solo se registra | Usuario: «Un parámetro por documento» |
| D3 | **Las cantidades de los levantes no cambian** (`H/` 5). El legacy admite decimales al digitar y al calcular desde el peso, con la misma fórmula que v2 (peso × cantidad ingresada ÷ suma de pesos de manifiesto, a 2 decimales; `bodegas-legacy/modulos/mod_levantes/registrarlevante.php:246-253`). En la base del legacy, el levante 372024000009520 de BA1452 tiene `cantidad_levante = 640` exacto: se digitó a mano, el legacy no redondea al mostrar. En v2 salió 640,13 porque solo se digitó el peso (32.023 kg de 96.050 kg, 1.920 unidades). Desde I-05 la cantidad digitada se respeta. El hallazgo se cierra sin código | Usuario: «Sin cambios, como el legacy» |
| D4 | **El depósito tiene dos estados aduaneros; el producto conserva tres** (`H/` 6). Detalle en D13 | Usuario: «Solo el depósito» |
| D5 | **«Unidad(es) de carga» solo cuando hay unidades**, en la etiqueta por depósito y en la tarjeta por vehículo (`H/` 8), como el legacy. Detalle en D17 | Usuario: «Ocultarla si no hay unidades» |
| D6 | **El producto nuevo de Báscula se crea en el catálogo al instante** (`H/` 1). Detalle en D8 | Usuario: «Crear en el catálogo ya» |
| D7 | **Colores del estado del depósito:** Borrador `secondary`, Confirmado `success` (verde), Cerrado `contrast` (gris oscuro) y Anulado `danger` (`H/` 4) | Usuario: «Gris oscuro (contrast)» |
| D7b | **Repesar y anular para el operario de CE sin cambiar permisos** (`H/` 2). CE es un operario de mayor nivel y controla los módulos inferiores; el operario de Báscula solo entra a Vigilancia y a Báscula. «Repesar» lleva a la página de proceso de Báscula y todo el API de Báscula exige `ScaleAccess` (Admin y Báscula), así que el operario de CE que deba repesar o anular recibe **además el rol Báscula** en su usuario. No cambian políticas, páginas ni menú. Detalle en D11 | Usuario: «En caso mejor asigno adicional el rol de báscula al operario de CE» |
| D7c | **La guía de salida no tiene columna «Unidad».** El hallazgo venía de una guía vieja generada en staging; en esta implementación esa columna ya no existe. Sin cambios | Usuario, 2026-11-26 (P1) |

### 1.2 Respuesta sin código (`H/` 9)

| # | Decisión | Fuente |
| --- | --- | --- |
| D21 | **La planilla de envío es un dato del depósito, no un documento.** «Planilla de envío» del menú Acciones guarda o quita el número de la planilla de envío de la DIAN (`PATCH …/shipping-form-number`, C-F05-46; `B/Wms.Domain/Entities/Warehouse/WarehouseStorage.cs:520`). El número sale en el encabezado del depósito («· Planilla de envío {N}», `F/features/foreign-trade/components/DepositDetailHeader.vue:159`) y en la columna «No. Planilla de Envío» del Diario de ingresos (`B/Wms.Application/Warehouse/Common/Services/DailyIncomingGoodsReportBuilder.cs:122`), como en el legacy (`bodegas-legacy/modulos/mod_inventario/reportediario.php:354`). No genera PDF. Se responde al usuario en el reporte de la fase 4 | `H/` 9 |

### 1.3 Báscula: producto nuevo (`H/` 1; fase 1 BE y fase 3 FE)

| # | Decisión | Fuente |
| --- | --- | --- |
| D8 | **Endpoint de producto rápido para Báscula, no `POST /product`.** <br>• **Por qué:** `POST /product` exige `ConfigurationAccess` (Admin, CE y Facturación; `B/Wms.Api/Controllers/v1/ProductController.cs:21-22`) y un SKU (`CreateProductCommand`), que el modal no pide. Abrirlo a Báscula daría también la creación completa del catálogo. <br>• **Contrato:** C-F05AQ-01 (§2). Crea el producto con la misma regla que hoy aplica el guardado del registro con texto libre: si ya hay un producto con el mismo nombre normalizado, lo devuelve; si no, lo crea con `Product.CreateFromWeighbridge` y un SKU único (`B/Wms.Application/Weighbridge/Common/Services/WeighbridgeProductResolver.cs:85-115`, `NewUniqueSkuAsync`). Queda marcado `CreatedFromWeighbridge`, para que Configuración lo revise como hoy. <br>• **Permiso:** `ScaleAccess` (Admin y Báscula). <br>• **Reutilización:** la búsqueda y la creación se sacan del resolver a un método que usan los dos | `H/` 1; D6 |
| D9 | **Modal «Nuevo producto» en la línea de mercancía.** <br>• **Hoy:** el «+» de `AppSearchSelect` (`quick-create`) toma el texto escrito como producto nuevo (`F/features/weighbridge/components/RegistrationGoodsLines.vue:70-75`, `onFreeText`); si el campo pierde el foco antes, el texto se borra. <br>• **Cambio:** el «+» abre `WeighbridgeProductDialog` (nuevo, en `F/features/weighbridge/components/`), con «Nombre» (precargado con lo escrito, 3 a 200 caracteres) y «Embalaje» (`Select` con los `packagingTypes` de la línea, obligatorio). «Crear» llama a C-F05AQ-01, cierra el modal y deja en la línea el producto y el embalaje elegidos (`patch(line.key, { productId, packagingTypeId, packaging })`). Invalida el prefijo de productos. <br>• **Opciones de la lista:** cada producto muestra el nombre y, debajo, su embalaje (`option-description`: `packagingTypeName`, o «Sin embalaje»); hoy muestra el SKU (`:66`). <br>• **Texto libre:** las líneas que ya traen `productDescription` (duplicadas o ediciones) se siguen mostrando con la etiqueta «Nuevo», como hoy (`:77-91`); las nuevas ya no lo generan | `H/` 1; D6 |

### 1.4 Detalle del depósito (`H/` 2, 4, 6 y 7a; fases 1 y 4)

| # | Decisión | Fuente |
| --- | --- | --- |
| D10 | **«Ver pesaje» abre un drawer de solo lectura** (`H/` 2; cambia `P05/` D40 y `AUI/` D3). <br>• **Hoy:** navega a `/operations/weighbridge/cycles/{id}` (`F/features/foreign-trade/components/DepositEntriesStage.vue:61` y `:82`). <br>• **Cambio:** `AppDetailDrawer` con `WeighbridgeEntryDetail`, leído con `useWeighbridgeDetail({ kind: "cycle", id })`, como el historial de Báscula (`F/pages/operations/weighbridge/history/index.vue:186-201`). Sin acciones en el drawer. <br>• **La página `/cycles/[id]` se queda:** la usan Facturación y otros enlaces (`F/pages/operations/weighbridge/cycles/[id].vue:3-5`) | `H/` 2 |
| D11 | **«Repesar» y «Anular pesaje» en el menú ⋮ de la fila de Entradas** (`H/` 2). <br>• **Quién:** usuarios con rol Admin o Báscula, como en la página del ciclo (`[id].vue:6-7`, `isScale`; `DEC-005`). Como el operario de Báscula no entra a Comercio Exterior, en la práctica los ven Admin y el operario de CE que tenga también el rol Báscula (D7b). Un usuario solo con el rol CE no los ve, porque el backend le respondería 403. <br>• **Cuándo:** con `weighbridgeCycleId` y el depósito sin anular. <br>• **Cómo:** `WeighbridgeEntryDialogs` (`open("reweigh" | "void", { kind: "cycle", id })`), el mismo componente de la página del ciclo. Si el pesaje no admite la acción, el diálogo muestra el error del backend. <br>• **Después:** invalida el prefijo del detalle del depósito y el de Báscula | `H/` 2; `DEC-005` |
| D12 | **Encabezado del depósito** (`H/` 4). <br>• **Colores:** D7, en `DEPOSIT_STATUS_SEVERITY` (`F/features/foreign-trade/utils/deposit-display.ts:39-44`); vale para el encabezado y las listas. <br>• **Documento comercial:** «Información general» (`DepositDetailHeader.vue:181-220`) suma «Documento comercial: {tipo} {número}» con `primaryDocumentTypeName` y `cargoManifestNumber`, que ya vienen en el detalle (`F/features/foreign-trade/contracts/deposit.ts:132-133`). Si faltan los dos, no se muestra | `H/` 4; D7 |
| D13 | **Estado aduanero del depósito: basta un levante** (`H/` 6; D4). <br>• **Backend:** `NationalizationRules.DepositStatus` devuelve `Nationalized` si algún producto tiene levante y `NotNationalized` si ninguno (`B/Wms.Application/ForeignTrade/Common/Services/NationalizationRules.cs:43-55`). `ProductStatus` no cambia: el producto sigue con `Partial` hasta completar su cantidad. <br>• **Efectos:** el encabezado, las listas de depósitos y la vista 2 de Levantes dejan de recibir `Partial` para el depósito. El contador `partial` de C-F05-33 queda en 0 (`GetReleasesHandler.cs:61`); el campo se conserva para no cambiar el contrato. El tablero de CE cuenta como pendientes solo los depósitos sin levantes (`F/features/foreign-trade/composables/useForeignTradeDashboard.ts:47`). Coincide con las etiquetas impresas, que ya usan «hay levantes» (`LabelGenerationService.cs:89` y `:719`). <br>• **Frontend:** `NATIONALIZATION_LABEL.Partial` pasa a «Parcial», el texto del producto (`deposit-display.ts:65-69`). El filtro de la vista 2 se queda (`F/pages/foreign-trade/releases/index.vue:47-50`) | `H/` 6; D4 |
| D14 | **Tabla de Levantes** (`H/` 7a; cambia `AUI/` D22 y D31). <br>• **Sin «Nuevo levante»:** la fila editable de cada producto ya está siempre abierta; el botón solo le llevaba el foco. Se quita de la etapa (`F/features/foreign-trade/components/DepositReleasesStage.vue:268-276`, con `focusNewRelease` de `:127-128` si queda sin uso) y de la vista 2, que la reutiliza (`ReleaseDepositExpansion.vue`). <br>• **Separación:** los botones de solo icono de la fila editable pasan de `gap-1` a `gap-2` (`ReleaseEditableRow.vue:340`) | `H/` 7a |

### 1.5 Edición del ingreso (`H/` 3; fase 3)

| # | Decisión | Fuente |
| --- | --- | --- |
| D15 | **El interruptor «Unidad de carga» solo cambia al pulsarlo.** Hoy la `<label>` envuelve el interruptor y el texto, y un clic en cualquier parte lo cambia (`F/features/foreign-trade/components/EntryEditForm.vue:669-673`). La `<label>` se cambia por un `div`; el texto queda en un `span` con id, y el `ToggleSwitch` lleva `aria-labelledby` a ese id | `H/` 3 |
| D16 | **Motivo de la corrección automático** (como `AUI/` D2). Se quita la sección del motivo (`EntryEditForm.vue:710-718`) y su validación (`:248`). Al guardar se envía «Corrección del ingreso desde el detalle del depósito {N}.», que cumple los 10 a 500 caracteres. Sin cambio de contrato ni de backend; la auditoría conserva un motivo | `H/` 3; `AUI/` D2 |
| D22 | **La placa del título en una etiqueta.** «Editar ingreso · {placa}» (`EntryEditForm.vue:355-357`) muestra la placa en un `Tag` (`severity="contrast"`, letra mono y más grande) | `H/` 3 |

### 1.6 PDF actuales (`H/` 8; fase 2)

| # | Decisión | Fuente |
| --- | --- | --- |
| D17 | **Unidades de carga solo con valor** (D5). En la etiqueta por depósito (`B/Wms.Application/ForeignTrade/Common/Services/LabelGenerationService.cs:206-213`) y en la tarjeta por vehículo (`:788-796`), la línea «Unidad(es) de carga» y su valor salen solo si hay unidades. `CargoUnitText.Format` sigue devolviendo «N/A» para los demás documentos | D5 |
| D18 | **La tarjeta por vehículo, como la del depósito** (`H/` 8). <br>• **Manifiesto:** «Manifiesto No.» muestra el manifiesto DIAN del depósito con su fecha, `{número}({aaaa-mm-dd})`, igual que la etiqueta del depósito (`:80-83` y `:195-202`). Hoy muestra el manifiesto del camión (`:702` y `:806-810`). <br>• **Datos de nacionalización:** con levantes, el bloque «DATOS DE NACIONALIZACION» (levantes y números de aceptación) con `FormatReleasesSummary` y `FormatAcceptancesSummary`, igual que la etiqueta del depósito (`:219-238`). La consulta ya incluye `Releases` (`:636`). <br>• **Alcance (fase 2, aprobado por la sesión de integración el 2026-11-26):** solo la tarjeta de importación; la de exportación y la de inspección no tienen manifiesto DIAN ni levantes y siguen con el manifiesto del camión | `H/` 8 |
| D19 | **PDF del depósito** (`B/Wms.Application/ForeignTrade/Common/Services/DepositPdfService.cs`). <br>• **Importador:** sale de `ServiceRecord.Customer` (`:57` y `:219`), vacío en los depósitos de los flujos nuevos. Se resuelve como la guía de salida: tercero con rol `IMPORTER` del servicio y, si no hay, el cliente (`DispatchGuidePdfService.cs:355-369`); con su identificación y dirección del contacto activo. <br>• **«Peso Kg.»:** usa `PhysicalNetWeight` (`:371`), nulo en los flujos nuevos. Pasa a `MerchandiseWeight` de la entrada (P. mercancía). <br>• **«TOTAL PESO (Kg)»:** suma `MerchandiseWeight` (`:152`); hoy suma `PhysicalNetWeight` y da 0. <br>• **Entrada, Ampara y Saldo:** hoy son `ReceivedQuantity`, `DeclaredQuantity` y `CurrentStock` (`:374-376`), que en el depósito de la QA valen 1.920 los tres. Se toman las reglas del PDF del legacy para los tres totales (cantidad total ingresada, cantidad amparada y saldo). El ejecutor localiza el PDF del depósito del legacy, documenta su regla aquí antes de cambiar y, si el saldo del legacy descuenta los levantes o solo las salidas no se puede leer, pregunta. <br>• **Regla del legacy (leída en la fase 2, `bodegas-legacy/modulos/mod_depositos/verdeposito.php:284-392`):** una fila por producto amparado (`productoamparado`, por producto y embalaje). **Entrada** = suma de `cantidad` de los pesajes no eliminados del producto (`:333`). **Ampara** = `cantidadamparada` (`:347`). **Saldo** = Ampara − Entrada (`:348`): no descuenta levantes ni salidas; es lo que falta por llegar. Con Ampara en 0, Ampara y Saldo salen en blanco (`:351-355`). **Peso Kg.** = `peso_manifiesto` de cada pesaje (`:337`), y **TOTAL PESO** = suma de `peso_manifiesto` de los pesajes no eliminados (`:387-389`). En v2 es la regla de `DepositCoverage` (ingresado = suma de lo declarado en las entradas no anuladas; saldo = amparado − ingresado), con `CoveredQuantity` como amparado. BA1452 en el legacy (depósito 27284): Entrada 1.920, Ampara 1.920, Saldo 0 y TOTAL PESO 96.050 (32.010 + 32.020 + 32.020). Las entradas anuladas no cuentan ni salen en la tabla, como los pesajes eliminados del legacy | `H/` 8 |
| D20 | **Guía de salida** (`B/Wms.Application/ForeignTrade/Common/Services/DispatchGuidePdfService.cs`). <br>• **Agencia:** «Agencia de aduanas: {nombre} ({rol})» repite el rol (`:378`). Queda solo el nombre. <br>• **Tiquetes (decisión del usuario del 2026-11-26, «Como el legacy: el de la salida»):** hoy salen de `Entries.TicketNumber` (`:390-395`), los tiquetes de los camiones que trajeron la mercancía (en los flujos nuevos sí se llenan: báscula los graba en la entrada, `RecordWeighingHandler.cs:222`; el ciclo con depósito no lleva tiquete). El legacy imprime el tiquete del pesaje del camión que saca la mercancía (`bodegas-legacy/modulos/mod_salidas/verguia.php:341-357`, `producto_salida.id_pesaje`). Pasa a eso: los tiquetes de los ciclos de báscula de salida no anulados de la salida (`ServiceRecord.GoodsExitId`, o `GoodsExit.WeighbridgeCycleId`); sin ciclo con tiquete, vacío. <br>• **QR:** va a la izquierda del bloque del número, no centrado (`:514-526`). <br>• **Dirección del importador:** el código la imprime (`:559`) desde el contacto activo (`:366`). Se verifica con el importador del depósito de la QA; si no tiene contacto activo con dirección, es un dato faltante y no se cambia código. <br>• **Verificado en la fase 2:** el importador del depósito de la QA (COMERCIALIZADORA LUHOMAR S.A.S) no tiene contactos: dato faltante, sin cambio de código. Con un contacto activo, la guía imprime su dirección. <br>• **Levante y Aceptación:** se verifica que cada línea liste todos los levantes y aceptaciones del producto en el depósito, separados por coma. Si no, se corrige. <br>• **Verificado en la fase 2:** la línea congelaba solo el levante vigente (CHG-35, `ReleaseSnapshotSelector.Latest`); el legacy lista todos (`verguia.php:600-616`). Pasa a congelar al emitir todos los levantes del producto y sus aceptaciones, separados por coma, por fecha de aceptación (`ReleaseSnapshotSelector.Joined`, cortado con «…» a los 500 caracteres de la columna). Las guías ya emitidas conservan lo que guardaron. <br>• **Columna «Unidad»:** sin cambios (D7c) | `H/` 8; D7c |

---

## 2. Contrato

| Id | Método y ruta | Cuerpo | Respuesta | Permiso |
| --- | --- | --- | --- | --- |
| C-F05AQ-01 | `POST /weighbridge/products` | `{ name: string (3–200), packagingTypeId: guid }` | `ProductDto` (el existente o el creado), 200 si existía y 201 si se creó | `ScaleAccess` |

- **Errores:** 400 con nombre fuera de rango o embalaje inexistente o inactivo.
- **Zod:** `weighbridgeProductCreateSchema` en `F/features/weighbridge/contracts/` y la respuesta con `productSchema` de `F/features/products/contracts/product.ts`.
- **Fuente:** `weighbridgeProductSource` con `create`, http directo (sin datos simulados; guardia `INTEGRATED_SOURCES`).

C-F05-33 conserva `partial` (D13). Ningún otro contrato cambia.

---

## 3. Archivos que se tocan

**Backend**

- `B/Wms.Api/Controllers/v1/` (controlador de Báscula): C-F05AQ-01.
- `B/Wms.Application/Weighbridge/Commands/Products/CreateQuickProduct/` (nuevo): comando, validador y handler.
- `B/Wms.Application/Weighbridge/Common/Services/WeighbridgeProductResolver.cs`: buscar o crear un producto, compartido (D8).
- `B/Wms.Application/ForeignTrade/Common/Services/NationalizationRules.cs` (D13).
- `B/Wms.Application/ForeignTrade/Common/Services/LabelGenerationService.cs` (D17, D18).
- `B/Wms.Application/ForeignTrade/Common/Services/DepositPdfService.cs` (D19).
- `B/Wms.Application/ForeignTrade/Common/Services/DispatchGuidePdfService.cs` (D20).
- Pruebas en `B/Wms.Tests` y `B/Wms.IntegrationTests` (§5).

**Frontend**

- `F/features/weighbridge/components/RegistrationGoodsLines.vue` y `WeighbridgeProductDialog.vue` (nuevo); `F/features/weighbridge/contracts/` y `services/` (C-F05AQ-01).
- `F/features/foreign-trade/components/DepositEntriesStage.vue` (D10, D11).
- `F/features/foreign-trade/components/EntryEditForm.vue` (D15, D16, D22).
- `F/features/foreign-trade/components/DepositDetailHeader.vue` y `F/features/foreign-trade/utils/deposit-display.ts` (D12, D13).
- `F/features/foreign-trade/components/DepositReleasesStage.vue`, `ReleaseDepositExpansion.vue` y `ReleaseEditableRow.vue` (D14).
- `FT/unit/guards/mock-sources.spec.ts` (la fuente nueva en `INTEGRATED_SOURCES`) y pruebas de §5.

**Docs:** este plan, la matriz, `D/planes/README.md`, `D/qa/` (casos) y, si cambia una regla del hub, `D/contexto/decisiones.md` (estado aduanero del depósito, D13).

---

## 4. Fases

| Fase | Repo | Contenido | Cierre | Estado |
| --- | --- | --- | --- | --- |
| 1 | BE | C-F05AQ-01 (D8) y el estado aduanero del depósito (D13) | Compuertas BE; QA-AJQ5-001 a 004 en PASA (API) | Hecha el 2026-11-26: BE `f076b2c` en `f2/f05-ajustes-qa`. `POST /weighbridge/products` (201 creado, 200 existente, 400, 403 con CE y Facturación) con `WeighbridgeProductResolver.FindOrCreateAsync` compartido; `DepositStatus` con un levante = `Nationalized`. `Wms.Tests` 2348 → 2350, `Wms.IntegrationTests` 879 → 886, `has-pending-model-changes` limpio. QA-AJQ5-001 a 004 en PASA contra el API local (el depósito de la QA, con 640,13 de 1.920 levantados: depósito `Nationalized`, producto `Partial`) |
| 2 | BE | PDF actuales: D17 a D20 | Compuertas BE; QA-AJQ5-005 a 012 en PASA (PDF descargados y revisados) | Hecha el 2026-11-26: BE `7733035` en `f2/f05-ajustes-qa`. Etiqueta y tarjeta sin «Unidad(es) de carga» cuando no hay unidades; tarjeta de importación con el manifiesto DIAN y los datos de nacionalización; PDF del depósito con el importador IMPORTER, el peso de mercancía (TOTAL PESO 96.050) y Entrada, Ampara y Saldo con la regla del legacy (1.920, 1.920 y 0 en el depósito de la QA); guía con la agencia sin el rol, el QR a la izquierda, el tiquete de la salida (decisión del usuario: como el legacy) y todos los levantes y aceptaciones. `Wms.Tests` 2350 → 2368, `Wms.IntegrationTests` 886 → 888, `has-pending-model-changes` limpio. QA-AJQ5-005 a 008 en PASA contra el API local; 009, 010 y 012 en PASA con la prueba de integración (nota de §5); 011 en PASA como dato faltante (LUHOMAR sin contacto). Evidencias `evidencias/ajq-f2-*` |
| 3 | FE | Báscula y edición del ingreso: D9, D15, D16 y D22 | Compuertas FE; QA-AJQ5-013 a 017 en PASA en el navegador | Hecha el 2026-11-26: FE `3cae866` en `f2/f05-ajustes-qa` (desde `fase-2` `00d15e5`). El «+» de la línea abre `WeighbridgeProductDialog` (nombre y embalaje) y crea con C-F05AQ-01 (contrato en `weighbridge/contracts/product.ts`, fuente `weighbridge/services/product.source.ts` en `INTEGRATED_SOURCES`); la opción muestra el embalaje; el modal se monta solo mientras está abierto. Edición del ingreso: switch con `aria-labelledby` y sin `<label>`, motivo fijo «Corrección del ingreso desde el detalle del depósito {N}.» sin sección, placa en `Tag` contrast. `yarn test` 790 → 794 (148 archivos, sigue el error heredado de `WeighbridgeQueuePage.spec.ts`), `yarn lint` 142 → 142 errores (265 avisos; ninguno en archivos tocados), `yarn build` 0, guardias en verde. QA-AJQ5-013 a 017 en PASA en el navegador contra el API de la rama (Báscula: 201 y la línea con «GARBANZO QA AJQ5» y Sacos; Administrador: el mismo nombre en minúsculas, 200 con el mismo producto; Comercio Exterior y Administrador en la edición). Nota de 016: una corrección sin cambios no escribe fila de auditoría (el motivo es la descripción de las filas cambiadas); se verificó con la fecha del manifiesto del ingreso ABC125 (2026BA00002), que se puso y se quitó en dos guardados. Queda en el catálogo local el producto de prueba «GARBANZO QA AJQ5» (`createdFromWeighbridge`). Evidencias `evidencias/ajq-f3-*` |
| 4 | FE y docs | Detalle del depósito y Levantes: D10 a D14; casos a `D/qa/`; respuesta de D21; fusión de `f2/f05-ajustes-qa` en `fase-2` en los dos repos | Compuertas FE; QA-AJQ5-018 a 025 en PASA; fusiones con push | Hecha el 2026-11-26: FE `e707ae9` en `f2/f05-ajustes-qa`. «Ver pesaje» abre `AppDetailDrawer` con `WeighbridgeEntryDetail` (`{ kind: "cycle" }`), sin acciones; «Repesar» y «Anular pesaje» en el menú de la fila con Admin o Báscula (`WeighbridgeEntryDialogs`; al terminar invalida `['foreign-trade']` y Báscula); Confirmado `success` y Cerrado `contrast`; «Documento comercial» en el resumen; `NATIONALIZATION_LABEL.Partial` = «Parcial»; sin «Nuevo levante» en la etapa ni en la vista 2 y la fila editable con `gap-2`. `yarn test` 794 → 805 (148 → 150 archivos; sigue el error heredado de `WeighbridgeQueuePage.spec.ts`), `yarn lint` 142 → 142 errores (265 avisos; ninguno en archivos tocados), `yarn build` 0, guardias en verde. QA-AJQ5-018 a 025 en PASA en el navegador contra el API de la rama, con Comercio Exterior y Administrador. 019: la combinación CE + Báscula se cubrió con Vitest, porque la base local no tiene un usuario con esos dos roles (decisión del usuario: no se creó). 021: la base local no tiene depósitos cerrados; Cerrado se verificó con la prueba del encabezado. Fusiones con `--no-ff` y push: BE `fase-2` `dcb7b8f` (`dotnet build` sin errores, `Wms.Tests` 2368 en verde) y FE `fase-2` `4ed9400` (`yarn test` 805 y `yarn build` 0). Casos en `D/qa/casos-qa2-f05-ajustes-qa-2026-11-26.md`; regla del estado aduanero en `D/contexto/decisiones.md` (`DEC-080`). Evidencias `evidencias/ajq-f4-*` |

---

## 5. Pruebas y casos QA

**Backend:**

- `NationalizationRulesTests`: un producto parcial y otro sin levantes → depósito `Nationalized`; ninguno con levante → `NotNationalized`; `ProductStatus` sin cambios.
- `CreateQuickProductTests` (integración): crea con SKU único y `CreatedFromWeighbridge`; con el mismo nombre en otra capitalización devuelve el existente; 400 con nombre corto o embalaje inexistente; 403 con Comercio Exterior y Facturación.
- `WmsPolicyRolesTests`: sin cambios (la política ya existe).
- PDF: pruebas de las reglas puras que se extraigan (importador del depósito, tiquetes de la guía, texto de la agencia y totales del PDF del depósito).

**Frontend (Vitest):**

- `RegistrationGoodsLines`: el «+» abre el modal con el texto escrito; «Crear» deja producto y embalaje en la línea; la opción muestra el embalaje.
- `EntryEditForm`: el clic en el texto no cambia el interruptor; guardar envía el motivo automático; sin sección de motivo.
- `DepositEntriesStage`: «Ver pesaje» abre el drawer; «Repesar» y «Anular pesaje» con Báscula y sin ellos con Comercio Exterior.
- `deposit-display`: colores de D7; `NATIONALIZATION_LABEL.Partial` = «Parcial».
- `DepositDetailHeader`: «Documento comercial» con tipo y número.
- `DepositReleasesStage`: sin «Nuevo levante».

**Casos QA** (navegador o API contra el API local):

| Caso | Hallazgo | Pasos | Resultado esperado |
| --- | --- | --- | --- |
| QA-AJQ5-001 | 1 | API con Báscula: C-F05AQ-01 con un nombre nuevo | 201; producto con SKU y `createdFromWeighbridge: true` |
| QA-AJQ5-002 | 1 | Lo mismo con el nombre en otra capitalización | 200 con el mismo producto |
| QA-AJQ5-003 | 1 | API con Comercio Exterior | 403 |
| QA-AJQ5-004 | 6 | Detalle de un depósito con un levante parcial | `nationalizationStatus: "Nationalized"`; el producto sigue `Partial` |
| QA-AJQ5-005 | 8 | Tarjeta por vehículo de un camión del depósito de la QA | Manifiesto DIAN con fecha; «DATOS DE NACIONALIZACION» con el levante 372024000009520 y su aceptación |
| QA-AJQ5-006 | 8 | Etiqueta y tarjeta de un depósito sin unidades de carga | Sin la línea «Unidad(es) de carga» |
| QA-AJQ5-007 | 8 | Lo mismo con unidades | La línea con las unidades |
| QA-AJQ5-008 | 8 | PDF del depósito de la QA | Importador con su identificación; «Peso Kg.» con el P. mercancía de cada camión; «TOTAL PESO» 96.050; Entrada, Ampara y Saldo con la regla de D19 |
| QA-AJQ5-009 | 8 | Guía de salida de una salida del depósito de la QA (fase 2: de un depósito sembrado por la prueba de integración, ver la nota) | Agencia sin el rol repetido; el tiquete de báscula de la salida (D20), no los de ingreso |
| QA-AJQ5-010 | 8 | La misma guía | QR a la izquierda |
| QA-AJQ5-011 | 8 | La misma guía | Dirección del importador si tiene contacto con dirección (si no, anotado como dato faltante) |
| QA-AJQ5-012 | 8 | La misma guía, con un producto de dos levantes | Levante y Aceptación con los dos |
| QA-AJQ5-013 | 1 | Báscula, registro: escribir un nombre nuevo y pulsar «+» | Modal con el nombre; al crear, la línea queda con producto y embalaje |
| QA-AJQ5-014 | 1 | Abrir la lista de productos | Cada opción con su embalaje |
| QA-AJQ5-015 | 3 | Edición del ingreso: clic en el texto «Unidad de carga» y fuera del interruptor | No cambia; solo cambia al pulsar el interruptor |
| QA-AJQ5-016 | 3 | Guardar la edición del ingreso | Sin campo de motivo; guarda y la auditoría muestra el motivo automático |
| QA-AJQ5-017 | 3 | Título de la edición | La placa en una etiqueta |
| QA-AJQ5-018 | 2 | Comercio Exterior, etapa Entradas: «Ver pesaje» | Drawer con el pesaje, sin acciones; la página no cambia |
| QA-AJQ5-019 | 2 | Usuario con roles CE y Báscula (y Administrador): menú ⋮ de la fila | «Repesar» y «Anular pesaje»; «Repesar» abre el paso Repesaje de Báscula, «Anular pesaje» su diálogo, y al volver la etapa está al día |
| QA-AJQ5-020 | 2 | Usuario solo con el rol CE: menú ⋮ de la fila | Sin «Repesar» ni «Anular pesaje» |
| QA-AJQ5-021 | 4 | Encabezado de un depósito confirmado y de uno cerrado | Confirmado en verde y Cerrado en gris oscuro, también en las listas |
| QA-AJQ5-022 | 4 | Información general | «Documento comercial» con tipo y número |
| QA-AJQ5-023 | 6 | Encabezado del depósito de la QA (un levante) | «Nacionalizado»; nunca «Nacionalización parcial» |
| QA-AJQ5-024 | 7a | Etapa Levantes y vista 2 | Sin «Nuevo levante»; la fila editable sigue disponible |
| QA-AJQ5-025 | 7a | Fila editable | Botones separados |

**Nota de la fase 2 (QA-AJQ5-009 a 012):** la base local no tiene guías de salida y el depósito de la QA no tiene salidas; un segundo levante en él rompería QA-AJQ5-023. Por acuerdo con la sesión de integración del 2026-11-26, los cuatro casos se corrieron con la prueba de integración (Testcontainers): un depósito sembrado con su camión y tiquete de ingreso, dos levantes en el mismo producto, una salida con su ciclo de báscula y tiquete, su guía y un contacto con dirección en el importador. La guía se descargó por el API de la prueba (`exits/{id}/guide/pdf`) y se revisó su texto y su imagen. Lo que queda en el código: `GuideExitTicketTests` (009) y `GuideReleaseSnapshotTests` (012). La dirección del importador del depósito de la QA (011) es un dato faltante. Ni el depósito de la QA ni la base local se tocaron.

---

## 6. Compuertas de cada fase

- **BE (fases 1 y 2):** `dotnet build Wms.sln` sin errores; `dotnet test Wms.Tests` (base 2348) y `dotnet test Wms.IntegrationTests` (base 879) en verde; `dotnet ef migrations has-pending-model-changes` limpio.
- **FE (fases 3 y 4):** `yarn build` con código 0; `yarn test` en verde (base medida en `fase-2` `00d15e5` al empezar la fase 3; queda el error no controlado heredado de `WeighbridgeQueuePage.spec.ts`); `yarn lint` sin subir la base medida y sin errores en archivos nuevos o tocados; las guardias de `FT/unit/guards/` en verde.
- Capturas o PDF de los casos de la fase.

---

## 7. Commits

| Fase | Repo | Mensaje |
| --- | --- | --- |
| 1 | BE | `feat(bascula): producto rápido desde el registro; estado aduanero del depósito con un levante (DEC-080, F05, QA manual de integración)` |
| 2 | BE | `fix(foreign-trade): PDF de etiqueta, tarjeta por vehículo, depósito y guía de salida (DEC-080, F05, QA manual de integración)` |
| 3 | FE | `fix(bascula,foreign-trade): producto nuevo en modal y edición del ingreso (DEC-080, F05, QA manual de integración)` |
| 4 | FE | `fix(foreign-trade): pesaje en drawer, encabezado del depósito y tabla de Levantes (DEC-080, F05, QA manual de integración)` |
| 4 | docs | `docs(f05): ajustes de la QA manual de la integración` |

Fusiones: `f2/f05-ajustes-qa` en `fase-2`, con `--no-ff`, en BE y en FE, al cerrar la fase 4.

---

## 8. Riesgos

| # | Riesgo | Mitigación |
| --- | --- | --- |
| R1 | Báscula crea productos con nombres casi iguales | Se reutiliza el producto con el mismo nombre normalizado (D8) y quedan marcados `CreatedFromWeighbridge` para que Configuración los depure |
| R2 | Cambiar el estado del depósito mueve contadores del tablero de CE y de la vista 2 | Es la regla pedida (D4) y coincide con las etiquetas impresas; QA-AJQ5-004 y 023 |
| R3 | La regla del legacy para Ampara y Saldo del PDF del depósito no se puede leer | D19 obliga a documentarla antes de cambiar y a preguntar si no se puede leer |
| R4 | Un operario de CE sin el rol Báscula no ve «Repesar» ni «Anular pesaje» y lo reporta como falla | D7b: el Administrador le suma el rol Báscula en Usuarios; el reporte de la fase 4 lo recuerda |

---

## 9. Preguntas pendientes

Ninguna. P1 (columna «Unidad» de la guía) se resolvió en D7c.
