# 07-reportes-exportaciones — 05 Análisis V2

> AG-07 · 2026-10-23 · Auditoría estática del código en disco (según `docs/contexto/estado.md`: BE `35a61b2` / FE `c924a8b`). Rutas relativas a `code_workspace/`.
> **Prefijos:** `FE:` = `Frontend/wms/app/`; `BE:` = `Backend/wms-api/`; `CTRL:` = `Backend/wms-api/Wms.Api/Controllers/v1/`; `REPQ:` = `Backend/wms-api/Wms.Application/Reports/Queries/`; `WHQ:` = `Backend/wms-api/Wms.Application/Warehouse/Queries/`.

## 1. Frontend

### 1.1 Páginas

| Página | `requiredRoles` | Menú | Qué hace | Exportación | Evidencia |
| --- | --- | --- | --- | --- | --- |
| `FE:pages/reports/warehouse-movements.vue` (kardex) | Admin, Warehouse, ForeignTrade, Billing | CE › Reportes › «Movimientos por Depósito»; Facturación › «Movimientos por depósito». **Bodega no tiene entrada** | Número de depósito (texto libre, placeholder `DEP-20260304-0002`), rango opcional; encabezado, tabla por producto con saldos, levantes, despachos y movimientos | PDF del backend; Excel con 4 hojas (Productos con totales, Levantes, Despachos, Movimientos) | `:18-24`, `:67-90`, `:132-243`, `:330-390`; `FE:components/layout/AppMenu.vue:404-406,513-515` |
| `FE:pages/reports/daily-incoming-goods.vue` | Admin, ForeignTrade | CE › Reportes › «Mercancías ingresadas (diario)» | Rango obligatorio; tabla de filas por producto; totales | **Solo PDF** | `:11`, `:66-120`, `:240-279`; `AppMenu.vue:409-411` |
| `FE:pages/reports/daily-outgoing-goods.vue` | Admin, ForeignTrade | CE › Reportes › «Salida de mercancía (diario)» | Rango, cliente y mercancía; tabla | **Solo PDF** | `:12`, `:287-360`; `AppMenu.vue:414-416` |
| `FE:pages/reports/general-inventory.vue` | Admin, ForeignTrade, Warehouse, Billing | CE › Reportes, Bodega y Facturación › «Inventario general» | Saldo, rango, importador, agencia, transportadora, producto, modalidad, ubicación, levantes; totales en pie de tabla | Excel `all=true` **sin fila de totales ni de filtros** | `:19`, `:47-55`, `:100-142`, `:303-346`; `AppMenu.vue:306-309,431-433,508-510` |
| `FE:pages/reports/policies.vue` | Admin, ForeignTrade | CE › Reportes › «Informe de póliza» | Año; 12 meses FOB UAP / no UAP / total; detalle del mes con filtro UAP | Excel resumen (las firmas `footerLines` **no se escriben**; la fila de totales escribe «undefined» en «Mes») y detalle (**sin total de FOB**) | `:15`, `:90-142`, `:195-309`; `FE:utils/excel-export.ts:158-166` |
| `FE:pages/reports/abandonment-candidates.vue` | Admin, ForeignTrade | CE › Reportes › «Mercancía en abandono» | Importador opcional; totales | Excel con totales | `:16`, `:56-82`, `:175-180` |
| `FE:pages/reports/abandonment-exits.vue` | Admin, ForeignTrade | CE › Reportes › «Salidas a destino de abandono» | Rango (1-ene a hoy) | Excel | `:15`, `:70-93` |
| `FE:pages/reports/incoming-by-product.vue` | Admin, ForeignTrade | CE › Reportes › «Ingresos por producto» | Rango e importador obligatorios, producto | Excel con total | `:15`, `:80-93`, `:189-192` |
| `FE:pages/reports/customs-agency-entries.vue` | Admin, ForeignTrade | CE › Reportes › «Ingresos por agencia de aduanas» | Agencia obligatoria; diálogo con pesajes, novedades (imprimir) y salidas | Excel del listado | `:18`, `:80-95`, `:163-225` |
| `FE:pages/reports/statistics.vue` | Admin, ForeignTrade | **Oculta** (`redirect: "/"`) | Estadísticas por período | — | `:12-18`; `AppMenu.vue:43`; `docs/contexto/contexto-negocio-wms-para-ia.md:461` |
| `FE:pages/billing/reports/annual.vue` | Admin, Billing | Facturación › «Facturación anual» | Año y servicio; meses y días | Excel (una fila por día) con totales | `:18`, `:27-31`, `:70-82`; `AppMenu.vue:496-498` |
| `FE:pages/billing/reports/deposit-billing.vue` | Admin, Billing | Facturación › «Facturación por CPI» | Depósito; encabezado, productos, salidas, facturas | Excel de 3 hojas con fila de filtros y total | `:19`, `:50-90`; `AppMenu.vue:502-504` |

