# 03 · Vigilancia y Bodega — Integraciones

> Trazas estáticas interacción → componente → servicio → HTTP → endpoint → lógica → persistencia → respuesta → UI. Prefijo del API `/api/v1` (`useApi`). `BE` = `Backend/wms-api/`, `FE` = `Frontend/wms/app/`.

## 1. Vigilancia

### 1.1 Registrar ingreso
1. `FE/pages/operations/entries/index.vue:156-245` `submitEntry`: valida placa (`utils/plate`) y motivo; busca el vehículo con inactivos (`VehicleService.getVehicleByPlate`) y el ingreso abierto (`GET /entry-logs?vehicleId=&hasDeparture=false&pageSize=1`); si no existe, `POST /vehicles`.
2. `EntryService.createEntryLog` → `POST /entry-logs` `{ vehicleId, entryReasonId, observations }` (`FE/features/entries/services/entry-service.ts:29-32`).
3. `BE/Wms.Api/Controllers/v1/EntryLogController.cs:23-40` (`GateAccess`) arma el comando con el usuario del token.
4. `CreateEntryLogHandler.cs:25-148`: vehículo, usuario, conductor y motivo existen; 409 «La placa ya tiene un ingreso abierto.» (`:79-84`); `EntryLog.RegisterEntry` (fecha no futura, `EntryLog.cs:52-73`); enlace opcional al servicio; `SaveChanges`; aviso de trazabilidad «Ingreso registrado».
5. Respuesta `EntryLogDto` → aviso «Ingreso registrado», refresco del contador. Opcional: `PATCH /weighbridge/entry-log/{id}/info` con vehículo y conductor (`index.vue:205-238`; `WeighbridgeSharedController.cs:35`, `OperationalAccess`).
6. Efecto en otros módulos: si el motivo requiere pesaje, el camión entra a la cola de báscula (módulo 02); «Solo bodega» aparece en `GET warehouse/pending-direct-reception`.

### 1.2 Registrar salida
1. `FE/pages/operations/entries/exits.vue:96-120` → confirmación → `POST /entry-logs/{id}/departure` con `{}`.
2. `EntryLogController.cs:74-86` → `RegisterDepartureHandler.cs:25-90`: 409 si ya salió; `EntryLogDepartureGuard.EnsureCanDepartAsync` (`Common/EntryLogDepartureGuard.cs:20-40`): ciclo de báscula sin terminar (`DepartureBlockRules.cs:13-24`) u órdenes de importación cargadas o despachadas sin guía vigente (`LoadingOrderGuideReader.cs:57-77`, mensaje `ImportGuideRules.cs:60-65`).
3. `EntryLog.RegisterDeparture` (no futura ni anterior al ingreso) → `SaveChanges` → aviso «Salida registrada».
4. UI: aviso y `refetch`; el 409 se muestra con su descripción.

### 1.3 Corregir un ingreso
`CorrectEntryLogDialog.vue` → `useCorrectEntryLog` → `PUT /entry-logs/{id}/correction` `{ licensePlate?, entryReasonId?, dateTimeEntry?, reason }` → `EntryLogCorrectionController.cs:30-53` (`EntryCorrectionAccess`) → `CorrectEntryLogCommandHandler` (placa: reasigna o desactiva el vehículo sin ingresos; motivo: D07; fecha: D08) → `audit_logs` y marca «Corregido» → resultado con cambios y depósitos no actualizados.

## 2. Bodega

