# 04 — Integraciones: trazas frontend → backend, procesos automáticos y servicios externos

> Estático, 2026-10-23. Prefijos: `B/` = `Backend/wms-api/`, `F/` = `Frontend/wms/app/`, `S` = `F/features/foreign-trade/services/foreign-trade-service.ts`. El prefijo HTTP es `/api/v1` (cliente `api` del proyecto). Ninguna traza se ejecutó.

## 1. Confirmar el depósito

1. `F/pages/foreign-trade/imports/[id]/index.vue:143-153`: `useConfirmationRequirements(warehouseStorageId, isDraft)` → `S:841-847` `GET /foreign-trade/warehouse-storages/{id}/confirmation-requirements` → `B/Wms.Api/Controllers/v1/DepositCompletionController.cs:58` → `GetConfirmationRequirementsQuery` → `DepositConfirmationSnapshotReader` (excluye camiones anulados, `:42`) → `DepositConfirmationRequirements.Evaluate` (`:64-124`) → `ConfirmationRequirementsDto {canConfirm, missing[{code,message}]}` → `DepositConfirmationRequirements.vue` lista lo que falta con enlaces a cada sección (`:519-524`) y el botón se deshabilita con el motivo (`:149-153`).
2. «Confirmar» → diálogo (`:852-861`) → `useConfirmDeposit` → `S:829-835` `POST /foreign-trade/warehouse-storages/{id}/confirm` → `ForeignTradeController.cs:399-407` → `ConfirmStorageDepositHandler`: evalúa de nuevo (400 con la lista unificada, `:52-58`), transacción `Confirm()` + `OpenPeriodWithInvoiceAsync` desde `StoragePeriodCalculator.FirstStart(EntryDate)` (`:68-87`), avisos post-commit a Facturación (TRM pendiente, mínimo) (`:92-94`). Al éxito, la página ofrece imprimir la etiqueta (`:211-212`); al error, refresca los requisitos (`:213-217`).

## 2. Anular el depósito

`imports/[id]/index.vue:220-243` (`ReasonDialog`, motivo 10–500) → `useCancelWarehouseStorage` → `S:876-885` `POST /foreign-trade/warehouse-storages/{id}/cancel {reason}` → `ForeignTradeController.cs:510-529` (autor del token) → `CancelWarehouseStorageCommandValidator` → `CancelWarehouseStorageHandler`: transacción → `WarehouseStorageCancellationService.CancelAsync` (`:51-209`): `EnsureCancellable` → 409 por salidas ejecutadas o camión en báscula → órdenes activas (`DepositCancellationPlan`, `LoadingOrderReservationService`) → `InventoryMovement` `StorageCancellation` y `VoidStock` por producto → `WarehousePlacementService.TrimToStockAsync` → `StorageBillingPeriod.Close` → `InvoiceCancellationPolicy.Apply` → `ServiceRecord.VoidService` → `WarehouseStorage.Cancel` → `SaveChanges` con auditoría «Anulación del depósito…» → commit → `NotifyAsync` (Bodega por orden en curso, Facturación por facturas a revisar y anuladas, `:215-271`) → `CancelWarehouseStorageResponseDto` → `CorrectionResultDialog` (ítems retirados, órdenes canceladas, períodos, facturas) (`:245-254`, `:898-904`) → al cerrar, `/foreign-trade/deposits` (`:257`). Un 409 se muestra bajo el motivo (`:235-242`).

## 3. Cerrar el ingreso de camiones

`imports/[id]/index.vue:195-204`, `:862-870` → `useCloseTruckEntries` → `S:866-871` `POST /foreign-trade/warehouse-storages/{id}/close-truck-entries` → `ForeignTradeController.cs:413-428` → `CloseTruckEntriesCommandHandler` (400 si anulado o cerrado, `:23`) → `ServiceRecord.CloseTruckEntries` (409 si ya cerrado; servicio `Completed`, `ServiceRecord.cs:330-342`) → `CloseTruckEntriesResultDto {closedAt, closedByName, truckCount}` → encabezado con «Ingreso de camiones cerrado» (`:472-473`). Efecto en báscula: `StorageDocumentLookup.EnsureTruckEntriesNotClosedAsync` rechaza un camión nuevo del documento (`:99-118`) (módulo 02).

