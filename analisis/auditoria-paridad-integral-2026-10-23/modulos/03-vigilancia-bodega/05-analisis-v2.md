# 03 · Vigilancia y Bodega — Análisis V2

> Código en disco el 2026-10-23 (según `docs/contexto/estado.md`: BE `35a61b2` / FE `c924a8b`). `BE` = `Backend/wms-api/`, `FE` = `Frontend/wms/app/`. El commit `83de58a` (camión del montacargas, recepción con todos los camiones, migración `20261008230241_AddForkliftUseEntryLog`) **está en disco** (`BE/Wms.Domain/Entities/Warehouse/ForkliftUse.cs:20-24`; `BE/Wms.Infrastructure/Migrations/20261008230241_AddForkliftUseEntryLog.cs`) pero, según `estado.md` §3, **no está en staging**.

## 1. Permisos efectivos por rol

| Política | Roles (`BE/Wms.Domain/Security/WmsPolicyRoles.cs`) | Usada en |
| --- | --- | --- |
| `GateAccess` | Admin, Receiving (`:57-58`) | `EntryLogController` (`:18-20`), `DepartureAuthorizationController` (`:12-13`) |
| `EntryCorrectionAccess` | Admin, Receiving (`:51-52`) | `EntryLogCorrectionController` (`:15-17`) |
| `WarehouseAccess` | Admin, Warehouse (`:33-34`, comentario «Vigilancia no entra a Bodega (§10 · Vigilancia, DEF-F9-002)») | `WarehouseController` (`:59-60`), `WarehousePlacementsController` (`:21-22`), escrituras de `WarehouseNoveltiesController` (`:74-75,98-99,117-118`) |
| `NoveltyReadAccess` | Admin, Warehouse, ForeignTrade (`:77-78`) | lecturas y PDF de novedades (`WarehouseNoveltiesController.cs:28-56`) |
| `AdminOnly` | Admin | alta, edición y baja de ubicaciones (`WarehouseController.cs:910-945`) |
| `BillingAccess` | Admin, Billing | `GET/PUT forklift-rates` (`ForkliftRateController.cs:44-45,71-72`) |
| `ForeignTradeAccess` | Admin, ForeignTrade | trazabilidad (`ReportController.cs:21-23`), CE-7 (`InventoryAdjustmentController.cs:20-21`) |

Frontend (`requiredRoles`): Vigilancia `["Admin","Receiving"]` (`FE/pages/operations/entries/index.vue:19`, `exits.vue:11`, `history.vue:25`); todas las páginas `/warehouse/*` `["Admin","Warehouse"]` (`FE/pages/warehouse/index.vue:4`, `receptions/*.vue`, `forklift/*.vue`, `loading-orders/*.vue`, `inventory/index.vue:38`, `novelties/index.vue:28`); `/admin/locations` y `/admin/forklift-rates` `["Admin"]`; trazabilidad `/` `["Admin","ForeignTrade"]` (`FE/pages/index.vue:10-12`). Menú: Vigilancia `["Admin","Receiving"]` (`FE/components/layout/AppMenu.vue:193-212`), Bodega `["Admin","Warehouse"]` (`:242-310`).

**Ronda de cierre punto 1 (báscula con el rol de Vigilancia).** El efecto lateral anotado en `DECISIONES_REVISION.md` §3.1 y `BASCULA_PARITY.md` §6 («ese rol también abre Bodega completa») **ya no se da**: desde DEF-F9-002 `WarehouseAccess` no incluye `Receiving` y las páginas de Bodega no lo aceptan. El operario de báscula con los dos roles ve Báscula y Vigilancia (Ingreso, Salida, Historial) y conserva la **corrección de ingresos** (`EntryCorrectionAccess`). `BASCULA_PARITY.md` §6 dice además que `POST entry-logs` exige `WarehouseAccess`: hoy exige `GateAccess`.

**DEC-005.** Al sacar `Receiving` de `WarehouseAccess` Vigilancia no perdió funciones de su flujo: sus llamadas son `entry-logs` (`GateAccess`), vehículos (`TransportCatalogAccess`, `:63-68`), conductores (`DriverCatalogAccess`), motivos de ingreso y `PATCH weighbridge/entry-log/{id}/info` (`OperationalAccess`, `WeighbridgeSharedController.cs:35`).

