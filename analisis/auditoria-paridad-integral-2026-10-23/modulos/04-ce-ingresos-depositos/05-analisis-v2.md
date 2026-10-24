# 04 — Análisis V2: frontend, backend e integración

> Estático, 2026-10-23. Según `docs/contexto/estado.md`: BE `35a61b2` / FE `c924a8b`. Prefijos: `B/` = `Backend/wms-api/`, `F/` = `Frontend/wms/app/`.
> Políticas (`B/Wms.Domain/Security/WmsPolicyRoles.cs:37`, `:55`): `ForeignTradeAccess` = Admin + ForeignTrade; `DepositEntryDateAccess` = Admin + Scale + ForeignTrade.

## 1. Frontend

### 1.1 Páginas

| Ruta | Archivo | `requiredRoles` | Menú | Qué hace |
| --- | --- | --- | --- | --- |
| `/foreign-trade` | `F/pages/foreign-trade/index.vue` | Admin, ForeignTrade (`:8`) | «Dashboard» (`F/components/layout/AppMenu.vue:313-321`) | Tablero; monta `AbandonmentSummaryAlert` (`:62`). |
| `/foreign-trade/deposits` | `F/pages/foreign-trade/deposits/index.vue` | Admin, ForeignTrade (`:16`) | «Depósitos» | Kanban por estado (Borrador, Confirmado, Anulado, Cerrado), una consulta paginada por columna (`F/features/foreign-trade/utils/kanban-columns.ts:20-28`). |
| `/foreign-trade/imports` | `F/pages/foreign-trade/imports/index.vue` | Admin, ForeignTrade (`:17`) | Atajo Alt+I (`F/composables/useGlobalShortcuts.ts:24`) y tablero | Listado con `DepositFiltersPanel` y filtros de levante y placa (`:206-210`), Excel con `all=true`. |
| `/foreign-trade/imports/[id]` | `F/pages/foreign-trade/imports/[id]/index.vue` | Admin, ForeignTrade (`:60`) | Desde listados | Detalle: confirmar con requisitos (`:143-153`, `:519-524`), anular con motivo y resultado (`:225-257`, `:888-904`), cerrar ingreso de camiones (`:195-204`, `:862-870`), etiqueta (descargar/imprimir, `:160-178`, `:394-412`), consolidado PDF (`:371-392`), plazo aduanero y prórroga (`:334-349`, `:556-583`, `:836-841`), información general con fecha de ingreso y del documento (`:585-602`), terceros (`:607-623`), productos y CE-7 (`:645-656`, `:871-878`), unidades de carga (`:736-742`), entradas por camión con manifiesto y listas de empaque (`:749-760`), levantes (módulo 05). |
| `/foreign-trade/exports`, `/exports/[id]` | `F/pages/foreign-trade/exports/…` | Admin, ForeignTrade | Desde Kanban | Mismas acciones que importación salvo levantes y prórroga (`exports/[id]/index.vue:271`, `:310-318`, `:373-391`). |
| `/foreign-trade/inspections`, `/inspections/[id]` | `F/pages/foreign-trade/inspections/…` | Admin, ForeignTrade | Desde Kanban | Ídem (`inspections/[id]/index.vue:270`, `:309-317`, `:372-388`). |
| `/foreign-trade/packing-lists` | `F/pages/foreign-trade/packing-lists/index.vue` | Admin, ForeignTrade (`:29`) | «Listas de empaque» (`AppMenu.vue:334-338`) | Archivos (filtros importador/proveedor, activos y asociados, `:52-53`, `:215-216`), artículos por importador (`:112`), carga (`PackingListUploadDialog`), eliminar (`:80`). |
| `/foreign-trade/abandonment` | `F/pages/foreign-trade/abandonment/index.vue` | Admin, ForeignTrade (`:26`) | «Abandono y prórrogas» (`AppMenu.vue:328-332`) | Listado con estado (por defecto «En alerta», `:51-55`), prórroga Sí/No, depósito, carta porte, importador, agencia; Excel con `all=true` (`:136`); prórroga desde la fila (`:126`). |