### 2.1 Recepción de un camión pesado
1. `FE/pages/warehouse/receptions/entry.vue` y `index.vue` → `useReceptionCreate` / `useCompleteReception` (`FE/features/warehouse/composables/useReceptionCreate.ts:31-80`).
2. `POST /warehouse/receptions/register-arrival` (llegada, requisito del segundo pesaje: §10 «Llegada a Bodega», DEF-F4-003) y `POST /warehouse/receptions/{id}/complete` `{ products (con su ubicación) o receivedCargoUnitIds, signatureDriver, comments, photos, crewId }` (`WarehouseController.cs:230-262`).
3. `CompleteReceptionCommandHandler.cs`: depósito no cerrado ni anulado; unidades de carga completas o productos contados; fotos validadas antes de escribir; transacción; **sin cambio de stock** (`:173-176`); ubica lo descargado hasta lo pendiente (`:166`); aviso a CE si lo contado difiere de lo declarado (`ReceptionDeclaredDifference.cs`).
4. Persistencia: `reception_logs`, productos de la recepción, fotos (servicio de archivos), placements. Respuesta `ReceptionResultDto`.

### 2.2 Recepción directa sin báscula
`DirectReceptionList.vue` (`GET /warehouse/pending-direct-reception`) → `ReceptionStepManualInfo.vue` → `POST /warehouse/receptions/without-weighbridge` → `WarehouseController.cs:338-347` (autor del token) → `CreateReceptionWithoutWeighbridgeCommandHandler.cs:104-309`: bloquea el ingreso, conductor y vehículo, `ServiceRecord`, depósito en **Borrador**, stock declarado con movimiento `DeclaredEntry` (`:267-276`), recepción completa y placements; aviso a administradores y, si difiere, a CE.

### 2.3 Ubicar, mover y liberar
`inventory/index.vue` «Ubicaciones» → `ProductPlacementsDialog.vue` → `usePlacements` → `POST /warehouse/storage-products/{id}/placements` | `/move` | `/release` (`warehouse-service.ts:622-645`) → `WarehousePlacementsController.cs:45-96` (`WarehouseAccess`) → handlers `PlaceStock`, `MovePlacement`, `ReleasePlacement` (transacción + `IAuditContext.Describe`) → `WarehousePlacementService` → `warehouse_storage_product_placements` (auditable) → `ProductPlacementsDto` → el diálogo se actualiza y se invalidan `['warehouse']`, `['warehouse-storage-stock']`, `['warehouse-locations']`. Sin movimientos de kárdex (como el legacy).

### 2.4 Ejecutar el cargue
1. `FE/pages/warehouse/loading-orders/index.vue` → `LoadingOrderExecutionDialog.vue` (cantidad 0…pedida, firma, cuadrilla, fotos) → `POST /warehouse/loading-orders/{id}/execute` (`warehouse-service.ts:445-449`).
2. `WarehouseController.cs:846-866` (usuario del token como `CompletedBy`) → validador (firma obligatoria, `ExecuteLoadingOrderCommandValidator.cs:40-43`) → `ExecuteLoadingOrderCommandHandler.cs`:
   - orden ejecutable y depósitos confirmados o cerrados (`:75-80`); algo cargado (`:116`); reservas emparejadas por ítem;
   - transacción (`:134`): por ítem, movimiento `Out` con motivo «Cargue - Orden … - Vehículo …» (`:176-187`), `ReleaseStock` (`:190`), **liberación LIFO de posiciones** (`:195`), liberación de lo no cargado (`:200`), unidades de carga, `reserve.Release()` y `RegisterLoaded` (`:219-220`);
   - cierre del depósito con stock 0 y de sus períodos (`:281`); commit (`:343`); avisos de trazabilidad y a roles (`:345-390`).
3. Respuesta `LoadingExecutionResultDto` con `releasedPlacements` → la UI muestra «Retirar de: …» (`LoadingOrderExecutionDialog.vue:228,289`).
4. Efecto en otros módulos: la orden pasa a Cargada o Despachada según la salida y la guía (`ImportGuideRules.ShouldDispatch`); la guía (módulo 05) congela lo cargado; la factura de almacenamiento (módulo 06) usa las salidas netas por cargue (DEC-028).

