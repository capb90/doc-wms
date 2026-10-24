# 05 · Integraciones: trazas frontend → backend, procesos automáticos e integraciones externas

> Auditoría estática del 2026-10-23 (AG-05). **Prefijos:** `F/` = `Frontend/wms/app/`, `FTS` = `Frontend/wms/app/features/foreign-trade/services/foreign-trade-service.ts`, `C/` = `Backend/wms-api/Wms.Api/Controllers/v1/`, `FT/` = `Backend/wms-api/Wms.Application/ForeignTrade/`, `D/` = `Backend/wms-api/Wms.Domain/Entities/`.
> Todas las rutas llevan el prefijo `/api/v1` (`baseURL` del cliente, `F/plugins/api-client.ts:34-42`). Respuesta envuelta en `ApiResponse` (`data`, `pagination`). Ninguna traza se ejecutó.

## T1 · Registrar un levante

1. `F/pages/foreign-trade/imports/[id]/index.vue:675` «Registrar Levante» (visible con `canRegisterRelease`: depósito `Confirmed` y recibido − levantes > 0, `F/features/foreign-trade/utils/release-rules.ts`).
2. `ReleaseForm.vue` valida cantidad ≤ pendiente (`:286-290`), FOB ≥ 0 y la tasa manual solo si la API la pidió (`:304-309`); arma `IRegisterReleaseRequest` (`:372-382`).
3. `useRegisterRelease` → `FTS:186-197` → `POST /foreign-trade/imports/{importWarehouseStorageId}/releases`.
4. `C/ForeignTradeController.cs:181-205` (`ForeignTradeAccess`) → `RegisterImportReleaseCommand`.
5. Validador (`RegisterImportReleaseCommandValidator.cs:9-47`) → handler: estado (`ReleaseStateGuard`), producto del depósito, tope por producto (`NationalizationBalance`), duplicados (`ReleaseDuplicateLookup`), FOB con la TRM de la DIAN (externo, 3 s) o manual (`ReleaseFobService`), `ImportRelease.Create`, `RecalculateTotals` (estado `Nacionalizado`) y `SaveChanges` (auditoría genérica).
6. Respuesta: `ImportDepositDetailDto` del depósito → el diálogo ofrece «Registrar otro producto con este levante» (DF4) o «Terminar»; invalidación `['foreign-trade']`; aviso de reimprimir la etiqueta (`onReleaseSaved`).
7. Errores visibles: 400 del tope y de la TRM; 409 de duplicados bajo el campo (`ReleaseForm.vue:354-370`).

## T2 · Crear la orden de cargue

1. `F/pages/foreign-trade/loading-orders/create.vue` → `LoadingOrderForm.vue`.
2. Selector de depósitos: `useLoadingOrderDeposits` → `FTS:453-473` → `GET /foreign-trade/loading-orders/deposits?searchField&searchValue&pageIndex&pageSize` → `GetLoadingOrderDepositsHandler` (disponible > 0, sin Borrador ni anulados; `nationalizedQuantity`/`nationalizedAvailable` por producto).
3. Vehículos, conductores y ciudades activas con `all: true` (`LoadingOrderForm.vue:82-91`) → `GET /administration/cities` (módulo 01); cuadrillas: `F/features/administration/components/CrewSelect.vue` → `GET /administration/crews`.
4. Estado financiero por cliente: `FTS` `validateClientFinancialStatus` → `GET /foreign-trade/validate-client/{id}` (`LoadingOrderForm.vue:426-437`).
5. Envío (`:467-490`) → `useCreateLoadingOrder` → `FTS:478-485` → `POST /foreign-trade/loading-orders` → `C/ForeignTradeController.cs:1005-1044` (autor del token) → `CreateLoadingOrderCommandHandler`:
   - validaciones fuera de transacción: Borrador, nacionalizado, mora por cliente, stock, nacionalizado por producto, tipo de carga y unidad, vehículo, conductor, ciudad activa, orden externa (emisor con rol, número único), cuadrilla;
   - soporte de la orden externa al almacenamiento (S3 o local, `IStorageService.SaveFileAsync`) **antes** de la transacción;
   - transacción: consecutivo `OC` (`document_sequences … FOR UPDATE`), `LoadingOrder.Create`, `SetDestination`, `AssignCrew`, `ReserveAsync` por ítem (ítem + reserva emparejada + `ReserveStock` + unidad de carga), commit.
