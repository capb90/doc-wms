# 02-bascula — 05 Análisis V2

> AG-02 · 2026-10-23 · Estático (código en disco; según `docs/contexto/estado.md`: BE `35a61b2` / FE `c924a8b`). Backend relativo a `Backend/wms-api/`, frontend a `Frontend/wms/app/`.

## 1. Frontend

| Página | `requiredRoles` | Menú | Qué hace | Evidencia |
| --- | --- | --- | --- | --- |
| `pages/operations/weighbridge/index.vue` (2 178 líneas) | Admin, Scale | Báscula › Proceso de Pesaje | Banco de trabajo: cola, ficha por camión con pasos en línea Registro → Cobro → Peso → Tiquete (DF5), borradores por camión, F2 peso en ventana, Enter por paso, Esc, operación preseleccionada por motivo (DF8), depósito adicional, otras órdenes del pesaje, recuperar | `:105` (roles); `:1024-1146` (cobro, DF9 `:1045-1048`); `:1157-…` (peso); `:1374-1403` (teclado); `:1491` (Recuperar); `:1756,1916` (otras órdenes) |
| `pages/operations/weighbridge/history.vue` | Admin, Scale | Báscula › Historial | Pestañas Entradas/Salidas, filtros, totales, Excel con `all=true`, detalle del ciclo, corrección de pesos y fechas, reimpresión con/sin observaciones, anular | `:44`; `:84-117`; `:146-154`; `:600-640`; `:710-725`; `:807` |
| `pages/operations/weighbridge/cycles/[id].vue` | Admin, Scale, Billing, ForeignTrade | (enlace) | Detalle del ciclo, línea de tiempo, tiquetes por depósito, corregir pesos (Admin/Scale/Billing), fecha de ingreso (Admin/Scale/CE), anular (Admin/Scale), «Cerrar ciclo» | `:49`; `:62-67`; `:100`; `:194-252`; `:348-368` |
| `pages/operations/weighbridge/recover.vue` | Admin, Scale | (botón en el banco) | Operaciones a medias: Retomar (`?resume=`) o Descartar | `:24`; `:100`; `:121`; `:213` |
| `pages/operations/weighbridge/dashboard.vue` | Admin, Scale | Báscula › Dashboard | Tarjetas (refresco 30 s) y accesos rápidos | `:7`; `:38`; `:98-122`; `features/weighbridge/composables/useWeighbridgeDashboard.ts:13` |
| `pages/operations/weighbridge/reports.vue` | Admin, Scale | Báscula › Reportes | Reporte diario de facturación de báscula y PDF | `:9`; `:30`; `:44` |
| `pages/operations/weighbridge/pending-reweigh.vue`, `in-process.vue` | Admin, Scale | — | Redirecciones a `?cola=por-repesar` / `?cola=por-pesar` | archivos completos (16 líneas c/u) |
| Menú | — | `components/layout/AppMenu.vue:214-239` (roles Admin, Scale) | Dashboard, Proceso de Pesaje, Historial, Reportes | — |
| Atajos globales | Admin, Scale | — | Alt+N → banco; Alt+K → `?cola=por-repesar` | `composables/useGlobalShortcuts.ts:22-23,48` |

Componentes principales: `features/weighbridge/components/StorageServiceForm.vue` (sección Documento, panel plegado DF11 `:1102`, búsqueda al salir del campo DF7 `:518`, moneda solo con valor DF10 `:823-824`, tipo de carga DF15 `:1057`, unidades `:1095`, panel de camiones previos `:1014`, documentos de envío `:1291`), `TruckGoodsLines.vue` (líneas en línea, descripción libre, unidad obligatoria DF16 `:63`), `CargoUnitsEditor.vue` (mercancía por unidad solo cuando el backend la exige `:43-46,133,198`), `WeightCapture.vue` (tipo permitido, fecha propuesta, neto en vista previa `:334,460`), `features/billing/components/BillingCollectForm.vue` (destinatario, modo Inmediato / Por facturar, sin efectivo), `TruckQueue.vue` + `useWeighbridgeQueue.ts:11-13` (refresco 15 s), `AdditionalOrdersDialog.vue`, `EntryTicketExitPanel.vue` (dentro de `OutputServiceForm.vue:30,382`), `DocumentMatchBanner.vue`, `PreviousEntriesPanel.vue`, `QuickCreateStakeholderDialog.vue`, `CompleteEntryInfo.vue`, `ServiceRecordDocumentsManager.vue`.

