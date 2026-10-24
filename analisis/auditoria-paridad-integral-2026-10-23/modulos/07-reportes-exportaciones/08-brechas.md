# 07-reportes-exportaciones — 08 Brechas

> AG-07 · 2026-10-23 · Auditoría estática. Rutas relativas a `code_workspace/`.
> **Prefijos:** `L:` = `bodegas-legacy/`; `INV:` = `bodegas-legacy/modulos/mod_inventario/`; `FE:` = `Frontend/wms/app/`; `BE:` = `Backend/wms-api/`; `WHQ:` = `Backend/wms-api/Wms.Application/Warehouse/Queries/`; `REPQ:` = `Backend/wms-api/Wms.Application/Reports/Queries/`.
> **Fichas existentes revisadas antes de registrar:** `docs/qa/resultados/defectos/INDICE.md` (DEF-F7-001…012, DEF-F4-008, DEF-F9-004, DEF-F8-009, DEF-F11-018), `docs/planes/migracion-staging/resultados/defectos/` y `docs/contexto/estado.md` §4. Ninguna ficha cubre estas brechas; donde hay relación se cita.

## Resumen

| ID | ID funcional | Título | Categoría | Criticidad |
| --- | --- | --- | --- | --- |
| BR-07-001 | CF-L210.a, CF-L210.b, CF-L232 | Los diarios de ingreso y de salida no se exportan a Excel | FRONTEND | MEDIA |
| BR-07-002 | CF-L210.a | El diario de ingresos no muestra depósito, importador, agencia, manifiesto DIAN ni firmas, y pierde la fila por camión | FRONTEND / BACKEND | MEDIA |
| BR-07-003 | CF-L209, CF-L210.a, CF-L232 | Informes y exportaciones toman la fecha de creación como fecha de ingreso (DEC-012) | REGLAS_NEGOCIO | MEDIA |
| BR-07-004 | CF-L209, CF-L210.a, CF-L210.b | «Manifiesto» muestra la carta porte; el kardex no muestra la agencia | BACKEND | MEDIA |
| BR-07-005 | CF-L232, CF-L211, CF-L215, CF-L209 | Excel incompleto: sin filtros, sin totales, sin firmas y con «undefined» | FRONTEND | BAJA |
| BR-07-006 | CF-L231.a, CF-L215 | Informes sin PDF ni impresión (y sin firmas) | FRONTEND / BACKEND | BAJA |
| BR-07-007 | CF-L232 | El botón genérico «Exportar» de `AppTable` exporta solo la página | FRONTEND | BAJA |
| BR-07-008 | CF-L213 | Sin informe por producto de mercancía nacionalizada o pendiente | FRONTEND / BACKEND | BAJA |
| BR-07-009 | CF-L215 | El detalle de pólizas no trae el valor de la mercancía ni el total por depósito | BACKEND | BAJA |
| BR-07-010 | CF-L211, CF-L172.c | Inventario general: ubicaciones sin cantidad y rango de fechas opcional | REGLAS_NEGOCIO | BAJA |
| BR-07-011 | CF-L229.b | Detalle por agencia: salidas sin producto y pesajes sin cantidad | CONTRATOS_API | BAJA |
| BR-07-012 | CF-L258 | Código de barras Code 39 en el depósito y la guía (legacy Code 128) | REGLAS_NEGOCIO | BAJA |
| BR-07-013 | CF-L209 | Kardex: sin autocompletar, sin búsqueda por número legacy y sin menú en Bodega | FRONTEND | BAJA |

Por criticidad: CRÍTICA 0 · ALTA 0 · MEDIA 4 · BAJA 9.

---

### BR-07-001 — Los diarios de ingreso y de salida no se exportan a Excel