6. Respuesta `LoadingOrderResultDto` → navega al detalle (protección de doble envío, DEF-F10-001).
7. Efecto lateral: el archivo de soporte queda guardado aunque la transacción falle después (huérfano, sin impacto funcional).

## T3 · Emitir la guía de importación

1. `F/pages/foreign-trade/dispatch-guides/create.vue` (o «Generar Guía» desde `pending.vue:84` con `?loadingOrderId=`).
2. `DispatchGuideForm.vue`: órdenes de `GET /foreign-trade/dispatch-guides/pending-orders?pageSize=50` (`:29-37`); detalle de la orden (`GET /foreign-trade/loading-orders/{id}`) para la ciudad; `GET /administration/cities?all=true`; vista previa `GET /foreign-trade/loading-orders/{id}/dispatch-guide-preview` (cargos por dueño, firmante forzado).
3. «Continuar al cobro» abre `BillingCollectForm` (destinatario, modo y método de pago, total) → `POST /foreign-trade/dispatch-guides` (`FTS:620-627`, `C/ForeignTradeController.cs:1199-1225`, autor del token).
4. `CreateDispatchGuideCommandHandler`: guardas (Borrador, tipo IMP, `EnsureGuidable`, guía vigente), servicio `GUIA_SALIDA` e IVA, dueños y mora, plan de cobro, vencimiento (`GuideExpirationCalculator`), firmante; transacción: consecutivo `S`, `DispatchGuide.Create` (cuadrilla de la orden), `FreezeLinesAsync` (`FOR UPDATE` de productos, saldos y levante congelados), facturas (una por dueño o una sola; contado con `InvoicePayment` `Received`; crédito propia o consolidada), despacho si la salida ya estaba registrada, PDF, commit.
5. Respuesta `DispatchGuideResultDto` (facturas, total, PDF) → vuelve al historial.
6. Paso a facturación: las facturas nacen sin N.º SIIGO; Facturación las numera, aprueba y cobra (módulo 06).

## T4 · Cancelar, modificar y revertir la orden; anular la guía

| Acción | FE | HTTP | Backend | Efectos |
| --- | --- | --- | --- | --- |
| Cancelar | `loading-orders/[id]/index.vue:85-102` (`ReasonDialog`) | `PATCH /foreign-trade/loading-orders/{id}/cancel` `{reason}` | `CancelLoadingOrderHandler` | Reservas liberadas, `Cancelled`, auditoría, aviso a Bodega si estaba en cargue. **La guía vigente no se toca** (BR-05-001) |
| Modificar ítems | `EditLoadingOrderItemsDialog.vue` | `PUT /foreign-trade/loading-orders/{id}/items` `{items, reason}` | `UpdateLoadingOrderItemsCommandHandler` | Ajusta, libera o reserva; auditoría; aviso a Bodega en cargue |
| Revertir | `loading-orders/[id]/index.vue:119-146` | `POST /foreign-trade/loading-orders/{id}/revert` `{reason}` | `RevertLoadingOrderCommandHandler` | Stock + movimiento `In`, unidades, depósitos y períodos reabiertos (`StorageRecalculationTrigger.HandleStockReturnedAsync`, módulo 06), aviso a Bodega |
| Anular guía | `dispatch-guides/index.vue` (`openCancelGuide`) | `POST /foreign-trade/dispatch-guides/{id}/cancel` `{reason}` | `CancelDispatchGuideCommandHandler` | Guía anulada (conserva número), facturas anuladas o para revisar, aviso a Facturación; el resultado se muestra en `CorrectionResultDialog` |
| Cambiar modo de pago | `ChangePaymentModeDialog` | `PATCH /foreign-trade/dispatch-guides/{id}/payment-mode` `{paymentMode, paymentMethod}` | `ChangeDispatchGuidePaymentModeCommandHandler` | Mueve líneas entre factura propia y consolidada; paga o rechaza el contado |