### 2.5 Novedad y su impresión
`inventory/index.vue:453` o `novelties/index.vue` → `NoveltyFormDialog.vue` (camión entre las recepciones del depósito, DF17) → `POST /warehouse/novelties` o `PUT /warehouse/novelties/{id}` → `WarehouseNoveltiesController.cs:74-110` → handlers (`CreateNoveltyCommandHandler.cs:21-39`): depósito no anulado, camión del depósito, validador; guarda con advertencia de descuadre en la auditoría (`NoveltyQuantityAudit.cs:13-29`); **después del commit** aviso Warning a ForeignTrade si dañada/faltante/sobrante > 0 (`WarehouseNoveltyService.cs:48-61`). Imprimir: `GET /warehouse/novelties/{id}/pdf` (`NoveltyReadAccess`) → `WarehouseNoveltyPdfService` (QuestPDF) → blob en pestaña nueva. CE lo ve en `DepositNoveltiesSection.vue` (solo lectura).

### 2.6 Montacargas y su factura
1. Inicio: `ForkliftUseDialog.vue` busca por placa (`GET /warehouse/search/plate/{plate}`) y envía `POST /warehouse/forklift-uses/start` `{ serviceRecordId, entryLogId, initHourmeter, vehicleType, comments, paymentMode }` (`features/warehouse/utils/forklift-start.ts:14-28`) → `StartForkliftUseCommandHandler.cs`: cliente del servicio (puede faltar), ingreso del mismo servicio, un uso activo por servicio, horómetro > 0 → `forklift_uses`.
2. Fin y cobro: `BillingCollectForm.vue` (precarga `GET /warehouse/forklift-rate`, check «Agregar IVA») → `POST /warehouse/forklift-uses/{id}/end` `{ endHourmeter, comments, billing, applyVat }` → `EndForkliftUseCommandHandler.cs:55-188`: final > inicial; tarifa por convenio o base (`ForkliftService.cs:67-139`); base = valor del cobro; IVA del catálogo solo si se marca; mora del destinatario; `Invoice` + `InvoiceItem` (servicio MONTACARGAS) y, en pago inmediato, `InvoicePayment` recibido; un solo `SaveChanges`.
3. Respuesta `ForkliftUseResultDto` (subtotal, IVA, total, mensaje). La factura aparece en `/billing/invoices` (módulo 06).

## 3. Procesos automáticos

| Proceso | Lado | Disparador | Efecto |
| --- | --- | --- | --- |
| Liberación de posiciones | Legacy | Generar la guía (`modulos/mod_salidas/verguia.php:659-676`) | `productodetalle_x_seccion` a `libre` |
| Liberación de posiciones | V2 | Ejecutar el cargue (`ExecuteLoadingOrderCommandHandler.cs:195`) y cuadre al bajar stock (`TrimToStockAsync`) | Placements reducidos o borrados, auditados |
| Avisos de trazabilidad | V2 | Ingreso, salida, cargue (`TraceabilityNotification.PublishAsync`) | Tiempo real a Admin y CE |
| Aviso de novedad | V2 | Novedad con dañada/faltante/sobrante | Notificación Warning a CE |
| Aviso de diferencia de recepción | V2 | Lo contado difiere de lo declarado | Notificación a CE |

El módulo no tiene jobs propios en `BE/Wms.Api/BackgroundJobs/` ni procesos de `cron.php`.

## 4. Integraciones externas

- **Archivos:** fotos de recepción y cargue (base64 → servicio de almacenamiento S3/local, validadas por `PhotoUploadRules`). Legacy: carpeta `fotosobservaciones/` en el servidor.
- **PDF:** QuestPDF para el «Reporte de mercancías» y la orden de trabajo de cargue.
- **Tiempo real:** `IRealtimeNotifier` para trazabilidad.
- **Sin báscula física ni lectores:** el legacy leía la guía (`id_vehiculo-nro_guia`) con lector o teclado; V2 no lee la guía en portería (decisión GAP-004).