- **ID funcional:** CF-L210.a, CF-L210.b, CF-L232.
- **Descripción:** el legacy exportaba a Excel los dos diarios (`INV:reportediario.php:198`; `INV:reportediariosalidas.php`, mismo bloque de iconos). En la V2 solo tienen PDF.
- **Esperado:** «los reportes que se exportan a excel debe ser los mismos que en la version legacy» (`bodegas-legacy/docs/legacy_analysis/DECISIONES_REVISION.md` §2.E.18; GAP-017 «dejar en Excel los mismos reportes que el legacy»).
- **Actual:** `FE:pages/reports/daily-incoming-goods.vue` y `daily-outgoing-goods.vue` no usan `useExcelExport` ni `exportRowsToExcel` (búsqueda en `FE:pages`); solo «Descargar PDF» (`daily-incoming-goods.vue:66-120,171-176`). El plan frontend F5-11 no los incluyó en su tabla (`docs/planes/paridad-legacy/plan-frontend-paridad-legacy.md` F5-11).
- **Capa:** frontend. **Categoría:** FRONTEND.
- **Impacto:** quien saca el diario para cuadrar o enviar a la DIAN no puede trabajarlo en hoja de cálculo; incumple una decisión explícita del negocio.
- **Criticidad:** MEDIA — función secundaria (hay PDF), pero contradice una decisión documentada.
- **Dependencias:** BR-07-002 y BR-07-004 (columnas que deberían ir en el Excel).
- **Acción recomendada:** agregar «Exportar Excel» con la utilidad común en las dos páginas (los endpoints no paginan: ya devuelven todas las filas).
- **Criterio de resolución:** en ambos diarios hay un botón Excel que descarga todas las filas del rango con las columnas de la pantalla y la fila de totales.

### BR-07-002 — El diario de ingresos no muestra depósito, importador, agencia, manifiesto DIAN ni firmas, y pierde la fila por camión

- **ID funcional:** CF-L210.a.
- **Descripción:** el legacy agrupa por depósito con encabezado Depósito / Intermediario / Importador y lista una fila por camión con manifiesto DIAN, CPI, manifiesto preimpreso, placa, fecha y hora, tiquete, transportadora, embalaje, cantidad y peso de manifiesto; cierra con «Total Vehículos» y las firmas «Jefe de Bodega», «Recibí conforme DIAN», «Firma Funcionario» (`INV:reportediario.php:340-431`). Solo importación (`:77`).
- **Esperado:** las mismas columnas y agrupación (objetivo del plan backend §C.5: «quien hoy saca un informe del legacy lo saca de la v2 con las mismas columnas»).
- **Actual:** una fila **por producto** con placas y tiquetes unidos por coma y el neto físico solo en la primera fila (`BE:Wms.Application/Warehouse/Common/Services/DailyIncomingGoodsRowBuilder.cs:28-73`); la pantalla y el PDF no muestran el número de depósito aunque el DTO lo trae (`FE:pages/reports/daily-incoming-goods.vue:240-279`; `BE:Wms.Application/Warehouse/Common/Services/DailyIncomingGoodsPdfService.cs:117-128`); no hay importador, agencia, manifiesto DIAN, manifiesto preimpreso, peso de manifiesto, total de vehículos ni firmas; mezcla todas las modalidades sin filtro ni columna (`WHQ:GetDailyIncomingGoodsReport/GetDailyIncomingGoodsReportHandler.cs:39-58`).
- **Capa:** backend (DTO) y frontend (tabla, PDF). **Categoría:** FRONTEND / BACKEND.
- **Impacto:** el informe no identifica a qué depósito pertenece cada fila ni sirve como constancia firmada; obliga a cruzar con otros listados.
- **Criticidad:** MEDIA — informe de control diario de uso habitual con datos clave ausentes.
- **Dependencias:** BR-07-003 (fecha del filtro), BR-07-004 (manifiesto), BR-07-001 (Excel). Relación: DEF-F7-004 (Verificado) corrigió peso, placa y tiquete, no estas columnas.
- **Acción recomendada:** confirmar con el negocio la granularidad (camión o producto) y agregar depósito, importador, agencia, manifiesto DIAN, peso de manifiesto, modalidad (o filtro) y firmas en pantalla, PDF y Excel.
- **Criterio de resolución:** el diario de un día con dos depósitos de importación muestra cada depósito con su importador y agencia, sus camiones con manifiesto DIAN y peso, el total de vehículos y las firmas, en pantalla, PDF y Excel.

