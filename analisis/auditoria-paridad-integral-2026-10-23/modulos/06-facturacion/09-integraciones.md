# 06-facturacion — 09 Integraciones

> AG-06 · 2026-10-23 · Estático. **Prefijos:** `L/` = `bodegas-legacy/`; `B/` = `Backend/wms-api/`; `F/` = `Frontend/wms/app/`. HTTP con prefijo `/api/v1`.

## 1. Operaciones principales (frontend → backend → persistencia → UI)

### 1.1 Apertura del período al confirmar el depósito (CF-L201, CF-L202.b, CF-L234.a)

1. Comercio Exterior confirma el depósito (módulo 04) → `POST foreign-trade/…/confirm` → `ConfirmStorageDepositHandler` (`B/Wms.Application/ForeignTrade/Commands/ConfirmStorageDeposit/ConfirmStorageDepositHandler.cs:60-89`).
2. En la misma transacción: `storage.Confirm()` y `OpenPeriodWithInvoiceAsync(storage, cliente, FirstStart(EntryDate))` (`:71-81`).
3. `OpenPeriodWithInvoiceAsync` (`B/Wms.Application/Billing/Common/Services/StorageBillingService.cs:348-439`): idempotencia → configuración del cliente (ciclo, preferencia) → TRM de la DIAN si falta (`:376-379`) → cargos (`:381`) → fechas `StoragePeriodCalculator.ForStart` (`:395`) → factura propia `Invoice.CreateForPeriod` o consolidada → un `StorageBillingPeriod` por cargo con `LimitDate` y sus líneas (`:427-433`).
4. Commit; después, avisos a Facturación (TRM pendiente o valor mínimo, `StorageBillingNotifier.NotifyBillingWarningsAsync`).
5. Si algo lanza (p. ej. BR-06-004), rollback: el depósito queda en Borrador (`:85-89`).
6. Facturación ve la factura Borrador en `/billing/invoices` (pestaña Almacenamiento) y el depósito en `/billing/pending-deposits`.

### 1.2 Asignar N.º SIIGO, aprobar y enviar (CF-L202.a)

`InvoiceActionsDialog.vue` → `useAssignInvoiceNumber` → `PATCH billing/invoices/{id}/number {invoiceNumber}` → `AssignInvoiceNumberHandler` (TRM pendiente → 400; número usado → 409; `Invoice.AssignInvoiceNumber`) → refresco del detalle → `PATCH …/approve` (sin cuerpo; autor del token) → `ApproveInvoiceHandler` (TRM pendiente → 400; `DueDate = hoy + plazo`) → `InvoiceDetailDto` → `PATCH …/send` → `Sent`. Reglas de botones en `F/features/billing/utils/invoice-action-rules.ts`, iguales a las del dominio (`B/Wms.Domain/Entities/Billing/Invoice.cs:345-379,521-551`).

### 1.3 TRM manual (CF-L070, CF-L071)

`ManualTrmDialog.vue` (detalle o diálogo de acciones) → `PUT billing/warehouse-storages/{id}/trm {trm, reason}` → `RegisterManualTrmCommandHandler` (`B/Wms.Application/Billing/Commands/RegisterManualTrm/RegisterManualTrmCommandHandler.cs:37-91`): factura del período ya aprobada → 400; DIAN → 409; `AssignManualTrm` + `RecalculateOpenPeriodAsync` en una transacción con descripción de auditoría → avisos (recálculo, sobrescrituras descartadas) → `InvoiceDepositDto` → la UI habilita N.º y aprobación.

### 1.4 Anular y refacturar (CF-L205, CF-V065)

`PATCH billing/invoices/{id}/cancel {reason}` → `CancelInvoiceHandler` (con dinero recibido → 400; pagos pendientes rechazados; estado financiero del cliente recalculado; aviso «quedaron por refacturar») → la factura queda `Cancelled` y sus períodos siguen ligados a ella → «Refacturar» → `POST billing/invoices/{id}/reissue` → `ReissueInvoiceCommandHandler` (clona líneas, re-enlaza períodos, guías, ciclos y entradas; recalcula los períodos abiertos con `StorageRecalculationTrigger`) → 201 con el detalle de la nueva → la UI navega a ella.

### 1.5 Recálculo único (DEC-022)

Disparadores → `StorageRecalculationTrigger` (`B/Wms.Application/Billing/Common/Services/StorageRecalculationTrigger.cs`): camión tardío (`InitiateStorageWeighingHandler`), CE-7 (`AdjustInventoryCommandHandler`), edición de productos y manifiesto (`DepositProductEditing`, `UpdateTruckManifestCommandHandler`), fecha de ingreso (`CorrectDepositEntryDateCommandHandler`), anulación de pesaje (`VoidWeighingCommandHandler:165`), devolución de mercancía (`RevertLoadingOrderCommandHandler:116`), refacturación. Corre **después** del commit del cambio; un fallo se notifica y no revierte el cambio (DEC-013). `RecalculateCoreAsync` (`StorageBillingService.cs:459-597`) reemplaza períodos y líneas con la cantidad facturable de DEC-028 y conserva fechas, N.º y aprobación.

### 1.6 Pagos (CF-V062)

