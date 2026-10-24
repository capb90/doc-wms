# 02-bascula — 09 Integraciones

> AG-02 · 2026-10-23 · Estático. Frontend relativo a `Frontend/wms/app/`, backend a `Backend/wms-api/`. Todas las rutas HTTP llevan el prefijo `/api/v1`.

## 1. Trazas frontend → backend de las operaciones principales

### T-1 · Registro de un camión con depósito (CF-L103.a)
1. **UI:** el operario toma el camión de la cola (`features/weighbridge/components/TruckQueue.vue`, refresco 15 s por `useWeighbridgeQueue.ts:11-13` → `GET weighbridge/queue`). La operación y la modalidad se preseleccionan por el motivo de ingreso (`features/weighbridge/utils/entry-reason-operation.ts`, DF8; `pages/operations/weighbridge/index.vue:528`).
2. **Documento:** al salir de «Nro. documento» (`StorageServiceForm.vue:518`) → `weighbridge-service.ts:411-475` → `GET weighbridge/service-records/by-document` y `GET weighbridge/warehouse-storage/by-document` (`WeighbridgeController.cs:760,782`, ScaleAccess) → `StorageDocumentLookup.MatchOpenAsync` (`Wms.Application/Weighbridge/Common/Services/StorageDocumentLookup.cs`, 409 si es ambiguo `:59-60`) → `DocumentMatchBanner.vue` y `PreviousEntriesPanel.vue`.
3. **Guardar (Enter):** `StorageServiceForm` arma `IRegisterStorageEntryRequest` (moneda solo con valor, `:823-824`) → `useRegisterStorageEntry` → `POST weighbridge/storage/register` (`WeighbridgeController.cs:245`) → `RegisterStorageEntryHandler` (actualiza conductor/vehículo con `EntryLogInfoUpdater`, DEC-017) → `InitiateStorageWeighingHandler`: bloqueo del ingreso (`:68-70`), 409 si el ingreso ya tiene servicio (`:196-204`), documento (`:272`), productos por id o descripción (`WeighbridgeProductResolver.cs`), unidades (`CargoUnitDeclaration.cs`), número de depósito `2026BA…` en la misma transacción, movimiento `DeclaredEntry` (`:869-…`), tarifa (`:697-701`), commit (`:709-712`), avisos a CE (`:716-748`).
4. **Respuesta:** `InitiateStorageResponseDto` (`warehouseStorageNumber`, `createdProducts`) → aviso «Depósito … creado» y paso 2.
5. **Persistencia:** `service_records`, `warehouse_storages` (+ `import_warehouse_storages` en IMP), `warehouse_storage_entries`, `warehouse_storage_products`, `inventory_movements`, `service_record_entry_logs`, `manifests`, auditoría genérica (`IAuditable`).

### T-2 · Cobro (CF-L116.a / .b)
1. `BillingCollectForm.vue` en línea (DF5); destinatario por defecto cliente o conductor (`features/billing/utils/billing-recipient-default.ts:13`, `index.vue:1045-1048`).
2. `index.vue:1066-1146`: inmediato → `POST weighbridge/{storage|weighing-only|output}/process-payment`; por facturar → `…/start-pending-billing` (`WeighbridgeController.cs:122,154,306,338,413,445`).
3. `ProcessStoragePaymentHandler`: servicio no descartado (`:63-64`), tipo de operación (`:66-67`), mora del destinatario registrado (`:85-89` → `BillingService.ValidateFinancialStatusAsync`, `Wms.Application/Billing/Common/Services/BillingService.cs:106-119`), caso A/B (`:91-125`), un ciclo por camión (`:150-161`), tarifa y total editable (`:167-182`), factura sin número fiscal (`:188-203`), ítem y pago recibido (`:205-229`), ciclo `ReadyForWeighing` (`:239-262`).
4. **Persistencia:** `invoices`, `invoice_items`, `invoice_payments`, `weighbridge_cycles`. Facturación verá la factura y le asigna el N.º SIIGO (`PATCH billing/invoices/{id}/number`, `BillingController.cs:178`).

### T-3 · Pesaje y cierre (CF-L114)
1. Paso 3 `WeightCapture.vue` (embebido) o ventana con F2 (`index.vue:1395`); tipo permitido según el ciclo, fecha propuesta (`WeightCapture.vue:170-183`).
2. `useRecordWeighing` → `POST weighbridge/cycles/{cycleId}/weighings` (`WeighbridgeController.cs:485`) → `RecordWeighingHandler`: estado del ciclo (`:67-79`), fecha dentro de la estadía (`:82-86`), transacción con el tiquete `2026T…` (`:88-92`, `WeighbridgeService.cs:105-106`, `DocumentNumberGenerator.cs:14-35`), reglas de tipo (`:112-160`), llegada a Bodega en el intermedio (`:245`), cierre vía `CompleteCycleCommand` (`:340-357`) con tara ≤ bruto, `ExitLoadingGuard` en salida (`CompleteCycleHandler.cs:143`), llegada a Bodega (`:204`) y neto por entrada (`:210-243`).
3. Paso 4: «Imprimir Ticket» → `useTicketPdf` → `GET weighbridge/{id}/ticket/pdf` (`WeighbridgeCycleReadController.cs:57`) → `WeighbridgeTicketPdfService` (marca la primera impresión, `:144-149`).

