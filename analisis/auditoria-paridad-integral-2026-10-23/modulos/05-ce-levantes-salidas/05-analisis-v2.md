# 05 · Análisis V2: levantes, órdenes de cargue, salidas y guías

> Código en disco el 2026-10-23 (según `docs/contexto/estado.md`: BE `35a61b2` / FE `c924a8b`). **Prefijos:** `B/` = `Backend/wms-api/`, `F/` = `Frontend/wms/app/`, `FT/` = `Backend/wms-api/Wms.Application/ForeignTrade/`, `C/` = `Backend/wms-api/Wms.Api/Controllers/v1/`.
> El commit `2eeaaad` (producto y cantidad en el historial de guías, cambio del modo de pago de la guía con `DispatchGuideInvoicedRule`, unidad de carga al crear la orden) **está en disco** (`FT/Common/DTOs/DispatchGuideDto.cs:51-62`; `FT/Commands/ChangeDispatchGuidePaymentMode/ChangeDispatchGuidePaymentModeCommandHandler.cs:66-75`; `F/features/foreign-trade/components/LoadingOrderForm.vue:471-476`) pero, según `estado.md` §3, **no está en staging**.

## 1. Permisos

| Política (`B/Wms.Domain/Security/WmsPolicyRoles.cs`) | Roles | Endpoints del módulo |
| --- | --- | --- |
| `ForeignTradeAccess` (`:37`) | Admin, ForeignTrade | Todo `C/ForeignTradeController.cs` (`:63-64`), `ReleasesController.cs:16-17`, `ImportReleaseActionsController.cs:17-18`, `LoadingOrderCorrectionsController.cs:21-22`, `LoadingOrderExitController.cs:17-18` |
| `WarehouseAccess` (`:34`) | Admin, Warehouse | `C/WarehouseController.cs` órdenes: `GET loading-orders/pending` (`:673`), `/{id}` (`:745`), `/{id}/pdf` (`:770`), `POST loading-orders` (`:791`, sin consumidor, BR-03-002), `PATCH /{id}/cancel` (`:830`), `POST /{id}/execute` (`:846`) — módulo 03 |
| `ScaleAccess` (`:38`) | Admin, Scale | `C/WeighbridgeOutputSharingController.cs:18,31,49` (pesaje compartido y salida con tiquete) — módulo 02 |
| `GateAccess` (`:58`) | Admin, Receiving | `C/DepartureAuthorizationController.cs:12-13,16` — módulo 03 (CF-V036) |
| `[Authorize]` (lectura) / `AdminOnly` (escritura) | — | `C/CitiesController.cs:24,34,43,61`, `C/CrewsController.cs:19,23,36,51,68` — módulo 01 |

Frontend: todas las páginas `F/pages/foreign-trade/{releases,loading-orders,dispatch-guides}/*` declaran `requiredRoles: ["Admin","ForeignTrade"]` (p. ej. `loading-orders/[id]/index.vue:22`, `dispatch-guides/index.vue`, `dispatch-guides/pending.vue:7`, `releases/index.vue`); menú «Comercio Exterior» con Levantes, Órdenes (crear, listar) y Guías (crear, historial, pendientes) (`F/components/layout/AppMenu.vue:313-378`). Coinciden con la política del API.

## 2. Frontend