Sin mocks ni datos estáticos (búsqueda `mock|faker|TODO|FIXME` en `F/features/foreign-trade` y `F/pages/foreign-trade`).

### 1.2 Servicios

`F/features/foreign-trade/services/foreign-trade-service.ts` (1128 líneas) y `deposit-service.ts:17` (cliente). El CE-7 está en `F/features/warehouse/services/warehouse-service.ts:601` y la fecha de ingreso en `foreign-trade-service.ts:907-917` (`/warehouse-storages/{id}/entry-date`, sin prefijo `foreign-trade`). Las llamadas del módulo están en el §2; todas tienen endpoint.

## 2. Backend: endpoints del módulo y consumidores

| Endpoint | Controlador:línea | Política | Handler / servicio | Consumidor FE |
| --- | --- | --- | --- | --- |
| `GET foreign-trade/deposits` | `ForeignTradeController.cs:73` | ForeignTradeAccess | `GetDepositsHandler` | `getDeposits` (`foreign-trade-service.ts:150`) |
| `GET foreign-trade/imports` | `:94` | ídem | `GetImportDepositsHandler` (`WhereListed` excluye anulados, filtros comunes, placa y levante, `:27-56`) | `getImportDeposits` (`:166`) |
| `GET foreign-trade/imports/{id}` | `:112` | ídem | `GetImportDepositDetailHandler` | `getImportDepositDetail` (`:295`) |
| `GET foreign-trade/imports/{id}/validation-info` | `:132` | ídem | `GetDepositValidationQuery` | `getDepositValidationInfo` (`:284`) vía `ValidationForm` — **sin camino en la UI** (ver §4) |
| `POST foreign-trade/imports/{id}/validate` | `:153` | ídem | `ValidateDepositCommand` | `validateDeposit` (`:178`) — **sin camino en la UI** |
| `PATCH foreign-trade/imports/{id}/manifest` | `:250` | ídem | `UpdateManifestInfoCommand` (manifiesto DIAN) | `updateManifestInfo` (`:308`) |
| `GET foreign-trade/imports/{id}/label?action=` | `:276-293` | ídem | `LabelGenerationService.GenerateImportLabelAsync` + `RecordPrintAsync` | `generateImportLabel` (`:266`) |
| `GET foreign-trade/imports/{id}/pdf` | `:303` | ídem | `IDepositPdfService` | `downloadImportDepositPdf` (`:274`) |
| `PATCH foreign-trade/warehouse-storages/{id}/customer` | `:328` | ídem | `AssignDepositCustomerCommand` | `deposit-service.ts:17` |
| `GET`/`PUT foreign-trade/warehouse-storages/{id}/stakeholders` | `:351`, `:371` | ídem | `GetDepositStakeholders`, `UpdateDepositStakeholders` (roles IMPORTER, EXPORTER, CUSTOMS_AGENCY, TRANSPORT_COMPANY, `DepositStakeholderRoles.cs:10-22`) | `:803`, `:817` |
| `POST foreign-trade/warehouse-storages/{id}/confirm` | `:399` | ídem | `ConfirmStorageDepositHandler` (requisitos `:52-58`, período y factura `:71-80`) | `:833` |
| `POST foreign-trade/warehouse-storages/{id}/close-truck-entries` | `:413` | ídem | `CloseTruckEntriesCommandHandler` (autor del token `:420-426`) | `:869` |
| `PATCH foreign-trade/warehouse-storages/{id}/draft` | `:440` | ídem | `UpdateDraftDepositCommand` (cliente, intermediario, moneda, valor, observaciones, fecha del documento) | `:895` |
| `PATCH foreign-trade/warehouse-storages/{id}/shipping-form-number` | `:470` | ídem | `UpdateShippingFormNumberCommand` | `:925` |
| `POST foreign-trade/warehouse-storages/{id}/return-for-correction` | `:493` | ídem | `ReturnStorageForCorrectionCommand` | `:774` |
| `POST foreign-trade/warehouse-storages/{id}/cancel` | `:510` | ídem | `CancelWarehouseStorageHandler` → `WarehouseStorageCancellationService` | `:883` |
| `GET foreign-trade/warehouse-storages/{id}/entries` | `:541` | ídem | `GetWarehouseStorageEntriesQuery` | `:665` |
| `GET`/`PATCH foreign-trade/warehouse-storages/{id}/cargo-units[/{cargoUnitId}]` | `:559`, `:572` | ídem | `GetWarehouseStorageCargoUnits`, `CorrectCargoUnitCommand` | `:684`, `:785` |
| `POST`/`PUT`/`DELETE foreign-trade/deposits/{id}/products[/{productId}]` | `:596`, `:625`, `:656` | ídem | `AddDepositProduct`, `UpdateDepositProduct`, `RemoveDepositProduct` (autor del token `:613`, `:644`) | `:701`, `:714`, `:759` |
| `GET foreign-trade/exports`, `exports/{id}`, `exports/{id}/label`, `exports/{id}/pdf` | `:716`, `:686`, `:735`, `:759` | ídem | Export handlers (modalidad exacta `EXP001`, `GetExportDepositsHandler.cs:17`) | `:324`, `:346`, `:358`, `:367` |
| `GET foreign-trade/inspections`, `inspections/{id}`, `/pdf`, `/label` | `:787`, `:805`, `:832`, `:853` | ídem | Inspection handlers (`StartsWith("INSP")`) | `:382`, `:392`, `:402`, `:411` |
| `PATCH foreign-trade/warehouse-storages/{id}/entries/{entryId}/manifest` | `DepositCompletionController.cs:36` | ForeignTradeAccess | `UpdateTruckManifestCommand` | `:860` |
| `GET foreign-trade/warehouse-storages/{id}/confirmation-requirements` | `DepositCompletionController.cs:58` | ídem | `GetConfirmationRequirementsQuery` | `:845` |
| `PUT foreign-trade/deposits/{id}/products/{storageProductId}/catalog-product` | `DepositCompletionController.cs:78` | ídem | `ChangeDepositLineProductCommand` | `:731` |
| `PUT foreign-trade/warehouse-storages/{id}/entries/{entryId}/cargo-unit-breakdown` | `DepositCompletionController.cs:104` | ídem | `SetCargoUnitBreakdownCommand` | `:747` |
| `PATCH warehouse-storages/{id}/entry-date` | `DepositEntryDateController.cs:28` | DepositEntryDateAccess | `CorrectDepositEntryDateCommandHandler` | `:914` (CE: `DepositDetailGeneralInfoCard.vue:183`; báscula: `F/pages/operations/weighbridge/cycles/[id].vue:606`) |
| `POST warehouse/inventory/adjustments` | `InventoryAdjustmentController.cs:34` | ForeignTradeAccess | `AdjustInventoryCommandHandler` | `F/features/warehouse/services/warehouse-service.ts:601` (diálogo en los tres detalles de CE) |
| `GET foreign-trade/warehouse-storages/{id}/label-prints` | `LabelPrintsController.cs:20` | ForeignTradeAccess | `GetLabelPrintsHandler` (conteos y últimas 50) | `getDepositLabelPrints` (`:415-417`) → `LabelPrintsBadge.vue:16` |
| `GET`/`POST foreign-trade/packing-list-suppliers` | `PackingListsController.cs:34`, `:46` | ForeignTradeAccess | `GetSuppliers`, `CreateSupplier` (único normalizado) | `:958`, `:964` |
| `POST foreign-trade/packing-lists/import` (multipart, ≤ 5 MB, `dryRun` por defecto true) | `:65` | ídem | `ImportPackingListCommandHandler` | `:984` (`postForm`) |
| `GET foreign-trade/packing-lists`, `/{id}`, `DELETE /{id}` | `:101`, `:111`, `:124` | ídem | `GetPackingLists`, `GetPackingListById`, `DeletePackingList` | `:990`, `:995`, `:1000` |
| `GET foreign-trade/packing-list-items` | `:134` | ídem | `GetPackingListItems` (importador obligatorio) | `:1006` |
| `POST foreign-trade/deposits/{id}/entries/{entryId}/packing-list-items` | `:154` | ídem | `AssociatePackingListItemsCommandHandler` | `:1018` |
| `POST foreign-trade/imports/{id}/extension` | `AbandonmentController.cs:33` | ForeignTradeAccess | `RegisterStorageExtensionCommandHandler` | `:223` |
| `GET foreign-trade/abandonment`, `/summary` | `AbandonmentController.cs:53`, `:63` | ídem | `GetAbandonmentListHandler`, `GetAbandonmentSummaryHandler` (`AbandonmentReader`) | `:236`, `:244` |