### T-4 · Anular un pesaje (CF-L105/L109/L113)
`history.vue` o `cycles/[id].vue` → `ReasonDialog` → `useVoidWeighing` → `POST weighbridge/cycles/{cycleId}/void` (`WeighbridgeVoidController.cs:33-50`, autor del token) → `VoidWeighingCommandHandler` (guardas, efectos por tipo, `InvoiceCancellationPolicy.Apply`, commit, avisos a CE y Facturación y recálculo del almacenamiento `:148-170`) → `CorrectionResultDialog` con `voidedEntries`, `cancelledDeposits`, `revertedOrders`, `cancelledInvoices`, `invoicesToReview`.

### T-5 · Salida compartida y salida con tiquete (CF-L119, CF-L120)
- `AdditionalOrdersDialog.vue` → `GET weighbridge/loading-orders/by-plate/{plate}` → `POST weighbridge/output/cycles/{cycleId}/additional-orders` (`WeighbridgeOutputSharingController.cs:31`) → servicios anclados (`ServiceRecord.CreateAnchoredOutput`), despacho al completar.
- `EntryTicketExitPanel.vue` → `GET weighbridge/history` (tiquetes de la placa) → `POST weighbridge/output/from-entry-ticket` (`:49`); desde CE, `ExitWithEntryTicketDialog.vue` → `POST foreign-trade/loading-orders/{id}/exit-with-entry-ticket` (`LoadingOrderExitController.cs`, ForeignTradeAccess). Mismo comando `ExitWithEntryTicketCommand`.

### T-6 · Historial y reporte (CF-L102, CF-L121)
`history.vue` → `useWeighbridgeHistory` / `useWeighbridgeHistoryTotals` → `GET weighbridge/history`, `GET weighbridge/history/totals` (`WeighbridgeController.cs:708,723`) → `WeighbridgeHistoryFilters` (`GetWeighbridgeHistory/WeighbridgeHistoryFilters.cs`) → Excel en el navegador con `all: true` (`history.vue:107-117`). El filtro «ID Ciclo» no llega al backend (BR-02-008).

## 2. Integraciones con otros módulos

| Integración | Dirección | Evidencia | Nota |
| --- | --- | --- | --- |
| Vigilancia → báscula | El ingreso de portería alimenta la cola y trae vehículo y conductor | `GET weighbridge/queue`; `PATCH weighbridge/entry-log/{id}/info` (`WeighbridgeSharedController.cs:35`, OperationalAccess) | Módulo 03 |
| Báscula → Comercio Exterior | Depósito en Borrador, avisos «Nuevo depósito…», «Producto creado desde báscula», camión tardío | `InitiateStorageWeighingHandler.cs:716-748,836-…` | Módulo 04 confirma (P2) |
| Báscula ↔ Bodega | Segundo pesaje exige llegada; pendientes de recepción | `Common/Services/ReceptionArrivalGuard.cs`; `features/warehouse/composables/usePendingFromWeighbridge.ts` | Módulo 03 |
| Báscula ↔ Comercio Exterior (salidas) | Orden de cargue previa; repesaje 409 hasta el cargue; guía de importación antes de despachar | `OutputInitiationRules.cs`; `ExitLoadingRules.cs`; `RecordWeighingHandler.cs:413,495` (CHG-33) | Módulo 05 |
| Báscula → Facturación | Facturas de báscula, N.º SIIGO, pagos, anulación de facturas | `BillingController.cs:178,278`; `InvoiceCancellationPolicy.cs` | Módulo 06 |
| Trazabilidad | Notificaciones de estado por placa | `NotifyTraceabilityUpdateAsync` en los handlers de inicio y cobro | Módulo 03 (CF-V034) |

## 3. Procesos automáticos

| Proceso | Legacy | V2 | Paridad |
| --- | --- | --- | --- |
| Lectura del indicador de peso | `peso.php` / `consultapesa.php`: sondeo cada 100 ms de la tabla `peso` | No existe (peso digitado) | `DIFERENCIA_INTENCIONAL` (DECISIONES_REVISION §2.E.17) |
| Refresco de la cola | Recarga manual del listado | `useWeighbridgeQueue.ts:13` (15 s); dashboard 30 s | `SOLO_V2` |
| Notificaciones en tiempo real | No hay | `INotificationOrchestrator` / `realtimeNotifier` (pesaje capturado, ciclo completo, perecedero) | `SOLO_V2` |
| Recálculo del período al llegar un camión tardío o anular | No hay | `StorageRecalculationTrigger.HandleLateTruckAsync` / `RecalculateAsync` (`InitiateStorageWeighingHandler.cs:745`; `VoidWeighingCommandHandler.cs:163-170`) | Módulo 06 |

No hay jobs (`Wms.Api/BackgroundJobs/`) propios de báscula.

## 4. Integraciones externas

| Integración | Legacy | V2 |
| --- | --- | --- |
| Indicador de la báscula (hardware) | Tabla `peso` llenada fuera de la aplicación; `consultapesa.php` | Ninguna (retirada por decisión) |
| DIAN (numeración) | `resolucion_numeracion` para el tiquete-factura | Ninguna en báscula; el PDF conserva la leyenda DIAN (BR-02-005). La TRM de la DIAN no se consulta en báscula (DEC-023) |
| SIIGO | N.º SIIGO digitado por báscula (`factusiigoticket.php`) | N.º SIIGO digitado por Facturación (DEC-024) |
| Impresora térmica | `window.print()` del HTML del tiquete | PDF QuestPDF de 80 mm (`WeighbridgeTicketPdfService.cs`) abierto por el navegador |