| Página | Componentes / servicio | Acciones reales | Observaciones |
| --- | --- | --- | --- |
| `pages/foreign-trade/imports/[id]/index.vue` (detalle IMP, sección Levantes) | `ReleaseForm.vue`, `WithdrawReleaseDialog.vue`, `ExitWithEntryTicketDialog.vue`; `useRegisterRelease`, `useUpdateImportRelease`, `useWithdrawRelease` | Registrar (`:675`, `canRegisterRelease` por recibido − levantes, `utils/release-rules.ts`), editar (`:704`), «Registrar otro producto con este levante» (DF4, `:706-714`), retirar con motivo (`:717-725`); columnas FOB/tasa/FOB COP; «Salida con este tiquete» en el historial de pesaje (`:778`, DF18) | Máximo de cantidad = recibido − otros levantes (`ReleaseForm.vue:128-133,286-290`); 409 de duplicado bajo su campo (`:354-370`); tasa manual solo si la DIAN no respondió (`:307-309`) |
| `pages/foreign-trade/releases/index.vue` | `useReleases`, `useStakeholders` (`all: true`) | Listado con filtros (levante/aceptación, depósito, importador, agencia, fechas) y Excel con `all=true` | **Las fechas se envían como `toISOString()`** (`:49-50`) a un `DateOnly` del API → el filtro se pierde (BR-05-007) |
| `pages/foreign-trade/loading-orders/create.vue` | `LoadingOrderForm.vue` (1150 líneas), `useCreateLoadingOrder`, `useLoadingOrderDeposits`, `useCities`, `CrewSelect` | Selector de depósitos (`loading-orders/deposits`), «Nacionalizado disponible» y «Sin levante» (`:256-284,769-773`), unidad de carga obligatoria en depósitos por unidad (`:509-516`), ciudad del catálogo obligatoria (`:443-447,1042`), cuadrilla, orden externa con soporte (`:161-225,600-665`), estado financiero por cliente (`:426-437,580`) | Envía `warehouseStorageCargoUnitId` (`:471-476`) aunque `ICreateLoadingOrderItemRequest` no lo declara (`types/loading-order.ts:74-77`) |
| `pages/foreign-trade/loading-orders/index.vue` | `useLoadingOrders` | Filtro por estado (incluye `Reverted`) y un criterio de búsqueda (`:29-46`); Excel con `all=true` (`:84-100`) | Sin filtro de fechas en pantalla (el API lo admite); botón «Ejecutar orden» comentado (`:279-285`) |
| `pages/foreign-trade/loading-orders/[id]/index.vue` | `useLoadingOrderDetail`, `useCancelLoadingOrder`, `useRevertLoadingOrder`, `EditLoadingOrderItemsDialog.vue`, `ReasonDialog`, `CorrectionResultDialog` | Modificar ítems y Cancelar en `Pending`/`InProgress` (`:44-46`); Revertir en `Loaded`/`Dispatched`/`Complete` (`:48`) con «Ir a guías» ante el 409 de la guía (`:119-134`); «Orden de trabajo (PDF)» (`:53-78,185-191`); columna «Cargado» | **Cancelar y Modificar no miran si la orden tiene guía vigente** (BR-05-001); la cabecera es de solo lectura (BR-05-005) |
| `pages/foreign-trade/dispatch-guides/create.vue` | `DispatchGuideForm.vue`, `BillingCollectForm.vue`, `useCreateDispatchGuide`, `useDispatchGuidePreview`, `useCities` | Orden pendiente (precargable por `?loadingOrderId=`), fecha de salida, vencimiento calculado o digitado (`DispatchGuideForm.vue:117-160`), firmante (forzado a conductor con varios dueños o importadores, `:96-113`), cobro centralizado | El selector de órdenes pide `pageSize: 50` (`:29-34`): con más de 50 pendientes, la precarga desde «Pendientes» puede fallar (BR-05-008) |
| `pages/foreign-trade/dispatch-guides/index.vue` | `useDispatchGuides`, `useChangeDispatchGuidePaymentMode`, `useCancelDispatchGuide`, `ChangePaymentModeDialog` | Historial con productos por línea y clientes (2eeaaad), PDF, ZIP por depósito, «Cambiar modo de pago» si `canChangePaymentMode`, «Anular guía» si no está anulada, Excel con `all=true` | Sin filtro por fecha; búsqueda libre por guía, orden, cliente, placa |
| `pages/foreign-trade/dispatch-guides/pending.vue` | `usePendingGuides` (refresco cada 30 s) | Lista de órdenes IMP sin guía vigente con «Generar Guía» | — |

**Mocks o datos estáticos:** ninguno en las páginas del módulo. `useValidateClientStatus.ts` no se usa (el formulario llama al servicio directamente).

## 3. Backend: endpoints del módulo y consumidor