**Mocks o datos estáticos:** ninguno (búsqueda `mock`, `faker`, `hardcod`, «datos de ejemplo», `TODO` en `features/weighbridge` y `pages/operations/weighbridge`).

**Llamadas del frontend sin endpoint:** ninguna. Las 51 funciones de `features/weighbridge/services/weighbridge-service.ts` apuntan a rutas existentes (contraste en §2).

## 2. Backend — endpoints del módulo (51 acciones)

Política de clase salvo indicación. «Consumidor» = archivo del frontend que llama (búsqueda por nombre de función y por ruta en `Frontend/wms/app`).

| Verbo y ruta (`/api/v1/weighbridge/…`) | Controlador | Política | Consumidor |
| --- | --- | --- | --- |
| POST `weighing-only/initiate` · `weighing-only/process-payment` · `weighing-only/start-pending-billing` | `WeighbridgeController.cs:84,122,154` | ScaleAccess | `index.vue` vía `useWeighingOnly`, `useProcessPayment`, `useStartWeighingPendingBilling` |
| POST `storage/initiate` (depósito adicional) · `storage/register` · `storage/process-payment` · `storage/start-pending-billing` | `:190,245,306,338` | ScaleAccess | `index.vue` (`useInitiateStorageWeighing`, `useRegisterStorageEntry`, …) |
| POST `output/initiate` · `output/process-payment` · `output/start-pending-billing` | `:374,413,445` | ScaleAccess | `index.vue` |
| POST `cycles/{cycleId}/weighings` | `:485` | ScaleAccess | `useRecordWeighing` (desde `useStorageWeighing`, `useWeighingOnly`, `index.vue`) |
| GET `pending` | `:518` | ScaleAccess | **sin consumidor** (`useWeighbridgePending.ts` sin uso) |
| GET `queue` · `dashboard` | `:535,548` | ScaleAccess | `useWeighbridgeQueue`, `useWeighbridgeDashboard` |
| GET `pending-second-weight` | `:563` | ScaleAccess | **sin consumidor** (`usePendingSecondWeight.ts` sin uso) |
| GET `cycles/open-by-plate` · `cycles/open` | `:583,601` | ScaleAccess | **sin consumidor** (`useOpenCycleByPlate.ts`, `useOpenCycles.ts` sin uso) |
| GET `recoverable` · DELETE `incomplete/{serviceRecordId}` | `:619,637` | ScaleAccess | `recover.vue`, `index.vue` |
| POST `cycles/{cycleId}/complete` | `:661` | ScaleAccess | `cycles/[id].vue` («Cerrar ciclo») |
| GET `{id}/invoice` | `:690` | ScaleAccess | **sin consumidor** (`getInvoiceByWeighbridgeCycle` sin uso) |
| GET `history` · `history/totals` | `:708,723` | ScaleAccess | `history.vue`, `EntryTicketExitPanel.vue` |
| GET `service-records/{id}/registration` · `service-records/by-document` · `warehouse-storage/by-document` | `:741,760,782` | ScaleAccess | `index.vue` |
| GET `loading-orders/by-plate/{plate}` · `loading-orders/{number}` | `:808,825` | ScaleAccess | `index.vue`, `AdditionalOrdersDialog.vue` |
| GET `entry-logs/{id}` | `:844` | ScaleAccess | `index.vue` |
| PATCH `{id}/weighing-date` · `{id}/ticket-observations` | `:885,916` | ScaleAccess | `ModifyWeighingDateDialog.vue`; `history.vue`, `index.vue` |
| GET `reports/daily-billing` · `reports/daily-billing/pdf` | `:951,968` | ScaleAccess | `reports.vue` |
| POST `stakeholders/quick` | `:996` | ScaleAccess | `features/stakeholders/composables/useQuickCreateStakeholder.ts:28` |
| GET `vehicle-types` · `vehicles/by-plate/{plate}` · `drivers/by-document` · `shipping-document-types` | `WeighbridgeCatalogController.cs:34,49,62,92` | ActiveUser | Vigilancia (`features/entries/*`), `CompleteEntryInfo.vue`, `useServiceRecordDocuments.ts` |
| GET `lookup` | `WeighbridgeCatalogController.cs:77-89` | ActiveUser | **sin consumidor a propósito** (plan frontend §A.3) |
| PATCH `{id}/first-weight-modify` · `{id}/second-weight` | `WeighbridgeCorrectionController.cs:23-24,36,62` | WeighingCorrectionAccess (Admin, Scale, Billing) | `ModifyWeighingDialog.vue` |
| GET `{id}` y `cycles/{id}` · `{id}/ticket/pdf` · `entries/{entryId}/ticket/pdf` | `WeighbridgeCycleReadController.cs:22-23,36-41,57,80` | ActiveUser | `index.vue`, `history.vue`, `useCycleDetail` (`cycles/[id].vue`), `useTicketPdf` |
| POST `output/cycles/{cycleId}/additional-orders` · `output/from-entry-ticket` | `WeighbridgeOutputSharingController.cs:17-18,31,49` | ScaleAccess | `useAddAdditionalOrders` → `AdditionalOrdersDialog.vue`; `useExitWithEntryTicket` → `EntryTicketExitPanel.vue` |
| PATCH `entry-log/{id}/info` · POST `service-records/{id}/documents` · DELETE `service-records/documents/{documentId}` · POST `transport-companies/quick` | `WeighbridgeSharedController.cs:25-26,35,66,91,107` | OperationalAccess | `CompleteEntryInfo.vue`, `pages/operations/entries/index.vue`, `useServiceRecordDocuments.ts`, `VehicleForm.vue` |
| POST `cycles/{cycleId}/void` | `WeighbridgeVoidController.cs:17-18,33` | ScaleAccess | `useVoidWeighing` (`history.vue`, `index.vue`, `cycles/[id].vue`) |