### BR-07-003 — Informes y exportaciones toman la fecha de creación como fecha de ingreso (DEC-012)

- **ID funcional:** CF-L209, CF-L210.a, CF-L232.
- **Descripción:** DEC-012 define la fecha de ingreso del depósito (`WarehouseStorage.EntryDate`: la de Vigilancia del primer camión, corregible) y DEC-010.4 exige que «todo lleve la fecha del sábado» cuando el camión entra el sábado y se procesa el lunes.
- **Esperado:** kardex, diario de ingresos y Excel de importaciones usan `EntryDate`, como ya lo hacen el inventario general, pólizas, ingresos por producto, abandono y agencias (`REPQ:GetGeneralInventory/GetGeneralInventoryHandler.cs:28-38`; `BE:Wms.Application/Reports/Common/PolicyReleaseQuery.cs:14-20`).
- **Actual:**
  - kardex: `EntryDateTime = serviceRecord.CreatedAt` (`WHQ:GetWarehouseStorageMovements/GetWarehouseStorageMovementsHandler.cs:309`), mostrado como «Fecha ingreso» en pantalla y PDF;
  - diario de ingresos: filtra y muestra `ws.CreatedAt` (`WHQ:GetDailyIncomingGoodsReport/GetDailyIncomingGoodsReportHandler.cs:51-53,81`); el comentario cita QA §10, que solo decide los estados (`docs/qa/00-plan-maestro.md` §10 «Reporte de ingresos diarios»);
  - Excel de importaciones: «Fecha de ingreso» = `createdAt` del depósito de importación (`FE:pages/foreign-trade/imports/index.vue:169`; `BE:Wms.Application/ForeignTrade/Queries/GetImportDeposits/GetImportDepositsHandler.cs:147`).
- **Capa:** backend y frontend. **Categoría:** REGLAS_NEGOCIO.
- **Impacto:** un depósito con fecha corregida (WMS-33) aparece en otro día del diario y con otra fecha en el kardex y en el Excel que en la etiqueta, la TRM y el período de facturación.
- **Criticidad:** MEDIA — contradice una decisión vigente en informes de uso diario; no altera datos.
- **Dependencias:** BR-04-002 del módulo 04 (corrección de la fecha de ingreso). El listado de importaciones es del módulo 04; aquí se registra su exportación.
- **Acción recomendada:** usar `WarehouseStorage.EntryDate` (con `CreatedAt` solo de respaldo) en las tres lecturas.
- **Criterio de resolución:** un depósito con fecha de ingreso corregida al día anterior aparece en el diario de ese día y con esa fecha en el kardex (pantalla y PDF) y en el Excel de importaciones.

### BR-07-004 — «Manifiesto» muestra la carta porte; el kardex no muestra la agencia