## 4. Corregir la fecha de ingreso

`F/features/foreign-trade/components/DepositDetailGeneralInfoCard.vue:183-218` → `EditDepositEntryDateDialog.vue` (límites `firstTruckEntryDateTime`/`firstTruckDepartureDateTime` y ahora, `:53-60`; motivo) → `useCorrectDepositEntryDate` → `S:905-917` `PATCH /warehouse-storages/{id}/entry-date` → `B/Wms.Api/Controllers/v1/DepositEntryDateController.cs:28` (`DepositEntryDateAccess`) → `CorrectDepositEntryDateCommandHandler` → `WarehouseStorage.CorrectEntryDate` (estado y estadía del primer camión; borra TRM DIAN si cambia el día) → auditoría → si Confirmado, `StorageRecalculationTrigger.HandleEntryDateChangedAsync` (rebase del período, nueva consulta TRM, aviso a Facturación) → `{entryDate, billingNotified}`. Efecto en etiqueta (`LabelGenerationService.cs:153`) y en abandono (`AbandonmentReader.cs:53`). Báscula usa el mismo endpoint (`F/pages/operations/weighbridge/cycles/[id].vue:606`).

## 5. Ajuste CE-7

`imports/[id]/index.vue:93-131`, `:871-878` (`AdjustInventoryDialog`, unidad de carga si aplica) → `useInventoryAdjustment` → `F/features/warehouse/services/warehouse-service.ts:601` `POST /warehouse/inventory/adjustments` → `InventoryAdjustmentController.cs:34` (`ForeignTradeAccess`; autor del token) → `AdjustInventoryCommandValidator` (observación obligatoria) → `AdjustInventoryCommandHandler`: estado, unidad, parámetro de correo, `EnsureReceivedCoversReleases` → `CorrectReceivedQuantity` → `TrimToStockAsync` → `InventoryMovement` (`Adjustment`) → auditoría → correo (no bloquea; `adminNotified`) → `RecalculateAsync` → aviso en pantalla según `adminNotified` (`:122-125`).

## 6. Etiqueta y registro de impresiones

`imports/[id]/index.vue:167-178` (imprimir en pestaña, `Print`) y `:394-412` (descargar, `Download`) → `S:262-266` `GET /foreign-trade/imports/{id}/label?action=` (blob) → `ForeignTradeController.cs:276-293`: `LabelPrintActions.Parse` (400 si no es `Print`/`Download`) → `GenerateImportLabelAsync` (400 si anulado) → `RecordLabelPrintAsync` → `LabelGenerationService.RecordPrintAsync` (fila en `WarehouseStorageLabelPrints`) → PDF → la página invalida `['foreign-trade','label-prints',warehouseStorageId]` → `LabelPrintsBadge` → `S:415-418` `GET /foreign-trade/warehouse-storages/{id}/label-prints` → `LabelPrintsController.cs:20` → conteos, última impresión y 50 filas. EXP (`:735-753`) e INSP (`:853-870`) igual.

## 7. Listas de empaque

- **Carga:** `PackingListUploadDialog.vue` (proveedor, alta rápida de proveedor `:37-65`, importador, archivo `.csv` `:235`, filas de encabezado `:88`, «Simular» `:312` / «Cargar» `:319`) → `S:971-986` `POST /foreign-trade/packing-lists/import` (multipart `file`, `supplierId`, `importerId`, `headerRows`, `dryRun`) → `PackingListsController.cs:65-99` (archivo requerido, ≤ 5 MB, UTF-8) → `ImportPackingListCommandHandler` (404 proveedor/importador; 400 sin filas válidas; simulación sin guardar; transacción; aviso a CE por productos creados) → `ImportPackingListResultDto` con filas y errores por fila.
- **Consulta y baja:** `F/pages/foreign-trade/packing-lists/index.vue` → `S:988-1001` → `PackingListsController.cs:101-131` (409 con asociados).
- **Asociación:** `DepositExpandedEntriesTable.vue:60` (solo Borrador) → `AssociatePackingListItemsDialog.vue` → `S:1003-1021` (`GET /foreign-trade/packing-list-items?importerId=…`, `POST /foreign-trade/deposits/{id}/entries/{entryId}/packing-list-items {itemIds, warehouseStorageCargoUnitId, reason}`) → `PackingListsController.cs:134-170` → `AssociatePackingListItemsCommandHandler` (Borrador, camión, artículos activos y de un importador, importador del depósito, unidad de carga; `AddToEntryAsync` por artículo con kárdex; asigna importador; `AfterCommitAsync`) → productos afectados.