Fuera del módulo (se citan solo como dependencia): levantes, órdenes, guías y `validate-client` (módulo 05); `reports/abandonment-*` (módulo 07, consumidos por `F/features/reports/services/reports-service.ts:171`, `:180`).

## 3. Lógica y persistencia relevantes

- **Estados del depósito** (`B/Wms.Domain/Enums/WarehouseStorageStatus.cs`): `Draft` (nace en báscula) → `Confirmed` (`WarehouseStorage.Confirm`, `:289-299`) → `Closed` (automático al agotar el stock en el cargue, `ExecuteLoadingOrderCommandHandler.cs:275-281`; reabre solo por reversión de salida, `WarehouseStorage.cs:363-371`). `Confirmed` → `Draft` por devolución a corrección, bloqueada con órdenes activas (`:306-332`). `Draft`/`Confirmed` → `Cancelled` (`EnsureCancellable`/`Cancel`, `:384-405`). Los listados excluyen `Cancelled` (`DepositSearchQueryExtensions.cs` `Listed`); el Kanban los muestra en su columna.
- **Anulación** (`WarehouseStorageCancellationService.cs:59-195`): guardas 409 (salidas `Loaded`/`Dispatched`/`Complete`, camión en báscula); órdenes activas: cancela las que solo llevan el depósito y retira ítems de las mixtas con sus reservas (`DepositCancellationPlan`); stock a cero con `InventoryMovement` `StorageCancellation`; libera ubicaciones; cierra períodos abiertos y aplica `InvoiceCancellationPolicy` a sus facturas; `ServiceRecord.VoidService`; avisos post-commit a Bodega y Facturación (`:215-271`). Motivo 10–500 (`CancelWarehouseStorageCommandValidator.cs:14`). Todo en una transacción (`CancelWarehouseStorageHandler`).
- **Confirmación** (`DepositConfirmationRequirements.cs:64-124`): lista unificada de faltantes, la misma que expone `confirmation-requirements`; al confirmar abre período y factura desde la fecha de ingreso (`ConfirmStorageDepositHandler.cs:71-80`).
- **Fecha de ingreso** (`WarehouseStorage.cs:194-232`, `CorrectDepositEntryDateCommandHandler.cs:29-53`): Borrador/Confirmado, dentro de la estadía del primer camión, no futura; borra la TRM DIAN si cambia el día y avisa a Facturación.
- **Etiqueta** (`LabelGenerationService.cs`): A5 con logo, n.º de depósito con Code128, importador, intermediario (agencia), transportadoras, fecha de ingreso, Ampara/Saldo/Unidad/Embalaje/Mercancía, carta porte, manifiesto DIAN, placas y unidades de carga, banner NACIONALIZADA/SIN NACIONALIZAR (`:85-87`), datos de nacionalización; prohibida en anulados (`:663-664`); registra la acción (`:667-679`; `LabelPrintActions.Parse`, `Print`/`Download`).
- **Abandono** (`AbandonmentCalculator.cs`, `AbandonmentReader.cs`): plazo 30/60, alerta en los últimos 10 días, universo IMP Borrador/Confirmado con recibido − levantes > 0, días desde `EntryDate`. Job `AbandonmentAlertBackgroundService` (registrado en `B/Wms.Api/Program.cs:81`) llama a `AbandonmentAlertService.SendDailyAlertAsync` a las 07:00 (Colombia), con idempotencia diaria por `RelatedEntityType = "AbandonmentReport"` (`:53-56`).
- **Listas de empaque**: parser puro (`PackingListCsvParser.cs:42-88`: separador `;` o `,`, coma decimal con `;`, filas de encabezado, errores por fila sin detener), importación con simulación y transacción (`ImportPackingListCommandHandler.cs:38-96`), eliminación solo sin asociados (`DeletePackingListCommand.cs:26-30`), asociación con las reglas de `AddDepositProduct` y asignación del importador (`AssociatePackingListItemsCommandHandler.cs:24-101`).
- **CE-7** (`AdjustInventoryCommandHandler.cs:47-193`): Borrador/Confirmado; por unidad de carga si aplica; no por debajo de los levantes (`:112`); movimiento de kárdex (`:138`); correo al parámetro `INVENTORY_ADJUSTMENT_ADMIN_EMAIL` sin bloquear (`:164`); recálculo del período (`:193`).
- Reglas extraídas a clases puras con pruebas en `B/Wms.Tests/ForeignTrade/` (`AbandonmentCalculatorTests`, `PackingListCsvParserTests`, `DepositConfirmationRequirementsTests`, `DepositCancellationPlanTests`, `CargoUnitBreakdownTests`, `LabelPrintActionTests`) y `B/Wms.Tests/Domain/` (`WarehouseStorageCancelTests`, `ImportWarehouseStorageExtensionTests`, `PackingListItemTests`). No se ejecutaron.