Los informes de facturación (`FE:pages/billing/reports/*`) se evaluaron **solo en forma, columnas y exportación**: el directorio `modulos/06-facturacion/` no existía al cerrar este módulo; el cálculo es del módulo 06.

### 1.2 Utilidad común de Excel (DF12, F5-01)

- `FE:utils/excel-export.ts`: carga `exceljs` con `await import("exceljs")` (`:155`); fila 1 «BODEGAS ASOCIADAS — {title}» (`:82-86`), fila 2 de filtros si se pasa `filtersSummary` (`:88-92`), encabezados en negrita con filtro automático (`:94-96,127-130`), números como números y fechas en hora de Colombia (`:63-76`, CHG-83), totales en negrita (`:106-115`), líneas al pie (`:117-123`), varias hojas (`:32-36`). **Defecto:** en modo de una sola hoja arma la hoja con `sheetName/title/filtersSummary/columns/rows/totals` y **omite `footerLines`** (`:158-166`).
- `FE:composables/useExcelExport.ts:12-30`: `fetchAll` con `all: true`; avisos «No hay datos para exportar.» y «Excel generado: {n} filas».
- `filtersSummary` solo lo usa `FE:pages/billing/reports/deposit-billing.vue:56` (búsqueda en `FE:pages` y `FE:features`).
- `package.json` declara `exceljs` `^4.4.0`; no quedan `XLSX`, `useExportImportsToExcel` ni `exportInventoryMovementsToExcel` (búsquedas en `Frontend/wms/app`).
- `FE:components/app/AppTable.vue:260-265,470-475`: botón genérico «Exportar» (por defecto visible) con `exportCSV` de PrimeVue: en tablas `lazy` (p. ej. `FE:pages/operations/entries/history.vue:268`, `FE:pages/admin/audit/index.vue:142`) exporta solo la página cargada. Solo `admin/cities` y `admin/crews` lo ocultan.

### 1.3 Exportaciones de listados (F5-11) y `all=true`

Todas piden `all: true` sin `pageIndex` ni `pageSize`: `FE:pages/foreign-trade/imports/index.vue:147`, `exports/index.vue:100`, `inspections/index.vue:71`, `loading-orders/index.vue:89`, `dispatch-guides/index.vue:218`, `releases/index.vue:74`, `abandonment/index.vue:136`, `FE:pages/billing/invoices/index.vue:137`, `FE:pages/warehouse/novelties/index.vue:83`, `FE:pages/operations/weighbridge/history.vue:109,115`, `FE:features/warehouse/composables/useWarehouseExports.ts:17`, y los siete informes de `FE:pages/reports/`. Ninguna sube `pageSize` (búsqueda `pageSize: *[0-9]{3,}`: solo `warehouse/inventory/index.vue:55` y `WarehouseDepositSelect.vue:39` con 100, que el API recorta a 50; no son exportaciones).

Observación: el Excel de importaciones rotula «Fecha de ingreso» el `createdAt` del depósito de importación (`FE:pages/foreign-trade/imports/index.vue:169`; `BE:Wms.Application/ForeignTrade/Queries/GetImportDeposits/GetImportDepositsHandler.cs:147`), no `WarehouseStorage.EntryDate` (DEC-012). Ver BR-07-003.

## 2. Backend

### 2.1 Endpoints