- **ID funcional:** CF-L209, CF-L210.a, CF-L210.b.
- **Descripción:** el legacy distingue el manifiesto DIAN (`ingreso.nro_manifiestodian`) del documento comercial (CPI / carta porte, `nro_doccomercial`) en el kardex (`INV:kardex.php:232-260`), el diario de ingresos (`INV:reportediario.php:348-386`) y el de salidas (`INV:reportediariosalidas.php:354-372`); el kardex muestra además la SIA.
- **Esperado:** «Manifiesto» = manifiesto DIAN (`ImportWarehouseStorage.ManifestNumber` o el del camión, como en `REPQ:GetGeneralInventory/GetGeneralInventoryHandler.cs:102-110,155`); agencia en el encabezado del kardex.
- **Actual:** kardex `ManifestNumber = serviceRecord.CargoManifestNumber` y `DocumentNumber` = lo mismo (`WHQ:GetWarehouseStorageMovements/GetWarehouseStorageMovementsHandler.cs:308-310`), sin agencia; diario de ingresos `CargoManifestNumber` y `CommercialDocumentNumber` = carta porte (`BE:Wms.Application/Warehouse/Common/Services/DailyIncomingGoodsRowBuilder.cs:57-59`), columna «Manifiesto»; diario de salidas igual (`WHQ:GetDailyOutgoingGoodsReport/GetDailyOutgoingGoodsReportHandler.cs:179-180`; `FE:pages/reports/daily-outgoing-goods.vue:340-345`). La observación de F11-S3 en DEF-F7-009 ya lo anotó («el encabezado dice "Manifiesto: QA-CP-F11-001" (carta porte)») sin ficha propia.
- **Capa:** backend. **Categoría:** BACKEND.
- **Impacto:** el dato aduanero de control no aparece y la carta porte sale duplicada con un rótulo equivocado.
- **Criticidad:** MEDIA — dato clave para la DIAN en tres informes.
- **Dependencias:** BR-07-002.
- **Acción recomendada:** leer el manifiesto DIAN como el inventario general y agregar la agencia al DTO del kardex.
- **Criterio de resolución:** para un depósito con carta porte `CP-1` y manifiesto DIAN `M-1`, los tres informes muestran `CP-1` como documento y `M-1` como manifiesto, y el kardex muestra la agencia.

### BR-07-005 — Excel incompleto: sin filtros, sin totales, sin firmas y con «undefined»

- **ID funcional:** CF-L232, CF-L211, CF-L215, CF-L209.
- **Descripción:** el plan frontend F5-01 pide fila 2 con los filtros y fila de totales; F5-06 pide las tres firmas al pie del resumen de pólizas; el legacy exportaba la tabla con su fila «Totales».
- **Actual:**
  - `filtersSummary` solo lo pasa la facturación por CPI (`FE:pages/billing/reports/deposit-billing.vue:56`);
  - el Excel del inventario general no pasa `totals` (`FE:pages/reports/general-inventory.vue:113-142`) y el del detalle de pólizas tampoco (`FE:pages/reports/policies.vue:108-142`);
  - el resumen de pólizas pasa `footerLines` (`policies.vue:105`), pero `exportRowsToExcel` en modo de una hoja no los copia (`FE:utils/excel-export.ts:158-166`): las firmas no salen;
  - la fila de totales del resumen escribe «undefined» en «Mes»: `MONTH_NAMES[m.month - 1] ?? String(m.month)` con `m = totals` (`policies.vue:99`);
  - el Excel del kardex no lleva el encabezado del depósito (importador, TRM, fechas) (`FE:pages/reports/warehouse-movements.vue:181-243`).
- **Capa:** frontend. **Categoría:** FRONTEND.
- **Impacto:** archivos sin contexto del filtro, sin cuadre y, en pólizas, sin el espacio de firmas del legacy.
- **Criticidad:** BAJA — los datos están; falta presentación.
- **Dependencias:** BR-07-006.
- **Acción recomendada:** incluir `footerLines` en la hoja única, pasar `filtersSummary` y `totals` en cada informe, usar un valor fijo («Total») en la primera columna de totales.
- **Criterio de resolución:** el Excel del inventario general y del detalle de pólizas termina con la fila de totales; el resumen de pólizas muestra «Total» y las tres firmas; cada informe trae su fila de filtros.

### BR-07-006 — Informes sin PDF ni impresión (y sin firmas)