## 2. Frontend

| Página | Componentes / servicio | Acciones reales | Observaciones |
| --- | --- | --- | --- |
| `pages/operations/entries/index.vue` (Ingreso) | `EntryService`, `VehicleService`, `EntryReasonService`, `WeighbridgeService.updateEntryLogInfo` | Placa normalizada y validada; busca vehículo (incluye inactivos) y el ingreso abierto; crea el vehículo si no existe; `POST entry-logs`; datos opcionales de vehículo y conductor plegables (`:331-341`) que se guardan con `PATCH weighbridge/entry-log/{id}/info` (`:205-238`); contador «en planta» | Motivo obligatorio (`:173-176`) |
| `pages/operations/entries/exits.vue` (Salida) | `useEntryLogs`, `EntryService.registerDeparture` | Lista paginada de 12 abiertos con búsqueda por placa y tiempo en planta; confirma y `POST entry-logs/{id}/departure` con cuerpo vacío (autor del token) (`:96-120`) | El 409 de las guardas se muestra en el aviso (`:103-105`) |
| `pages/operations/entries/history.vue` (Historial) | `useEntryLogs`, `CorrectEntryLogDialog`, `useCreateDepartureAuthorization`, `useCreateManifest` | Filtros por placa y motivo; ver; corregir (Admin/Receiving) | Los diálogos «Autorización de Salida» y «Crear Manifiesto» (`:150-223`, plantilla `:345-463`) **no tienen disparador**: `openDepartureAuthDialog` y `openManifestDialog` (`:156,193`) no se llaman (`AppTable` solo emite `view` y `edit`, `:264-278`) → BR-03-003 |
| `pages/warehouse/receptions/entry.vue`, `index.vue`, `[id].vue`, `history.vue` | `useReceptionCreate`, `useCompleteReception`, `ReceptionStepCompletion`, `ReceptionStepManualInfo`, `DirectReceptionList`, `PendingFromWeighbridgeList` | Llegada (`register-arrival`), completar recepción, recepción directa sin báscula, historial | Ubicación opcional en la recepción |
| `pages/warehouse/inventory/index.vue` | `useStockByWarehouseStorage`, `useInventoryMovements`, `ProductPlacementsDialog`, `LocationContentPanel`, `NoveltyFormDialog` | Consultar stock por depósito, movimientos (kárdex), «Ubicaciones» por producto, pestaña «Ubicaciones» por posición, «Registrar novedad» (`:453`) | Tarjetas de estadísticas y alertas alimentadas por **stubs** (`useInventoryStatistics`, `:167-169`; plantilla `:262-298`) → BR-03-007 |
| `pages/warehouse/novelties/index.vue` | `useNovelties`, `NoveltiesTable`, `NoveltyFormDialog`, `ReasonDialog` | Listar con filtros, nueva, editar, anular, imprimir | El camión se elige entre las recepciones del depósito (DF17, `NoveltyFormDialog.vue:80-99`) |
| `pages/warehouse/forklift/index.vue`, `history.vue` | `ForkliftUseDialog`, `ForkliftUseList`, `ForkliftUseDetailDialog`, `BillingCollectForm` | Iniciar por placa (envía `entryLogId`, `features/warehouse/utils/forklift-start.ts:14-28`), finalizar y cobrar con «Agregar IVA» desmarcado (`BillingCollectForm.vue:228-238,765`) | IVA en UI con `Math.round` (`:231`) → BR-03-009 |
| `pages/warehouse/loading-orders/index.vue`, `[id].vue` | `LoadingOrderList`, `LoadingOrderExecutionDialog`, `useLoadingOrderCancel`, `downloadLoadingOrderWorkPdf` | Pendientes, detalle, ejecutar cargue (0…pedido, firma obligatoria, cuadrilla, «Retirar de» con `releasedPlacements`, `LoadingOrderExecutionDialog.vue:86-96,228,289`), cancelar con motivo, orden de trabajo PDF | — |
| `pages/admin/locations/index.vue` | `useWarehouseLocations`, mutaciones | CRUD de ubicaciones con «Estado» (disponible) | Capacidad mostrada en kg (`:301-303`) |
| `pages/admin/forklift-rates/index.vue` | `ForkliftRatesGrid`, `forklift-rate-service.ts` | Tarifa base por tipo de vehículo | Página solo Admin; el API admite también Billing |
| `pages/index.vue` (Trazabilidad) | `features/traceability/*` | KPIs y camiones por etapa, filtro por placa y fecha | Etapa «Cancelado» (`features/traceability/types/index.ts:16`) |