| Verbo y ruta (`/api/v1`) | Controlador · política | Consulta / handler | Respuesta | `all` |
| --- | --- | --- | --- | --- |
| `GET warehouse/movements-report` | `CTRL:WarehouseMovementsReportController.cs:35-52` · `ActiveUser` + `InventoryReportAccess` | `WHQ:GetWarehouseStorageMovements/GetWarehouseStorageMovementsHandler.cs` | `WarehouseStorageMovementsReportDto` (encabezado, productos con saldos y movimientos, `releases`, `dispatches`, `totals`); 404 si no existe | No paginado |
| `GET warehouse/movements-report/pdf` | ídem `:63-82` | `WarehouseMovementsPdfService` (QuestPDF) | PDF con secciones INGRESO, NACIONALIZADOS, POR NACIONALIZAR, DESPACHADOS, EXISTENCIAS (`BE:Wms.Application/Warehouse/Common/Services/WarehouseMovementsPdfService.cs:84-97,247-321`) | — |
| `GET reports/daily-incoming-goods` y `/pdf` | `CTRL:ReportController.cs:56-91` · `ForeignTradeAccess` | `WHQ:GetDailyIncomingGoodsReport/*`; `DailyIncomingGoodsPdfService` | `DailyIncomingGoodsReportDto` (filas y totales) | No paginado (todas las filas) |
| `GET reports/daily-outgoing-goods` y `/pdf` | `CTRL:ReportController.cs:106-147` · `ForeignTradeAccess` | `WHQ:GetDailyOutgoingGoodsReport/*`; `DailyOutgoingGoodsPdfService` | `DailyOutgoingGoodsReportDto` | No paginado |
| `GET reports/statistics` | `CTRL:ReportController.cs:157-168` · `ForeignTradeAccess`; bloque de facturación solo Admin (CHG-80) | `REPQ:GetOperationalStatistics/*` | `OperationalStatisticsDto` | — |
| `GET reports/traceability` | `CTRL:ReportController.cs:36-45` | `REPQ:GetTraceabilityDashboard/*` | (CF-V034, módulo 03) | — |
| `GET reports/general-inventory` | `CTRL:InventoryReportsController.cs:33-43` · `ActiveUser` + `InventoryReportAccess` | `REPQ:GetGeneralInventory/*` (validador) | `data: { items, totals }` + `pagination` | Sí |
| `GET reports/general-inventory/locations` | `:51-59` · `InventoryReportAccess` | `GetWarehouseLocationsQuery` | Lista de ubicaciones | — |
| `GET reports/incoming-by-product` | `:67-77` · `ActiveUser` + `ForeignTradeAccess` | `REPQ:GetIncomingByProduct/*` | `{ items, totals }` | Sí |
| `GET reports/policies`, `GET reports/policies/detail` | `CTRL:PolicyReportsController.cs:25-46` · `ForeignTradeAccess` | `REPQ:GetPoliciesSummary/*`, `GetPoliciesDetail/*` | `PolicySummaryDto`; `{ items, totals }` | Detalle sí |
| `GET reports/abandonment-candidates`, `GET reports/abandonment-exits` | `CTRL:AbandonmentReportsController.cs:25-48` · `ForeignTradeAccess` | `REPQ:GetAbandonmentCandidates/*`, `GetAbandonmentExits/*` | `{ items, totals }`; lista paginada | Sí (`request.All` en memoria, `CreateAsync`) |
| `GET reports/customs-agency-entries`, `GET reports/customs-agency-entries/{id}` | `CTRL:CustomsAgencyReportsController.cs:27-52` · `ForeignTradeAccess` | `REPQ:GetCustomsAgencyEntries/*`, `GetCustomsAgencyEntryDetail/*` | lista; detalle (404 si no es de la agencia) | Listado sí |
| `GET reports/billing-annual`, `GET reports/deposit-billing` | `CTRL:BillingReportsController.cs:28-53` · `BillingAccess` | `REPQ:GetBillingAnnual/*`, `GetDepositBilling/*` | `BillingAnnualReportDto`; `DepositBillingReportDto` | — |
| `GET foreign-trade/warehouse-storages/{id}/label-prints` | `CTRL:LabelPrintsController.cs:20-25` · `ForeignTradeAccess` | `GetLabelPrintsQuery` (últimas 50) | conteos y lista (acción, usuario, fecha) | — |

Paginación: `BE:Wms.Common/Wrappers/QueryParametersBase.cs:20-32` (`All` → `PageIndex=1`, `PageSize=int.MaxValue`; tope 50 sin `All`) y `BE:Wms.Application/Common/Models/PaginatedList.cs` (normaliza `int.MaxValue` al total). Los handlers aplican `Skip((PageIndex−1)·PageSize).Take(PageSize)` o `CreateAsync` (verificado en los 13 handlers de §4). Las consultas pasan por `ValidationBehavior` (`BE:Wms.Api/Program.cs:46`).