Endpoints de otros módulos que cierran flujos de báscula: `PATCH billing/invoices/{id}/number` (`BillingController.cs:178`, BillingAccess) — N.º SIIGO; `POST billing/invoices/{id}/payments` (`:278`) — cobro de lo «por facturar»; `POST foreign-trade/loading-orders/{id}/exit-with-entry-ticket` (`LoadingOrderExitController.cs`, ForeignTradeAccess) — salida con tiquete desde CE (`features/foreign-trade/components/ExitWithEntryTicketDialog.vue`, montado en `pages/foreign-trade/{imports,exports,inspections}/[id]/index.vue`).

**Código del backend sin endpoint:** `Commands/Storage/GenerateGlobalGuide/GenerateGlobalDispatchGuideHandler.cs` solo se invoca desde `RecordWeighingHandler.cs:300-318` (cierre del perecedero) y tiene el `TODO` de la guía (`:71`).

## 3. Integración y contratos (campo por campo)

| Operación | Petición (DTO ↔ TS) | Respuesta (DTO ↔ TS) | Resultado |
| --- | --- | --- | --- |
| Registro con depósito `POST storage/register` | `Wms.Application/Weighbridge/Common/Dtos/Requests/RegisterStorageEntryRequest.cs` (40 campos: conductor por documento, vehículo, documento, terceros con rol, documentos, manifiesto, transportadora, moneda/valor, productos, pesaje, `EntryDate`, `CargoHandling`, `CargoUnits`, exportador) ↔ `features/weighbridge/types/requests.ts` (`IRegisterStorageEntryRequest` + `IEntryInfoFields` + `IInitiateStorageWeighingRequest`) | `InitiateStorageResponseDto.cs` ↔ `IInitiateStorageResponse` (`types/weighbridge-cycle.ts`) | Coinciden todos los campos de la petición. La respuesta TS no declara `documentDate`, `isAdditionalDeposit`, `weighbridgeCycleId`, `newWarehouseStorageEntryId` (no se leen por tipo; sin efecto) |
| Cobro `POST {storage\|weighing-only\|output}/process-payment` y `…/start-pending-billing` | `ProcessStoragePaymentRequest.cs` / `StartStoragePendingBillingRequest.cs` (`ServiceRecordId`, `EntryLogId`, `PaymentMethod`, `AmountReceived`, `ReferenceNumber`, `Notes`, `UnregisteredRecipient`, `InvoiceNumber`, `RecipientMode`, `CustomerId`) ↔ `IProcessStoragePaymentRequest` / `IStartPendingBillingRequest` (`requests.ts:245-257,386-398`); envío en `index.vue:1074-1087` | `ProcessPaymentResponseDto.cs` ↔ `IProcessPaymentResponse` (`weighbridge-cycle.ts:351-362`) | Coinciden. `InvoiceNumber` existe en el API y el frontend no lo envía (correcto: lo asigna Facturación, DEC-024). `invoiceNumber` de la respuesta puede ser nulo y el TS lo tipa `string` (BR-02-008). Sin `cashReceived`/`changeAmount` en ambos lados (§10; `PaymentContractsTests.cs`) |
| Pesaje `POST cycles/{id}/weighings` | `RecordWeighingRequest.cs` (`Weight`, `WeightType`, `Observations`, `CapturedAt`) ↔ `IRecordWeighingRequest` (`requests.ts:295-301`) | `RecordWeighingResponseDto.cs` ↔ `IRecordWeighingResponse` (`types/responses.ts:6-13`) | Coinciden |
| Historial `GET history` | `GetWeighbridgeHistoryQuery.cs` (15 filtros) ↔ `IGetWeighbridgeHistoryQuery` (`requests.ts:325-347`) | `WeighbridgeHistoryDto.cs` ↔ `IWeighbridgeHistory` (`weighbridge-cycle.ts:181-218`) | El TS envía `weighbridgeCycleId` (filtro «ID Ciclo», `WeighbridgeHistoryTable.vue:248-253`) y el backend **no lo tiene** (`GetWeighbridgeHistoryQuery.cs`, `WeighbridgeHistoryFilters.cs:9-25`): se ignora. El TS declara `netWeight` y `mode`, que el DTO no trae (la UI usa `netWeightKg ?? netWeight`) → BR-02-008. El DTO trae `hasAdditionalDeposits` y `ticketNumbers`, que el TS no declara |
| Anular `POST cycles/{id}/void` | `VoidWeighingRequest(string Reason)` (`Controllers/v1/Requests/WeighbridgeVoidRequests.cs:4`) ↔ `{ reason }` (`weighbridge-service.ts:713-716`) | `VoidWeighingResultDto` (`VoidWeighingCommand.cs`) ↔ `IVoidWeighingResultDto` (`weighbridge-cycle.ts:258-268`) | Coinciden. El autor sale del token (`WeighbridgeVoidController.cs:40-43`) |
| Otras órdenes / salida con tiquete | `AddAdditionalOrdersRequest(List<Guid>?)`, `ExitFromEntryTicketRequest(Guid, Guid)` (`Controllers/v1/Requests/WeighbridgeOutputSharingRequests.cs`) ↔ `weighbridge-service.ts:725-742` | `AdditionalOrderResultDto`, `ExitWithEntryTicketResultDto` ↔ `IAdditionalOrderResult`, `IExitWithEntryTicketResult` (`weighbridge-cycle.ts:234-255`) | Coinciden, incluido `awaitingGuide` |
| Documento `GET service-records/by-document`, `warehouse-storage/by-document` | query `cargoManifestNumber`, `primaryDocumentTypeId`, `documentDate` | `data` o `null`; 409 ambiguo (`StorageDocumentLookup.cs:59-60`) | Coinciden (C-F1-03) |
| Enums | `WeighbridgeCyclesStatus`, `ServiceRecordsType`, `InvoiceStatus` se serializan por nombre y el TS los tipa como uniones de cadenas | — | Coinciden |