**Mocks o datos estáticos:** `FE/features/warehouse/services/warehouse-service.ts:570-596` (`getInventoryStatistics` → `null`, `getStockAlerts` → `[]`, `getStockHistorySummary` → `[]`) y `:690-712` (`getLocationOccupancySummary`, `getLocationStatistics`, `getLocationHierarchy`), marcados «stubs - backend not implemented yet». Solo el primero llega a una página (inventario), donde la tarjeta queda oculta.

## 3. Backend: endpoints del módulo y consumidor

| Endpoint | Política | Consumidor FE | Nota |
| --- | --- | --- | --- |
| `POST entry-logs` | GateAccess | `entry-service.ts:29-32` ← `entries/index.vue` | Autor del token (`EntryLogController.cs:28-31`) |
| `GET entry-logs`, `GET entry-logs/{id}` | GateAccess | `entry-service.ts:19-27` | Filtro de placa parcial (`GetAllEntryLogsQuery.cs`) |
| `PATCH entry-logs/{id}` | GateAccess | **ninguno** (`updateEntryLog`, `entry-service.ts:34-40`, sin llamadas) | Cambia conductor, motivo, observaciones y vincula un `ServiceRecord` sin la guarda D07 → BR-03-001 |
| `PUT entry-logs/{id}/correction` | EntryCorrectionAccess | `CorrectEntryLogDialog.vue` vía `useCorrectEntryLog` | — |
| `POST entry-logs/{id}/departure` | GateAccess | `exits.vue:101` | Guardas CHG-30 y CHG-33 |
| `POST entry-logs/{id}/departure-authorizations` | GateAccess | diálogo inalcanzable (`history.vue:150-178`) | BR-03-003 |
| `PATCH departure-authorizations/{id}` | GateAccess | **ninguno** (`useUpdateDepartureAuthorization` sin uso) | Aplica la misma guarda al aprobar (`UpdateDepartureAuthorizationHandler.cs:85`) |
| `POST entry-logs/{id}/manifests` | GateAccess | diálogo inalcanzable (`history.vue:186-223`) | BR-03-003 |
| `GET warehouse/receptions`, `/{id}`, `POST receptions`, `/register-arrival`, `/{id}/complete`, `/without-weighbridge`, `GET pending-from-weighbridge`, `pending-direct-reception`, `search/plate/{plate}`, `warehouse-storages/{id}/cargo-units` | WarehouseAccess | `warehouse-service.ts:82-260,499-500` | Recepción directa: autor del token (`WarehouseController.cs:343-346`) |
| `GET forklift-uses`, `/active`, `/{id}`, `forklift-rate`, `POST forklift-uses/start`, `/{id}/end`, `PATCH /{id}/payment-mode` | WarehouseAccess | `warehouse-service.ts:272-361` | «Cambiar modo de pago» solo visible sin factura y fuera de «InProgress» (`ForkliftUseDetailDialog.vue:79`): con `End` siempre facturando, el botón no aparece en la práctica |
| `GET loading-orders/pending`, `/{id}`, `/{id}/pdf`, `POST /{id}/execute`, `PATCH /{id}/cancel` | WarehouseAccess | `warehouse-service.ts:375-449`; `loading-orders/[id].vue:38,45` | Autor del cargue del token (`WarehouseController.cs:858-859`) |
| `POST warehouse/loading-orders` | WarehouseAccess | **ninguno** (`useLoadingOrderCreate`, `useLoadingOrderMutations.ts:25-33`, sin uso; CE usa `POST foreign-trade/loading-orders`) | BR-03-002 |
| `GET/POST/PATCH/DELETE warehouse/locations` | lectura WarehouseAccess; escritura AdminOnly | `warehouse-service.ts:536-568` | `DELETE` no revisa ubicaciones con mercancía → BR-03-008 |
| `GET warehouse/inventory/movements`, `/stock/{id}`, `/deposits` | WarehouseAccess | `warehouse-service.ts:476-519` | `deposits` con `IncludeReceivedDrafts` |
| `POST warehouse/inventory/adjustments` | ForeignTradeAccess (`InventoryAdjustmentController`) | detalle de depósito CE (`useInventoryAdjustment`) | CE-7, DEC-019 |
| `GET/POST warehouse/storage-products/{id}/placements`, `/move`, `/release`, `GET warehouse/locations/{id}/placements` | WarehouseAccess | `warehouse-service.ts:614-650` | Transacción y `Describe` de auditoría (`PlaceStockCommandHandler.cs:21-31`) |
| `GET/POST warehouse/novelties`, `GET/PUT /{id}`, `POST /{id}/void`, `GET /{id}/pdf` | lectura NoveltyReadAccess; escritura WarehouseAccess | `warehouse-service.ts:659-687`; `DepositNoveltiesSection.vue` en los tres detalles de CE | — |
| `GET forklift-rates`, `/vehicle-types`, `PUT /{vehicleType}` | Authorize; GET/PUT BillingAccess | `forklift-rate-service.ts:7-18` | Facturación no llega a la página (solo Admin) |
| `GET reports/traceability` | ForeignTradeAccess | `traceability-service.ts:9-14` | — |