- **ID funcional:** CF-L231.a, CF-L215.
- **Descripción:** en el legacy todos los informes tenían PDF e Imprimir con encabezado, pie y numeración (`bodegas-legacy/reportes/crearpdf.php`; iconos en cada informe de `INV:`), y varios eran constancias con firmas (póliza, diarios, nacionalizados).
- **Actual:** solo el kardex y los dos diarios tienen PDF (`BE:Wms.Api/Controllers/v1/WarehouseMovementsReportController.cs:63-82`; `ReportController.cs:76-91,130-147`). Inventario general, pólizas, abandono, nacionalizados (vía inventario o importaciones), ingresos por producto y agencias solo tienen Excel; ninguno imprime firmas. Para pólizas el plan backend F5-06 regla 4 dice que «las firmas las agrega el frontend si imprime», y el frontend no imprime.
- **Capa:** frontend y backend. **Categoría:** FRONTEND / BACKEND.
- **Impacto:** el informe de póliza no se puede entregar firmado como en el legacy sin rearmarlo a mano.
- **Criticidad:** BAJA — hay alternativa (imprimir el Excel); se eleva si el negocio confirma que la póliza se entrega firmada.
- **Dependencias:** BR-07-005.
- **Acción recomendada:** confirmar con el negocio qué informes se imprimen; como mínimo, imprimir la póliza con sus firmas.
- **Criterio de resolución:** decisión registrada; los informes que el negocio confirme tienen PDF o impresión con sus firmas.

### BR-07-007 — El botón genérico «Exportar» de `AppTable` exporta solo la página

- **ID funcional:** CF-L232.
- **Descripción:** `FE:components/app/AppTable.vue:260-265,470-475` muestra por defecto «Exportar» y llama `exportCSV` de PrimeVue, que exporta las filas cargadas. En tablas `lazy` es solo la página: historial de Vigilancia (`FE:pages/operations/entries/history.vue:268`), auditoría (`FE:pages/admin/audit/index.vue:142`) y maestros.
- **Esperado:** exportación completa (GAP-017; DF12: Excel con la utilidad común y `all=true`).
- **Actual:** CSV parcial sin aviso; ya anotado y no corregido (`docs/planes/paridad-legacy/plan-frontend-paridad-legacy.md` §G.8).
- **Capa:** frontend. **Categoría:** FRONTEND.
- **Impacto:** archivos incompletos sin aviso.
- **Criticidad:** BAJA — pantallas de maestros y consulta, no informes legacy.
- **Dependencias:** —.
- **Acción recomendada:** ocultar el botón en tablas `lazy` o reemplazarlo por la utilidad común con `all=true`.
- **Criterio de resolución:** ninguna tabla paginada en servidor ofrece una exportación que traiga solo la página.

### BR-07-008 — Sin informe por producto de mercancía nacionalizada o pendiente

- **ID funcional:** CF-L213.
- **Descripción:** el legacy tenía «M/cia Nacionalizada» (productos con nacionalizado > 0 y sus levantes) y «M/cia Sin Nacionalizar» (productos con saldo > 0 y pendiente > 0) (`INV:reportenacionalizados.php:50-75,329-374`; `INV:reportesinnacionalizar.php:305-337`).
- **Actual:** no hay informe equivalente ni está en el mapa del plan (`docs/planes/paridad-legacy/plan-backend-paridad-legacy.md` §C.5.0). Se aproxima con el listado de importaciones (filtro de estado del depósito, donde un levante parcial ya cuenta como «Nacionalizado»: `BE:Wms.Application/ForeignTrade/Queries/GetImportDeposits/GetImportDepositsHandler.cs:38-39`) y con el inventario general (columnas Entran / Nalzdos. / Saldo y levantes, sin filtro por pendiente: `REPQ:GetGeneralInventory/GetGeneralInventoryQuery.cs:18-33`). Términos buscados: `nacionaliz`, `PendingToNationalize`, `SinNacionalizar`, `Nationalized` en `BE:Wms.Application/Reports`, `FE:pages/reports`, `FE:components/layout/AppMenu.vue`.
- **Capa:** frontend y backend. **Categoría:** FRONTEND / BACKEND.
- **Impacto:** CE no obtiene en un paso la lista de productos pendientes de nacionalizar (sí la de abandono, desde 30 días).
- **Criticidad:** BAJA — se puede reconstruir desde el inventario general.
- **Dependencias:** —.
- **Acción recomendada:** confirmar con el negocio; si se necesita, agregar al inventario general un filtro «pendiente de nacionalizar» / «nacionalizado».
- **Criterio de resolución:** decisión registrada o filtro que lista solo productos con pendiente > 0 (o nacionalizado > 0), con Excel.

