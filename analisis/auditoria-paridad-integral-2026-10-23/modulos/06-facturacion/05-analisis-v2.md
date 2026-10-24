# 06-facturacion — 05 Análisis V2

> AG-06 · 2026-10-23 · Estático. **Prefijos:** `B/` = `Backend/wms-api/`; `F/` = `Frontend/wms/app/`. Prefijo HTTP `/api/v1` (`B/Wms.Api/Program.cs:162`; `Frontend/wms/nuxt.config.ts:31`). Enums por nombre (`JsonStringEnumConverter`, `B/Wms.Api/Program.cs:63`).

## 1. Frontend

| Página | `requiredRoles` | Qué hace | Servicio / llamadas |
| --- | --- | --- | --- |
| `F/pages/billing/index.vue` | Admin, Billing (`:10`) | Tablero: KPI del mes, últimas facturas, clientes en mora | `useBillingDashboard` → `GET billing/dashboard/summary`, `GET billing/dashboard/overdue` |
| `F/pages/billing/invoices/index.vue` | Admin, Billing (`:20`) | Facturas por pestaña de servicio (Báscula, Montacargas, Guía, Almacenamiento), filtros estado/N.º/destinatario/día, Excel `all=true` (`:60-160`), diálogo de acciones | `useInvoices` → `GET billing/invoices` (`serviceCategory`, `status`, `invoiceNumber`, `recipient`, `fromDate/toDate`) |
| `F/pages/billing/invoices/[id].vue` | Admin, Billing (`:26`) | Detalle: destinatario, líneas con método de cálculo, override en Borrador (`:77-90`), depósitos con TRM y «Registrar TRM» (`:101-106,446`), pagos (`:585`), PDF (`:224`), enlaces de refacturación (`:58-61,284-287`) | `GET billing/invoices/{id}`; `POST billing/invoice-items/{id}/override`; `PUT billing/warehouse-storages/{id}/trm`; `POST billing/invoices/{id}/payments`; `GET billing/invoices/{id}/pdf` |
| `F/features/billing/components/InvoiceActionsDialog.vue` | (en las tres páginas) | N.º SIIGO, aprobar, enviar, registrar pago, detalle, notas, refacturar (`:395-402`), anular (`:421-434`); reglas en `F/features/billing/utils/invoice-action-rules.ts` | `PATCH …/number`, `/approve`, `/send`, `/cancel`, `PATCH billing/invoices/{id}`, `POST …/reissue` |
| `F/pages/billing/pending-deposits/index.vue` | Admin, Billing (`:17`) | Depósitos con período abierto: días, documento, terceros, manifiesto, valor y TRM, «Por refacturar» (`:277-284`), historial de facturas expandible (`:307`), resumen (`:296-297`) | `GET billing/pending-deposits`; `GET billing/pending-deposits/{id}/summary`; `GET billing/storage-periods?warehouseStorageId=` (`F/features/billing/components/DepositSummaryDialog.vue:39`) |
| `F/pages/billing/payments/index.vue` | Admin, Billing (`:16`) | Pagos con filtros, registrar con comprobante, verificar, rechazar | `GET billing/payments`; `POST billing/payments/vouchers`; `PATCH billing/payments/{id}/verify|reject` |
| `F/pages/billing/configurations/index.vue` | Admin, Billing (`:16`) | Configuración por cliente: ciclo (catálogo del API), plazo, límite, preferencia (`F/features/billing/components/BillingConfigForm.vue:25,35-36`) | `GET billing/configurations`, `GET billing/configurations/cycles`, `GET|PUT billing/configurations/{stakeholderId}` |
| `F/pages/billing/reports/annual.vue` | Admin, Billing (`:18`) | Año + servicio → meses y días; Excel | `GET reports/billing-annual` |
| `F/pages/billing/reports/deposit-billing.vue` | Admin, Billing (`:19`) | «Facturación por CPI»: N.º de depósito exacto (`:110-116`) → encabezado, productos, salidas, facturas; Excel de 3 hojas (`:45-94`) | `GET reports/deposit-billing?warehouseStorageNumber=` |
| `F/pages/admin/stakeholders/[id].vue` | Admin, ForeignTrade, Billing (`:132`) | Convenios del tercero: crear, editar, activar/desactivar, servicios con fórmula y vista previa | `F/features/agreements/services/agreement-service.ts:17-134` → `…/stakeholder/{id}/agreement…`; `POST billing/formula-preview` |
| `F/pages/admin/services/*` | **Admin** (`index.vue:14`, `[id].vue:102`, `create.vue:10`, `edit/[id].vue:12`) | Servicios, precio base con vigencia, reglas base, mínimos por modalidad, impuestos | `F/features/services/services/service-service.ts:21-113`, `service-pricing-rule-service.ts` |
| `F/pages/admin/forklift-rates/index.vue` | **Admin** (`:6`) | Tarifas de montacargas por tipo de vehículo | `GET/PUT forklift-rates…` |