| Endpoint | Handler | Consumidor FE |
| --- | --- | --- |
| `POST foreign-trade/imports/{id}/releases` (`C/ForeignTradeController.cs:181`) | `FT/Commands/RegisterImportRelease/RegisterImportReleaseCommandHandler.cs` | `foreign-trade-service.ts:186-197` ← `ReleaseForm.vue` |
| `PATCH foreign-trade/imports/{id}/releases/{releaseId}` (`:214`) | `UpdateImportReleaseCommandHandler.cs` (`PatchField` para observaciones y FOB) | `:248-258` |
| `POST foreign-trade/imports/{id}/releases/{releaseId}/withdraw` (`ImportReleaseActionsController.cs:32`) | `WithdrawImportReleaseCommandHandler.cs` | `:205-215` ← `WithdrawReleaseDialog.vue` |
| `GET foreign-trade/releases` (`ReleasesController.cs:23`) | `GetReleasesHandler.cs` (excluye depósitos anulados) | `:948-951` |
| `GET foreign-trade/loading-orders` (`:913`) | `GetLoadingOrdersHandler.cs` | `:441-450`; también `ExitWithEntryTicketDialog.vue` (`searchField=LicensePlate`, `all=true`) |
| `GET foreign-trade/loading-orders/deposits` (`:927`) | `GetLoadingOrderDepositsHandler.cs` (+ `nationalizedQuantity`/`nationalizedAvailable`) | `:453-473` |
| `GET foreign-trade/loading-orders/{id}` (`:962`) | `GetLoadingOrderDetailHandler.cs` | `:490-497` |
| `GET foreign-trade/loading-orders/{id}/dispatch-guide-preview` (`:987`) | `GetDispatchGuidePreviewQuery` | `:597-604` ← `DispatchGuideForm.vue` |
| `POST foreign-trade/loading-orders` (`:1005`) | `CreateLoadingOrderCommandHandler.cs` | `:478-485` |
| `GET foreign-trade/loading-orders/{id}/pdf` (`:1052`) | `LoadingOrderPdfService` (orden de trabajo, WMS-17) | `:501-503` |
| `PATCH foreign-trade/loading-orders/{id}/cancel` (`:1072`) | `B/Wms.Application/Warehouse/Commands/LoadingOrder/CancelLoadingOrder/CancelLoadingOrderHandler.cs` | `:510-517` |
| `PUT foreign-trade/loading-orders/{id}/items` (`LoadingOrderCorrectionsController.cs:34`) | `UpdateLoadingOrderItemsCommandHandler.cs` + `LoadingOrderReservationService.cs` | `:522-529` ← `EditLoadingOrderItemsDialog.vue` |
| `POST foreign-trade/loading-orders/{id}/revert` (`:102`) | `RevertLoadingOrderCommandHandler.cs` | `:534-541` |
| `POST foreign-trade/loading-orders/{id}/exit-with-entry-ticket` (`LoadingOrderExitController.cs:30`) | `B/Wms.Application/Weighbridge/Commands/Output/ExitWithEntryTicket/ExitWithEntryTicketCommandHandler.cs` | `:935-941` ← `ExitWithEntryTicketDialog.vue` |
| `GET foreign-trade/dispatch-guides` (`:1098`) | `GetDispatchGuidesHandler.cs` | `:562-576` |
| `GET foreign-trade/dispatch-guides/pending-orders` (`:1114`) | `GetPendingImportLoadingOrdersHandler.cs` (`Pending`…`Complete` sin guía vigente) | `:581-592` ← `DispatchGuideForm.vue` |
| `GET foreign-trade/dispatch-guides/pending` (`:1128`) | `GetPendingGuidesQuery.cs` | `:609-614` ← `pending.vue`, `useForeignTradeDashboard.ts:59-63` |
| `GET foreign-trade/dispatch-guides/{id}/pdf` (`:1143`) | `DispatchGuidePdfService.cs` (marca «ANULADA» `:366-372`, cuadrilla `:599`, vence `:613-615`) | `:630-634` |
| `GET foreign-trade/dispatch-guides/{id}/pdf/per-deposit` (`:1166`) | `GetDispatchGuidePerDepositZipHandler.cs` (registra `DispatchGuidePrintLog`, `:68-71`) | `:640-642` |
| `POST foreign-trade/dispatch-guides` (`:1199`) | `CreateDispatchGuideCommandHandler.cs` | `:620-627` |
| `PATCH foreign-trade/dispatch-guides/{id}/payment-mode` (`:1233`) | `ChangeDispatchGuidePaymentModeCommandHandler.cs` | `:646-655` |
| `POST foreign-trade/dispatch-guides/{id}/cancel` (`LoadingOrderCorrectionsController.cs:72`) | `CancelDispatchGuideCommandHandler.cs` | `:546-553` |
| (interno) guía de exportación automática | `CreateExportDispatchGuideCommandHandler.cs`, llamado al final del cargue (`B/Wms.Application/Warehouse/Commands/LoadingOrder/ExecuteLoadingOrderCommandHandler.cs:352-366`) | — |