### BR-07-009 — El detalle de pólizas no trae el valor de la mercancía ni el total por depósito

- **ID funcional:** CF-L215.
- **Descripción:** el detalle legacy es una fila por depósito con «Val. M/cia. (FOB)» (valor del depósito, `vista_poliza.FOB`) y «Tot. CIF» (suma de sus levantes) (`INV:reportepolizadetalle.php:314-332,440-500`).
- **Actual:** una fila por levante de producto con su FOB y el total general (`REPQ:GetPoliciesDetail/GetPoliciesDetailHandler.cs:27-97`; `BE:Wms.Application/Reports/Common/DTOs/PolicyReportDtos.cs`); no hay valor de la mercancía del depósito ni subtotal por depósito.
- **Capa:** backend. **Categoría:** BACKEND.
- **Impacto:** no se compara el valor declarado del depósito con lo levantado.
- **Criticidad:** BAJA.
- **Dependencias:** pendiente 8 de `docs/contexto/estado.md` §4 (FOB/CIF de la migración sin validar).
- **Acción recomendada:** confirmar con el negocio; agregar `cargoValue` del depósito y subtotal por depósito si se usa.
- **Criterio de resolución:** el detalle muestra por depósito el valor de la mercancía y la suma de FOB de sus levantes, o la decisión de no hacerlo queda registrada.

### BR-07-010 — Inventario general: ubicaciones sin cantidad y rango de fechas opcional

- **ID funcional:** CF-L211, CF-L172.c.
- **Descripción:** «Bodega(s)» del legacy dice cuántas unidades hay en cada bodega («(3) en Bodega 2», `INV:reportegeneral.php:620-645`; `L:modulos/mod_bodegas/reportegeneral.php:567-570`); el informe de CE exige siempre el rango de fechas (`INV:reportegeneral.php:118-131`).
- **Actual:** «Bodega(s)» lista solo los códigos de ubicación (`REPQ:GetGeneralInventory/GetGeneralInventoryHandler.cs:121-125,142-160`); con «Con saldo» las fechas son opcionales (`GetGeneralInventoryQueryValidator.cs:13-17`). La segunda diferencia coincide con la variante de Bodega del legacy, pero no hay decisión escrita para el informe de CE.
- **Capa:** backend. **Categoría:** REGLAS_NEGOCIO.
- **Impacto:** Bodega no ve el reparto de cantidades por ubicación en el informe (sí en Inventario › Ubicaciones, módulo 03).
- **Criticidad:** BAJA.
- **Dependencias:** CF-L172 del módulo 03.
- **Acción recomendada:** confirmar con el negocio; mostrar la cantidad por ubicación (`Placements`).
- **Criterio de resolución:** «Bodega(s)» muestra «código (cantidad)» por ubicación, y la regla de fechas queda decidida.

### BR-07-011 — Detalle por agencia: salidas sin producto y pesajes sin cantidad

- **ID funcional:** CF-L229.b.
- **Descripción:** el detalle legacy lista pesajes con fecha, placa y **cantidad** con su total (`L:reportesweb/reportesiasdetalle.php:369-393`) y salidas por carga (`:442-447`).
- **Actual:** el DTO de salidas trae `ProductName` (`BE:Wms.Application/Reports/Common/DTOs/CustomsAgencyReportDtos.cs`; `REPQ:GetCustomsAgencyEntryDetail/GetCustomsAgencyEntryDetailHandler.cs:96,130`), pero `ICustomsAgencyExitDto` no lo declara (`FE:features/reports/types/customs-agency-entries.ts`) y la tabla no lo muestra (`FE:pages/reports/customs-agency-entries.vue:220-225`): con dos productos, las filas de salida no se distinguen. Los pesajes muestran bruto, tara y neto, no la cantidad ingresada. Las imágenes de novedades del legacy no se replican (fotos por recepción, módulo 03, CF-L178).
- **Capa:** integración (contrato). **Categoría:** CONTRATOS_API.
- **Impacto:** detalle ambiguo en depósitos con varios productos.
- **Criticidad:** BAJA.
- **Dependencias:** —.
- **Acción recomendada:** agregar `productName` al tipo y a la tabla; confirmar si la cantidad por pesaje hace falta.
- **Criterio de resolución:** en un depósito con dos productos, cada salida del detalle muestra su producto.