Menú: grupo «Facturación» para Admin y Billing con Dashboard, Facturas, Depósitos Pendientes, Pagos, Configuraciones, Clientes, Facturación anual y por CPI (`F/components/layout/AppMenu.vue:460-506`). «Tarifas base» y «Tarifas de montacargas» están en «Administración», solo Admin (`:47-49,130-151`).

No hay mocks ni datos estáticos en `F/features/billing`, `F/features/agreements`, `F/features/services` ni en las páginas (búsqueda `mock|faker|stub|TODO|FIXME`). La pantalla de creación manual no existe (`F/pages/billing/invoices/` solo tiene `index.vue` y `[id].vue`; DEC-021).

## 2. Backend: endpoints y políticas

`BillingController` (`B/Wms.Api/Controllers/v1/BillingController.cs:52-53`, `[Route("billing")]`, `BillingAccess` = Admin + Billing, `B/Wms.Domain/Security/WmsPolicyRoles.cs:36`), 27 acciones:

| # | Verbo y ruta | Línea | Consumidor FE |
| --- | --- | --- | --- |
| 1 | `POST billing/invoice-items/{id}/override` | 73 | `F/features/billing/services/billing-engine.service.ts:21-34` (OverrideAmountDialog) |
| 2 | `GET billing/invoices` | 102 | `billing-service.ts:42-48` |
| 3 | `GET billing/invoices/{id}` | 119 | `billing-service.ts:50-55` |
| 4 | `PATCH billing/invoices/{id}` (notas, notas internas, detalle) | 138 | `useUpdateInvoice` (InvoiceActionsDialog) |
| 5 | `PATCH billing/invoices/{id}/recipient` | 158 | `billing-service.ts:96-102` → `useUpdateInvoiceRecipient` → `UpdateRecipientDialog.vue`, **que ninguna página monta** |
| 6 | `PATCH billing/invoices/{id}/number` | 178 | `useAssignInvoiceNumber` |
| 7 | `PATCH billing/invoices/{id}/approve` (autor del token) | 197 | `useApproveInvoice` |
| 8 | `PATCH billing/invoices/{id}/send` | 217 | `useSendInvoice` |
| 9 | `PATCH billing/invoices/{id}/cancel` (autor del token) | 237 | `useCancelInvoice` |
| 10 | `GET billing/invoices/{id}/pdf` | 256 | `useInvoiceActions` |
| 11 | `POST billing/invoices/{id}/payments` (autor del token) | 278 | `useRecordPayment` |
| 12 | `POST billing/payments/vouchers` | 314 | `PaymentDialog.vue` |
| 13 | `GET billing/invoices/{id}/payments` | 377 | **Sin consumidor** (los pagos llegan en el detalle) |
| 14 | `GET billing/payments` | 394 | `usePayments` |
| 15 | `PATCH billing/payments/{id}/verify` | 411 | `useVerifyPayment` |
| 16 | `PATCH billing/payments/{id}/reject` | 430 | `useRejectPayment` |
| 17 | `GET billing/configurations` | 451 | `useBillingConfigurations` |
| 18 | `GET billing/configurations/{stakeholderId}` | 468 | `useBillingConfig` |
| 19 | `PUT billing/configurations/{stakeholderId}` | 487 | `useUpsertBillingConfiguration` |
| 20 | `GET billing/storage-periods` | 518 | `useStoragePeriods` (DepositSummaryDialog) |
| 21 | `GET billing/storage-periods/{id}` | 535 | **Sin consumidor** (`getStoragePeriodById` definido y no usado) |
| 22 | `POST billing/storage-periods/close` (autor del token) | 554 | **Sin consumidor**: cierre y renovación manual solo por API (lo usó QA, F6-ALM-008) |
| 23 | `GET billing/pending-deposits` | 574 | `usePendingDeposits` |
| 24 | `GET billing/pending-deposits/{id}/summary` | 590 | `useDepositSummary` |
| 25 | `GET billing/dashboard/summary` | 609 | `useBillingDashboard` |
| 26 | `GET billing/dashboard/overdue` | 623 | `useBillingDashboard` |
| 27 | `PUT billing/warehouse-storages/{id}/trm` | 643 | `useRegisterManualTrm` (ManualTrmDialog). Lee el usuario con `FindFirst(NameIdentifier)` (`:650-654`) en vez de `GetRequiredUserId()`: sigue saliendo del token |