## 8. Prórroga y abandono

- **Prórroga:** detalle (`imports/[id]/index.vue:556-583`) o fila del listado (`abandonment/index.vue:126`) → `RegisterExtensionDialog.vue` (notas ≤ 500) → `useRegisterExtension` → `S:219-226` `POST /foreign-trade/imports/{id}/extension {notes}` → `AbandonmentController.cs:33-45` → `RegisterStorageExtensionCommandHandler` (400 estado o sin saldo; 409 ya registrada, con fecha y usuario) → `ImportWarehouseStorage.RegisterExtension` → auditoría → `StorageExtensionResultDto` → invalida `['foreign-trade']`.
- **Listado:** `abandonment/index.vue:76-103` → `useAbandonmentList` → `S:231-239` `GET /foreign-trade/abandonment?status&hasExtension&warehouseStorageNumber&cargoManifestNumber&importerId&customsAgencyId&pageIndex&pageSize[&all]` → `AbandonmentController.cs:53-59` → `GetAbandonmentListHandler` (universo en memoria, d ≥ 20, filtros, paginación o `all`) → `ApiResponse.Success(items, pagination)`.
- **Resumen:** `AbandonmentSummaryAlert.vue` (tablero, `F/pages/foreign-trade/index.vue:62`) → `S:242-245` `GET /foreign-trade/abandonment/summary` → `{inAlert, abandoned}` → enlace a `?estado=en-alerta`.

## 9. Procesos automáticos

| Proceso | Legacy | V2 | Comparación |
| --- | --- | --- | --- |
| Alerta de abandono | `L/menus/evaluaabandonos.php` invocado al cargar `inicial.php` (nivel ≤ 1) y el menú (`bodegas-legacy/`) | `B/Wms.Api/BackgroundJobs/AbandonmentAlertBackgroundService.cs` (espera 1 min al arrancar, luego cada día a las 07:00 de Colombia; registrado en `B/Wms.Api/Program.cs:81`) → `AbandonmentAlertService.SendDailyAlertAsync` (`B/Wms.Application/ForeignTrade/Jobs/AbandonmentAlertService.cs:40-74`): universo de `AbandonmentReader`, sin envío si no hay casos, idempotencia diaria por `RelatedEntityType="AbandonmentReport"`, `NotifyRoleAsync(ForeignTrade)` nivel Warning «Depósitos en ventana de abandono», sin correo. | Equivalente con más alcance (BR-04-010). Errores del job solo se registran en el log (`AbandonmentAlertBackgroundService.cs:68-74`). |
| Reactivación de depósitos | Efecto del listado `listardepositos.php:507-576` | Sin equivalente; cierre automático por agotamiento en el cargue (`ExecuteLoadingOrderCommandHandler.cs:275-281`) y reapertura por reversión | BR-04-001 |
| Conciliación de VIN | Al listar (`listaringresos.php:384-404`) | Excluida (Colmotores) | NO_APLICA |

## 10. Servicios externos y efectos laterales

| Integración | Dónde | Nota |
| --- | --- | --- |
| TRM DIAN | Al confirmar (apertura de la factura) y al corregir la fecha de ingreso (`HandleEntryDateChangedAsync`) | La consulta y la factura son del módulo 06 (DEC-023). |
| Correo SMTP | CE-7 al parámetro `INVENTORY_ADJUSTMENT_ADMIN_EMAIL` (`AdjustInventoryCommandHandler.cs:164`) | No bloquea el ajuste (DEF-F5-003 Verificado). |
| Notificaciones | Anulación (Bodega, Facturación), listas de empaque (CE), job de abandono (CE), avisos de recálculo | Infraestructura en el módulo 08. |
| Auditoría genérica | `auditContext.Describe` en anulación, prórroga, cierre de camiones, fecha de ingreso, CE-7, listas de empaque | `IAuditable` → `audit_logs` (módulo 01). |
| PDF | Etiquetas (QuestPDF, `LabelGenerationService`), consolidado (`IDepositPdfService`) | Generación común en el módulo 07. |