**Endpoints sin consumidor del módulo:** `POST warehouse/loading-orders` (ya registrado como BR-03-002) y `PATCH departure-authorizations/{id}` (BR-03-003, CF-V036). Ninguno nuevo.
**Llamadas del frontend sin endpoint:** ninguna. Se contrastaron las 22 rutas de `foreign-trade-service.ts` del módulo con los atributos `[Http*]` citados.

## 4. Contratos (DTO ↔ TypeScript)

| Operación | Backend | Frontend | Resultado |
| --- | --- | --- | --- |
| Registrar/editar levante | `RegisterImportReleaseRequest`, `UpdateImportReleaseRequest` (`ForeignTradeController.cs:1265-1293`) | `IRegisterReleaseRequest` (`types/import-deposit.ts:279-292`) | Coinciden; la edición ignora `warehouseStorageProductId` |
| Levante en el detalle | `ImportReleaseDto` (15 campos) | `IImportReleaseDto` (`import-deposit.ts:109-130`) | Coinciden campo a campo |
| Listado de levantes | `GetReleasesQuery.FromDate/ToDate` = `DateOnly?` (`FT/Queries/GetReleases/GetReleasesQuery.cs:19-20`); `ReleaseListItemDto` | `IGetReleasesQuery` (`string`), `releases/index.vue:49-50` envía `toISOString()` | **Incompatible:** `DateOnly` no admite hora; con `SuppressModelStateInvalidFilter` (`B/Wms.Api/Program.cs:69`) el valor queda nulo y el filtro se ignora sin error (el binder de Colombia solo cubre `DateTimeOffset`, `B/Wms.Api/Common/ModelBinding/ColombiaDateTimeOffsetModelBinder.cs:55-63`) → BR-05-007. Las filas coinciden |
| Crear orden | `CreateLoadingOrderRequest` / `CreateLoadingOrderItemRequest` (`ForeignTradeController.cs:1317-1340`) | `ICreateLoadingOrderRequest` / `ICreateLoadingOrderItemRequest` (`types/loading-order.ts:54-77`) | El TS no declara `warehouseStorageCargoUnitId` del ítem (el formulario lo envía igual) ni el `destinationCity` de texto (ignorado) → BR-05-013 |
| Depósitos para la orden | `LoadingOrderDepositDto` / `...ProductDto` (`JsonIgnore` en recibido y reservado) | `types/loading-order-deposit.ts` | Coinciden; el TS declara además `cargoHandling` del depósito, que no viaja (opcional, sin uso) |
| Detalle de la orden | `LoadingOrderDto` (`B/Wms.Application/Warehouse/Common/DTOs/LoadingOrderDto.cs`) | `ILoadingOrder` (`F/features/warehouse/types/loading-order.ts`) | Coinciden los 29 campos de la orden y los 15 del ítem (`loadedQuantity`, `revertedAt`, `reversalReason`, `crewName`, `destinationCityId`) |
| Modificar ítems | `UpdateLoadingOrderItemsRequest` | `IUpdateLoadingOrderItemsRequest` (`types/loading-order.ts:89-98`) | Coinciden |
| Revertir | `RevertLoadingOrderResultDto` | `IRevertLoadingOrderResultDto` (`:101-107`) | Coinciden |
| Emitir guía | `CreateDispatchGuideRequest` (`ForeignTradeController.cs:1342-1350`) | `ICreateDispatchGuideRequest` (`types/dispatch-guide.ts`) | Coinciden (`expirationDate` nulo con días de tránsito) |
| Historial de guías | `DispatchGuideDto` (`FT/Common/DTOs/DispatchGuideDto.cs:3-68`) | `IDispatchGuideDto` (`types/dispatch-guide.ts:59-112`) | El TS declara `signerType` y `signerName` (`:73-74`), que el DTO no tiene; no se leen en pantalla → BR-05-013 |
| Anular guía | `CancelDispatchGuideResultDto` + `CancelledInvoiceDto` (con `Total`) + `InvoiceToReviewDto` | `ICancelDispatchGuideResultDto` (`:155-161`) | Coinciden (el TS omite `total` de la anulada, que no se muestra) |
| Pendientes de guía | `PendingImportLoadingOrderDto` | `IPendingImportLoadingOrderDto` (`:11-33`) | Coinciden |
| Salida con tiquete | `ExitWithEntryTicketResultDto` (`.../ExitWithEntryTicketCommand.cs:12-19`) | `IExitWithEntryTicketResult` (`F/features/weighbridge/types/weighbridge-cycle.ts:246-255`) | Coinciden |