Otros controladores:

| Controlador | Ruta y política | Consumidor |
| --- | --- | --- |
| `BillingCyclesController.cs:11-21` | `GET billing/configurations/cycles`, `BillingAccess` | `useBillingCycles` |
| `BillingPreviewController.cs:12-62` | `POST billing/preview`, `POST billing/formula-preview`, `ActiveUser` | `billing/preview`: `BillingCollectForm.vue:270` (cobro en línea de báscula, montacargas y guía); `formula-preview`: `F/features/agreements/services/formula-type-service.ts:24-30` (FormulaPreviewPanel). **No son restos de la creación manual**: DEC-021 retiró `create.vue`, `BillingPreviewPanel.vue` y `GetStorageInvoiceDraft`, que no existen (búsqueda en `B/` y `F/`), y `B/Wms.Tests/Api/BillingControllerSurfaceTests.cs:15-31` lo asegura. La política `ActiveUser` responde a la decisión del usuario del 3-oct (tarifas y simulaciones abiertas, DEF-F9-005 Verificado) |
| `BillingReportsController.cs:14-53` | `GET reports/billing-annual`, `GET reports/deposit-billing`, `BillingAccess` | `useBillingReports` |
| `InvoiceReissueController.cs:11-23` | `POST billing/invoices/{id}/reissue`, `BillingAccess` | `useReissueInvoice` |
| `FormulaTypeController.cs:12-33` | `GET formulatype`, `GET formulatype/{code}`, `[Authorize]` | `getFormulaTypes`; `getFormulaTypeByCode` **sin uso** |
| `ServiceController.cs:32-271` | `service…`: escrituras `BillingAccess`; lecturas `[Authorize]` | `F/features/services/*` (todas las funciones usadas) |
| `ForkliftRateController.cs:18-85` | `forklift-rates`: vehicle-types autenticado; lista y upsert `BillingAccess` | `F/features/forklift-rates/services` |
| `StakeholderController.cs:245-415` | `stakeholder/{id}/agreement…`: escrituras `BillingAccess`, lecturas `ActiveUser` (`:43`) | `agreement-service.ts` |
| `SystemController.cs:12-46` | `GET system/dian-trm/today`, `[Authorize]` | **Sin consumidor** |

**Llamadas del frontend sin endpoint:** ninguna en `billing-service.ts`, `billing-engine.service.ts`, `agreement-service.ts`, `formula-type-service.ts`, `service-service.ts`, `service-pricing-rule-service.ts` (rutas cotejadas una por una con los atributos `[Http*]`).

## 3. Servicios y procesos del backend