Paginación: los listados de báscula usan `QueryParametersBase`; el Excel del historial pide `all: true` (`history.vue:109,115`).

## 4. Seguridad y permisos

- Escrituras de báscula: `ScaleAccess` (Admin, Scale). Correcciones de peso: `WeighingCorrectionAccess` (Admin, Scale, Billing); la fecha del pesaje queda en `ScaleAccess`. UI alineada por código de rol (`utils/weighing-permissions.ts`, CHG-47).
- `WeighbridgeCycleReadController` es `ActiveUser`: cualquier usuario autenticado lee el ciclo y descarga el tiquete, y esa descarga marca la primera impresión (`WeighbridgeTicketPdfService.cs:92,136,144-149`) → parte de BR-02-009.
- Las correcciones (`ModifyFirstWeightHandler.cs`, `ModifySecondWeightHandler.cs:51-63`, `ModifyWeighingDateHandler.cs`, `UpdateTicketObservationsHandler.cs`) no validan que el ciclo esté anulado (`Canceled`); solo la UI las oculta (`history.vue:607,627`) → BR-02-007.

## 5. Endpoints sin consumidor

| Endpoint | ¿A propósito? | Conclusión |
| --- | --- | --- |
| GET `lookup` | Sí: plan frontend §A.3 («No se conecta, porque precargaría cliente y tarifa») | Cumple la decisión; el DTO no trae tarifa (`WeighbridgeLookupDto.cs:7-49`) |
| GET `pending`, `pending-second-weight`, `cycles/open`, `cycles/open-by-plate`, `{id}/invoice` | Sin decisión encontrada; sus composables quedaron sin uso tras WMS-31 (cola única) | BR-02-018 (BAJA): retirarlos o documentar su uso por API |
| `useInitiateAdditionalDeposit.ts` | — | Composable sin uso (el depósito adicional usa `useInitiateStorageWeighing`) — BR-02-018 |