**Llamadas del frontend sin endpoint:** `useReceptionReceiptPdf` (`FE/features/warehouse/composables/useWarehouseExports.ts:41-48`) llama a `warehouseService.downloadReceptionReceiptPdf`, que no existe en el servicio ni en el API. El composable se exporta (`composables/index.ts:124`) pero ninguna página lo usa: código muerto ya señalado como fuera de alcance por el plan frontend (F4-03, §G). Sin impacto en pantalla.

## 4. Contratos (DTO ↔ TypeScript)

| Operación | Backend | Frontend | Resultado |
| --- | --- | --- | --- |
| Ingreso | `CreateEntryLogRequest` (`EntryLogController.cs:120-126`); `EntryLogDto` (`Wms.Application/Logistics/Common/Dtos/EntryLogDto.cs:6-44`) | `ICreateEntryLogRequest`, `IEntryLog` (`features/entries/types/entry-log.ts:4-29`) | Coinciden (estado `Registered`/`Completed` por nombre; `JsonStringEnumConverter`, `Wms.Api/Program.cs:63`). El TS no declara `manifests` ni `departureAuthorizations` (no se leen) |
| Manifiesto | `CreateManifestRequest(ManifestNumber, ManifestWeight)` (`EntryLogController.cs:131-133`) | `ICreateManifestRequest` con `manifestPackaging`, `manifestAmount`, `unitMeasure` de más (`entry-log.ts:119-125`) | El API los ignora (BR-03-003) |
| Ubicaciones | `PlacementDtos.cs:4-43` | `types/placements.ts` | Coinciden campo a campo |
| Novedades | `WarehouseNoveltyDto.cs:7-40`; `WarehouseNoveltyRequests.cs:7-54` | `types/novelty.ts:35-101` | Coinciden; enums por nombre |
| Cargue | `ExecuteLoadingOrderRequest`, `LoadingItemResultDto` (con `ReleasedPlacements`) | `types/loading-order.ts` y `LoadingOrderExecutionDialog.vue:165-195,228` | Coinciden (verificado en los campos usados) |
| Montacargas | `StartForkliftUseCommand` (`Commands/Forklift/StartForkliftUseCommand.cs:12-20`), `EndForkliftUseRequest` | `IStartForkliftUseRequest`, `IEndForkliftUseRequest` (`types/forklift.ts:57-90`) | Coinciden (`entryLogId`, `applyVat`, `billing`) |

## 5. Kárdex, stock y posiciones