- **Apertura** `StorageBillingService.OpenPeriodWithInvoiceAsync` (`B/Wms.Application/Billing/Common/Services/StorageBillingService.cs:348-437`): idempotente si hay período abierto (`:354`); `OnDemand` no abre (`:368`); TRM de la DIAN (`:376-379`); cargos (`:381`); fechas con `StoragePeriodCalculator` (`:395`); factura propia o consolidada (`:407-425`); un período por cargo con sus líneas (`:427-433`, `:711-800`). Llamadores: confirmación (`ConfirmStorageDepositHandler.cs:76`), job (`BillingJobService.cs:237`), cierre manual (`CloseStoragePeriodsHandler.cs:61`), camión tardío y devolución (`StorageRecalculationTrigger.cs:309`), migración (`OpenMigratedBillingCommand.cs:106`).
- **Cargos** `ResolveStorageChargesAsync` (`:43-307`): magnitudes del depósito, CIF por grupo, resolución por producto, coherencia de unidad, magnitud única, respaldo por mínimo.
- **Recálculo** `RecalculateCoreAsync` (`:459-597`), disparado por `StorageRecalculationTrigger` (camión tardío, CE-7, devolución, fecha de ingreso, manifiesto, anulación de pesaje, refacturación) y por la TRM manual (`RegisterManualTrmCommandHandler.cs:70`).
- **Jobs** (`B/Wms.Api/Program.cs:77-80`): ver `09-integraciones.md` §3.

## 4. DTO ↔ tipos TypeScript

| Operación | DTO (backend) | Tipo TS | Diferencias |
| --- | --- | --- | --- |
| Listado de facturas | `InvoiceDto` (`B/Wms.Application/Billing/Common/DTOs/InvoiceDto.cs`) | `IInvoiceDto` (`F/features/billing/types/invoice.ts`) | `customerId`/`customerName` son nulos en el backend (destinatario no registrado) y no nulos en TS; TS agrega `unregisteredRecipientPhone` (no se envía) |
| Detalle | `InvoiceDetailDto` | `IInvoiceDetailDto extends IInvoiceDto` | TS hereda `recipientName`, `recipientIdNumber`, `recipientKind`, `itemCount`, `paymentCount`, que el detalle **no envía**; `recipientIdType` es `IdentificationType` en TS y `string` en el DTO. La página no lee esos campos (usa `customerName`, `customerIdNumber`, `recipientIdType`): sin efecto visible hoy |
| Líneas | `InvoiceItemDto` | `IInvoiceItemDto` | TS declara `productPriceId` (el DTO tiene `ServicePriceId`); faltan `serviceId`, `serviceCode`, `serviceName` en TS |
| Depósitos de la factura | `InvoiceDepositDto` | `IInvoiceDepositDto` | Coinciden campo a campo (`trmDate` `DateOnly` ↔ `string`) |
| Pendientes | `DepositPendingBillingRow`, `InvoiceHistoryEntryDto` | `IDepositPendingBillingRow`, `IInvoiceHistoryEntryDto` | TS no declara `totalAmount` del historial (no se muestra); resto igual |
| Períodos | `StoragePeriodDto` | `IStoragePeriodDto` | TS acepta el estado `"Invoiced"`, que el enum no tiene (`B/Wms.Domain/Enums/StorageBillingPeriodStatus.cs`: `Open`, `Closed`); TS no declara `formulaCode`, `basis`, `source`, `products` |
| Configuración | `UpsertBillingConfigurationRequest` | `IBillingConfigurationDto`, `BillingCycle` | Coinciden; TS ya no ofrece `OnDemand` (DEF-F6-008) |
| Informe por CPI | `DepositBillingReportDto` | `IDepositBillingReportDto` | `cargoManifestNumber`, `importerName`, `entryDate`, `vehiclePlate`, `departureDate` nulos en el backend, no nulos en TS |
| Informe anual | `BillingAnnualReportDto` | `IBillingAnnualReportDto` | Coinciden |
| TRM manual | `RegisterManualTrmRequest(Trm, Reason)` | `IRegisterManualTrmRequest` | Coinciden |
| Override | `OverrideBillingAmountRequest(NewAmount, Reason)` | `IOverrideBillingAmountBody` (`billing-engine.service.ts:5-8`) | Coinciden; sin autor en el cuerpo |
| Pago | `RecordPaymentRequest` | `IRecordPaymentRequest` | Coinciden (sin efectivo y cambio) |