## 4. Endpoints sin consumidor y llamadas sin endpoint

| Hallazgo | Evidencia | Valoración |
| --- | --- | --- |
| `POST imports/{id}/validate` y `GET imports/{id}/validation-info` tienen servicio y composable, pero ningún control abre el diálogo: `showValidationDialog` solo se declara y se cierra (`F/pages/foreign-trade/imports/index.vue:73`, `:107`; `imports/[id]/index.vue:259`, `:365`, `:810-812`). | Búsqueda de `showValidationDialog.value = true` y de un botón «Validar»: sin resultados. QA validó el flujo por API (`docs/qa/resultados/defectos/DEF-F5-008.md`). | BR-04-007 (SOLO_V2, CF-V047). |
| `getExportDepositById` (`foreign-trade-service.ts:333-338`, `@deprecated`) sin uso; `GetExportDepositById` (`B/Wms.Application/ForeignTrade/Queries/GetExportDepositById/`) sin acción en el controlador. | Conteo de usos = 0. | Código muerto, sin impacto funcional. |
| Ninguna llamada del frontend del módulo apunta a una ruta inexistente. | Contraste del §2. | — |

## 5. Contratos (DTO ↔ TypeScript)

| Operación | Resultado | Evidencia |
| --- | --- | --- |
| Detalle de importación | El backend coincide campo a campo con la interfaz salvo **9 campos que solo existen en TS**: `releaseNumber`, `releaseDate`, `acceptanceNumber`, `acceptanceDate`, `currentStock` (obligatorio), `receivedQuantity` (obligatorio), `unitMeasure` (obligatorio), `productName`, `productDescription`. `depositDetail.unitMeasure` se pasa a `ValidationForm` y llega `undefined`. | `B/Wms.Application/ForeignTrade/Common/DTOs/ImportDepositDetailDto.cs` frente a `F/features/foreign-trade/types/import-deposit.ts` (interfaz `IImportDepositDetailDto`, líneas 1-40); `imports/[id]/index.vue:811`. BR-04-008. |
| Abandono (lista, resumen, prórroga) | Coinciden; `status` como texto (`EnPlazo`/`EnAlerta`/`EnAbandono`); `ImporterId`/`CustomsAgencyId` con `JsonIgnore`. | `AbandonmentItemDto.cs`; `F/features/foreign-trade/types/abandonment.ts`; `RegisterStorageExtensionCommand.cs` ↔ `import-deposit.ts:300-311`. |
| Listas de empaque | Coinciden (archivo, detalle, artículo, resultado de importación con `errors[{row,message}]`, asociación). | `PackingListDtos.cs` ↔ `F/features/foreign-trade/types/packing-list.ts`. |
| Anulación | Coincide; TS omite `total` en `cancelledInvoices` (no lo usa). | `CancelWarehouseStorageCommand.cs:14-21`, `InvoiceCancellationDtos.cs:7-10` ↔ `deposit-kanban.ts:152-160`. |
| Impresiones de etiqueta | Coincide; `action` como texto `Print`/`Download`. | `GetLabelPrintsQuery.cs:12-20` ↔ `types/label-prints.ts`. |
| Requisitos, cierre de camiones, fecha de ingreso, manifiesto por camión | Coinciden. | `ConfirmationRequirementsDto.cs`, `CloseTruckEntriesCommand.cs:12`, `CorrectDepositEntryDateCommand.cs:13` ↔ `deposit-kanban.ts:36-138`. |
| Paginación | Abandono, listas de empaque y listados usan `QueryParametersBase` con `all=true` en los Excel (`abandonment/index.vue:136`). | — |

