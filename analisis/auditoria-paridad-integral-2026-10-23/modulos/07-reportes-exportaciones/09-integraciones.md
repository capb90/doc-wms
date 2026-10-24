# 07-reportes-exportaciones — 09 Integraciones

> AG-07 · 2026-10-23 · Auditoría estática (trazas leídas en código, no ejecutadas). Rutas relativas a `code_workspace/`.
> **Prefijos:** `FE:` = `Frontend/wms/app/`; `CTRL:` = `Backend/wms-api/Wms.Api/Controllers/v1/`; `REPQ:` = `Backend/wms-api/Wms.Application/Reports/Queries/`; `WHQ:` = `Backend/wms-api/Wms.Application/Warehouse/Queries/`.
> Base del API: `NUXT_PUBLIC_API_BASE` = `…/api/v1` (`Frontend/wms/nuxt.config.ts:31`); `api.get(path, query)` envía `query` como parámetros (`FE:composables/useApi.ts:21-23`); errores con el interceptor global.

## 1. Traza común de exportación a Excel (DF12)

```
Botón «Exportar Excel» (página)
 → useExcelExport().run(fetchAll, opciones)            FE:composables/useExcelExport.ts:12-30
   → fetchAll(): servicio(...filtros, all: true, pageIndex: undefined, pageSize: undefined)
     → GET /api/v1/<endpoint>?<filtros>&all=true
       → [Authorize(Policy)] → MediatR → ValidationBehavior (Backend/wms-api/Wms.Api/Program.cs:46)
         → Query : QueryParametersBase (All → PageIndex 1, PageSize int.MaxValue)  Backend/wms-api/Wms.Common/Wrappers/QueryParametersBase.cs:20-32
           → handler: Skip(0).Take(int.MaxValue) o PaginatedList.CreateAsync     Backend/wms-api/Wms.Application/Common/Models/PaginatedList.cs
           ← ApiResponse { data: items | { items, totals }, pagination (pageSize = total) }
   → exportRowsToExcel(opciones + rows)                FE:utils/excel-export.ts:154-175
     → import("exceljs") → hoja(s) → writeBuffer → descarga {fileName}_{yyyyMMdd}.xlsx
   ← toast «Excel generado: n filas» / «No hay datos para exportar.» / «No se pudo generar el Excel.»
```

Puntos de falla observados: `footerLines` se pierde en hoja única (`FE:utils/excel-export.ts:158-166`); las páginas no pasan `filtersSummary` (salvo CPI) y dos no pasan `totals` (BR-07-005).

## 2. Kardex (CF-L209)

```
FE:pages/reports/warehouse-movements.vue:67-90 (onSearch: número + rango Colombia, CHG-77)
 → useWarehouseStorageMovements(filters)  clave ["warehouse-movements-report", …]
   → reports-service.ts:42-50 → GET /api/v1/warehouse/movements-report?warehouseStorageNumber&fromDate&toDate
     → CTRL:WarehouseMovementsReportController.cs:35-52 (ActiveUser + InventoryReportAccess)
       → WHQ:GetWarehouseStorageMovements/GetWarehouseStorageMovementsHandler.cs
          · depósito por número (mayúsculas), importador IMPORTER o cliente (:29-60)
          · movimientos por rango y enriquecimiento con orden/guía/tiquete o recepción/entrada (:62-258)
          · secciones: KardexAggregator + DepositDispatchReader + ImportReleases (:322-351)
       ← WarehouseStorageMovementsReportDto (404 si no existe)
 → «Exportar PDF»: reports-service.ts:52-74 → GET …/movements-report/pdf → WarehouseMovementsPdfService (QuestPDF)
 → «Exportar Excel»: exportRowsToExcel con 4 hojas (warehouse-movements.vue:155-243), datos ya cargados (no vuelve a consultar)
```

## 3. Diarios (CF-L210)

```
FE:pages/reports/daily-incoming-goods.vue → reports-service.ts:76-84 → GET /api/v1/reports/daily-incoming-goods?dateFrom&dateTo
 → CTRL:ReportController.cs:56-67 (ForeignTradeAccess) → WHQ:GetDailyIncomingGoodsReport (validador + handler :36-114)
 ← DailyIncomingGoodsReportDto { rows, totalRows, totalQuantity, totalNetWeightKg }  (no paginado)
 → PDF: reports-service.ts:86-110 → GET …/daily-incoming-goods/pdf → DailyIncomingGoodsPdfService
FE:pages/reports/daily-outgoing-goods.vue → reports-service.ts:125-143 → GET /api/v1/reports/daily-outgoing-goods?dateFrom&dateTo&customerId&productName
 → CTRL:ReportController.cs:106-119 → WHQ:GetDailyOutgoingGoodsReport (:21-117, releases en segunda consulta)
 → PDF: reports-service.ts:145-160 → GET …/daily-outgoing-goods/pdf → DailyOutgoingGoodsPdfService
```

Sin Excel en ninguno de los dos (BR-07-001).

## 4. Inventario general (CF-L211, CF-L172.c, CF-L252)