### BR-07-012 — Código de barras Code 39 en el depósito y la guía (legacy Code 128)

- **ID funcional:** CF-L258.
- **Descripción:** el legacy usa Code 128 en guía, autorización de cargue, depósito y adhesivos (`L:includes/barcode/code128.php:1-30`; invocadores en `L:modulos/mod_salidas/verguia.php:268`, `mod_depositos/verdeposito.php:207`, `adhesivos.php:276`).
- **Actual:** Code 128 en etiquetas (`BE:Wms.Application/ForeignTrade/Common/Services/LabelGenerationService.cs:845`), **Code 39** en el PDF del depósito (`DepositPdfService.cs:161-162,546-567`) y en el de la guía (`DispatchGuidePdfService.cs:344-345,784-805`), con el código duplicado. `MIGRATION_MATRIX.md` (LEGACY-FUNC-258) afirma «Code128 en etiquetas, depósito y guía».
- **Capa:** backend. **Categoría:** REGLAS_NEGOCIO.
- **Impacto:** si algún lector o proceso externo espera Code 128, no leerá el depósito ni la guía.
- **Criticidad:** BAJA — no hay evidencia de lectores configurados.
- **Dependencias:** —.
- **Acción recomendada:** confirmar con el negocio; unificar en Code 128 con un generador compartido.
- **Criterio de resolución:** decisión registrada o los tres documentos usan la misma simbología.

### BR-07-013 — Kardex: sin autocompletar, sin búsqueda por número legacy y sin menú en Bodega

- **ID funcional:** CF-L209.
- **Descripción:** el kardex legacy sugiere depósitos al digitar (`INV:kardex.php:133`, CF-L241).
- **Actual:** texto libre con el ejemplo de un formato que ya no se usa (`DEP-20260304-0002`, `FE:pages/reports/warehouse-movements.vue:257-264`; `BE:Wms.Api/Controllers/v1/WarehouseMovementsReportController.cs:29`); el número legacy de los depósitos migrados (`LegacyNumber`) no se expone en ningún DTO (solo en `BE:Wms.Application/Administration/LegacyImport/*`), así que tras el corte no se puede pedir el kardex con el número antiguo (ya anotado en `plan-frontend-paridad-legacy.md` §G.12); la página admite el rol Warehouse pero el menú de Bodega no la enlaza (`FE:components/layout/AppMenu.vue:242-310`).
- **Capa:** frontend. **Categoría:** FRONTEND.
- **Impacto:** búsqueda lenta y propensa a errores; operarios con el número legacy en papel no encuentran el depósito.
- **Criticidad:** BAJA.
- **Dependencias:** módulo 08 (migración); módulo 04 (búsqueda de depósitos).
- **Acción recomendada:** selector de depósito con búsqueda (incluido el número legacy) y entrada de menú en Bodega.
- **Criterio de resolución:** desde Bodega se abre el kardex por menú y se encuentra un depósito migrado por su número legacy.


---

## Decisiones posteriores (2026-10-23)

> Nota del orquestador. Después de esta auditoría, el usuario respondió las preguntas al negocio (`docs/contexto/decisiones.md`, DEC-050…054; `06-brechas-priorizadas.md` §3.1). El registro de arriba es la foto previa y no se reescribe. El estado vigente está en `06-brechas-priorizadas.md` y `04-matriz-global.csv`.

| Brecha | Estado | Decisión |
| --- | --- | --- |
| BR-07-002 | Abierta: se construye (requiere plan cerrado) | DEC-054 |