## 6. Capacidades SOLO_V2 del módulo

| ID | Capacidad | Frontend | Backend | Integración | Nota |
| --- | --- | --- | --- | --- | --- |
| CF-V040 | Unidades de carga del depósito (consulta, corrección de tipo/placa, reparto por camión, exigencia al confirmar) | `DepositDetailCargoUnitsSection`, `CargoUnitBreakdownDialog` | `ForeignTradeController.cs:559-585`; `DepositCompletionController.cs:104`; `DepositConfirmationRequirements.cs:108-124` | CONECTADO_CODIGO | DEC-014, P5. El legacy tenía el catálogo (CF-L077–080, módulo 01) pero no la unidad en el depósito. |
| CF-V041 | Inspecciones (INSP) | `pages/foreign-trade/inspections/…` | `ForeignTradeController.cs:787-870`; serie `INSP` (`DocumentNumberFormat.cs:34`) | CONECTADO_CODIGO | El legacy solo tenía el prefijo genérico `OT` (`registrardeposito.php:292-296`). |
| CF-V042 | Cierre explícito del ingreso de camiones | Diálogo en los tres detalles | `:413`; `ServiceRecord.cs:330-342`; `StorageDocumentLookup.cs:73-118` | CONECTADO_CODIGO | DEC-013. |
| CF-V043 | Fecha de ingreso editable | `EditDepositEntryDateDialog.vue:53-60`, `:105-126` | `DepositEntryDateController.cs:28` | CONECTADO_CODIGO | Límite inferior distinto de DEC-012 (BR-04-002). |
| CF-V044 | Ajuste de cantidad CE-7 con kárdex | `AdjustInventoryDialog` en los detalles | `InventoryAdjustmentController.cs:34` | CONECTADO_CODIGO | DEC-019. |
| CF-V045 | Exportaciones (EXP) como operación propia | `pages/foreign-trade/exports/…` | Export handlers | CONECTADO_CODIGO | **Reasignada:** el legacy ya tenía depósitos de exportación (CF-L134/CF-L135). Lo propio de V2 (guía EXP automática) es del módulo 05. |
| CF-V046 | Confirmación del depósito con requisitos y devolución a corrección | `DepositConfirmationRequirements.vue`, botón Confirmar, `DepositProductsTable` (devolver) | `:399`, `:493`; `DepositCompletionController.cs:58` | CONECTADO_CODIGO | P2, P5. El legacy no tenía estado de confirmación. |
| CF-V047 | Validación del depósito contra la plantilla (peso y cantidad) | `ValidationForm.vue` sin disparador | `:132`, `:153` | SIN_INTEGRACION | BR-04-007. |
| CF-V048 | Manifiesto por camión y cambio de producto de la línea | `TruckManifestDialog.vue`, `ChangeLineProductDialog.vue` | `DepositCompletionController.cs:36`, `:78` | CONECTADO_CODIGO | F1-04, F1-07 (P3). El manifiesto del legacy era por ingreso. |
| CF-V084 | Alerta diaria de abandono (job) | Notificación al rol CE | `AbandonmentAlertBackgroundService`, `AbandonmentAlertService` | CONECTADO_CODIGO | Equivale y amplía CF-LX04-01. QA: F5-ABA-006 bloqueado (`docs/qa/resultados/F5-informe-2026-10-02.md:166`); el riesgo R-ADM-01 se corrigió con DEF-F3-001 (Verificado). |