Enums viajan por nombre (`JsonStringEnumConverter`, `B/Wms.Api/Program.cs:63`). Paginación: listados exportan con `all=true`; ningún componente sube `pageSize` salvo el selector de la guía (50).

## 5. Estados y transiciones

**Orden de cargue** (`B/Wms.Domain/Enums/LoadingOrdersStatus.cs`; `B/Wms.Domain/Entities/Warehouse/LoadingOrder.cs`):

| De → a | Disparador | Evidencia |
| --- | --- | --- |
| — → `Pending` | Crear orden | `LoadingOrder.cs:130` |
| `Pending` → `InProgress` | Inicio de salida en báscula o con tiquete; inicio del cargue en Bodega | `:203-214` (`BeginWeighbridgeExit`), `:186-193` (`StartLoading`) |
| `InProgress` → `Pending` | Se descarta la salida en báscula | `:225-235` |
| `Pending`/`InProgress` → `Loaded` | Ejecutar cargue | `:241-253` |
| `Loaded` → `Dispatched` | Salida registrada + guía vigente (IMP) | `ImportGuideRules.ShouldDispatch`; `CreateDispatchGuideCommandHandler.cs:410-417`; `CreateExportDispatchGuideCommandHandler.cs:146-147` |
| `Dispatched` → `Loaded` | Anulación del pesaje de salida | `LoadingOrder.cs:281-289`; `VoidWeighingCommandHandler.cs:104,364` |
| `Pending`/`InProgress` → `Cancelled` | Cancelar (motivo 10–500) | `:309-330` |
| `Loaded`/`Dispatched`/`Complete` → `Reverted` | Revertir sin guía vigente | `:337-356`; `RevertLoadingOrderCommandHandler.cs:41-46` |
| → `Complete` | `LoadingOrder.Complete()` (`:294-302`) | **Sin llamadores** en `Wms.Application` (grep `.Complete();`): estado residual → BR-05-013 |

**Guía de salida** (`B/Wms.Domain/Entities/Warehouse/DispatchGuide.cs`): vigente → anulada (`Cancel`, `:176-187`, conserva número); cambio de modo de pago solo vigente y no facturada (`:194-208`; `DispatchGuideInvoicedRule.cs:20-37`). Una guía vigente por orden (`CreateDispatchGuideCommandHandler.cs:137-143,216-222`); el índice de `loading_order_id` no es único (`B/Wms.Infrastructure/Persistence/Configurations/Warehouse/DispatchGuideConfiguration.cs:38`).

**Incoherencia de transiciones:** `EnsureGuidable` (`LoadingOrder.cs:390-398`) permite emitir la guía con la orden `Pending` o `InProgress`, y `Cancel` (`:309-330`) y `EnsureItemsEditable` (`:402-409`) no comprueban si hay guía vigente; `Revert` sí la exige (`RevertLoadingOrderCommandHandler.cs:44-46`). El único bloqueo es retirar un ítem que figura en una guía (`LoadingOrderReservationService.cs:135-143`) → BR-05-001.