```
FE:pages/reports/general-inventory.vue
 → selects: GET /api/v1/stakeholder?businessRolCode=IMPORTER|CUSTOMS_AGENCY|TRANSPORT_COMPANY&all=true; productos all=true (:47-50)
 → useReportLocations → reports-service.ts:202-208 → GET /api/v1/reports/general-inventory/locations?isAvailable=true
   → CTRL:InventoryReportsController.cs:51-59 (InventoryReportAccess; CHG-03, DEF-F7-005)
 → useGeneralInventory(appliedQuery) → reports-service.ts:190-200 → GET /api/v1/reports/general-inventory?balanceType&fromDate&toDate&…&pageIndex&pageSize
   → CTRL:InventoryReportsController.cs:33-43 → REPQ:GetGeneralInventory (validador :13-24; handler :21-174)
   ← { data: { items, totals }, pagination }
 → Excel: general-inventory.vue:113-142 → mismo endpoint con all=true (sin totales en el archivo)
```

## 5. Pólizas, abandono, ingresos por producto y agencias

| Operación | Traza |
| --- | --- |
| Resumen de póliza | `FE:pages/reports/policies.vue` → `usePolicies` → `reports-service.ts:211-215` → `GET /api/v1/reports/policies?year` → `CTRL:PolicyReportsController.cs:25-32` → `REPQ:GetPoliciesSummary` → `PolicySummaryDto` |
| Detalle de póliza | clic en el mes → `reports-service.ts:217-224` → `GET /api/v1/reports/policies/detail?year&month&uap&pageIndex&pageSize` (Excel con `all=true`) → `REPQ:GetPoliciesDetail` → `{ items, totals }` |
| Mercancía en abandono | `FE:pages/reports/abandonment-candidates.vue` → `reports-service.ts:169-176` → `GET /api/v1/reports/abandonment-candidates?importerId&all` → `CTRL:AbandonmentReportsController.cs:25-35` → `REPQ:GetAbandonmentCandidates` (en memoria; `request.All`) |
| Salidas a destino de abandono | `FE:pages/reports/abandonment-exits.vue` → `reports-service.ts:178-188` → `GET /api/v1/reports/abandonment-exits?fromDate&toDate&all` → `REPQ:GetAbandonmentExits` (`CreateAsync`) |
| Ingresos por producto | `FE:pages/reports/incoming-by-product.vue` → `reports-service.ts:226-233` → `GET /api/v1/reports/incoming-by-product?fromDate&toDate&importerId&productId&all` → `CTRL:InventoryReportsController.cs:67-77` (ActiveUser + ForeignTradeAccess) → `REPQ:GetIncomingByProduct` |
| Agencias: listado | `FE:pages/reports/customs-agency-entries.vue` → `reports-service.ts:235-241` → `GET /api/v1/reports/customs-agency-entries?customsAgencyId&all` → `REPQ:GetCustomsAgencyEntries` |
| Agencias: detalle | clic en la fila → `reports-service.ts:243-249` → `GET /api/v1/reports/customs-agency-entries/{warehouseStorageId}?customsAgencyId` → `REPQ:GetCustomsAgencyEntryDetail` (404 si no es de la agencia); `productName` se pierde en el tipo TS (BR-07-011) |
| Estadísticas (oculta) | `FE:pages/reports/statistics.vue` (`redirect: "/"`) → `useOperationalStatistics` (refresco 120 s) → `GET /api/v1/reports/statistics?period` → `CTRL:ReportController.cs:157-168` (bloque de facturación solo Admin) |

## 6. Facturación (solo forma; cálculo en el módulo 06)

`FE:pages/billing/reports/annual.vue` → `FE:features/billing/services/billing-service.ts:283` → `GET /api/v1/reports/billing-annual?year&serviceCategory` (`CTRL:BillingReportsController.cs:28-37`, `BillingAccess`; enum por nombre). `FE:pages/billing/reports/deposit-billing.vue` → `billing-service.ts:292` → `GET /api/v1/reports/deposit-billing?warehouseStorageNumber` (`:45-53`). Excel: una hoja por día (anual) y tres hojas con filtros y total (CPI). Sin PDF (el legacy `informefacturacion.php` tenía PDF y Excel: lo evalúa el módulo 06).

## 7. Procesos automáticos

El módulo no tiene procesos automáticos ni en el legacy ni en la V2. El efecto lateral legacy al consultar (escritura de `reportes/*/informe_u*.html`, CF-LX07-01) no tiene equivalente: en la V2 ningún informe escribe (sin `SaveChanges` en `Backend/wms-api/Wms.Application/Reports`). La única escritura relacionada con informes es la marca de primera impresión del tiquete de báscula (F5-09), que pertenece al módulo 02.

## 8. Integraciones externas

- **Legacy:** el Excel antepone un logo cargado de un dominio externo (`bodegas-legacy/reportes/reporteexcel.php:20`); dompdf local (`bodegas-legacy/includes/dompdf/`).
- **V2:** ninguna integración externa en tiempo de ejecución. Librerías: `exceljs` (navegador, carga diferida), QuestPDF y SkiaSharp (servidor); los códigos de barras se generan en el propio servicio.