Invalidaciones: `['foreign-trade']` y las claves de Bodega y Facturación de cada composable (`useCancelLoadingOrder`, `useUpdateLoadingOrderItems`, `useRevertLoadingOrder`, `useCancelDispatchGuide`).

## T5 · Salida con el tiquete de ingreso (DF18)

`imports/[id]/index.vue:778` → `ExitWithEntryTicketDialog.vue` (órdenes de la misma placa con `GET /foreign-trade/loading-orders?searchField=LicensePlate&all=true`, filtradas por placa normalizada y estado) → `POST /foreign-trade/loading-orders/{id}/exit-with-entry-ticket` `{entryWeighbridgeCycleId}` → `C/LoadingOrderExitController.cs:30-39` → `ExitWithEntryTicketCommandHandler` (reglas `EntryTicketExitRules`: tiquete de ingreso completo, no anulado ni usado, mismo vehículo, depósitos del tiquete; servicio de salida sin ciclo ni cobro; despacho inmediato si está cargada y con guía) → `ExitWithEntryTicketResultDto` → aviso «Despachada» o «Se despacha cuando…». La misma regla tiene la ruta de báscula `POST /weighbridge/output/from-entry-ticket` (módulo 02).

## Procesos automáticos del módulo

| Proceso | Disparador | Evidencia | Observación |
| --- | --- | --- | --- |
| Guía de exportación automática | Al final de `ExecuteLoadingOrderCommandHandler` (Bodega), si todos los ítems son de exportación | `B/Wms.Application/Warehouse/Commands/LoadingOrder/ExecuteLoadingOrderCommandHandler.cs:348-366` | Fuera de la transacción del cargue; un fallo solo se registra en el log (BR-05-009) |
| Despacho de la orden | Al emitir la guía (IMP con salida registrada), al completar el pesaje de salida o al cargar con la salida ya registrada | `CreateDispatchGuideCommandHandler.cs:410-417`; `ImportGuideRules.ShouldDispatch` | — |
| Avisos | Retiro de levante que deja el depósito sin nacionalizar (Comercio Exterior); cancelación o modificación en cargue y reversión (Bodega); guía anulada con factura emitida (Facturación) | `WithdrawImportReleaseCommandHandler.cs:85-110`; `CancelLoadingOrderHandler.cs:53-73`; `UpdateLoadingOrderItemsCommandHandler.cs:124-144`; `RevertLoadingOrderCommandHandler.cs:166-192`; `InvoiceCancellationPolicy.NotifyToReviewAsync` | Después del commit; un fallo de notificación no revierte |
| Refresco de pendientes | `usePendingGuides` cada 30 s | `F/features/foreign-trade/composables/usePendingGuides.ts:7-11` | — |

No hay jobs (`Wms.Api/BackgroundJobs/`) propios del módulo. El legacy tampoco tenía procesos automáticos en levantes ni salidas (el estado «incompleto» se escribía al listar, RN-037).

## Integraciones externas

| Integración | Uso | Evidencia | Falla |
| --- | --- | --- | --- |
| TRM de la DIAN (`IDianTrmService`) | FOB del levante | `FT/Common/Services/ReleaseFobService.cs:17,60-80` | 3 s; sin respuesta → 400 que pide la tasa manual |
| Almacenamiento de archivos (`IStorageService`) | Soporte de la orden externa | `CreateLoadingOrderCommandHandler.cs:430-476` | 400 por tipo o tamaño |
| Generación de PDF (QuestPDF) | Guía, ZIP por depósito, orden de trabajo | `FT/Common/Services/DispatchGuidePdfService.cs`; `LoadingOrderPdfService.cs` | La guía genera su PDF dentro de la transacción de emisión |
| Notificaciones en tiempo real y correo | Avisos citados arriba (`sendEmail: false`) | `INotificationOrchestrator` | — |