### 2.2 Generación de PDF y código de barras

- QuestPDF `2025.12.4` + SkiaSharp (`BE:Wms.Api/Wms.Api.csproj`, `BE:Wms.Application/Wms.Application.csproj`). PDF de informes: kardex, diario de ingresos y diario de salidas; el resto de documentos (tiquete, etiqueta, depósito, guía, factura, orden de trabajo, novedad) pertenece a sus módulos.
- Informes **sin PDF** en V2: inventario general, pólizas, abandono (dos), ingresos por producto, agencias, facturación anual y por CPI (solo Excel).
- Código de barras: Code 128 propio en etiquetas (`BE:Wms.Application/ForeignTrade/Common/Services/LabelGenerationService.cs:83,845-896`); **Code 39** en el PDF del depósito (`DepositPdfService.cs:161-162,546-567`) y de la guía (`DispatchGuidePdfService.cs:344-345,784-805`), con la tabla de patrones duplicada en los dos servicios.

### 2.3 Reglas y lecturas destacadas

- Kardex: encabezado `EntryDateTime = serviceRecord.CreatedAt`, `ManifestNumber = serviceRecord.CargoManifestNumber`, `DocumentNumber = CargoManifestNumber`, sin agencia (`WHQ:GetWarehouseStorageMovements/GetWarehouseStorageMovementsHandler.cs:301-311`); importador del rol IMPORTER o el cliente (`:56-60`); secciones con `KardexAggregator` y `DepositDispatchReader` (`:322-351`), independientes del rango de fechas de los movimientos (`:70-77`).
- Diario de ingresos: `Confirmed`/`Closed` por `ws.CreatedAt` (`WHQ:GetDailyIncomingGoodsReport/GetDailyIncomingGoodsReportHandler.cs:36-58`), una fila por producto con placas, tiquetes y transportadoras unidas y el neto físico en la primera fila (`BE:Wms.Application/Warehouse/Common/Services/DailyIncomingGoodsRowBuilder.cs:28-73`); sin modalidad, depósito visible, importador ni agencia; `TimeZoneInfo` propio en vez de `ColombiaTime` (`:14-34`).
- Diario de salidas: órdenes `Dispatched`/`Complete` por fecha de salida → guía → fin de cargue (`WHQ:GetDailyOutgoingGoodsReport/GetDailyOutgoingGoodsReportHandler.cs:66-117`); `CommercialDocumentNumber` y `CargoManifestNumber` son ambos la carta porte (`:179-180`).
- Inventario general: filtros y totales sobre todo el filtro (`REPQ:GetGeneralInventory/GetGeneralInventoryHandler.cs:21-86`); manifiesto DIAN del depósito de importación o del primer camión (`:102-110,155`); ubicaciones como códigos (`:121-125,142-160`).
- Pólizas: `PolicyReleaseQuery` (`BE:Wms.Application/Reports/Common/PolicyReleaseQuery.cs:14-30`); detalle por levante (`REPQ:GetPoliciesDetail/GetPoliciesDetailHandler.cs:27-97`).
- Agencias: visibilidad 13 h (`BE:Wms.Application/Reports/Common/CustomsAgencyVisibility.cs`); detalle con `ProductName` en las salidas (`REPQ:GetCustomsAgencyEntryDetail/GetCustomsAgencyEntryDetailHandler.cs:96,130`).
- Solo lectura: ningún handler de `REPQ:` ni los de informes de `WHQ:` llama a `SaveChanges` (búsqueda `grep -rln SaveChanges`).

## 3. Integración y contratos (DTO ↔ TS)