`PaymentDialog.vue` → (comprobante) `POST billing/payments/vouchers` (multipart) → `POST billing/invoices/{id}/payments` → `RecordPaymentHandler` (estado pagable, no excede el saldo, nace Verificado con autor del token) → `Invoice.RecordPayment` → `RefreshStatus`. Verificar y rechazar en `/billing/payments`.

### 1.7 Informes (CF-L206, CF-L207)

`annual.vue` → `GET reports/billing-annual?year=&serviceCategory=` → `GetBillingAnnualHandler` → `BillingAnnualAggregator` → meses/días; Excel con `useExcelExport`. `deposit-billing.vue` → `GET reports/deposit-billing?warehouseStorageNumber=` → `GetDepositBillingHandler` → encabezado, productos, despachos, facturas; Excel de 3 hojas.

## 2. Comparación de procesos automáticos

| Proceso | Legacy | V2 | Horario y zona | Idempotencia |
| --- | --- | --- | --- | --- |
| Períodos de almacenamiento | `L/cron.php` (horario desconocido) y la misma lógica al abrir «Depósitos x Facturar» (`L/modulos/mod_facturacion/listardepositosfacturar.php:311-436`) | `StoragePeriodAutoCloseBackgroundService` → `BillingJobService.AutoCloseExpiredStoragePeriodsAsync` (`B/Wms.Application/Billing/Jobs/BillingJobService.cs:154-282`) | Arranque + 30 s; luego espera hasta el próximo vencimiento (`LimitDate + 1` a las 00:00 de Colombia, `:354-373`), entre 5 min y 24 h; el día con `ColombiaTime.Today` (`:160`) | Por depósito: DbContext y transacción propios; cierre guardado antes de abrir; `OpenPeriodWithInvoiceAsync` no abre si ya hay uno abierto (D13). Sin bloqueo entre instancias (MAF-09; staging tiene una) |
| Mora | — | `OverdueDetectionBackgroundService` → `DetectOverdueAndRecalculateStatusAsync` (`:28-97`) | Arranque + 30 s, luego cada 24 h desde el arranque (no a hora fija); compara `DueDate` con `UtcNow` (instantes) | Recalcula desde los datos; un `SaveChanges` |
| Conciliación de pagos | — | `InvoicePaymentReconciliationBackgroundService` → `ReconcileInvoicePaymentsAsync` (`:111-152`) | Arranque + 45 s, cada 24 h | Solo escribe si cambian pagado o saldo |
| Aviso de vencimiento | — | `InvoiceDueNotificationBackgroundService` → `NotifyUpcomingDueDatesAsync(3)` (`:289-348`) | Arranque + 1 min, cada 24 h | `DueNoticeSentAt`: una vez por factura (DEF-F6-018) |
| Alerta de TRM | `L/menus/evaluatasacambio.php` desde `inicial.php` y el menú (cada segundo) | Aviso «TRM pendiente» por depósito al abrir o recalcular el período | En el evento | — |

Registro de los jobs: `B/Wms.Api/Program.cs:77-80`.

### `cron.php` frente al job, regla a regla

Ver `03-reglas-negocio.md` §1 (P-01 a P-13). Resumen: la regla de fechas (P-03…P-09) es la misma; el legacy rehace en cada pasada lo no facturado (P-10) y la V2 conserva los períodos; el legacy no tiene importe (P-11); la cantidad del período renovado difiere (P-12, BR-06-005).

## 3. Integraciones externas

| Integración | Dónde | Comportamiento |
| --- | --- | --- |
| DIAN — TRM | `B/Wms.Infrastructure/External/DianTrmService.cs:30-77` (dataset público; solo USD→COP; caché por fecha); `StorageBillingService.EnsureTrmAsync` (`:679-703`, espera 3 s); `SystemController` (`GET system/dian-trm/today`, sin consumidor) | Al abrir el período con la fecha de ingreso. Si falla o tarda: TRM pendiente, cargo al mínimo, aviso; Facturación registra la manual |
| SIIGO | Sin integración. Facturación digita el N.º SIIGO (`PATCH billing/invoices/{id}/number`), igual que el legacy | La factura V2 es la representación interna; el documento fiscal es el de SIIGO (MAF-05) |
| Correo y notificaciones | `INotificationOrchestrator.NotifyRoleAsync(Billing, …)` desde los jobs, la anulación, la TRM y el recálculo | Infraestructura en el módulo 08 |
| PDF | `InvoicePdfService` (`GET billing/invoices/{id}/pdf`) | Documento interno |

## 4. Endpoints sin consumidor y llamadas sin endpoint

- Sin consumidor: `GET billing/invoices/{id}/payments`, `GET billing/storage-periods/{id}`, `POST billing/storage-periods/close`, `PATCH billing/invoices/{id}/recipient` (diálogo sin montar), `GET system/dian-trm/today`, `GET formulatype/{code}` (BR-06-007, BR-06-011).
- `BillingPreviewController` **sí** tiene consumidores (cobro en línea y vista previa de fórmulas); no es resto de la creación manual (DEC-021).
- Llamadas del frontend sin endpoint: ninguna en los servicios del módulo.