## 6. Transacciones y concurrencia

| Operación | Transacción | Bloqueo | Observación |
| --- | --- | --- | --- |
| Crear orden | Sí (`CreateLoadingOrderCommandHandler.cs:309-424`) | Solo la fila del consecutivo `OC` (`DocumentNumberGenerator.cs:30-37`) | Stock, reservado y levantes se leen **antes** de la transacción (`:79-198`) y se escriben como valores absolutos (`WarehouseStorageProduct.ReserveStock`, `B/Wms.Domain/Entities/Warehouse/WarehouseStorageProduct.cs:239-249`) |
| Modificar ítems | Sí (`UpdateLoadingOrderItemsCommandHandler.cs:59-121`) | Ninguno | Ídem |
| Cancelar orden | `SaveChanges` único (`CancelLoadingOrderHandler.cs:47-50`) | Ninguno | — |
| Ejecutar cargue (módulo 03) | Sí (`ExecuteLoadingOrderCommandHandler.cs:134`) | Ninguno | Puede cruzarse con cancelar o modificar |
| Registrar, editar o retirar levante | `SaveChanges` único | Ninguno | La guarda de «usado» lee el reservado sin bloqueo |
| Emitir guía | Sí (`CreateDispatchGuideCommandHandler.cs:213-459`) | `warehouse_storage_products … FOR UPDATE` al congelar saldos (`DispatchGuideBalanceService.cs:28-30`) y consecutivo `S` | La comprobación de guía existente precede a los bloqueos (`:216-222`) y no hay índice único filtrado: un doble envío simultáneo podría crear dos guías (el botón está protegido, DEF-F10-001 Verificado) |
| Revertir | Sí (`RevertLoadingOrderCommandHandler.cs:55-111`) | Ninguno | — |

No hay `IsConcurrencyToken`/`RowVersion` ni `CHECK` sobre `warehouse_storage_products.reserved_stock` (grep en `B/Wms.Infrastructure/Persistence/Configurations`). Dos usuarios de Comercio Exterior (o Comercio Exterior y Bodega) que operen a la vez sobre el mismo producto pueden perder una actualización del reservado y despachar por encima de lo nacionalizado → BR-05-002. La aclaración «un solo operario de báscula» (`docs/qa/00-plan-maestro.md` §10) no cubre Comercio Exterior.

## 7. Anulaciones y sus efectos

| Acción | Stock | Kárdex | Reserva | Factura de la guía | Consecutivo | Evidencia |
| --- | --- | --- | --- | --- | --- | --- |
| Cancelar orden | — | — | Libera todas (y la de la unidad de carga) | **No la toca** si hay guía vigente | La orden conserva su número | `CancelLoadingOrderHandler.cs:41-49`; `LoadingOrderReservationService.cs:161-175` |
| Modificar ítems | — | — | Ajusta, libera o reserva | **No la toca** (la guía conserva lo pedido) | — | `LoadingOrderReservationService.cs:98-154` |
| Anular guía | — | — | — | Anula la factura en Borrador/Pendiente sin pagos ni consolidación; las demás quedan «para revisar» con aviso a Facturación | La guía conserva el número | `CancelDispatchGuideCommandHandler.cs:32-60`; `B/Wms.Application/Billing/Common/Services/InvoiceCancellationPolicy.cs:21-24,59-77` |
| Revertir orden | Devuelve lo cargado (`ReturnDispatchedStock`) | `In` / `LoadingOrderReversal` | Ya inactivas | Exige la guía anulada antes | — | `RevertLoadingOrderCommandHandler.cs:57-118` |
| Retirar levante | — | — | — | — | — | `WithdrawImportReleaseCommandHandler.cs:66-87` (auditoría con `Describe`, aviso si queda sin nacionalizar) |

Una guía de contado nace pagada (`CreateDispatchGuideCommandHandler.cs:306-322,377-391`): al anularla siempre queda «para revisar», como dice §B.4.4. En crédito consolidado la línea queda en la factura consolidada del cliente, que tampoco se toca (`InvoiceCancellationPolicy.CanAutoCancel`).