## 6. Capacidades `SOLO_V2` (confirmadas)

| ID | Capacidad | Frontend | Backend | Integración | Nota |
| --- | --- | --- | --- | --- | --- |
| CF-V020 | Cola de camiones con estado y filtro `?cola=` | COMPLETO_CODIGO (`TruckQueue.vue`, `useWeighbridgeQueue.ts:11-13`) | COMPLETO_CODIGO (`GET queue`, `Queries/GetWeighbridgeQueue/`) | CONECTADO_CODIGO | F3-COL-001…005 PASA (`docs/qa/resultados/F3-informe-2026-10-02.md` §4) |
| CF-V021 | Recuperar operaciones a medias | COMPLETO_CODIGO (`recover.vue`) | COMPLETO_CODIGO (`GET recoverable`, `DELETE incomplete/{id}`, `DiscardIncompleteOperationHandler.cs`) | CONECTADO_CODIGO | DEF-F3-004 Verificado |
| CF-V022 | Pendientes de repesar / en proceso | COMPLETO_CODIGO (redirecciones a la cola) | NO_APLICA (usa `GET queue`; `GET pending-second-weight` quedó sin uso) | CONECTADO_CODIGO | Absorbida por la cola (WMS-31 D11) |
| CF-V023 | Tablero de báscula | COMPLETO_CODIGO (`dashboard.vue`) | COMPLETO_CODIGO (`GET dashboard`, `WeighbridgeDashboardCounts.cs`) | CONECTADO_CODIGO | DEF-F3-015 Verificado |
| CF-V024 | Corrección de pesajes del ciclo | COMPLETO_CODIGO (`ModifyWeighingDialog.vue`) | PARCIAL (sin guarda de anulado; multidepósito) | CONECTADO_CODIGO | **Reasignada en parte** a CF-L104/L108/L112 (el legacy modificaba pesos); lo propio de V2 es el motivo obligatorio, la conservación del peso original y el aviso a Admin (`ModifySecondWeightHandler.cs:86-100`). BR-02-006, BR-02-007 |
| CF-V025 | Flujo perecedero y depósito adicional | PARCIAL | PARCIAL | CONECTADO_CODIGO | **Depósito adicional reasignado a CF-L103.c** (equivale a «Vehículo con varios Doc.»). Perecedero = SOLO_V2: cierra en un pesaje vía `GenerateGlobalDispatchGuideCommand` sin guía persistida (`GenerateGlobalDispatchGuideHandler.cs:71`); el aviso de `WeightCapture.vue:386-390` promete una «guía de despacho global» que no existe; la notificación sale con título técnico «PerishableFlowClosed» (`:100-108`). F3-REG-019 y F3-PES-013/014 no ejecutados |
| CF-V026 | Reporte diario de facturación de báscula (pantalla y PDF) | COMPLETO_CODIGO (`reports.vue`) | COMPLETO_CODIGO (`GET reports/daily-billing[/pdf]`, `DailyBillingReportBuilder.cs`, `DailyBillingPdfService.cs`) | CONECTADO_CODIGO | F3-RPT-001 PASA; DEF-F11-018 y DEF-F8-009 Verificados |
| CF-V027 | Documentos de envío del servicio (tipo, número, fecha) | COMPLETO_CODIGO (`ServiceRecordDocumentsManager.vue`, `StorageServiceForm.vue:1291`) | COMPLETO_CODIGO (`POST/DELETE service-records/.../documents`, `GET shipping-document-types`) | CONECTADO_CODIGO | Pariente lejano de `docmercial_x_modalidad` del legacy; no son los «soportes documentales» retirados (§A.3), que eran archivos. F3-REG-023 no ejecutado |
| CF-V028 | Alta rápida de tercero y transportadora desde báscula | COMPLETO_CODIGO (`QuickCreateStakeholderDialog.vue`, `VehicleForm.vue`) | COMPLETO_CODIGO (`POST stakeholders/quick`, `POST transport-companies/quick`) | CONECTADO_CODIGO | §A.5 plan frontend. F3-CAM-009 y F3-REG-016 no ejecutados |
| CF-V029 | Observación del tiquete y reimpresión con o sin ella | COMPLETO_CODIGO (`history.vue:867`, `index.vue`) | COMPLETO_CODIGO (`PATCH {id}/ticket-observations`; PDF `WeighbridgeTicketPdfService.cs:405-410`) | CONECTADO_CODIGO | F3-TIQ-003 no ejecutado |

## 7. Lo que la V2 hace distinto y está decidido (resumen)

Peso digitado (sin captura), sin precarga de cliente/tarifa por placa, sin efectivo ni cambio, N.º SIIGO por Facturación, cartera por Facturación, consecutivo `2026T00001`, repesaje de salida bloqueado hasta el cargue, llegada a Bodega antes del segundo pesaje, validación de mora, salida con tiquete camión por camión, datos de CE opcionales en báscula, producto libre que crea catálogo, unidades de carga sin desglose. Fuentes en `03-reglas-negocio.md`.