- **Recepción:** no cambia el stock (DEC-010); ubica lo descargado hasta lo pendiente (`PlaceUpToPendingAsync`). Recepción directa: entra el stock declarado con movimiento `DeclaredEntry` (`CreateReceptionWithoutWeighbridgeCommandHandler.cs:267-276`).
- **Ubicar, mover, liberar:** solo filas de `warehouse_storage_product_placements` (auditadas, `WarehouseStorageProductPlacement : IAuditable`); no tocan stock ni kárdex, como el legacy.
- **Cargue:** movimiento `Out` por lo cargado con el usuario del token, baja de stock y reserva, liberación del resto de la reserva, liberación LIFO de posiciones y cierre del depósito con stock 0 (`ExecuteLoadingOrderCommandHandler.cs:134-281`).
- **Cuadre posiciones ↔ stock:** `TrimToStockAsync` en anulación de depósito, anulación de pesaje, ajuste CE-7 y edición de productos; el retiro de un producto borra sus posiciones en cascada (`WarehouseStorageProductPlacementConfiguration.cs:31-34`). La guía y la reversión no tocan posiciones (sin referencias a `Placement` en `ForeignTrade/Commands/CreateDispatchGuide`, `CreateExportDispatchGuide`, `CancelDispatchGuide`, `RevertLoadingOrder`).
- **Migración:** `LocationsImporter` crea las ubicaciones desde `bodega`/`seccion` (`Administration/LegacyImport/Importers/LocationsImporter.cs:118-123`); `DepositsImporter` no carga posiciones (grep de `ubic`, `location`, `placement`, `seccion` sin resultados): el stock migrado queda «por ubicar» → BR-03-006.

## 6. Montacargas y su paso a facturación

`EndForkliftUseCommandHandler.cs:55-188`: finaliza, resuelve la tarifa (convenio activo o `ForkliftRate` por tipo, `ForkliftService.cs:67-139`), toma como base el valor del cobro, suma el IVA del catálogo solo con `applyVat`, valida mora del destinatario registrado, crea `Invoice` + `InvoiceItem` del servicio `MONTACARGAS` con la placa del camión del uso en las notas y, en pago inmediato, el `InvoicePayment`. Todo en un solo `SaveChanges`. El detalle de la factura lo audita el módulo 06. `ForkliftUse` **no** es `IAuditable` (`ForkliftUse.cs:11`): inicio, fin, horómetros e IVA no quedan en `audit_logs` (sí la factura) → BR-03-011.

## 7. Documentación V2 desactualizada

`BE/Wms.Application/Warehouse/README.md:134` («Actualiza warehouse_storage (stock + status STORED)»), `GUIA_USUARIO.md:224` («Actualiza stock en inventario») y `Commands/Reception/README.md` (pasos 6-7: «Crea InventoryMovement (tipo IN)», «incrementa stock») contradicen DEC-010 y el código actual (§5). No es brecha funcional; se anota para el consolidado.

## 8. Capacidades SOLO_V2

| ID | Capacidad | Confirmada | Evidencia principal |
| --- | --- | --- | --- |
| CF-V030 | Vigilancia: ingreso y salida de vehículos (motivo, placa, guardas de salida) | Sí (el legacy no registraba ingresos; la salida reemplaza a CF-L230) | `EntryLogController.cs`; `entries/index.vue`, `exits.vue` |
| CF-V031 | Corrección de ingresos | Sí | `EntryLogCorrectionController.cs`; `CorrectEntryLogDialog.vue` |
| CF-V032 | Recepción informativa en Bodega | Sí | `CreateReceptionCommandHandler.cs`, `CompleteReceptionCommandHandler.cs`; `receptions/index.vue` |
| CF-V033 | Montacargas: uso, cobro con IVA opcional y tarifas base | Sí (sin equivalente legacy) | `StartForkliftUseCommandHandler.cs`, `EndForkliftUseCommandHandler.cs`, `ForkliftRateController.cs` |
| CF-V034 | Trazabilidad por placa | Sí | `ReportController.cs:36-45`; `TruckStageResolver.cs` |
| CF-V035 | Inventario de Bodega (stock, kárdex, ubicaciones) | Sí, con piezas en stub | `inventory/index.vue` |
| CF-V036 (nueva) | Autorizaciones de salida y manifiestos desde Vigilancia | API sí; UI inalcanzable | `EntryLogController.cs:88-116`; `DepartureAuthorizationController.cs` |
| CF-V037 (nueva) | Recepción directa sin báscula («Solo bodega») | Sí | `WarehouseController.cs:280-347`; `DirectReceptionList.vue` |
| CF-V038 (nueva) | Cancelar una orden de cargue desde Bodega con motivo | Sí | `WarehouseController.cs:830-844`; `loading-orders/[id].vue:74-140` |
| CF-V039 (nueva) | Orden de trabajo de cargue en PDF para Bodega (WMS-17) | Sí | `WarehouseController.cs:770-786`; `loading-orders/[id].vue:37-60,125` |