| Informe | DTO | Tipo TS | Resultado |
| --- | --- | --- | --- |
| Kardex | `BE:Wms.Application/Warehouse/Common/DTOs/WarehouseStorageMovementsReportDto.cs` | `FE:features/reports/types/index.ts` (§ CE-14a) | Coincide en lo que la pantalla lee |
| Diarios | `DailyIncomingGoodsReportRowDto.cs`, `DailyOutgoingGoodsReportRowDto.cs` | `FE:features/reports/types/daily-*.ts` | `warehouseStorageNumber` llega en ingresos pero la tabla y el PDF no lo muestran |
| Inventario general | `BE:Wms.Application/Reports/Common/DTOs/GeneralInventoryRowDto.cs` | `FE:features/reports/types/general-inventory.ts` | Coincide; `warehouseStorageId` y `warehouseStorageProductId` no se tipan (no se usan) |
| Pólizas | `PolicyReportDtos.cs` | `policies.ts` | Coincide (nulabilidad de `fobUsd` y `importerName` más estricta en TS) |
| Ingresos por producto | `IncomingByProductDtos.cs` | `incoming-by-product.ts` | Coincide |
| Agencias | `CustomsAgencyReportDtos.cs` | `customs-agency-entries.ts` | **`ICustomsAgencyExitDto` no tiene `productName`** (el DTO sí, `CustomsAgencyExitDto`): las salidas se listan sin producto. El listado no tipa `warehouseStorageNumber` |
| Abandono | `AbandonmentCandidateDto.cs`, `AbandonmentExitDto.cs` | `abandonment-reports.ts` | Coincide |
| Estadísticas | `OperationalStatisticsDto.cs` | `FE:features/reports/types/index.ts:1-60` | Coincide; `billing` nulo para no Admin |
| Facturación | `BillingReportDtos.cs` | `FE:features/billing/types/billing-reports.ts` | Coincide; enums como texto (`JsonStringEnumConverter`, `BE:Wms.Api/Program.cs:63`) |

Prefijo `/api/v1`: `NUXT_PUBLIC_API_BASE` (`Frontend/wms/.env.example:2`, `Frontend/wms/nuxt.config.ts:31`); `api.get(path, query)` envía la consulta como `params` (`FE:composables/useApi.ts:21-23`).

## 4. Endpoints de exportación y su paginación (verificado)

`GetImportDepositsQuery`, `GetExportDepositsQuery`, `GetInspectionDepositsQuery`, `GetLoadingOrdersQuery`, `GetDispatchGuidesQuery` (constructor con 20 por defecto), `GetInvoicesQuery`, `GetNoveltiesQuery`, `GetReleasesQuery`, `GetAbandonmentListQuery`, `GetWeighbridgeHistoryQuery`, `GetInventoryMovementsQuery`, `GetCustomsAgencyEntriesQuery`, `GetAbandonmentExitsQuery` heredan de `QueryParametersBase` y sus handlers pasan `PageIndex/PageSize` (búsqueda por clase en `BE:Wms.Application`). `GetGeneralInventoryQuery`, `GetIncomingByProductQuery`, `GetPoliciesDetailQuery` y `GetAbandonmentCandidatesQuery` también.

## 5. Endpoints sin consumidor y llamadas sin endpoint

- Sin consumidor alcanzable: `GET reports/statistics` (la página redirige a `/` por decisión del usuario, `FE:pages/reports/statistics.vue:12-18`). No es defecto: es una pantalla oculta.
- Todas las llamadas de `FE:features/reports/services/reports-service.ts` y de los informes de `FE:features/billing/services/billing-service.ts:283,292` tienen endpoint. No se encontraron llamadas sin endpoint en el módulo.

## 6. Datos simulados

Ninguno: búsqueda `mock|Mock|faker|sampleData|dummy` en `FE:features/reports`, `FE:pages/reports`, `FE:pages/billing/reports` sin resultados; todas las pantallas consumen el API.

## 7. SOLO_V2

| ID | Capacidad | Estado | Evidencia |
| --- | --- | --- | --- |
| CF-V070 | Estadísticas operativas (báscula, bodega, facturación, CE) | Confirmada como SOLO_V2; pantalla oculta del menú y con `redirect: "/"`; API activo | `FE:pages/reports/statistics.vue:12-18`; `CTRL:ReportController.cs:157-168`; `REPQ:GetOperationalStatistics/GetOperationalStatisticsHandler.cs` |
| CF-V071 | «Movimientos de bodega» (`WarehouseMovementsReportController`) | **Reasignada a CF-L209**: es el kardex del legacy (CE-14a ampliado con F5-04) | `CTRL:WarehouseMovementsReportController.cs:12-20`; plan backend §C.5.0 |

No se encontraron otras capacidades `SOLO_V2` propias del módulo (el tablero de trazabilidad es CF-V034, módulo 03; el reporte diario de facturación de báscula, módulo 02).