Paginación: los listados usan `QueryParametersBase` (`pageIndex`, `pageSize`, `all`); la exportación de facturas envía `all: true` (`F/pages/billing/invoices/index.vue:137`).

## 5. Capacidades `SOLO_V2`

| ID | Capacidad | Evidencia | Estado |
| --- | --- | --- | --- |
| CF-V060 | Motor de acuerdos y fórmulas (4 niveles; 8 calculadoras más `BASE_PRICE` y el respaldo `MINIMUM_VALUE`) | `B/Wms.Application/Billing/Services/BillingResolver.cs`; `FormulaPricing.cs`; `B/Wms.Application/Billing/Calculators/*` (`FIXED`, `PER_UOM`, `PERCENTAGE_OF_VALUE`, `PERCENTAGE_OF_VALUE_PRORATED`, `PER_VEHICLE`, `PER_VEHICLE_TYPE`, `PER_CARGO_UNIT`, `WEIGHT_THRESHOLD`); `B/Wms.Application/Agreements/*` | Confirmada; brechas BR-06-001, BR-06-004 |
| CF-V061 | Ciclos configurables (8 ofrecidos; `OnDemand` solo lectura) | `BillingCycleCatalog.cs:24-46`; `BillingCyclesController`; `F/pages/billing/configurations/index.vue` | Confirmada; BR-06-010 |
| CF-V062 | Pagos, comprobantes, verificación y conciliación diaria | `BillingController.cs:278-449`; `BillingJobService.ReconcileInvoicePaymentsAsync` (`:111-152`); `F/pages/billing/payments/index.vue` | Confirmada |
| CF-V063 | Mora y bloqueo de servicios | `BillingJobService.DetectOverdueAndRecalculateStatusAsync` (`:28-97`); `OverdueSweep`; `ClientFinancialStatusRules`; `BillingService.ValidateFinancialStatusAsync` (`:106-120`) | Confirmada |
| CF-V064 | Aviso de vencimiento (3 días antes, una vez por factura) | `BillingJobService.NotifyUpcomingDueDatesAsync` (`:289-348`) | Confirmada |
| CF-V065 | Refacturación de la anulada | `InvoiceReissueController`; `ReissueInvoiceCommandHandler.cs` | Confirmada (es el reemplazo de CF-L205; se mantiene la fila por ser candidata) |
| CF-V066 | TRM de la DIAN al crear la factura | `StorageBillingService.EnsureTrmAsync` (`:679-703`); `B/Wms.Infrastructure/External/DianTrmService.cs:30-77` (caché) | Confirmada |
| CF-V067 | Cierre automático y renovación de períodos | `B/Wms.Api/BackgroundJobs/StoragePeriodAutoCloseBackgroundService.cs`; `BillingJobService.AutoCloseExpiredStoragePeriodsAsync` (`:154-282`) | Confirmada; BR-06-005 |
| CF-V068 (nueva) | Tablero de facturación | `F/pages/billing/index.vue`; `GetBillingDashboardHandler.cs` | Confirmada; BR-06-012 |
| CF-V069 (nueva) | Sobrescritura del total de una línea en Borrador, con motivo | `BillingController.cs:73-90`; `OverrideBillingAmountHandler.cs`; `OverrideAmountDialog.vue` | Confirmada (DEF-F6-003/004 Verificados) |
| CF-V06A (nueva) | Factura consolidada por cliente (`InvoicingPreference.Consolidated`) | `BillingService.GetOrCreateConsolidatedInvoiceAsync` (`:44-78`); `StorageBillingService.cs:407-411` | Confirmada; BR-06-012 (ventana en UTC) |
| CF-V06B (nueva) | PDF interno de la factura | `GET billing/invoices/{id}/pdf`; `B/Wms.Application/Billing/Common/Services/InvoicePdfService.cs` | Confirmada (F6-INV-006 PASA) |