## 8. Guía: PDF, cobro y paso a facturación

- **PDF** bajo demanda para importación y exportación, con saldos congelados por línea (WMS-19, `DispatchGuideBalanceService.cs:9-80`), levante congelado en la línea (CHG-35), cuadrilla, vencimiento y marca «ANULADA».
- **Cobro** (IMP): servicio `GUIA_SALIDA`, tarifa del convenio del cliente o precio base (`ForeignTradeService.cs:22-57`), por cada depósito del cliente dueño (`DispatchGuideBillingPlan.cs`), una factura por dueño con «Clientes» (CHG-34) o una sola con destinatario único y total editable; contado → pago `Received`; crédito → factura propia o consolidada. Sin precio: 400 (`DispatchGuideBillingPlan.cs:46-52`). El motor y el ciclo de la factura los audita el módulo 06.
- **Exportación:** guía automática, sin PDF entregado ni cobro, con `PaymentMode = Immediate` por defecto (`CreateExportDispatchGuideCommand.cs:11-15`). Si falla, solo se registra en el log (`ExecuteLoadingOrderCommandHandler.cs:355-366`) y no hay ruta para emitirla a mano (`CreateDispatchGuideCommandHandler.cs:125-130`) → BR-05-009.

## 9. Capacidades SOLO_V2

| ID | Capacidad | Resultado | Evidencia principal |
| --- | --- | --- | --- |
| CF-V050 | Autorización de salida | **Duplicada de CF-V036** (módulo 03): es la autorización de salida del vehículo en Vigilancia (`B/Wms.Application/Logistics/DepartureAuthorizations/Commands/UpdateDepartureAuthorization/UpdateDepartureAuthorizationHandler.cs`), no la autorización de cargue de Comercio Exterior. UI inalcanzable (BR-03-003) | `C/DepartureAuthorizationController.cs:12-27` |
| CF-V051 | Correcciones de orden de cargue | **Reasignada** a CF-L158, CF-L159.a/.b, CF-L162 y CF-L163 (F3-02, F3-03, F3-04, F3-07 implementan capacidades legacy) | `C/LoadingOrderCorrectionsController.cs:34,72,102` |
| CF-V052 | Guías pendientes | Confirmada (vista nueva; el legacy mostraba «Crear Guía» por fila del listado de salidas) | `F/pages/foreign-trade/dispatch-guides/pending.vue`; `FT/Queries/GetPendingGuides/GetPendingGuidesQuery.cs:24-79` |
| CF-V053 | Salida de la orden con el tiquete de ingreso | **Reasignada** a CF-L166 (F4-08, P16, DF18) | `C/LoadingOrderExitController.cs:30-39` |
| CF-V054 (nueva) | Vista previa y cobro de la guía por cliente dueño | Confirmada (el legacy no cobraba la guía) | `ForeignTradeController.cs:987-995`; `DispatchGuideBillingPlan.cs` |
| CF-V055 (nueva) | Cambiar el modo de pago de la guía | Confirmada (DEC-019; 2eeaaad, no en staging) | `ChangeDispatchGuidePaymentModeCommandHandler.cs` |
| CF-V056 (nueva) | Guía por depósito en ZIP con registro de impresión | Confirmada | `GetDispatchGuidePerDepositZipHandler.cs:68-71` |
| CF-V057 (nueva) | Orden de cargue externa (número, emisor agencia o importador, fecha, soporte) | Confirmada (DEC-016) | `CreateLoadingOrderCommandHandler.cs:267-306,430-476` |
| CF-V058 (nueva) | Salida de importación solo con guía vigente y regularización de salidas sin guía | Confirmada (QA §10, CHG-33) | `ImportGuideRules.cs`; `GetPendingImportLoadingOrdersHandler.cs:32-40` |

## 10. Documentación V2 desactualizada

- `ForeignTradeController.cs:180` documenta «400 si el depósito ya está nacionalizado», mensaje retirado en F2-01; `:1070` dice «Cancela una orden de cargue en estado Pendiente», cuando también se cancela en cargue.
- `CreateExportDispatchGuideCommand.cs:8-10` dice «No genera PDF»: el PDF existe bajo demanda.
