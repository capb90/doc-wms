# Plan de corrección de defectos — Campaña QA de octubre de 2026

> **Qué es:** el plan por fases para corregir los 126 defectos registrados en `docs/qa/resultados/defectos/` (125 fichas propias más DEF-F8-001, unificada en DEF-F3-002). No contiene código: cada cambio (`CHG-NN`) dice qué archivo, clase o componente se modifica, cómo queda el comportamiento y qué no se toca.
> **Fecha:** 3 de octubre de 2026. **Estado:** ejecutado. Aprobado el 2026-10-03; las 12 fases quedaron completadas el 2026-10-05 (cuadro de seguimiento de §4) y el re-test de la fase 11 de QA las verificó (`docs/qa/resultados/informe-final.md`). *Estado original:* propuesto; ninguna fase empieza sin la aprobación del usuario.
> **Código verificado (HEAD):** backend `wms-api` `develop` `191d4b1`; frontend `wms` `develop` `cd121d8`. Desde los builds de QA no hay commits de código: el backend sigue en `191d4b1`, y en el frontend los commits posteriores a `a5289ce` (`0d66226` … `cd121d8`) solo tocan `docs/` y `README.md`. Por eso ningún defecto figura como «Corregido en …».
> **Rutas:** las del backend son relativas a `Backend/wms-api` y empiezan por `Wms.`; las del frontend son relativas a `Frontend/wms` y empiezan por `app/` o `test/`. Un nombre de archivo sin carpeta (`RecordWeighingHandler.cs`) es único en su repositorio. Los números de línea son los de HEAD.
> **Fuentes:** `docs/contexto/contexto-negocio-wms-para-ia.md`, `docs/qa/00-plan-maestro.md` (§9 y §10), las 126 fichas, los informes F0–F10, `docs/qa/fase-11-regresion-cierre.md`, `docs/planes/paridad-legacy/plan-frontend-paridad-legacy.md` y el código de HEAD de los dos repositorios (y del legacy donde una ficha habla de paridad). `ajustes/historias-usuario-linear-2026-09-10.md` no está en el workspace; ninguna ficha depende de él para definir su corrección.
> **Estado del backlog:** las Olas 1, 2 y 3 (WMS-5 … WMS-33, salvo WMS-12, que no se implementa) y las fases 1 a 6 del plan de paridad ya están en `develop` (verificado en `git log` de ambos repositorios). El contexto del 14-sep las daba como pendientes.
> **Precedencia:** si una ficha choca con el §10 del plan maestro, manda el §10. Las decisiones del §10 se citan como «§10 · tema».

## 1. Resumen ejecutivo

- **Alcance:** las 126 fichas de la campaña QA de octubre de 2026 (13 CRITICAL, 46 MAJOR, 64 MINOR y 3 TRIVIAL), verificadas una por una en HEAD: 116 se reproducen, 10 se reproducen en parte y ninguna dejó de reproducirse. No hay commits de código posteriores a QA, así que ninguna queda como «corregida, solo re-test».
- **Destino:** 125 fichas en 90 cambios (CHG-01 a CHG-90) y DEF-F8-001 como duplicado de DEF-F3-002; ninguna se cierra por el §10.
- **Fases:** 12. Las Fases 1 a 3 cierran los 13 CRITICAL (seguridad y auditoría, operación diaria, dinero); las Fases 4 a 7, los MAJOR (seguridad y cobro en báscula, pagos y tarifas, inventario y salidas sin guía, resto); las Fases 8 a 12, los MINOR y TRIVIAL (validación en el servidor, facturación, Comercio Exterior e inventario, reportes y documentos, interfaz y textos). Ninguna fase depende de una posterior ni pasa de 12 cambios.
- **Causas raíz dominantes:** el API confía en lo que envía la pantalla (autor, permisos y validaciones que solo existen en el frontend); la báscula no es idempotente; la salida de importación no exige guía; varias reglas de dinero usan el dato equivocado (modalidad, período, base del IVA, vencimiento); fechas en UTC; mensajes técnicos.
- **Pruebas:** el primer cambio crea `Wms.IntegrationTests` (API con PostgreSQL en contenedor) y Vitest en el frontend; cada cambio trae sus pruebas, su re-test QA y sus criterios Dado/Cuando/Entonces.
- **Datos:** 8 migraciones, que genera y aplica el implementador de cada fase con `dotnet ef` sobre la base local de pruebas (regla 4.0.2); sin scripts de saneamiento mientras las bases sean de prueba; nada se aplica en staging ni en producción sin aprobación escrita del usuario.
- **Decisiones requeridas:** ninguna pendiente. D-1 (consolidación de los cobros «por facturar») y D-2 (cambio del modo de pago en báscula) se resolvieron el 3-oct-2026 con la recomendación del plan (§5). Pendientes que no son código: PRF-002 y la base de la fase 11 de QA (§7.3).

## 2. Verificación en HEAD

Cada ficha se verificó leyendo el código de HEAD (backend `191d4b1`, frontend `cd121d8`). «Parcialmente» significa que la ficha mezcla un síntoma que se reproduce con otro que no; la causa y el cambio cubren lo que sí se reproduce y la tarjeta del cambio explica el resto. Orden: severidad y luego ID.

| ID | Severidad | ¿Se reproduce? | Causa raíz (archivo:línea) | CHG |
|---|---|---|---|---|
| DEF-F2-001 | CRITICAL | Sí | `app/pages/operations/entries/index.vue:115-121,170-175` y `history.vue:84-90` usan `GET vehicles?licensePlate=…&pageSize=1` → `GetAllVehiclesHandler.cs:16-19` (`ILIKE %texto%`, toma el primero) | CHG-05 |
| DEF-F3-001 | CRITICAL | Sí | `Wms.Infrastructure/Persistence/SeedDataExtensions.cs:100` siembra el rol ForeignTrade con `NormalizedName = "FOREXTERIOR"` y `NotificationOrchestrator.cs:77` busca con `GetUsersInRoleAsync("ForeignTrade")`: CE no recibe avisos | CHG-04 |
| DEF-F3-004 | CRITICAL | Sí | `DiscardIncompleteOperationHandler.cs:29-33,70` no borra el vínculo `service_record_entry_logs`; la cola (`GetWeighbridgeQueueHandler.cs:48-62`) y los 6 cobros (p. ej. `ProcessStoragePaymentHandler.cs:47-54`) no filtran `Discarded` | CHG-06 |
| DEF-F4-001 | CRITICAL | Sí | `Wms.Application/Warehouse/Commands/Reception/CompleteReceptionCommandValidator.cs:12-13` exige productos y `CompleteReceptionCommandHandler.cs:85-89` los prohíbe en unidades de carga (igual en `CreateReceptionCommandValidator.cs:13-14`) | CHG-07 |
| DEF-F4-002 | CRITICAL | Sí | `app/features/warehouse/components/ReceptionStepManualInfo.vue:196-237` envía un cuerpo fuera de contrato (`authorizedByUserId: ""`, producto suelto); con `SuppressModelStateInvalidFilter` (`Wms.Api/Program.cs:51-53`) el comando llega nulo (500) | CHG-08 |
| DEF-F6-001 | CRITICAL | Sí | `Wms.Application/Billing/Services/RuleSpecificity.cs:41,48` (peldaños que aceptan cualquier modalidad), usados en `BillingResolver.cs:264-272` (convenio) y `:289-297` (tarifa base) | CHG-09 |
| DEF-F6-002 | CRITICAL | Sí | `Wms.Application/Billing/Commands/CloseStoragePeriods/CloseStoragePeriodsHandler.cs:65` llama `StoragePeriodCalculator.RenewalStart` (`StoragePeriodCalculator.cs:43-47`), que recorta el inicio a hoy | CHG-10 |
| DEF-F6-003 | CRITICAL | Sí | `Wms.Domain/Entities/Billing/InvoiceItem.cs:156-159`: el monto digitado se asigna al unitario neto, se multiplica por la cantidad y se suma IVA | CHG-11 |
| DEF-F6-004 | CRITICAL | Sí | `app/pages/billing/invoices/[id].vue:524` y `app/features/billing/components/OverrideAmountDialog.vue:122-125` muestran el total con IVA; `OverrideBillingAmountHandler.cs:31` guarda el original neto y `InvoiceItem.cs:156-159` toma lo digitado como neto | CHG-11 |
| DEF-F6-005 | CRITICAL | Sí | Vencimiento = creación en los cobros por facturar (`StartStoragePendingBillingHandler.cs:119`, `StartWeighingOnlyPendingBillingHandler.cs:93`, `StartOutputPendingBillingHandler.cs:99`, `EndForkliftUseCommandHandler.cs:134`, `CreateDispatchGuideCommandHandler.cs:333`) y `BillingJobService.cs:25-32` marca Overdue sin filtrar Draft/PendingApproval | CHG-12 |
| DEF-F6-006 | CRITICAL | Sí | `Invoice.cs:402` (`AmountPaid` nulo no vence), `BillingJobService.cs:41-49` (resumen por cliente antes de guardar) e `Invoice.cs:587-589` (la conciliación devuelve Overdue a PartiallyPaid) | CHG-13 |
| DEF-F7-001 | CRITICAL | Sí | `Wms.Infrastructure/Persistence/AppDbContext.cs:139-216` (`CollectAuditEntries`) serializa todas las propiedades, incluidas `PasswordHash`, `SecurityStamp` y `ConcurrencyStamp` de `ApplicationUser` (`ApplicationUser.cs:8`) | CHG-02 |
| DEF-F9-001 | CRITICAL | Sí | Escrituras sin política propia bajo `[Authorize]` de clase que solo exige autenticación: `Wms.Api/Controllers/v1/StakeholderController.cs:44` (terceros `:47,81,97,113,135,150,163,185,200,224`; convenios `:235,273,285,296`; servicios del convenio `:309,341,357,371,385`), `EntryReasonController.cs:18` (`:21,62,73`), `DriverController.cs:16` y `VehicleController.cs:16` (`:19,51`), `ProductController.cs:17` (`POST :20`) | CHG-03 |
| DEF-F1-001 | MAJOR | Sí | `Wms.Application/Products/Common/Mappers/ProductMapper.cs:11-12` lee `UnitMeasure` sin cargar en `CreateProductHandler.cs:45`, `GetProductHandler.cs:24` y `UpdateProductHandler.cs:47` | CHG-41 |
| DEF-F1-002 | MAJOR | Sí | `Wms.Api/Common/Behaviors/ValidationBehavior.cs:6` (`where TRequest : IRequest<TResponse>`) no se aplica a comandos `IRequest` sin respuesta: `ChangePasswordValidator.cs:10-12` nunca corre (y otros 10 comandos) | CHG-14 |
| DEF-F1-003 | MAJOR | Sí | `ServicePricingRuleRequest.cs:9-15` no declara `AppliesToPerishable`; `UpdateServicePricingRuleHandler.cs:46` lo borra en cada edición | CHG-26 |
| DEF-F1-004 | MAJOR | Sí | `AddAgreementServiceHandler.cs:96-123` y `UpdateAgreementServiceHandler.cs:125-152` no llaman `FormulaCalculatorRegistry.ValidateParameters` (rangos en `PercentageOfValueFormulaCalculator.cs:51-66`) | CHG-27 |
| DEF-F1-005 | MAJOR | Sí | `CreateVehicleHandler.cs:16-22` (igualdad sensible a mayúsculas), `VehicleConfiguration.cs:24` (índice no único), `CreateVehicleValidator.cs:10-12` (sin formato), `CreateVehicleHandler.cs:32-38` (transportadora sin rol) | CHG-05 |
| DEF-F1-009 | MAJOR | Sí | `WmsAuthentication.cs:38-67` no revalida al usuario por petición; `TokenService.cs:62-69` no incluye el `SecurityStamp`; desactivar, cambiar roles y cerrar sesión no rotan el sello (`ManageUserActivationHandler.cs:44-56`, `RemoveRolesToUserHandler.cs:43-48`, `LogoutHandler.cs:8-12`) | CHG-16 |
| DEF-F2-004 | MAJOR | Sí | `Wms.Application/Reports/Queries/GetTraceabilityDashboard/TruckStageResolver.cs:20-21` evalúa «En portería» antes de la salida; `GetTraceabilityDashboardHandler.cs:179-186` cuenta por rótulo | CHG-42 |
| DEF-F3-002 | MAJOR | Sí | Lectura previa sin bloqueo ni índice único: `InitiateStorageWeighingHandler.cs:192-196` (el único bloqueo, el del consecutivo, llega después en `:390-391`), `InitiateOutputWeighingHandler.cs:47-52`, `InitiateWeighingOnlyHandler.cs:49-54`, `ProcessStoragePaymentHandler.cs:94-141`, `ProcessWeighingOnlyPaymentHandler.cs:76-83`, `ProcessOutputPaymentHandler.cs:82-89`; `EntryLogConfiguration.cs:89-91` y `WeighbridgeCycleConfiguration.cs:42-44` sin índice que lo impida | CHG-17 |
| DEF-F3-003 | MAJOR | Sí | `app/features/weighbridge/components/WeightCapture.vue:158-174` inicia y repone la hora con el ingreso o el pesaje anterior y `:216` la envía con `toOperationalIso` (instante exacto del límite) | CHG-44 |
| DEF-F3-005 | MAJOR | Sí | `RegisterDepartureHandler.cs:47-52` y `UpdateDepartureAuthorizationHandler.cs:64-84` solo validan que no haya salida previa | CHG-30 |
| DEF-F3-006 | MAJOR | Sí | `app/pages/operations/weighbridge/index.vue:461-483` rearma la operación con ceros y los formularios del Registro (`:1486-1534`) quedan en blanco; no hay `beforeunload` | CHG-20 |
| DEF-F3-007 | MAJOR | Sí | `index.vue:939-941` lee `customerId`, que no traen `InitiateWeighingResponseDto`, `InitiateStorageResponseDto` (`RegisterStorageEntryHandler.cs:44-65`) ni `InitiateOutputResponseDto`; `:961-965` cae en el conductor | CHG-19 |
| DEF-F3-008 | MAJOR | Sí | `index.vue:633-636` y `:738-740` no envían la tarjeta «Camión y conductor» que `:582-585` exige; `InitiateWeighingOnlyRequest` e `InitiateOutputWeighingRequest` no tienen esos campos | CHG-46 |
| DEF-F3-011 | MAJOR | Sí | `WeightCapture.vue:372-379` exige el modo `MultiDeposit`, que el backend solo informa con más de un depósito (`GetWeighbridgeCycleHandler.cs:79-83`) | CHG-45 |
| DEF-F3-012 | MAJOR | Sí | `InitiateOutputWeighingHandler.cs:62-93` no valida el estado de la OC ni la existencia de un servicio de salida activo | CHG-32 |
| DEF-F3-013 | MAJOR | Parcialmente | `history.vue:200-210` compara nombres visibles de rol; `weighbridge-service.ts:223` llama `PATCH weighbridge/{id}/payment-mode`, que no existe (borrado en `a088674`), y la acción no se muestra (`history.vue:572`) | CHG-47 |
| DEF-F3-014 | MAJOR | Sí | `CompleteCycleHandler.cs:113-122`, `RecordWeighingHandler.cs:460-477`, `ModifyFirstWeightHandler.cs:62` y `ModifySecondWeightHandler.cs:66` no comparan tara con bruto | CHG-37 |
| DEF-F3-016 | MAJOR | Parcialmente | `GetVehicleByPlateHandler.cs:19-24` sin filtro `IsActive` ni orden (se reproduce); la salida con tiquete compara `VehicleId` (`EntryTicketExitRules.cs:59-61`), no placas (la hipótesis de mayúsculas no se reproduce) | CHG-05 |
| DEF-F3-017 | MAJOR | Sí | `index.vue:376-380` convierte todo `Input` en depósito; Solo báscula también es `Input` y `ProcessStoragePaymentHandler.cs:57-61` acepta el cobro sin enlazar la factura al ciclo | CHG-20 |
| DEF-F4-003 | MAJOR | Sí | `RecordWeighingHandler.cs:223-242` y `CompleteCycleHandler.cs:163-175` no exigen la llegada a Bodega; `GetPendingFromWeighbridgeHandler.cs:22-26` oculta los ciclos completos de dos pesajes | CHG-36 |
| DEF-F4-004 | MAJOR | Sí | `WarehouseStorage.cs:285-303` (`MarkForCorrection` no mira órdenes) y `ExecuteLoadingOrderCommandHandler.cs:53-68` (no mira el estado del depósito) | CHG-31 |
| DEF-F4-005 | MAJOR | Sí | `CreateReceptionWithoutWeighbridgeCommandHandler.cs:169-178` crea un `EntryLog` nuevo sin usar el ingreso abierto | CHG-08 |
| DEF-F4-006 | MAJOR | Sí | `WarehouseStorage.Close()` pone `IsActive = false` (`WarehouseStorage.cs:325-326`) y `GetExportDepositDetailHandler.cs:67`, `GetExportDepositsHandler.cs:28` filtran por `IsActive` | CHG-43 |
| DEF-F5-001 | MAJOR | Sí | `DepositDetailGeneralInfoCard.vue:224-235`: el diálogo con `v-if` quedó entre `v-if="!editing"` y `v-else`, que se empareja con el diálogo | CHG-21 |
| DEF-F5-002 | MAJOR | Sí | `AdjustInventoryCommandHandler.cs:122-146` no crea `InventoryMovement`; `UpdateDepositProductCommandHandler.cs:58` y `DepositProductEditing.cs:28-32,263` mueven stock sin movimiento | CHG-39 |
| DEF-F5-003 | MAJOR | Sí | `AdjustInventoryCommandHandler.cs:116` envía el correo antes de validar (`:131`, `:136`) y de guardar (`:146`); `EmailService.cs:183-219` relanza la `SmtpException` | CHG-38 |
| DEF-F5-004 | MAJOR | Sí | `WarehouseStorageProduct.CorrectReceivedQuantity` (`WarehouseStorageProduct.cs:334-356`) no consulta los levantes | CHG-38 |
| DEF-F5-005 | MAJOR | Sí | `RegisterImportReleaseCommandHandler.cs:36` solo rechaza Borrador; `UpdateImportReleaseCommandHandler.cs:30-35` y `LabelGenerationService.cs:54,280,484` no miran el estado; `imports/[id]/index.vue:402-421` muestra «Registrar levante» sin estado | CHG-40 |
| DEF-F5-014 | MAJOR | Sí | Ningún punto que despacha una OC consulta la guía: `RecordWeighingHandler.cs:500-520` (`Dispatch()` en `:515`), `CompleteCycleHandler.cs:224-236`, `ExecuteLoadingOrderCommandHandler.cs:333-356`, `ExitWithEntryTicketCommandHandler.cs:94-96`, `AddAdditionalOrdersCommandHandler.cs:77-78`; Vigilancia (`RegisterDepartureHandler.cs:35-52`) no mira órdenes | CHG-33 |
| DEF-F6-007 | MAJOR | Sí | `StorageBillingService.cs:292-297` cuenta el piso de la regla PER_CARGO_UNIT también como «por contenedor»; `PerCargoUnitFormulaCalculator.cs:16-25` no aplica el piso | CHG-25 |
| DEF-F6-009 | MAJOR | Sí | `RecordPaymentHandler.cs:30-37` solo rechaza Cancelled/Paid; `app/plugins/api-client.ts:22` sin `paramsSerializer` (el filtro `statuses[]` no enlaza) y `app/pages/billing/payments/index.vue:80-81` imprime «null» | CHG-22 |
| DEF-F6-010 | MAJOR | Sí | `PaymentDialog.vue:48-66` envía el archivo como data-URL en `voucherUrl`; `InvoicePaymentConfiguration.cs:24` limita la columna a 500 | CHG-29 |
| DEF-F6-011 | MAJOR | Sí | `BillingController.cs:134-165` mantiene `POST billing/invoices` y `app/pages/billing/invoices/create.vue` carga por URL | CHG-28 |
| DEF-F6-012 | MAJOR | Sí | `Agreement.cs:71-77,90-97` comparan sin el indicador perecedero; los comandos no lo declaran y `idx_agreement_service_unique_active` (`AgreementServiceConfiguration.cs:30-34`) no lo incluye | CHG-26 |
| DEF-F6-013 | MAJOR | Sí | `Invoice.cs:409-427` (`Cancel` no mira pagos) y `CancelInvoiceHandler.cs:24-31` (no carga pagos) | CHG-22 |
| DEF-F6-021 | MAJOR | Sí | `StorageBillingService.cs:237,251` cobra el mínimo de modalidad como neto + IVA y `PercentageOfValueFormulaCalculator.cs:41-42` (y `StorageMinimumFloor.cs:41-42`) trata el mínimo de fórmula como IVA incluido; `ServiceMinimumValue.cs:15-26` no tiene campo de base | CHG-24 |
| DEF-F6-022 | MAJOR | Sí | `Invoice.cs:441-445` (`AssignInvoiceNumber` rechaza Paid) y `app/features/billing/utils/invoice-action-rules.ts:53-58` | CHG-23 |
| DEF-F7-002 | MAJOR | Sí | `TruckStageResolver.cs:58` devuelve «Desconocido» para Discarded, ciclo InProgress, Weighing sin ciclo e ingreso Completed sin servicio | CHG-42 |
| DEF-F8-001 | MAJOR | Sí (misma causa) | Idéntica a DEF-F3-002: `InitiateStorageWeighingHandler.cs:192-196` y `ProcessStoragePaymentHandler.cs:94-141` | Duplicado de DEF-F3-002 |
| DEF-F8-002 | MAJOR | Parcialmente | La rama multicliente ya factura por dueño (`CreateDispatchGuideCommandHandler.cs:215-306`), pero con destinatario único factura todo al primer dueño (`:307-372`, `:311`) y nada exige el modo multicliente con varios dueños (`:143-153`); firmante = `loadingOrder.Stakeholder` (`:167-172`) | CHG-34 |
| DEF-F8-003 | MAJOR | Sí | `ExecuteLoadingOrderCommandHandler.cs:342-355` despacha al cargar cuando la salida fue con tiquete de ingreso y `CreateDispatchGuideCommandHandler.cs:115-123` rechaza órdenes Dispatched | CHG-33 |
| DEF-F8-004 | MAJOR | Sí | `DispatchGuidePdfService.cs:499-504` calcula al imprimir el levante más reciente del depósito; `DispatchGuideLine.cs:21-31` no lo congela | CHG-35 |
| DEF-F8-005 | MAJOR | Sí | `CreateReceptionWithoutWeighbridgeCommandHandler.cs:281` confirma el depósito y `:289-315` abre período y factura | CHG-08 |
| DEF-F9-002 | MAJOR | Sí | `WmsAuthentication.cs:77-79` (`WarehouseAccess` incluye Receiving), usada por `EntryLogController.cs:19` y `DepartureAuthorizationController.cs:13`; las 12 páginas de `app/pages/warehouse/**` incluyen `Receiving` en `requiredRoles` (p. ej. `app/pages/warehouse/index.vue:4`) | CHG-03 |
| DEF-F9-003 | MAJOR | Sí | El autor viaja en el cuerpo: `CreateEntryLogCommand.cs:8`, `RegisterDepartureCommand.cs:8` (`EntryLogController.cs:69-71`), `CreateDepartureAuthorizationCommand.cs:8`, `CreateReceptionWithoutWeighbridgeCommand.cs:73-74`, `ExecuteLoadingOrderRequest.CompletedBy` (`WarehouseController.cs:1158`) y 8 campos de `BillingController.cs` (p. ej. `:332-345`); la firma solo limita tamaño (`ExecuteLoadingOrderCommandValidator.cs:39-40`) | CHG-15 |
| DEF-F10-001 | MAJOR | Sí | No hay guardia de envío común: `ReceptionStepManualInfo.vue:622-630` nunca bloquea; `app/pages/billing/invoices/[id].vue:54-55,105-111` y `payments/index.vue:52-53,140-146` usan `mutate` sin estado; `loading-orders/create.vue:19-24` y `dispatch-guides/create.vue:22-27` rehabilitan el botón 2 s; `PaymentDialog.vue:57-79` y `InvoiceActionsDialog.vue:278` sin bloqueo | CHG-18 |
| DEF-F0-001 | MINOR | Sí | 10 componentes usan `<LabelBase>` sin `import`; Nuxt solo registra `BaseLabelBase` (`.nuxt/components.d.ts:22`) | CHG-85 |
| DEF-F0-002 | MINOR | Sí | `app/pages/warehouse/receptions/create.vue:15-20` no importa `ReceptionStepManualInfo` (usado en `:297-303`); la página no tiene menú y duplica flujos | CHG-85 |
| DEF-F0-003 | MINOR | Sí | `app/components/layout/AppTopbar.vue:39` y `AppSidebar.vue:34` enlazan `/`, que solo admite Admin y ForeignTrade (`app/pages/index.vue:11`); `app/pages/access-denied.vue:28-35` solo ofrece cerrar sesión | CHG-87 |
| DEF-F1-006 | MINOR | Sí | `app/features/users/components/UserForm.vue:191` (`extend(schemaSecurityBase.shape)` descarta el `.refine` de coincidencia de `:178-189`) | CHG-50 |
| DEF-F1-007 | MINOR | Sí | `UpdateStakeholderHandler.cs:24-32` y `UpdateProductHandler.cs:29-37` sin chequeo de unicidad; `Wms.Api/Common/Exception/GlobalExceptionHandler.cs:103-111` devuelve el texto de Postgres | CHG-49 |
| DEF-F1-008 | MINOR | Sí | `app/features/stakeholders/components/StakeholderForm.vue:315`, `useStakeholderCreate.ts:14-15`, `QuickCreateStakeholderDialog.vue:66-203` y `CreateStakeholderHandler.cs:20` | CHG-90 |
| DEF-F1-010 | MINOR | Sí | `RemoveRolesToUserHandler.cs:38-48` y `ManageUserActivationHandler.cs:44-56` sin reglas sobre el propio usuario, el último rol ni el último administrador | CHG-50 |
| DEF-F1-011 | MINOR | Sí | `LoginHandler.cs:30-33` responde «Usuario inactivo» antes de verificar la contraseña; `RequestPasswordResetHandler.cs:56-59` responde 401 a cuentas existentes no administradoras y 204 a las inexistentes | CHG-51 |
| DEF-F2-002 | MINOR | Sí | `CreateVehicleValidator.cs:10-12` y `Vehicle.cs:24-37` guardan la placa sin formato; `entries/index.vue:197-199` crea el vehículo sin validar | CHG-05 |
| DEF-F2-003 | MINOR | Sí | `EntryLog.cs:55` (`RegisterEntry` acepta fecha futura) y `EntryLog.cs:83-88` (`RegisterDeparture` no compara con el ingreso) | CHG-52 |
| DEF-F3-009 | MINOR | Sí | `RegisterStorageEntryValidator.cs:13-45` sin transportadora; `InitiateStorageWeighingValidator.cs:114-122` sin 2 decimales ni moneda con valor; los 6 validadores de cobro solo exigen nombre no vacío (p. ej. `ProcessStoragePaymentValidator.cs:42-54`) | CHG-53 |
| DEF-F3-010 | MINOR | Sí | `GetServiceRecordByDocumentHandler.cs:34-40` usa `StorageDocumentLookup.MatchOpenAsync`, que excluye documentos con ingreso cerrado (`StorageDocumentLookup.cs:33`) | CHG-54 |
| DEF-F3-015 | MINOR | Parcialmente | `WeighingTotals.cs:15-16` anula los pesos con un solo pesaje; el tablero (`app/features/weighbridge/composables/useWeighbridgeDashboard.ts:10-60`) cuenta con el historial (solo ciclos terminales) y con `GetPendingSecondWeightHandler.cs:37-38`; el contador «Entradas» del historial no es defecto (cuenta ciclos terminales) | CHG-76 |
| DEF-F3-018 | MINOR | Parcialmente | `index.vue:1461-1465` muestra el formulario editable con `:inert` (no se puede teclear, pero parece editable y no dice dónde corregir) | CHG-20 |
| DEF-F3-019 | MINOR | Sí | `CashReceived` en los 3 requests y commands de cobro, `CashChangeCalculator.cs:10-33` y las reglas de `ProcessStoragePaymentValidator.cs:32-40` (y equivalentes) | CHG-53 |
| DEF-F4-007 | MINOR | Sí | `app/features/warehouse/components/ReceptionList.vue:56-57` envía los dos límites con la medianoche local en UTC (desde = hasta); `GetReceptionsHandler.cs:29-37` compara el `DateTimeOffset` sin normalizar y Npgsql rechaza el desfase -05:00 (500) | CHG-77 |
| DEF-F4-008 | MINOR | Sí | `WarehouseController.cs:991-1018` no enlaza `all`, así que el Excel recibe 20 filas; `useWarehouseExports.ts:43,45` lee campos que el API no envía | CHG-78 |
| DEF-F4-009 | MINOR | Sí | `CompleteReceptionCommandValidator.cs` sin reglas de fotos y `CompleteReceptionCommandHandler.cs:259-268` deduce el tipo del prefijo y usa `.jpg` por defecto (igual en cargue: `ExecuteLoadingOrderCommandHandler.cs:482-492`) | CHG-55 |
| DEF-F4-010 | MINOR | Sí | `ReceptionDeclaredDifference.cs:63-68` compara solo productos contados; `ReceptionLineDifference.cs:11-12` devuelve null si falta lo contado | CHG-56 |
| DEF-F4-011 | MINOR | Sí | `NoveltyInputValidator.cs:21-24` y `WarehouseNovelty.cs:121` no comparan buena + dañada + faltante con el total (regla de paridad «sin suma, como el legacy») | CHG-57 |
| DEF-F4-012 | MINOR | Sí | `ExecuteLoadingOrderCommandHandler.cs:47-50` toma `CompletedBy` del cuerpo; `ExecuteLoadingOrderCommandValidator.cs:39-40` no exige la firma (y el handler no la guarda) | CHG-15 |
| DEF-F4-013 | MINOR | Sí | `StartForkliftUseCommandValidator.cs:21-22` y `EndForkliftUseCommandValidator.cs:13-14` con `>= 0`; `ForkliftUse.cs:52,84` acepta inicial 0 y final igual al inicial | CHG-58 |
| DEF-F4-014 | MINOR | Parcialmente | `ExecuteLoadingOrderCommandHandler.cs:75-89` cubre Cancelled, Complete y Loaded; con Dispatched o Reverted cae al 404 de reserva de `:157-161` | CHG-31 |
| DEF-F4-015 | MINOR | Sí | `app/pages/warehouse/receptions/entry.vue:184-188` y `types/reception.ts:274-276` leen `firstWeight`/`firstWeightCapturedAt`; el API envía `entryWeight`/`entryCapturedAt` (`PendingFromWeighbridgeDto.cs:25-27`) | CHG-75 |
| DEF-F4-016 | MINOR | Parcialmente | `ForkliftUseList.vue:670-717` no pinta horómetros, valor, modo ni factura y `ForkliftUseDto` no los trae (`GetActiveForkliftUsesHandler.cs:20-27`); el detalle sí existe (`:718-730`) | CHG-58 |
| DEF-F4-018 | MINOR | Sí | `WarehouseController.cs:1078-1099` reutiliza el listado de CE, que excluye Borrador y exige cliente (`GetLoadingOrderDepositsHandler.cs:30-35`) | CHG-74 |
| DEF-F5-006 | MINOR | Sí | `GetImportDepositsHandler.cs:27-38` no excluye anulados y el tablero cuenta su total; `app/pages/foreign-trade/index.vue:43` enlaza «Guías pendientes» al historial | CHG-43 |
| DEF-F5-007 | MINOR | Sí | `app/pages/foreign-trade/deposits/index.vue:37-47,61-69` pagina todo el Kanban junto; `GetDepositsHandler.cs:112-115` suma stock de unidades distintas con la unidad del primer producto | CHG-69 |
| DEF-F5-008 | MINOR | Sí | `ValidateDepositCommandHandler.cs:46-54` y `GetDepositValidationHandler.cs:43-58` usan solo el último ciclo; `MarkAsValidated()` no guarda la plantilla ni impide revalidar | CHG-70 |
| DEF-F5-009 | MINOR | Sí | `GetLoadingOrdersHandler.cs:50-62` filtra por `lo.ServiceRecord`, que nunca se asigna (`LoadingOrder.cs:122`), y por el cliente en vez del importador | CHG-71 |
| DEF-F5-010 | MINOR | Sí | `DispatchGuidePdfService.cs:91-143` sin `Include` de `Product` (producto «N/A» al reimprimir); `CreateDispatchGuideCommandHandler.cs:167-172` firma con el cliente; `StorageBillingService.cs:774` compara el nombre «Agencia de Aduanas» (el catálogo dice «Agencia de aduanas»); `LabelGenerationService.cs:67-70,292-295` toma como intermediario el primer tercero no importador | CHG-73 |
| DEF-F5-011 | MINOR | Sí | `app/features/billing/components/BillingCollectForm.vue:238,535-540,587,629` no calcula ni muestra el total en modo multicliente; `app/pages/foreign-trade/dispatch-guides/create.vue:74,98-104` con textos obsoletos | CHG-34 |
| DEF-F5-012 | MINOR | Sí | `GetImportDepositDetailHandler.cs:222` toma a `EntryLog.EntryAuthorizedBy` (Vigilancia); `ReceptionLog` no guarda quién recibió; `:215-224` mezcla unidades | CHG-72 |
| DEF-F6-008 | MINOR | Sí | `BillingCycleCatalog.cs:33` publica OnDemand y `StorageBillingService.cs:368-372` no abre período para ese ciclo | CHG-60 |
| DEF-F6-014 | MINOR | Sí | `StakeholderBillingConfiguration.cs:57-77` solo asigna el límite con valor (`:75`) y `BillingConfigForm.vue:86` omite el campo vacío | CHG-61 |
| DEF-F6-015 | MINOR | Sí | `UpdateAgreementServiceHandler.cs` convierte los campos omitidos en `null` y `AgreementService.Update` (`AgreementService.cs:67-77`) los asigna | CHG-26 |
| DEF-F6-016 | MINOR | Sí | `PreviewFormulaHandler.cs:39,45-46` omite IVA incluido, cantidad base, unidades por tipo y tipo de vehículo que sí usa `BillingResolver.cs:93-119` | CHG-64 |
| DEF-F6-017 | MINOR | Sí | `BillingJobService.cs:111-167` solo concilia pagos; los cobros por facturar de báscula y montacargas no leen la preferencia (`StartWeighingOnlyPendingBillingHandler.cs:89`, `EndForkliftUseCommandHandler.cs:130`) | CHG-63 |
| DEF-F6-018 | MINOR | Sí | `BillingJobService.cs:293-340` no guarda qué facturas avisó y notifica en cada corrida; `CloseStoragePeriodsHandler.cs:76-81` y `BillingJobService.cs:263` no avisan la renovación | CHG-62 |
| DEF-F6-019 | MINOR | Sí | `Program.cs:51-53` suprime el 400 automático: un enum inválido deja el cuerpo en `null` y `BillingController.cs:334` lanza NullReference (500) | CHG-48 |
| DEF-F7-003 | MINOR | Sí | `GetDailyOutgoingGoodsReportHandler.cs:39,66-72` parte de las guías vigentes y omite órdenes despachadas sin guía | CHG-79 |
| DEF-F7-004 | MINOR | Sí | `GetDailyIncomingGoodsReportHandler.cs:115` usa `NetDeclaredWeight` (vacío desde WMS-10); `:75-88,95-96,106,112` buscan placa y transportadora en el ciclo del servicio ancla; `:108` toma una entrada cualquiera para el tiquete | CHG-82 |
| DEF-F7-005 | MINOR | Sí | `app/pages/reports/general-inventory.vue:55` llama `GET warehouse/locations` (`WarehouseController.cs:897-905`, política `WarehouseAccess`): CE recibe 403 y `app/app.vue:53-69` lo pinta como error | CHG-03 |
| DEF-F7-006 | MINOR | Sí | `app/utils/excel-export.ts:59-73` convierte con `toColombiaPickerDate` (`app/utils/colombia-date.ts:60-65`), un `Date` local que exceljs serializa en UTC (+5 h) | CHG-83 |
| DEF-F7-007 | MINOR | Sí | `GetDepositBillingHandler.cs:65-72` parte de los períodos, que la refacturación re-enlaza a la factura nueva (`ReissueInvoiceCommandHandler.cs:72`) | CHG-65 |
| DEF-F7-008 | MINOR | Sí | 17 entidades de catálogo sin `IAuditable` (p. ej. `PackagingType.cs:5`, `UnitMeasure.cs:10`, `ForkliftRate.cs:6`, `Vehicle.cs:5`, `AgreementService.cs:11`); `AppDbContext.cs:149-150` solo audita `IAuditable` | CHG-68 |
| DEF-F7-009 | MINOR | Parcialmente | `app/pages/reports/warehouse-movements.vue:154-215` no exporta la hoja de movimientos; en pantalla las líneas están en una fila expandible cerrada (`:129`, `:446-500`) | CHG-78 |
| DEF-F7-010 | MINOR | Sí | `GetTraceabilityDashboardHandler.cs:20-21,192-203` (día UTC) y `:40-41` (`Contains` sensible a mayúsculas); `app/pages/index.vue:17,23-28` abre en «Hoy»; título literal en 17 handlers (p. ej. `CreateEntryLogHandler.cs:154`) | CHG-81 |
| DEF-F7-011 | MINOR | Parcialmente | `InvoicePdfService.cs:145-147` no imprime el detalle; `WeighbridgeTicketPdfService.cs:203-206` toma el contacto de otro tercero («Teléfono: 0»); ocho PDF con literales de empresa distintos y sin parámetros `COMPANY_*` | CHG-84 |
| DEF-F7-012 | MINOR | Sí | `GetOperationalStatisticsHandler.cs:20,27` calcula el bloque `Billing` para cualquier rol (`ReportController.cs:155-162` no pasa el rol); `app/pages/reports/statistics.vue:232-375` lo muestra a CE | CHG-80 |
| DEF-F8-006 | MINOR | Sí | `StorageBillingService.cs:779-783` (`BuildDepositDetail` usa `DeclaredQuantity`) | CHG-66 |
| DEF-F8-007 | MINOR | Sí | `WarehouseStorageCancellationService.cs:200-232` solo avisa órdenes en cargue y facturas «para revisar»; el stock retirado y las facturas que anula el WMS no generan aviso | CHG-67 |
| DEF-F8-008 | MINOR | Sí | `InitiateOutputWeighingHandler.cs:136-144` crea el servicio de salida sin pasar la OC a InProgress; `LoadingOrder.StartLoading` solo se llama al cargar (`ExecuteLoadingOrderCommandHandler.cs:141-145`) | CHG-32 |
| DEF-F8-009 | MINOR | Sí | `GetDailyBillingReportHandler.cs:54-56` rotula «Solo Pesaje» todo ingreso con `SingleWeightOnly` (también INSP) | CHG-76 |
| DEF-F9-004 | MINOR | Sí | `app/pages/reports/general-inventory.vue:19` sin `Billing` en `requiredRoles` y el grupo «Facturación» de `app/components/layout/AppMenu.vue:431-474` sin el ítem | CHG-03 |
| DEF-F9-005 | MINOR | Sí | `InventoryReportsController.cs:18,27-30` y `WarehouseMovementsReportController.cs:22,34-38,61-65` solo exigen autenticación (`ActiveUser` de clase) | CHG-03 |
| DEF-F9-006 | MINOR | Sí | `Wms.Api/Program.cs:51-54` (`SuppressModelStateInvalidFilter = true`): el cuerpo inválido llega nulo, `mediator.Send(null)` lanza `ArgumentNullException`; `GlobalExceptionHandler.cs:16-18` expone el tipo en Development y `:103-111` el texto de PostgreSQL | CHG-48 |
| DEF-F10-002 | MINOR | Sí | `app/features/billing/components/PaymentDialog.vue:77-78` emite `submit` y llama `resetForm()` sin esperar el resultado | CHG-18 |
| DEF-F10-003 | MINOR | Sí | Tres emisores del mismo error: `app/app.vue:53-69` (global), el `onError` de los hooks (`useAssignInvoiceNumber.ts:23-28`, `useRecordPayment.ts:23-28`) y el texto en línea (`InvoiceActionsDialog.vue:100-110`); `api-client.ts:147` rechaza con el cuerpo y no con un error | CHG-86 |
| DEF-F10-004 | MINOR | Sí | `api-client.ts:90-97` rotula la caída como 500; `app/plugins/vue-query.ts:18` deja el reintento 3 por defecto y los sondeos repiten el aviso; nada refresca al volver el API | CHG-86 |
| DEF-F10-005 | MINOR | Parcialmente | `app/pages/billing/invoices/[id].vue:255-266` lee `error.message` (tarjeta vacía tras 4 intentos); `api-client.ts:143` rotula «Error interno» el 404 sin cuerpo del ID mal formado; no existe `app/error.vue` | CHG-87 |
| DEF-F10-006 | MINOR | Sí | 63 `toLocaleString()` sin locale, 59 `<InputNumber>` sin `locale="es-CO"` y 93 formatos de fecha distintos con la zona del navegador (p. ej. `app/pages/operations/weighbridge/history.vue:352`, `cycles/[id].vue:502`) | CHG-88 |
| DEF-F10-007 | MINOR | Sí | Faltan claves del idioma de PrimeVue en `nuxt.config.ts:47-215` y los mensajes de `FileUpload`; `history.vue:650` muestra «Pesaje #0 (Gross)»; `app/pages/admin/audit/index.vue:84-88` muestra la clase; mensajes del backend con estados en inglés (`WeighbridgeCycle.cs:78,89,100,113`, `Invoice.cs:76,93,339,494`) | CHG-90 |
| DEF-F10-008 | MINOR | Sí | `app/components/app/AppTable.vue:635-669` pinta acciones de solo ícono sin `aria-label`; filtros solo con placeholder (`:456`, `:565-600`); ningún formulario mueve el foco al primer error | CHG-89 |
| DEF-F4-017 | TRIVIAL | Sí | `StartForkliftUseCommandValidator.cs:12-35` devuelve dos errores con «service record» y claves internas del enum; `StartForkliftUseCommandHandler.cs:75-77` muestra un GUID | CHG-58 |
| DEF-F5-013 | TRIVIAL | Sí | `WarehouseStorage.cs:278,290,402`, `UpdateDraftDepositHandler.cs:40`, `UpdateDepositStakeholdersHandler.cs:43` y `CreateDispatchGuideCommandHandler.cs:122` interpolan el enum en inglés; `CreateDispatchGuideCommandHandler.cs:107-112` trata inspección como exportación | CHG-90 |
| DEF-F6-020 | TRIVIAL | Sí | `UpdateInvoiceValidator.cs:9` sin mensaje propio; `ReissueInvoiceCommandHandler.cs:43` arma «sin número … como sin número» | CHG-90 |

## 3. Matriz de trazabilidad

Las 126 fichas de `docs/qa/resultados/defectos/INDICE.md`, cada una una sola vez, en orden de ID. «Casos detectores» son los de la ficha; el re-test completo de cada cambio está en su tarjeta (§4).

| ID | Severidad | Título | Destino | Casos detectores |
|---|---|---|---|---|
| DEF-F0-001 | MINOR | 10 componentes usan `LabelBase` sin importarlo | Fase 12 · CHG-85 | F0-NAV-003 |
| DEF-F0-002 | MINOR | `receptions/create.vue` usa `ReceptionStepManualInfo` sin importarlo | Fase 12 · CHG-85 | F0-NAV-003 |
| DEF-F0-003 | MINOR | El logo lleva a «Acceso Denegado» y esa pantalla no permite volver | Fase 12 · CHG-87 | F0-NAV-005, F0-LOG-007, F0-NAV-004 |
| DEF-F1-001 | MAJOR | Productos: `GET`, `POST` y `PATCH product` responden 500 (NullReferenceException) | Fase 7 · CHG-41 | F1-PRO-001, F1-PRO-002, F1-PRO-005, F1-PRO-007 |
| DEF-F1-002 | MAJOR | El cambio de contraseña no aplica la política de contraseña fuerte en el backend | Fase 4 · CHG-14 | F1-AUT-011 |
| DEF-F1-003 | MAJOR | La dimensión «perecedero» (WMS-32) no se puede configurar: el API descarta `appliesToPerishable` | Fase 5 · CHG-26 | F1-SRV-019 |
| DEF-F1-004 | MAJOR | El convenio acepta porcentajes fuera de rango (150 %) | Fase 5 · CHG-27 | F1-CNV-006 |
| DEF-F1-005 | MAJOR | Vehículos: placa duplicada por mayúsculas, sin validación de formato y transportadora sin rol | Fase 2 · CHG-05 | F1-VEH-002, F1-VEH-004, F1-VEH-005 |
| DEF-F1-006 | MINOR | El alta de usuario no valida que las contraseñas coincidan | Fase 8 · CHG-50 | F1-USR-006 |
| DEF-F1-007 | MINOR | Editar con identificación o SKU duplicados muestra el error crudo de Postgres; el nombre de producto se puede duplicar | Fase 8 · CHG-49 | F1-TER-008, F1-PRO-005 |
| DEF-F1-008 | MINOR | Quedan textos «Stakeholder» visibles en el alta de terceros | Fase 12 · CHG-90 | F1-TER-001, F1-TER-005 |
| DEF-F1-009 | MAJOR | Usuario desactivado, con rol retirado o deslogueado conserva acceso con su token hasta que expira | Fase 4 · CHG-16 | F1-USR-015, F1-USR-010, F1-AUT-018 |
| DEF-F1-010 | MINOR | Un Admin puede quitarse su rol o desactivarse a sí mismo, y un usuario puede quedar sin roles | Fase 8 · CHG-50 | F1-USR-010, F1-USR-012, F1-USR-017 |
| DEF-F1-011 | MINOR | Enumeración de cuentas por los mensajes de login y de recuperación | Fase 8 · CHG-51 | F1-AUT-005, F1-AUT-015 |
| DEF-F2-001 | CRITICAL | La búsqueda de placa por coincidencia parcial registra el ingreso al vehículo equivocado | Fase 2 · CHG-05 | F2-ING-007, F2-ING-010, F2-HIS-003 |
| DEF-F2-002 | MINOR | El ingreso crea vehículos con placa de formato inválido | Fase 2 · CHG-05 | F2-ING-010 |
| DEF-F2-003 | MINOR | El API acepta fecha de ingreso futura y salida anterior al ingreso | Fase 8 · CHG-52 | F2-ING-012, F2-SAL-009 |
| DEF-F2-004 | MAJOR | La trazabilidad muestra «En portería» a camiones que ya salieron | Fase 7 · CHG-42 | F2-INT-007 |
| DEF-F3-001 | CRITICAL | Las notificaciones al rol Comercio Exterior no llegan a nadie | Fase 2 · CHG-04 | F3-REG-003, F3-INT-004, F3-MCA-009 |
| DEF-F3-002 | MAJOR | Báscula sin idempotencia: dos envíos del registro o del cobro duplican depósitos, stock, ciclos y facturas | Fase 4 · CHG-17 | F3-COB-013, F3-COB-001, E2E-18, E2E-20, F10-ERR-007 |
| DEF-F3-003 | MAJOR | La hora del pesaje se propone con la del ingreso / pesaje anterior: tiquetes con horas falsas | Fase 7 · CHG-44 | F3-PES-003, F3-TIQ-002 |
| DEF-F3-004 | CRITICAL | Descartar una operación no libera el camión y permite cobrar el servicio descartado | Fase 2 · CHG-06 | F3-REC-006, F3-REC-007, F3-REC-008 |
| DEF-F3-005 | MAJOR | La salida en Vigilancia con ciclo abierto deja el ciclo atascado e invisible | Fase 6 · CHG-30 | F3-PES-016, F2-SAL-005 |
| DEF-F3-006 | MAJOR | Tras recargar, el Registro guardado se ve vacío; recargar con borradores no avisa | Fase 4 · CHG-20 | F3-REI-005, F3-REI-003 |
| DEF-F3-007 | MAJOR | El cobro no preselecciona al cliente de la operación: propone al conductor y el precio base | Fase 4 · CHG-19 | F3-COB-003 |
| DEF-F3-008 | MAJOR | Conductor y vehículo exigidos no se guardan en Solo báscula ni en Salida | Fase 7 · CHG-46 | F3-CAM-010, F3-CAM-011 |
| DEF-F3-009 | MINOR | El API de registro y cobro acepta datos que la interfaz rechaza | Fase 8 · CHG-53 | F3-REG-014, F3-COB-005 |
| DEF-F3-010 | MINOR | Un documento con ingreso de camiones cerrado se ve como «Documento nuevo» | Fase 8 · CHG-54 | F3-MCA-008 |
| DEF-F3-011 | MAJOR | «Agregar otro depósito» (multidepósito) es inalcanzable | Fase 7 · CHG-45 | F3-MUL-001..004 |
| DEF-F3-012 | MAJOR | Se puede iniciar una segunda salida con una orden de cargue que ya tiene salida activa | Fase 6 · CHG-32 | F3-SAL-009, F3-SAL-008 |
| DEF-F3-013 | MAJOR | Historial: «Cambiar modo de pago» da 404 y el operario de báscula no ve «Editar peso» | Fase 7 · CHG-47 | F3-HIS-008, F3-COR-002 |
| DEF-F3-014 | MAJOR | Se acepta una tara mayor que el bruto (neto negativo) sin advertencia | Fase 6 · CHG-37 | F3-PES-007 |
| DEF-F3-015 | MINOR | Historial y dashboard: pesos de operaciones de un pesaje no se muestran y los conteos no cuadran | Fase 11 · CHG-76 | F3-HIS-001, F3-HIS-005, F3-DSH-001 |
| DEF-F3-016 | MAJOR | La búsqueda de vehículo por placa en báscula devuelve el duplicado inactivo (`qaa101`) | Fase 2 · CHG-05 | F3-SAL-011 |
| DEF-F3-017 | MAJOR | Solo báscula retomada tras recargar se cobra como depósito y el ciclo queda sin factura | Fase 4 · CHG-20 | F3-REI-010 |
| DEF-F3-018 | MINOR | El registro guardado se muestra en campos editables sin forma de guardar los cambios | Fase 4 · CHG-20 | F3-REI-009 |
| DEF-F3-019 | MINOR | El API de cobro conserva efectivo recibido y cambio, que el negocio decidió eliminar | Fase 8 · CHG-53 | F3-COB-012 |
| DEF-F4-001 | CRITICAL | La recepción de depósitos con unidades de carga es imposible | Fase 2 · CHG-07 | F4-RUC-001, F4-RUC-002, F4-RUC-004 |
| DEF-F4-002 | CRITICAL | La recepción directa sin báscula falla siempre desde la interfaz (500) | Fase 2 · CHG-08 | F4-RSB-002 |
| DEF-F4-003 | MAJOR | Báscula permite el segundo pesaje sin la llegada registrada en Bodega; esas entradas quedan sin recepción | Fase 6 · CHG-36 | F4-REC-001, F4-REC-017, F4-REC-019 |
| DEF-F4-004 | MAJOR | Se ejecuta un cargue sobre un depósito devuelto a Borrador | Fase 6 · CHG-31 | F4-CAR-014 |
| DEF-F4-005 | MAJOR | La recepción directa crea ingresos abiertos duplicados para el mismo vehículo | Fase 2 · CHG-08 | F4-RSB-007 |
| DEF-F4-006 | MAJOR | El detalle de un depósito de exportación cerrado da 404 y desaparece de la lista | Fase 7 · CHG-43 | F4-CAR-009 |
| DEF-F4-007 | MINOR | Historial de recepciones: filtrar un solo día no devuelve nada y el API da 500 con fecha local | Fase 11 · CHG-77 | F4-REC-015 |
| DEF-F4-008 | MINOR | Exportar movimientos a Excel solo incluye la primera página | Fase 11 · CHG-78 | F4-INV-003 |
| DEF-F4-009 | MINOR | La recepción acepta más de 5 fotos y archivos que no son imagen | Fase 8 · CHG-55 | F4-REC-009 |
| DEF-F4-010 | MINOR | Un producto declarado y no contado no genera aviso y el historial dice «Sin diferencia» | Fase 8 · CHG-56 | F4-REC-012 |
| DEF-F4-011 | MINOR | Las novedades no validan que las cantidades cuadren con el total | Fase 8 · CHG-57 | F4-NOV-006 |
| DEF-F4-012 | MINOR | El API ejecuta cargues sin firma y toma el responsable del cliente | Fase 4 · CHG-15 | F4-CAR-010 |
| DEF-F4-013 | MINOR | Montacargas: el API acepta horómetro inicial 0 y final igual al inicial | Fase 8 · CHG-58 | F4-MON-004, F4-MON-006 |
| DEF-F4-014 | MINOR | Reejecutar una orden ya cargada da un mensaje erróneo (404 de reserva) | Fase 6 · CHG-31 | F4-CAR-007 |
| DEF-F4-015 | MINOR | Las tarjetas de pendientes de Bodega muestran «kg (Invalid Date)» | Fase 10 · CHG-75 | F4-REC-001 |
| DEF-F4-016 | MINOR | El historial de montacargas no muestra horómetros, valor, modo de pago ni factura | Fase 8 · CHG-58 | F4-MON-014 |
| DEF-F4-017 | TRIVIAL | Montacargas: mensajes técnicos al iniciar sin servicio | Fase 8 · CHG-58 | F4-MON-012 |
| DEF-F4-018 | MINOR | El inventario de Bodega no muestra depósitos en Borrador con mercancía recibida | Fase 10 · CHG-74 | F4-INV-001 |
| DEF-F5-001 | MAJOR | En Borrador no se pueden editar fecha del documento, moneda ni valor: la tarjeta «Información General» queda en blanco | Fase 4 · CHG-21 | F5-CNF-001 |
| DEF-F5-002 | MAJOR | El ajuste CE-7 y la corrección de productos cambian el stock sin registrar movimiento de inventario | Fase 6 · CHG-39 | F5-AJU-001, F5-PRD-001, F5-PRD-002 |
| DEF-F5-003 | MAJOR | El ajuste CE-7 envía el correo antes de validar; si el SMTP falla, responde 500 | Fase 6 · CHG-38 | F5-AJU-004 |
| DEF-F5-004 | MAJOR | El ajuste CE-7 permite dejar el recibido por debajo de lo ya levantado (pendiente por nacionalizar negativo) | Fase 6 · CHG-38 | F5-AJU-005 |
| DEF-F5-005 | MAJOR | Se aceptan levantes en depósitos anulados, que se ven «Nacionalizado», imprimen etiqueta y muestran «Registrar levante» en Borrador | Fase 6 · CHG-40 | F5-LEV-012, F5-LEV-013, F5-ETI-006 |
| DEF-F5-006 | MINOR | El tablero de CE cuenta anulados y «Guías pendientes» abre el historial | Fase 7 · CHG-43 | F5-TAB-002, F5-TAB-003 |
| DEF-F5-007 | MINOR | Kanban paginado en conjunto y cantidades que suman unidades distintas | Fase 10 · CHG-69 | F5-LIS-001, F5-ETI-007 |
| DEF-F5-008 | MINOR | «Validar depósito» compara solo el peso del último ciclo | Fase 10 · CHG-70 | F5-VAL-003, F5-VAL-001 |
| DEF-F5-009 | MINOR | Filtros de órdenes de cargue por documento comercial, importador y manifiesto DIAN no devuelven nada | Fase 10 · CHG-71 | F5-OC-019 |
| DEF-F5-010 | MINOR | Datos de terceros y producto incorrectos en guía, factura y etiqueta | Fase 10 · CHG-73 | F5-GUI-003, F5-INT-001 |
| DEF-F5-011 | MINOR | El cobro de la guía no muestra el total y el formulario tiene textos obsoletos | Fase 6 · CHG-34 | F5-GUI-002 |
| DEF-F5-012 | MINOR | El «Responsable» de la recepción en el detalle de CE es el usuario de Vigilancia | Fase 10 · CHG-72 | F5-CNF-001 (detalle) |
| DEF-F5-013 | TRIVIAL | Mensajes con el estado en inglés y textos equivocados por modalidad | Fase 12 · CHG-90 | F5-CNF-009, F5-COR-003, F5-GUI-008 |
| DEF-F5-014 | MAJOR | Mercancía de importación despachada sin guía de salida | Fase 6 · CHG-33 | F5-GUI-003 (OBS-F5-001), F3-SAL-*, F4-CAR-001/003/008 |
| DEF-F6-001 | CRITICAL | La tarifa de almacenamiento se toma de otra modalidad: el convenio IMP cobra EXP e INSP y la tarifa base EXP cobra INSP | Fase 3 · CHG-09 | F6-TAR-004, F6-TAR-007, F6-INV-011, F6-ACC-005 |
| DEF-F6-002 | CRITICAL | El cierre manual de períodos abre el nuevo con la misma fecha de inicio: doble cobro del mismo período | Fase 3 · CHG-10 | F6-ALM-008, F6-FOR-005 |
| DEF-F6-003 | CRITICAL | El override de una línea con cantidad > 1 multiplica el monto por la cantidad y suma IVA | Fase 3 · CHG-11 | F6-OVR-003 |
| DEF-F6-004 | CRITICAL | El override muestra el total con IVA como «Monto original» pero aplica el valor digitado como neto + IVA | Fase 3 · CHG-11 | F6-OVR-002, F6-OVR-004 |
| DEF-F6-005 | CRITICAL | Los cargos «por facturar» vencen el mismo instante en que se crean y quedan atascados en Overdue | Fase 3 · CHG-12 | F6-CAR-005, F6-CON-003, F6-INV-008 |
| DEF-F6-006 | CRITICAL | Mora: las facturas con pago parcial nunca quedan vencidas y el bloqueo tarda 3 corridas diarias | Fase 3 · CHG-13 | F6-CAR-001, F6-CAR-002, F6-CAR-003 |
| DEF-F6-007 | MAJOR | El piso por unidad de carga provoca una falsa «magnitud facturada dos veces» y cae al mínimo de la modalidad | Fase 5 · CHG-25 | F6-FOR-013 |
| DEF-F6-008 | MINOR | El ciclo OnDemand se ofrece pero no factura el almacenamiento (retirarlo de las opciones) | Fase 9 · CHG-60 | F6-ALM-006 |
| DEF-F6-009 | MAJOR | Se registran pagos en borradores y el buscador de pagos lista facturas no pagables con «null» | Fase 5 · CHG-22 | F6-PAG-010, F6-PAG-007 |
| DEF-F6-010 | MAJOR | El comprobante del pago no se puede guardar (varchar(500)) | Fase 5 · CHG-29 | F6-PAG-008 |
| DEF-F6-011 | MAJOR | La creación manual de facturas sigue expuesta (pantalla y API) | Fase 5 · CHG-28 | F6-INV-020 |
| DEF-F6-012 | MAJOR | Las reglas para perecederos (WMS-32) no se pueden configurar | Fase 5 · CHG-26 | F6-TAR-009 |
| DEF-F6-013 | MAJOR | Se puede anular una factura con pagos; el dinero queda en la anulada | Fase 5 · CHG-22 | F6-ACC-018 |
| DEF-F6-014 | MINOR | No se puede quitar el límite de crédito | Fase 9 · CHG-61 | F6-CFG-006 |
| DEF-F6-015 | MINOR | El PATCH de un servicio de convenio borra los campos omitidos (producto y modalidad) | Fase 5 · CHG-26 | F6-FOR-013 (preparación) |
| DEF-F6-016 | MINOR | Las previsualizaciones de fórmula no coinciden con el cobro real | Fase 9 · CHG-64 | F6-PRE-001, F6-PRE-002, F6-PRE-003 |
| DEF-F6-017 | MINOR | No existe la consolidación diaria de cargos por facturar | Fase 9 · CHG-63 | F6-CON-001 |
| DEF-F6-018 | MINOR | Jobs: el aviso de vencimiento se duplica en cada corrida y la renovación manual no avisa | Fase 9 · CHG-62 | F6-JOB-002, F6-CAR-011, F6-ALM-008 |
| DEF-F6-019 | MINOR | Un método de pago inválido produce 500 NullReference | Fase 8 · CHG-48 | F6-PAG-006 |
| DEF-F6-020 | TRIVIAL | Mensajes de facturación técnicos o confusos | Fase 12 · CHG-90 | F6-ACC-008, F6-REF-003 |
| DEF-F6-021 | MAJOR | El tratamiento del IVA en los mínimos de almacenamiento no es configurable | Fase 5 · CHG-24 | F6-ALM-010, F6-FOR-013, F6-FOR-014 |
| DEF-F6-022 | MAJOR | No se puede asignar N.º SIIGO a facturas de contado ya pagadas | Fase 5 · CHG-23 | F6-ACC-017 |
| DEF-F7-001 | CRITICAL | La auditoría guarda el PasswordHash y el SecurityStamp de los usuarios | Fase 1 · CHG-02 | F7-AUD-006 |
| DEF-F7-002 | MAJOR | Trazabilidad: los camiones que salen siguen «En portería» y hay etapas «Desconocido» | Fase 7 · CHG-42 | F7-TRZ-001, F7-TRZ-005 |
| DEF-F7-003 | MINOR | El reporte de salidas diarias omite despachos sin guía | Fase 11 · CHG-79 | F7-REP-003 |
| DEF-F7-004 | MINOR | Ingresos diarios: peso neto en 0 y placa/tiquete vacíos | Fase 11 · CHG-82 | F7-REP-001 |
| DEF-F7-005 | MINOR | Inventario general como Comercio Exterior muestra «Error 403 Error interno del servidor» | Fase 1 · CHG-03 | F7-REP-016 |
| DEF-F7-006 | MINOR | Las exportaciones a Excel escriben las fechas en UTC | Fase 11 · CHG-83 | F7-REP-019 |
| DEF-F7-007 | MINOR | Facturación por CPI pierde la factura anulada tras refacturar | Fase 9 · CHG-65 | F7-REP-022 |
| DEF-F7-008 | MINOR | Catálogos sin auditoría | Fase 9 · CHG-68 | F7-AUD-004 |
| DEF-F7-009 | MINOR | Kárdex: la pantalla y el Excel no muestran las líneas de movimiento | Fase 11 · CHG-78 | F7-REP-012, F7-REP-013 |
| DEF-F7-010 | MINOR | Trazabilidad: «Hoy» en UTC, placa sensible a mayúsculas y aviso con título técnico | Fase 11 · CHG-81 | F7-TRZ-002, F7-TRZ-003, F7-NOT-008 |
| DEF-F7-011 | MINOR | Documentos impresos: detalle del depósito ausente, teléfono 0 y datos de empresa inconsistentes | Fase 11 · CHG-84 | F7-PDF-001, F7-PDF-004, F7-PDF-007 |
| DEF-F7-012 | MINOR | El API de estadísticas entrega el bloque de facturación a Comercio Exterior | Fase 11 · CHG-80 | F7-TRZ-006 |
| DEF-F8-001 | MAJOR | [UNIFICADO EN DEF-F3-002] Báscula sin idempotencia: dos envíos simultáneos del registro o del cobro duplican depósitos, stock, ciclos y facturas | Duplicado de DEF-F3-002 | E2E-18, E2E-20 |
| DEF-F8-002 | MAJOR | La guía de una orden multi-cliente se factura entera al primer cliente | Fase 6 · CHG-34 | E2E-10 |
| DEF-F8-003 | MAJOR | Tras la salida con el tiquete de ingreso, la OC queda Dispatched al cargar y ya no se puede emitir la guía | Fase 6 · CHG-33 | E2E-17 |
| DEF-F8-004 | MAJOR | Al reimprimir una guía de salida aparece el levante de otra salida | Fase 6 · CHG-35 | E2E-02 |
| DEF-F8-005 | MAJOR | La recepción sin báscula crea el depósito de inspección ya Confirmado, sin revisión de Comercio Exterior y con factura en $0 | Fase 2 · CHG-08 | E2E-08, E2E-12 |
| DEF-F8-006 | MINOR | El detalle de la factura de almacenamiento usa la cantidad declarada y no la ajustada | Fase 9 · CHG-66 | E2E-02 |
| DEF-F8-007 | MINOR | Anular un depósito no avisa a Bodega ni a Facturación | Fase 9 · CHG-67 | E2E-11 paso 6 |
| DEF-F8-008 | MINOR | La OC sigue Pending durante la salida por báscula (no pasa a «en cargue») | Fase 6 · CHG-32 | E2E-01 paso 10 |
| DEF-F8-009 | MINOR | Reporte diario de báscula: una inspección de pesaje único se rotula «Solo Pesaje» | Fase 11 · CHG-76 | E2E-20 |
| DEF-F9-001 | CRITICAL | Cualquier usuario autenticado puede crear y editar terceros, convenios y tarifas, motivos de ingreso, conductores, vehículos y productos | Fase 1 · CHG-03 | F9-API-010, 011, 012, 013, 014, 015 |
| DEF-F9-002 | MAJOR | Vigilancia y Bodega se cruzan: Vigilancia entra a las páginas y al API de Bodega, y Bodega registra ingresos y salidas de Vigilancia | Fase 1 · CHG-03 | F9-MEN-004, F9-PAG-004, F9-API-019 |
| DEF-F9-003 | MAJOR | El API guarda como autor el usuario que envía el cliente (autorizó la salida, autorizó la recepción, completó el cargue) y la firma del cargue no es obligatoria | Fase 4 · CHG-15 | F9-API-020 |
| DEF-F9-004 | MINOR | Facturación no puede abrir el reporte de inventario general en la interfaz | Fase 1 · CHG-03 | F9-PAG-002 |
| DEF-F9-005 | MINOR | Datos sensibles legibles por roles operativos: tarifas de convenios, simulación de facturas, inventario general y kárdex | Fase 1 · CHG-03 | F9-API-021, F9-PAG-* |
| DEF-F9-006 | MINOR | Un cuerpo JSON mal formado devuelve 500 con el texto interno de la excepción | Fase 8 · CHG-48 | F9-API-* (sondeo) |
| DEF-F10-001 | MAJOR | Acciones sin protección contra doble envío (recepción sin báscula, verificar/rechazar pago, crear OC, emitir guía, registrar pago con comprobante, N.º con Enter) y «Rechazar pago» sin confirmación | Fase 4 · CHG-18 | F10-ERR-007, F10-UX-003 |
| DEF-F10-002 | MINOR | El formulario de pago borra el monto y la referencia cuando el backend rechaza el pago | Fase 4 · CHG-18 | F10-UX-005, F10-ERR-006 |
| DEF-F10-003 | MINOR | Los errores de negocio se muestran duplicados (aviso global + aviso del componente + texto en línea) | Fase 12 · CHG-86 | F10-ERR-003, F10-ERR-005, F10-ERR-006 |
| DEF-F10-004 | MINOR | Con el API caído se apilan avisos «Error 500 / Error de conexión con el servidor» que tapan la pantalla | Fase 12 · CHG-86 | F10-ERR-001 |
| DEF-F10-005 | MINOR | Callejones sin salida: factura inexistente con spinner infinito, ID mal formado como «Error interno», 404 de ruta en inglés | Fase 12 · CHG-87 | F10-ERR-005, F10-UX-010 |
| DEF-F10-006 | MINOR | Formatos inconsistentes: báscula usa separador de miles estadounidense y hay cuatro formatos de fecha | Fase 12 · CHG-88 | F10-UI-005 |
| DEF-F10-007 | MINOR | Textos en inglés, técnicos o con errores: «Stakeholder», «role», validación de archivo de PrimeVue, estados en inglés en mensajes del backend | Fase 12 · CHG-90 | F10-UI-006, F10-UX-012, F10-ERR-010, F10-ERR-013 |
| DEF-F10-008 | MINOR | Accesibilidad: botones de solo ícono sin tooltip ni etiqueta, campos sin label asociado y el foco no va al primer error | Fase 12 · CHG-89 | F10-UI-008, F10-ACC-001, F10-UX-004 |

**Conteo por destino**

| Destino | Fichas |
|---|---|
| Fase 1 | 6 |
| Fase 2 | 10 |
| Fase 3 | 6 |
| Fase 4 | 12 |
| Fase 5 | 11 |
| Fase 6 | 16 |
| Fase 7 | 9 |
| Fase 8 | 16 |
| Fase 9 | 9 |
| Fase 10 | 7 |
| Fase 11 | 11 |
| Fase 12 | 12 |
| Duplicado de DEF-F3-002 | 1 |
| Corregido en un commit posterior a QA (solo re-test) | 0 |
| Cerrado por §10 | 0 |
| **Total** | **126** |

**Severidad por fase**

| Fase | CRITICAL | MAJOR | MINOR | TRIVIAL |
|---|---|---|---|---|
| 1 | 2 | 1 | 3 | 0 |
| 2 | 5 | 4 | 1 | 0 |
| 3 | 6 | 0 | 0 | 0 |
| 4 | 0 | 9 | 3 | 0 |
| 5 | 0 | 10 | 1 | 0 |
| 6 | 0 | 13 | 3 | 0 |
| 7 | 0 | 8 | 1 | 0 |
| 8 | 0 | 0 | 15 | 1 |
| 9 | 0 | 0 | 9 | 0 |
| 10 | 0 | 0 | 7 | 0 |
| 11 | 0 | 0 | 11 | 0 |
| 12 | 0 | 0 | 10 | 2 |

## 4. Fases

### Cuadro de seguimiento de fases

Marcar la columna «Estado» al cerrar cada fase (checkpoint aprobado y commits hechos por el usuario). Valores: **Pendiente**, **En curso**, **En re-test**, **Completada**. La complejidad sale del tamaño de los cambios (S/M/L), su riesgo de regresión y si hay migración o concurrencia. «Modelo sugerido» es el mínimo recomendado para implementar la fase; los cambios S de texto o validación de una fase pueden delegarse a un modelo menor, y el diseño de transacciones, concurrencia y dinero conviene dejarlo siempre al modelo mayor.

| Fase | Tema | Severidad | Cambios | Tamaños (S/M/L) | Riesgo mayor | Migración | Complejidad | Modelo sugerido | Estado |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Seguridad crítica e infraestructura de pruebas | CRITICAL | CHG-01 a 03 | 1 / 1 / 1 | Medio | No | Alta | Opus 5.5 | Completada |
| 2 | Operación crítica: portería, avisos, báscula y recepción | CRITICAL | CHG-04 a 08 | 2 / 2 / 1 | Medio | Sí | Alta | Opus 5.5 | Completada |
| 3 | Facturación crítica: lo que se cobra | CRITICAL | CHG-09 a 13 | 2 / 3 / 0 | Medio | No | Alta (dinero) | Opus 5.5 | Completada |
| 4 | MAJOR de seguridad y del cobro en báscula | MAJOR | CHG-14 a 21 | 2 / 4 / 2 | Medio-alto | Sí | Muy alta (concurrencia) | Opus 5.5 | Completada |
| 5 | MAJOR de dinero: pagos, mínimos y reglas de tarifas | MAJOR | CHG-22 a 29 | 4 / 4 / 0 | Medio | Sí (2) | Media-alta | Sonnet 5.5 (CHG-24, 25 y 26 con Opus 5.5) | Completada |
| 6 | MAJOR de inventario y salidas sin guía | MAJOR | CHG-30 a 40 | 2 / 6 / 3 | Alto | Sí | Muy alta | Opus 5.5 | Completada |
| 7 | MAJOR restantes: productos, trazabilidad y báscula | MAJOR | CHG-41 a 47 | 5 / 2 / 0 | Bajo | No | Baja-media | Sonnet 5.5 | Completada |
| 8 | MINOR de validación y reglas en el servidor | MINOR | CHG-48 a 59 | 8 / 4 / 0 | Bajo | No | Media (muchos archivos) | Sonnet 5.5 (los S pueden ir con Haiku 4.5) | Completada |
| 9 | MINOR de facturación, avisos y auditoría | MINOR | CHG-60 a 68 | 7 / 2 / 0 | Medio | Sí | Media | Sonnet 5.5 | Completada |
| 10 | MINOR de Comercio Exterior e inventario de Bodega | MINOR | CHG-69 a 75 | 1 / 5 / 1 | Medio | Sí | Media | Sonnet 5.5 | Completada |
| 11 | MINOR de reportes, fechas y documentos impresos | MINOR | CHG-76 a 84 | 2 / 6 / 1 | Medio | Sí | Media | Sonnet 5.5 | Completada |
| 12 | MINOR y TRIVIAL de interfaz, avisos, formatos y textos | MINOR/TRIVIAL | CHG-85 a 90 | 1 / 2 / 3 | Medio | No | Media (mecánica, ~100 archivos) | Sonnet 5.5 | Completada |

Los tamaños son los de las tarjetas (S ≈ medio día, M ≈ 1 a 2 días, L ≈ 3 a 5 días). Antes de pasar a la fase siguiente, el estado de la fase anterior debe ser **Completada**.

### 4.0 Reglas comunes a todas las fases

1. **Repositorios y commits.** Se trabaja en `develop` de los dos repositorios, sin ramas. El implementador no ejecuta `git add`, `commit`, `push` ni `merge`; el usuario hace los commits al cerrar cada fase (DF1 del plan de paridad).
2. **Migraciones y base de datos** (decisión del usuario, 4-oct-2026). El implementador de la fase cambia entidad, configuración y `HasData` y, cuando la fase lo requiere, **genera, aplica, revierte o elimina** él mismo, siempre con comandos `dotnet ef` desde `Backend/wms-api`:
   - Generar: `dotnet ef migrations add <NombreDeLaFase> --project Wms.Infrastructure --startup-project Wms.Api`, con el nombre que indica la fase.
   - Aplicar: `dotnet ef database update --project Wms.Infrastructure --startup-project Wms.Api`.
   - Recrear la base: `dotnet ef database drop --force --project Wms.Infrastructure --startup-project Wms.Api` seguido de `dotnet ef database update …`.
   - Rehacer una migración propia antes del commit: `dotnet ef migrations remove --project Wms.Infrastructure --startup-project Wms.Api` y volver a generarla.
   - **Única restricción: ningún archivo generado se edita a mano** (`Wms.Infrastructure/Migrations/*`, incluidos `*.Designer.cs` y `AppDbContextModelSnapshot.cs`). Si la migración generada no es la esperada, se corrige el modelo y se regenera. Tampoco se modifica la base con SQL manual: todo cambio de esquema o de datos sembrados pasa por el modelo y `dotnet ef`.
   - Alcance: solo la base local de pruebas que apunta `Wms.Api` en Development. Staging y producción quedan fuera; ahí se despliega con el procedimiento existente (`scripts/deploy-staging.sh`) y con aprobación del usuario.
   - Una columna nueva `NOT NULL` en una tabla con `HasData` no lleva `HasDefaultValue` (falla del 1-oct-2026 con la migración de paridad). Antes de terminar la fase, `dotnet ef migrations has-pending-model-changes` no debe reportar cambios pendientes y la migración va en el mismo commit que el código.
3. **Saneamiento de datos.** Cada script vive en `Backend/wms-api/scripts/saneamiento-qa/fase-NN-<tema>.sql` y tiene dos bloques: detección (solo `SELECT`) y corrección (`BEGIN … COMMIT`). Se ejecuta en la base local y en staging, nunca en producción sin aprobación escrita del usuario. Si el usuario recrea la base antes de la fase 11 (§7), el bloque de corrección de la base local se omite y la detección se conserva como verificación (debe devolver 0 filas). Decisión del 3-oct-2026: las bases de local y staging son de prueba y se recrean con cada migración de fase; los bloques de corrección no se escriben ni se ejecutan mientras no haya datos reales, y solo se conserva la detección. Los scripts de la Fase 1 ya entregados se pueden descartar.
4. **Compuertas de salida comunes.** Toda fase cierra con: `dotnet build` sin errores; `dotnet test` de `Wms.Tests` y de `Wms.IntegrationTests` (con Docker) en verde; `yarn build` con código 0; `yarn test` en verde; errores de lint del frontend iguales o menores que al cierre de la fase anterior (punto de partida 296: `yarn lint` mide 295 errores el 4-oct-2026, con `typescript` y el script `lint` agregados al proyecto; los 397-398 que midieron las Fases 1 y 2 salieron de una instalación de `typescript` fuera del proyecto y no son la referencia) y cero en archivos nuevos; los casos QA de re-test de la fase en PASA y la suite REG indicada.
5. **Orden por severidad.** Un defecto de menor severidad entra en una fase anterior solo cuando lo cierra el mismo cambio que corrige un defecto de esa fase (misma causa raíz o mismo comportamiento en el mismo código).
6. **Archivos compartidos.** Dentro de una fase, los cambios que tocan el mismo archivo se implementan uno detrás de otro en el «Orden interno» de la fase. Entre fases, cada fase parte del código que dejó la anterior.
7. **Convenciones.** Errores de negocio con `BadRequestException`, `ConflictException` o `NotFoundException` y mensaje en español; fechas de negocio con `ColombiaTime`; en el frontend, `usePermissions` con import explícito, invalidación del prefijo de la consulta tras cada mutación y `all=true` para listas completas; estados siempre traducidos al español en mensajes y pantallas.
8. **Identidad del autor.** Desde CHG-08 existe `ClaimsPrincipalExtensions.GetRequiredUserId()` (`Wms.Application/Common/Identity/`): devuelve el `Guid` de `ClaimTypes.NameIdentifier` o lanza `UnauthorizedException("No se pudo obtener la información del usuario autenticado")`. Ningún cambio de este plan acepta el autor de una operación desde el cuerpo de la petición.
9. **Pruebas.** Las pruebas unitarias siguen el patrón del repositorio: la regla se extrae a una clase pura en `Wms.Application` o `Wms.Domain` y se prueba en `Wms.Tests`. Lo que depende de EF, índices o transacciones se prueba en `Wms.IntegrationTests` (CHG-01). El frontend se prueba con Vitest en `test/`.
10. **Sin retrocesos funcionales** (instrucción del usuario, 3-oct-2026). Ningún cambio quita a un rol una función que hoy usa en sus pantallas y que debe conservar. Cuando el §10 restringe un permiso, la restricción cierra el acceso a quien no usa la función, nunca a quien la usa en su flujo. Antes de restringir una política, el cambio lista las pantallas que llaman al endpoint y sus roles; si un rol pierde algo que usa, el rol se incluye en la política. Los accesos que el §10 manda cerrar (Vigilancia en Bodega, Bodega en portería) son la corrección del defecto, no un retroceso.

### Fase 1 — Seguridad crítica e infraestructura de pruebas

- **Objetivo:** cerrar los dos CRITICAL de seguridad (DEF-F7-001, hashes de contraseña en la auditoría; DEF-F9-001, escrituras de catálogos abiertas a cualquier usuario autenticado) junto con los defectos que tienen la misma causa (la matriz de políticas y de páginas por rol: DEF-F9-002, DEF-F9-004, DEF-F9-005 y DEF-F7-005), y dejar lista la infraestructura de pruebas que usan todas las fases.
- **Criterio de entrada:** el usuario aprobó este plan; HEAD en `191d4b1` (backend) y `cd121d8` (frontend); Docker disponible en el equipo donde corren las pruebas de integración.
- **Cambios:** CHG-01, CHG-02, CHG-03.
- **Orden interno:** CHG-01 → CHG-02 → CHG-03. Las pruebas de autorización por reflexión de CHG-03 necesitan la referencia a `Wms.Api` que agrega CHG-01.
- **Riesgos y mitigación:**
  - Un rol pierde una pantalla o un endpoint que usaba de forma legítima (403). Mitigación: el inventario de llamadas de Vigilancia está verificado (solo usa `entry-logs`, `departure-authorizations`, `manifests`, `vehicles`, `drivers`, catálogos y `weighbridge/*` de lectura); `ControllerAuthorizationTests` fija la matriz; se repite el sondeo completo del API del anexo F9 (menos de un minuto).
  - Una política nueva podría dejar sin una función a un rol que la usa (regla 4.0.10). Mitigación: CHG-03 se verificó contra las pantallas que llaman cada endpoint restringido: las escrituras de terceros, productos y motivos solo las usan páginas que hoy ya son exclusivas del Admin; las de conductores y vehículos las usan Vigilancia (ingreso), Comercio Exterior (orden de cargue) y el Admin, y los tres quedan en `TransportCatalogAccess`; las páginas de portería solo son de Admin y Vigilancia.
  - Las copias de respaldo hechas antes del saneamiento conservan los hashes. Mitigación: el saneamiento se ejecuta en local y staging; las copias previas de staging no se restauran en otro ambiente.
- **Saneamiento de datos:** `fase-01-auditoria.sql` (corrección) y `fase-01-escrituras-sin-rol.sql` (solo detección), descritos en cada cambio.
- **Criterio de salida:** compuertas comunes (regla 4.0.4) y en PASA: F11-AUT-001, F11-AUT-002, F7-AUD-006, F7-AUD-002, F9-API-010, F9-API-011, F9-API-012, F9-API-013, F9-API-014, F9-API-015, F9-API-016, F9-API-019, F9-API-021, F9-MEN-004, F9-PAG-002, F9-PAG-004, F9-PAG-020, F7-REP-016, F10-ERR-004; REG F11-REG-002, F11-REG-003, F11-REG-004, F11-REG-027, F11-REG-028, F11-REG-031.
- **Checkpoint:** se entrega al usuario la matriz resultante (rol × escritura de catálogo y rol × página), el resultado del sondeo del API con las 9 cuentas y el número de filas saneadas en `audit_logs`. El usuario aprueba: (1) la matriz, en la que ningún rol pierde una función que usa hoy (regla 4.0.10); (2) la ejecución del saneamiento de auditoría en staging.

#### CHG-01 — Infraestructura de pruebas automatizadas

- **Cierra:** ningún defecto. Habilita las pruebas de los demás cambios.
- **Causa raíz:** `Wms.Tests/Wms.Tests.csproj:22-24` solo referencia `Wms.Application`, `Wms.Domain` y `Wms.Common`: no hay pruebas de autorización (controladores) ni de base de datos (índices, transacciones, consultas EF). En el frontend, `package.json` no tiene framework de pruebas (sin vitest, jest ni playwright) y no existe ningún `*.spec.ts`.
- **Cambio exacto:**
  - Backend:
    1. `Wms.Tests/Wms.Tests.csproj`: agregar `ProjectReference` a `..\Wms.Api\Wms.Api.csproj` y `..\Wms.Infrastructure\Wms.Infrastructure.csproj` (pruebas por reflexión de controladores y de clases puras de Infrastructure).
    2. `Wms.Api/Program.cs`: agregar al final `public partial class Program;` (punto de entrada para `WebApplicationFactory`).
    3. Proyecto nuevo `Wms.IntegrationTests` en `Wms.sln`: xUnit 2.9.3 (la versión de `Wms.Tests`), `Microsoft.AspNetCore.Mvc.Testing` 10.0.x y `Testcontainers.PostgreSql` 4.x. Clase `WmsApiFactory : WebApplicationFactory<Program>, IAsyncLifetime`: arranca un contenedor `postgres:18.0` (la imagen del ambiente local) y aplica la migración vigente con `Database.MigrateAsync()`; fija configuración de prueba en memoria (cadena de conexión del contenedor, `Jwt:Key` aleatoria de 64 caracteres generada en la prueba, `Jwt:Issuer` y `Jwt:Audience` = `wms-tests`, `Jwt:AccessTokenExpirationMinutes` = 60, `Bootstrap:AdminPassword` aleatoria); en `ConfigureTestServices` retira por tipo los 6 servicios de fondo de `Program.cs:61-66` y reemplaza el envío de correo e `IDianTrmService` por dobles en memoria. Método `CreateClientForRoleAsync(params SystemRolesCode[] roles)`: crea un usuario de prueba con esos roles mediante `UserManager` (contraseña aleatoria, `MustChangePassword = false`) y devuelve un `HttpClient` con el token de `POST /api/v1/auth/login`. Todas las pruebas del proyecto llevan `[Trait("Category", "Integration")]`.
  - Frontend:
    1. `package.json`: devDependencies `vitest`, `@nuxt/test-utils`, `@vue/test-utils` y `happy-dom` (versiones compatibles con Nuxt 4.2), script `"test": "vitest run"`; instalación con `yarn` (gestor declarado en `packageManager`).
    2. `vitest.config.ts` con `defineVitestConfig` (entorno `happy-dom`, `include: ["test/**/*.spec.ts"]`); las pruebas de componentes que necesitan el contexto de Nuxt declaran `// @vitest-environment nuxt`.
    3. Carpetas `test/unit/` (utilidades, esquemas y composables puros) y `test/components/` (componentes). Ninguna prueba vive dentro de `app/`.
  - No se toca: las pruebas existentes de `Wms.Tests` (siguen en verde) ni el código de producción, salvo la línea de `Program.cs`.
- **Migración o script:** ninguno.
- **Pruebas automatizadas nuevas:** `Wms.IntegrationTests/Smoke/ApiSmokeTests.cs` → `Login_InvalidCredentials_Returns400WithMessage` (cuerpo con «Credenciales inválidas») y `UserMe_WithAdminToken_Returns200`; `test/unit/utils/role-routes.spec.ts` → `getDefaultRouteForRoles(["Billing"])` devuelve `/billing` y `getDefaultRouteForRoles(["Scale", "ForeignTrade"])` devuelve `/`.
- **Criterios de aceptación:**
  - Dado el repositorio del backend con Docker disponible, cuando se ejecuta `dotnet test`, entonces corren `Wms.Tests` y `Wms.IntegrationTests` y todas las pruebas pasan.
  - Dado el repositorio del backend sin Docker, cuando se ejecuta `dotnet test --filter Category!=Integration`, entonces corren y pasan todas las pruebas unitarias.
  - Dado el frontend, cuando se ejecuta `yarn test`, entonces Vitest ejecuta `test/**/*.spec.ts` y termina con código 0; y `yarn build` termina con código 0.
- **Re-test QA:** F11-AUT-001, F11-AUT-002.
- **Riesgo de regresión:** bajo; `Program.cs` solo gana la declaración parcial.
- **Tamaño:** M. **Dependencias:** ninguna.

#### CHG-02 — La auditoría no guarda secretos ni campos sin cambio

- **Cierra:** DEF-F7-001 (CRITICAL).
- **Causa raíz:** `Wms.Infrastructure/Persistence/AppDbContext.cs:139-216` (`CollectAuditEntries`, llamado desde `SaveChangesAsync` en `:124-137`) serializa en `Added` todas las propiedades no nulas (`:173-180`), en `Modified` todas las marcadas `IsModified` (`:181-189`) y en `Deleted` todas (`:190-196`), sin lista de exclusión. `ApplicationUser : IdentityUser<Guid>, IAuditable` (`Wms.Domain/Entities/Users/ApplicationUser.cs:8`) trae `PasswordHash`, `SecurityStamp` y `ConcurrencyStamp`, y `UserStore.UpdateAsync` de Identity marca todas las propiedades como modificadas: cada actualización de usuario copia el hash en `previous_value` y `new_value`. `ReceptionLog.SignatureDriver` (`ReceptionLog.cs:12`, base64 de hasta 500 000 caracteres) también se copia.
- **Cambio exacto:**
  - Backend: nueva clase pura `Wms.Infrastructure/Persistence/AuditPayloadBuilder.cs` con la lista de propiedades excluidas `PasswordHash`, `SecurityStamp`, `ConcurrencyStamp` y `SignatureDriver`, y los métodos `ForCreate`, `ForUpdate` y `ForDelete` sobre `AuditProperty(Name, Original, Current, IsModified)`. `CollectAuditEntries` la usa: en `Added` y `Deleted` omite las excluidas; en `Modified` incluye solo las propiedades `IsModified` cuyo valor cambió (`!Equals(Original, Current)`) y no excluidas; si no queda ninguna y `auditContext.Description` es nulo, no escribe la fila.
  - Frontend: ninguno.
  - No se toca: la entidad `AuditLog` y sus columnas, `UtcDateTimeOffsetNormalizer` ni la pantalla `/admin/audit`.
- **Migración o script:** sin migración. `fase-01-auditoria.sql`: detección `SELECT affected_table, action, count(*) FROM audit_logs WHERE previous_value ~ '"(PasswordHash|SecurityStamp|ConcurrencyStamp|SignatureDriver)"' OR new_value ~ '"(PasswordHash|SecurityStamp|ConcurrencyStamp|SignatureDriver)"' GROUP BY 1,2;`; corrección `UPDATE audit_logs SET previous_value = CASE WHEN previous_value IS NULL THEN NULL ELSE ((previous_value::jsonb) - ARRAY['PasswordHash','SecurityStamp','ConcurrencyStamp','SignatureDriver'])::text END, new_value = CASE WHEN new_value IS NULL THEN NULL ELSE ((new_value::jsonb) - ARRAY['PasswordHash','SecurityStamp','ConcurrencyStamp','SignatureDriver'])::text END WHERE <mismo filtro>;`. Tras la corrección, la detección devuelve 0 filas.
- **Pruebas automatizadas nuevas:**
  - `Wms.Tests/Common/AuditPayloadBuilderTests.cs`: `ForCreate_UserWithPasswordHash_OmitsSensitiveProperties`, `ForUpdate_OnlyStampsAndPasswordHashChanged_ReturnsNoChanges`, `ForUpdate_NameChangedAndHashUnchanged_ReturnsOnlyName` (anterior `{"FirstName":"Ana"}`, nuevo `{"FirstName":"Ana María"}`), `ForUpdate_ModifiedFlagButSameValue_IsIgnored`, `ForDelete_OmitsSensitiveProperties`.
  - `Wms.IntegrationTests/Security/AuditRedactionTests.cs`: `ResetPassword_DoesNotStoreHashOrStampInAuditLog` (Admin ejecuta `POST user/{id}/reset-password` y ninguna fila de `audit_logs` de ese usuario contiene las claves excluidas).
- **Criterios de aceptación:**
  - Dado el usuario `qa_cambio`, cuando Admin reinicia su contraseña con `POST user/{id}/reset-password`, entonces las filas de `audit_logs` de `ApplicationUser` de esa operación no contienen `PasswordHash`, `SecurityStamp` ni `ConcurrencyStamp` en `previousValue` ni en `newValue`, ni por API (`GET administration/audit-logs`) ni en `/admin/audit`.
  - Dado un usuario al que Admin le cambia el nombre, cuando se consulta su auditoría, entonces la fila `Update` contiene solo el nombre anterior y el nuevo.
  - Dado el script `fase-01-auditoria.sql` ejecutado, cuando se corre su bloque de detección, entonces devuelve 0 filas.
- **Re-test QA:** F7-AUD-006, F7-AUD-002; REG F11-REG-031.
- **Riesgo de regresión:** bajo; la auditoría deja de registrar propiedades que no cambiaron (menos ruido, mismos cambios reales).
- **Tamaño:** S. **Dependencias:** CHG-01.

#### CHG-03 — Matriz de permisos por endpoint y por página

- **Cierra:** DEF-F9-001 (CRITICAL), DEF-F9-002 (MAJOR), DEF-F9-004 (MINOR), DEF-F9-005 (MINOR), DEF-F7-005 (MINOR).
- **Causa raíz:**
  - DEF-F9-001: las escrituras no tienen política propia bajo un `[Authorize]` de clase que solo exige autenticación (`ActiveUser`, `WmsAuthentication.cs:111-113`): `Wms.Api/Controllers/v1/StakeholderController.cs:44` (terceros `:47, 81, 97, 113, 135, 150, 163, 185, 200, 224`; convenios `:235, 273, 285, 296`; servicios del convenio `:309, 341, 357, 371, 385`), `EntryReasonController.cs:18` (`:21, 62, 73`), `DriverController.cs:16` y `VehicleController.cs:16` (`:19, 51`) y `ProductController.cs:17` (`POST :20`; el `PATCH :44` exige `WarehouseAccess`).
  - DEF-F9-002: `WmsAuthentication.cs:77-79` incluye `Receiving` en `WarehouseAccess`, política que usan `EntryLogController.cs:19` y `DepartureAuthorizationController.cs:13` (portería) y todo Bodega; las 12 páginas de `app/pages/warehouse/**` declaran `Receiving` en `requiredRoles` (p. ej. `app/pages/warehouse/index.vue:4`); las lecturas de novedades (`WarehouseNoveltiesController.cs:23, 28, 40, 53`) solo exigen `[Authorize]`.
  - DEF-F9-004: `app/pages/reports/general-inventory.vue:19` no incluye `Billing` y el grupo «Facturación» de `app/components/layout/AppMenu.vue:431-474` no tiene el ítem.
  - DEF-F9-005: `InventoryReportsController.cs:18, 27-30` y `WarehouseMovementsReportController.cs:22, 34-38, 61-65` solo exigen autenticación.
  - DEF-F7-005: `app/pages/reports/general-inventory.vue:55` llama `useAvailableLocations()` → `GET warehouse/locations` (`WarehouseController.cs:897-905`, política de clase `WarehouseAccess`): Comercio Exterior recibe 403 y `app/app.vue:53-69` lo pinta como aviso de error.
- **Cambio exacto:**
  - Backend:
    - Nuevo `Wms.Domain/Security/WmsPolicyRoles.cs`: tabla política → roles que `AddWmsAuthentication` recorre para registrar las políticas. Cambios frente a hoy: `WarehouseAccess` = Admin, Warehouse (sin Receiving); nuevas `GateAccess` = Admin, Receiving; `StakeholderAccess` = Admin, ForeignTrade; `TransportCatalogAccess` = Admin, Receiving, Scale, ForeignTrade (§10 · Permisos de catálogos más Comercio Exterior, que crea vehículos y conductores desde la orden de cargue; regla 4.0.10); `NoveltyReadAccess` = Admin, Warehouse, ForeignTrade; `InventoryReportAccess` = Admin, ForeignTrade, Warehouse, Billing. Las demás políticas no cambian.
    - Atributos de método (las clases conservan su `[Authorize]`; los atributos se suman): `StakeholderAccess` en las 10 escrituras de terceros y `BillingAccess` en las 9 de convenios y servicios del convenio (`StakeholderController.cs`); `AdminOnly` en crear, editar y borrar motivos (`EntryReasonController.cs:21, 62, 73`); `TransportCatalogAccess` en crear y editar de `DriverController.cs` y `VehicleController.cs` (`:19, 51`); `AdminOnly` en `POST product` (`:20`) y `PATCH product/{id}` (`:44`, reemplaza `WarehouseAccess`; solo las páginas de administración usan esos dos endpoints); `NoveltyReadAccess` en las cuatro lecturas de `WarehouseNoveltiesController.cs`; `InventoryReportAccess` en `GetGeneralInventory` (`InventoryReportsController.cs:27`) y en las dos acciones de `WarehouseMovementsReportController.cs` (`:34`, `:61`).
    - `EntryLogController.cs:19` y `DepartureAuthorizationController.cs:13` pasan a `GateAccess`. Se actualizan los comentarios de `EntryLogCorrectionController.cs:13` e `InventoryReportsController.cs:15-19`.
    - Nueva acción `GET reports/general-inventory/locations` en `InventoryReportsController` con `InventoryReportAccess`, que envía el mismo `GetWarehouseLocationsQuery` de `WarehouseController.cs:897-905`.
  - Frontend:
    - Las 12 páginas de `app/pages/warehouse/**` quedan con `requiredRoles: ["Admin", "Warehouse"]`; `app/composables/usePermissions.ts:18` (`MODULE_ROLES.warehouse`) igual.
    - Terceros: `app/pages/admin/stakeholders/index.vue:17` y `[id].vue:128` → `["Admin", "ForeignTrade", "Billing"]`; `create.vue:10` y `edit/[id].vue:32` → `["Admin", "ForeignTrade"]`. En `[id].vue`, computed `canManageStakeholder` (Admin o ForeignTrade) y `canManageAgreements` (Admin o Billing) con `usePermissions` importado explícitamente; `StakeholderHeader.vue`, `StakeholderBusinessRoles.vue`, `BankAccountsList.vue` y `ContactsList.vue` reciben `readonly` y ocultan sus botones de edición cuando es verdadero; el bloque de convenios y sus diálogos se muestran con `isCustomer && canManageAgreements`. En el listado, `:enable-create` y `:enable-edit` de `AppTable` toman `canManageStakeholder`.
    - `app/components/layout/AppMenu.vue`: el grupo «Comercio Exterior» agrega «Terceros» (Listado → `/admin/stakeholders`, Crear → `/admin/stakeholders/create`); el grupo «Facturación» agrega «Clientes» (`/admin/stakeholders?rol=CUSTOMER`, desde cuyo detalle se llega a los convenios), «Inventario general» (`/reports/general-inventory`) y «Movimientos por depósito» (`/reports/warehouse-movements`). No se crea un ítem «Convenios» (§10 · Menú).
    - `app/pages/reports/general-inventory.vue:19` → `["Admin", "ForeignTrade", "Warehouse", "Billing"]`; `:55` usa el nuevo `useReportLocations()` (`app/features/reports/composables/useReportLocations.ts`, clave `["reports", "locations"]`, `GET reports/general-inventory/locations`). `app/pages/reports/warehouse-movements.vue:16` → `["Admin", "Warehouse", "ForeignTrade", "Billing"]`.
    - `app/features/foreign-trade/components/LoadingOrderForm.vue` no cambia: los botones «Agregar Nuevo» de vehículo (`:933-942`) y de conductor (`:979-988`) siguen disponibles para Comercio Exterior.
  - No se toca: `ServiceController` (ya `BillingAccess`), las lecturas de tarifas y `BillingPreviewController` (§10 · Lectura de tarifas), los catálogos anónimos (§10 · Catálogos sin autenticación), las altas rápidas operativas de báscula (`POST weighbridge/stakeholders/quick` y `POST weighbridge/transport-companies/quick`, que no son el CRUD de `StakeholderController` y no forman parte de DEF-F9-001), `OperationalAccess`, `EntryCorrectionAccess` y las páginas de administración de conductores, vehículos, motivos y productos (siguen solo Admin).
- **Migración o script:** sin migración. `fase-01-escrituras-sin-rol.sql` (solo detección): escrituras de `Stakeholder`, `Agreement` y `Product` registradas en `audit_logs` por usuarios sin el rol que ahora se exige (`Stakeholder`: Admin o ForeignTrade; `Agreement`: Admin o Billing; `Product`: Admin), unidas a `"AspNetUserRoles"` y `system_roles` por `code`. Las filas se revisan con el usuario; los artefactos de QA («QA F9 Tercero creado por Bascula», convenio `QA-F9-BAS` archivado) se dejan como evidencia.
- **Pruebas automatizadas nuevas:**
  - `Wms.Tests/Security/WmsPolicyRolesTests.cs`: un caso por política con el conjunto exacto de roles; en particular `WarehouseAccess_ExcludesReceiving`, `GateAccess_IsAdminAndReceiving`, `TransportCatalogAccess_IsAdminReceivingScaleForeignTrade`, `InventoryReportAccess_IsAdminForeignTradeWarehouseBilling`.
  - `Wms.Tests/Security/ControllerAuthorizationTests.cs` (reflexión sobre `Wms.Api`): `[Theory] WriteAction_HasExpectedMethodPolicy(controller, action, policy)` con las 27 escrituras de la causa; `EntryLogController_ClassPolicy_IsGateAccess`; `DepartureAuthorizationController_ClassPolicy_IsGateAccess`; `ReadActions_KeepActiveUser` para `GetStakeholders`, `GetAgreementServices`, `GetEntryReasonsList`, `GetDrivers`, `GetVehicles` y `GetProducts`.
  - `Wms.IntegrationTests/Security/CatalogWriteAuthorizationTests.cs`: `Scale_CreateStakeholder_Returns403`, `Scale_CreateAgreementService_Returns403`, `Billing_CreateAgreementService_IsNotForbidden`, `ForeignTrade_CreateStakeholder_IsNotForbidden`, `Receiving_GetWarehouseInventory_Returns403`, `Warehouse_CreateEntryLog_Returns403`, `Receiving_CreateEntryLog_IsNotForbidden`, `Scale_GetGeneralInventory_Returns403`, `Billing_GetReportLocations_Returns200`, `ForeignTrade_CreateVehicleAndDriver_IsNotForbidden`, `Warehouse_CreateVehicle_Returns403`.
  - `test/components/layout/AppMenu.spec.ts`: con el rol Billing el menú contiene «Clientes», «Inventario general» y «Movimientos por depósito» y no contiene «Convenios»; con el rol Receiving no contiene «Bodega».
- **Criterios de aceptación:**
  - Dado el token de `bascula`, cuando llama `POST stakeholder`, `POST stakeholder/{id}/agreement`, `POST stakeholder/{id}/agreement/{agreementId}/services`, `POST entry-reasons` o `DELETE entry-reasons/{id}`, entonces cada llamada responde 403 y no se crea ni se borra nada.
  - Dado `facturacion`, cuando crea o edita un convenio o un servicio del convenio desde el detalle del cliente, entonces la operación responde 2xx; y cuando llama `POST stakeholder`, responde 403.
  - Dado `c_exterior`, cuando crea o edita un tercero, entonces responde 2xx; y cuando llama `POST stakeholder/{id}/agreement`, responde 403.
  - Dado `vigilancia`, cuando abre `/warehouse`, `/warehouse/inventory`, `/warehouse/receptions` o `/warehouse/loading-orders`, entonces ve «Acceso Denegado»; cuando llama `POST warehouse/receptions/without-weighbridge`, `POST warehouse/forklift-uses/start`, `POST warehouse/loading-orders/{id}/execute` o `GET warehouse/inventory/deposits`, recibe 403; y registra ingresos y salidas como antes.
  - Dado `bodega`, cuando llama `POST entry-logs` o `POST entry-logs/{id}/departure`, entonces recibe 403.
  - Dado `facturacion`, cuando abre `/reports/general-inventory`, entonces la página carga sin avisos de error, con el filtro «Ubicación» poblado, y su menú muestra «Inventario general».
  - Dado `c_exterior`, cuando abre `/reports/general-inventory`, entonces no aparece ningún aviso de error y el filtro «Ubicación» lista las 20 ubicaciones sembradas.
  - Dado `bascula` o `vigilancia`, cuando llama `GET reports/general-inventory` o `GET warehouse/movements-report`, entonces recibe 403; con `bodega`, `c_exterior`, `facturacion` o `capb90` recibe 200.
  - Dado `c_exterior`, cuando crea un vehículo y un conductor con «Agregar Nuevo» en «Nueva orden de cargue», entonces ambos se guardan y quedan seleccionados en la orden, igual que hoy; dado `bodega` o `facturacion`, cuando llaman `POST vehicles` o `POST drivers`, entonces reciben 403.
- **Re-test QA:** F9-API-010, F9-API-011, F9-API-012, F9-API-013, F9-API-014, F9-API-015, F9-API-016, F9-API-019, F9-API-021, F9-MEN-004, F9-PAG-002, F9-PAG-004, F9-PAG-020, F7-REP-016, F10-ERR-004 y el sondeo completo del anexo F9; REG F11-REG-002, F11-REG-003, F11-REG-004, F11-REG-027, F11-REG-028.
- **Riesgo de regresión:** medio (cambia la matriz de todo el API). Lo mitigan `ControllerAuthorizationTests`, las pruebas de integración por rol y el sondeo del anexo F9.
- **Tamaño:** L. **Dependencias:** CHG-01.

### Fase 2 — Operación crítica: portería, avisos, báscula y recepción

- **Objetivo:** cerrar los CRITICAL que rompen la operación diaria —placa equivocada en portería (DEF-F2-001), avisos a Comercio Exterior que no llegan (DEF-F3-001), operación descartada que bloquea el camión y se cobra (DEF-F3-004), recepción imposible de unidades de carga (DEF-F4-001) y recepción directa que falla siempre (DEF-F4-002)— junto con los defectos de la misma causa (DEF-F2-002, DEF-F1-005, DEF-F3-016, DEF-F4-005 y DEF-F8-005).
- **Criterio de entrada:** checkpoint de la Fase 1 aprobado.
- **Cambios:** CHG-04, CHG-05, CHG-06, CHG-07, CHG-08.
- **Orden interno:** CHG-04 → CHG-05 (crea `CarrierCompanyGuard`, que usa CHG-08) → CHG-06 → CHG-07 → CHG-08. Los scripts `fase-02-placas.sql` y `fase-02-ingresos-abiertos.sql` se ejecutan **antes** de aplicar la migración, porque los índices únicos fallan si quedan duplicados.
- **Migración de la fase (la genera el implementador con `dotnet ef`):** `FixRoleSeedAndOperationalUniqueness`: `UpdateData` del rol ForeignTrade (`normalized_name = 'FOREIGNTRADE'`); índice único `idx_vehicle_plate` sobre `vehicles(license_plate)` (hoy no único); índice único parcial `idx_entry_vehicle_open_unique` sobre `entry_logs(vehicle_id) WHERE date_time_departure IS NULL`.
- **Riesgos y mitigación:**
  - La migración falla si quedan placas duplicadas o ingresos abiertos duplicados. Mitigación: los scripts de saneamiento van primero y terminan con consultas de verificación que deben devolver 0 filas.
  - Comercio Exterior empieza a recibir unos 20 tipos de aviso que hoy se pierden. Mitigación: es el comportamiento esperado; se avisa a CE antes del despliegue.
  - El flujo de Vigilancia cambia de búsqueda (exacta en lugar de parcial). Mitigación: el re-test F2 completo de ingreso, historial y salida.
- **Saneamiento de datos:** `fase-02-placas.sql`, `fase-02-ingresos-abiertos.sql` y `fase-02-descartes.sql`, descritos en cada cambio.
- **Criterio de salida:** compuertas comunes (regla 4.0.4) y en PASA: F2-ING-007, F2-ING-010, F2-HIS-003, F1-VEH-002, F1-VEH-004, F1-VEH-005, F3-SAL-011, F3-REC-006, F3-REC-007, F3-REC-008, E2E-11, F4-RUC-001, F4-RUC-002, F4-RUC-004, E2E-05, F4-RSB-002, F4-RSB-004, F4-RSB-007, E2E-08, E2E-12, F9-API-020; REG F11-REG-005, F11-REG-006, F11-REG-010, F11-REG-014, F11-REG-026, F11-REG-031.
- **Checkpoint:** se entrega al usuario el número de vehículos fusionados e ingresos abiertos depurados, la evidencia de los avisos recibidos por `c_exterior`, `j_coral` y `f_chosi`, y el resultado de las pruebas. El usuario aprueba la migración aplicada y la ejecución de los scripts en staging.

#### CHG-04 — Los avisos por rol llegan a los usuarios de Comercio Exterior

- **Cierra:** DEF-F3-001 (CRITICAL).
- **Causa raíz:** el rol sembrado tiene `NormalizedName = "FOREXTERIOR"` (`Wms.Infrastructure/Persistence/SeedDataExtensions.cs:100`), mientras `Wms.Api/Services/NotificationOrchestrator.cs:77` busca los destinatarios con `GetUsersInRoleAsync("ForeignTrade")`, que normaliza a `FOREIGNTRADE`: no encuentra a nadie y solo deja el log «No active users found for role». Los otros cinco roles sembrados sí tienen `NormalizedName` igual al código en mayúsculas (`:82, 91, 109, 118, 127`). Con la misma causa (rol de destino que no resuelve usuarios), `GenerateGlobalDispatchGuideHandler.cs:112` envía al rol inexistente «Weighbridge».
- **Cambio exacto:**
  - Backend: `SeedDataExtensions.cs:100` → `NormalizedName = "FOREIGNTRADE"` (el `Name` «Comercio exterior» no cambia). `GenerateGlobalDispatchGuideHandler.cs:112` → `SystemRolesCode.Scale.ToString()`.
  - Frontend: ninguno (`/notifications` ya lista los avisos persistidos).
  - No se toca: `NotificationOrchestrator`, los 20 envíos a `"ForeignTrade"` ni los nombres visibles de los roles.
- **Migración o script:** forma parte de `FixRoleSeedAndOperationalUniqueness` (`UpdateData` del rol). Verificación posterior: `SELECT code, name, normalized_name FROM system_roles ORDER BY code;` devuelve `FOREIGNTRADE` para ForeignTrade. Los avisos que no llegaron no se reenvían.
- **Pruebas automatizadas nuevas:**
  - `Wms.Tests/Security/SeededRolesTests.cs`: `SeededRoles_NormalizedNameIsCodeInUpperCase` (construye el modelo EF con la extensión de semillas y compara `NormalizedName` con `Code.ToString().ToUpperInvariant()` en los 6 roles).
  - `Wms.IntegrationTests/Notifications/ForeignTradeNotificationTests.cs`: `ImportDepositCreated_NotifiesEveryForeignTradeUser` (un usuario CE y uno Facturación + CE; el registro IMP con documento nuevo deja el aviso en ambos).
- **Criterios de aceptación:**
  - Dado `c_exterior`, `j_coral` y `f_chosi` activos, cuando báscula registra un ingreso de importación con documento nuevo, entonces los tres tienen en `/notifications` el aviso «Nuevo depósito de importación».
  - Dado un depósito confirmado, cuando báscula asocia un camión tardío, entonces los usuarios de Comercio Exterior reciben el aviso de camión tardío y de reimpresión de etiqueta.
  - Dado una recepción con diferencia, una novedad o un cargue completado, cuando Bodega los registra, entonces Comercio Exterior recibe su aviso; Admin y Facturación siguen recibiendo los suyos.
- **Re-test QA:** F3-REG-003, F3-INT-004, F3-MCA-009, F4-REC-006, F4-NOV-001, F4-NOV-002, F4-CAR-002, F5-INT-002, F5-INT-003, F5-LEV-009, F7-NOT-003, E2E-01 (paso 2), E2E-02 (paso 2), E2E-03 (paso 3); REG F11-REG-026.
- **Riesgo de regresión:** bajo.
- **Tamaño:** S. **Dependencias:** CHG-01.

#### CHG-05 — Una sola regla de placa: normalizada, válida, única y buscada por igualdad

- **Cierra:** DEF-F2-001 (CRITICAL), DEF-F1-005 (MAJOR), DEF-F3-016 (MAJOR), DEF-F2-002 (MINOR).
- **Causa raíz:**
  - DEF-F2-001: `app/pages/operations/entries/index.vue:115-121` (Enter) y `:170-175` (registrar), y `app/pages/operations/entries/history.vue:84-90`, resuelven la placa con `GET vehicles?licensePlate=…&pageSize=1` (`app/features/entries/services/vehicle-service.ts:6-9`) y toman el primero; `GetAllVehiclesHandler.cs:16-19` filtra con `ILIKE '%texto%'` y ordena por fecha: «AA102» toma QAA102 y «QAB20» toma QAB201. Además `index.vue:169,178` reutiliza el vehículo de una búsqueda anterior y el historial queda reducido a un solo `vehicleId` (`history.vue:99`).
  - DEF-F1-005 y DEF-F2-002: `CreateVehicleHandler.cs:16-22` compara la placa con igualdad sensible a mayúsculas, `Vehicle.cs:24-37` guarda el texto crudo, `CreateVehicleValidator.cs:10-12` no valida formato, `VehicleConfiguration.cs:24` define `idx_vehicle_plate` sin `IsUnique()` y `CreateVehicleHandler.cs:32-38` acepta como transportadora un tercero sin el rol TRANSPORT_COMPANY. La regla 3–20 `[A-Z0-9-]` solo existe en la corrección de ingresos (`CorrectEntryLogCommandHandler.cs:41`).
  - DEF-F3-016 (parcialmente): `GetVehicleByPlateHandler.cs:19-24` no filtra `IsActive` ni ordena y devolvió el duplicado inactivo `qaa101`. La hipótesis de la ficha sobre la salida con tiquete no se reproduce: `EntryTicketExitRules.cs:59-61` compara `VehicleId`; falló porque la OC se creó con el id del duplicado.
- **Cambio exacto:**
  - Backend:
    - `Wms.Common/Text/PlateNormalizer.cs`: agregar `ResolveChange(string? requested, string? current, string label)` (nulo si no se pide placa o si la normalizada es igual a la actual; si no, `NormalizeAndValidate`) y `ToContainsPattern(string? raw)` (`""` sin texto; si no, `%` + `ForSearch(raw)` con `\`, `%` y `_` escapados + `%`).
    - `Wms.Domain/Entities/Logistics/Vehicle.cs`: `Create` guarda `PlateNormalizer.NormalizeAndValidate(placa, "La placa")`; `Update` normaliza la placa cuando viene.
    - `CreateVehicleHandler`: normaliza y valida; duplicado con `AnyAsync(v => v.LicensePlate == plate)` → `ConflictException("La placa {plate} ya existe.")`. `UpdateVehicleHandler`: usa `ResolveChange` y la misma unicidad excluyendo el propio vehículo.
    - Nuevo `Wms.Application/Common/Validation/CarrierCompanyGuard.cs`: `EnsureAsync(context, id)` + regla pura `Check(name, isActive, roleCodes)`: inexistente → `NotFoundException("La empresa transportadora no existe.")`; inactiva → `BadRequestException("La empresa de transporte '{nombre}' está inactiva.")`; sin rol TRANSPORT_COMPANY → `BadRequestException("El tercero '{nombre}' no tiene el rol de empresa de transporte.")`. Se invoca en `CreateVehicleHandler`, en `UpdateVehicleHandler` (solo si cambia la transportadora) y en `EntryLogInfoUpdater.cs:151-157`.
    - `VehicleConfiguration.cs:24` → `HasIndex(v => v.LicensePlate).IsUnique().HasDatabaseName("idx_vehicle_plate")`.
    - `GetVehicleByPlateQuery(string LicensePlate, bool IncludeInactive = false)`: igualdad con la placa normalizada, `IsActive` salvo `IncludeInactive`, orden `IsActive` descendente y `CreatedAt`. `WeighbridgeCatalogController.cs:46-53` recibe `[FromQuery] bool includeInactive = false`.
    - `GetOpenCycleByPlateHandler.cs:30,61`, `SearchByPlateForReceptionHandler.cs:46,72` y `CorrectEntryLogCommandHandler.cs:46-47` comparan por igualdad con la placa normalizada.
    - Filtros parciales: `GetAllEntryLogsHandler.cs:28-32` y `GetAllVehiclesHandler.cs:16-19` usan `EF.Functions.ILike(v.LicensePlate.Replace("-", ""), PlateNormalizer.ToContainsPattern(texto))`.
  - Frontend:
    - `app/utils/plate.ts`: agregar `PLATE_FORMAT_MESSAGE = "La placa debe tener de 3 a 20 letras, números o guiones."`.
    - `app/features/entries/services/vehicle-service.ts`: `getVehicleByPlate(plate, { includeInactive })` → `GET weighbridge/vehicles/by-plate/{plate}`; devuelve el vehículo o `null` y no oculta otros errores.
    - `app/pages/operations/entries/index.vue`: importa `normalizePlate`, `isValidPlate` y `PLATE_FORMAT_MESSAGE` de `~/utils/plate` (elimina la copia local de `:76-77`); al editar la placa limpia el vehículo, el «no encontrado» y el ingreso abierto previos; con placa inválida muestra «Placa no válida» y el mensaje de formato sin llamar al API; la búsqueda (Enter) y el registro resuelven siempre con `getVehicleByPlate(placa, { includeInactive: true })`; el aviso de éxito muestra la placa del vehículo asignado; «Registrar ingreso» queda deshabilitado con placa inválida.
    - `history.vue:75-112`: el filtro envía `licensePlate` normalizado (sin buscar vehículos), con `watchDebounced` de 400 ms; «Limpiar» borra también `licensePlate`. `exits.vue:33-37` importa `normalizePlate`.
    - `app/features/entries/components/CreateVehicleDialog.vue:62-67` y `app/pages/admin/vehicles/index.vue`: normalizan la placa, validan con `isValidPlate` y muestran `PLATE_FORMAT_MESSAGE`.
    - `app/features/foreign-trade/components/ExitWithEntryTicketDialog.vue:46-48`: lista solo las órdenes cuya placa normalizada es igual a la del tiquete.
  - No se toca: `VehiclesImporter.cs` (ya normaliza), `CreateEntryLogHandler.cs:66` (un vehículo inactivo sigue recibiendo el ingreso, OBS-F2-002), `EntryTicketExitRules.cs` y `AdditionalOutputOrderRules.cs` (comparan por id), y la placa del handler sin báscula (la rehace CHG-08).
- **Migración o script:** índice único de `FixRoleSeedAndOperationalUniqueness`. `fase-02-placas.sql`, antes de la migración: (1) detección de placas duplicadas por mayúsculas o espacios (`upper(regexp_replace(license_plate,'\s+','','g'))` con `count(*) > 1`); (2) fusión en una transacción: sobrevive el activo, luego el que tiene transportadora, luego el más antiguo; se copian al sobreviviente transportadora, país y tipo faltantes; `entry_logs.vehicle_id` y `loading_orders.vehicle_id` se repuntan al sobreviviente; se borran los duplicados; (3) normalización de `vehicles.license_plate` y `warehouse_storage_entries.vehicle_plate`; (4) verificación: 0 placas duplicadas y 0 vehículos con más de un ingreso abierto; (5) detección de transportadoras sin rol TRANSPORT_COMPANY (se dejan sin transportadora con `UPDATE vehicles SET carrier_company_id = NULL …` por id); (6) detección de placas con formato inválido, que se conservan como histórico inactivo.
- **Pruebas automatizadas nuevas:**
  - `Wms.Tests/Common/PlateNormalizerTests.cs`: `ResolveChange_NotRequested_ReturnsNull`, `ResolveChange_SameNormalizedPlate_ReturnsNull` (« qaa 101 » frente a QAA101), `ResolveChange_NewPlate_ReturnsNormalized` («qab 201» → QAB201), `ResolveChange_InvalidNewPlate_ThrowsBadRequest`, `ResolveChange_UnchangedLegacyInvalidPlate_ReturnsNull`, `ToContainsPattern_PartialText_BuildsContainsPattern` («qab 20» → `%QAB20%`), `ToContainsPattern_EscapesWildcards`, `ToContainsPattern_Blank_ReturnsEmpty`.
  - `Wms.Tests/Domain/Logistics/VehicleTests.cs`: `Create_NormalizesPlate` («  qaa 101 » → QAA101), `Create_InvalidPlate_ThrowsBadRequest` («AB#12» → «La placa 'AB#12' no es válida: use de 3 a 20 letras, números o guiones.»), `Update_WithPlate_NormalizesIt`, `Update_WithoutPlate_KeepsCurrent`.
  - `Wms.Tests/Common/CarrierCompanyGuardTests.cs`: `Check_WithoutTransportRole_ThrowsBadRequest`, `Check_Inactive_ThrowsBadRequest`, `Check_ActiveWithRole_DoesNotThrow`.
  - `Wms.Tests/Weighbridge/EntryTicketExitRulesTests.cs`: `OrderOfAnotherVehicle_Throws`.
  - `Wms.IntegrationTests/Logistics/VehiclePlateTests.cs`: `CreateVehicle_LowercaseDuplicate_Returns409`, `GetByPlate_PartialText_ReturnsNoVehicle`, `GetByPlate_InactiveVehicle_OnlyWithIncludeInactive`, `EntryLogs_FilterByPartialPlate_ReturnsEveryMatch`.
  - `test/unit/utils/plate.spec.ts`: `normalizePlate(" qab 202 ")` → `QAB202`; `isValidPlate("AB#12")` → falso; `isValidPlate("QAB20")` → verdadero.
- **Criterios de aceptación:**
  - Dado QAA102 existente y AA102 inexistente, cuando Vigilancia digita «AA102» y pulsa Enter, entonces la pantalla indica que el vehículo no existe y se creará al registrar; al registrar, el ingreso queda a nombre de un vehículo nuevo AA102 y QAA102 no recibe ningún ingreso.
  - Dado QAB201 con un ingreso abierto, cuando Vigilancia digita «QAB20» y pulsa Enter, entonces no aparece QAB201 ni su ingreso, y el ingreso de QAB20 se registra.
  - Dado ingresos de QAB201 a QAB205, cuando el historial se filtra con «qab20», entonces lista los ingresos de las cinco placas.
  - Dado Vigilancia digita «AB#12», cuando pulsa Enter o «Registrar ingreso», entonces ve «Placa no válida» con «La placa debe tener de 3 a 20 letras, números o guiones.» y no se llama al API; por API, `POST vehicles` con «AB#12» responde 400 «La placa 'AB#12' no es válida: use de 3 a 20 letras, números o guiones.».
  - Dado QAA101 existente, cuando se envía `POST vehicles` con «qaa101», entonces responde 409 «La placa QAA101 ya existe.».
  - Dado un tercero que solo tiene el rol CUSTOMER, cuando se crea un vehículo con ese `carrierCompanyId`, entonces responde 400 «El tercero 'QA Cliente Uno SAS' no tiene el rol de empresa de transporte.».
  - Dado el saneamiento aplicado, cuando se consulta `GET weighbridge/vehicles/by-plate/qaa101`, entonces devuelve el vehículo activo QAA101 con su transportadora; un vehículo inactivo solo aparece con `includeInactive=true`.
- **Re-test QA:** F2-ING-007, F2-ING-010, F2-HIS-003, F1-VEH-002, F1-VEH-004, F1-VEH-005, F3-SAL-011; REG F11-REG-005, F11-REG-006.
- **Riesgo de regresión:** medio; cambia la búsqueda de portería. Lo cubren el re-test F2 y `VehiclePlateTests`.
- **Tamaño:** M. **Dependencias:** CHG-01.

#### CHG-06 — Descartar una operación libera el camión y bloquea su cobro

- **Cierra:** DEF-F3-004 (CRITICAL).
- **Causa raíz:** `Wms.Application/Weighbridge/Commands/DiscardIncompleteOperation/DiscardIncompleteOperationHandler.cs:29-33` no incluye los vínculos del servicio con el ingreso y `:70` solo marca el servicio como descartado: el vínculo `service_record_entry_logs` queda vivo. La cola (`GetWeighbridgeQueueHandler.cs:48` y `:50-62`), los pendientes (`GetPendingEntryLogsHandler.cs:24`), el registro (`InitiateStorageWeighingHandler.cs:192-196`, `InitiateWeighingOnlyHandler.cs:49-54`, `InitiateOutputWeighingHandler.cs:47-52`) y los seis cobros (`ProcessStoragePaymentHandler.cs:47-54`, `ProcessWeighingOnlyPaymentHandler.cs:45-52`, `ProcessOutputPaymentHandler.cs:45-52` y los tres `Start*PendingBillingHandler.cs:34-39`) no filtran servicios `Discarded`.
- **Cambio exacto:**
  - Backend:
    - `DiscardIncompleteOperationHandler`: `.Include(sr => sr.EntryLogLinks)` y, después de `Discard`, `context.ServiceRecordEntryLogs.RemoveRange(serviceRecord.EntryLogLinks)` (todos los camiones del servicio). El camión vuelve a «Sin iniciar», se registra de nuevo y Vigilancia puede corregir su motivo.
    - `ServiceRecord`: nuevo `EnsureNotDiscarded()` → `ConflictException("La operación fue descartada; registre el ingreso del camión de nuevo.")`, llamado justo después de cargar el servicio en los seis handlers de cobro.
    - Defensa para datos viejos: la cola, los pendientes y los tres `Initiate*` ignoran vínculos de servicios `Discarded` (`l.ServiceRecord.Status != ServiceRecordsStatus.Discarded`).
  - Frontend: `app/pages/operations/weighbridge/recover.vue:241-243`: tras descartar, invalida `["weighbridge"]` además del `refetch()`.
  - No se toca: `GetRecoverableOperationsHandler` (ya filtra), la conservación del `ServiceRecord` descartado ni la liberación de la orden de cargue al descartar una salida (la hace CHG-32).
- **Migración o script:** sin migración. `fase-02-descartes.sql`: detección y borrado de vínculos de servicios descartados sin ciclo (`DELETE FROM service_record_entry_logs l USING service_records sr WHERE sr.id = l.service_record_id AND sr.status = 'Discarded' AND NOT EXISTS (SELECT 1 FROM weighbridge_cycles wc WHERE wc.service_record_id = sr.id);`), que cubre 2026BA00003 y 2026BA00030; detección de ciclos y facturas creados sobre servicios descartados (`weighbridge_cycles` con `status <> 'Canceled'` cuyo servicio está `Discarded`, con su `invoice_id`): Báscula anula ese pesaje y Facturación anula la factura con el motivo «Cobro sobre una operación descartada (DEF-F3-004)».
- **Pruebas automatizadas nuevas:**
  - `Wms.Tests/Domain/Services/ServiceRecordDiscardTests.cs`: `EnsureNotDiscarded_Discarded_ThrowsConflictWithMessage`, `EnsureNotDiscarded_InTransit_DoesNotThrow`, `Discard_InWeighing_ThrowsConflict`, `Discard_InTransit_SetsDiscardedAtAndBy`.
  - `Wms.IntegrationTests/Weighbridge/DiscardOperationTests.cs`: `Discard_ReleasesTruckToNotStarted`, `Discard_ThenRegisterAgain_Returns201`, `ProcessPayment_OnDiscardedService_Returns409`.
- **Criterios de aceptación:**
  - Dado QAC402 registrado y sin cobrar, cuando báscula lo descarta desde «Recuperar operaciones», entonces el depósito queda Anulado, la cola muestra QAC402 «Sin iniciar» y registrarlo de nuevo responde 201.
  - Dado el servicio descartado, cuando se llama `POST weighbridge/storage/process-payment`, entonces responde 409 «La operación fue descartada; registre el ingreso del camión de nuevo.» y no se crea ciclo ni factura.
  - Dado el camión descartado, cuando Vigilancia corrige su motivo, entonces la corrección se guarda.
- **Re-test QA:** F3-REC-006, F3-REC-007, F3-REC-008, E2E-11 (paso 1); REG F11-REG-010, F11-REG-031.
- **Riesgo de regresión:** bajo.
- **Tamaño:** M. **Dependencias:** CHG-01.

#### CHG-07 — La recepción de unidades de carga se completa sin contar productos

- **Cierra:** DEF-F4-001 (CRITICAL).
- **Causa raíz:** `Wms.Application/Warehouse/Commands/Reception/CompleteReceptionCommandValidator.cs:12-13` exige `Products` no vacío y corre antes del handler (`ValidationBehavior`), mientras `CompleteReceptionCommandHandler.cs:85-89` rechaza productos en un depósito de unidades de carga: toda entrada termina en 400. La misma regla está en `CreateReceptionCommandValidator.cs:13-14` (recepción en un paso). La pantalla ya envía `products: []` y `receivedCargoUnitIds` (`app/features/warehouse/components/ReceptionStepCompletion.vue:267-271`).
- **Cambio exacto:**
  - Backend: borrar `RuleFor(x => x.Products).NotEmpty()` en `CompleteReceptionCommandValidator.cs:12-13` y en `CreateReceptionCommandValidator.cs:13-14`, conservando el `RuleForEach` sobre los productos enviados. La regla queda en los handlers con los mensajes existentes: mercancía suelta sin productos → 400 «Debe indicar al menos un producto con cantidad a descargar.»; unidades de carga con productos → 400 «En un depósito de unidades de carga no se cuentan productos: confirme las unidades recibidas completas.»; unidades sin confirmar → 400 «Confirme que llegaron completas todas las unidades de carga del camión: {placas}.» (`ReceptionCargoUnits.cs:35-37`).
  - Frontend: ninguno.
  - No se toca: `ReceptionCargoUnits.cs`, `WarehouseStorageCargoUnit.MarkReceived` ni el cálculo de diferencias (lo ajusta CHG-56).
- **Migración o script:** sin migración. Detección de recepciones atascadas: `SELECT rl.id, ws.warehouse_storage_number, rl.arrival_at FROM reception_logs rl JOIN warehouse_storage_entries e ON e.id = rl.warehouse_storage_entry_id JOIN warehouse_storages ws ON ws.id = e.warehouse_storage_id WHERE ws.cargo_handling = 'CargoUnits' AND rl.is_active AND rl.status = 'InProgress';` (BA00005/QAB202 y EXP00004/QAEC0001); se completan desde la pantalla tras el despliegue.
- **Pruebas automatizadas nuevas:**
  - `Wms.Tests/Warehouse/CompleteReceptionCommandValidatorTests.cs` y `CreateReceptionCommandValidatorTests.cs`: `Validate_EmptyProducts_HasNoErrors`, `Validate_NullProducts_HasNoErrors`, `Validate_ZeroQuantity_FailsWithMessage` («La cantidad descargada debe ser mayor a cero.»).
  - `Wms.Tests/Warehouse/ReceptionCargoUnitsTests.cs`: `EnsureAllConfirmed_AllIdsPresent_DoesNotThrow`, `EnsureAllConfirmed_NullIds_ThrowsWithPlates` («Confirme que llegaron completas todas las unidades de carga del camión: ABC123, DEF456.»), `EnsureAllConfirmed_OneUnitMissing_Throws`.
  - `Wms.IntegrationTests/Warehouse/CargoUnitReceptionTests.cs`: `CompleteReception_CargoUnitsConfirmedWithoutProducts_Returns200`, `CompleteReception_CargoUnitsWithProducts_Returns400WithMessage`.
- **Criterios de aceptación:**
  - Dado el tanquero QAB202 (2026BA00005, unidad QAT001) con la llegada registrada, cuando Bodega completa la recepción sin productos y con QAT001 confirmada, entonces la recepción queda Completed y la unidad recibida.
  - Dado el mismo camión, cuando Bodega completa sin confirmar QAT001, entonces responde 400 «Confirme que llegaron completas todas las unidades de carga del camión: QAT001.».
  - Dado un depósito de mercancía suelta, cuando se completa la recepción sin productos, entonces responde 400 «Debe indicar al menos un producto con cantidad a descargar.».
- **Re-test QA:** F4-RUC-001, F4-RUC-002, F4-RUC-004, E2E-05 (paso 2); REG F11-REG-014.
- **Riesgo de regresión:** bajo.
- **Tamaño:** S. **Dependencias:** CHG-01.

#### CHG-08 — Recepción sin báscula: contrato correcto, ingreso existente y depósito en Borrador

- **Cierra:** DEF-F4-002 (CRITICAL), DEF-F4-005 (MAJOR), DEF-F8-005 (MAJOR).
- **Causa raíz:**
  - DEF-F4-002: `app/features/warehouse/components/ReceptionStepManualInfo.vue:196-237` envía un cuerpo fuera del contrato de `CreateReceptionWithoutWeighbridgeCommand.cs:26-78` (producto en campos sueltos en vez de `receptionProducts`, `unitMeasureId: ""`, `authorizedByUserId: ""`). Un `""` en un `Guid` rompe el enlace del JSON y, con `SuppressModelStateInvalidFilter = true` (`Wms.Api/Program.cs:51-53`), `WarehouseController.cs:340-346` recibe el comando nulo y `mediator.Send(null)` lanza `ArgumentNullException` (500). El validador nunca corre.
  - DEF-F4-005: `CreateReceptionWithoutWeighbridgeCommandHandler.cs:169-178` crea siempre un `EntryLog` nuevo y busca el vehículo por placa (`:108-110`, `:429-443`): el ingreso «Solo bodega» original queda abierto y aparece otra vez en pendientes.
  - DEF-F8-005: el mismo handler confirma el depósito (`:281`, `warehouseStorage.Confirm()`) y abre período y factura después del commit (`:289-315`), saltándose la confirmación de Comercio Exterior (`ConfirmStorageDepositHandler.cs:63-80`), que exige los datos aduaneros.
- **Cambio exacto:**
  - Backend:
    - Nuevo `Wms.Application/Common/Identity/ClaimsPrincipalExtensions.cs` con `GetRequiredUserId()` (§4.0 regla 8).
    - `CreateReceptionWithoutWeighbridgeCommand`: agrega `string EntryLogId` como primer parámetro y elimina `VehiclePlate`; `AuthorizedByUserId` pasa a `[JsonIgnore] public Guid AuthorizedByUserId { get; init; }`, que fija `WarehouseController.cs:340-346` con `command with { AuthorizedByUserId = User.GetRequiredUserId() }`.
    - Validador: `EntryLogId` no vacío («El Id del ingreso es requerido.») y GUID válido («El Id del ingreso no es válido.»); se borra la regla de `VehiclePlate` (`:30-32`).
    - Nueva clase pura `DirectReceptionEntryRules.EnsureEligible(DirectReceptionEntryInfo)` con este orden: ingreso con salida → `ConflictException("El ingreso de la placa {placa} ya tiene salida registrada. Vigilancia debe registrar un nuevo ingreso «Solo bodega».")`; sin motivo → `BadRequestException("El ingreso de la placa {placa} no tiene motivo de ingreso. Asígnele «Solo bodega» en Vigilancia.")`; motivo que requiere pesaje → `BadRequestException("El ingreso de la placa {placa} requiere pesaje en báscula; la recepción directa solo aplica a ingresos que no requieren pesaje.")`; recepción activa → `ConflictException("El ingreso de la placa {placa} ya tiene una recepción registrada.")`. Un ingreso inexistente responde `NotFoundException("El ingreso no existe.")`.
    - Handler: dentro de la transacción bloquea el ingreso (`SELECT id FROM entry_logs WHERE id = {id} FOR UPDATE`, patrón de `DispatchGuideBalanceService.cs:29-30`), lo carga con vehículo y motivo y aplica `EnsureEligible`; la fecha de ingreso del depósito es `entryLog.DateTimeEntry`; actualiza el vehículo del ingreso con transportadora, país y tipo (`CarrierCompanyGuard` de CHG-05 en `ValidateStakeholdersAsync`, `:388`); crea o reutiliza el conductor y lo asigna al ingreso; borra la creación del `EntryLog` (`:169-178`) y `GetOrCreateVehicleAsync`; conserva el vínculo y la `WarehouseStorageEntry` sobre el ingreso existente.
    - El mismo handler deja el depósito en Borrador: se borran `warehouseStorage.Confirm()` (`:281`), el bloque de facturación posterior al commit (`:289-315`) y el parámetro `IStorageBillingService`; se conservan `ValidateFinancialStatusAsync` (§10 · Mora), `CompleteReception()`, el aviso al Admin y el aviso de diferencias a Comercio Exterior (§10 · Recepción sin báscula).
    - Se actualizan `Wms.Application/Warehouse/README.md:471-510` y el XML del endpoint (`WarehouseController.cs:262-336`) al contrato real.
  - Frontend:
    - `app/features/warehouse/types/reception.ts:326-389`: el request queda con `entryLogId`, datos del conductor y del vehículo (sin placa), `operationModalityCode: "INSP"`, carta porte, cliente y su rol, importador y agencia con su rol solo si se eligen, documentos, moneda y valor solo si se digitan, `receptionProducts: [{ productId, productDescription, declaredQuantity, unitMeasureId, unloadedQuantity }]`, ubicación, firma, fotos (máximo 5), cuadrilla y motivo. Nunca se envía `""` en un campo `Guid`, ni `authorizedByUserId`, ni `vehiclePlate`.
    - `ReceptionStepManualInfo.vue`: arma el cuerpo con la función pura nueva `buildManualReceptionRequest(form, entryLogId)` (`app/features/warehouse/utils/manual-reception.ts`); exige producto y unidad de medida («Producto requerido», «Unidad de medida requerida») y quita el segundo selector de unidad de «Recepción Física».
    - `app/pages/warehouse/receptions/index.vue:181-196`: muestra `error.description` del error del API. `useReceptionCreate.ts:10-16`: invalida `["warehouse-pending-direct-reception"]`.
  - No se toca: `ConfirmStorageDepositHandler.cs`, `DepositConfirmationRequirements.cs`, `CreateEntryLogHandler.cs` ni `GetPendingDirectReceptionHandler.cs`.
- **Migración o script:** índice único parcial `idx_entry_vehicle_open_unique` de `FixRoleSeedAndOperationalUniqueness`. `fase-02-ingresos-abiertos.sql`, antes de la migración: detección de vehículos con más de un ingreso abierto; corrección en una transacción: por cada ingreso duplicado creado por la recepción directa (sin motivo y con observación «Ingreso manual sin báscula.%»), repunta `warehouse_storage_entries`, `service_record_entry_logs` y `manifests` al ingreso «Solo bodega» original abierto del mismo vehículo y borra el duplicado; los duplicados sin ingreso original abierto se cierran con la salida en Vigilancia. Detección de depósitos creados por este flujo que quedaron Confirmados sin datos de Comercio Exterior (`observations LIKE 'Ingreso manual sin báscula.%' AND status = 'Confirmed'`): son datos de QA de la base local (2026INSP00005 a 2026INSP00008) y se resuelven al recrear la base (§7).
- **Pruebas automatizadas nuevas:**
  - `Wms.Tests/Warehouse/CreateReceptionWithoutWeighbridgeCommandValidatorTests.cs`: `Validate_FinalContract_HasNoErrors`, `Validate_NoReceptionProducts_FailsWithMessage`, `Validate_EmptyUnitMeasure_FailsWithMessage` («La unidad de medida del producto es requerida.»), `Validate_EmptyEntryLogId_Fails`.
  - `Wms.Tests/Warehouse/DirectReceptionEntryRulesTests.cs`: un caso por regla con el mensaje exacto y la placa «QAB204», y `EnsureEligible_OpenEntryWithoutWeighing_DoesNotThrow`.
  - `Wms.Tests/Domain/Warehouse/WarehouseStorageReceptionTests.cs`: `CompleteReception_OnDraftStorage_KeepsDraft`.
  - `Wms.Tests/Common/ClaimsPrincipalExtensionsTests.cs`: `GetRequiredUserId_ValidGuidClaim_ReturnsGuid`, `GetRequiredUserId_MissingClaim_ThrowsUnauthorized`, `GetRequiredUserId_NotAGuid_ThrowsUnauthorized`.
  - `Wms.IntegrationTests/Warehouse/DirectReceptionTests.cs`: `CreateWithoutWeighbridge_UsesOpenEntryAndLeavesDraft` (sin `EntryLog` nuevo, depósito en Borrador, sin período ni factura), `CreateWithoutWeighbridge_Twice_SecondReturns409`, `CreateWithoutWeighbridge_AuthorFromBody_IsIgnored`.
  - `test/unit/warehouse/manual-reception.spec.ts`: `buildManualReceptionRequest` arma un solo `receptionProducts` y no incluye `authorizedByUserId`, `vehiclePlate` ni valores `""`.
- **Criterios de aceptación:**
  - Dado QAB204 con un ingreso abierto «Solo bodega», cuando Bodega completa «Recepción Directa» desde `/warehouse/receptions` con cliente, QA Repuestos 12, ubicación, firma y motivo, entonces responde 201, nace un depósito INSP en Borrador con stock 12 y movimiento `DeclaredEntry`, la recepción queda Completed, QAB204 conserva un solo ingreso abierto y no se abre período ni factura.
  - Dado ese ingreso ya recibido, cuando se envía otra recepción directa para él, entonces responde 409 «El ingreso de la placa QAB204 ya tiene una recepción registrada.».
  - Dado el depósito en Borrador, cuando Comercio Exterior completa fecha del documento, moneda, valor y manifiesto y lo confirma, entonces se abren el período y la factura de almacenamiento.
  - Dado un ingreso cuyo motivo requiere pesaje, cuando se intenta la recepción directa por API, entonces responde 400 «El ingreso de la placa {placa} requiere pesaje en báscula; la recepción directa solo aplica a ingresos que no requieren pesaje.».
  - Dado un cuerpo con `authorizedByUserId` de otro usuario, cuando se procesa, entonces el movimiento de inventario queda autorizado por el usuario del token.
- **Re-test QA:** F4-RSB-002, F4-RSB-004, F4-RSB-007, E2E-08 (pasos 2 y 4), E2E-12, F9-API-020 (parte de recepción); REG F11-REG-014.
- **Riesgo de regresión:** medio (cambia el contrato del endpoint). Lo cubren las pruebas de integración y el re-test E2E-08.
- **Tamaño:** L. **Dependencias:** CHG-05.

### Fase 3 — Facturación crítica: lo que se cobra

- **Objetivo:** que cada factura cobre la tarifa de la modalidad correcta, que un período no se facture dos veces, que el override fije un total en una base explícita y que el vencimiento y la mora se calculen bien en una sola corrida. Cierra DEF-F6-001, DEF-F6-002, DEF-F6-003, DEF-F6-004, DEF-F6-005 y DEF-F6-006 (los seis CRITICAL de dinero).
- **Criterio de entrada:** checkpoint de la Fase 2 aprobado; migración de la Fase 2 aplicada; para el re-test manual, el dataset maestro de F1 (descrito en `resultados/registro-datos-qa.md`) cargado en la base de pruebas (convenio `QA-CONV-001`, tarifas base IMP y EXP, mínimos por modalidad, configuraciones de facturación).
- **Cambios:** CHG-09, CHG-10, CHG-11, CHG-12, CHG-13.
- **Orden interno:** CHG-09 → CHG-10 → CHG-11 (crea `VatMath`, que reutiliza CHG-24) → CHG-12 → CHG-13. Los dos últimos tocan `Invoice.cs` y `BillingJobService.cs`: CHG-13 parte del código que deja CHG-12.
- **Riesgos y mitigación:**
  - Los depósitos EXP e INSP de clientes con convenio solo para IMP cambian de importe (ahora el correcto). Mitigación: el script de detección lista las facturas afectadas y Facturación recibe la lista antes del despliegue; las facturas emitidas se ajustan en SIIGO.
  - Las reglas de BASCULA, MONTACARGAS o GUIA_SALIDA con modalidad dejan de aplicar (esos servicios se resuelven sin modalidad). Mitigación: consulta previa del script y corrección de esas reglas antes del despliegue.
  - El bloqueo por mora pasa a la primera corrida del job: al desplegar, los clientes con deuda vencida sobre su límite quedan bloqueados de inmediato. Mitigación: el script lista esos clientes y Facturación los revisa antes.
- **Saneamiento de datos:** `fase-03-tarifa-modalidad.sql` (detección), `fase-03-periodos-duplicados.sql`, `fase-03-overrides.sql` y `fase-03-vencimientos.sql` (detección y corrección), descritos en cada cambio. Se ejecutan después del despliegue del backend y antes del re-test.
- **Criterio de salida:** compuertas comunes (regla 4.0.4) y en PASA: F6-TAR-004, F6-TAR-007, F6-INV-011, F6-ACC-005, E2E-06, E2E-08, F6-ALM-008, F6-FOR-005, E2E-13, F6-OVR-002, F6-OVR-003, F6-OVR-004, F6-CAR-005, F6-CON-003, F6-INV-008, E2E-07, E2E-12, F6-CAR-001, F6-CAR-002, F6-CAR-003; REG F11-REG-021, F11-REG-022, F11-REG-025, F11-REG-031.
- **Checkpoint:** se entrega al usuario el resumen de la fase, el resultado de las pruebas, las filas detectadas y corregidas por cada script y la hoja de verificación del informe F6 (§4) recalculada con el código nuevo. El usuario aprueba: (1) la base «total de la línea con IVA incluido» del override, que aplica §10 · IVA en valores digitados; (2) la lista de clientes que quedan bloqueados al desplegar; (3) la ejecución de los scripts en staging.

#### CHG-09 — Una tarifa solo aplica a su modalidad y a su producto

- **Cierra:** DEF-F6-001 (CRITICAL).
- **Causa raíz:** `Wms.Application/Billing/Services/RuleSpecificity.cs:41` y `:48` agregan peldaños que comparan solo el producto y aceptan cualquier modalidad. `BillingResolver.cs:264-272` (convenio) y `:289-297` (tarifa base) usan esa escalera, de modo que la regla IMP001 de QA Cliente Uno cubre un depósito EXP o INSP (peldaño 6) y la tarifa base EXP001 cubre un INSP. Además `Wms.Application/Warehouse/Common/Services/ForkliftService.cs:81-88` decide «hay convenio» con un `AnyAsync` que no filtra modalidad ni perecedero.
- **Cambio exacto:**
  - Backend:
    - `RuleSpecificity.cs` → `Select`: borrar las líneas 41 y 48. Escalera final: producto + modalidad → producto con modalidad nula → producto nulo con modalidad → ambos nulos; en cada peldaño, primero la regla con perecedero exacto y luego la genérica (sin cambio). Una regla con modalidad solo aplica a esa modalidad, una sin modalidad aplica a todas; igual con el producto. Un contexto sin modalidad (báscula, montacargas, guía) solo ve reglas sin modalidad. Actualizar el comentario `<summary>` de las líneas 9-18.
    - `ForkliftService.cs:81-88`: el `AnyAsync` agrega `a.OperationModalityId == null && a.AppliesToPerishable == null`, para que un convenio de MONTACARGAS con modalidad no entre a `ResolveAsync` y siga usando `ForkliftRates`.
    - Extraer el texto de advertencia de `StorageBillingService.cs:268-276` a `public static class StorageFallbackWarning` (`Wms.Application/Billing/Common/Services/StorageFallbackWarning.cs`) con `Build(string productLabels, string modalityName, string amountText, IEnumerable<string> reasons)`; el texto no cambia.
  - Frontend: ninguno (`AgreementServiceFormDialog.vue:58,75` y `ServicePricingRuleFormDialog.vue:36,54` ya rotulan «— Todas las modalidades —» y «— Todos los productos del cliente —»).
  - No se toca: el respaldo a `ServiceMinimumValue` (`StorageBillingService.cs:135-138` y `:225-256`) ni la dimensión perecedero.
- **Migración o script:** sin migración. `fase-03-tarifa-modalidad.sql`: (a) detección de períodos facturados con una regla de otra modalidad (períodos con `source = 'Agreement'` o `'ServiceRule'` sin regla activa de ALMACENAMIENTO cuya modalidad sea nula o igual a la del depósito, con su factura); (b) reglas de BASCULA, MONTACARGAS y GUIA_SALIDA con `operation_modality_id` no nulo en `agreement_services` y `service_pricing_rules`, que se corrigen con `UPDATE … SET operation_modality_id = NULL WHERE id = '<regla>'` (si choca con el índice único parcial, la regla se desactiva). Las facturas en Borrador o Pendiente de la consulta (a) se corrigen con «Sobrescribir total» (CHG-11); las emitidas, con nota crédito en SIIGO.
- **Pruebas automatizadas nuevas:**
  - `Wms.Tests/Billing/Services/RuleSpecificityModalityTests.cs`: `Select_ImportOnlyRule_ForExportDeposit_ReturnsNull`, `Select_ImportOnlyRule_ForImportDeposit_ReturnsRule`, `Select_ProductRuleWithOtherModality_ReturnsNull`, `Select_RuleWithoutModality_AppliesToEveryModality` (IMP, EXP e INSP), `Select_ContextWithoutModality_IgnoresRulesWithModality`, `Select_Ladder_PrefersProductAndModality_ThenProduct_ThenModality_ThenGeneric`, `ExportDeposit_ImportOnlyAgreement_FallsToExportBaseRate_178500` (convenio solo IMP → null; tarifa base FIXED 150.000 EXP → regla; `InvoiceItem.Create(..., 1m, 150_000m, 19m).Total == 178_500m`), `InspectionDeposit_WithOnlyExportRules_HasNoRule`.
  - `Wms.Tests/Billing/Services/StorageFallbackWarningTests.cs`: `Build_InspectionWithoutRule_StatesZeroMinimum` (contiene «Se facturó el valor mínimo de Inspección ($0,00)»).
  - `Wms.IntegrationTests/Billing/StorageTariffResolutionTests.cs`: `ConfirmExportDeposit_WithImportOnlyAgreement_BillsExportBaseRate` (178.500) y `ConfirmInspectionDeposit_WithoutRules_BillsZeroMinimumWithWarning`.
- **Criterios de aceptación:**
  - Dado QA Cliente Uno con convenio de ALMACENAMIENTO `PERCENTAGE_OF_VALUE` solo para IMP001 (0,255 %, mínimo 184.000) y la tarifa base `FIXED` 150.000 solo para EXP001 con IVA 19 %, cuando CE confirma un depósito EXP001 de ese cliente con valor COP 50.000.000, entonces la factura de almacenamiento tiene una línea de 150.000 + IVA 28.500 = 178.500 con fuente «tarifa base».
  - Dado QA Cliente Mora sin convenio, la tarifa base `FIXED` 150.000 solo para EXP001 y el mínimo de INSP001 en $0, cuando CE confirma un depósito INSP001 de QA Cliente Mora con valor COP 5.000.000, entonces la factura sale en $0, su detalle dice que se aplicó el valor mínimo de Inspección y Facturación recibe el aviso.
  - Dado el mismo convenio de QA Cliente Uno, cuando CE confirma un depósito IMP001 con valor COP 200.000.000, entonces la factura es 510.000 + IVA 96.900 = 606.900 (sin cambio).
  - Dado un convenio de MONTACARGAS de QA Cliente Uno sin modalidad, cuando Bodega cierra un uso de montacargas Tractomula, entonces se cobra la tarifa del convenio (90.000) como hoy.
- **Re-test QA:** F6-TAR-004, F6-TAR-007, F6-INV-011, F6-ACC-005, E2E-06 (paso 5), E2E-08 (paso 3); REG F11-REG-021, F11-REG-031.
- **Riesgo de regresión:** medio. Reglas de servicios no de almacenamiento con modalidad dejan de aplicar; lo mitiga la consulta (b) del script, que se ejecuta antes del despliegue.
- **Tamaño:** S. **Dependencias:** CHG-01.

#### CHG-10 — El cierre manual abre el período siguiente desde el fin del cerrado

- **Cierra:** DEF-F6-002 (CRITICAL).
- **Causa raíz:** `Wms.Application/Billing/Commands/CloseStoragePeriods/CloseStoragePeriodsHandler.cs:53` calcula bien el fin del período cerrado, pero `:65` llama `StoragePeriodCalculator.RenewalStart(closedEnd, ColombiaTime.Today)` (`StoragePeriodCalculator.cs:43-47`), que devuelve hoy cuando fin + 1 es futuro. BA00002 (02/10–02/11) se cerró el 02/10 y el período nuevo volvió a empezar el 02/10. El job no falla porque usa `NextStart(EndOf(max PeriodEnd))` sin recorte (`BillingJobService.cs:240-241`). La prueba `Wms.Tests/Billing/StoragePeriodCalculatorTests.cs:95-101` fija el comportamiento errado.
- **Cambio exacto:**
  - Backend:
    - `StoragePeriodCalculator.cs`: eliminar `RenewalStart`; agregar `StartAfter(IEnumerable<DateTimeOffset> closedPeriodEnds)` = `NextStart(EndOf(closedPeriodEnds.Max()))`.
    - `CloseStoragePeriodsHandler.cs:53-65` y `BillingJobService.cs:240-241` usan `StartAfter`. El período siguiente empieza siempre el día posterior al fin del cerrado, aunque esa fecha sea futura (se cobra por adelantado): BA00002 → 03/11/2026–03/12/2026.
  - Frontend: ninguno (ninguna pantalla llama `POST billing/storage-periods/close`).
  - No se toca: `OpenPeriodWithInvoiceAsync` (idempotencia), `StorageRecalculationTrigger.cs:309-310` ni los avisos del cierre manual (los corrige CHG-62).
- **Migración o script:** sin migración. `fase-03-periodos-duplicados.sql`: detección de pares de períodos del mismo depósito con rangos solapados creados con más de un minuto de diferencia y la factura del duplicado; corrección, solo para duplicados en Borrador o Pendiente de aprobación no consolidados: `UPDATE invoices SET status = 'Cancelled', cancelled_at = now(), cancellation_reason = 'Período duplicado por cierre manual (DEF-F6-002)', updated_at = now() WHERE id IN (<facturas duplicadas>) AND status IN ('Draft','PendingApproval') AND is_consolidated = false;` y `UPDATE storage_billing_periods SET status = 'Closed', closed_at = now(), closed_by_id = '<id de un Admin>', updated_at = now() WHERE id IN (<períodos duplicados>) AND status = 'Open';`. Los duplicados dentro de una consolidada o ya emitidos (BA00017 y los aprobados) se ajustan en SIIGO.
- **Pruebas automatizadas nuevas:**
  - `Wms.Tests/Billing/StoragePeriodCalculatorTests.cs`: se reemplaza `RenewalStart_IsContiguousUnlessItWouldBeInTheFuture` por `StartAfter_ManualCloseBeforeTheEnd_IsStillEndPlusOne` (fin 2026-11-02 → 2026-11-03), `StartAfter_SeveralPeriods_UsesTheLatestEnd` (fines 2026-10-09 y 2026-11-02 → 2026-11-03) y `Next_MonthlyFromNov3_EndsDec3WithLimitDec6`.
  - `Wms.IntegrationTests/Billing/ManualPeriodCloseTests.cs`: `CloseBeforeEnd_OpensNextPeriodFromEndPlusOne` y `CloseWeekly_OpensFromEndPlusOneLikeTheJob`.
- **Criterios de aceptación:**
  - Dado 2026BA00002 con el período mensual 02/10/2026–02/11/2026 abierto y facturado por 501.865,34, cuando Facturación ejecuta `POST billing/storage-periods/close` el 03/10/2026, entonces el período queda cerrado con su factura y se abre 03/11/2026–03/12/2026 con una factura nueva; no existe otra factura por 02/10–02/11.
  - Dado un depósito con ciclo semanal y período 02/10–09/10, cuando se cierra manualmente, entonces el período nuevo es 10/10–17/10, igual que la renovación del job.
  - Dado 2026BA00028 con stock 110 y período 03/10–03/11, cuando se cierra manualmente, entonces el período nuevo es 04/11–04/12 y su factura es 110 × 1.500 + IVA = 196.350.
- **Re-test QA:** F6-ALM-008, F6-FOR-005, E2E-13 (paso 1); REG F11-REG-021.
- **Riesgo de regresión:** bajo; job y cierre manual comparten la misma función.
- **Tamaño:** S. **Dependencias:** CHG-01.

#### CHG-11 — El override fija el total de la línea, con IVA incluido y rotulado

- **Cierra:** DEF-F6-003 (CRITICAL), DEF-F6-004 (CRITICAL).
- **Causa raíz:** `Wms.Domain/Entities/Billing/InvoiceItem.cs:156-159` asigna el monto digitado al precio unitario neto, lo multiplica por la cantidad y le suma el IVA (cantidad 6, 8.000 → 48.000 + 9.120 = 57.120). `OverrideBillingAmountHandler.cs:31` guarda como original el subtotal neto (`UnitPrice * Quantity`), mientras `app/pages/billing/invoices/[id].vue:524` abre el diálogo con el total con IVA y `app/features/billing/components/OverrideAmountDialog.vue:122-125` lo rotula «Monto original» sin decir la base (184.000 mostrado, 178.500 digitado → 212.415).
- **Base elegida (aplica §10 · IVA en valores digitados):** el valor que se digita es el **total de la línea con IVA incluido**. Es lo que el operario ve en la columna «Total» y en el original del diálogo, y es la misma base del «Total a pagar» de báscula y guías (`BillingCollectForm.vue:630`, descompuesto por `BillingRecipientFactory.SplitTotal`). El IVA de una línea ya generada es propiedad de la línea (`TaxRate`), no una elección del override.
- **Cambio exacto:**
  - Backend:
    - Nuevo `Wms.Domain/Billing/VatMath.cs` (estático): `SplitTotal(decimal total, decimal taxRatePercent)` → `(subtotal = Round(total / (1 + tasa/100), 2, AwayFromZero), iva = total − subtotal)` y `ToNet(decimal gross, decimal taxRatePercent)`. `BillingRecipientFactory.SplitTotal` (`BillingRecipientFactory.cs:35-52`) delega en él.
    - `InvoiceItem.Override(decimal newTotal, string reason, Guid userId)`: `SubTotal` e `TaxAmount` salen de `VatMath.SplitTotal(newTotal, TaxRate)`, `Total = newTotal`, `UnitPrice = Round(SubTotal / Quantity, 2, AwayFromZero)`, `IsOverridden = true`; la cantidad no cambia. Se conservan «Esta línea ya fue sobrescrita.» y «El monto de sobrescritura debe ser mayor a cero.».
    - `OverrideBillingAmountHandler.cs:31-52`: el original es `invoiceItem.Total` (antes del override); `BillingAmountOverride.Create(item.Id, originalTotal, request.NewAmount, …)`; la respuesta agrega `NewSubTotal` y `NewTaxAmount`. El campo del request sigue siendo `NewAmount`; su documentación XML (`BillingController.cs:61-70`) dice «nuevo total de la línea, IVA incluido».
  - Frontend:
    - `OverrideAmountDialog.vue`: nueva prop `taxRate`; título «Sobrescribir total de la línea»; texto «Total actual de la línea (IVA incluido): $ 184.000» (con `taxRate` 0: «Total actual de la línea (sin IVA): …»); etiqueta del campo «Nuevo total de la línea (IVA incluido) *»; debajo, el desglose en vivo «Base $ 150.000 + IVA 19 %: $ 28.500 = Total $ 178.500» con la misma fórmula; mensaje de validación «El nuevo total debe ser diferente al total actual de la línea.».
    - `app/pages/billing/invoices/[id].vue`: `openOverrideDialog(data.id, data.total, data.taxRate)` (`:71-75`, `:524`), `:tax-rate` en el diálogo (`:633-639`) y tooltip `:508` «Total original (IVA incluido): …».
    - `app/features/billing/types/billing-override.ts`: `newAmount` documentado como total con IVA; respuesta con `newSubTotal` y `newTaxAmount`.
  - No se toca: la regla «solo en Borrador» (`OverrideBillingAmountHandler.cs:25-26`), `useBillingOverride.ts`, `InvoiceItem.Update`.
- **Migración o script:** sin migración (cambia el significado de `billing_amount_overrides.original_amount` y `override_amount`: ambos pasan a ser totales con IVA). `fase-03-overrides.sql`: detección de líneas sobrescritas cuyo total difiere de lo digitado (`ABS(ii.total - bo.override_amount) > 0.01`); corrección en una transacción, solo para facturas en Borrador o Pendiente de aprobación: recalcular `sub_total`, `tax_amount`, `total` y `unit_price` de la línea con el total digitado, recalcular `sub_total`, `tax_amount`, `total` y `pending_amount` de la factura desde sus líneas, y pasar los `original_amount` anteriores al despliegue de neto a total (`ROUND(original_amount * (1 + tax_rate / 100), 2)`). Las facturas aprobadas, enviadas o pagadas de la detección se ajustan en SIIGO.
- **Pruebas automatizadas nuevas:**
  - `Wms.Tests/Domain/Billing/InvoiceItemOverrideTests.cs`: `Override_Quantity6Vat19_SetsTotalTo8000` (Total 8.000, SubTotal 6.722,69, TaxAmount 1.277,31, UnitPrice 1.120,45, Quantity 6), `Override_Export184000To178500_Gives150000Plus28500`, `Override_Api95000Qty1_Gives79831_93Plus15168_07`, `Override_ZeroTaxLine_TotalEqualsTyped`, `Override_Twice_Throws`.
  - `Wms.Tests/Domain/Billing/VatMathTests.cs`: `SplitTotal_178500At19_Gives150000And28500`, `SplitTotal_8000At19_Gives6722_69And1277_31`, `ToNet_184000At19_Gives154621_85`.
  - `test/components/billing/OverrideAmountDialog.spec.ts`: `muestra la base IVA incluido y el desglose` (total actual 184.000, tasa 19; al digitar 178.500 el texto contiene «Base $ 150.000» e «IVA 19 %: $ 28.500»).
- **Criterios de aceptación:**
  - Dado la línea «Almacenamiento QA Cebolla» de BA00013 con cantidad 6 e IVA 19 % en una factura en Borrador, cuando Facturación sobrescribe el total con 8.000, entonces la línea queda en 8.000 (subtotal 6.722,69 + IVA 1.277,31) y el total de la factura se recalcula.
  - Dado la línea de EXP00001 con total 184.000, cuando Facturación abre «Sobrescribir total de la línea», entonces ve «Total actual de la línea (IVA incluido): $ 184.000»; al digitar 178.500 ve «Base $ 150.000 + IVA 19 %: $ 28.500 = Total $ 178.500» y, al guardar, la línea queda en 178.500.
  - Dado una línea de cantidad 1 e IVA 19 %, cuando se envía por API `newAmount` 95.000, entonces la línea queda en 95.000 (79.831,93 + 15.168,07).
  - Dado el override del segundo criterio, cuando se consulta su registro, entonces `originalAmount` es 184.000 y `overrideAmount` es 178.500.
- **Re-test QA:** F6-OVR-002, F6-OVR-003, F6-OVR-004; REG F11-REG-022, F11-REG-031.
- **Riesgo de regresión:** bajo; el override solo lo usa la pantalla de detalle de factura.
- **Tamaño:** M. **Dependencias:** CHG-01.

#### CHG-12 — Solo vencen las facturas emitidas; el vencimiento se fija al aprobar

- **Cierra:** DEF-F6-005 (CRITICAL).
- **Causa raíz:** los cobros «por facturar» crean la factura con vencimiento igual al instante de creación: `StartWeighingOnlyPendingBillingHandler.cs:93`, `StartStoragePendingBillingHandler.cs:119`, `StartOutputPendingBillingHandler.cs:99`, `EndForkliftUseCommandHandler.cs:134` y `CreateDispatchGuideCommandHandler.cs:333` (`dueDate: DateTimeOffset.UtcNow`); los demás creadores calculan el vencimiento al crear (`StorageBillingService.cs:415-421`, `BillingService.cs:65-73`, `CreateDispatchGuideCommandHandler.cs:255`, `ReissueInvoiceCommandHandler.cs:57`). `BillingJobService.cs:25-32` toma toda factura con `DueDate < now` salvo Paid, Cancelled y Overdue, así que marca Overdue a Borradores y Pendientes de aprobación, que luego no se pueden numerar ni aprobar (`Invoice.cs:337,441`) y suman a la deuda vencida del cliente (`BillingJobService.cs:41-49`).
- **Cambio exacto:**
  - Backend:
    - `Invoice.cs:335-352` → `Approve(Guid approvedById, DateTimeOffset dueDate)` fija `DueDate`. Es el único lugar donde se asigna el vencimiento.
    - `ApproveInvoiceHandler.cs`: inyecta `IBillingService`, obtiene `GetPaymentTermDaysAsync(invoice.CustomerId ?? Guid.Empty)` (30 días sin configuración, `BillingService.cs:12,171-180`) y llama `invoice.Approve(request.ApprovedById, DateTimeOffset.UtcNow.AddDays(term))`.
    - Los creadores de factura listados en la causa y `BillingRecipientFactory.cs:67-92` dejan de pasar `dueDate`: Borradores y Pendientes nacen con `DueDate` nulo; `Invoice.CreateReissueOf` deja de recibir la fecha.
    - `BillingJobService.cs:25-32` (detección) y `NotifyUpcomingDueDatesAsync` (`:298-307`) filtran por estado emitido: `Approved`, `Sent` y `PartiallyPaid` (el barrido completo lo reescribe CHG-13).
  - Frontend: ninguno (`app/pages/billing/invoices/index.vue:125-128` ya muestra «—» con vencimiento nulo).
  - No se toca: `GetOverdueClientsHandler.cs`, `GetBillingDashboardHandler.cs` y `GetOperationalStatisticsHandler.cs:157`, que leen `Status == Overdue` y quedan correctos al garantizar que solo las emitidas vencen.
- **Migración o script:** sin migración (`invoices.due_date` ya es nulable). `fase-03-vencimientos.sql`: detección `SELECT id, invoice_number, status, due_date, total, pending_amount FROM invoices WHERE status = 'Overdue' AND approved_at IS NULL;`; corrección: `UPDATE invoices SET status = 'Draft', due_date = NULL, updated_at = now() WHERE status = 'Overdue' AND approved_at IS NULL AND COALESCE(amount_paid, 0) = 0;`, `UPDATE invoices SET due_date = NULL, updated_at = now() WHERE status IN ('Draft','PendingApproval') AND due_date IS NOT NULL;` y, para emitidas con vencimiento anterior o igual a su aprobación, `due_date = approved_at + días de plazo del cliente (30 sin configuración)`. Las `Overdue` sin aprobar con pagos las trata CHG-22.
- **Pruebas automatizadas nuevas:**
  - `Wms.Tests/Domain/Billing/InvoiceOverdueStatusTests.cs`: `Approve_SetsDueDateFromTheGivenDate`.
  - Ajuste de llamadores de `Approve` en `InvoiceActionRulesTests.cs:32,68`, `InvoiceStorageRecalculationTests.cs:56` e `InvoiceReissueTests.cs:36,68`.
  - `Wms.IntegrationTests/Billing/PendingBillingDueDateTests.cs`: `PendingBillingInvoice_HasNoDueDate_AndJobKeepsItDraft` y `Approve_SetsDueDateFromCustomerTerm` (30 días).
- **Criterios de aceptación:**
  - Dado un cobro de báscula «por facturar» de QA Cliente Consolidado (factura en Borrador por 57.120), cuando corre el job de vencidas, entonces la factura sigue en Borrador, sin vencimiento, y Facturación le asigna el N.º SIIGO y la aprueba.
  - Dado esa factura, cuando Facturación la aprueba el 03/10/2026 y el cliente tiene 30 días de plazo, entonces su vencimiento es el 02/11/2026.
  - Dado el Borrador de montacargas de 80.000 de QA Cliente Mora, cuando corre el job, entonces no pasa a Overdue y no suma a la deuda vencida del cliente.
- **Re-test QA:** F6-CAR-005, F6-CON-003, F6-INV-008, E2E-07 (paso 3), E2E-12 (paso 1); REG F11-REG-022, F11-REG-025.
- **Riesgo de regresión:** bajo; los reportes que mostraban vencimiento en Borradores pasan a «—».
- **Tamaño:** M. **Dependencias:** CHG-01.

#### CHG-13 — Mora en una sola corrida y pagos parciales que vencen

- **Cierra:** DEF-F6-006 (CRITICAL).
- **Causa raíz:** cuatro fallas encadenadas: (1) `Wms.Domain/Entities/Billing/Invoice.cs:402` compara `AmountPaid < Total` con `AmountPaid` nulo y no marca nada en la primera corrida; (2) `Wms.Application/Billing/Jobs/BillingJobService.cs:41-49` calcula la deuda por cliente con una consulta anterior al `SaveChangesAsync` (`:106`) y no ve los Overdue recién marcados; (3) la conciliación (`BillingJobService.cs:142` → `Invoice.cs:587-589`) devuelve a PartiallyPaid una factura vencida con pago parcial; (4) registrar, verificar o rechazar un pago no recalcula el estado del cliente (`RecordPaymentHandler.cs`, `VerifyPaymentHandler.cs`, `RejectPaymentHandler.cs`).
- **Cambio exacto:**
  - Backend:
    - `Invoice.cs`: nuevo `RefreshStatus(DateTimeOffset now)`, única fuente del estado de una factura emitida; lo usan `RecordPayment` (`:372-393`), `ReplaceStorageLines` (`:551-563`), `ReconcilePayments(decimal paid, DateTimeOffset now)` (`:570-597`) y el job (reemplaza `MarkAsOverdue`, `:395-407`). Reglas: Draft, PendingApproval y Cancelled no cambian; emitida con total > 0 y saldo 0 → Paid; saldo > 0 y vencida → Overdue (con o sin pagos parciales); saldo > 0, no vencida y pagado > 0 → PartiallyPaid; saldo > 0, no vencida y sin pagos → Sent si `SentAt` existe, si no Approved; Paid de contado sin aprobación con pago rechazado y saldo > 0 → Draft. `AmountPaid` nulo vale 0. `RecordPayment` sobre un Borrador de contado conserva el paso a Paid.
    - Nueva clase pura `Wms.Application/Billing/Jobs/OverdueSweep.cs`: `Apply(IEnumerable<Invoice>, DateTimeOffset now)` refresca los estados y devuelve la deuda vencida por cliente (Σ `PendingAmount` de las Overdue con `CustomerId`); y `ClientFinancialStatusRules.Resolve(decimal overdueTotal, decimal? creditLimit)`: deuda 0 → Active; deuda > límite → Blocked; deuda ≤ límite o sin límite → OverdueWarning (sin límite nunca Blocked, §10 · Mora).
    - `BillingJobService.DetectOverdueAndRecalculateStatusAsync` (`:21-109`) en una sola corrida: carga con `Include(i => i.Payments)` las facturas Approved, Sent, PartiallyPaid y Overdue; concilia con la suma de pagos Received y Verified; aplica `OverdueSweep`; actualiza el estado de cada cliente con `ClientFinancialStatusRules` y devuelve a Active a los demás; un único `SaveChangesAsync`. El log informa transiciones reales.
    - `ConsolidateDailyChargesAsync` (`:124-143`) concilia solo facturas emitidas con `ReconcilePayments(paid, now)`: ya no baja Overdue a PartiallyPaid.
    - `IBillingService.RefreshFinancialStatusAsync(Guid stakeholderId)` (en `BillingService.cs`, con `ClientFinancialStatusRules`): se llama después del `SaveChangesAsync` y antes del commit en `RecordPaymentHandler.cs:63`, `VerifyPaymentHandler.cs`, `RejectPaymentHandler.cs` y `CancelInvoiceHandler.cs`. Pagar desbloquea en la misma operación.
  - Frontend: ninguno (una factura vencida con pago parcial se ve «Vencida» y su «Pagado» en el detalle).
  - No se toca: `OverdueDetectionBackgroundService`, `DailyChargeConsolidationBackgroundService` ni `BillingService.ValidateFinancialStatusAsync`.
- **Migración o script:** sin migración. `fase-03-vencimientos.sql` agrega la verificación posterior, que debe devolver 0 filas: `SELECT status, COUNT(*) FROM invoices WHERE status IN ('Approved','Sent','PartiallyPaid') AND pending_amount > 0 AND due_date < now() GROUP BY status;`, y la lista previa al despliegue de clientes cuya deuda vencida supera su límite (quedarán Blocked en la primera corrida).
- **Pruebas automatizadas nuevas:**
  - `Wms.Tests/Domain/Billing/InvoiceOverdueStatusTests.cs`: `RefreshStatus_ApprovedPastDueWithNullAmountPaid_BecomesOverdue`, `RefreshStatus_PartiallyPaidPastDue_BecomesOverdueWithBalance` (501.865,34 con pago 100.000 → Overdue, pendiente 401.865,34), `RefreshStatus_DraftPastDue_StaysDraft`, `RefreshStatus_PendingApprovalPastDue_StaysPendingApproval`, `ReconcilePayments_OverdueWithPartialPayment_StaysOverdue`, `ReconcilePayments_NotDueWithPartialPayment_BecomesPartiallyPaid`, `RecordPayment_PartialOnOverdue_StaysOverdue`, `ReconcilePayments_RejectedPaymentOnCashInvoice_BackToDraft`.
  - `Wms.Tests/Billing/OverdueSweepTests.cs`: `Apply_MoraApprovedPastDue_ReturnsDebtInFirstRun` (17.850), `Apply_PartiallyPaidInvoice_CountsItsBalance` (401.865,34), `Apply_Drafts_AreExcluded`.
  - `Wms.Tests/Billing/ClientFinancialStatusRulesTests.cs`: 17.850 con límite 1.000 → Blocked; deuda > 0 con límite 0 → Blocked; sin límite → OverdueWarning; deuda 0 → Active; deuda igual al límite → OverdueWarning.
  - `Wms.IntegrationTests/Billing/OverdueJobTests.cs`: `SingleRun_MarksOverdueAndBlocksMoraClient`, `PartiallyPaidPastDue_CountsAsOverdueDebt`, `FullPayment_UnblocksClientImmediately`.
- **Criterios de aceptación:**
  - Dado QA Cliente Mora (límite 1.000) con una factura aprobada de 17.850 vencida hace 2 días y sin pagos, cuando corre una sola vez el job de vencidas, entonces la factura queda Overdue y el cliente Blocked.
  - Dado QA Cliente Uno (sin límite) con QA-SIIGO-0011 de 501.865,34, un pago de 100.000 y vencida, cuando corren el job y la conciliación, entonces la factura queda Overdue con saldo 401.865,34, ese saldo cuenta como deuda vencida y el cliente queda OverdueWarning, nunca Blocked.
  - Dado QA Cliente Mora Blocked, cuando Facturación registra el pago total de su factura vencida, entonces el cliente queda Active en la misma operación y báscula le cobra sin esperar el job.
  - Dado una factura Overdue con pago parcial, cuando corre la conciliación diaria, entonces sigue Overdue.
- **Re-test QA:** F6-CAR-001, F6-CAR-002, F6-CAR-003, E2E-12; REG F11-REG-025, F11-REG-031.
- **Riesgo de regresión:** medio; el estado de factura pasa a una sola regla usada por pagos, recálculo y job. Lo cubren las pruebas de `InvoiceOverdueStatusTests` y E2E-12.
- **Tamaño:** M. **Dependencias:** CHG-12.

### Fase 4 — MAJOR de seguridad y del cobro en báscula

- **Objetivo:** cerrar los MAJOR que comprometen la seguridad (autor elegido por el cliente, sesión que no se revoca, política de contraseña) y los que cobran mal o dos veces en báscula (doble envío, destinatario por defecto, operación retomada tras recargar), más el bloqueo de Comercio Exterior para completar un depósito en Borrador. Cierra DEF-F9-003, DEF-F1-009, DEF-F1-002, DEF-F3-002 (con DEF-F8-001 unificada), DEF-F10-001, DEF-F3-007, DEF-F3-006, DEF-F3-017, DEF-F5-001 y, por compartir causa, DEF-F4-012, DEF-F3-018 y DEF-F10-002.
- **Criterio de entrada:** checkpoint de la Fase 3 aprobado.
- **Cambios:** CHG-14, CHG-15, CHG-16, CHG-17, CHG-18, CHG-19, CHG-20, CHG-21.
- **Orden interno:** CHG-14 → CHG-15 (usa `GetRequiredUserId` de CHG-08) → CHG-16 → CHG-17 → CHG-18 → CHG-19 → CHG-20 (los dos últimos tocan `app/pages/operations/weighbridge/index.vue` en bloques distintos) → CHG-21.
- **Migración de la fase (la genera el implementador con `dotnet ef`):** `AddLoadingOrderSignatureAndWeighbridgeIdempotency`: columna `loading_orders.signature_driver` (`text`, nula); columna `service_record_entry_logs.is_primary` (`boolean NOT NULL`, el `AddColumn` rellena `false`); índice único parcial `idx_service_record_entry_logs_primary_entry_log_unique` sobre `(entry_log_id) WHERE is_primary`; índice único parcial `idx_weighbridge_cycle_active_service_entry_unique` sobre `weighbridge_cycles(service_record_id, entry_log_id) WHERE status <> 'Canceled'`; índice único parcial `idx_service_record_active_output_per_order_unique` sobre `service_records(loading_order_id) WHERE service_type = 'OutputCargo' AND status <> 'Discarded'`.
- **Riesgos y mitigación:**
  - Bloqueos y transacciones nuevos en nueve handlers de báscula. Mitigación: orden de bloqueo fijo (primero el ingreso, después la orden de cargue), pruebas de concurrencia en `Wms.IntegrationTests` y medición del tiempo de registro en el re-test (meta de ~30 s, PRF-002).
  - Los tokens emitidos antes del despliegue no traen el sello de seguridad: la primera petición responde 401 y la aplicación los renueva con el refresh (`app/plugins/api-client.ts:100-125`). Mitigación: comportamiento esperado; se avisa a los usuarios que verán un refresco de sesión.
  - La migración falla si quedan ciclos duplicados o salidas duplicadas por orden. Mitigación: la primera parte de `fase-04-idempotencia.sql` va antes de la migración.
- **Saneamiento de datos:** `fase-04-autoria.sql` (detección y corrección en ambientes de prueba) y `fase-04-idempotencia.sql` (antes y después de la migración), descritos en cada cambio.
- **Criterio de salida:** compuertas comunes (regla 4.0.4) y en PASA: F1-AUT-011, F9-API-020, F4-CAR-010, F2-SAL-009, F1-USR-015, F1-USR-010, F1-AUT-018, F9-SES-001, F9-SES-002, F3-COB-013, F3-COB-001, E2E-18, E2E-20, F10-ERR-007, F10-UX-003, F10-UX-005, F10-ERR-006, F3-COB-003, F3-REI-003, F3-REI-005, F3-REI-009, F3-REI-010, F5-CNF-001; REG F11-REG-001, F11-REG-007, F11-REG-008, F11-REG-010, F11-REG-016, F11-REG-017, F11-REG-019, F11-REG-020, F11-REG-023, F11-REG-031.
- **Checkpoint:** se entrega al usuario el resultado de las pruebas de concurrencia (registro y cobro simultáneos), la lista de registros con autor corregido en la base de prueba y la evidencia del cierre de sesión inmediato. El usuario aprueba la migración aplicada y el saneamiento en staging, y cronometra con el operario el registro de un camión (PRF-002) para confirmar que los bloqueos no lo hacen más lento.

#### CHG-14 — FluentValidation corre también en los comandos sin respuesta

- **Cierra:** DEF-F1-002 (MAJOR).
- **Causa raíz:** `Wms.Api/Common/Behaviors/ValidationBehavior.cs:6` declara `where TRequest : IRequest<TResponse>`. En MediatR 12, `IRequest` (sin respuesta) no hereda de `IRequest<Unit>`, así que el comportamiento no se cierra para esos comandos y sus validadores nunca corren: `ChangePasswordValidator.cs:10-12` (`MustBeStrongPassword`) no se ejecuta y solo responde Identity con «Error al cambiar la contraseña» (`ChangePasswordHandler.cs:41-46`). Afecta además a `ResetPasswordWithToken`, `RequestPasswordReset`, `CloseStoragePeriods`, `DeleteEntryReason`, `DeleteUnitMeasure`, `DeleteCity`, `DeletePackagingType`, `DeleteCargoUnitType`, `DeleteServicePricingRule` y `DeleteServicePrice`.
- **Cambio exacto:**
  - Backend: `ValidationBehavior.cs:6` → `where TRequest : IBaseRequest` (registro de `Program.cs:42` sin cambios).
  - Frontend: ninguno (`app/utils/password-schema.ts:4-19` ya aplica la misma política).
  - No se toca: los once comandos (no se convierten a `IRequest<Unit>`) ni `ChangePasswordHandler`.
- **Migración o script:** ninguno. Las cuentas de QA con contraseña débil se restablecen con el reset del Admin.
- **Pruebas automatizadas nuevas:**
  - `Wms.Tests/Auth/ChangePasswordValidatorTests.cs`: `NoSpecialCharacter_Fails` («Debe contener al menos un caracter especial»), `ContainsSpace_Fails` («No puede contener espacios»), `DisallowedSpecialCharacter_Fails`, `HundredAndOneCharacters_Fails` («La contraseña no puede exceder 100 caracteres»), `ValidPassword_Passes` (`Abcd#1234`).
  - `Wms.Tests/Security/ValidationBehaviorTests.cs`: `Send_VoidCommandWithFailingValidator_ThrowsValidationException` y `Send_TypedCommandWithFailingValidator_ThrowsValidationException`.
- **Criterios de aceptación:**
  - Dado un usuario con contraseña temporal, cuando llama `POST auth/change-password` con `Abcd12345`, entonces responde 400 con el error «Debe contener al menos un caracter especial» y la contraseña no cambia; con `Abc# 12345` el error es «No puede contener espacios»; con `Abcd-12345`, «Debe contener al menos un caracter especial»; con 101 caracteres, «La contraseña no puede exceder 100 caracteres».
  - Dado el mismo usuario, cuando envía `Abcd#1234`, entonces responde 204 y la contraseña cambia.
  - Dado `DELETE entry-reasons/{id}` con un id mal formado, cuando lo llama Admin, entonces responde 400 (no 500).
- **Re-test QA:** F1-AUT-011; REG F11-REG-001.
- **Riesgo de regresión:** bajo; los once comandos pasan a validarse como el resto.
- **Tamaño:** S. **Dependencias:** CHG-01.

#### CHG-15 — El autor de cada operación sale del token y la firma del cargue es obligatoria

- **Cierra:** DEF-F9-003 (MAJOR), DEF-F4-012 (MINOR).
- **Causa raíz:** el autor viaja en el cuerpo y los handlers lo guardan sin compararlo con el token: `CreateEntryLogCommand.cs:8` (`EntryLogController.cs:25`), `RegisterDepartureRequest.DepartureAuthorizedById` (`EntryLogController.cs:69-71, 108`), `CreateDepartureAuthorizationRequest.DepartureAuthorizedById` (`:81-85, 109`), `ExecuteLoadingOrderRequest.CompletedBy` (`WarehouseController.cs:848-860, 1158`, usado en `ExecuteLoadingOrderCommandHandler.cs:47-50, 188, 322, 378`) y ocho campos de `BillingController.cs` (`OverriddenBy`, `CreatedById`, `ApprovedById`, `CancelledById`, `ReceivedById`, `RecordedById`, `VerifiedById`, `ClosedById`; p. ej. `:332-345`). `ExecuteLoadingOrderCommandValidator.cs:39-40` solo limita el tamaño de la firma y el handler nunca la guarda (`LoadingOrder` no tiene columna), aunque el XML del endpoint dice «Guarda firma».
- **Cambio exacto:**
  - Backend:
    - `EntryLogController.cs`: `CreateEntryLog` recibe `CreateEntryLogRequest` sin autor y arma el comando con `User.GetRequiredUserId()`; `RegisterDepartureRequest` queda `(DateTimeOffset? DateTimeDeparture)` y `CreateDepartureAuthorizationRequest` queda `(string? Observations)`, ambos con el autor del token.
    - `WarehouseController.cs`: se elimina `CompletedBy` de `ExecuteLoadingOrderRequest` (`:1158` y su `<param>`); `:857` pasa `User.GetRequiredUserId()`. `ExecuteLoadingOrderCommandValidator.cs:39-40`: `SignatureDriver` no vacía («La firma del conductor es requerida.», mismo texto de `CreateReceptionCommandValidator.cs:30-31`) y máximo 500 000 caracteres.
    - `Wms.Domain/Entities/Warehouse/LoadingOrder.cs`: propiedad `SignatureDriver` (`string?`) y `CompleteLoading(Guid completedBy, string signatureDriver, string? sealNumber = null)`, que rechaza una firma vacía con `BadRequestException("La firma del conductor es requerida.")`; el handler (`:322`) pasa la firma. `LoadingOrderConfiguration.cs`: `Property(lo => lo.SignatureDriver).HasColumnType("text").IsRequired(false)`. La auditoría ya excluye `SignatureDriver` (CHG-02).
    - `BillingController.cs`: se eliminan los ocho campos de autor de los records de petición (`:679-682, 690, 715, 720, 734-735, 737, 747`) y las acciones usan `User.GetRequiredUserId()` (`:78-82, 144-149, 244, 283, 332-345, 400, 542`).
  - Frontend: se quita el campo de autor de tipos y cargas: `app/features/entries/types/entry-log.ts:45,75,96`; `app/pages/operations/entries/index.vue:205`, `exits.vue:113` (envía `{}`) y `history.vue:176,184`; `app/features/warehouse/types/loading-order.ts:102` y `LoadingOrderExecutionDialog.vue:153-157,191` (y el `useUserStore` que solo servía para eso); `app/features/billing/types/requests.ts:67,91,95,113,118`, `InvoiceActionsDialog.vue:123,179`, `app/pages/billing/payments/index.vue:141`, `app/pages/billing/invoices/[id].vue:106` y `app/features/billing/services/billing-engine.service.ts:8,24-34`.
  - No se toca: los comandos de Facturación con pruebas existentes (`CancelInvoiceCommand`, `ApproveInvoiceCommand`): el controlador les pasa el usuario del token; `CreateReceptionCommandHandler` y `CompleteReceptionCommandHandler`, que ya toman el usuario del token.
- **Migración o script:** columna `loading_orders.signature_driver` de `AddLoadingOrderSignatureAndWeighbridgeIdempotency`. `fase-04-autoria.sql`: detección de salidas cuyo `departure_authorized_by_id` difiere del usuario que la registró en `audit_logs`, de movimientos de inventario cuyo `authorized_by` difiere del usuario auditado y de órdenes cuyo `completed_by` difiere del usuario auditado; en ambientes de prueba se corrige con `UPDATE … SET <autor> = a.user_id FROM audit_logs a WHERE …` (mismas uniones). Las firmas de cargues anteriores no se guardaron y no son recuperables.
- **Pruebas automatizadas nuevas:**
  - `Wms.Tests/Security/ClientAuthorshipGuardTests.cs`: `BodyModels_DoNotExposeAuthorFields` (recorre los tipos `[FromBody]` de los controladores y falla si una propiedad pública sin `[JsonIgnore]` se llama `AuthorizedBy*`, `CompletedBy*`, `ApprovedBy*`, `CancelledBy*`, `VerifiedBy*`, `ClosedBy*`, `CreatedBy*`, `ReceivedBy*`, `RecordedBy*`, `OverriddenBy*` o `PerformedBy*`).
  - `Wms.Tests/Warehouse/ExecuteLoadingOrderCommandValidatorTests.cs`: `Validate_EmptySignature_FailsWithMessage`, `Validate_WithSignature_Passes`, `Validate_SignatureOver500000Chars_Fails`.
  - `Wms.Tests/Domain/Warehouse/LoadingOrderTransitionsTests.cs`: `CompleteLoading_WithSignature_StoresSignatureAndCompletedBy`, `CompleteLoading_BlankSignature_ThrowsBadRequest` (se ajusta el helper `OrderIn`, `:117`).
  - `Wms.IntegrationTests/Security/AuthorFromTokenTests.cs`: `RegisterDeparture_ForeignAuthorInBody_StoresTokenUser`, `ExecuteLoadingOrder_WithoutSignature_Returns400`, `RecordPayment_ReceivedByInBody_IsIgnored`.
- **Criterios de aceptación:**
  - Dado `vigilancia`, cuando registra la salida de QAF901 enviando en el cuerpo el id de `facturacion` como autorizador, entonces la salida queda autorizada por `vigilancia`.
  - Dado `bodega`, cuando ejecuta un cargue por API sin `signatureDriver`, entonces responde 400 «La firma del conductor es requerida.»; con firma y un `completedBy` de otro usuario, el cargue queda completado por `bodega` y la firma queda guardada en la orden.
  - Dado `facturacion`, cuando registra un pago enviando `receivedById` de otro usuario, entonces el pago queda recibido y registrado por `facturacion`.
- **Re-test QA:** F9-API-020, F4-CAR-010, F2-SAL-009; REG F11-REG-016, F11-REG-023.
- **Riesgo de regresión:** bajo; System.Text.Json ignora propiedades desconocidas, así que un cliente que aún envíe el autor no falla.
- **Tamaño:** M. **Dependencias:** CHG-08, CHG-02.

#### CHG-16 — El acceso se corta al desactivar, cambiar roles o cerrar sesión

- **Cierra:** DEF-F1-009 (MAJOR).
- **Causa raíz:** `Wms.Api/Common/Identity/WmsAuthentication.cs:38-67` valida firma y vencimiento del JWT y no consulta al usuario (los eventos solo implementan `OnMessageReceived`); `Wms.Infrastructure/Services/TokenService.cs:62-69` no incluye el `SecurityStamp`; desactivar (`ManageUserActivationHandler.cs:44-56`), asignar y quitar roles (`AssignRolesToUserHandler.cs:44-49`, `RemoveRolesToUserHandler.cs:43-48`) y cerrar sesión (`LogoutHandler.cs:8-12`, solo revoca el refresh) no rotan el sello. El access token sigue válido hasta vencer (`Jwt:AccessTokenExpirationMinutes`, `TokenService.cs:39-46`).
- **Cambio exacto:**
  - Backend:
    - `Wms.Domain/Contracts/WmsClaimTypes.cs` (nuevo): `SecurityStamp = "sstamp"`; `TokenService.cs:62-69` agrega ese claim con `user.SecurityStamp`.
    - `Wms.Domain/Services/IUserSessionGuard.cs` (nuevo) con `IsSessionValidAsync(Guid userId, string? tokenStamp)` e `Invalidate(Guid userId)`; implementación `Wms.Infrastructure/Services/UserSessionGuard.cs`: lee `is_active` y `security_stamp` del usuario sin rastreo, los guarda 15 s en `IMemoryCache` y decide con la regla pura `Wms.Domain/Security/SessionValidityRules.IsValid(userExists, isActive, currentStamp, tokenStamp)` (válido solo si existe, está activo y el sello del token no está vacío y es igual al actual). Registro `AddScoped` en `Wms.Infrastructure/DependencyInjection.cs`.
    - `WmsAuthentication.cs`: evento `OnTokenValidated` que consulta el guardián y, si no es válido, hace `context.Fail("La sesión ya no es válida.")` (401).
    - `await userManager.UpdateSecurityStampAsync(user)` y `sessionGuard.Invalidate(user.Id)` en desactivar (más `RevokeAllRefreshTokensAsync`), asignar roles, quitar roles y cerrar sesión; `Invalidate` y revocación de refresh en `ResetUserPasswordHandler.cs:22-27` y `ResetPasswordWithTokenHandler.cs` (Identity ya rota el sello al restablecer).
  - Frontend: ninguno (`app/plugins/api-client.ts:100-125` responde a un 401 con un refresh y un reintento, y a un refresh fallido con cierre de sesión).
  - No se toca: la vida del token (60 min en `appsettings.Development.example.json:11`, `deploy/staging/compose.staging.yaml:44` e `infra/main.tf:107`) ni `ChangePasswordHandler`.
- **Migración o script:** ninguno (los tokens previos sin `sstamp` se renuevan solos).
- **Pruebas automatizadas nuevas:**
  - `Wms.Tests/Security/SessionValidityRulesTests.cs`: `IsValid_ActiveUserSameStamp_ReturnsTrue`, `IsValid_InactiveUser_ReturnsFalse`, `IsValid_StampChanged_ReturnsFalse`, `IsValid_TokenWithoutStamp_ReturnsFalse`, `IsValid_UserNotFound_ReturnsFalse`.
  - `Wms.IntegrationTests/Security/SessionRevocationTests.cs`: `Deactivate_OldTokenGets401AndRefreshFails`, `RemoveRole_OldTokenGets401_NewTokenGets403`, `Logout_OldTokenGets401`.
- **Criterios de aceptación:**
  - Dado `qa_inactivo` con sesión abierta, cuando Admin lo desactiva, entonces su siguiente petición con el token anterior (`GET user/me`) responde 401 y el refresh es rechazado.
  - Dado `j_coral` con sesión abierta, cuando Admin le quita el rol Facturación, entonces el token anterior recibe 401 en `GET billing/invoices`, la aplicación obtiene un token nuevo con el refresh y la siguiente llamada a facturas responde 403.
  - Dado un usuario que cerró sesión, cuando se reutiliza su access token, entonces responde 401.
- **Re-test QA:** F1-USR-015, F1-USR-010, F1-AUT-018, F9-SES-001, F9-SES-002; REG F11-REG-001.
- **Riesgo de regresión:** bajo; una lectura de usuario por petición cada 15 s como máximo.
- **Tamaño:** M. **Dependencias:** CHG-01.

#### CHG-17 — Un doble envío del registro o del cobro no duplica nada

- **Cierra:** DEF-F3-002 (MAJOR). DEF-F8-001 es la misma causa (ficha unificada: «Duplicado de DEF-F3-002»).
- **Causa raíz:** los nueve handlers de registro, cobro e inicio de cobro comprueban «ya tiene servicio/ciclo» con una lectura previa, sin bloqueo ni restricción única: `InitiateStorageWeighingHandler.cs:192-196` (su transacción abre en `:61`, pero el único bloqueo, el del consecutivo, llega en `:390-391`, después de la lectura), `InitiateOutputWeighingHandler.cs:47-52`, `InitiateWeighingOnlyHandler.cs:49-54`, `ProcessStoragePaymentHandler.cs:94-111` y `:131-141`, `ProcessWeighingOnlyPaymentHandler.cs:76-83`, `ProcessOutputPaymentHandler.cs:82-89` y los tres `Start*PendingBillingHandler.cs` (`:41-66`). `EntryLogConfiguration.cs:89-91` solo hace único `(service_record_id, entry_log_id)` y `WeighbridgeCycleConfiguration.cs:42-44` no tiene índices únicos. Además `ProcessStoragePaymentHandler.cs:101-111,131-136` ignora los ciclos `Complete`: un cobro repetido después del cierre crea otro ciclo y otra factura. Por eso dos envíos del mismo usuario (QAE029, QAE030) dejaron dos depósitos con stock 6 cada uno, dos ciclos y dos facturas pagadas de 28.560.
- **Cambio exacto:**
  - Backend:
    - Nuevo `Wms.Application/Weighbridge/Common/Services/EntryLogLock.cs`: `AcquireAsync(context, entryLogId)` exige una transacción abierta y ejecuta `SELECT id FROM entry_logs WHERE id = {entryLogId} FOR UPDATE`. Los nueve handlers siguen este orden: abrir transacción, bloquear el ingreso, leer, guardar, confirmar, notificar. El segundo envío espera, relee y recibe el 409 de negocio.
    - `ProcessStoragePaymentHandler`: en el caso A, después de `:131-141`, si existe un ciclo no cancelado del servicio para ese ingreso lanza `ConflictException("Este camión ya tiene el cobro de báscula registrado.")` (el mismo texto reemplaza el de `:301-305`).
    - El mensaje «El entry log ya tiene un servicio asignado.» de los tres `Initiate*` pasa a «Este ingreso ya tiene un servicio de báscula asignado. Actualice la cola.».
    - `ServiceRecordEntryLog`: propiedad `IsPrimary` y `Create(serviceRecordId, entryLogId, bool isPrimary)`; `true` en `CreateEntryLogHandler.cs:118`, `UpdateEntryLogHandler.cs:94`, `CreateReceptionWithoutWeighbridgeCommandHandler.cs:182`, `InitiateStorageWeighingHandler.cs:694`, `InitiateWeighingOnlyHandler.cs:117` e `InitiateOutputWeighingHandler.cs:154`; `false` en los vínculos legítimos adicionales (`InitiateStorageWeighingHandler.cs:1102`, `AddAdditionalOrdersCommandHandler.cs:75`, `ExitWithEntryTicketCommandHandler.cs:92`).
    - Índices únicos parciales en `EntryLogConfiguration.cs` (vínculo principal por ingreso), `WeighbridgeCycleConfiguration.cs` (ciclo activo por servicio y camión) y `ServiceRecordConfiguration.cs` (salida activa por orden), con los nombres de la migración de la fase como constantes en `Wms.Infrastructure/Persistence/ConstraintNames.cs`.
    - Nueva clase pura `Wms.Application/Common/Persistence/UniqueViolationMessages.cs` (`TryGetMessage(sqlState, constraintName, out message)`) y, en `Wms.Api/Common/Exception/GlobalExceptionHandler.cs:103`, antes del caso genérico de `DbUpdateException`: una violación `23505` de una restricción conocida responde 409 con título «Operación duplicada.» y el mensaje del mapa. Mapa: vínculo principal → «Este ingreso ya tiene un servicio de báscula asignado. Actualice la cola.»; ciclo activo → «Este camión ya tiene el cobro de báscula registrado. Actualice la cola.»; salida por orden → «La orden de cargue ya tiene un servicio de salida en báscula.»; `idx_weighbridge_weighing_cycle_sequence` → «Este pesaje ya fue registrado. Actualice la pantalla.»; `idx_ws_entry_storage_entrylog_unique` → «Este camión ya tiene una entrada registrada en el depósito.».
  - Frontend: `useProcessPayment.ts` (sus 3 mutaciones), `useStartWeighingPendingBilling.ts` y `useRegisterStorageEntry.ts` agregan `onError`: con 409 invalidan `["weighbridge"]` para que la cola muestre el estado real.
  - No se toca: el `isPending` de `app/pages/operations/weighbridge/index.vue:558-563` (ya protege el doble clic), `DocumentNumberGenerator` ni `RecordPaymentHandler`.
- **Migración o script:** índices y columna `is_primary` de `AddLoadingOrderSignatureAndWeighbridgeIdempotency`. `fase-04-idempotencia.sql`:
  - Antes de la migración: (b) ciclos duplicados por servicio y camión → `UPDATE weighbridge_cycles … SET status = 'Canceled', voided_at = now(), void_reason = 'Ciclo duplicado por doble envío (DEF-F3-002)'` en todos menos el que referencia la entrada del depósito (luego el de más pesajes, luego el más antiguo); (d) órdenes con más de un servicio de salida activo → se descartan los sobrantes desde «Recuperar operaciones». Ambas detecciones deben quedar en 0 filas.
  - Después de la migración: `UPDATE service_record_entry_logs SET is_primary = true` en el vínculo más antiguo no descartado de cada ingreso; (a) depósitos duplicados por doble registro (entrada sin ciclo sobre el mismo ingreso; 2026BA00038/39 y 2026BA00040/41) → Comercio Exterior los anula con motivo; (c) facturas BASCULA sin ciclo ni entrada que las referencie (`663899`, `ea0dda`) → Facturación las anula con el motivo «Cobro duplicado por doble envío (DEF-F3-002)».
- **Pruebas automatizadas nuevas:**
  - `Wms.Tests/Common/UniqueViolationMessagesTests.cs`: `TryGetMessage_PrimaryLinkIndex_ReturnsEntryHasServiceMessage`, `TryGetMessage_CycleIndex_ReturnsChargeAlreadyRegisteredMessage`, `TryGetMessage_OutputIndex_ReturnsOrderHasServiceMessage`, `TryGetMessage_UnknownConstraint_ReturnsFalse`, `TryGetMessage_SqlState23503_ReturnsFalse`.
  - `Wms.Tests/Domain/Logistics/ServiceRecordEntryLogTests.cs`: `Create_Primary_SetsIsPrimaryTrue`, `Create_Additional_SetsIsPrimaryFalse`.
  - `Wms.IntegrationTests/Weighbridge/WeighbridgeIdempotencyTests.cs`: `ConcurrentRegister_SameEntry_OneCreatedOneConflict` (dos `POST storage/register` simultáneos → 201 y 409; un depósito con stock 6), `ConcurrentProcessPayment_SameService_OneCycleOneInvoice` (200 y 409), `ProcessPayment_AfterCycleComplete_Returns409`, `ConcurrentOutputInitiate_SameOrder_OneService`.
- **Criterios de aceptación:**
  - Dado el ingreso de QAE029 (Descargue importación), cuando `bascula` envía a la vez dos `POST weighbridge/storage/register` para ese ingreso, entonces una responde 201 y la otra 409 «Este ingreso ya tiene un servicio de báscula asignado. Actualice la cola.», y queda un solo depósito con stock 6.
  - Dado el servicio de QAE029, cuando se envían a la vez dos `POST weighbridge/storage/process-payment` con cobro inmediato de 28.560, entonces una responde 200 y la otra 409 «Este camión ya tiene el cobro de báscula registrado.», y quedan un ciclo y una factura BASCULA pagada.
  - Dado un ciclo ya completo, cuando se repite el cobro, entonces responde 409 con el mismo mensaje y no se crea ciclo ni factura.
  - Dado un día con estas operaciones, cuando se compara el reporte diario de báscula con las facturas BASCULA del día, entonces los totales coinciden.
- **Re-test QA:** F3-COB-013, F3-COB-001, E2E-18, E2E-20, F10-ERR-007; REG F11-REG-007, F11-REG-008, F11-REG-031.
- **Riesgo de regresión:** medio-alto (transacciones en nueve handlers). Lo mitigan el orden de bloqueo fijo y las pruebas de concurrencia.
- **Tamaño:** L. **Dependencias:** CHG-06, CHG-01.

#### CHG-18 — Un guardia de envío común: cada acción se envía una vez y el pago fallido conserva lo digitado

- **Cierra:** DEF-F10-001 (MAJOR), DEF-F10-002 (MINOR).
- **Causa raíz:** no existe un guardia de envío compartido; cada pantalla liga `isPending` a mano o no lo liga, y quedan ventanas sin cubrir (conversión de archivos, espera de 2 s antes de navegar, Enter):
  - Recepción directa: el botón de `app/features/warehouse/components/ReceptionStepManualInfo.vue:622-630` nunca se bloquea y `onSubmit` (`:168-239`) espera la conversión de fotos (`:177`) antes de emitir.
  - Verificar y rechazar pago: `mutate` sin estado de carga en `app/pages/billing/invoices/[id].vue:54-55,105-111` y `app/pages/billing/payments/index.vue:52-53,140-146` (botones `[id].vue:605-617` y `payments/index.vue:295-308`); «Rechazar» no pide confirmación.
  - Crear OC y emitir guía: `app/pages/foreign-trade/loading-orders/create.vue:19-24` y `dispatch-guides/create.vue:22-27` esperan la mutación y navegan con `setTimeout` de 2 s, durante los cuales el botón vuelve a habilitarse (`LoadingOrderForm.vue:1112-1118`, `DispatchGuideForm.vue:328-334`); el backend impide el duplicado (`idx_loading_order_external`, `LoadingOrderConfiguration.cs:70-73`) y el usuario ve un error después del éxito.
  - Registrar pago: `app/features/billing/components/PaymentDialog.vue:57-79` convierte el comprobante antes de emitir y su botón (`:174`) no tiene estado de carga; los tres padres usan `mutate` sin `isPending` (`[id].vue:53,98-103,649`, `InvoiceActionsDialog.vue:55,140-151,445`, `payments/index.vue:54,89-100,347`).
  - N.º SIIGO con Enter: `InvoiceActionsDialog.vue:278` llama `handleSaveNumber` (`:100-114`) sin mirar `isAssigningNumber` (`:54`).
  - Fotos: `ReceptionStepCompletion.vue:222-264` y `LoadingOrderExecutionDialog.vue:150-216` bloquean el botón solo después de convertir las fotos.
  - DEF-F10-002: `PaymentDialog.vue:77-78` emite `submit` y llama `resetForm()` sin esperar el resultado: un pago rechazado pierde monto y referencia, y el archivo sigue visible aunque ya no se envía.
- **Cambio exacto (aplica §10 · Un solo operario de báscula, que mantiene la protección del doble envío del mismo usuario):**
  - Frontend:
    - `app/utils/submit-guard.ts` (`createSubmitGuard()`: `run(tarea)` ignora una llamada mientras otra está en curso y libera al terminar; `hold()` mantiene el bloqueo tras el éxito hasta navegar; `release()`) y `app/composables/useSubmitGuard.ts` (expone `busy` y libera al desmontar). Regla de botones: `:loading` y `:disabled` = `busy || mutation.isPending`; en filas, el indicador en la fila enviada y todas las filas de esa acción deshabilitadas.
    - Aplicación: `ReceptionStepManualInfo.vue:168`, `ReceptionStepCompletion.vue:222` y `LoadingOrderExecutionDialog.vue:164-205` envuelven el envío (incluida la conversión de fotos) con `guard.run`; `loading-orders/create.vue:19-24` y `dispatch-guides/create.vue:22-27` usan `guard.run`, `guard.hold()` y `router.push` sin `setTimeout`, y pasan el estado a sus botones (`:54`, `:83`); `PaymentDialog.vue` recibe la prop `loading` (de `isRecordingPayment` en `payments/index.vue:347` y de `isPending` en `[id].vue:649` e `InvoiceActionsDialog.vue:445`), envía dentro de `guard.run` y bloquea «Cancelar» y el cierre mientras envía; `InvoiceActionsDialog.vue:100` no envía si hay una asignación en curso, si la acción no está habilitada o si el número no cambió; verificar y rechazar ligan `isPending` y `variables` a sus botones; `AgreementDetailDialog.vue:286-337` usa el guardia en sus cinco mutaciones.
    - «Rechazar pago» pide confirmación con `useAppConfirm`: «¿Rechazar el pago de {monto} (ref. {referencia o «sin referencia»}) de la factura {número}? El saldo de la factura se recalcula.» (texto en `app/features/billing/utils/payment-actions.ts`).
    - `PaymentDialog.vue`: se quita `resetForm()` después de emitir y el formulario se reinicia al abrir el diálogo (`watch` de `visible`); tras un rechazo del backend se conservan monto, referencia, notas y archivo.
  - Backend: ninguno.
  - No se toca: «Cobrar» de báscula (`isCollecting`, `app/pages/operations/weighbridge/index.vue:967,1081`, ya protegido), `useApiMutation` ni la página duplicada `app/pages/warehouse/receptions/create.vue` (sin enlace en el menú).
- **Migración o script:** sin migración. `fase-04-envios-duplicados.sql`: detección de pagos iguales (misma factura, monto, método y referencia) creados con menos de 10 s de diferencia y de recepciones directas iguales (mismo cliente y carta porte) con menos de 15 s; corrección operativa sin `UPDATE`: Facturación rechaza el pago duplicado desde Pagos (`RejectPaymentHandler.cs:25-27` recalcula el saldo) y CE anula con motivo el depósito duplicado en Borrador.
- **Pruebas automatizadas nuevas:** `test/unit/utils/submit-guard.spec.ts`: dos llamadas simultáneas ejecutan la tarea una vez y la segunda devuelve `undefined`; tras un rechazo se libera; `hold` mantiene `busy` hasta `release`; `test/components/billing/PaymentDialog.spec.ts`: doble clic con comprobante emite una vez; con `loading` el botón queda deshabilitado; tras emitir siguen en pantalla 1.000 y «QAF10-COMPROBANTE»; al reabrir el monto vuelve a 0 y la referencia queda vacía; `test/unit/billing/payment-actions.spec.ts`: el mensaje de rechazo sin referencia dice «sin referencia».
- **Criterios de aceptación:**
  - Dado una factura pendiente, cuando Facturación hace doble clic en «Registrar pago» con un comprobante, entonces se crea un solo pago.
  - Dado un pago recibido, cuando Facturación pulsa «Rechazar», entonces aparece la confirmación con monto, referencia y factura, y sin aceptar no se envía nada.
  - Dado el N.º SIIGO digitado, cuando se pulsa Enter dos veces seguidas, entonces se envía una sola asignación.
  - Dado «Crear orden de cargue», cuando la orden se crea, entonces el botón sigue deshabilitado hasta abrir la orden creada.
  - Dado un pago de 1.000 con referencia «QAF10-COMPROBANTE» que el backend rechaza con 409, cuando aparece el error, entonces el formulario conserva el monto, la referencia y el archivo.
- **Re-test QA:** F10-ERR-007, F10-UX-003, F10-UX-005, F10-ERR-006; REG F11-REG-019, F11-REG-020, F11-REG-023.
- **Riesgo de regresión:** bajo. Lo mitigan las pruebas del guardia y del diálogo de pago.
- **Tamaño:** M. **Dependencias:** CHG-01.

#### CHG-19 — El cobro de báscula propone al cliente de la operación

- **Cierra:** DEF-F3-007 (MAJOR).
- **Causa raíz:** `app/pages/operations/weighbridge/index.vue:939-941` lee `customerId` de la respuesta del registro, pero ninguno de los tres DTO lo trae (`InitiateWeighingResponseDto.cs`, `InitiateStorageResponseDto.cs` con su derivado armado campo a campo en `RegisterStorageEntryHandler.cs:44-65`, e `InitiateOutputResponseDto.cs`), ni los tipos del frontend (`app/features/weighbridge/types/weighbridge-cycle.ts:287-337`; un `as { customerId?: … }` lo oculta). Sin cliente, `billingInitialRecipientMode` (`:961-965`) propone al conductor y `BillingCollectForm.vue:237-263` pide el precio base sin convenio. El cliente existe en `ServiceRecord.CustomerId` en los tres flujos, y la cola tampoco lo expone.
- **Cambio exacto:**
  - Backend: `Guid? CustomerId` en los tres DTO de registro y en `WeighbridgeQueueItemDto`, asignado en `InitiateWeighingOnlyHandler.cs:147-158`, `InitiateStorageWeighingHandler.cs:745` y `:1240`, `InitiateOutputWeighingHandler.cs:177-190` (el cliente de la orden), `RegisterStorageEntryHandler.cs:44-65` y `GetWeighbridgeQueueHandler.cs:50-61` (fila del servicio pendiente).
  - Frontend: `customerId: string | null` en los tipos de registro y en `IWeighbridgeQueueItem`; `index.vue:939-941` → `initiateResponse.value?.customerId ?? null` sin conversión forzada; la elección del destinatario (`:960-965`) pasa a la función pura `defaultBillingRecipient(clienteId, conductor)` en `app/features/billing/utils/billing-recipient-default.ts`: con cliente, «Cliente registrado» con ese cliente; sin cliente, el conductor; sin conductor, cliente registrado vacío.
  - No se toca: `BillingCollectForm.vue` (ya usa `preselectedCustomerId` e `initialRecipientMode`), los handlers de cobro ni la reanudación tras recargar (la rehace CHG-20).
- **Migración o script:** sin migración. `fase-04-destinatarios.sql` (solo detección): facturas de báscula no anuladas sin cliente cuya operación sí tenía cliente; Facturación revisa cada una (el destinatario pudo elegirse a propósito).
- **Pruebas automatizadas nuevas:** `Wms.IntegrationTests/Weighbridge/InitiateCustomerIdTests.cs`: `InitiateWeighingOnly_ReturnsCustomerId`, `RegisterStorageEntry_ReturnsCustomerId`, `InitiateOutput_ReturnsLoadingOrderCustomerId`, `Queue_PendingService_ReturnsCustomerId`; `test/unit/billing/billing-recipient-default.spec.ts`: con cliente → registrado con ese cliente; sin cliente y con conductor → conductor; sin ninguno → registrado vacío.
- **Criterios de aceptación:**
  - Dado el registro de QAE030 (Descargue importación) para QA Cliente Uno, con convenio de báscula de 25.000 + IVA, cuando báscula pasa al cobro, entonces el destinatario propuesto es «Cliente registrado: QA Cliente Uno» y el total es 29.750.
  - Dado un Solo báscula sin cliente con conductor, cuando pasa al cobro, entonces se propone al conductor.
- **Re-test QA:** F3-COB-003; REG F11-REG-008.
- **Riesgo de regresión:** bajo.
- **Tamaño:** M. **Dependencias:** CHG-17.

#### CHG-20 — Retomar una operación tras recargar muestra lo guardado, con su tipo real y en solo lectura

- **Cierra:** DEF-F3-006 (MAJOR), DEF-F3-017 (MAJOR), DEF-F3-018 (MINOR).
- **Causa raíz:** la ficha del camión vive solo en memoria y, al recargar o «Recuperar», se rearma con suposiciones:
  - DEF-F3-006: `app/pages/operations/weighbridge/index.vue:461-483` rearma la operación con una respuesta en ceros y monta los formularios del Registro (`:1486-1534`) en blanco; nada lee el registro guardado. No hay `beforeunload` (`onBeforeRouteLeave`, `:1299-1315`, solo cubre la navegación interna), así que recargar con camiones digitados no avisa.
  - DEF-F3-017: `index.vue:376-380` (`operationTypeForService`) convierte todo `Input` en «storage», pero Solo báscula también es `Input` (`ServiceRecord.cs:111`); el cobro va a `storage/process-payment` y `ProcessStoragePaymentHandler.cs:57-61` lo acepta porque solo valida `Input`; la factura no queda enlazada al ciclo. `recover.vue:95-111` adivina el tipo por el nombre de la modalidad y `:157` usa `cycle.invoiceId`, que el API no envía.
  - DEF-F3-018: el Registro hecho es el mismo formulario editable con `:inert` (`index.vue:1461-1465`): parece editable y no dice dónde corregir.
- **Cambio exacto:**
  - Backend:
    - Clase pura `Wms.Application/Weighbridge/Common/Services/WeighbridgeOperationType.cs`: `From(tipoDeServicio, cartaPorte)` → «output» para `OutputCargo`, «weighing-only» sin documento (`ServiceRecord.CreateForWeighingOnly`, `ServiceRecord.cs:99-120`) y «storage» en los demás; `EnsureIs(servicio, esperado)` lanza `ConflictException("Este servicio es {de Solo báscula | un ingreso con depósito | una salida de mercancía}; no se puede cobrar como {…}.")`. Guardas en `ProcessStoragePaymentHandler.cs:57-61`, `StartStoragePendingBillingHandler.cs:41`, `ProcessWeighingOnlyPaymentHandler.cs:49` y `StartWeighingOnlyPendingBillingHandler.cs:38`.
    - `OperationType` en `WeighbridgeQueueItemDto` (`GetWeighbridgeQueueHandler.cs:100-127`), `RecoverableOperationDto` (`GetRecoverableOperationsHandler.cs:41-78`, `:98-127`) y `ServiceRecordInfoDto` (`GetWeighbridgeCycleHandler.cs:149-163`).
    - Consulta nueva `GET weighbridge/service-records/{serviceRecordId}/registration?entryLogId=` (`WeighbridgeController.cs`, junto a `:709`; política de la clase): `WeighbridgeRegistrationDto` con tipo de operación, cliente, carta porte, tipo y fecha del documento, modalidad, depósito, orden de cargue, configuración del pesaje (un solo peso, tipo del primer peso, perecedero), terceros y líneas del camión (producto, cantidad declarada, unidad). Errores 404 «El servicio no existe o fue descartado.» y «El servicio no pertenece a este camión.».
  - Frontend:
    - `weighbridge-service.ts` (`getWeighbridgeRegistration`), tipo `IWeighbridgeRegistration` y `operationType` en `IWeighbridgeQueueItem`, `IRecoverableOperation` e `IServiceRecordInfo`.
    - `index.vue`: función única `resumeSavedOperation(ingreso, servicio, ciclo)` que lee el registro guardado y fija el tipo de operación, el cliente, el depósito, la configuración del pesaje y, en depósitos, el registro principal con `buildParentServiceRecord` (`app/features/weighbridge/utils/parent-service-record.ts`); reemplaza `operationTypeForService` (`:376-380`), el rearmado en ceros (`:461-483`) y la reanudación de `onMounted` (`:1318-1362`, por `?resume=&sr=&cycle=`, sin `sessionStorage`). `afterInitiated` (`:624-631`) usa la misma consulta tras «Guardar», así que el Registro se ve igual antes y después de recargar.
    - Registro en solo lectura: nuevo `app/features/weighbridge/components/RegistrationSummary.vue` (operación, documento, modalidad, depósito, cliente, terceros, orden de cargue y productos con cantidad y unidad, sin campos editables) con el texto «Registro guardado, solo lectura. Para corregirlo: Comercio Exterior ajusta los productos en el detalle del depósito mientras esté en Borrador; si el registro está mal y aún no se cobró, descártelo desde «Recuperar operaciones»; si ya se cobró, anule el pesaje desde el historial.»; el formulario del paso 1 deja de mostrarse después de guardar (`:1461-1465`, `:1486-1534`).
    - Aviso al recargar: `useEventListener(window, "beforeunload", …)` que guarda el borrador y avisa si hay placas digitadas sin guardar (`unsavedDraftPlates`, extraída de `:313-317` a `app/features/weighbridge/utils/truck-drafts.ts`).
    - `recover.vue`: «Retomar» (`:212-233`) solo navega con `?resume=&sr=&cycle=`; se borran la heurística por nombre de modalidad (`:95-111`), `resumeFromCycle` y `resumeFromServiceRecord` (`:113-210`) y el `sessionStorage`.
  - No se toca: `onBeforeRouteLeave`, el `KeepAlive` de los borradores ni `CompleteEntryInfo.vue`.
- **Migración o script:** sin migración. `fase-04-solo-bascula.sql`: detección de ciclos de Solo báscula sin factura y de facturas «Servicio de Báscula - Ingreso a Depósito» sin entrada ni ciclo; corrección en la base local y en staging: enlazar cada ciclo con su factura (`UPDATE weighbridge_cycles SET invoice_id = … WHERE id = …`, por pares con la misma hora de creación).
- **Pruebas automatizadas nuevas:** `Wms.Tests/Weighbridge/WeighbridgeOperationTypeTests.cs`: `From_InputWithoutDocument_ReturnsWeighingOnly` (también con «  »), `From_InputWithDocument_ReturnsStorage`, `From_OutputCargo_ReturnsOutput`, `EnsureIs_WeighingOnlyRecordAsStorage_ThrowsConflictWithMessage` («Este servicio es de Solo báscula; no se puede cobrar como un ingreso con depósito.»), `EnsureIs_StorageRecordAsStorage_DoesNotThrow`; `Wms.IntegrationTests/Weighbridge/WeighbridgeRegistrationTests.cs`: `GetRegistration_StorageTruck_ReturnsDocumentCustomerAndLines`, `GetRegistration_EntryNotLinked_Returns404`; `Wms.IntegrationTests/Weighbridge/PaymentRouteGuardTests.cs`: `ProcessStoragePayment_WeighingOnlyService_Returns409`; `test/unit/weighbridge/truck-drafts.spec.ts`: placa digitada sin servicio → aparece; guardada → no; sin placa → «Sin placa»; sin tocar → no; `test/components/weighbridge/RegistrationSummary.spec.ts`: muestra documento QA-CP-0420 y la línea «Producto QA · 6 · Unidad» sin `input`, `textarea` ni `select`, y menciona «Comercio Exterior» y «Recuperar operaciones».
- **Criterios de aceptación:**
  - Dado QAE020 registrado (documento QA-CP-0420, 6 unidades) y la página recargada, cuando báscula lo abre desde la cola, entonces el Registro muestra documento, cliente y productos con su cantidad, en solo lectura y con la indicación de dónde corregir.
  - Dado un Solo báscula de QAC420 retomado tras recargar, cuando báscula cobra, entonces la ficha dice «Solo báscula», el cobro va por Solo báscula con la factura enlazada al ciclo y el primer peso permite Tara o Bruto; un cobro por la ruta de depósito responde 409 «Este servicio es de Solo báscula; no se puede cobrar como un ingreso con depósito.».
  - Dado dos camiones digitados sin guardar, cuando báscula recarga la página, entonces el navegador pide confirmación.
- **Re-test QA:** F3-REI-003, F3-REI-005, F3-REI-009, F3-REI-010; REG F11-REG-010.
- **Riesgo de regresión:** medio (reescribe la reanudación de la pantalla principal de báscula). Lo mitigan las pruebas de componentes y el re-test de reingreso completo.
- **Tamaño:** L. **Dependencias:** CHG-17, CHG-19.

#### CHG-21 — «Información General» se puede editar en un depósito en Borrador

- **Cierra:** DEF-F5-001 (MAJOR).
- **Causa raíz:** `app/features/foreign-trade/components/DepositDetailGeneralInfoCard.vue:224-235`: `<EditDepositEntryDateDialog v-if="canEditEntryDate">` (`:224`) quedó entre `<div v-if="!editing">` (`:179`) y `<div v-else>` (`:235`), así que el `v-else` se empareja con el diálogo. En Borrador y Confirmado (`canEditEntryDate` verdadero), al pulsar «Editar» no se pinta ni la lectura ni el formulario; en Cerrado y Anulado el formulario con «Guardar» aparece siempre junto a la lectura. La tarjeta la usan `imports/[id]`, `exports/[id]` e `inspections/[id]`.
- **Cambio exacto:**
  - Backend: ninguno.
  - Frontend: `DepositDetailGeneralInfoCard.vue`: el bloque `<EditDepositEntryDateDialog …/>` (`:224-232`) se mueve antes de la vista de lectura (`:178`), de modo que `<div v-else>` queda inmediatamente después de `<div v-if="!editing">`.
  - No se toca: `handleSave`, `canEdit` ni `EditDepositEntryDateDialog.vue`.
- **Migración o script:** ninguno.
- **Pruebas automatizadas nuevas:** `test/components/foreign-trade/DepositDetailGeneralInfoCard.spec.ts`: `shows_edit_form_after_clicking_edit_in_draft` (existen `#general-document-date`, `#general-currency` y `#general-cargo-value`, y desaparece la lectura), `shows_only_shipping_field_in_confirmed`, `closed_shows_no_form_until_edit`, `cancelled_has_no_edit_button_nor_form`.
- **Criterios de aceptación:**
  - Dado 2026BA00008 en Borrador, cuando CE pulsa «Editar» en «Información General», entonces aparecen la fecha del documento, la moneda y el valor de la mercancía, y al guardar el depósito queda listo para confirmar.
  - Dado un depósito Anulado, cuando CE abre su detalle, entonces «Información General» se ve solo en lectura y sin botón «Guardar».
- **Re-test QA:** F5-CNF-001; REG F11-REG-017.
- **Riesgo de regresión:** bajo.
- **Tamaño:** S. **Dependencias:** CHG-01.

### Fase 5 — MAJOR de dinero: pagos, numeración, mínimos y reglas de tarifas

- **Objetivo:** que los pagos solo entren en facturas emitidas y que una factura con dinero no se anule, que las facturas de contado pagadas reciban su N.º SIIGO (§10 · N.º SIIGO en contado), que el mínimo de almacenamiento diga si incluye IVA (§10 · Mínimo con o sin IVA), que el piso por unidad de carga no se cuente dos veces, que las reglas para perecederos y los rangos de los parámetros se puedan configurar y validar, que la creación manual de facturas desaparezca de la pantalla y del API (§10 · Sin creación manual de facturas) y que el comprobante del pago se guarde. Cierra DEF-F6-009, DEF-F6-013, DEF-F6-022, DEF-F6-021, DEF-F6-007, DEF-F1-003, DEF-F6-012, DEF-F1-004, DEF-F6-011, DEF-F6-010 y, por compartir causa, DEF-F6-015.
- **Criterio de entrada:** checkpoint de la Fase 4 aprobado; migración de la Fase 4 aplicada.
- **Cambios:** CHG-22, CHG-23, CHG-24, CHG-25, CHG-26, CHG-27, CHG-28, CHG-29.
- **Orden interno:** CHG-22 → CHG-23 (ambos en `Invoice.cs` y en los handlers de pagos) → CHG-24 → CHG-25 (ambos en el esquema de fórmulas y en `StorageBillingService.cs`) → CHG-26 → CHG-27 (ambos en los handlers de convenio y de tarifa base; CHG-27 usa el PATCH parcial de CHG-26) → CHG-28 → CHG-29 (ambos en `BillingController.cs`).
- **Migraciones de la fase (las genera el implementador con `dotnet ef`, en este orden):** `AddMinimumIncludesVatSetting` (CHG-24 y CHG-25) y `AddPerishableToRuleUniqueIndexes` (CHG-26).
- **Riesgos y mitigación:**
  - Facturación deja de registrar pagos en borradores que no son de contado y de anular facturas con dinero. Mitigación: el script lista los casos existentes antes del despliegue y Facturación los resuelve con el cliente.
  - El PATCH del servicio de convenio pasa a «campo ausente = se conserva». Mitigación: la pantalla ya envía todos los campos; pruebas del convertidor y del PATCH.
  - Se retira `POST billing/invoices`. Mitigación: su único consumidor es `app/pages/billing/invoices/create.vue`, que se retira en el mismo cambio.
  - Los comprobantes quedan en `wwwroot/uploads/payment-vouchers` con un nombre de GUID, igual que las fotos de recepción. Mitigación: tipo y tamaño validados por contenido.
- **Saneamiento de datos:** `fase-05-pagos.sql`, `fase-05-siigo.sql`, `fase-05-minimos.sql`, `fase-05-reglas.sql` y `fase-05-comprobantes.sql`, descritos en cada cambio.
- **Criterio de salida:** compuertas comunes (regla 4.0.4) y en PASA: F6-PAG-010, F6-PAG-007, F6-ACC-018, E2E-12, F6-ACC-017, F6-ALM-010, F6-FOR-013, F6-FOR-014, F1-SRV-019, F6-TAR-009, F1-CNV-006, F6-INV-020, F6-PAG-008; REG F11-REG-002, F11-REG-004, F11-REG-021, F11-REG-022, F11-REG-023.
- **Checkpoint:** se entrega al usuario la lista de pagos y anulaciones regularizados, las facturas de contado numeradas, la lista de reglas con parámetros fuera de rango corregidas por Facturación y la evidencia de un pago con comprobante PDF. El usuario aprueba las dos migraciones y el saneamiento en staging.

#### CHG-22 — Pagos solo en facturas emitidas y sin anular facturas con dinero

- **Cierra:** DEF-F6-009 (MAJOR), DEF-F6-013 (MAJOR).
- **Causa raíz:**
  - DEF-F6-009: `Wms.Application/Billing/Commands/RecordPayment/RecordPaymentHandler.cs:30-37` solo rechaza facturas anuladas o pagadas y el exceso sobre el saldo; `Invoice.RecordPayment` (`Invoice.cs:372-393`) lleva un Borrador a PartiallyPaid o Paid sin número ni aprobación. El buscador de `app/pages/billing/payments/index.vue:65-73` envía `statuses`, pero `app/plugins/api-client.ts:22-27` crea axios sin `paramsSerializer`: viaja `statuses[]=…`, ASP.NET Core no lo enlaza (`GetInvoicesQuery.Statuses`) y se listan todos los estados; la etiqueta (`index.vue:80-81`) imprime «null» sin número.
  - DEF-F6-013: `Invoice.cs:409-427` (`Cancel`) solo impide anular facturas pagadas o ya anuladas y `CancelInvoiceHandler.cs:24-31` no carga los pagos: una factura con pago parcial se anula con el dinero dentro. En la pantalla, `app/features/billing/utils/invoice-action-rules.ts:67-70` habilita «Anular» salvo en Paid y Cancelled.
- **Cambio exacto:**
  - Backend:
    - `Invoice.cs`: nuevo `EnsureAcceptsManualPayment()`: Draft → `BadRequestException("La factura está en borrador. Asigne el número SIIGO y apruébela antes de registrar un pago.")`; PendingApproval → «La factura está pendiente de aprobación. Apruébela antes de registrar un pago.»; Cancelled → «No se puede registrar un pago en una factura cancelada.»; Paid → «La factura ya está completamente pagada.». Admite Approved, Sent, Overdue y PartiallyPaid. `RecordPaymentHandler.cs:30-34` lo llama (se conserva el control de saldo de `:36-37`). Los cobros de contado de báscula, montacargas y guía no pasan por este handler y no cambian.
    - `InvoiceCancellationPolicy.cs`: nuevo `EnsureCanCancelManually(IEnumerable<InvoicePayment> payments)`: con algún pago Received o Verified → `BadRequestException("No se puede anular la factura porque tiene pagos recibidos o verificados. Gestione la devolución o el traslado del dinero antes de anularla.")`. `CancelInvoiceHandler.cs:24-31` carga los pagos, aplica la política antes de `Cancel`, rechaza los pagos Pending con el motivo «Factura anulada» y llama `RefreshFinancialStatusAsync` (CHG-13).
  - Frontend:
    - `app/plugins/api-client.ts:22`: `axios.create({ …, paramsSerializer: { indexes: null } })` (arreglos como llaves repetidas).
    - `app/pages/billing/payments/index.vue`: la búsqueda conserva `statuses` y descarta facturas con saldo 0; la etiqueta sale de la función pura nueva `paymentInvoiceLabel` (`app/features/billing/utils/payment-invoice-label.ts`): `«{N.º o "Pendiente de número"} — {cliente o "Sin destinatario"} — {saldo}»`; la búsqueda consulta por cliente y por número y une los resultados por id.
    - `invoice-action-rules.ts`: «Anular» deshabilitada con «Tiene pagos recibidos o verificados: gestione la devolución o el traslado del dinero antes de anular.» cuando algún pago está Received o Verified (`InvoiceForRules` agrega `payments`).
  - No se toca: `PaymentDialog.vue` (lo cambian CHG-18 y CHG-29), `InvoicePayment` ni los flujos de contado.
- **Migración o script:** sin migración. `fase-05-pagos.sql` (detección): pagos Pending, Received o Verified sobre facturas nunca aprobadas que no son de contado; facturas anuladas con pagos Received o Verified. Con esas filas, Facturación decide con el cliente la devolución o el traslado del pago a la factura refacturada; en la base local son datos de QA y se resuelven al recrear la base (§7).
- **Pruebas automatizadas nuevas:**
  - `Wms.Tests/Domain/Billing/InvoicePaymentRulesTests.cs`: `EnsureAcceptsManualPayment_Draft_ThrowsDraftMessage`, `…_PendingApproval_ThrowsPendingMessage`, `…_Cancelled_Throws`, `…_Paid_Throws` y un `Theory` sin excepción para Approved, Sent, Overdue y PartiallyPaid.
  - `Wms.Tests/Billing/InvoiceCancellationPolicyTests.cs`: `EnsureCanCancelManually_WithReceivedPayment_ThrowsExactMessage`, `…_WithVerifiedPayment_Throws`, `…_WithPendingAndRejectedOnly_DoesNotThrow`, `…_WithoutPayments_DoesNotThrow`.
  - `Wms.IntegrationTests/Billing/PaymentRulesTests.cs`: `RecordPayment_OnDraft_Returns400WithMessage`, `CancelInvoice_WithReceivedPayment_Returns400`, `GetInvoices_WithRepeatedStatuses_FiltersByStatus`.
  - `test/unit/billing/invoice-action-rules.spec.ts` (anular deshabilitada con pago recibido, habilitada sin pagos) y `test/unit/billing/payment-invoice-label.spec.ts` (sin número → «Pendiente de número»).
- **Criterios de aceptación:**
  - Dado una factura en Borrador, cuando Facturación registra por API un pago de 5.000, entonces responde 400 «La factura está en borrador. Asigne el número SIIGO y apruébela antes de registrar un pago.» y el estado no cambia.
  - Dado Pagos → «Registrar Pago», cuando Facturación busca «QA Cliente», entonces solo aparecen facturas Aprobadas, Enviadas, Vencidas o con Pago parcial y saldo mayor que 0, y las que no tienen número dicen «Pendiente de número».
  - Dado una factura con un pago recibido de 5.000, cuando Facturación abre sus acciones, entonces «Anular» está deshabilitada con «Tiene pagos recibidos o verificados: gestione la devolución o el traslado del dinero antes de anular.»; por API, la anulación responde 400 con «No se puede anular la factura porque tiene pagos recibidos o verificados. Gestione la devolución o el traslado del dinero antes de anularla.».
  - Dado una factura sin pagos, cuando se anula con un motivo de al menos 10 caracteres, entonces queda anulada.
- **Re-test QA:** F6-PAG-010, F6-PAG-007, F6-ACC-018, E2E-12 (paso 7); REG F11-REG-023.
- **Riesgo de regresión:** bajo; el serializador cambia el formato de los arreglos en la URL y hoy `statuses` es el único parámetro de consulta con arreglo.
- **Tamaño:** M. **Dependencias:** CHG-13, CHG-15.

#### CHG-23 — N.º SIIGO en facturas de contado ya pagadas

- **Cierra:** DEF-F6-022 (MAJOR).
- **Causa raíz:** `Wms.Domain/Entities/Billing/Invoice.cs:441-445` (`AssignInvoiceNumber`) solo admite Borrador y Pendiente de aprobación. Las facturas de contado nacen sin número y quedan pagadas al crearse (`Invoice.cs:383-388`), así que no tienen ruta de numeración. La pantalla repite la regla (`app/features/billing/utils/invoice-action-rules.ts:53-58`, «El número queda fijo después de aprobar.»).
- **Cambio exacto (aplica §10 · N.º SIIGO en facturas de contado):**
  - Backend: `AssignInvoiceNumber` (`:434-454`): en Paid sin número asigna el número; en Paid con número lanza `BadRequestException("La factura pagada ya tiene número de factura (SIIGO); no se puede cambiar.")`; en Paid con total 0 lanza «Una factura en cero no requiere número fiscal.»; los demás estados conservan la regla y el mensaje actuales. La unicidad sigue en `AssignInvoiceNumberHandler.cs:30-35` («Ya existe una factura con el número '…'.»).
  - Frontend: `invoice-action-rules.ts:53-58` → `assignNumber` habilitada en Paid sin número, deshabilitada en Paid con número («La factura pagada ya tiene N.º SIIGO; no se puede cambiar.») y en facturas en 0 («Las facturas en cero no llevan número.»). `InvoiceActionsDialog.vue:270,289`: en Paid sin número muestra la ayuda «Factura de contado: asigne el N.º SIIGO una sola vez; después queda fijo.».
  - No se toca: `Approve`, `Send`, la regla de TRM pendiente ni `AssignInvoiceNumberHandler`.
- **Migración o script:** sin migración. Detección de facturas pendientes de numerar: `SELECT id, created_at, total, customer_id FROM invoices WHERE status = 'Paid' AND invoice_number IS NULL AND NOT is_zero_value ORDER BY created_at;` (las numera Facturación desde la pantalla).
- **Pruebas automatizadas nuevas:** `Wms.Tests/Domain/Billing/InvoiceActionRulesTests.cs`: `AssignInvoiceNumber_OnPaidInvoiceWithoutNumber_AssignsIt`, `AssignInvoiceNumber_OnPaidInvoiceWithNumber_Throws`, `AssignInvoiceNumber_OnPaidZeroValueInvoice_Throws`; `test/unit/billing/invoice-action-rules.spec.ts`: `assignNumber` habilitada en Paid sin número y deshabilitada con número.
- **Criterios de aceptación:**
  - Dado una factura de báscula de contado Paid sin número, cuando Facturación asigna «QA-SIIGO-0100», entonces el número queda asignado.
  - Dado esa factura, cuando intenta cambiar el número, entonces responde 400 «La factura pagada ya tiene número de factura (SIIGO); no se puede cambiar.».
  - Dado otro número ya usado, cuando se asigna, entonces responde 409 «Ya existe una factura con el número 'QA-SIIGO-0100'.».
- **Re-test QA:** F6-ACC-017; REG F11-REG-022.
- **Riesgo de regresión:** bajo.
- **Tamaño:** S. **Dependencias:** CHG-22.

#### CHG-24 — Quien configura un mínimo de almacenamiento dice si incluye IVA

- **Cierra:** DEF-F6-021 (MAJOR).
- **Causa raíz:** el mínimo de modalidad se cobra siempre como neto más IVA: `StorageBillingService.cs:237` lo usa como neto y `:251` como monto del cargo; `ServiceMinimumValue.cs:15-26` no tiene campo de base (184.000 → 218.960). El mínimo de fórmula se trata siempre como IVA incluido: `PercentageOfValueFormulaCalculator.cs:41-42`, `PercentageOfValueProratedFormulaCalculator.cs:57-58`, `WeightThresholdFormulaCalculator.cs:41-42` y `StorageMinimumFloor.cs:41-42`, con rótulos sembrados «(IVA incluido)» (`SeedDataExtensions.cs:644-701`). La pista de la ficha se corrige: no se trata de pasar el mínimo de modalidad a IVA incluido, sino de hacer configurables las dos vías (§10 · Mínimo de almacenamiento).
- **Cambio exacto:**
  - Backend:
    - `ServiceMinimumValue`: propiedad `IncludesVat` (por defecto `false`, que conserva el comportamiento actual), `Create(…, bool includesVat = false)` y `Update(decimal amount, bool includesVat)`; configuración `Property(v => v.IncludesVat).IsRequired()` sin `HasDefaultValue`; semillas `SeedDataExtensions.cs:174-177` con `IncludesVat = false`. `ServiceMinimumValueDto`, `UpdateServiceMinimumValueRequest(decimal Amount, bool IsActive, bool IncludesVat)`, `UpdateServiceMinimumValueHandler.cs:28-45` y `GetServiceMinimumValuesHandler.cs:24-33` lo exponen.
    - `StorageBillingService.cs:234-243`: neto del mínimo = `VatMath.ToNet(monto, IncludesVat ? tasa : 0)` (CHG-11); las advertencias (`:261-265`, `:273-276`) dicen «(${monto} IVA incluido)» o «(${monto} más IVA)».
    - Nuevo `Wms.Application/Billing/Calculators/MinimumVat.cs` (interno): parámetro `minimumIncludesVat` (`true` si falta, que conserva el comportamiento actual); `ToNet(amount, ctx)`; `ValidateOptional` exige «true» o «false» (`BadRequestException("Parámetro inválido: 'minimumIncludesVat' debe ser true o false.")`). Reemplaza la normalización en los cuatro puntos de la causa y gobierna `minimum` y `minimumPerCargoUnit`.
    - `PreviewFormulaHandler.cs:105-106` usa `MinimumVat.ToNet` y sus textos (`:67-81`) dicen «IVA incluido» o «neto».
    - Esquema sembrado de fórmulas (`SeedDataExtensions.cs:621-717`): rótulos neutros («Mínimo a cobrar ($)», «Mínimo por unidad de carga ($)», «Mínimo por debajo del umbral ($)») y parámetro nuevo `minimumIncludesVat` («El mínimo incluye IVA (desmarcado: es neto y se suma el IVA)», booleano, no obligatorio, valor por defecto «true») en PER_CARGO_UNIT, PER_UOM, PERCENTAGE_OF_VALUE, PERCENTAGE_OF_VALUE_PRORATED, FIXED y WEIGHT_THRESHOLD. `FormulaParameterSchema` (`FormulaType.cs:58-72`) agrega `DefaultValue` y los DTO de tipos de fórmula lo exponen.
  - Frontend:
    - `app/features/services/components/ServiceMinimumValuesCard.vue` y `types/minimum-value.ts`: columna «Base» con «IVA incluido» o «Neto (+ IVA)»; en el diálogo, selector «El valor mínimo se digita: Con IVA incluido | Neto (se suma el IVA)».
    - `AgreementServiceFormDialog.vue` y `ServicePricingRuleFormDialog.vue`: el control booleano guarda «true»/«false»; al abrir o cambiar de fórmula se asigna el `defaultValue` del esquema a los parámetros sin valor; el texto «El "Mínimo a cobrar" sí se registra con IVA incluido.» (`AgreementServiceFormDialog.vue:228-232`, `ServicePricingRuleFormDialog.vue:196-200`) pasa a «El mínimo tiene su propia opción “El mínimo incluye IVA”.». `AgreementServicesList.vue:45-50` y `ServicePricingRulesList.vue:183-186` muestran «Mínimo con IVA incluido» o «Mínimo neto (+ IVA)».
  - No se toca: `FormulaCalculatorRegistry` ni el «IVA incluido» de la tarifa (`TaxIncluded`), que es otro concepto.
- **Migración o script:** `AddMinimumIncludesVatSetting` (de la Fase 5): `service_minimum_values.includes_vat boolean NOT NULL` y `UpdateData` de `formula_types.parameter_schema` de las seis fórmulas. Sin saneamiento: las filas existentes quedan `includes_vat = false` y las reglas sin el parámetro se leen como IVA incluido, de modo que ningún total cambia al desplegar.
- **Pruebas automatizadas nuevas:**
  - `Wms.Tests/Billing/Calculators/PercentageOfValueMinimumTests.cs`: `BelowThresholdWithNetMinimum_DoesNotNormalize` (`minimumIncludesVat=false`, IVA 19 %, CIF 10.000.000 → monto 184.000; con IVA 218.960).
  - `StorageMinimumFloorTests.cs`: `WithNetFlag_DoesNotNormalizeFloor`; `WeightThresholdFormulaCalculatorTests.cs`: `BelowThresholdWithNetFlag_ReturnsMinimumAsNet`; `MinimumVatTests.cs`: `ValidateOptional_InvalidValue_Throws`.
  - `Wms.Tests/Billing/StorageMinimumChargeTests.cs` (cálculo extraído a la clase pura `StorageMinimumCharge.NetAmount`): (184.000, IVA incluido, 19) → 154.621,85; (184.000, neto, 19) → 184.000; (0, IVA incluido, 19) → 0.
  - `test/components/services/ServiceMinimumValuesCard.spec.ts`: el diálogo muestra el selector de base y la tabla la columna «Base».
- **Criterios de aceptación:**
  - Dado el mínimo de IMP001 en 184.000 configurado «Con IVA incluido», cuando un depósito de importación cae al mínimo, entonces la línea es 154.621,85 + IVA 29.378,15 = 184.000.
  - Dado el mismo mínimo configurado «Neto (se suma el IVA)», cuando un depósito cae al mínimo, entonces la línea es 184.000 + IVA 34.960 = 218.960.
  - Dado un convenio `PERCENTAGE_OF_VALUE` con mínimo 184.000 y «El mínimo incluye IVA» desmarcado, cuando se factura un depósito con CIF COP 10.000.000, entonces la línea es 184.000 + IVA = 218.960; marcado o sin el parámetro, la línea suma 184.000 con IVA incluido.
  - Dado los formularios de mínimos, tarifas base y convenios, cuando Admin o Facturación digita un mínimo, entonces el formulario indica si ese valor es con IVA incluido o neto.
- **Re-test QA:** F6-ALM-010, F6-FOR-013, F6-FOR-014; REG F11-REG-021.
- **Riesgo de regresión:** bajo (los valores por defecto conservan los totales actuales).
- **Tamaño:** M. **Dependencias:** CHG-11.

#### CHG-25 — El piso por unidad de carga no se cuenta como magnitud doble

- **Cierra:** DEF-F6-007 (MAJOR).
- **Causa raíz:** `Wms.Application/Billing/Common/Services/StorageBillingService.cs:292-293` cuenta una regla como «por contenedor» si tiene piso configurado (`StorageMinimumFloor.IsConfigured`), y `:294` cuenta la misma regla PER_CARGO_UNIT como «por unidad de carga»: `:296-297` devuelve la violación D12 y `:160-168` manda el depósito al mínimo de modalidad (184.000 + IVA = 218.960). Además `PerCargoUnitFormulaCalculator.cs:16-25` no aplica el piso y el esquema sembrado de PER_CARGO_UNIT (`SeedDataExtensions.cs:628-635`) no ofrece `minimumPerCargoUnit`.
- **Cambio exacto:**
  - Backend: extraer `GetSingleMagnitudeViolation` (`:285-310`) a la clase pura `Wms.Application/Billing/Common/Services/StorageMagnitudeRules.cs` (`FindViolation(IReadOnlyList<ResolvedRule>)`), llamada desde `:160`, con el predicado: una regla cuenta como «por contenedor» si su base es `PerContainer`, o si es `Flat` o `PerQuantity` con piso configurado. `PerCargoUnitFormulaCalculator`: `CalculateDetailed` aplica `StorageMinimumFloor.Apply(rate * unidades, contexto)` y `ValidateParameters` agrega `StorageMinimumFloor.ValidateOptional`. El esquema sembrado de PER_CARGO_UNIT agrega `minimumPerCargoUnit` y `minimumIncludesVat` (CHG-24).
  - Frontend: ninguno (el diálogo de convenio pinta el parámetro desde el esquema).
  - No se toca: la regla de dos PER_CARGO_UNIT del mismo tipo de unidad (`:302-307`) ni el bloque de grupos de depósito (`:160-168`).
- **Migración o script:** el `UpdateData` del esquema de PER_CARGO_UNIT va en `AddMinimumIncludesVatSetting`. Detección de facturas que cayeron al mínimo por la falsa violación: `SELECT id, invoice_number, status, total FROM invoices WHERE status <> 'Cancelled' AND detail ILIKE '%magnitud del depósito facturada más de una vez (D12)%';` (en Borrador, Facturación corrige con «Sobrescribir total»; emitidas, en SIIGO).
- **Pruebas automatizadas nuevas:** `Wms.Tests/Billing/Services/StorageMagnitudeRulesTests.cs`: `FindViolation_PerCargoUnitRuleWithOwnFloor_ReturnsNull`, `FindViolation_FloorRuleAndPerCargoUnitRule_ReturnsViolation`, `FindViolation_TwoFloorRules_ReturnsViolation`, `FindViolation_PerContainerAndFloorRule_ReturnsViolation`, `FindViolation_TwoPerCargoUnitSameType_ReturnsDuplicateTypeMessage`, `FindViolation_TwoPerVehicle_ReturnsVehicleMessage`; `PerCargoUnitFormulaCalculatorTests.cs`: `CalculateDetailed_WithFloorAboveRate_AppliesFloorPerUnit` y `CalculateDetailed_WithFloorBelowRate_KeepsRate`.
- **Criterios de aceptación:**
  - Dado el convenio de QA Cliente Uno con ALMACENAMIENTO `PER_CARGO_UNIT` para QA Aceite IMP con rate 70.000 y `minimumPerCargoUnit` 100.000, cuando se factura 2026BA00005 (1 tanquero), entonces la línea es 84.033,61 + IVA 15.966,39 = 100.000 rotulada «(mínimo aplicado)» y sin la advertencia de magnitud facturada dos veces.
  - Dado la misma regla sin piso, cuando se factura, entonces la línea es 70.000 + IVA = 83.300.
  - Dado la misma regla con `minimumIncludesVat` en «false», cuando se factura, entonces la línea es 100.000 + IVA = 119.000.
- **Re-test QA:** F6-FOR-013; REG F11-REG-021.
- **Riesgo de regresión:** bajo.
- **Tamaño:** S. **Dependencias:** CHG-24.

#### CHG-26 — Reglas para perecederos configurables y PATCH del servicio de convenio sin borrar campos

- **Cierra:** DEF-F1-003 (MAJOR), DEF-F6-012 (MAJOR), DEF-F6-015 (MINOR).
- **Causa raíz:**
  - DEF-F1-003: `Wms.Application/Services/Common/Dtos/ServicePricingRuleRequest.cs:9-15` no declara `AppliesToPerishable` (el JSON lo descarta); `CreateServicePricingRuleHandler.cs:41-50` no lo pasa; `UpdateServicePricingRuleHandler.cs:46` llama `rule.Update(...)` sin él y `ServicePricingRule.Update` lo asigna siempre (cada edición lo borra); `ServicePricingRuleDto` y `ServicePricingRuleMapper.ToDto` no lo devuelven.
  - DEF-F6-012: `Wms.Domain/Entities/Agreement/Agreement.cs:71-77` (`AddService`) y `:90-97` (`UpdateService`) comparan servicio, producto y modalidad sin el indicador, de ahí el 409; `AddAgreementServiceCommand.cs:6-15` y `UpdateAgreementServiceCommand.cs` no lo declaran; `Agreement.cs:99` llama `service.Update(...)` sin él; el índice `idx_agreement_service_unique_active` (`AgreementServiceConfiguration.cs:30-34`) tampoco lo incluye; `ActivateService` (`Agreement.cs:111`) no valida unicidad.
  - DEF-F6-015: `UpdateAgreementServiceHandler.cs` convierte `ProductId`, `OperationModalityId` y `LinkedServiceId` omitidos en `null`, y `AgreementService.Update` (`AgreementService.cs:67-77`) los asigna siempre.
- **Cambio exacto:**
  - Backend:
    - `Wms.Common/Patch/PatchField.cs` (`readonly record struct PatchField<T>(bool IsSet, T? Value)`) y `PatchFieldJsonConverterFactory` (propiedad ausente = `IsSet` falso; `null` explícito = limpiar), registrados en `Program.cs:49` y en `AddSwaggerGen` (`MapType`).
    - `UpdateAgreementServiceRequest`: `PatchField<string>` para `ProductId`, `OperationModalityId` y `LinkedServiceId`, `PatchField<bool?> AppliesToPerishable` y `Parameters` puede omitirse (ausente = se conservan). Clase pura `Wms.Application/Agreements/Common/AgreementServicePatch.Resolve(actual, petición)`; el validador lee `.Value`.
    - `AddAgreementServiceRequest` suma `bool? AppliesToPerishable`; `Stakeholder.UpdateAgreementService` (`:265`), `Agreement.UpdateService` (`:84`) y `AgreementService.Update` (`:67`) reciben el indicador. `AddService`, `UpdateService` y `ActivateService` comparan también el indicador: «Ya existe un servicio activo para este acuerdo con el mismo servicio, producto, modalidad y tipo de carga (perecedero).». `AgreementServiceDto` lo devuelve y `GetAgreementServicesHandler.cs:43` usa `MapToDto`.
    - Tarifa base: `ServicePricingRuleRequest` suma `bool? AppliesToPerishable`; Create y Update lo pasan (el PUT reemplaza todo y la pantalla siempre lo envía); `EnsureUniqueActiveRuleAsync(…, appliesToPerishable)` en Create (`:39`), Update (`:43`) y `ActivateServicePricingRuleHandler.cs:25`: «Ya existe una tarifa base activa para este servicio con el mismo producto, modalidad y tipo de carga (perecedero).»; `ServicePricingRuleDto` y `ToDto` lo devuelven.
    - Índices `idx_agreement_service_unique_active` e `idx_service_pricing_rule_unique_active` con `applies_to_perishable` y filtro `is_active = true`.
  - Frontend: ninguno (`AgreementServiceFormDialog.vue:495,507` y `ServicePricingRuleFormDialog.vue:463` ya envían el indicador).
  - No se toca: `RuleSpecificity` ni `BillingResolver` (ya resuelven por el indicador, `BillingResolver.cs:271,296`).
- **Migración o script:** `AddPerishableToRuleUniqueIndexes` (recrea los dos índices; son más permisivos, no hay datos que sanear).
- **Pruebas automatizadas nuevas:** `Wms.Tests/Common/PatchFieldJsonTests.cs`: `Deserialize_OmittedProperty_IsNotSet`, `Deserialize_ExplicitNull_IsSetWithNull`, `Deserialize_Value_IsSetWithValue`; `Wms.Tests/Agreements/AgreementServicePatchTests.cs`: `Resolve_OnlyParameters_KeepsProductModalityLinkedAndPerishable`, `Resolve_ExplicitNullProduct_ClearsProduct`, `Resolve_ExplicitNullPerishable_ClearsFlag`; `Wms.Tests/Domain/Agreements/AgreementServiceUniquenessTests.cs`: `AddService_GenericThenPerishableSameProductAndModality_Allowed`, `AddService_TwoPerishableSameScope_ThrowsConflict`, `AddService_PerishableAndNonPerishableSameScope_Allowed`, `UpdateService_KeepsAppliesToPerishable`, `ActivateService_DuplicatingActiveScope_ThrowsConflict`; `Wms.Tests/Domain/Services/ServicePricingRuleTests.cs`: `Create_AppliesToPerishableTrue_KeepsFlag`, `Update_WithFlagTrue_KeepsFlag`; `Wms.IntegrationTests/Billing/PerishableRulesTests.cs`: `CreatePricingRule_Perishable_ReturnsFlag`, `PatchAgreementService_OnlyParameters_KeepsProductAndModality`.
- **Criterios de aceptación:**
  - Dado ALMACENAMIENTO con tarifa base genérica para Cebolla e IMP, cuando el Admin crea otra con «Aplica a perecederos», entonces responde 201 y el detalle la muestra marcada; al editar su tarifa, el indicador se conserva.
  - Dado el convenio de QA Cliente Uno con ALMACENAMIENTO para Cebolla e IMP, cuando Facturación agrega la variante perecedera, entonces se guarda; una segunda variante perecedera igual responde 409 «Ya existe un servicio activo para este acuerdo con el mismo servicio, producto, modalidad y tipo de carga (perecedero).».
  - Dado ese servicio de convenio, cuando se envía un PATCH solo con los parámetros, entonces conserva producto, modalidad, servicio complementario e indicador.
- **Re-test QA:** F1-SRV-019, F6-TAR-009, F6-FOR-013; REG F11-REG-004, F11-REG-021.
- **Riesgo de regresión:** medio (cambia el contrato del PATCH). Lo mitigan las pruebas del convertidor y del PATCH.
- **Tamaño:** M. **Dependencias:** CHG-09, CHG-24.

#### CHG-27 — Los parámetros del convenio se validan con los mismos rangos que la tarifa base

- **Cierra:** DEF-F1-004 (MAJOR).
- **Causa raíz:** `AddAgreementServiceHandler.cs:73,96-123` y `UpdateAgreementServiceHandler.cs:88,125-152` tienen una `ValidateParameters` privada que revisa presencia, tipo y lista del esquema, pero no llama `FormulaCalculatorRegistry.ValidateParameters`, donde viven los rangos (`PercentageOfValueFormulaCalculator.cs:51-66`: porcentaje de 0 a 100, mínimo ≥ 0). La tarifa base sí los valida (`CreateServicePricingRuleHandler.cs:118`). Con 150 % el convenio se guarda y al facturar el resolutor falla y el grupo cae al mínimo.
- **Cambio exacto:**
  - Backend: clase estática `Wms.Application/Billing/Services/FormulaParameterValidator.Validate(registry, tipoDeFórmula, parámetros)` con el cuerpo de `CreateServicePricingRuleHandler.ValidateParameters` (esquema y `registry.ValidateParameters`). La usan Create y Update de tarifa base y Add y Update del servicio de convenio (en Update, solo cuando el PATCH trae `Parameters`); se borran las tres copias privadas. Mensaje con 150: «Parámetro inválido: 'percentage' debe ser un decimal en el rango 0–100.» (el mismo de la tarifa base).
  - Frontend: ninguno (el aviso global muestra el mensaje).
  - No se toca: los calculadores de fórmula.
- **Migración o script:** sin migración. `fase-05-reglas.sql` (solo detección): parámetros activos de convenios y tarifas base con `percentage` fuera de 0–100, `minimum` o `ratePerKg` negativos o `thresholdKg` ≤ 0; Facturación los corrige desde la pantalla de convenios.
- **Pruebas automatizadas nuevas:** `Wms.Tests/Billing/Services/FormulaParameterValidatorTests.cs`: `Validate_PercentageOfValue150_ThrowsRangeMessage`, `Validate_PercentageOfValue100_Passes`, `Validate_PercentageOfValueMinimumMinus1_Throws`, `Validate_WeightThresholdThreshold0_Throws`, `Validate_DecimalNotNumeric_ThrowsSchemaMessage`.
- **Criterios de aceptación:**
  - Dado el convenio de QA Cliente Uno, cuando Facturación guarda ALMACENAMIENTO con PERCENTAGE_OF_VALUE y porcentaje 150, entonces responde 400 «Parámetro inválido: 'percentage' debe ser un decimal en el rango 0–100.»; con 100 se guarda.
  - Dado ese servicio guardado con 1 %, cuando Facturación lo edita a 150, entonces responde 400 con el mismo mensaje y conserva 1 %.
- **Re-test QA:** F1-CNV-006; REG F11-REG-004.
- **Riesgo de regresión:** bajo.
- **Tamaño:** S. **Dependencias:** CHG-26.

#### CHG-28 — Se retira la creación manual de facturas de la pantalla y del API

- **Cierra:** DEF-F6-011 (MAJOR).
- **Causa raíz:** `Wms.Api/Controllers/v1/BillingController.cs:134-165` mantiene `POST billing/invoices` (política `BillingAccess`) y `app/pages/billing/invoices/create.vue` carga por URL aunque no tiene enlace. `CreateInvoiceCommand` solo lo envía ese endpoint; `GET billing/storage-invoice-draft` (`BillingController.cs:592-605`), `BillingPreviewPanel.vue`, `useCreateInvoice` y `useStorageInvoiceDraft` solo sirven a esa pantalla.
- **Cambio exacto (aplica §10 · Sin creación manual de facturas):**
  - Backend: se borran `Wms.Application/Billing/Commands/CreateInvoice/` (comando, handler y validador), la acción `CreateInvoice` (`BillingController.cs:127-166`), `CreateInvoiceRequest` y `CreateInvoiceItemRequestModel` (`:684-700`) con su `using` (`:9`), la acción `GetStorageInvoiceDraft` (`:592-605`) con su `using` (`:32`) y `Wms.Application/Billing/Queries/GetStorageInvoiceDraft/`.
  - Frontend: se borran `app/pages/billing/invoices/create.vue`, `app/features/billing/components/BillingPreviewPanel.vue`, `useCreateInvoice.ts` y `useStorageInvoiceDraft.ts` (y sus exportaciones en `composables/index.ts:3,30`), `createInvoice` y `getStorageInvoiceDraft` de `services/billing-service.ts` (`:58`, `:259`, `:313`, `:340`) y los tipos `ICreateInvoiceRequest` e `ICreateInvoiceItemRequest` (`types/requests.ts:50-70`).
  - No se toca: `Invoice.CreateForPeriod` y `CreateForWeighbridge*` (báscula, guías y almacenamiento), `OverrideAmountDialog`, `CustomerSelect` ni `useBillingPreview`.
- **Migración o script:** ninguno (la factura manual de QA quedó anulada).
- **Pruebas automatizadas nuevas:** `Wms.Tests/Api/BillingControllerSurfaceTests.cs`: `BillingController_HasNoCreateInvoiceAction`, `BillingController_HasNoStorageInvoiceDraftAction` (reflexión sobre `Wms.Api`); `Wms.IntegrationTests/Billing/ManualInvoiceRemovedTests.cs`: `PostInvoices_Returns405`.
- **Criterios de aceptación:**
  - Dado Facturación, cuando envía `POST billing/invoices`, entonces responde 405 y no se crea ninguna factura.
  - Dado Facturación, cuando escribe la URL `/billing/invoices/create`, entonces no aparece el formulario de creación manual.
- **Re-test QA:** F6-INV-020; REG F11-REG-002, F11-REG-022.
- **Riesgo de regresión:** bajo; no hay otros consumidores.
- **Tamaño:** S. **Dependencias:** CHG-22.

#### CHG-29 — El comprobante del pago se sube como archivo y se puede consultar

- **Cierra:** DEF-F6-010 (MAJOR).
- **Causa raíz:** `app/features/billing/components/PaymentDialog.vue:48-66` convierte el archivo a data-URL (`fileToBase64`) y lo envía en `voucherUrl`; `Wms.Infrastructure/Persistence/Configurations/Billing/InvoicePaymentConfiguration.cs:24` limita `voucher_url` a 500 caracteres y `RecordPaymentValidator` no valida longitud ni formato, así que un comprobante de 70 KB falla en PostgreSQL. Además ninguna pantalla muestra el comprobante guardado.
- **Cambio exacto:**
  - Backend: clase pura `Wms.Application/Billing/Common/Services/PaymentVoucherRules.cs`: extensiones `.jpg`, `.jpeg`, `.png`, `.webp` y `.pdf`; de 1 byte a 5 MiB; firma del contenido (JPEG, PNG, WEBP, `%PDF-`); nombre visible de hasta 255 caracteres; mensajes «Adjunte el comprobante del pago.», «El comprobante no puede superar 5 MB.», «El comprobante debe ser JPG, PNG, WEBP o PDF.» y «El contenido del archivo no corresponde a su extensión.». Acción `POST billing/payments/vouchers` en `BillingController.cs` (`multipart/form-data`, `RequestSizeLimit(5_500_000)`, política de la clase): valida, guarda con `IStorageService.SaveFileAsync(stream, "voucher{ext}", "payment-vouchers")` y responde `{ voucherUrl, voucherFileName }`. `RecordPaymentValidator`: `VoucherUrl` de hasta 500 caracteres y bajo `/payment-vouchers/` («El comprobante debe subirse como archivo (JPG, PNG, WEBP o PDF, máximo 5 MB).»); `VoucherFileName` de hasta 255.
  - Frontend: `PaymentDialog.vue` elimina `fileToBase64` y, dentro del guardia de envío de CHG-18, sube primero el archivo con `billingService.uploadPaymentVoucher(file)` (`api.postForm('/billing/payments/vouchers', fd)`), conserva la respuesta para reintentar sin volver a subir y envía `voucherUrl` y `voucherFileName`; `accept="image/jpeg,image/png,image/webp,application/pdf"` y `:max-file-size="5242880"`. Validación previa en `app/features/billing/utils/payment-voucher.ts`. Enlace «Ver comprobante» (`resolvePhotoUrl(voucherUrl)`) en `app/pages/billing/payments/index.vue` y en el detalle de la factura.
  - No se toca: `RecordPaymentRequest` ni su handler (siguen recibiendo JSON con la ruta).
- **Migración o script:** sin migración. `fase-05-comprobantes.sql` (solo detección): `SELECT id FROM invoice_payments WHERE voucher_url LIKE 'data:%';` (debe dar 0 filas).
- **Pruebas automatizadas nuevas:** `Wms.Tests/Billing/PaymentVoucherRulesTests.cs`: `Validate_Png5MiBExact_Accepts`, `Validate_Jpg5MiBPlus1_RejectsSizeMessage`, `Validate_Gif_RejectsTypeMessage`, `Validate_ExeBytesNamedPng_RejectsContentMessage`, `Validate_PdfUpperCaseExtension_Accepts`; `Wms.Tests/Billing/Validators/RecordPaymentValidatorTests.cs`: `Validate_VoucherUrlDataUrl_FailsWithMessage`, `Validate_VoucherUrlStoredPath_Passes`; `test/unit/billing/payment-voucher.spec.ts`: PDF de 5 MiB aceptado, GIF rechazado, 5 MiB + 1 rechazado; `Wms.IntegrationTests/Billing/PaymentVoucherUploadTests.cs`: `UploadVoucher_Pdf_ReturnsStoredPath`.
- **Criterios de aceptación:**
  - Dado una factura pendiente de QA Cliente Uno, cuando Facturación registra un pago con un comprobante PDF de 70 KB, entonces el pago se guarda y «Ver comprobante» abre el PDF.
  - Dado un comprobante GIF, cuando Facturación lo adjunta, entonces ve «El comprobante debe ser JPG, PNG, WEBP o PDF.» y no se envía el pago.
  - Dado un archivo de 6 MB, cuando se adjunta, entonces ve «El comprobante no puede superar 5 MB.».
- **Re-test QA:** F6-PAG-008; REG F11-REG-023.
- **Riesgo de regresión:** bajo.
- **Tamaño:** M. **Dependencias:** CHG-18, CHG-22, CHG-28.

### Fase 6 — MAJOR de inventario y de salidas sin guía

- **Objetivo:** que ninguna mercancía de importación salga sin guía (§10 · Salida de importación), que la guía se cobre a cada cliente dueño (§10 · Guía de orden multi-cliente) y conserve su levante, que el inventario solo cambie con movimiento y con validaciones de estado, y que báscula y Vigilancia respeten el orden del flujo (llegada a Bodega antes del segundo pesaje, salida sin ciclo abierto, tara no mayor que el bruto). Cierra DEF-F5-014, DEF-F8-003, DEF-F8-002, DEF-F8-004, DEF-F4-004, DEF-F3-012, DEF-F4-003, DEF-F3-005, DEF-F3-014, DEF-F5-002, DEF-F5-003, DEF-F5-004 y DEF-F5-005, y por compartir causa DEF-F5-011, DEF-F4-014 y DEF-F8-008.
- **Criterio de entrada:** checkpoint de la Fase 5 aprobado; migraciones de las fases 1 a 5 aplicadas.
- **Cambios:** CHG-30, CHG-31, CHG-32, CHG-33, CHG-34, CHG-35, CHG-36, CHG-37, CHG-38, CHG-39, CHG-40.
- **Orden interno:** CHG-30 (crea `EntryLogDepartureGuard`, al que CHG-33 agrega su regla) → CHG-31 → CHG-32 → CHG-33 → CHG-34 → CHG-35 (los tres tocan `CreateDispatchGuideCommandHandler.cs` o el PDF de la guía) → CHG-36 → CHG-37 (ambos en `CompleteCycleHandler.cs` y `RecordWeighingHandler.cs`, después de la regla de guía de CHG-33) → CHG-38 → CHG-39 (ambos en `AdjustInventoryCommandHandler.cs`) → CHG-40.
- **Migración de la fase (la genera el implementador con `dotnet ef`):** `AddDispatchGuideLineReleaseSnapshot`: columnas `dispatch_guide_lines.release_number` y `dispatch_guide_lines.acceptance_number` (`varchar(500)`, nulas).
- **Riesgos y mitigación:**
  - Báscula y Vigilancia empiezan a rechazar salidas de importación sin guía; camiones que hoy salen sin guía quedan retenidos hasta que CE la emita. Mitigación: aviso a CE y a Vigilancia antes del despliegue; el script lista las órdenes sin guía para regularizarlas antes.
  - Cambia el cobro de la guía de órdenes con varios clientes (más de una factura). Mitigación: vista previa del cobro en la pantalla, igual a la factura.
  - Las guías emitidas antes de la migración no tienen el levante guardado. Mitigación: el relleno posterior a la migración lo toma del levante vigente a la fecha de emisión.
- **Saneamiento de datos:** `fase-06-guias.sql`, `fase-06-guia-multicliente.sql`, `fase-06-levantes-guia.sql` (después de la migración), `fase-06-cargue-borrador.sql`, `fase-06-salidas.sql`, `fase-06-llegadas.sql`, `fase-06-ciclos-salida.sql`, `fase-06-taras.sql` y los de Comercio Exterior, descritos en cada cambio.
- **Criterio de salida:** compuertas comunes (regla 4.0.4) y en PASA: F3-PES-016, F2-SAL-005, F4-CAR-014, F5-COR-005, F5-COR-006, F4-CAR-007, F3-SAL-008, F3-SAL-009, E2E-01, F5-GUI-003, F3-SAL-005, F3-SAL-006, F4-CAR-001, F4-CAR-003, F4-CAR-008, E2E-10, E2E-17, F5-GUI-002, E2E-02, F4-REC-001, F4-REC-017, F4-REC-019, F3-PES-007, F3-COR-003, F5-AJU-004, F5-AJU-005, F5-AJU-001, F5-PRD-001, F5-PRD-002, F5-LEV-012, F5-LEV-013, F5-ETI-006; REG F11-REG-005, F11-REG-009, F11-REG-014, F11-REG-016, F11-REG-017, F11-REG-018, F11-REG-019, F11-REG-020, F11-REG-029.
- **Checkpoint:** se entrega al usuario la lista de órdenes regularizadas con su guía, la evidencia de una guía multicliente (una factura por cliente y vista previa igual al cobro), la reimpresión de 2026S00007 con su levante original y el resultado de las pruebas. El usuario aprueba la migración, el saneamiento en staging y el aviso operativo a Vigilancia y Báscula sobre la nueva regla de salida.

#### CHG-30 — Vigilancia no registra la salida de un camión con pesaje sin terminar

- **Cierra:** DEF-F3-005 (MAJOR).
- **Causa raíz:** `Wms.Application/Logistics/EntryLogs/Commands/RegisterDeparture/RegisterDepartureHandler.cs:47-52` solo valida que el ingreso no tenga salida, y la aprobación de una autorización de salida (`UpdateDepartureAuthorizationHandler.cs:64-84`) no valida nada. Después la tara se rechaza por la fecha de salida (`OperationalDateRules.cs:36-38`) y la cola oculta el camión (`GetWeighbridgeQueueHandler.cs:29`, `DateTimeDeparture == null`).
- **Cambio exacto:**
  - Backend: regla pura `Wms.Application/Weighbridge/Common/Services/DepartureBlockRules.cs` y guarda `Wms.Application/Logistics/EntryLogs/Common/EntryLogDepartureGuard.cs` (`EnsureCanDepartAsync(context, entryLogId)`), invocada en `RegisterDepartureHandler` antes de `RegisterDeparture` (`:52`) y en `UpdateDepartureAuthorizationHandler.ApplyApproval` antes de `:84`. Con un ciclo de báscula del ingreso en estado distinto de `Complete` y `Canceled` lanza `ConflictException("El camión {placa} tiene un pesaje de báscula sin terminar ({estado}). Termínelo o anúlelo en Báscula antes de registrar la salida.")`, con estado «por cobrar» (PendingPayment), «por pesar» (ReadyForWeighing) o «por repesar» (FirstWeightCaptured o InProgress).
  - Frontend: ninguno (`app/pages/operations/entries/exits.vue:118` ya muestra el mensaje del 409).
  - No se toca: `OperationalDateRules` (la defensa de fechas sigue) ni el servicio sin cobrar ni ciclo (se descarta desde «Recuperar operaciones»).
- **Migración o script:** sin migración. `fase-06-ciclos-salida.sql`: detección de ciclos abiertos de camiones con salida (`weighbridge_cycles` en PendingPayment, ReadyForWeighing, FirstWeightCaptured o InProgress cuyo `entry_logs.date_time_departure` no es nulo; p. ej. QAC406); Báscula los anula desde el historial con motivo.
- **Pruebas automatizadas nuevas:** `Wms.Tests/Weighbridge/DepartureBlockRulesTests.cs`: `Check_OpenCycleFirstWeight_ThrowsWithPlateAndPorRepesarLabel` («El camión ABC123 tiene un pesaje de báscula sin terminar (por repesar). Termínelo o anúlelo en Báscula antes de registrar la salida.»), `Check_ReadyForWeighing_UsesPorPesarLabel`, `Check_PendingPayment_UsesPorCobrarLabel`, `Check_NothingPending_DoesNotThrow`; `Wms.IntegrationTests/Logistics/DepartureGuardTests.cs`: `RegisterDeparture_WithOpenCycle_Returns409`.
- **Criterios de aceptación:**
  - Dado QAC406 registrado, cobrado y con primer peso, cuando Vigilancia registra la salida, entonces responde 409 «El camión QAC406 tiene un pesaje de báscula sin terminar (por repesar). Termínelo o anúlelo en Báscula antes de registrar la salida.» y el camión sigue en la cola de báscula.
  - Dado el mismo camión con la tara registrada, cuando Vigilancia registra la salida, entonces se registra.
- **Re-test QA:** F3-PES-016, F2-SAL-005; REG F11-REG-005.
- **Riesgo de regresión:** bajo.
- **Tamaño:** S. **Dependencias:** CHG-15.

#### CHG-31 — Cargue y devolución a Borrador con guardas de estado en los dos sentidos

- **Cierra:** DEF-F4-004 (MAJOR), DEF-F4-014 (MINOR).
- **Causa raíz:**
  - DEF-F4-004: `Wms.Domain/Entities/Warehouse/WarehouseStorage.cs:285-303` (`MarkForCorrection`) solo exige estado Confirmed y `ReturnStorageForCorrectionHandler.cs:33` no mira órdenes de cargue; `ExecuteLoadingOrderCommandHandler.cs:53-68` carga los depósitos de la orden pero nunca mira su estado. La creación de órdenes y el pesaje de salida sí rechazan Borrador (`LoadingOrderReservationService.cs:38-41`, `InitiateOutputWeighingHandler.cs:89-93`): el cargue es el único punto sin guarda.
  - DEF-F4-014 (parcialmente): `ExecuteLoadingOrderCommandHandler.cs:75-89` ya rechaza órdenes canceladas, completas y cargadas («La orden ya fue cargada.»), pero no las despachadas ni las revertidas, que llegan al 404 de reserva de `:157-161`. La orden 2026OC00006 del caso no estaba en Loaded cuando se reejecutó.
- **Cambio exacto:**
  - Backend:
    - `LoadingOrder.cs`: `EnsureExecutable()` con `BadRequestException` por estado: Cancelled «No se puede ejecutar una orden cancelada.», Complete «La orden ya está completa.», Loaded «La orden ya fue cargada.», Dispatched «La orden ya fue despachada.», Reverted «La orden fue revertida.»; Pending e InProgress pasan. El handler reemplaza `:75-89` por esa llamada. Y `BlocksStorageCorrection(status, hasActiveGuide)`: verdadero para Pending, InProgress y Loaded sin guía vigente.
    - `WarehouseStorage.MarkForCorrection(IReadOnlyCollection<string> activeLoadingOrders, string? reason = null)`: con órdenes activas lanza `ConflictException("No se puede devolver el depósito {número} a Borrador: tiene órdenes de cargue activas ({OC (estado)}, …). Cancele las pendientes o revierta las cargadas antes de devolverlo.")`. `ReturnStorageForCorrectionHandler` consulta las órdenes del depósito (Pending, InProgress o Loaded con indicador de guía vigente), filtra con `BlocksStorageCorrection` y etiqueta con `LoadingOrder.StatusLabel`.
    - `LoadingExecutionMath.EnsureStoragesConfirmed(orderNumber, storages)`: si algún depósito no está Confirmed → `BadRequestException("No se puede ejecutar el cargue de la orden {OC}: hay depósitos que no están confirmados ({depósito}: {estado}).")`, con el nuevo `WarehouseStorage.StatusLabel` (Borrador, Confirmado, Cerrado, Anulado); el handler lo llama después de `EnsureExecutable()`.
  - Frontend: ninguno (`useReturnStorageForCorrection.ts` y el aviso global muestran los mensajes).
  - No se toca: `CancelWarehouseStorage` ni `RevertLoadingOrder`.
- **Migración o script:** sin migración. `fase-06-cargue-borrador.sql`: detección de órdenes Pending, InProgress, Loaded, Dispatched o Complete con ítems de depósitos en Borrador (con lo cargado); corrección operativa sin `UPDATE`: CE confirma de nuevo el depósito o revierte la orden (devuelve el stock); las pendientes se cancelan.
- **Pruebas automatizadas nuevas:** `Wms.Tests/Domain/Warehouse/WarehouseStorageCorrectionTests.cs`: `MarkForCorrection_WithActiveLoadingOrders_ThrowsConflictWithExactMessage`, `MarkForCorrection_WithoutActiveOrders_ReturnsToDraft`; `LoadingOrderTransitionsTests.cs`: `EnsureExecutable_NotExecutableStatus_ThrowsWithMessage` (Theory de 5 estados), `EnsureExecutable_PendingOrInProgress_DoesNotThrow`, `BlocksStorageCorrection_ByStatusAndGuide` (Theory); `LoadingExecutionMathTests.cs`: `EnsureStoragesConfirmed_DraftStorage_ThrowsWithMessage`, `EnsureStoragesConfirmed_AllConfirmed_DoesNotThrow`.
- **Criterios de aceptación:**
  - Dado 2026INSP00001 confirmado con la orden 2026OC00009 pendiente, cuando CE intenta devolverlo a Borrador, entonces responde 409 «No se puede devolver el depósito 2026INSP00001 a Borrador: tiene órdenes de cargue activas (2026OC00009 (pendiente)). Cancele las pendientes o revierta las cargadas antes de devolverlo.».
  - Dado un depósito en Borrador con una orden, cuando Bodega ejecuta el cargue, entonces responde 400 «No se puede ejecutar el cargue de la orden 2026OC00009: hay depósitos que no están confirmados (2026INSP00001: Borrador).» y el stock no cambia.
  - Dado una orden despachada, cuando se ejecuta de nuevo, entonces responde 400 «La orden ya fue despachada.»; una orden cargada responde «La orden ya fue cargada.».
- **Re-test QA:** F4-CAR-014, F5-COR-005, F5-COR-006, F4-CAR-007; REG F11-REG-016, F11-REG-017.
- **Riesgo de regresión:** bajo.
- **Tamaño:** M. **Dependencias:** CHG-15.

#### CHG-32 — La salida en báscula valida la orden y la pone «en cargue»

- **Cierra:** DEF-F3-012 (MAJOR), DEF-F8-008 (MINOR).
- **Causa raíz:** `Wms.Application/Weighbridge/Commands/Output/Initiate/InitiateOutputWeighingHandler.cs:62-93` carga la orden y solo valida que exista, que tenga ítems y el estado de los depósitos: no mira el estado de la orden (cancelada, despachada) ni si ya tiene un servicio de salida activo, que sí validan `AddAdditionalOrdersCommandHandler.cs:53-67` y `ExitWithEntryTicketCommandHandler.cs:48-78`. Además crea el servicio (`:136-144`) sin tocar la orden: `LoadingOrder.StartLoading` solo se llama al cargar (`ExecuteLoadingOrderCommandHandler.cs:141-145`), así que la orden sigue Pending y nunca se persiste InProgress ni `LoadingOrder.ServiceRecordId`.
- **Cambio exacto:**
  - Backend:
    - Regla pura `Wms.Application/Weighbridge/Common/Services/OutputInitiationRules.cs`: estado permitido Pending, InProgress o Loaded; si no, `ConflictException("La orden {OC} está {estado}; no se puede iniciar la salida en báscula.")` (estado con `LoadingOrder.StatusLabel`); con servicio de salida activo, `ConflictException("La orden {OC} ya tiene un servicio de salida en báscula.")`.
    - `InitiateOutputWeighingHandler`: después del bloqueo del ingreso (CHG-17) bloquea la orden (`SELECT id FROM loading_orders WHERE id = {id} FOR UPDATE`), calcula el servicio activo y aplica la regla antes de crear el servicio; luego llama `loadingOrder.BeginWeighbridgeExit(serviceRecord.Id)`.
    - `LoadingOrder`: `BeginWeighbridgeExit(Guid serviceRecordId)` (Pending → InProgress con `LoadingStartDate`; InProgress y Loaded conservan su estado; siempre fija `ServiceRecordId`) y `ReleaseWeighbridgeExit(Guid serviceRecordId)` (si el servicio es el enlazado, limpia `ServiceRecordId` y una orden InProgress vuelve a Pending). `AddAdditionalOrdersCommandHandler.cs:70-78` y `ExitWithEntryTicketCommandHandler.cs:87-96` llaman `BeginWeighbridgeExit`; `DiscardIncompleteOperationHandler` (tras descartar una salida) y `VoidWeighingCommandHandler.cs:102-108, 358-362` llaman `ReleaseWeighbridgeExit`.
  - Frontend: ninguno («En progreso» ya existe en `app/features/warehouse/types/loading-order.ts:7`).
  - No se toca: `AdditionalOutputOrderRules`, `EntryTicketExitRules` ni `ExecuteLoadingOrderCommandHandler` (sigue llamando `StartLoading` solo con la orden Pending).
- **Migración o script:** sin migración (el índice de salida por orden es de CHG-17). `fase-06-salidas.sql`: detección de servicios de salida activos sobre órdenes Cancelled, Reverted, Dispatched o Complete (se descartan desde «Recuperar operaciones»); corrección de órdenes Pending con salida en curso (`UPDATE loading_orders SET status = 'InProgress', loading_start_date = COALESCE(loading_start_date, now()), service_record_id = sr.id …`) y enlace del servicio de salida en las demás órdenes sin `service_record_id`.
- **Pruebas automatizadas nuevas:** `Wms.Tests/Weighbridge/OutputInitiationRulesTests.cs`: `Check_Cancelled_ThrowsConflictWithStatusMessage`, `Check_Dispatched_Throws`, `Check_Complete_Throws`, `Check_Reverted_Throws`, `Check_ActiveService_ThrowsAlreadyHasOutputMessage`, `Check_PendingInProgressLoadedWithoutService_Passes`; `LoadingOrderTransitionsTests.cs`: `BeginWeighbridgeExit_Pending_GoesInProgressAndLinksService`, `BeginWeighbridgeExit_Loaded_KeepsLoadedAndLinks`, `ReleaseWeighbridgeExit_InProgress_ReturnsToPendingAndClearsLink`, `ReleaseWeighbridgeExit_OtherService_DoesNothing`; `Wms.IntegrationTests/Weighbridge/OutputInitiationTests.cs`: `InitiateOutput_SameOrderTwice_SecondReturns409`, `InitiateOutput_CancelledOrder_Returns409`.
- **Criterios de aceptación:**
  - Dado QAB205 con la salida iniciada con 2026OC00001, cuando otro camión (QAC408) inicia una salida con la misma orden, entonces responde 409 «La orden 2026OC00001 ya tiene un servicio de salida en báscula.».
  - Dado la orden 2026OC00003 cancelada, cuando báscula inicia una salida con ella, entonces responde 409 «La orden 2026OC00003 está cancelada; no se puede iniciar la salida en báscula.».
  - Dado la orden 2026OC00020 pendiente, cuando báscula inicia la salida con ella, entonces la orden pasa a «En progreso»; si esa operación se descarta, la orden vuelve a «Pendiente».
- **Re-test QA:** F3-SAL-008, F3-SAL-009, E2E-01 (paso 10); REG F11-REG-019.
- **Riesgo de regresión:** bajo.
- **Tamaño:** M. **Dependencias:** CHG-17, CHG-06.

#### CHG-33 — Una orden de importación solo se despacha con guía vigente

- **Cierra:** DEF-F5-014 (MAJOR), DEF-F8-003 (MAJOR).
- **Causa raíz:** ningún punto que despacha una orden consulta la guía, todos llaman `LoadingOrder.Dispatch()` (`LoadingOrder.cs:211-225`): el repesaje de salida (`RecordWeighingHandler.cs:414-418` y `:471-477` → `DispatchLoadingOrderIfLoadedAsync`, `:500-520`; `CompleteCycleHandler.cs:224-236`; órdenes ancladas en `SharedOutputDispatch.cs:28-33`), el cargue con la salida ya registrada (`ExecuteLoadingOrderCommandHandler.cs:333-356`, la ruta de DEF-F8-003 con `SourceEntryCycleId`), la salida con tiquete de ingreso (`ExitWithEntryTicketCommandHandler.cs:94-96`) y las órdenes adicionales (`AddAdditionalOrdersCommandHandler.cs:77-78`). Después, `CreateDispatchGuideCommandHandler.cs:115-123` rechaza las órdenes Dispatched («No se puede generar guía para una orden en estado 'Dispatched'.») y Vigilancia registra la salida sin mirar órdenes (`RegisterDepartureHandler.cs:35-52`). Los despachos sin guía no cuentan en los saldos congelados (`DispatchGuideBalanceService.cs:40-47`): la guía posterior de BA00001 mostró saldo anterior 160 con stock real 31.
- **Cambio exacto (aplica §10 · Salida de importación):**
  - Backend:
    - Regla pura `Wms.Application/ForeignTrade/Common/Services/ImportGuideRules.cs`: una orden es de importación si algún ítem pertenece a un depósito de modalidad `IMP*`; `ShouldDispatch(status, exitRegistered, requiresGuide, hasActiveGuide)` = estado Loaded y salida registrada y (no requiere guía o tiene guía vigente); `EnsureScaleCanClose(orderNumber, requiresGuide, hasActiveGuide)` y `DepartureBlockedMessage(placa, órdenes)`.
    - `LoadingOrderGuideReader.cs` (EF): estado de guía por orden (guía con `cancelled_at` nulo), salida registrada (lógica que hoy vive en `ExecuteLoadingOrderCommandHandler.cs:333-351`) y órdenes de importación cargadas o despachadas sin guía de un ingreso.
    - Báscula: `RecordWeighingHandler` (antes de cerrar en `:414` y antes del pesaje en `:471`) y `CompleteCycleHandler` (antes de `:131` con orden) llaman `EnsureScaleCanClose`: `ConflictException("No se puede cerrar el pesaje de salida: la orden {OC} es de importación y no tiene guía de salida vigente. Comercio Exterior debe emitir la guía antes de cerrar el pesaje.")`.
    - Salida con tiquete y órdenes adicionales: `EntryTicketExitRules` y `AdditionalOutputOrderRules` devuelven `AwaitingGuide` cuando la orden de importación no tiene guía; los handlers solo despachan con `Now` y sus resultados agregan `AwaitingGuide`.
    - Cargue: `ExecuteLoadingOrderCommandHandler.cs:333-356` despacha solo si `ShouldDispatch`; sin guía la orden queda Loaded sin error, Comercio Exterior recibe «Orden {OC} cargada (Importación) con la salida ya registrada. Genere la guía de salida: con ella la orden se despacha.» y el mensaje del resultado agrega « Falta la guía de salida: Comercio Exterior fue notificado.».
    - Guía: `LoadingOrder.EnsureGuidable()` solo rechaza Cancelled y Reverted («No se puede generar guía para la orden {OC}: está {cancelada|revertida}.»); una orden Dispatched o Complete sin guía vigente recibe guía (regularización) y una con guía vigente conserva el conflicto «Ya existe una guía de salida para esta orden de cargue.». El tipo de guía se decide con todos los ítems (`ImportGuideRules`), no con el primero. Al emitir, si la orden está Loaded y ya salió, se despacha. `GetPendingImportLoadingOrdersHandler.cs:29-31` y `GetPendingGuidesQuery.cs:26-29` incluyen las Dispatched y Complete sin guía vigente (el DTO agrega `Status`).
    - Exportación: `CreateExportDispatchGuideCommandHandler.cs:139` despacha solo si la orden está Loaded. Inspección: sin guía, como hoy (`GuideType.cs:18-21`).
    - Vigilancia: `EntryLogDepartureGuard` (CHG-30) agrega la regla de órdenes de importación cargadas o despachadas del ingreso sin guía vigente: «No se puede registrar la salida del vehículo {placa}: la orden {OC} es de importación y no tiene guía de salida vigente. Comercio Exterior debe emitir la guía.» (en plural: «… las órdenes {OC1}, {OC2} son de importación y no tienen guía de salida vigente. Comercio Exterior debe emitir las guías.»).
  - Frontend: `app/features/weighbridge/types/weighbridge-cycle.ts:233-250` agrega `awaitingGuide`; con ese indicador, `ExitWithEntryTicketDialog.vue:73-75`, `app/pages/operations/weighbridge/index.vue:758-761` y `AdditionalOrdersDialog.vue:77-78` dicen «Se despacha cuando esté cargada y tenga guía de salida». `DispatchGuideForm.vue:221-225`: «Órdenes de importación sin guía vigente: pendientes, en cargue, cargadas o despachadas sin guía.» y la etiqueta «Despachada sin guía».
  - No se toca: `LoadingOrder.Dispatch()`, `RevertDispatchToLoaded()`, `RevertLoadingOrderCommandHandler` (sigue exigiendo anular la guía primero) ni `DispatchGuideBalanceService` (los saldos nuevos cuadran con la regla).
- **Migración o script:** sin migración. `fase-06-guias.sql`: detección de órdenes Loaded, Dispatched o Complete con ítems de depósitos IMP y sin guía vigente (en la base local: 2026OC00001, 00002, 00005, 00029 despachadas y 00006, 00018, 00019 cargadas). Las cargadas siguen el flujo normal; para cada despachada, CE emite una guía de regularización desde «Crear guía» con la fecha de salida igual a `loading_orders.departure_date` y destinatario «Por facturar»; si no corresponde cobrarla, Facturación anula ese Borrador con el motivo «Guía de regularización (DEF-F5-014)». La misma consulta con `LIKE 'EXP%'` debe devolver 0 filas.
- **Pruebas automatizadas nuevas:** `Wms.Tests/ForeignTrade/ImportGuideRulesTests.cs` (`RequiresGuide_ImportDeposit_ReturnsTrue`, `RequiresGuide_MixedExportAndImport_ReturnsTrue`, `RequiresGuide_ExportOrInspectionOnly_ReturnsFalse`, `ShouldDispatch_LoadedExitedImportWithGuide_ReturnsTrue`, `ShouldDispatch_LoadedExitedImportWithoutGuide_ReturnsFalse`, `ShouldDispatch_LoadedExitedInspectionWithoutGuide_ReturnsTrue`, `ShouldDispatch_NotLoaded_ReturnsFalse`, `EnsureScaleCanClose_ImportWithoutGuide_ThrowsConflict` con «2026OC00010», `DepartureBlockedMessage_OneOrder_UsesSingular`, `DepartureBlockedMessage_TwoOrders_UsesPlural`); `EntryTicketExitRulesTests.cs`: `LoadedImportOrderWithoutGuide_AwaitsGuide`, `LoadedImportOrderWithGuide_DispatchesNow`; `AdditionalOutputOrderRulesTests.cs`: `LoadedImportOrderWithCompleteAnchorAndNoGuide_AwaitsGuide`; `LoadingOrderTransitionsTests.cs`: `EnsureGuidable_DispatchedOrder_Passes`, `EnsureGuidable_CancelledOrReverted_ThrowsWithLabel`; `Wms.IntegrationTests/ForeignTrade/ImportExitRequiresGuideTests.cs`: `CloseExitWeighing_ImportOrderWithoutGuide_Returns409`, `LoadAfterEntryTicketExit_WithoutGuide_StaysLoaded_ThenGuideDispatches`, `RegisterDeparture_ImportOrderLoadedWithoutGuide_Returns409`.
- **Criterios de aceptación:**
  - Dado la orden de importación 2026OC00001 cargada y sin guía, cuando báscula intenta el repesaje de salida, entonces responde 409 «No se puede cerrar el pesaje de salida: la orden 2026OC00001 es de importación y no tiene guía de salida vigente. Comercio Exterior debe emitir la guía antes de cerrar el pesaje.» y el ciclo sigue abierto; con la guía emitida, el repesaje cierra el ciclo y la orden queda despachada.
  - Dado 2026BA00036 con levante y la orden 2026OC00029 (20) con la salida registrada con el tiquete de ingreso de QAE026, cuando Bodega carga, entonces la orden queda cargada (no despachada) y CE recibe «Orden 2026OC00029 cargada (Importación) con la salida ya registrada. Genere la guía de salida: con ella la orden se despacha.»; cuando CE emite la guía, la orden pasa a despachada.
  - Dado QAE026 con esa orden cargada y sin guía, cuando Vigilancia registra la salida, entonces responde 409 «No se puede registrar la salida del vehículo QAE026: la orden 2026OC00029 es de importación y no tiene guía de salida vigente. Comercio Exterior debe emitir la guía.».
  - Dado una orden de importación despachada sin guía, cuando CE abre «Crear guía», entonces la orden aparece como «Despachada sin guía» y la guía se emite.
  - Dado una orden de exportación, cuando Bodega carga, entonces la guía se genera sin cargo y la orden se despacha como hoy; una orden de inspección se despacha sin guía.
- **Re-test QA:** F5-GUI-003, F3-SAL-005, F3-SAL-006, F4-CAR-001, F4-CAR-003, F4-CAR-008, E2E-01, E2E-10, E2E-17; REG F11-REG-016, F11-REG-019, F11-REG-020, F11-REG-029.
- **Riesgo de regresión:** alto (cambia el cierre de la salida en tres módulos). Lo mitigan las pruebas de reglas puras, las de integración y el re-test E2E completo de importación.
- **Tamaño:** L. **Dependencias:** CHG-30, CHG-31, CHG-32.

#### CHG-34 — La guía se cobra a cada cliente dueño, con el total visible antes de crearla

- **Cierra:** DEF-F8-002 (MAJOR), DEF-F5-011 (MINOR).
- **Causa raíz:**
  - DEF-F8-002 (parcialmente): la rama de destinatario «Clientes» ya factura por dueño (`CreateDispatchGuideCommandHandler.cs:215-306`), pero nada exige ese modo cuando la orden tiene varios dueños (`:143-153`): con destinatario único, `:307-372` factura todo al primer dueño (`:311`). El firmante sale de `loadingOrder.Stakeholder.Name` (`:167-172`), que es el primer cliente de la orden (`CreateLoadingOrderCommandHandler.cs:109-121`). En la rama multicliente el pago inmediato queda fijo en efectivo (`:289`) y no se valida la mora de cada dueño (solo en `:326`).
  - DEF-F5-011: en modo multicliente `app/features/billing/components/BillingCollectForm.vue:238` no precarga el total, `:587` y `:629` ocultan «Total a pagar», `:535-540` solo muestra un aviso y `:356` envía `totalAmount: 0`. `/billing/preview` no sirve para la guía porque su cálculo es plano y la factura multiplica la tarifa por depósito (`CreateDispatchGuideCommandHandler.cs:225-235`). `app/pages/foreign-trade/dispatch-guides/create.vue:74` muestra el GUID de la orden y `:98-104` textos obsoletos («GSI-YYYYMMDD-NNNN», «Se registrará automáticamente la hora de salida», «crédito (30 días)», «se marcará como despachada»).
- **Cambio exacto (aplica §10 · Guía de orden multi-cliente):**
  - Backend:
    - Clase pura `DispatchGuideBillingPlan.Build(depósitos por dueño, precio por dueño, IVA)`: un cargo por dueño con `UnitPrice × depósitos`, subtotal, IVA y total; sin precio, `BadRequestException("No se encontró precio para la guía de salida del cliente '{nombre}'. Configure un precio estándar o convenio para el servicio GUIA_SALIDA.")` antes de escribir nada.
    - `CreateDispatchGuideCommandHandler`: con más de un dueño y destinatario distinto de «Clientes» → `BadRequestException("La orden {OC} tiene depósitos de {n} clientes: la guía se factura a cada cliente dueño. Use el destinatario «Clientes».")`; valida la mora de cada dueño (§10 · Mora); el pago inmediato registra un pago por factura con el método, la referencia y las notas del formulario; «Por facturar» crea la factura a crédito con el plazo del cliente o suma la línea a su consolidada en Borrador (lógica actual `:240-261`). `DispatchGuideResultDto` agrega la lista `Invoices` (id, número, cliente, total).
    - Clase pura `DispatchGuideSignerRules.Resolve(...)`: con más de un dueño o más de un importador firma el conductor («{nombres} {apellidos} ({cédula})», como el legacy validado en DEF-F8-002); con un importador y firmante «Importador», el nombre del IMPORTER del depósito (no el cliente); sin importador y firmante «Importador» → `BadRequestException("Los depósitos de la orden {OC} no tienen importador registrado: seleccione al conductor como firmante.")`. Reemplaza `:167-172`.
    - Consulta nueva `GET foreign-trade/loading-orders/{id}/dispatch-guide-preview` (`ForeignTradeController`, política de clase): `isMultiClient`, `charges[]` (cliente, depósitos, tarifa, IVA, total), totales, importadores y firmante, calculados con las mismas dos clases. Errores: 404 «La orden de cargue no existe.», 400 de precio y 400 «La orden {OC} no es de importación: no lleva guía de salida manual.». `GetPendingImportLoadingOrdersHandler.cs:62` lista los dueños separados por coma.
  - Frontend:
    - `foreign-trade-service.ts` (`getDispatchGuidePreview`), composable `useDispatchGuidePreview.ts` (clave `["foreign-trade", "dispatch-guide-preview", orderId]`, invalidada al crear la guía) y tipos en `types/dispatch-guide.ts`.
    - `BillingCollectForm.vue`: props `multiClientCharges`, `multiClientLoading`, `multiClientError` y `lockMultiClient`; en modo «Clientes» muestra la tabla Cliente · Depósitos · Tarifa · IVA · Total y la fila «Total a cobrar», con «Calculando tarifa…» mientras carga; el error bloquea «Crear Guía de Salida»; con `lockMultiClient` deshabilita los otros destinatarios.
    - `DispatchGuideForm.vue`: usa la vista previa, activa `lockMultiClient` con `isMultiClient` y fija el firmante «Conductor» con el texto «Con varios clientes dueños la guía la firma el conductor.».
    - `create.vue`: se borra el bloque `:68-77` y los textos `:96-105` pasan a: «Se asigna el consecutivo anual de guías de salida (por ejemplo, 2026S00001).», «La fecha y hora de salida se digitan en el formulario; el vencimiento es la salida más los días de tránsito de la ciudad de destino de la orden.», «Se factura el servicio de guía a cada cliente dueño de los depósitos de la orden, con su convenio o el precio general, por depósito.», «Pago inmediato: se registra el pago de cada factura al crear la guía. Por facturar: cada factura queda a crédito con el plazo de su cliente o en su factura consolidada.», «Con la guía vigente, la báscula puede cerrar el pesaje de salida y Vigilancia puede registrar la salida del camión.» y «El PDF se descarga al crear la guía y se puede reimprimir desde el historial.». `useCreateDispatchGuide.ts:11-16`: con más de una factura, «{n} facturas generadas por $ {total}».
  - No se toca: `/billing/preview` (lo usan báscula y montacargas), `ForeignTradeService.GetGuidePriceAsync`, `BillingRecipientFactory` ni `LoadingOrder.StakeholderId`.
- **Migración o script:** sin migración. `fase-06-guia-multicliente.sql`: detección de guías vigentes cuya orden tiene más de un cliente dueño y una sola factura (en la base local, 2026S00011); CE anula la guía y emite otra con destinatario «Clientes» (permitido para órdenes despachadas por CHG-33).
- **Pruebas automatizadas nuevas:** `Wms.Tests/ForeignTrade/DispatchGuideBillingPlanTests.cs`: `Build_TwoOwners_OneChargePerOwnerWithOwnPrice` (30.000 y 35.000 → 65.000), `Build_SameOwnerTwoDeposits_MultipliesPricePerDeposit` (2 × 30.000 = 60.000), `Build_WithTax19_SplitsTax`, `Build_OwnerWithoutPrice_ThrowsBadRequest`; `DispatchGuideSignerRulesTests.cs`: `Resolve_TwoOwners_ForcesDriver`, `Resolve_TwoImporters_ForcesDriver`, `Resolve_SingleImporter_UsesImporterName` («QA Importación Andina Ltda»), `Resolve_NoImporterAndImporterRequested_ThrowsBadRequest`; `Wms.IntegrationTests/ForeignTrade/MultiClientGuideTests.cs`: `CreateGuide_TwoOwners_OneInvoicePerOwner`, `CreateGuide_TwoOwnersSingleRecipient_Returns400`, `Preview_TotalEqualsCreatedInvoices`; `test/components/billing/BillingCollectForm.spec.ts`: en modo «Clientes» muestra una fila por cliente y «Total a cobrar».
- **Criterios de aceptación:**
  - Dado la orden 2026OC00025 con 2026BA00004 (QA Cliente Uno) y 2026BA00017 (QA Cliente Consolidado), cuando CE emite la guía con destinatario «Clientes», entonces se generan dos facturas GUIA_SALIDA, una por cliente con la tarifa de su convenio o el precio general por depósito, y la guía la firma el conductor.
  - Dado la misma orden, cuando se envía un destinatario único, entonces responde 400 «La orden 2026OC00025 tiene depósitos de 2 clientes: la guía se factura a cada cliente dueño. Use el destinatario «Clientes».».
  - Dado «Continuar al cobro», cuando CE revisa el cobro, entonces ve una fila por cliente y «Total a cobrar» antes de crear la guía, y ese total es la suma de las facturas generadas.
  - Dado una orden de un solo cliente cuyo depósito tiene importador QA Importación Andina Ltda, cuando se emite con firmante «Importador», entonces la guía imprime la firma del importador QA Importación Andina Ltda, no la del cliente.
  - Dado `create.vue`, cuando CE la abre, entonces no aparece el GUID de la orden ni el texto «GSI-YYYYMMDD-NNNN».
- **Re-test QA:** E2E-10, F5-GUI-002, F5-GUI-003; REG F11-REG-020.
- **Riesgo de regresión:** medio. Lo mitigan la vista previa calculada con las mismas clases que la factura y las pruebas de integración.
- **Tamaño:** L. **Dependencias:** CHG-33.

#### CHG-35 — La guía conserva el levante vigente al emitirla

- **Cierra:** DEF-F8-004 (MAJOR).
- **Causa raíz:** `Wms.Application/ForeignTrade/Common/Services/DispatchGuidePdfService.cs:499-504` calcula al imprimir el levante más reciente de todo el depósito (cargado en `:149-152`), sin filtrar por producto; `DispatchGuideLine.cs:21-31` congela los saldos pero no el levante. Al registrar QAE-LEV-022, la reimpresión de 2026S00007 cambió de levante.
- **Cambio exacto:**
  - Backend: `DispatchGuideLine` agrega `ReleaseNumber` y `AcceptanceNumber` (`string?`, parámetros finales con valor nulo en `Create` y en `DispatchGuide.AddLine`, `DispatchGuide.cs:147`); configuración `HasMaxLength(500)`, nulas. Clase pura `ReleaseSnapshotSelector.Latest(levantes)`: el de mayor `AcceptanceDate`, desempate por `CreatedAt`; nulo sin levantes. `DispatchGuideBalanceService.FreezeLinesAsync` (`:10-67`) toma los levantes del producto de cada línea y guarda los dos números al emitir. `DispatchGuidePdfService.cs:499-504` imprime los valores de la línea y se elimina el `Include` de levantes de `:149-152`.
  - Frontend: ninguno.
  - No se toca: la lista de levantes del informe diario de salidas (`GetDailyOutgoingGoodsReportHandler.cs:171-182`).
- **Migración o script:** `AddDispatchGuideLineReleaseSnapshot`. `fase-06-levantes-guia.sql`, después de la migración: rellena `release_number` y `acceptance_number` de las líneas de guías de importación con el levante más reciente del producto creado hasta la fecha de emisión de la guía (2026S00007 → QAE-LEV-021; 2026S00008 → QAE-LEV-022); las guías sin levante quedan en nulo e imprimen el campo en blanco.
- **Pruebas automatizadas nuevas:** `Wms.Tests/ForeignTrade/ReleaseSnapshotSelectorTests.cs`: `Latest_PicksHighestAcceptanceDate`, `Latest_SameAcceptanceDate_BreaksTieWithCreatedAt`, `Latest_NoReleases_ReturnsNull`; `Wms.Tests/Domain/Warehouse/DispatchGuideLineTests.cs`: `AddLine_WithRelease_StoresSnapshot` («QAE-LEV-021»); `Wms.IntegrationTests/ForeignTrade/GuideReleaseSnapshotTests.cs`: `NewRelease_AfterEmission_DoesNotChangeStoredRelease`.
- **Criterios de aceptación:**
  - Dado 2026BA00027 con el levante QAE-LEV-021 (50), la orden 2026OC00021 y la guía 2026S00007, y después el levante QAE-LEV-022 (48), la orden 2026OC00022 y la guía 2026S00008, cuando CE reimprime 2026S00007, entonces la guía muestra QAE-LEV-021 y los saldos 98 / 98 / 50 / 48, igual que la original.
- **Re-test QA:** E2E-02 (paso 5); REG F11-REG-020.
- **Riesgo de regresión:** bajo.
- **Tamaño:** M. **Dependencias:** CHG-34.

#### CHG-36 — El segundo pesaje exige la llegada registrada en Bodega

- **Cierra:** DEF-F4-003 (MAJOR).
- **Causa raíz:** no existe la guarda: `RecordWeighingHandler.cs:223-242` (pesaje intermedio) y `CompleteCycleHandler.cs:163-175` (pesaje final) no consultan las recepciones. `GetPendingFromWeighbridgeHandler.cs:22-26` solo lista ciclos con primer peso o de un solo pesaje: una entrada con ciclo de dos pesajes completo queda sin recepción posible desde la interfaz. `PendingSecondWeightDto.HasWarehouseReception` (`GetPendingSecondWeightHandler.cs:83-85`) existe pero ninguna pantalla lo usa.
- **Cambio exacto (aplica §10 · Llegada a Bodega):**
  - Backend: regla pura `ReceptionArrivalRules` y guarda `ReceptionArrivalGuard.EnsureArrivedAsync(context, entrada)` en `Wms.Application/Weighbridge/Common/Services/`. Llegada registrada = existe una recepción de la entrada activa y no cancelada; si no, `ConflictException("El camión {placa} no tiene registrada su llegada a Bodega (depósito {número}). Bodega debe registrar la llegada antes del segundo pesaje.")`. Aplica a servicios que no son de pesaje único y que tienen entradas de depósito (incluidos los de unidades de carga); no aplica a INSP ni perecederos de pesaje único, Solo báscula ni salidas. Se llama en `RecordWeighingHandler` antes de `AssignExitWeighing` (`:242`) y en `CompleteCycleHandler` tras elegir la entrada pendiente (`:169-175`). La cola (`GetWeighbridgeQueueHandler`) agrega `AwaitingWarehouseArrival` a cada camión por repesar. `GetPendingFromWeighbridgeHandler.cs:22-26` incluye los ciclos completos sin recepción (predicado extraído a `PendingReceptionFilters.cs`).
  - Frontend: `app/features/weighbridge/types/queue.ts` (`awaitingWarehouseArrival`) y `TruckQueue.vue:144-148`: etiqueta «Falta llegada a Bodega» junto al estado «Por repesar».
  - No se toca: `RegisterReceptionArrivalCommandHandler`, `CreateReceptionCommandHandler` ni el flujo de pesaje único.
- **Migración o script:** sin migración. `fase-06-llegadas.sql`: detección de entradas con ciclo completo de dos pesajes, depósito abierto y sin recepción activa (las 15 de QA); con el cambio de filtro aparecen en «Ingresos» de Bodega, que registra la llegada y completa la recepción.
- **Pruebas automatizadas nuevas:** `Wms.Tests/Weighbridge/ReceptionArrivalRulesTests.cs`: `Check_NoArrival_ThrowsExactMessage` («El camión ABC123 no tiene registrada su llegada a Bodega (depósito 2026BA00012). Bodega debe registrar la llegada antes del segundo pesaje.»), `Check_ArrivalRegistered_Passes`, `Check_SingleWeightService_Skips`; `Wms.Tests/Warehouse/PendingReceptionFiltersTests.cs`: `CompleteTwoWeighingCycleWithoutReception_IsPending`, `CompleteCycleWithActiveReception_IsNotPending`, `CompleteCycleWithCancelledReception_IsPending`, `ClosedDeposit_IsNotPending`; `Wms.IntegrationTests/Weighbridge/SecondWeighingRequiresArrivalTests.cs`: `SecondWeighing_WithoutArrival_Returns409`.
- **Criterios de aceptación:**
  - Dado QAA101 (importación, dos pesajes) con primer peso y sin llegada registrada en Bodega, cuando báscula intenta el segundo pesaje, entonces responde 409 «El camión QAA101 no tiene registrada su llegada a Bodega (depósito 2026BA00001). Bodega debe registrar la llegada antes del segundo pesaje.» y la cola muestra «Falta llegada a Bodega».
  - Dado el mismo camión con la llegada registrada, cuando báscula registra la tara, entonces el ciclo se completa.
  - Dado una inspección de pesaje único o un Solo báscula, cuando báscula pesa, entonces no se exige la llegada.
  - Dado entradas de ciclo completo sin recepción, cuando Bodega abre «Ingresos», entonces aparecen y se reciben con el flujo normal.
- **Re-test QA:** F4-REC-001, F4-REC-017, F4-REC-019; REG F11-REG-009, F11-REG-014.
- **Riesgo de regresión:** medio (agrega un paso obligatorio entre báscula y Bodega). Lo mitiga la etiqueta en la cola, que avisa antes del intento.
- **Tamaño:** M. **Dependencias:** CHG-33.

#### CHG-37 — La tara no puede superar el peso bruto

- **Cierra:** DEF-F3-014 (MAJOR).
- **Causa raíz:** ningún camino de captura compara los pesos: `CompleteCycleHandler.cs:113-122` solo exige el tipo opuesto y `:152-161` crea el pesaje final; `RecordWeighingHandler.cs:460-477` (salidas y Solo báscula) tampoco; las correcciones (`ModifyFirstWeightHandler.cs:62`, `ModifySecondWeightHandler.cs:66`) tampoco. El servidor guarda el neto físico con `Math.Abs` (`WarehouseStorageEntry.cs:156-160`) y la pantalla calcula bruto − tara sin validar (`app/features/weighbridge/components/WeightCapture.vue:297-305`).
- **Cambio exacto:**
  - Backend: regla pura `Wms.Application/Weighbridge/Common/Services/WeighingPairRules.cs`: `EnsureTareNotAboveGross(pesajes en secuencia)` toma el primero y el último; con tara mayor que bruto lanza `BadRequestException("La tara ({tara} kg) no puede ser mayor que el peso bruto ({bruto} kg).")` con formato es-CO; tara igual al bruto es válida; los pesajes intermedios no participan. Se llama en `CompleteCycleHandler` (entre `:122` y `:131`), en `RecordWeighingHandler` antes de `:471` y en los dos handlers de corrección después de modificar el peso.
  - Frontend: `WeightCapture.vue` (`onSubmit`, antes de `:219`) y `ModifyWeighingDialog.vue` (`:70`, `:93`) usan la función pura nueva `tareExceedsGross` (`app/features/weighbridge/utils/weighing-rules.ts`) y muestran el mismo mensaje sin enviar. `ModifyWeighingDialog.vue:57` identifica el primer peso con `sequence === 1`, pero el backend numera desde 0 (`WeighbridgeCycle.cs:171`, `ModifyFirstWeightHandler.cs:56`), así que las correcciones de primer y segundo peso quedan invertidas (`:112-123`): pasa a `sequence === 0` (hallazgo de la verificación, sin ficha propia; la regla de la tara depende de identificar bien cada peso).
  - No se toca: `WeighingTotals` ni el `Math.Abs` del neto físico.
- **Migración o script:** sin migración. `fase-06-taras.sql`: detección de ciclos completos con tara mayor que bruto (QAC410); se corrigen con «Modificar peso» y motivo.
- **Pruebas automatizadas nuevas:** `Wms.Tests/Weighbridge/WeighingPairRulesTests.cs`: `GrossThenTare_TareAboveGross_ThrowsExactMessage` (15.000 y 35.000 → «La tara (35.000 kg) no puede ser mayor que el peso bruto (15.000 kg).»), `TareThenGross_TareAboveGross_Throws`, `TareEqualsGross_IsValid`, `GrossThenTare_Normal_IsValid`, `IntermediateBetween_DoesNotParticipate`, `SingleWeighing_IsValid`; `test/unit/weighbridge/weighing-rules.spec.ts`: `tareExceedsGross(15000, 35000)` verdadero y `(30000, 12000)` falso, `isFirstWeighing(0)` verdadero e `isFirstWeighing(1)` falso.
- **Criterios de aceptación:**
  - Dado QAC410 con bruto 15.000, cuando báscula registra una tara de 35.000, entonces la pantalla muestra «La tara (35.000 kg) no puede ser mayor que el peso bruto (15.000 kg).» sin enviar, el API responde 400 con el mismo mensaje y el ciclo sigue abierto.
  - Dado un ciclo completo, cuando se modifica el segundo peso a un valor mayor que el bruto, entonces responde 400 con el mismo mensaje.
  - Dado una tara igual al bruto, cuando se registra, entonces se acepta con neto 0.
  - Dado un ciclo completo de QAA101, cuando báscula corrige el primer peso desde el historial, entonces cambia el pesaje 1 y no el 2.
- **Re-test QA:** F3-PES-007, F3-COR-003; REG F11-REG-009.
- **Riesgo de regresión:** bajo.
- **Tamaño:** S. **Dependencias:** CHG-36.

#### CHG-38 — El ajuste CE-7 valida primero, respeta los levantes y no depende del correo

- **Cierra:** DEF-F5-003 (MAJOR), DEF-F5-004 (MAJOR).
- **Causa raíz:**
  - DEF-F5-003: `Wms.Application/Warehouse/Commands/AdjustInventory/AdjustInventoryCommandHandler.cs:116` envía el correo con `SendRequiredEmailToMultipleAsync` antes de las validaciones del dominio (`WarehouseStorageProduct.CorrectReceivedQuantity`, invocado en `:131` y `:136`) y antes de `SaveChangesAsync` (`:146`); `EmailService.cs:183-219` relanza la `SmtpException` y el ajuste responde 500. Con unidades de carga, `delta` (`:100`) mezcla el recibido del producto con el de la unidad.
  - DEF-F5-004: `CorrectReceivedQuantity` (`WarehouseStorageProduct.cs:334-356`) solo exige stock resultante ≥ reservado y ≥ 0; nunca consulta los levantes, así que el recibido queda por debajo de lo nacionalizado.
- **Cambio exacto:**
  - Backend: `AdjustInventoryCommandHandler.Handle` en este orden: (1) precondiciones sin efectos (estado, unidad de carga y parámetro `INVENTORY_ADJUSTMENT_ADMIN_EMAIL`, con el 400 actual si falta); (2) calcula el nuevo recibido del producto (con unidad de carga: recibido del producto + nuevo de la unidad − declarado de la unidad), suma los levantes del producto y llama `NationalizationBalance.EnsureReceivedCoversReleases(producto, nuevoRecibido, levantado)` → «La cantidad recibida de «{producto}» ({nuevo}) no puede ser menor que la suma de sus levantes ({levantado}). Edite o retire primero el levante.»; luego `CorrectReceivedQuantity`; (3) `SaveChangesAsync`; (4) correo con `SendEmailToMultipleAsync` dentro de `try/catch`: si falla, se registra el error y la respuesta lleva `AdminNotified = false`; (5) `RecalculateAsync`. `delta` = stock nuevo − stock anterior. `InventoryMovementResultDto` suma `AdminNotified`. Se elimina `SendRequiredEmailToMultipleAsync` (`IEmailService.cs:34`, `EmailService.cs:183`) y se actualiza la descripción de `InventoryAdjustmentController.cs:25-34`.
  - Frontend: `app/pages/foreign-trade/imports/[id]/index.vue:113-123`, `exports/[id]/index.vue` e `inspections/[id]/index.vue`: con `adminNotified === false`, aviso «Cantidad ajustada» / «El ajuste se aplicó, pero no se pudo enviar el correo al administrador.»; `AdjustInventoryDialog.vue:163-165`: «Si el correo no se puede enviar, el ajuste se aplica igual.».
  - No se toca: los mensajes 400 del dominio ni `CorrectReceivedQuantity`.
- **Migración o script:** sin migración. `fase-06-levantes-recibido.sql` (solo detección): productos cuya suma de levantes supera el recibido (+0,0001); en la base local, 2026BA00004 se restituye a recibido ≥ 20 con un CE-7 ya corregido.
- **Pruebas automatizadas nuevas:** `Wms.Tests/ForeignTrade/NationalizationBalanceTests.cs`: `EnsureReceivedCoversReleases_BelowReleased_Throws` (15 frente a 20, «Aceite»), `EnsureReceivedCoversReleases_EqualToReleased_Passes`, `EnsureReceivedCoversReleases_NoReleases_Passes`, `EnsureReceivedCoversReleases_WithinTolerance_Passes`; `Wms.IntegrationTests/Warehouse/AdjustInventoryCommandHandlerTests.cs` (con un doble de `IEmailService`): `Handle_SameQuantity_Throws400_AndSendsNoEmail`, `Handle_BelowReserved_Throws400_AndSendsNoEmail`, `Handle_BelowReleases_Throws400_AndSendsNoEmail`, `Handle_SmtpFails_StillPersistsAdjustment_AdminNotifiedFalse`, `Handle_CargoUnit_EmailUsesProductDelta`.
- **Criterios de aceptación:**
  - Dado 2026BA00004 con Aceite recibido 20 y levantes por 20, cuando CE lo ajusta a 15, entonces responde 400 «La cantidad recibida de «Aceite» (15) no puede ser menor que la suma de sus levantes (20). Edite o retire primero el levante.» y no se envía correo.
  - Dado el servidor de correo caído, cuando CE ajusta 2026INSP00001 de 35 a 34, entonces el ajuste se guarda, la respuesta trae `adminNotified: false` y la pantalla muestra «El ajuste se aplicó, pero no se pudo enviar el correo al administrador.».
- **Re-test QA:** F5-AJU-004, F5-AJU-005; REG F11-REG-018.
- **Riesgo de regresión:** bajo.
- **Tamaño:** M. **Dependencias:** CHG-31.

#### CHG-39 — Todo cambio de stock por Comercio Exterior deja un movimiento en el kárdex

- **Cierra:** DEF-F5-002 (MAJOR).
- **Causa raíz:** `AdjustInventoryCommandHandler.cs:122-146` cambia el stock sin `InventoryMovement` (el comentario de `:122-125` lo deja fuera del kárdex) y devuelve `MovementId = Guid.Empty` (`:156`) y `Reason = null` (`:165`). La corrección de productos (WMS-29) tampoco lo registra: `UpdateDepositProductCommandHandler.cs:58` y `DepositProductEditing.cs:28-32,263` recalculan `ReceivedQuantity` y `CurrentStock` con `RecalculateFromEntries`, y `AddToEntryAsync` (alta de producto y `AssociatePackingListItemsCommandHandler.cs:76`) suma stock sin movimiento. El filtro `sourceType` sí se aplica (`GetInventoryMovementsHandler.cs:49-52`), pero un valor inválido se enlaza en silencio a `null` y la documentación de `WarehouseController.cs:976-979` y las etiquetas del frontend usan valores que no existen.
- **Cambio exacto:**
  - Backend:
    - Clase pura `Wms.Application/Warehouse/Common/Services/StockChangeMovement.For(stockAnterior, stockNuevo)`: `null` si no cambia; si sube, `In` con la diferencia; si baja, `Out` (no `Adjustment`: los informes y `ReconcileDeposits` solo suman In y Out).
    - `AdjustInventoryCommandHandler`: antes de `SaveChangesAsync`, `InventoryMovement.Create(producto, tipo, cantidad, SourceTypeMovements.Adjustment, anterior, nuevo, sourceId: depósito, reason: observación, authorizedBy: usuario)`; devuelve `MovementId` y `Reason` reales; `AdjustInventoryCommandValidator` limita la observación a 500 caracteres («La observación no puede exceder 500 caracteres.»). Se actualizan los textos que decían «sin movimiento» (`:122-125`, `AdjustInventoryCommandValidator.cs:17-18`, `InventoryAdjustmentController.cs:25-34`, `WarehouseStorageProduct.cs:329-333`) y el pie del correo: «La corrección queda registrada en la auditoría y en el kárdex (movimiento de entrada o salida, origen Ajuste).».
    - Origen nuevo `SourceTypeMovements.DepositProductEdit` (se guarda como texto, sin migración). `DepositProductEditing.RecordStockChange(producto, anterior, usuario, motivo)` se llama en `UpdateDepositProductCommandHandler` (anterior capturado antes de aplicar cantidades) y en `AddToEntryAsync` (anterior 0 en una línea nueva; motivo del alta o «Lista de empaque {n}»). `AddDepositProductCommand` y `UpdateDepositProductCommand` reciben `UserId` desde `GetRequiredUserId()` (`ForeignTradeController.cs:598`). `DepositProductDependencies` no cuenta los movimientos `DepositProductEdit` como dependencia y `RemoveDepositProductCommandHandler` los borra antes de retirar la línea.
    - `WarehouseController.GetInventoryMovements` (`:991`): con `ModelState` inválido lanza `BadRequestException("Parámetro no válido: {campos}. Valores de sourceType: ReceptionLog, LoadingOrder, Adjustment, Damage, Return, DeclaredEntry, LoadingOrderReversal, WeighingVoid, StorageCancellation, MigrationOpening, DepositProductEdit.")`; se corrige la documentación de `:976-979`.
  - Frontend: un solo mapa de etiquetas con los 11 orígenes en `app/features/warehouse/utils/inventory-labels.ts` («Ajuste CE-7», «Corrección de producto», …), usado por `types/inventory.ts:5-12`, `app/pages/warehouse/inventory/index.vue:218-228` y `useWarehouseExports.ts:6-15`; «Ajustes» (`inventory/index.vue:489`) filtra `sourceType=Adjustment`; `AdjustInventoryDialog.vue:163-165,277,288` ya no dice «no deja registro en el sistema».
  - No se toca: `KardexAggregator` ni `ReceptionDeclaredDifference`.
- **Migración o script:** sin migración. `fase-06-kardex.sql` (solo detección): productos cuyo stock difiere de Σ entradas − Σ salidas. En la base local son datos de QA (INSP00001, BA00008, Aceite) y no se corrigen; en producción, la regularización (un movimiento por la diferencia con motivo «Regularización DEF-F5-002») requiere la aprobación del usuario.
- **Pruebas automatizadas nuevas:** `Wms.Tests/Warehouse/StockChangeMovementTests.cs`: `For_StockIncreases_ReturnsIn` (3 → 4: entrada 1), `For_StockDecreases_ReturnsOut` (30 → 25: salida 5), `For_NoChange_ReturnsNull`; `Wms.IntegrationTests/Warehouse/AdjustInventoryMovementTests.cs`: `Handle_Valid_CreatesOutMovementWithUserAndReason`; `Wms.IntegrationTests/ForeignTrade/DepositProductEditingMovementTests.cs`: `UpdateDepositProduct_QuantityChange_CreatesMovement`, `AddDepositProduct_NewLine_CreatesInFromZero`, `RemoveDepositProduct_AfterEdit_IsAllowed`; `test/unit/warehouse/inventory-labels.spec.ts`: cada origen del enum tiene etiqueta en español.
- **Criterios de aceptación:**
  - Dado 2026INSP00001 con stock 30, cuando CE lo ajusta a 25 con la observación «Conteo físico», entonces el kárdex muestra una salida de 5 con origen «Ajuste CE-7», el usuario de CE, el motivo y los saldos 30 → 25.
  - Dado un producto de 2026BA00008 con 3 unidades, cuando CE corrige la cantidad a 4, entonces aparece una entrada de 1 con origen «Corrección de producto».
  - Dado el inventario, cuando Bodega filtra «Ajustes», entonces solo aparecen movimientos de origen Ajuste; un `sourceType=MANUAL` responde 400 con la lista de valores.
- **Re-test QA:** F5-AJU-001, F5-PRD-001, F5-PRD-002; REG F11-REG-014.
- **Riesgo de regresión:** medio (cambia lo que cuentan el kárdex y los informes). Lo mitiga que Σ movimientos = stock pasa a cumplirse.
- **Tamaño:** L. **Dependencias:** CHG-38.

#### CHG-40 — Levantes y etiquetas solo en el estado que corresponde

- **Cierra:** DEF-F5-005 (MAJOR).
- **Causa raíz:** `RegisterImportReleaseCommandHandler.cs:36` solo rechaza Borrador, así que Anulado y Cerrado aceptan levantes; `UpdateImportReleaseCommandHandler.cs:30-35` no mira el estado del depósito; `LabelGenerationService.cs:54,280,484` imprime etiquetas de depósitos anulados (y `:86-88` las rotula «NACIONALIZADA» por tener levantes). En la interfaz, `app/pages/foreign-trade/imports/[id]/index.vue:402-421` (`canRegisterRelease`) no mira el estado, los botones de `:683` y `:714` y «Editar levante» (`:712`) quedan visibles, y `ImportDepositList.vue:147` ofrece «Nacionalizar» sin estado porque `ImportDepositDto` no lo trae.
- **Cambio exacto:**
  - Backend: clase pura `Wms.Application/ForeignTrade/Common/Services/ReleaseStateGuard.EnsureCanRegister(estado)`: Confirmado pasa; Borrador → «No se pueden registrar levantes en un depósito en estado Borrador. Confirme primero el depósito.»; Anulado → «No se pueden registrar levantes en un depósito anulado.»; Cerrado → «No se pueden registrar levantes en un depósito cerrado.». La llama `RegisterImportReleaseCommandHandler:36`. `UpdateImportReleaseCommandHandler` incluye el depósito y, si está anulado, lanza «No se pueden editar levantes de un depósito anulado.». `LabelGenerationService`, en los tres generadores, rechaza el depósito anulado con «No se puede imprimir la etiqueta de un depósito anulado.» (Borrador sigue imprimiendo). `ImportDepositDto` suma `WarehouseStorageStatus`.
  - Frontend: regla pura `canRegisterRelease(detalle)` en `app/features/foreign-trade/utils/release-rules.ts` (verdadero solo en Confirmado con saldo pendiente), usada en `imports/[id]/index.vue:402-421`; «Editar levante» (`:712`) con `v-if="canWithdrawRelease"`; `ImportDepositList.vue:147` exige `warehouseStorageStatus === 'Confirmed'`.
  - No se toca: `WithdrawImportReleaseCommandHandler` (ya rechaza anulados) ni la regla de la etiqueta «NACIONALIZADA» con cualquier levante (§10 · Etiqueta NACIONALIZADA).
- **Migración o script:** sin migración. `fase-06-levantes-anulados.sql`: detección de levantes en depósitos anulados; corrección en la base local y en staging: se borra el levante (QA-LEV-1100 de 2026BA00011) y, si el depósito queda sin levantes, `import_warehouse_storages` vuelve a `SinNacionalizar` con cantidades nacionalizadas en 0.
- **Pruebas automatizadas nuevas:** `Wms.Tests/ForeignTrade/ReleaseStateGuardTests.cs`: `EnsureCanRegister_Draft_Throws`, `EnsureCanRegister_Cancelled_Throws`, `EnsureCanRegister_Closed_Throws` (mensajes exactos), `EnsureCanRegister_Confirmed_Passes`; `test/unit/foreign-trade/release-rules.spec.ts`: falso en Borrador, Anulado y Cerrado; verdadero en Confirmado con saldo; falso en Confirmado sin saldo.
- **Criterios de aceptación:**
  - Dado 2026BA00011 anulado, cuando CE registra un levante por el API, entonces responde 400 «No se pueden registrar levantes en un depósito anulado.»; cuando pide su etiqueta, responde 400 «No se puede imprimir la etiqueta de un depósito anulado.».
  - Dado un depósito en Borrador, cuando CE abre su detalle, entonces no aparece «Registrar levante».
- **Re-test QA:** F5-LEV-012, F5-LEV-013, F5-ETI-006; REG F11-REG-018.
- **Riesgo de regresión:** bajo.
- **Tamaño:** M. **Dependencias:** CHG-39.

### Fase 7 — MAJOR restantes: productos, trazabilidad, visibilidad de depósitos y báscula

- **Objetivo:** cerrar los MAJOR que no tocan dinero ni salidas: el alta y la edición de productos (500), la trazabilidad (camiones que salieron siguen «En portería» y etapas «Desconocido»), el detalle de los depósitos cerrados de exportación, la hora del pesaje (§10 · Hora del pesaje), el multidepósito, el conductor y el vehículo en Solo báscula y Salida, y las acciones del historial de báscula. Cierra DEF-F1-001, DEF-F2-004, DEF-F7-002, DEF-F4-006, DEF-F3-003, DEF-F3-011, DEF-F3-008, DEF-F3-013 y, por compartir causa, DEF-F5-006.
- **Criterio de entrada:** checkpoint de la Fase 6 aprobado.
- **Cambios:** CHG-41, CHG-42, CHG-43, CHG-44, CHG-45, CHG-46, CHG-47.
- **Orden interno:** CHG-41 → CHG-42 → CHG-43 → CHG-44 → CHG-45 (ambos en `WeightCapture.vue`) → CHG-46 → CHG-47.
- **Migración de la fase:** ninguna.
- **Riesgos y mitigación:**
  - Los contadores de la trazabilidad cambian («Completados» incluye las salidas registradas). Mitigación: aviso al Admin y a CE con la fecha del despliegue.
  - Los tiquetes dejan de copiar la hora del ingreso. Mitigación: el operario corrige la hora cuando registra tarde un pesaje.
- **Saneamiento de datos:** `fase-07-horas-pesaje.sql` y `fase-07-conductores.sql` (solo detección), descritos en cada cambio.
- **Criterio de salida:** compuertas comunes (regla 4.0.4) y en PASA: F1-PRO-001, F1-PRO-002, F1-PRO-005, F1-PRO-007, F2-INT-007, F7-TRZ-001, F7-TRZ-005, F4-CAR-009, F5-TAB-002, F5-TAB-003, F3-PES-003, F3-TIQ-002, F3-MUL-001, F3-MUL-002, F3-MUL-003, F3-MUL-004, F3-CAM-010, F3-CAM-011, F3-HIS-008, F3-COR-002; REG F11-REG-002, F11-REG-006, F11-REG-009, F11-REG-011, F11-REG-012, F11-REG-013, F11-REG-016, F11-REG-028.
- **Checkpoint:** se entrega al usuario la trazabilidad de un día con salidas y descartes, un tiquete con dos pesajes y sus horas reales, un ingreso multidepósito y el resultado de las pruebas.

#### CHG-41 — Alta, detalle y edición de productos sin error 500

- **Cierra:** DEF-F1-001 (MAJOR).
- **Causa raíz:** `Wms.Application/Products/Common/Mappers/ProductMapper.cs:11-12` lee `UnitMeasure.Code` y `UnitMeasure.Name`, y `Product.cs:28` declara la navegación no nula, así que el mapeo no tiene guarda. Ningún handler carga esa navegación: `CreateProductHandler.cs:40-45` mapea después de guardar (`:43`, `:45`) y `UnitMeasureGuard` solo proyecta el `Id`; `GetProductHandler.cs:18-20` incluye `PackagingType` y no `UnitMeasure` (falla en `:24`); `UpdateProductHandler.cs:20-21` no tiene `Include` y mapea en `:47` después de guardar en `:45`. Por eso el alta y la edición quedan guardadas y responden 500. El listado funciona porque proyecta en SQL (`GetAllProductHandler.cs:38-54`).
- **Cambio exacto:**
  - Backend: nuevo `Wms.Application/Products/Common/Mappers/ProductProjection.cs` con `Expression<Func<Product, ProductDto>> ToDto` (la proyección de `GetAllProductHandler.cs:38-54`: `PackagingTypeName = p.PackagingType != null ? p.PackagingType.Name : null`, `UnitMeasureCode = p.UnitMeasure.Code`, `UnitMeasureName = p.UnitMeasure.Name`). `GetProductHandler` consulta con `AsNoTracking().Where(id).Select(ProductProjection.ToDto).FirstOrDefaultAsync` y, si no existe, `NotFoundException("El producto no existe.")`. `CreateProductHandler` y `UpdateProductHandler` devuelven, después de `SaveChangesAsync`, la misma proyección por `Id` (así el PATCH que cambia la unidad devuelve la nueva). `GetAllProductHandler` usa `ProductProjection.ToDto`. Se eliminan `ProductMapper.cs`, el alias de `Wms.Application/DependencyInjection.cs:22` y el registro de `:45`.
  - Frontend: ninguno (`useProductCreate.ts`, `useProductUpdate.ts`, `useProductByID.ts` y las páginas `admin/products/*` dejan de mostrar el error al recibir 2xx).
  - No se toca: el dominio `Product` ni las validaciones de unicidad (CHG-49).
- **Migración o script:** ninguno (el alta fallida sí guardó el producto; el reintento fue rechazado por nombre duplicado, no quedan datos inconsistentes).
- **Pruebas automatizadas nuevas:** `Wms.Tests/Products/ProductProjectionTests.cs`: `ToDto_WithUnitAndWithoutPackaging_MapsUnitFieldsAndNullPackagingName` (unidad SACO «Saco» → `UnitMeasureCode == "SACO"`, `UnitMeasureName == "Saco"`, `PackagingTypeName == null`), `ToDto_MapsIdentityFields` («QA Cebolla», «QA-001», activo); `Wms.IntegrationTests/Products/ProductEndpointsTests.cs`: `Create_Returns201WithUnit`, `GetById_SeededProduct_Returns200`, `Patch_ChangingUnit_Returns200WithNewUnit`.
- **Criterios de aceptación:**
  - Dado el Admin en «Nuevo producto», cuando crea «QA Cebolla» con unidad Saco, entonces responde 201 y el detalle muestra la unidad «Saco».
  - Dado un producto sembrado, cuando el Admin abre su detalle, entonces responde 200 con sus datos.
  - Dado «QA Cebolla», cuando el Admin cambia la unidad a Kilogramo, entonces responde 200 y la respuesta trae la unidad «Kilogramo».
- **Re-test QA:** F1-PRO-001, F1-PRO-002, F1-PRO-005, F1-PRO-007; REG F11-REG-002.
- **Riesgo de regresión:** bajo.
- **Tamaño:** S. **Dependencias:** ninguna.

#### CHG-42 — La trazabilidad respeta la salida y no muestra etapas «Desconocido»

- **Cierra:** DEF-F2-004 (MAJOR), DEF-F7-002 (MAJOR).
- **Causa raíz:** `Wms.Application/Reports/Queries/GetTraceabilityDashboard/TruckStageResolver.cs:20-21` devuelve «En portería» para un ingreso Registered sin servicio antes de mirar la salida, que solo se evalúa al final (`:55-56`); `:58` devuelve «Desconocido» para las combinaciones sin regla (servicio descartado, ciclo InProgress, servicio en pesaje sin ciclo propio, ingreso Completed sin servicio). El resumen de `GetTraceabilityDashboardHandler.cs:179-186` cuenta `InGate` por el rótulo sin excluir salidos, compara en `:182` contra «En báscula (1er peso)», que el resolver nunca devuelve (`TruckStageResolver.cs:33` devuelve «Pesado (1er peso)»), y `Completed` solo cuenta «Completado».
- **Cambio exacto:**
  - Backend:
    - Nuevo `TruckStages.cs` con las constantes de los rótulos y `All`.
    - `TruckStageResolver.Determine` (misma firma), primera regla que cumple: (1) con salida: «Cancelado» si el ciclo está Canceled o el servicio Discarded; «Completado» si el ciclo está Complete o el servicio Completed; si no, «Salida registrada»; (2) sin servicio: «En portería»; (3) servicio InTransit: «En tránsito»; (4) ciclo abierto: PendingPayment «Pendiente pago», ReadyForWeighing «Listo para pesaje», FirstWeightCaptured «Pesado (1er peso)», InProgress «Pesaje en curso»; (5) Unloading «En bodega (descarga)», Loading «En bodega (carga)», PendingDeparture «Pendiente salida»; (6) ciclo Complete: «Completado» si el servicio está Completed o es entrada de almacenamiento, si no «Pesaje completo»; (7) servicio Completed: «Completado»; (8) ciclo Canceled o servicio Discarded: «Cancelado»; (9) cualquier otro caso: «En tránsito». Desaparece «Desconocido».
    - El cálculo del resumen pasa a la clase pública `TraceabilitySummaryCalculator.Calculate(camiones)`: `InGate` = «En portería»; `InWeighbridge` = «Pendiente pago», «Listo para pesaje», «Pesado (1er peso)» y «Pesaje en curso»; `Completed` = «Completado» o «Salida registrada»; los demás contadores como hoy.
  - Frontend: `app/features/traceability/types/index.ts:3-16` quita «En báscula (1er peso)» y agrega «Pesaje en curso»; `TruckStageBadge.vue:8-25` agrega «Pesaje en curso» (`severity: "warn"`, `pi pi-arrows-v`); `TruckDetailSidebar.vue:11-25` agrega «Pesaje en curso» con el paso 1 y quita la clave obsoleta.
  - No se toca: `ServiceRecord.cs`, los handlers de pesaje, `TraceabilityStats.vue` ni la firma de `Determine` (las 3 pruebas de `TruckStageResolverTests` siguen pasando).
- **Migración o script:** ninguno (la etapa se calcula en cada consulta).
- **Pruebas automatizadas nuevas:** en `Wms.Tests/Reports/TruckStageResolverTests.cs`: `Departed_WithoutServiceRecord_IsDepartureRegistered`, `NotDeparted_WithoutServiceRecord_EntryCompleted_IsInGate`, `Departed_WithCompleteCycle_IsCompleted`, `Departed_WithOpenCycle_IsDepartureRegistered`, `Departed_WithCanceledCycle_IsCanceled`, `Discarded_OnSite_IsCanceled`, `InProgressCycle_IsWeighingInProgress`, `Weighing_WithoutCycle_IsInTransit`, `Determine_AllCombinations_NeverReturnsUnknown` (recorre todas las combinaciones de estados y afirma que el resultado pertenece a `TruckStages.All`); nueva `Wms.Tests/Reports/TraceabilitySummaryCalculatorTests.cs`: con camiones «En portería», «Salida registrada», «Completado» en sitio, «Pesado (1er peso)» y «Pesaje en curso» afirma `TotalEntries == 5`, `InSite == 4`, `InGate == 1`, `Completed == 2`, `InWeighbridge == 2`.
- **Criterios de aceptación:**
  - Dado QAB204 con salida registrada y sin servicio, cuando se abre la trazabilidad, entonces aparece «Salida registrada» y no cuenta en «En portería».
  - Dado QAC408 con el servicio descartado y sin salida, cuando se abre la trazabilidad, entonces aparece «Cancelado».
  - Dado cualquier camión del día, cuando se abre la trazabilidad, entonces ninguno aparece como «Desconocido» y los contadores suman lo mismo que la lista.
- **Re-test QA:** F2-INT-007, F7-TRZ-001, F7-TRZ-005; REG F11-REG-006.
- **Riesgo de regresión:** bajo.
- **Tamaño:** M. **Dependencias:** ninguna.

#### CHG-43 — Los depósitos cerrados se ven y los anulados no cuentan en el tablero

- **Cierra:** DEF-F4-006 (MAJOR), DEF-F5-006 (MINOR).
- **Causa raíz:** `WarehouseStorage.Close()` pone `IsActive = false` (`WarehouseStorage.cs:325-326`) y las consultas de exportación e inspección usan `IsActive` como visibilidad: `GetExportDepositDetailHandler.cs:67` (404), `GetExportDepositByIdHandler.cs:24`, `GetExportDepositsHandler.cs:28`, `GetInspectionDepositDetailHandler.cs:65`, `GetInspectionDepositsHandler.cs:26` y la etiqueta de inspección (`LabelGenerationService.cs:484`); el tablero (`GetDepositsHandler`) sí los lista y enlaza a un detalle que da 404. En importación es al revés: `GetImportDepositsHandler.cs:27-38` no excluye los anulados y el tablero de CE (`useForeignTradeDashboard.ts:17-44`) los cuenta; además la tarjeta «Guías pendientes» enlaza al historial (`app/pages/foreign-trade/index.vue:43`).
- **Cambio exacto:**
  - Backend: en `DepositSearchQueryExtensions.cs`, la expresión `Listed = ws => ws.Status != WarehouseStorageStatus.Cancelled` y `WhereListed()`. `GetImportDepositsHandler.cs:27`, `GetExportDepositsHandler` y `GetInspectionDepositsHandler` usan `WhereListed()` (listan Borrador, Confirmado y Cerrado; los anulados siguen en la columna «Anulado» del tablero Kanban). Los detalles de exportación e inspección y la etiqueta de inspección dejan de filtrar por `IsActive` y responden en cualquier estado.
  - Frontend: `app/pages/foreign-trade/index.vue:43` → `route: '/foreign-trade/dispatch-guides/pending'`.
  - No se toca: `WarehouseStorage.Close()`, `GetDepositsHandler` ni `GetLoadingOrderDepositsHandler` (allí `IsActive` es intencional).
- **Migración o script:** ninguno.
- **Pruebas automatizadas nuevas:** `Wms.Tests/ForeignTrade/DepositVisibilityTests.cs`: `Listed_CancelledStorage_IsFalse`, `Listed_DraftConfirmedClosed_IsTrue`, `Listed_ClosedStorage_IsTrue`; `Wms.IntegrationTests/ForeignTrade/DepositQueriesTests.cs`: `ExportDetail_Closed_ReturnsDetail`, `ExportList_Closed_IsIncluded`, `ImportList_Cancelled_NotCountedInTotal`.
- **Criterios de aceptación:**
  - Dado un depósito de exportación cerrado, cuando CE abre su detalle desde la lista o desde el tablero, entonces responde 200 con estado «Cerrado» y el depósito aparece en la lista de exportaciones.
  - Dado 2026BA00011 anulado, cuando CE abre su tablero, entonces no cuenta en los contadores de importación y sí aparece en la columna «Anulado» del Kanban.
  - Dado el tablero de CE, cuando pulsa «Guías pendientes», entonces abre `/foreign-trade/dispatch-guides/pending`.
- **Re-test QA:** F4-CAR-009, F5-TAB-002, F5-TAB-003; REG F11-REG-016.
- **Riesgo de regresión:** bajo.
- **Tamaño:** S. **Dependencias:** CHG-40.

#### CHG-44 — La hora del pesaje propuesta es la hora actual

- **Cierra:** DEF-F3-003 (MAJOR).
- **Causa raíz:** `app/features/weighbridge/components/WeightCapture.vue:158-174` inicia y repone el selector de hora con `toColombiaPickerDate(minCapturedAt ?? new Date())`, es decir con la hora del ingreso o del pesaje anterior, y `:216` la envía con `toOperationalIso(picker, minCapturedAt)`, que devuelve el instante exacto del límite cuando coincide el minuto (por eso los dos pesajes quedaron a las 16:00:01); la ayuda de `:458` lo anuncia. El servidor ya usa la hora actual cuando no llega fecha (`RecordWeighingHandler.cs:82`). `RecordWeighingDialog.vue:130-138,184` repite la lógica y ninguna página lo usa.
- **Cambio exacto (aplica §10 · Hora del pesaje):**
  - Backend: ninguno.
  - Frontend: `WeightCapture.vue`: el selector arranca en la hora actual (`nowColombiaPickerDate()`) con un indicador `capturedAtEdited` en falso; se repone igual tras cada pesaje y al cambiar de camión (`:168-174`, `handleContinueWeighing` de `:252-257`); mientras no se edite, se actualiza cada 30 s (`useIntervalFn`); al editar, el indicador pasa a verdadero. El envío (`:216`) usa la función pura `resolveCapturedAt(valor, editado, mínimo)` (`app/features/weighbridge/utils/weighing-captured-at.ts`): sin edición envía `capturedAt: null` y el servidor estampa la hora actual; con edición envía la hora digitada. La ayuda (`:458`) dice «Por defecto: la hora actual. Puede corregirla dentro de la estadía del camión.». Se borra `RecordWeighingDialog.vue`.
  - No se toca: `RecordWeighingHandler.cs:82-85`, `OperationalDateRules.cs` ni `ModifyWeighingDateDialog.vue`.
- **Migración o script:** sin migración. `fase-07-horas-pesaje.sql` (solo detección): pesajes sin corrección de fecha cuya hora quedó más de 5 minutos antes de su registro; báscula los corrige desde «Modificar fecha» del historial.
- **Pruebas automatizadas nuevas:** `test/unit/weighbridge/weighing-captured-at.spec.ts`: sin edición → `null`; editado en el mismo minuto del mínimo (16:00 con mínimo `2026-10-02T16:00:21-05:00`) → ese instante; editado a las 16:27 → `2026-10-02T16:27:00-05:00`.
- **Criterios de aceptación:**
  - Dado QAA101 que ingresó a las 15:40, cuando báscula registra el primer pesaje a las 16:27 sin tocar la hora, entonces el tiquete muestra 16:27.
  - Dado el segundo pesaje a las 16:52 sin tocar la hora, cuando se registra, entonces queda a las 16:52, no a la hora del primero.
- **Re-test QA:** F3-PES-003, F3-TIQ-002; REG F11-REG-009, F11-REG-012.
- **Riesgo de regresión:** bajo.
- **Tamaño:** S. **Dependencias:** CHG-37.

#### CHG-45 — «Agregar otro depósito» se ofrece en el pesaje de un ingreso con depósito

- **Cierra:** DEF-F3-011 (MAJOR).
- **Causa raíz:** `WeightCapture.vue:372-379` muestra «Agregar otro depósito» solo con `serviceRecordMode === 'MultiDeposit'`, `index.vue:175-179` usa `"Standard"` por defecto y el backend solo informa `MultiDeposit` cuando ya hay más de un depósito (`GetWeighbridgeCycleHandler.cs:79-83`): el modo que habilita crear el segundo depósito solo existe después de crearlo. El resto del flujo existe y el backend lo admite con el ciclo en primer peso o en curso (`InitiateStorageWeighingHandler.cs`, rama de depósito adicional).
- **Cambio exacto:**
  - Backend: ninguno.
  - Frontend: `WeightCapture.vue` recibe la prop `canAddDeposit` (falsa por defecto) y la usa en `:373`; `index.vue` la calcula con la función pura `canOfferAddDeposit(tipoDeOperación)` (`app/features/weighbridge/utils/cycle-actions.ts`: verdadero solo para «storage») y la pasa en `:1605-1625` y `:1737-1755`. Las operaciones de un solo peso cierran en el primer pesaje y no ven la acción. Tras recargar, el registro principal lo arma `buildParentServiceRecord` de CHG-20.
  - No se toca: el modo `MultiDeposit` del backend (habilita el pesaje intermedio) ni `StorageServiceForm` en modo adicional.
- **Migración o script:** ninguno.
- **Pruebas automatizadas nuevas:** `test/unit/weighbridge/cycle-actions.spec.ts`: «storage» → verdadero; «weighing-only», «output» y `null` → falso; `test/unit/weighbridge/parent-service-record.spec.ts`: un registro de depósito IMP con primer peso Tara y ciclo `c1` arma el registro principal con `weighbridgeCycleId = "c1"`.
- **Criterios de aceptación:**
  - Dado QAB201 (importación) con el primer peso registrado, cuando báscula ve las acciones del pesaje, entonces aparece «Agregar otro depósito» y permite registrar el segundo depósito con su pesaje intermedio.
  - Dado un Solo báscula o una salida, cuando báscula pesa, entonces la acción no aparece.
- **Re-test QA:** F3-MUL-001, F3-MUL-002, F3-MUL-003, F3-MUL-004; REG F11-REG-009, F11-REG-011.
- **Riesgo de regresión:** bajo.
- **Tamaño:** S. **Dependencias:** CHG-20, CHG-44.

#### CHG-46 — Conductor y vehículo se guardan también en Solo báscula y en Salida

- **Cierra:** DEF-F3-008 (MAJOR).
- **Causa raíz:** `index.vue:582-585` exige la tarjeta «Camión y conductor» completa en los tres tipos de operación, pero solo el registro con depósito la envía (`:675-680`, `registerStorageEntry`); `handleWeighingOnlySubmit` (`:633-636`) y `handleOutputSubmit` (`:738-740`) envían solo los datos del servicio, y la tarjeta no llama al API (`CompleteEntryInfo.vue:243-257`). `InitiateWeighingOnlyRequest/Command` e `InitiateOutputWeighingRequest/Command` no tienen campos de conductor ni de vehículo.
- **Cambio exacto:**
  - Backend: `InitiateWeighingOnlyRequest.cs` e `InitiateOutputWeighingRequest.cs` suman, al final y con valor nulo por defecto, nombres, apellidos, número, tipo, país y teléfono del conductor, transportadora, país y tipo del vehículo; los comandos reciben `EntryLogInfoInput? EntryInfo`, que arman `WeighbridgeController.cs:88-95` y `:370-378`. `InitiateWeighingOnlyHandler` e `InitiateOutputWeighingHandler` llaman `EntryLogInfoUpdater.ApplyAsync(ingreso, EntryInfo)` antes de guardar (`InitiateWeighingOnlyHandler.cs:141`, `InitiateOutputWeighingHandler.cs:170`), dentro de la transacción y del bloqueo del ingreso de CHG-17: si el servicio falla no se guarda nada. Los errores son los del actualizador («Para crear un conductor nuevo se requieren: nombres, apellidos, número de documento y tipo de documento.») y los de `CarrierCompanyGuard` (CHG-05).
  - Frontend: `types/requests.ts:16-23` e `IInitiateOutputWeighingRequest` con los mismos campos, que pueden omitirse; `index.vue:633-636` y `:738-740` envían `{ ...data, ...(entryInfoRef.value?.getEntryInfo() ?? {}) }`.
  - No se toca: `UpdateEntryLogInfo*` (lo usa `app/pages/operations/entries/index.vue:234`) ni `RegisterStorageEntry*`.
- **Migración o script:** sin migración. `fase-07-conductores.sql` (solo detección): ingresos con servicio de Solo báscula o de salida no descartado sin conductor, o con vehículo sin transportadora, tipo o país; se completan con `PATCH weighbridge/entry-log/{id}/info` o al recrear la base.
- **Pruebas automatizadas nuevas:** `Wms.IntegrationTests/Weighbridge/EntryInfoOnRegisterTests.cs`: `InitiateWeighingOnly_WithDriverAndVehicle_StoresThem`, `InitiateOutput_WithDriverAndVehicle_StoresThem`, `InitiateWeighingOnly_TariffMissing_StoresNothing`.
- **Criterios de aceptación:**
  - Dado QAC405 (Solo báscula) con conductor nuevo, transportadora y tipo de vehículo digitados, cuando báscula guarda, entonces el ingreso queda con ese conductor y el vehículo con transportadora, tipo y país.
  - Dado una salida con la orden 2026OC00020, cuando báscula guarda con los datos del camión, entonces quedan guardados en el ingreso.
  - Dado un Solo báscula sin tarifa configurada, cuando báscula guarda, entonces responde el error de tarifa y el conductor no se guarda.
- **Re-test QA:** F3-CAM-010, F3-CAM-011; REG F11-REG-013.
- **Riesgo de regresión:** bajo.
- **Tamaño:** M. **Dependencias:** CHG-17, CHG-05, CHG-32.

#### CHG-47 — Historial de báscula: corrección de pesos por rol y sin acciones muertas

- **Cierra:** DEF-F3-013 (MAJOR).
- **Decisión:** D-2 resuelta el 3-oct-2026 (§5): báscula no cambia el modo de pago de una operación cobrada; la acción se retira.
- **Causa raíz:**
  - «Editar peso»: `app/pages/operations/weighbridge/history.vue:200-210` compara nombres visibles de rol («administrador», «supervisor», «scale») y el rol Scale se llama «Operario báscula»; el backend está bien (`WeighingCorrectionAccess` = Admin, Scale, Billing, `WmsAuthentication.cs:95-97`, en `WeighbridgeCorrectionController.cs:24,36,62`). Facturación no tiene acceso al historial (matriz de la fase 9 de QA) y en el detalle del ciclo (`cycles/[id].vue:394`) la corrección solo aparece en ciclos abiertos.
  - «Cambiar modo de pago»: `weighbridge-service.ts:223` llama `PATCH weighbridge/{id}/payment-mode`, que no existe (el comando se borró en `a088674` y `WeighbridgeCycle.ChangePaymentMode` en `3ea20db`); en pantalla la acción nunca aparece porque `history.vue:572` exige `invoiceId === null` y el API no envía `invoiceId`.
- **Cambio exacto (decisión D-2):**
  - Backend: se borra `WeighbridgeCyclePaymentModeChangedDto.cs` (huérfano).
  - Frontend: `app/utils/weighing-permissions.ts` con `canCorrectWeighings(roles)` (Admin, Scale, Billing) y `canModifyWeighingDate(roles)` (Admin, Scale); `history.vue` los usa para los botones de peso (`:674`, `:306-312`) y de fecha (`:654`, `:319`) y elimina `normalizeRoleName` (`:200-205`) y el uso de `userStore` (`:30,48`); `cycles/[id].vue` muestra a Facturación, en ciclos completos, las mismas acciones de corrección de peso del historial. Se retira la acción muerta: `history.vue:15,27,259-275,566-579,905-912`, `weighbridge-service.ts:210-226,767-768`, `useChangeWeighbridgeCyclePaymentMode.ts`, `types/requests.ts:384-390` y `weighbridge-cycle.ts:34` y `:427-431`.
  - Documentación de QA: `docs/qa/fase-03-bascula.md`, F3-HIS-008, pasa a esperar que el historial no ofrezca «Cambiar modo de pago»; un cobro «por facturar» se paga en Facturación → Pagos.
  - No se toca: `WeighbridgeCorrectionController.cs`, `ChangePaymentModeDialog.vue` (lo usan montacargas y guías) ni la anulación (`history.vue:149`).
- **Migración o script:** ninguno.
- **Pruebas automatizadas nuevas:** `test/unit/utils/weighing-permissions.spec.ts`: `canCorrectWeighings` verdadero para Scale, Billing y Admin, falso para Warehouse; `canModifyWeighingDate` falso para Billing.
- **Criterios de aceptación:**
  - Dado `bascula`, cuando abre el detalle de un ciclo completo en el historial, entonces ve «Editar» en peso y en fecha.
  - Dado `facturacion`, cuando abre el detalle de un ciclo completo desde su factura (`/operations/weighbridge/cycles/{id}`), entonces ve «Editar» en peso y no en fecha.
  - Dado el historial, cuando se revisa cualquier ciclo, entonces no aparece «Cambiar modo de pago» ni se llama a un endpoint inexistente.
- **Re-test QA:** F3-HIS-008 (con el resultado esperado actualizado), F3-COR-002; REG F11-REG-028.
- **Riesgo de regresión:** bajo.
- **Tamaño:** S. **Dependencias:** CHG-03.

### Fase 8 — MINOR de validación y reglas en el servidor

- **Objetivo:** que el API aplique las reglas que la pantalla ya aplica y responda con mensajes de negocio: cuerpos inválidos, duplicados, administración de usuarios, enumeración de cuentas, fechas de portería, contrato del cobro de báscula (§10 · Efectivo y cambio fuera de la UI y del API), documentos cerrados, fotos, diferencias de recepción, novedades y montacargas. Cierra DEF-F9-006, DEF-F6-019, DEF-F1-007, DEF-F1-006, DEF-F1-010, DEF-F1-011, DEF-F2-003, DEF-F3-009, DEF-F3-019, DEF-F3-010, DEF-F4-009, DEF-F4-010, DEF-F4-011, DEF-F4-013, DEF-F4-016 y DEF-F4-017.
- **Criterio de entrada:** checkpoint de la Fase 7 aprobado.
- **Cambios:** CHG-48, CHG-49, CHG-50, CHG-51, CHG-52, CHG-53, CHG-54, CHG-55, CHG-56, CHG-57, CHG-58, CHG-59.
- **Orden interno:** CHG-48 → CHG-49 (ambos en `GlobalExceptionHandler.cs` y `UniqueViolationMessages`) → CHG-50 → CHG-51 → CHG-52 → CHG-53 → CHG-54 → CHG-55 → CHG-56 (ambos en los handlers de recepción) → CHG-57 → CHG-58 → CHG-59.
- **Migración de la fase:** ninguna.
- **Riesgos y mitigación:**
  - Los validadores nuevos rechazan peticiones que hoy pasan (registro sin transportadora, destinatario de dos letras, más de 5 fotos, horómetro 0). Mitigación: la pantalla ya exige lo mismo y no hay integraciones externas con el API.
  - El filtro del cuerpo inválido convierte en 400 los 500 de todos los endpoints. Mitigación: pruebas de las reglas y el sondeo de la fase 9 de QA.
  - `infra/main.tf` pasa a Production en el repositorio. Mitigación: no se aplica a Azure sin la aprobación del usuario.
- **Saneamiento de datos:** `fase-08-productos-duplicados.sql`, `fase-08-usuarios.sql`, `fase-08-fechas-ingreso.sql`, `fase-08-contrato-bascula.sql`, `fase-08-fotos.sql`, `fase-08-novedades.sql`, `fase-08-montacargas.sql` y `fase-08-patch.sql`, descritos en cada cambio.
- **Criterio de salida:** compuertas comunes (regla 4.0.4) y en PASA: F6-PAG-006, sondeo F9-API-*, F1-TER-008, F1-PRO-005, F9-INP-004, F1-USR-006, F1-USR-010, F1-USR-012, F1-USR-017, F1-AUT-005, F1-AUT-015, F2-ING-012, F2-SAL-009, F3-MCA-008, F4-REC-009, F4-REC-012, F4-NOV-006, F4-MON-004, F4-MON-006, F4-MON-012, F4-MON-014, F7-AUD-004; REG F11-REG-001, F11-REG-003, F11-REG-004, F11-REG-005, F11-REG-007, F11-REG-008, F11-REG-011, F11-REG-014, F11-REG-015, F11-REG-016, F11-REG-023, F11-REG-026.
- **Checkpoint:** se entrega al usuario el sondeo de cuerpos inválidos con 0 respuestas 500, la lista de productos renombrados y el resultado de las pruebas. El usuario aprueba el saneamiento en staging y decide si aplica `infra/main.tf` a Azure.

#### CHG-48 — Un cuerpo inválido responde 400 con el campo y los errores de base de datos no exponen texto interno

- **Cierra:** DEF-F9-006 (MINOR), DEF-F6-019 (MINOR).
- **Causa raíz:** `Wms.Api/Program.cs:51-53` fija `SuppressModelStateInvalidFilter = true` y no hay filtro sustituto. Un JSON mal formado, un enum desconocido («Transfer» con `JsonStringEnumConverter`, `Program.cs:49`) o un tipo inválido (`amount: "abc"`) hacen fallar el formateador: el parámetro del cuerpo llega `null`, la acción se ejecuta y termina en 500 (`mediator.Send(null)` en `ProductController.cs:24-26`; `request.Amount` en `BillingController.cs:334`), antes de que corran los validadores (`RecordPaymentValidator` con `IsInEnum`). `Wms.Api/Common/Exception/GlobalExceptionHandler.cs:16-18` devuelve el tipo y el mensaje interno en Development, y `:103-111` devuelve en `description` el texto de PostgreSQL (restricción y valores) en todos los ambientes. `infra/main.tf:102` declara `ASPNETCORE_ENVIRONMENT = "Development"` para Azure.
- **Cambio exacto:**
  - Backend:
    - Nuevo `Wms.Api/Common/Filters/InvalidRequestBodyFilter.cs` (`IActionFilter` global, `AddControllers(o => o.Filters.Add<InvalidRequestBodyFilter>())` en `Program.cs`): si `ModelState` trae un error con excepción del formateador, o si un parámetro `[FromBody]` llegó `null`, lanza `BadRequestException` con el texto de la clase pura `Wms.Common/Http/RequestBodyErrorMessages.cs`: campo inválido «El valor del campo '{campo}' no es válido.» (la ruta `$.items[0].quantity` se muestra como `items[0].quantity`); `paymentMethod` «El método de pago no es válido.»; `billingCycle` «El ciclo de facturación no es válido.»; `invoicingPreference` «La preferencia de facturación no es válida.»; JSON mal formado (ruta `$`) «El cuerpo de la solicitud no es un JSON válido.»; sin cuerpo «El cuerpo de la solicitud es requerido.». Se exceptúa el parámetro declarado anulable cuando la petición no trae cuerpo (`AbandonmentController.cs:38`, `ForeignTradeController.cs:658`, `LegacyImportController.cs:102`). Los demás errores de `ModelState` (ruta y query) quedan como hoy.
    - `GlobalExceptionHandler.cs:103-111`, en todos los ambientes: `23505` de una restricción del mapa `UniqueViolationMessages` (CHG-17) responde 409 con su mensaje; `23505` de otra restricción, 409 «Ya existe un registro con esos datos.»; `23503`, 409 «El registro está relacionado con otros datos y no se puede modificar ni eliminar.». Cualquier otra `DbUpdateException` responde 409 «No se pudo guardar el cambio. Verifique los datos e intente de nuevo.» fuera de Development y con el mensaje técnico en Development. Los textos genéricos viven en la clase pura `Wms.Common/Http/DatabaseErrorMessages.For(sqlState)`; el detalle técnico sigue en el log.
    - `infra/main.tf:102` → `"Production"` (igual que `deploy/staging/compose.staging.yaml:33`). El cambio queda en el repositorio; aplicarlo a Azure requiere la aprobación del usuario.
  - Frontend: ninguno (el aviso global muestra la `description`).
  - No se toca: `Program.cs:53` (reactivar el filtro automático cambiaría los mensajes de FluentValidation de todos los DTO).
- **Migración o script:** ninguno.
- **Pruebas automatizadas nuevas:** `Wms.Tests/Common/RequestBodyErrorMessagesTests.cs`: `Describe_PaymentMethodPath_ReturnsKnownMessage`, `Describe_AmountPath_ReturnsGenericMessage` («El valor del campo 'amount' no es válido.»), `Describe_NestedPath_StripsDollarPrefix`, `Describe_RootPath_ReturnsJsonMessage`, `Describe_NullBody_ReturnsRequiredMessage`, `Describe_NullableParameterWithoutBody_IsAccepted`; `Wms.Tests/Common/DatabaseErrorMessagesTests.cs`: `For_23505_ReturnsDuplicateMessage`, `For_23503_ReturnsRelatedDataMessage`, `For_Null_ReturnsGenericMessage`; `Wms.IntegrationTests/Api/InvalidBodyTests.cs`: `PostProduct_MalformedJson_Returns400`, `PostPayment_PaymentMethodTransfer_Returns400WithMessage`, `PostPayment_AmountAsText_Returns400`.
- **Criterios de aceptación:**
  - Dado el Admin, cuando envía `POST product` con el cuerpo `{"__qa":`, entonces responde 400 «El cuerpo de la solicitud no es un JSON válido.» sin nombres de clases.
  - Dado Facturación, cuando registra un pago con `paymentMethod: "Transfer"`, entonces responde 400 «El método de pago no es válido.» y no se crea el pago.
  - Dado un ambiente distinto de Development, cuando una escritura viola una restricción `23505` que no está en el mapa, entonces responde 409 «Ya existe un registro con esos datos.» sin el texto de PostgreSQL.
- **Re-test QA:** sondeo F9-API-* (las escrituras con el cuerpo `{"__qa":` como Admin dan 0 respuestas 500; hoy son 139), F6-PAG-006; REG F11-REG-003, F11-REG-023.
- **Riesgo de regresión:** bajo; el filtro solo actúa cuando el cuerpo no se pudo leer.
- **Tamaño:** S. **Dependencias:** CHG-17.

#### CHG-49 — Unicidad de NIT, SKU y nombre de producto con mensajes de negocio

- **Cierra:** DEF-F1-007 (MINOR).
- **Causa raíz:** `UpdateStakeholderHandler.cs:24-32` y `UpdateProductHandler.cs:29-37` no validan duplicados antes de guardar; la base rechaza por `idx_stakeholder_identification` (`StakeholderConfiguration.cs:26`) e `idx_product_sku` (`ProductConfiguration.cs:32`) y `GlobalExceptionHandler.cs:103-111` devuelve el texto de PostgreSQL. El nombre de producto solo se valida en el alta (`CreateProductHandler.cs:17`, igualdad exacta) y no tiene índice, así que la edición lo duplica. `Stakeholder.cs:64` interpreta el tipo de identificación con `Enum.TryParse` sensible a mayúsculas mientras el validador lo acepta en minúsculas (`UpdateStakeholderValidator.cs:19`): «nit» se ignora en silencio.
- **Cambio exacto:**
  - Backend:
    - Clase pura `Wms.Application/Stakeholders/Common/StakeholderIdentityRules.cs`: `Resolve(tipoActual, númeroActual, tipoPedido, númeroPedido)` (tipo sin distinguir mayúsculas, número recortado, en blanco = sin cambio) y `DuplicateMessage(número)` = «Ya existe un tercero con número de identificación {número}.». `UpdateStakeholderHandler` consulta duplicados (otro tercero con el mismo tipo y número) solo si la identificación cambia y lanza `ConflictException` con ese mensaje; `CreateStakeholderHandler.cs:20` usa el mismo mensaje; `Stakeholder.cs:64` usa `ignoreCase: true`.
    - Clase pura `Wms.Application/Products/Common/ProductUniquenessRules.cs`: clave de nombre = `CatalogNameNormalizer.ForComparison(nombre)`; `Conflict(candidatos, sku, claveNombre)` devuelve «Ya existe un producto con el SKU '{sku}'.» o «Ya existe un producto con el nombre '{nombre}'.» o `null`. `CreateProductHandler.cs:17-18` y `UpdateProductHandler` consultan candidatos (`p.Id != id && (p.Sku == sku || unaccent(upper(p.Name)) == unaccent(upper(clave)))`, el patrón de `WeighbridgeProductResolver.FindByKeyAsync`) y lanzan `ConflictException`; la edición solo valida lo que cambia; se guarda el nombre con espacios colapsados y el SKU recortado.
    - `UniqueViolationMessages` (CHG-17) agrega `idx_stakeholder_identification` → «Ya existe un tercero con ese tipo y número de identificación.», `idx_product_sku` → «Ya existe un producto con ese SKU.» e `idx_vehicle_plate` → «Ya existe un vehículo con esa placa.» (respaldo ante carreras).
  - Frontend: ninguno (`useStakeholderUpdate.ts` y `useProductUpdate.ts` muestran la descripción).
  - No se toca: los índices existentes, `QuickCreateStakeholderHandler.cs` ni `QuickCreateTransportCompanyHandler.cs`.
- **Migración o script:** sin migración. `fase-08-productos-duplicados.sql`: detección de productos con la misma clave de nombre (`upper(unaccent(regexp_replace(trim(name),'\s+',' ','g')))` con `count(*) > 1`); corrección: el más antiguo conserva el nombre y los demás se renombran a «{nombre} ({sku})».
- **Pruebas automatizadas nuevas:** `Wms.Tests/Administration/StakeholderIdentityRulesTests.cs`: `Resolve_LowercaseType_ParsesIgnoringCase`, `Resolve_SameValues_IsNotChanged`, `Resolve_NewNumber_IsChanged`, `DuplicateMessage_UsesTerceroWording` («Ya existe un tercero con número de identificación 900123456.»); `Wms.Tests/Administration/ProductUniquenessRulesTests.cs`: `Conflict_SameSku_ReturnsSkuMessage` («QA-REP»), `Conflict_SameNameDifferentCaseAndAccent_ReturnsNameMessage` («qa cebolla» frente a «QA Cebolla»), `Conflict_NoMatch_ReturnsNull`; en `UniqueViolationMessagesTests`: `TryGetMessage_ProductSku_ReturnsSkuMessage`; `Wms.IntegrationTests/Administration/UniquenessTests.cs`: `UpdateStakeholder_DuplicateNit_Returns409WithMessage`, `UpdateProduct_DuplicateName_Returns409WithMessage`.
- **Criterios de aceptación:**
  - Dado el tercero A y el tercero B con NIT 900123456, cuando el Admin edita A con NIT 900123456, entonces responde 409 «Ya existe un tercero con número de identificación 900123456.».
  - Dado el producto «QA Cebolla», cuando el Admin renombra otro producto a «qa cebolla», entonces responde 409 «Ya existe un producto con el nombre 'qa cebolla'.».
  - Dado un producto con SKU QA-REP, cuando el Admin asigna QA-REP a otro producto, entonces responde 409 «Ya existe un producto con el SKU 'QA-REP'.».
- **Re-test QA:** F1-TER-008, F1-PRO-005, F9-INP-004; REG F11-REG-003.
- **Riesgo de regresión:** bajo.
- **Tamaño:** M. **Dependencias:** CHG-41, CHG-48.

#### CHG-50 — Reglas de administración de usuarios: contraseñas coincidentes, un rol mínimo y un Admin activo

- **Cierra:** DEF-F1-006 (MINOR), DEF-F1-010 (MINOR).
- **Causa raíz:**
  - DEF-F1-006: `app/features/users/components/UserForm.vue:178-189` define la coincidencia con `.refine` sobre `schemaSecurityBase` y `:191` lo combina con `schemaProfileBase.extend(schemaSecurityBase.shape)`: `.shape` solo copia los campos y pierde la validación de objeto.
  - DEF-F1-010: `UserController.cs:112-123` (`remove-roles`) y `:138-149` (`manage-active`) no envían el usuario que actúa; `RemoveRolesToUserHandler.cs:38-48` solo rechaza una lista vacía y `ManageUserActivationHandler.cs:44-56` desactiva sin condiciones.
- **Cambio exacto:**
  - Backend: clase pura `Wms.Application/Users/Common/UserAdministrationRules.cs`: `EnsureCanDeactivate(actor, objetivo)` → «No puede desactivar su propio usuario.»; `EnsureCanRemoveRoles(actor, objetivo, rolesActuales, rolesAQuitar)` → «El usuario debe conservar al menos un rol.» y «No puede quitarse a sí mismo el rol de Administrador.»; `EnsureAdminRemains(adminsActivosDespués)` → «Debe quedar al menos un administrador activo.». `ManageUserActivationCommand` y `RemoveRolesToUserCommand` reciben `ActingUserId` desde `User.GetRequiredUserId()`; los handlers cuentan administradores activos con `UserRoles` unido a `Users` (`IsActive`) y el rol de código Admin, y aplican las reglas antes de modificar (400).
  - Frontend: el esquema del alta pasa a `app/features/users/schemas/user-create-schema.ts`: `schemaProfileBase.extend({ password, confirmPassword, rolIds }).refine(contraseñas iguales, { message: "Las contraseñas no coinciden", path: ["confirmPassword"] })`; `UserForm.vue` lo importa y se elimina `schemaSecurityBase`.
  - No se toca: `resolverEdit` (`UserForm.vue:194`) ni el alta de usuarios en el backend (ya exige un rol).
- **Migración o script:** sin migración. `fase-08-usuarios.sql` (solo detección): usuarios sin rol y número de administradores activos; los usuarios sin rol se corrigen desde «Usuarios» asignando un rol.
- **Pruebas automatizadas nuevas:** `Wms.Tests/Users/UserAdministrationRulesTests.cs`: `EnsureCanDeactivate_SameUser_Throws`, `EnsureCanDeactivate_OtherUser_Passes`, `EnsureCanRemoveRoles_AllRoles_ThrowsMustKeepOneRole`, `EnsureCanRemoveRoles_OwnAdminRole_Throws`, `EnsureCanRemoveRoles_OtherUsersAdminRole_Passes`, `EnsureAdminRemains_ZeroAdmins_Throws`, `EnsureAdminRemains_OneAdmin_Passes`; `test/unit/users/user-create-schema.spec.ts`: contraseñas distintas → error «Las contraseñas no coinciden» en `confirmPassword`; iguales → válido.
- **Criterios de aceptación:**
  - Dado el alta de usuario con dos contraseñas distintas que cumplen la política, cuando el Admin intenta crear, entonces «Crear Usuario» queda deshabilitado y «Repetir Contraseña» muestra «Las contraseñas no coinciden».
  - Dado el Admin conectado, cuando intenta desactivarse, entonces responde 400 «No puede desactivar su propio usuario.».
  - Dado un usuario con un solo rol, cuando el Admin le quita ese rol, entonces responde 400 «El usuario debe conservar al menos un rol.».
- **Re-test QA:** F1-USR-006, F1-USR-010, F1-USR-012, F1-USR-017; REG F11-REG-001.
- **Riesgo de regresión:** bajo.
- **Tamaño:** S. **Dependencias:** CHG-08 (`GetRequiredUserId`), CHG-16.

#### CHG-51 — Login y recuperación no revelan qué cuentas existen

- **Cierra:** DEF-F1-011 (MINOR).
- **Causa raíz:** `Wms.Application/Auth/Commands/Login/LoginHandler.cs:30-33` responde «Usuario inactivo» antes de verificar la contraseña (`:35-39`) y un usuario inexistente responde sin calcular el hash (`:24-28`), lo que revela la cuenta por mensaje y por tiempo. `RequestPasswordResetHandler.cs:56-59` responde 401 «Solo los administradores…» para cuentas existentes no administradoras, mientras las inexistentes e inactivas responden 204 (`:27-37`); `:46-49` y `:62-65` también se distinguen.
- **Cambio exacto:**
  - Backend: clase pura `Wms.Application/Auth/Common/LoginCredentialRules.Classify(existe, contraseñaVálida, activo)`: `InvalidCredentials` si no existe o la contraseña es incorrecta (activo o inactivo); `InactiveAccount` solo con contraseña correcta e inactivo. `LoginHandler.cs:24-39` verifica siempre la contraseña (con un hash ficticio estático si el usuario no existe) y responde «Credenciales inválidas» o «Usuario inactivo. Comuníquese con el administrador.». Clase pura `PasswordResetEligibility.CanSend(existe, activo, esAdmin, tieneCorreo)`: `RequestPasswordResetHandler.cs:34-65` responde 204 en todos los casos y solo envía el correo cuando es verdadero (el motivo se registra en el log como advertencia).
  - Frontend: ninguno (`app/pages/auth/request-password-reset.vue:35,61` ya muestra un texto genérico).
  - No se toca: `ResetPasswordWithTokenHandler`.
- **Migración o script:** ninguno.
- **Pruebas automatizadas nuevas:** `Wms.Tests/Auth/LoginCredentialRulesTests.cs`: `Classify_UserDoesNotExist_ReturnsInvalidCredentials`, `Classify_WrongPasswordActiveUser_ReturnsInvalidCredentials`, `Classify_WrongPasswordInactiveUser_ReturnsInvalidCredentials`, `Classify_RightPasswordInactiveUser_ReturnsInactiveAccount`, `Classify_RightPasswordActiveUser_ReturnsSuccess`; `Wms.Tests/Auth/PasswordResetEligibilityTests.cs`: `CanSend_NonAdmin_ReturnsFalse`, `CanSend_UnknownUser_ReturnsFalse`, `CanSend_InactiveAdmin_ReturnsFalse`, `CanSend_AdminWithoutEmail_ReturnsFalse`, `CanSend_ActiveAdminWithEmail_ReturnsTrue`; `Wms.IntegrationTests/Auth/AccountEnumerationTests.cs`: `RequestPasswordReset_NonAdminAndUnknown_BothReturn204`.
- **Criterios de aceptación:**
  - Dado un usuario inactivo, cuando inicia sesión con una contraseña incorrecta, entonces ve «Credenciales inválidas», igual que un usuario inexistente.
  - Dado un usuario inactivo, cuando inicia sesión con su contraseña correcta, entonces ve «Usuario inactivo. Comuníquese con el administrador.».
  - Dado un usuario de Bodega y un correo inexistente, cuando se pide la recuperación de contraseña para cada uno, entonces ambos responden 204 y la pantalla muestra el mismo texto.
- **Re-test QA:** F1-AUT-005, F1-AUT-015; REG F11-REG-001.
- **Riesgo de regresión:** bajo.
- **Tamaño:** S. **Dependencias:** ninguna.

#### CHG-52 — Ingreso sin fecha futura y salida no anterior al ingreso

- **Cierra:** DEF-F2-003 (MINOR).
- **Causa raíz:** `EntryLog.cs:55` asigna `DateTimeEntry = parameters.DateTimeEntry ?? UtcNow` sin validar (`CreateEntryLogHandler.cs:103-111`), y `EntryLog.RegisterDeparture` (`EntryLog.cs:83-88`), usado por `RegisterDepartureHandler.cs:52` y `UpdateDepartureAuthorizationHandler.cs:83-84`, asigna la salida sin compararla con el ingreso ni con la hora actual. Las reglas de `OperationalDateRules.cs:18-22` solo se aplican en la corrección (`EntryLog.cs:129-147`).
- **Cambio exacto:**
  - Backend: `OperationalDateRules.EnsureDeparture(salida, ingreso)`: no futura («La fecha de salida no puede ser futura.») y no anterior al minuto del ingreso («La fecha de salida no puede ser anterior al ingreso del camión ({dd/MM/yyyy HH:mm}).»). `EntryLog.RegisterEntry` aplica `EnsureNotFuture(fecha, "La fecha de ingreso")` cuando la fecha viene (tolerancia actual de 2 minutos); `EntryLog.RegisterDeparture` aplica `EnsureDeparture` cuando la fecha viene y, sin fecha, usa el mayor entre la hora actual y el ingreso.
  - Frontend: ninguno (la interfaz no envía fechas).
  - No se toca: `CreateEntryLogHandler.cs` ni `RegisterDepartureHandler.cs` (basta el dominio).
- **Migración o script:** sin migración. `fase-08-fechas-ingreso.sql` (solo detección): ingresos con fecha mayor que ahora + 2 minutos y salidas anteriores al minuto del ingreso (p. ej. QAC320); se corrigen con «Corregir ingreso» (`PUT entry-logs/{id}/correction`), que deja el motivo auditado.
- **Pruebas automatizadas nuevas:** en `Wms.Tests/Common/OperationalDateRulesTests.cs`: `EnsureDeparture_BeforeEntry_ThrowsBadRequest` (ingreso 2026-09-12T13:00Z, salida un minuto antes → «La fecha de salida no puede ser anterior al ingreso del camión (12/09/2026 08:00).»), `EnsureDeparture_Future_ThrowsBadRequest`, `EnsureDeparture_SameMinuteAsEntryWithSeconds_DoesNotThrow`; nueva `Wms.Tests/Domain/Logistics/EntryLogRegistrationTests.cs`: `RegisterEntry_FutureDate_ThrowsBadRequest` (+3 días → «La fecha de ingreso no puede ser futura.»), `RegisterEntry_WithinTolerance_Registers` (+1 minuto), `RegisterDeparture_BeforeEntry_ThrowsBadRequest`, `RegisterDeparture_WithoutDate_UsesNowAndNeverBeforeEntry`.
- **Criterios de aceptación:**
  - Dado Vigilancia, cuando el API recibe un ingreso con fecha de dentro de tres días, entonces responde 400 «La fecha de ingreso no puede ser futura.».
  - Dado un ingreso del 12/09/2026 08:00, cuando el API recibe la salida del 12/09/2026 07:59, entonces responde 400 «La fecha de salida no puede ser anterior al ingreso del camión (12/09/2026 08:00).».
- **Re-test QA:** F2-ING-012, F2-SAL-009; REG F11-REG-005.
- **Riesgo de regresión:** bajo.
- **Tamaño:** S. **Dependencias:** CHG-30.

#### CHG-53 — El API de registro y cobro aplica las reglas de la pantalla y ya no recibe efectivo ni cambio

- **Cierra:** DEF-F3-009 (MINOR), DEF-F3-019 (MINOR).
- **Causa raíz:**
  - DEF-F3-009: `RegisterStorageEntryValidator.cs:13-45` no exige transportadora, país y tipo de vehículo ni los datos del conductor, que la pantalla sí exige (`app/features/weighbridge/components/CompleteEntryInfo.vue:83-95`); `InitiateStorageWeighingValidator.cs:114-122` solo valida valor > 0 y moneda COP o USD (la columna `numeric(18,2)` redondeó 1500.555 sin aviso); los seis validadores de cobro (`ProcessStoragePaymentValidator.cs:42-54`, `ProcessWeighingOnlyPaymentValidator.cs:37-49`, `ProcessOutputPaymentValidator.cs:40-52`, `StartStoragePendingBillingValidator.cs:26-38`, `StartWeighingOnlyPendingBillingValidator.cs:26-38`, `StartOutputPendingBillingValidator.cs:26-38`) y `UpdateInvoiceRecipientValidator.cs:17-29` solo exigen que la persona no registrada no esté vacía (la pantalla, `BillingCollectForm.vue:313-327`, exige nombre de 3 a 255, tipo, número de 4 a 50 alfanumérico y teléfono válido).
  - DEF-F3-019: `CashReceived` sigue en los requests (`ProcessStoragePaymentRequest.cs:20`, `ProcessWeighingOnlyPaymentRequest.cs:23`, `ProcessOutputPaymentRequest.cs:23`), en los comandos, en `WeighbridgeController.cs:127,312,410`, en los validadores (`ProcessStoragePaymentValidator.cs:32-40` y sus pares), en los handlers (`ProcessStoragePaymentHandler.cs:167-176,216-219,271-272` y sus pares) con `CashChangeCalculator.cs:10-33`, en `InvoicePayment.RegisterCash` (`InvoicePayment.cs:91-104`) y en las lecturas (`WeighbridgeHistoryDto.cs:46-47`, `WeighbridgeCycleDetailDto.cs:148-150`, `InvoiceDto.cs:164-166`).
- **Cambio exacto (aplica §10 · Efectivo y cambio fuera de la UI y del API, y §10 · Datos de CE no obligatorios en báscula):**
  - Backend:
    - `RegisterStorageEntryValidator`: transportadora obligatoria y válida («La transportadora es obligatoria.», «El Id de la empresa de transporte no es válido.»), país («El país del vehículo es obligatorio.»), tipo de vehículo («El tipo de vehículo es obligatorio.»), tipo y número de documento del conductor, apellidos y nombres («Los apellidos del conductor son obligatorios.», «Los nombres del conductor son obligatorios.»). `InitiateStorageWeighingValidator.cs:114-122`: valor > 0 («El valor de la mercancía debe ser mayor que cero.»), máximo 2 decimales («El valor acepta máximo 2 decimales.») y, con valor, moneda obligatoria («La moneda es obligatoria cuando se informa el valor de la mercancía.»). El valor y los demás datos de CE siguen sin ser obligatorios.
    - Nuevo `Wms.Application/Billing/Common/Validators/UnregisteredRecipientDtoValidator.cs`: nombre de 3 a 255 caracteres, tipo de identificación de la lista (Nit, Rut, Cc, Pasaporte, Ruc), número de 4 a 50 alfanumérico y teléfono con la expresión de la pantalla; se aplica con `SetValidator` en los seis validadores de cobro y en `UpdateInvoiceRecipientValidator`.
    - Se retira `CashReceived` de los 3 requests, los 3 comandos, el controlador, los 3 validadores y los 3 handlers; `ProcessPaymentResponseDto` (`:11-14`) pierde `ChangeAmount` y `CashReceived`; se borran `CashChangeCalculator.cs`, `Wms.Tests/Weighbridge/CashChangeCalculatorTests.cs` e `InvoicePayment.RegisterCash`; las lecturas (`WeighbridgeHistoryDto`, `WeighbridgeCycleDetailDto`, `InvoiceDto`) y sus mapeos (`GetWeighbridgeHistoryHandler.cs:104-128`, `GetWeighbridgeCycleHandler.cs:195-196`, `GetOpenCycleByPlateHandler.cs:204-205`, `GetInvoiceByWeighbridgeCycleHandler.cs:81-82`, `GetInvoiceByIdHandler.cs:161-162`, `GetInvoicePaymentsHandler.cs:44-45`, `RecordPaymentHandler.cs:86-87`) dejan de exponer efectivo y cambio. Las columnas `invoice_payments.cash_received` y `change_given` se conservan con su historia y ya no se escriben (sin migración).
  - Frontend: `app/features/weighbridge/types/weighbridge-cycle.ts:121-123,213-214,346-349` sin `cashReceived`, `changeGiven` ni `changeAmount`; `app/pages/operations/weighbridge/index.vue` (`describePayment`, `:506-512`, `:551`, `:1055-1058`) sin «Cambio»; `recover.vue:160` sin `changeAmount`; `WeighbridgeHistoryTable.vue:449-455` sin las columnas «Efectivo» y «Cambio»; `history.vue:101-102` y `:840-843` sin efectivo ni cambio en el Excel y en el detalle.
  - No se toca: `InvoicePayment.Create`, `MarkAsReceived` ni `EntryLogInfoUpdater`.
- **Migración o script:** sin migración. `fase-08-contrato-bascula.sql` (solo detección): facturas con destinatario no registrado de menos de 3 caracteres (la factura «QA») y depósitos con valor sin moneda (2026BA00002/3/4); son datos de QA y se corrigen desde la pantalla o al recrear la base.
- **Pruebas automatizadas nuevas:** en `RegisterStorageEntryValidatorTests` (el ayudante `Command()` pasa a enviar una transportadora): `CarrierCompanyId_Missing_RequiresIt`, `VehicleType_Missing_RequiresIt`, `DriverLastName_Missing_RequiresIt`; en `InitiateStorageWeighingValidatorTests`: `CargoValue_ThreeDecimals_IsRejected` (1500.555), `CargoValue_TwoDecimals_IsValid`, `CargoValue_WithoutCurrency_RequiresCurrency`, `CargoValue_WithCurrency_HasNoCurrencyError`; `Wms.Tests/Billing/UnregisteredRecipientDtoValidatorTests.cs`: `Name_TwoCharacters_IsRejected` («QA» → «El nombre debe tener al menos 3 caracteres.»), `Name_ThreeCharacters_IsValid`, `IdNumber_ThreeCharacters_IsRejected`, `IdNumber_WithSymbols_IsRejected`, `Phone_Invalid_IsRejected`, y un caso por cada comando de cobro; `Wms.Tests/Weighbridge/PaymentContractsTests.cs`: `PaymentCommandsAndRequests_DoNotExposeCashReceived`, `ProcessPaymentResponse_DoesNotExposeChangeFields`.
- **Criterios de aceptación:**
  - Dado báscula, cuando el API recibe un registro sin transportadora, entonces responde 400 «La transportadora es obligatoria.».
  - Dado un valor de mercancía 1500.555, cuando se registra, entonces responde 400 «El valor acepta máximo 2 decimales.».
  - Dado un cobro a persona no registrada con nombre «QA», cuando se envía, entonces responde 400 «El nombre debe tener al menos 3 caracteres.».
  - Dado un cobro en efectivo con `cashReceived: 50000`, cuando se procesa, entonces el campo se ignora, la respuesta no trae `changeAmount` y el historial no muestra «Efectivo» ni «Cambio».
- **Re-test QA:** F3-REG-014, F3-COB-005, F3-COB-012; REG F11-REG-007, F11-REG-008.
- **Riesgo de regresión:** bajo.
- **Tamaño:** M. **Dependencias:** CHG-17, CHG-28.

#### CHG-54 — Un documento con el ingreso de camiones cerrado se muestra cerrado desde la búsqueda

- **Cierra:** DEF-F3-010 (MINOR).
- **Causa raíz:** `GetServiceRecordByDocumentHandler.cs:34-40` usa `documentLookup.MatchOpenAsync`, que solo ve depósitos abiertos (`StorageDocumentLookup.cs:33`, `TruckEntriesClosedAt == null`): con el ingreso cerrado responde `null` y la pantalla lo trata como «Documento nuevo». El rechazo solo llega al guardar (`StorageDocumentLookup.cs:69-110`, desde `InitiateStorageWeighingHandler.cs:349-350`). El DTO ya trae `TruckEntriesClosedAt` y `TruckEntriesClosedByName` (`GetServiceRecordByDocumentHandler.cs:79-86`) y la pantalla ya pinta el aviso (`app/pages/operations/weighbridge/index.vue:911-920`).
- **Cambio exacto:**
  - Backend: `StorageDocumentLookup.FindClosedAsync(número, tipo, fecha)` extraído de `EnsureTruckEntriesNotClosedAsync` (misma consulta; selección pura `StorageDocumentMatcher.SelectClosed(cerrados, fechaPedida)`); `EnsureTruckEntriesNotClosedAsync` lo usa y conserva `ClosedMessage`. `GetServiceRecordByDocumentHandler`: sin candidato abierto, busca el cerrado y, si existe, devuelve el DTO con `TruckEntriesClosedAt` y `TruckEntriesClosedByName`.
  - Frontend: `index.vue`, `handleSearchCargoManifest` (`:854`): la rama `serviceRecord.truckEntriesClosedAt` (`:912`) se evalúa antes de `existingServiceRecord.value = serviceRecord` (`:908`) y deja `existingServiceRecord.value = null`; el mensaje existente y `blocksSave: true` bloquean el registro.
  - No se toca: `StorageDocumentMatcher.ClosedMessage` (defensa al guardar) ni `GetWarehouseStorageByDocumentHandler`.
- **Migración o script:** ninguno.
- **Pruebas automatizadas nuevas:** en `Wms.Tests/Weighbridge/StorageDocumentMatcherTests.cs`: `SelectClosed_SameDay_ReturnsClosed`, `SelectClosed_ServiceWithoutDate_ReturnsClosed`, `SelectClosed_OtherDay_ReturnsNull`, `SelectClosed_NoRequestDate_ReturnsMostRecentlyClosed`; `Wms.IntegrationTests/Weighbridge/ClosedDocumentLookupTests.cs`: `GetByDocument_ClosedTruckEntries_ReturnsClosedInfo`.
- **Criterios de aceptación:**
  - Dado el documento de 2026BA00012 con el ingreso de camiones cerrado por CE, cuando báscula lo busca para un camión nuevo, entonces la pantalla muestra el aviso de ingreso cerrado con quién lo cerró y no permite registrar.
- **Re-test QA:** F3-MCA-008; REG F11-REG-011.
- **Riesgo de regresión:** bajo.
- **Tamaño:** S. **Dependencias:** CHG-17.

#### CHG-55 — Máximo 5 fotos por recepción y por cargue, solo imágenes reales

- **Cierra:** DEF-F4-009 (MINOR).
- **Causa raíz:** `CompleteReceptionCommandValidator.cs` y `ExecuteLoadingOrderCommandValidator.cs` no validan las fotos (sí lo hacen `CreateReceptionCommandValidator.cs:33-44` y `CreateReceptionWithoutWeighbridgeCommandValidator.cs:111-122`). El tipo se deduce solo del prefijo `data:` y lo demás cae en `.jpg` en cuatro copias (`CompleteReceptionCommandHandler.cs:259-268`, `CreateReceptionCommandHandler.cs:360-368`, `CreateReceptionWithoutWeighbridgeCommandHandler.cs:475-481`, `ExecuteLoadingOrderCommandHandler.cs:482-492`); `StorageService.cs:112-130` valida extensión y tamaño, no el contenido: un PDF se guardó como `.jpg`. Las fotos se escriben dentro de la transacción después de otras escrituras: una foto inválida a mitad de lista revierte la base y deja archivos huérfanos.
- **Cambio exacto:**
  - Backend: clase pura `Wms.Application/Common/Validation/PhotoUploadRules.cs`: `MaxPhotos = 5`, `MaxSizeInMb = 5`, `Decode(base64)` detecta el tipo por la firma de bytes (JPEG, PNG, WEBP) y rechaza un prefijo `data:` que no sea imagen; errores «El formato de la imagen no es válido (Base64).», «La foto debe ser una imagen JPG, PNG o WEBP.» y «La foto no puede superar 5 MB.»; `DecodeAll`. `CompleteReceptionCommandValidator` agrega «Se permiten máximo 5 fotos por recepción.» y `ExecuteLoadingOrderCommandValidator` «Se permiten máximo 5 fotos por cargue.», ambos con «Los datos de la foto son requeridos.». Los cuatro handlers decodifican todas las fotos antes de abrir la transacción y guardan con la extensión detectada; se eliminan las cuatro copias de `DetectImageExtension`.
  - Frontend: `app/features/warehouse/components/PhotoUploader.vue:54` y `:163` aceptan solo `image/jpeg`, `image/png` e `image/webp`.
  - No se toca: `StorageService.ValidateFile` (segunda barrera) ni el soporte de la orden externa (`CreateLoadingOrderCommandHandler.cs:425-470`).
- **Migración o script:** sin migración. `fase-08-fotos.sql` (solo detección): recepciones con más de 5 fotos; en el servidor de pruebas, `file --mime-type` sobre `wwwroot/uploads/reception-photos` y `loading-photos` lista los archivos que no son imagen, que se retiran a mano junto con su fila (INSP00001 con 6 fotos y QAC411 con un PDF).
- **Pruebas automatizadas nuevas:** `Wms.Tests/Common/PhotoUploadRulesTests.cs`: `Decode_JpegBytes_ReturnsJpgExtension`, `Decode_PngBytes_ReturnsPngExtension`, `Decode_WebpBytes_ReturnsWebpExtension`, `Decode_PdfDataUri_ThrowsInvalidType`, `Decode_PdfBytesLabelledImageJpeg_ThrowsInvalidType`, `Decode_JpegOf5MbPlusOneByte_ThrowsTooLarge`, `Decode_InvalidBase64_Throws`, `Decode_RawBase64WithoutPrefix_DetectsByBytes`; `Wms.Tests/Warehouse/CompleteReceptionCommandValidatorTests.cs`: `Validate_SixPhotos_FailsWithMessage`, `Validate_FivePhotos_Passes`; `Wms.Tests/Warehouse/ExecuteLoadingOrderCommandValidatorTests.cs`: `Validate_SixPhotos_FailsWithMessage`.
- **Criterios de aceptación:**
  - Dado la recepción de QAC411, cuando Bodega completa con 6 fotos, entonces responde 400 «Se permiten máximo 5 fotos por recepción.» y no se guarda ningún archivo.
  - Dado una foto que en realidad es un PDF, cuando Bodega la envía, entonces responde 400 «La foto debe ser una imagen JPG, PNG o WEBP.».
- **Re-test QA:** F4-REC-009; REG F11-REG-014, F11-REG-016.
- **Riesgo de regresión:** bajo.
- **Tamaño:** M. **Dependencias:** CHG-08, CHG-31.

#### CHG-56 — Un producto declarado y no contado cuenta como faltante y avisa a Comercio Exterior

- **Cierra:** DEF-F4-010 (MINOR).
- **Causa raíz:** `Wms.Application/Warehouse/Commands/Reception/ReceptionDeclaredDifference.cs:53-69` (`ForTruck`) solo recorre los productos contados (`:63-68`): uno declarado y no contado no entra en las líneas, `HasDiscrepancy` queda en falso y no se avisa a CE. La vista tiene el mismo vacío: `ReceptionLineDifference.cs:11-12` y `ReceptionProjection.cs:105-122` y `:243-260` devuelven `null` sin cantidad contada.
- **Cambio exacto:**
  - Backend: `ForTruck` recorre la unión de productos contados y declarados para el camión (declarado > 0) y toma como 0 lo no contado; `Detail` conserva el formato («Aceite: declarado 7,00, contado 0,00 (diferencia -7)»). `ReceptionLineDifference.Compute(contado, declarado, conteoCerrado)`: sin contado y con conteo cerrado devuelve `-declarado`. `ReceptionProjection` pasa `conteoCerrado` = recepción Completed de mercancía suelta; `CountedQuantity` sigue nulo («—»).
  - Frontend: ninguno (`ReceptionProductBreakdown.vue` ya pinta «Diferencia: −7»).
  - No se toca: `FromLines` ni el flujo sin báscula; las unidades de carga no calculan diferencias.
- **Migración o script:** ninguno (las recepciones completadas muestran la diferencia con la proyección nueva; los avisos no emitidos no se reenvían).
- **Pruebas automatizadas nuevas:** en `Wms.Tests/Warehouse/ReceptionDeclaredDifferenceTests.cs`: `ForTruck_DeclaredProductNotCounted_FlagsFullShortage` (Cebolla 2 y Aceite 7 declarados, contada solo Cebolla 2 → diferencia −7 y 77,78 %), `ForTruck_DeclaredZeroOrNull_IsNotAShortage`, `ForTruck_CountedButNotDeclared_IsComparedAgainstZero`, `ForTruck_NothingDeclaredNothingCounted_HasNoDiscrepancy`; en `ReceptionLineDifferenceTests.cs`: `Compute_UncountedDeclaredWhenCountingClosed_IsMinusDeclared`, `Compute_UncountedWhileOpen_IsNull`, `Compute_NothingDeclaredWhenClosed_IsNull`.
- **Criterios de aceptación:**
  - Dado un camión con Cebolla 2 y Aceite 7 declarados, cuando Bodega completa la recepción contando solo Cebolla 2, entonces la respuesta trae `hasDiscrepancy` verdadero, CE recibe el aviso con «Aceite: declarado 7,00, contado 0,00 (diferencia -7)» y el detalle muestra «Diferencia: −7» en Aceite.
- **Re-test QA:** F4-REC-012; REG F11-REG-014, F11-REG-026.
- **Riesgo de regresión:** bajo.
- **Tamaño:** S. **Dependencias:** CHG-04.

#### CHG-57 — La novedad advierte cuando el desglose no cuadra con el total

- **Cierra:** DEF-F4-011 (MINOR).
- **Causa raíz:** ni el validador único de alta y edición (`Wms.Application/Warehouse/Novelties/Common/NoveltyInputValidator.cs:21-24`, solo negativos) ni el dominio (`WarehouseNovelty.cs:121`) comparan buena + dañada + faltante con el total: 100 con 90 + 20 responde 201 sin aviso. El plan de paridad dejó las novedades «sin regla de suma, como el legacy» (`docs/planes/paridad-legacy/plan-backend-paridad-legacy.md:169`) y la pantalla lo documenta en `NoveltyFormDialog.vue:6`.
- **Cambio exacto (advertencia, sin bloquear, para respetar la regla de paridad):**
  - Backend: clase pura `Wms.Domain/Entities/Warehouse/NoveltyQuantityRules.BalanceWarning(total, buena, dañada, faltante)`: con desglose en cero o cuadrado devuelve `null`; si no, «La suma de buena, dañada y faltante ({suma}) no coincide con el total ({total}).» (números es-CO, hasta 4 decimales; el sobrante no entra en la suma). Los handlers de alta y edición de novedades devuelven la advertencia en el campo nuevo `QuantityWarning` del DTO y la guardan en la auditoría de la novedad.
  - Frontend: `app/features/warehouse/utils/novelty-quantities.ts` con la misma regla (`noveltyBalanceWarning`) y `suggestGoodQuantity` (= máx(0, total − dañada − faltante)). `NoveltyFormDialog.vue:179-192` muestra la advertencia bajo las cantidades (`:387`) y, al guardar con advertencia, pide confirmación «¿Guardar la novedad de todos modos?» (`useConfirm` de PrimeVue); «Buena» se autocompleta con `suggestGoodQuantity` mientras no se edite a mano; el comentario de `:6` pasa a «Sin regla de suma obligatoria, como el legacy; la pantalla advierte el descuadre.».
  - No se toca: `UnloadedQuantity` ni el aviso a CE de `WarehouseNoveltyService.HasIssues`.
- **Migración o script:** sin migración. `fase-08-novedades.sql` (solo detección): novedades vigentes con desglose distinto de cero y distinto del total; Bodega decide al editarlas.
- **Pruebas automatizadas nuevas:** `Wms.Tests/Domain/Warehouse/NoveltyQuantityRulesTests.cs`: `BalanceWarning_QaCase90Plus20Over100_ReturnsMessage` (110 frente a 100), `BalanceWarning_EightyFifteenFive_ReturnsNull`, `BalanceWarning_AllZero_ReturnsNull`, `BalanceWarning_SurplusDoesNotCount`, `BalanceWarning_Decimals_ReturnsNull` (12,5 = 10 + 2,5); `test/unit/warehouse/novelty-quantities.spec.ts`: 100/90/20/0 → mensaje; 100/0/0/0 → `null`; 0,1 + 0,2 frente a 0,3 → `null`; `suggestGoodQuantity(100, 20, 0) = 80`.
- **Criterios de aceptación:**
  - Dado `POST warehouse/novelties` con total 100, buena 90 y dañada 20, cuando se envía, entonces responde 201 con `quantityWarning` «La suma de buena, dañada y faltante (110) no coincide con el total (100).».
  - Dado el formulario de novedad con esas cantidades, cuando Bodega pulsa «Guardar», entonces ve la advertencia y la confirmación; con «Cancelar» no se guarda nada.
- **Re-test QA:** F4-NOV-006; REG F11-REG-014.
- **Riesgo de regresión:** bajo.
- **Tamaño:** S. **Dependencias:** CHG-01.

#### CHG-58 — Montacargas: horómetros válidos, mensajes de negocio e historial completo

- **Cierra:** DEF-F4-013 (MINOR), DEF-F4-016 (MINOR), DEF-F4-017 (TRIVIAL).
- **Causa raíz:**
  - DEF-F4-013: `StartForkliftUseCommandValidator.cs:21-22` y `EndForkliftUseCommandValidator.cs:13-14` usan `GreaterThanOrEqualTo(0)`; el dominio acepta inicial 0 (`ForkliftUse.cs:52`, `< 0`) y final igual al inicial (`:84`, `<`), y `EndForkliftUseCommandHandler.cs:48` repite la regla. La pantalla exige más (`ForkliftUseDialog.vue:81-116`).
  - DEF-F4-017: `StartForkliftUseCommandValidator.cs:17-19` encadena `NotEmpty` y `Must(Guid.TryParse)` y devuelve dos errores con «service record»; `:12-15`, `:24-27` y `:32-35` listan claves internas (`DobleTroque`, `GuacalEstiba`, `Immediate`, `PendingBilling`); `StartForkliftUseCommandHandler.cs:75-77` muestra un GUID; `Enum.TryParse` (`:26`) acepta «99».
  - DEF-F4-016: el historial (`ForkliftUseList.vue:670-717`, modo `history`) no pinta horómetros, valor, modo de pago ni factura, y `ForkliftUseDto` no trae valor ni factura (`GetActiveForkliftUsesHandler.cs:20-27` no incluye `InvoiceItem`). El detalle (botón de ojo de `:718-730`, sin etiqueta) sí los muestra.
- **Cambio exacto:**
  - Backend: validadores con `GreaterThan(0)` («El horómetro inicial debe ser mayor que cero.», «El horómetro final debe ser mayor que cero.»); `ForkliftUse.Start` rechaza inicial ≤ 0 y `ForkliftUse.End` final ≤ inicial («El horómetro final debe ser mayor que el inicial ({inicial}).»); se elimina el bloque duplicado de `EndForkliftUseCommandHandler.cs:47-52`. Nuevo `Wms.Application/Warehouse/Commands/Forklift/ForkliftMessages.cs`: servicio ausente o mal formado → un solo error «El camión no tiene un servicio activo. Seleccione un camión con servicio activo para iniciar el montacargas.»; cliente → «El cliente indicado no es válido.»; tipo de vehículo (`Cascade(Stop)`, `Enum.IsDefined`) → «Seleccione el tipo de vehículo: Tractomula, Doble troque, Sencillo, Turbo o Guacal / Estiba.»; modo de pago → «Seleccione el modo de pago: Pago inmediato o Pendiente por facturar.»; uso activo → «Ya existe un uso de montacargas activo para este camión. Finalícelo antes de iniciar uno nuevo.»; fin con id inválido → «El uso de montacargas indicado no es válido.». `ForkliftUseDto` suma `SubTotal`, `TaxAmount`, `Total`, `InvoiceId` e `InvoiceNumber`, llenados desde `InvoiceItem` (`GetActiveForkliftUsesHandler.cs:20-27` y `:89-135`; `WarehouseMapper.cs:40-49` los ignora en el mapeo automático).
  - Frontend: `types/forklift.ts` con los campos nuevos; `ForkliftUseList.vue:670-717` agrega Horómetro inicial, Horómetro final, Valor (sin IVA), IVA, Total, Modo de pago y Factura; el botón de ojo lleva `aria-label="Ver detalle"` y la fila abre el detalle; `ForkliftUseDetailDialog.vue:132-147` agrega «Valor (sin IVA)» e «IVA» (§10 · Valor con IVA o neto). Formato en `app/features/warehouse/utils/forklift-history.ts`.
  - No se toca: las restricciones `chk_forklift_*` de la base (`ForkliftUseConfiguration.cs:12-15`) ni el cálculo de la tarifa.
- **Migración o script:** sin migración. `fase-08-montacargas.sql` (solo detección): usos con inicial ≤ 0 o final ≤ inicial; son datos de QA.
- **Pruebas automatizadas nuevas:** `Wms.Tests/Domain/Warehouse/ForkliftUseTests.cs`: `Start_ZeroHourmeter_Throws`, `End_EqualToInitial_Throws` (100 → 100), `End_GreaterThanInitial_Succeeds` (100 → 105: 5 h); `Wms.Tests/Warehouse/ForkliftValidatorsTests.cs`: `Start_InitHourmeterZero_Rejected`, `End_EndHourmeterZero_Rejected`, `Start_WithoutServiceRecord_ReturnsSingleBusinessMessage`, `Start_InvalidVehicleType_DoesNotExposeEnumKeys`, `Start_NumericVehicleType_Rejected`, `Start_InvalidPaymentMode_DoesNotExposePendingBilling`, `End_MalformedId_ReturnsSingleMessage`; `Wms.IntegrationTests/Warehouse/ForkliftUsesListTests.cs`: `GetForkliftUses_Complete_ReturnsSubTotalTotalAndInvoiceNumber`; `test/unit/warehouse/forklift-history.spec.ts`: `formatHourmeter(1250)` → «1.250,0 h», `formatHourmeter(null)` → «—».
- **Criterios de aceptación:**
  - Dado Bodega, cuando inicia un montacargas con horómetro 0, entonces responde 400 «El horómetro inicial debe ser mayor que cero.»; cuando finaliza con 100 un uso iniciado en 100, responde 400 «El horómetro final debe ser mayor que el inicial (100).».
  - Dado QAB204 sin servicio, cuando Bodega inicia el montacargas, entonces ve un solo mensaje: «El camión no tiene un servicio activo. Seleccione un camión con servicio activo para iniciar el montacargas.».
  - Dado un uso completado y facturado, cuando Bodega abre `/warehouse/forklift/history`, entonces ve horómetros, valor sin IVA, IVA, total, modo de pago y número de factura.
- **Re-test QA:** F4-MON-004, F4-MON-006, F4-MON-012, F4-MON-014; REG F11-REG-015.
- **Riesgo de regresión:** bajo.
- **Tamaño:** M. **Dependencias:** CHG-15.

#### CHG-59 — Los demás PATCH dejan de borrar o desactivar lo que no se envía

- **Cierra:** ningún defecto con ficha propia. Corrige la misma causa de CHG-26 (PATCH que borra lo que no se envía) en otros cinco PATCH encontrados en la verificación; en F7-AUD-004 un PATCH de unidad de medida la desactivó.
- **Causa raíz:** los requests declaran campos no anulables o los handlers asignan sin distinguir «ausente» de «vacío»: `UpdateUnitMeasureRequest(string Name, bool IsActive)` (`UpdateUnitMeasureHandler.cs:24-29`: `isActive` ausente vale `false` y desactiva); `UpdateCargoUnitTypeRequest` (mismo patrón); `SystemParameter.Update` (`SystemParameter.cs:37-43`) borra la descripción ausente; `WarehouseLocation.Update` (`WarehouseLocation.cs:85-87`) borra pasillo, estante y nivel ausentes; el PATCH de levantes ejecuta `ClearFob()` sin `fobUsd` (`ReleaseFobService.cs:37-42`) y deja las observaciones en `null`.
- **Cambio exacto:**
  - Backend: con `PatchField<T>` de CHG-26: `UpdateUnitMeasureRequest` y `UpdateCargoUnitTypeRequest` pasan a `string? Name` y `bool? IsActive` (el nombre se valida solo si viene; el estado cambia solo si viene); `PATCH administration/system-parameters/{id}` usa `PatchField<string> Description`; `PATCH warehouse/locations/{id}` usa `PatchField<string>` para pasillo, estante y nivel; `PATCH foreign-trade/imports/{id}/releases/{releaseId}` usa `PatchField<decimal?> FobUsd` y `PatchField<string> Observations`. Ausente = se conserva; `null` explícito = se limpia.
  - Frontend: ninguno (las pantallas envían todos los campos).
  - No se toca: los PATCH ya verificados que usan `??` o guardas (terceros, cuentas, contactos, convenios, servicios, precios, motivos, productos, conductores, vehículos, usuarios, ingresos, embalajes, borrador del depósito y factura).
- **Migración o script:** sin migración. `fase-08-patch.sql` (solo detección): unidades de medida inactivas (`SELECT name, is_active FROM unit_measures WHERE is_active = false;`); el Admin reactiva «Bulto» desde la pantalla si QA la dejó inactiva.
- **Pruebas automatizadas nuevas:** `Wms.IntegrationTests/Administration/CatalogPatchTests.cs`: `PatchUnitMeasure_NameOnly_KeepsIsActive`, `PatchCargoUnitType_NameOnly_KeepsIsActive`, `PatchSystemParameter_ValueOnly_KeepsDescription`, `PatchLocation_NameAndCapacityOnly_KeepsAisleRackLevel`, `PatchRelease_WithoutFob_KeepsFob`.
- **Criterios de aceptación:**
  - Dado la unidad «Bulto» activa, cuando el Admin envía un PATCH solo con el nombre, entonces el nombre cambia y la unidad sigue activa.
  - Dado un levante con FOB 1.200 USD, cuando CE envía un PATCH solo con la cantidad, entonces el FOB se conserva.
- **Re-test QA:** F7-AUD-004; REG F11-REG-004.
- **Riesgo de regresión:** bajo.
- **Tamaño:** S. **Dependencias:** CHG-26.

### Fase 9 — MINOR de facturación, avisos y auditoría

- **Objetivo:** retirar el ciclo OnDemand (§10 · OnDemand se retira), permitir quitar el límite de crédito con efecto inmediato (§10 · Mora), avisar una sola vez el vencimiento y cada renovación, alinear la preferencia «Consolidada» con lo que hace el sistema, igualar la previsualización con el cobro real, conservar la factura anulada en el reporte por CPI, mostrar la cantidad facturada en el detalle de almacenamiento, avisar la anulación de depósitos y auditar los catálogos. Cierra DEF-F6-008, DEF-F6-014, DEF-F6-018, DEF-F6-017, DEF-F6-016, DEF-F7-007, DEF-F8-006, DEF-F8-007 y DEF-F7-008.
- **Criterio de entrada:** checkpoint de la Fase 8 aprobado.
- **Cambios:** CHG-60, CHG-61, CHG-62, CHG-63, CHG-64, CHG-65, CHG-66, CHG-67, CHG-68.
- **Orden interno:** CHG-60 → CHG-61 → CHG-62 → CHG-63 (los tres últimos en `BillingJobService.cs` o en `BillingConfigForm.vue`) → CHG-64 → CHG-65 → CHG-66 → CHG-67 → CHG-68.
- **Migración de la fase (la genera el implementador con `dotnet ef`):** `AddInvoiceDueNoticeSentAt` (CHG-62).
- **Riesgos y mitigación:**
  - CHG-64 extrae el cálculo real a `FormulaPricing`. Mitigación: las pruebas existentes de facturación y las nuevas de `FormulaPricing` corren antes del re-test.
  - Un cliente con OnDemand en producción sigue sin cobro de almacenamiento hasta que Facturación cambie su ciclo. Mitigación: la detección del script se entrega en el checkpoint.
- **Saneamiento de datos:** `fase-09-ondemand.sql`, `fase-09-avisos.sql` (después de la migración), `fase-09-preferencias.sql` y `fase-09-detalle-almacenamiento.sql`, descritos en cada cambio.
- **Criterio de salida:** compuertas comunes (regla 4.0.4) y en PASA: F6-ALM-006, F6-CFG-004, F6-CFG-006, F6-JOB-002, F6-CAR-011, F6-ALM-008, F6-CON-001, F6-PRE-001, F6-PRE-002, F6-PRE-003, F7-REP-022, E2E-02, E2E-11, F7-AUD-004; REG F11-REG-004, F11-REG-021, F11-REG-025, F11-REG-026.
- **Checkpoint:** se entrega al usuario la lista de clientes con OnDemand o `PerWeighbridgeCycle`, la corrida doble del job sin avisos repetidos y la previsualización frente al cobro real de las cuatro fórmulas. El usuario aprueba la migración y el saneamiento en staging.

#### CHG-60 — El ciclo OnDemand deja de ofrecerse

- **Cierra:** DEF-F6-008 (MINOR).
- **Causa raíz:** `Wms.Application/Billing/Common/Services/BillingCycleCatalog.cs:33` publica OnDemand en `GET billing/configurations/cycles` (el selector del frontend se arma con esa lista) y `StorageBillingService.cs:368-372` no abre período ni factura para ese ciclo: el depósito nunca se cobra ni aparece en pendientes.
- **Cambio exacto (aplica §10 · OnDemand se retira):**
  - Backend: `BillingCycleCatalog.cs` quita OnDemand (línea `:33`) y el texto «y bajo demanda» (`:3`, `:40`); `BillingCyclesController.cs:21,27` dice «Los ocho ciclos»; `UpsertBillingConfigurationValidator` rechaza OnDemand con «El ciclo de facturación no es válido.». El miembro `OnDemand` del enum se conserva, con el comentario «Retirado (DEF-F6-008); solo para leer configuraciones antiguas», para que EF lea las filas existentes.
  - Frontend: `app/features/billing/types/billing-config.ts:5` y `:13` sin OnDemand; `useBillingCycles.ts:19` devuelve «Mes calendario» para Monthly y texto vacío sin días.
  - No se toca: `StorageBillingService.cs:368-372` (una configuración antigua sigue sin cobrar hasta que Facturación cambie su ciclo).
- **Migración o script:** sin migración. `fase-09-ondemand.sql`: detección de clientes con ciclo OnDemand y de sus depósitos confirmados sin período; corrección en la base local y en staging: `UPDATE stakeholder_billing_configurations SET billing_cycle = 'Monthly', updated_at = now() WHERE billing_cycle = 'OnDemand';`. En producción, Facturación cambia el ciclo desde la configuración del cliente.
- **Pruebas automatizadas nuevas:** en `Wms.Tests/Billing/BillingCycleCatalogTests.cs`: `Catalog_ListsTheEightCycles`, `Catalog_DoesNotOfferOnDemand`; `Wms.Tests/Billing/Validators/UpsertBillingConfigurationValidatorTests.cs`: `Validate_OnDemand_IsRejected`; `test/unit/billing/billing-cycles.spec.ts`: Monthly → «Mes calendario», Days15 → «Períodos de 15 días».
- **Criterios de aceptación:**
  - Dado Facturación en la configuración de un cliente, cuando abre «Ciclo de facturación», entonces ve ocho ciclos y no «Bajo demanda».
  - Dado el API, cuando recibe una configuración con ciclo OnDemand, entonces responde 400 «El ciclo de facturación no es válido.».
- **Re-test QA:** F6-ALM-006, F6-CFG-004; REG F11-REG-021.
- **Riesgo de regresión:** bajo.
- **Tamaño:** S. **Dependencias:** CHG-48.

#### CHG-61 — Quitar el límite de crédito se guarda y desbloquea al instante

- **Cierra:** DEF-F6-014 (MINOR).
- **Causa raíz:** `StakeholderBillingConfiguration.cs:57-77`: `Update(decimal? creditLimit = null)` solo asigna con valor (`:75`), así que `null` significa «sin cambio»; `app/features/billing/components/BillingConfigForm.vue:86` además omite el campo vacío (`creditLimit.value ?? undefined`). El estado del cliente solo lo recalcula el job diario.
- **Cambio exacto (aplica §10 · Mora, sin límite nunca bloquea):**
  - Backend: `StakeholderBillingConfiguration.Update(ciclo, plazo, creditLimit, preferencia)` asigna todos los campos (el PUT reemplaza la configuración; `null` = sin límite). `UpsertBillingConfigurationHandler.cs:30` pasa los cuatro y, después de guardar, llama `IBillingService.RefreshFinancialStatusAsync(clienteId)` (CHG-13).
  - Frontend: `BillingConfigForm.vue:86` envía `creditLimit: creditLimit.value` (vacío = `null`), con la construcción extraída a `app/features/billing/utils/billing-config-payload.ts`; `types/requests.ts:135` → `creditLimit?: number | null`.
  - No se toca: `ClientFinancialStatusRules` ni el job.
- **Migración o script:** ninguno (QA vuelve a guardar «QA Cliente Mora» sin límite).
- **Pruebas automatizadas nuevas:** `Wms.Tests/Domain/Billing/StakeholderBillingConfigurationTests.cs`: `Update_NullCreditLimit_ClearsLimit` (1.000 → `null`), `Update_NegativeCreditLimit_Throws`; `test/unit/billing/billing-config-payload.spec.ts`: límite vacío → `creditLimit: null`; `Wms.IntegrationTests/Billing/CreditLimitTests.cs`: `RemoveLimit_BlockedCustomer_BecomesOverdueWarning`.
- **Criterios de aceptación:**
  - Dado «QA Cliente Mora» bloqueado con límite 1.000 y deuda vencida 5.000.000, cuando Facturación borra el límite y guarda, entonces la configuración queda sin límite y el cliente pasa de inmediato a «Con mora» (no bloqueado).
- **Re-test QA:** F6-CFG-006; REG F11-REG-025.
- **Riesgo de regresión:** bajo.
- **Tamaño:** S. **Dependencias:** CHG-13.

#### CHG-62 — Un solo aviso de vencimiento por factura y aviso de cada renovación

- **Cierra:** DEF-F6-018 (MINOR).
- **Causa raíz:** `BillingJobService.cs:293-340` (`NotifyUpcomingDueDatesAsync`) no guarda qué facturas ya avisó y notifica con correo (`:321`) en cada corrida; el servicio corre un minuto después de cada arranque y luego cada 24 h, de ahí 16 avisos en QA; el mensaje usa el número crudo (vacío en Borrador). `CloseStoragePeriodsHandler.cs:76-81` solo avisa los valores mínimos y la renovación del job (`BillingJobService.cs:263`) no avisa.
- **Cambio exacto:**
  - Backend: `Invoice` suma `DueNoticeSentAt` y `MarkDueNoticeSent(fecha)` (columna `due_notice_sent_at timestamptz` nula); `NotifyUpcomingDueDatesAsync` filtra `DueNoticeSentAt == null`, marca cada factura avisada y guarda; el texto sale de la clase pura `DueNoticeMessage.Build(número, cliente, días, pendiente)` con «sin número» cuando falta. `StorageBillingOpenResult` suma `PeriodStart` y `PeriodEnd` (`StorageBillingService.cs:437`); `StorageBillingNotifier.NotifyPeriodRenewedAsync` avisa a Facturación «Almacenamiento renovado» / «El depósito {número} abrió un nuevo período de almacenamiento del {inicio:dd/MM/yyyy} al {fin:dd/MM/yyyy}. Revise la factura en Borrador.». Lo llaman, después de confirmar, `CloseStoragePeriodsHandler` (junto con `NotifyBillingWarningsAsync`, que reemplaza a `NotifyMinimumValueBillingAsync`) y la renovación del job cuando abre períodos.
  - Frontend: ninguno.
  - No se toca: la frecuencia de los servicios de fondo.
- **Migración o script:** `AddInvoiceDueNoticeSentAt` (columna nula, sin valor por defecto). `fase-09-avisos.sql`, después de la migración: marca `due_notice_sent_at` con la fecha del primer aviso de cada factura y deja como leídos los avisos duplicados («Factura próxima a vencer» repetidos por usuario y factura).
- **Pruebas automatizadas nuevas:** `Wms.Tests/Domain/Billing/InvoiceDueNoticeTests.cs`: `MarkDueNoticeSent_SetsTimestamp`; `Wms.Tests/Billing/DueNoticeMessageTests.cs`: `Build_NullNumber_UsesSinNumero`; `Wms.IntegrationTests/Billing/DueNoticeJobTests.cs`: `NotifyUpcomingDueDates_RunTwice_NotifiesOnce`; `Wms.IntegrationTests/Billing/ManualPeriodCloseTests.cs`: `CloseBeforeEnd_NotifiesRenewal`.
- **Criterios de aceptación:**
  - Dado una factura que vence en dos días, cuando el job corre tres veces, entonces Facturación recibe un solo aviso y un solo correo.
  - Dado 2026BA00002, cuando Facturación cierra su período, entonces recibe «El depósito 2026BA00002 abrió un nuevo período de almacenamiento del 03/11/2026 al 03/12/2026. Revise la factura en Borrador.».
- **Re-test QA:** F6-JOB-002, F6-CAR-011, F6-ALM-008; REG F11-REG-021.
- **Riesgo de regresión:** bajo.
- **Tamaño:** M. **Dependencias:** CHG-10, CHG-13.

#### CHG-63 — La preferencia «Consolidada» promete solo lo que hace

- **Cierra:** DEF-F6-017 (MINOR).
- **Decisión:** D-1 resuelta el 3-oct-2026 (§5): «Consolidada» queda para almacenamiento y guías a crédito; báscula y montacargas siguen con factura individual.
- **Causa raíz:** `BillingJobService.cs:111-167` (`ConsolidateDailyChargesAsync`) no fusiona cargos: solo concilia pagos. La consolidación existe al crear la factura en almacenamiento (`StorageBillingService.cs:408-412`) y en la guía a crédito (`CreateDispatchGuideCommandHandler.cs:244-249`) con `BillingService.GetOrCreateConsolidatedInvoiceAsync` (`:43-78`); los cobros «por facturar» de báscula y montacargas crean factura individual sin leer la preferencia (`StartWeighingOnlyPendingBillingHandler.cs:89`, `StartStoragePendingBillingHandler.cs:115`, `StartOutputPendingBillingHandler.cs:95`, `EndForkliftUseCommandHandler.cs:130`) y `PerWeighbridgeCycle` no tiene código. La configuración promete otra cosa (`BillingConfigForm.vue:137`). El legacy no consolida.
- **Cambio exacto (decisión D-1):**
  - Backend: `IBillingJobService.cs:11-14` y `BillingJobService.cs:111-167` pasan a `ReconcileInvoicePaymentsAsync` y `ReconciliationResult`, solo sobre facturas con pagos, con el log «Conciliación diaria de pagos: …»; `DailyChargeConsolidationBackgroundService.cs` pasa a `InvoicePaymentReconciliationBackgroundService` (registro en `Program.cs:62`).
  - Frontend: `BillingConfigForm.vue:137` → «Consolidada: una sola factura por ventana (semanal, quincenal o mensual según el ciclo) con los depósitos y las guías de salida a crédito; los cobros de báscula y montacargas siguen como factura individual.»; `PerWeighbridgeCycle` sale de `INVOICING_PREFERENCES` (`:31-35`) y de la ayuda (el enum conserva el valor).
  - Documentación de QA: `docs/qa/fase-06-facturacion.md`, F6-CON-001, pasa a esperar «factura individual para báscula y montacargas».
  - No se toca: la consolidación de almacenamiento y guías (ya funciona, F6-ALM-007).
- **Migración o script:** sin migración. `fase-09-preferencias.sql`: detección de clientes con `PerWeighbridgeCycle`; corrección en la base local y en staging: `UPDATE stakeholder_billing_configurations SET invoicing_preference = 'PerService', updated_at = now() WHERE invoicing_preference = 'PerWeighbridgeCycle';` (hoy se comportan igual).
- **Pruebas automatizadas nuevas:** `Wms.IntegrationTests/Billing/PaymentReconciliationJobTests.cs`: `Reconcile_ZeroValueDraft_StaysDraft`, `Reconcile_InvoiceWithVerifiedPayment_RecalculatesPending`; `test/components/billing/BillingConfigForm.spec.ts`: no ofrece «Por ciclo de báscula».
- **Criterios de aceptación:**
  - Dado un cliente con preferencia «Consolidada», cuando Facturación abre su configuración, entonces el texto dice que báscula y montacargas siguen como factura individual y no aparece «Por ciclo de báscula».
  - Dado una factura en Borrador de valor 0 sin pagos, cuando corre la conciliación diaria, entonces sigue en Borrador.
- **Re-test QA:** F6-CON-001 (con el resultado esperado actualizado); REG F11-REG-021.
- **Riesgo de regresión:** bajo.
- **Tamaño:** S. **Dependencias:** CHG-62.

#### CHG-64 — La previsualización de fórmulas calcula igual que el cobro real

- **Cierra:** DEF-F6-016 (MINOR).
- **Causa raíz:** `Wms.Application/Billing/Queries/PreviewFormula/PreviewFormulaHandler.cs` repite una parte del cálculo de `BillingResolver.CalculateAsync` (`BillingResolver.cs:93-119`) y omite el resto: FIXED con IVA incluido suma IVA al bruto (`:45-46`) en vez de desagregarlo (100.000 frente a 119.000); PRORATED usa `BaseQuantity = Quantity` (`:39`), así que la fracción siempre es 1; PER_CARGO_UNIT no arma `CargoUnitCountsByType` (`StorageBillingService.cs:193`) y da 0 unidades; PER_VEHICLE_TYPE exige las cinco tarifas (`PerVehicleTypeFormulaCalculator.cs:39-56`) y no recibe el tipo de vehículo.
- **Cambio exacto:**
  - Backend: clase estática `Wms.Application/Billing/Services/FormulaPricing.Price(registry, regla, contexto, tasaIva)` con los pasos de `BillingResolver.CalculateAsync` (cantidad facturable, bruto, IVA incluido o no, unidades de carga); `BillingResolver` la usa. `PreviewFormulaHandler` arma la regla con `TaxIncluded` y un contexto con `Quantity`, `BaseQuantity` (o `Quantity`), `VehicleType` y las unidades por tipo, y responde el valor, el IVA y el total de `Price`. `PreviewFormulaQuery` y `PreviewFormulaRequest` (`BillingPreviewController.cs`) suman `TaxIncluded`, `BaseQuantity` y `VehicleType`. PER_VEHICLE_TYPE exige el tipo («Indique el tipo de vehículo a previsualizar.», «El tipo de vehículo no es válido.») y solo su tarifa. Cantidad facturable 0 responde el mismo 400 del cobro real. FIXED con IVA incluido explica «Tarifa fija de $100.000 (IVA incluido).».
  - Frontend: `FormulaPreviewPanel.vue` recibe `taxIncluded` (desde `AgreementServiceFormDialog.vue:236` y `ServicePricingRuleFormDialog.vue:203`), muestra «Cantidad inicial (recibida)» solo para PRORATED y «Tipo de vehículo» solo para PER_VEHICLE_TYPE; `types/formula-preview.ts` con los tres campos.
  - No se toca: los calculadores.
- **Migración o script:** ninguno.
- **Pruebas automatizadas nuevas:** `Wms.Tests/Billing/Services/FormulaPricingTests.cs` y `Wms.Tests/Billing/Queries/PreviewFormulaHandlerTests.cs`: `Fixed_TaxIncluded19_Rate100000_Total100000` (neto 84.033,61 e IVA 15.966,39), `Fixed_NotTaxIncluded_Rate100000_Total119000`, `Prorated_Pct1_CIF10000000_Qty40_Base100_Amount40000`, `PerCargoUnit_Rate35000_TwoUnits_Amount70000`, `PerCargoUnit_ZeroUnits_ThrowsBadRequest`, `PerVehicleType_Tractomula_OnlyThatRateRequired`, `PerVehicleType_WithoutVehicleType_ThrowsBadRequest`.
- **Criterios de aceptación:**
  - Dado una tarifa FIXED de 100.000 con IVA incluido, cuando Facturación la previsualiza, entonces ve total 100.000 (84.033,61 + 15.966,39), igual que el cobro real.
  - Dado PRORATED al 1 % con CIF 10.000.000, stock 40 y recibido 100, cuando se previsualiza, entonces el valor es 40.000.
  - Dado PER_VEHICLE_TYPE con solo la tarifa de Tractomula, cuando se previsualiza para Tractomula, entonces muestra esa tarifa sin pedir las otras cuatro.
- **Re-test QA:** F6-PRE-001, F6-PRE-002, F6-PRE-003; REG F11-REG-021.
- **Riesgo de regresión:** medio (toca el cálculo real al extraerlo). Lo mitigan las pruebas de `FormulaPricing` y las de facturación existentes.
- **Tamaño:** M. **Dependencias:** CHG-24, CHG-25.

#### CHG-65 — El reporte por CPI conserva la factura anulada al refacturar

- **Cierra:** DEF-F7-007 (MINOR).
- **Causa raíz:** `Wms.Application/Reports/Queries/GetDepositBilling/GetDepositBillingHandler.cs:65-72` obtiene las facturas desde `StorageBillingPeriods.InvoiceId`, y la refacturación (`ReissueInvoiceCommandHandler.cs:72`) re-enlaza los períodos a la factura nueva: la anulada se queda sin períodos y desaparece. Las líneas clonadas conservan `StorageBillingPeriodId` en las dos facturas (`InvoiceItem.CloneFor`, `:139`).
- **Cambio exacto:**
  - Backend: `GetDepositBillingHandler` une las facturas de los períodos con las de las líneas que apuntan a esos períodos; el rango de cada factura sale de los períodos de sus líneas. Clase pura `Wms.Application/Reports/Common/DepositInvoiceLinks.Resolve(períodos, enlacesDeLíneas)`. `InvoicesTotal` sigue excluyendo las anuladas (`:131`). `DepositBillingInvoiceDto` suma `IsReissued`.
  - Frontend: `app/pages/billing/reports/deposit-billing.vue:185`: «Refacturada como» muestra el número, «Sin número» si fue refacturada sin número, o «—».
  - No se toca: `ReissueInvoiceCommandHandler`.
- **Migración o script:** ninguno.
- **Pruebas automatizadas nuevas:** `Wms.Tests/Reports/DepositInvoiceLinksTests.cs`: `Resolve_CancelledAndReissueShareSamePeriods_ReturnsBothInvoices`, `Resolve_PeriodLinkedOnlyViaItems_StillIncluded`, `Resolve_PeriodsOfOtherDeposit_Excluded`, `Resolve_NoLinks_ReturnsEmpty`.
- **Criterios de aceptación:**
  - Dado un depósito cuya factura de almacenamiento se anuló y refacturó, cuando Facturación abre el reporte por CPI, entonces aparecen las dos facturas: la anulada con «Refacturada como» y la nueva; el total suma solo la nueva.
- **Re-test QA:** F7-REP-022; REG F11-REG-021.
- **Riesgo de regresión:** bajo.
- **Tamaño:** S. **Dependencias:** CHG-22.

#### CHG-66 — El detalle de la factura de almacenamiento usa la cantidad facturada

- **Cierra:** DEF-F8-006 (MINOR).
- **Causa raíz:** `Wms.Application/Billing/Common/Services/StorageBillingService.cs:779-783` (`BuildDepositDetail`, `:769-795`) arma el texto con `DeclaredQuantity`, que CE-7 no cambia (`WarehouseStorageProduct.cs:334-358`) y que las salidas tampoco mueven; el importe sí usa el stock vigente (`:176`). Además lista productos sin stock (`:778`). Se usa al abrir (`:400`) y al recalcular (`:566`).
- **Cambio exacto:**
  - Backend: `BuildDepositDetail(depósito, cargos, inicio, fin)` toma los productos de los cargos y muestra `StorageChargeProduct.StockAtBilling` (recibido tras CE-7 en el primer período; saldo en las renovaciones); solo aparecen los productos facturados en el período; nombre y unidad salen de los productos del depósito ya cargados (`:759-766`). La construcción de líneas pasa a la clase pura `StorageDetailLines.FromCharges(...)`.
  - Frontend: ninguno.
  - No se toca: `StorageInvoiceDetailFormatter` (el formato no cambia).
- **Migración o script:** sin migración. `fase-09-detalle-almacenamiento.sql` (solo detección): facturas no anuladas de depósitos cuyo declarado difiere del stock; las de Borrador se corrigen con «Editar detalle» y las emitidas en SIIGO.
- **Pruebas automatizadas nuevas:** `Wms.Tests/Billing/StorageInvoiceDetailLinesTests.cs`: `FromCharges_FirstPeriodAfterCe7_ShowsReceived98NotDeclared100` («98 BULTO»), `FromCharges_Renewal_ShowsBalance110NotDeclared120`, `FromCharges_ProductWithoutStock_IsOmitted`; `StorageInvoiceDetailFormatterTests.Build_UsesTheGivenQuantity` («ALMACENAMIENTO DE: 98 BULTO QA Cebolla…»).
- **Criterios de aceptación:**
  - Dado 2026BA00027 con declarado 100 y recibido 98 tras CE-7, cuando se abre su primer período, entonces el detalle dice «ALMACENAMIENTO DE: 98 BULTO …».
  - Dado su renovación con saldo 110 frente a un declarado de 120, cuando se abre el período, entonces el detalle dice 110.
- **Re-test QA:** E2E-02; REG F11-REG-021.
- **Riesgo de regresión:** bajo.
- **Tamaño:** S. **Dependencias:** CHG-24, CHG-28.

#### CHG-67 — Anular un depósito avisa a Bodega y a Facturación

- **Cierra:** DEF-F8-007 (MINOR).
- **Causa raíz:** `CancelWarehouseStorageHandler.cs:45` delega en `WarehouseStorageCancellationService.NotifyAsync` (`WarehouseStorageCancellationService.cs:200-232`), que solo avisa a Bodega por órdenes en curso que perdieron ítems (`:202-221`) y a Facturación por facturas «para revisar» (`:224`). El stock que sale (`:138-154`) y las facturas que el WMS anula solo (`InvoiceCancellationPolicy.Apply`, `:178`) no generan avisos.
- **Cambio exacto:**
  - Backend: `WarehouseStorageCancellationResult` (`:16-24`) agrega `RemovedStock`, `RemovedProductCount` y `Reason`; `CancelledInvoiceDto` (`InvoiceCancellationDtos.cs:4`) agrega `Total`, que llena `InvoiceCancellationPolicy.cs:56`. Clase pura `DepositCancellationNotices.Build(resultado)`: a Bodega, solo si salió stock, «Depósito anulado: mercancía fuera del inventario» / «El depósito {número} fue anulado y su mercancía salió del inventario ({stock} en {n} producto(s)). Motivo: {motivo}.» (advertencia); a Facturación, uno por factura anulada, «Factura anulada por depósito anulado» / «El depósito {número} fue anulado y el WMS anuló la factura {número o «sin número»} ({total}). Motivo: {motivo}.». `NotifyAsync` los envía con `NotifyRoleAsync`.
  - Frontend: ninguno (`app/pages/notifications` lista cualquier aviso).
  - No se toca: los avisos existentes de `:202-221` y `:224`.
- **Migración o script:** ninguno (las anulaciones pasadas no se notifican de nuevo).
- **Pruebas automatizadas nuevas:** `Wms.Tests/ForeignTrade/DepositCancellationNoticesTests.cs`: `Build_StockRemoved_NoticesWarehouse` (25 unidades, 1 producto), `Build_ZeroStock_NoWarehouseNotice`, `Build_TwoCancelledInvoices_TwoBillingNotices`, `Build_NoInvoices_NoBillingNotice`.
- **Criterios de aceptación:**
  - Dado 2026BA00031 con 25 unidades en stock y una factura en Borrador, cuando CE lo anula con el motivo «Prueba QA», entonces Bodega recibe «El depósito 2026BA00031 fue anulado y su mercancía salió del inventario (25 en 1 producto(s)). Motivo: Prueba QA.» y Facturación recibe el aviso de la factura anulada con su total.
- **Re-test QA:** E2E-11 (paso 6); REG F11-REG-026.
- **Riesgo de regresión:** bajo.
- **Tamaño:** S. **Dependencias:** CHG-22.

#### CHG-68 — Los catálogos y los roles de usuario quedan en la auditoría

- **Cierra:** DEF-F7-008 (MINOR).
- **Causa raíz:** `AppDbContext.cs:149-150` audita solo las entidades que implementan `IAuditable`, y los catálogos no lo hacen: `PackagingType.cs:5`, `UnitMeasure.cs:10`, `CargoUnitType.cs:10`, `ForkliftRate.cs:6`, `WarehouseLocation.cs:5`, `EntryReason.cs:3`, `Driver.cs:5`, `Vehicle.cs:5`, `ServicePrice.cs:5`, `ServicePricingRule.cs:14`, `ServicePricingRuleParameter.cs:8`, `AgreementService.cs:11`, `AgreementParameter.cs:5`, `StakeholderBillingConfiguration.cs:7`, `StakeholderBankAccount.cs:5`, `StakeholderContactInfo.cs:3` y `Tax.cs:6`. Los roles de usuario viven en la tabla de Identity `AspNetUserRoles`, que no se puede marcar.
- **Cambio exacto:**
  - Backend: las 17 entidades implementan `IAuditable` (interfaz marcadora, sin cambio de modelo). `AssignRolesToUserHandler.cs:44` y `RemoveRolesToUserHandler.cs:43` envuelven la operación con `auditContext.Describe("Roles asignados a {usuario}: {roles}")` y «Roles retirados a {usuario}: {roles}»; Identity actualiza la fila del usuario y esa fila queda auditada con la descripción (sin `PasswordHash` ni `SecurityStamp`, por CHG-02).
  - Frontend: ninguno (el filtro de tabla de `app/pages/admin/audit/index.vue:27,90` es texto libre).
  - No se toca: los importadores legacy (generan una fila por registro importado, como `ProductsImporter` hoy).
- **Migración o script:** ninguno (`IAuditable` no cambia el esquema; los cambios previos no son recuperables).
- **Pruebas automatizadas nuevas:** `Wms.Tests/Domain/AuditableCatalogsTests.cs`: `[Theory] CatalogEntity_ImplementsIAuditable(Type)` con las 17 entidades; `Wms.IntegrationTests/Audit/CatalogAuditTests.cs`: `UpdatePackagingType_WritesAuditLog`, `AssignRole_WritesAuditLogWithDescription`.
- **Criterios de aceptación:**
  - Dado el Admin, cuando cambia el nombre de un embalaje, la unidad de medida y la tarifa de montacargas «Turbo», entonces la auditoría muestra un registro de actualización por cada cambio con el valor anterior y el nuevo.
  - Dado el Admin, cuando asigna el rol Facturación a un usuario, entonces la auditoría muestra «Roles asignados a {usuario}: Facturación».
- **Re-test QA:** F7-AUD-004; REG F11-REG-004.
- **Riesgo de regresión:** bajo.
- **Tamaño:** S. **Dependencias:** CHG-02.

### Fase 10 — MINOR de Comercio Exterior e inventario de Bodega

- **Objetivo:** que el Kanban y las cantidades respeten la paginación por estado y las unidades, que «Validar depósito» compare con todos los camiones, que los filtros de órdenes de cargue busquen en los depósitos, que el responsable de la recepción sea quien recibió, que los documentos muestren producto, agencia y transportadora correctos, que el inventario de Bodega muestre los Borradores con mercancía recibida (§10 · Inventario de Bodega con Borradores) y que las tarjetas de pendientes muestren el pesaje. Cierra DEF-F5-007, DEF-F5-008, DEF-F5-009, DEF-F5-012, DEF-F5-010, DEF-F4-018 y DEF-F4-015.
- **Criterio de entrada:** checkpoint de la Fase 9 aprobado.
- **Cambios:** CHG-69, CHG-70, CHG-71, CHG-72, CHG-73, CHG-74, CHG-75.
- **Orden interno:** CHG-69 → CHG-70 (ambos en `imports/[id]/index.vue`) → CHG-71 → CHG-72 → CHG-73 (ambos en `LabelGenerationService.cs` y en los detalles de depósito) → CHG-74 → CHG-75.
- **Migración de la fase (la genera el implementador con `dotnet ef`):** `AddValidationTemplateAndReceptionReceiver` (CHG-70 y CHG-72).
- **Riesgos y mitigación:**
  - Cambian los DTO de las listas de depósitos (resumen por unidad). Mitigación: el frontend se ajusta en el mismo cambio y no hay otros consumidores.
  - El relleno del receptor desde la auditoría puede dejar recepciones sin receptor. Mitigación: se muestran con «—» y la detección se entrega en el checkpoint.
- **Saneamiento de datos:** `fase-10-receptor.sql` (después de la migración) y `fase-10-terceros-documentos.sql`, descritos en cada cambio.
- **Criterio de salida:** compuertas comunes (regla 4.0.4) y en PASA: F5-LIS-001, F5-ETI-007, F5-VAL-001, F5-VAL-003, F5-OC-019, F5-CNF-001, F5-GUI-003, F5-INT-001, F4-INV-001, F4-REC-001; REG F11-REG-014, F11-REG-017, F11-REG-018, F11-REG-019, F11-REG-020.
- **Checkpoint:** se entrega al usuario el Kanban con más de 10 depósitos por columna, una guía reimpresa con producto y agencia, el inventario de Bodega con un Borrador y el resultado de las pruebas. El usuario aprueba la migración y el saneamiento en staging.

#### CHG-69 — Kanban por columna y cantidades separadas por unidad

- **Cierra:** DEF-F5-007 (MINOR).
- **Causa raíz:** `app/pages/foreign-trade/deposits/index.vue:37-47,61-69` hace una sola consulta de 10 depósitos para todos los estados y agrupa en el navegador; el contador usa `items.length` de esa página («Confirmado 0»). `GetDepositsHandler.cs:112-115` suma el stock de todos los productos y lo rotula con la unidad del primero (orden no determinista: «Bulto» en la lista, «Litro» en la tarjeta); `GetImportDepositsHandler.cs:127-131` hace lo mismo con `NationalizationBalance.ForDeposit`; la etiqueta (`LabelGenerationService.cs:183-185,701-707`) imprime como «Ampara» la suma de levantes de productos con unidades distintas (10 bultos + 3 litros = 13), y el detalle (`imports/[id]/index.vue:680,698`) rotula con una sola unidad.
- **Cambio exacto:**
  - Backend: `Wms.Application/Common/Formatting/QuantityDisplay.Summary(líneas)` agrupa por unidad y une con « + » («7 Litro + 12 Bulto»; sin líneas, «—»). `DepositKanbanDto` reemplaza `CurrentStock` y `UnitMeasure` por `StockSummary` (en `GetDepositsHandler`, `GetExportDepositsHandler.cs:38-43` y `GetInspectionDepositsHandler.cs:36-42`). `NationalizationBalance.ForDepositByUnit(...)` da un saldo por unidad y `ImportDepositDto` reemplaza sus cantidades únicas por `Balances`. `LabelGenerationService.AddProductRows`: «Ampara» consolidada solo si todos los productos comparten unidad; si no, una fila por producto con lo levantado de ese producto (regla pura `LabelAmpara.ForRows`).
  - Frontend: `deposits/index.vue` hace una consulta por columna (estado fijo, 10 por página, paginador propio) y el contador usa `pagination.totalCount` (ayudante puro `app/features/foreign-trade/utils/kanban-columns.ts`); la tarjeta muestra `stockSummary`; `ImportDepositList.vue:67-90` y el Excel de `imports/index.vue:137-155` muestran un saldo por unidad; `imports/[id]/index.vue:680,698` usan la unidad del producto de cada levante.
  - No se toca: las fórmulas por producto de `NationalizationBalance`.
- **Migración o script:** ninguno.
- **Pruebas automatizadas nuevas:** `Wms.Tests/Common/QuantityDisplayTests.cs`: `Summary_MixedUnits_KeepsUnitsSeparate`, `Summary_SameUnit_Sums`, `Summary_NoLines_ReturnsDash`; en `NationalizationBalanceTests`: `ForDepositByUnit_MixedUnits_ReturnsOneBalancePerUnit`; `Wms.Tests/ForeignTrade/LabelAmparaTests.cs`: `ForRows_MixedUnits_UsesReleasedPerProduct` (10 y 3, no 13), `ForRows_SingleUnit_Consolidates`; `test/unit/foreign-trade/kanban-columns.spec.ts`: sin filtro arma cuatro consultas, con filtro una, el contador usa el total.
- **Criterios de aceptación:**
  - Dado más de 10 depósitos confirmados, cuando CE abre el Kanban, entonces la columna «Confirmado» muestra el total real y pagina sola.
  - Dado 2026BA00004 con 12 bultos y 7 litros, cuando CE ve la lista, la tarjeta y la etiqueta, entonces leen «7 Litro + 12 Bulto» y «Ampara» trae una fila por producto.
- **Re-test QA:** F5-LIS-001, F5-ETI-007; REG F11-REG-018.
- **Riesgo de regresión:** medio (cambia el DTO de la lista de importaciones). Lo mitiga que el frontend se ajusta en el mismo cambio.
- **Tamaño:** L. **Dependencias:** CHG-43.

#### CHG-70 — «Validar depósito» compara con todos los camiones y se hace una sola vez

- **Cierra:** DEF-F5-008 (MINOR).
- **Causa raíz:** `ValidateDepositCommandHandler.cs:46-54` toma solo el último ciclo de báscula (QAB201 = 18.000 frente a 38.000 de los dos camiones) y `GetDepositValidationHandler.cs:43-58` usa otra fórmula del último ciclo y devuelve `TemplateWeight = 0` fijo (`:73`). `ImportWarehouseStorage.MarkAsValidated()` no guarda la plantilla ni impide validar de nuevo (vuelve a avisar al Admin y duplica observaciones, `:116`). La pantalla pasa el neto del último camión (`imports/[id]/index.vue:819`). El archivo del handler tiene acentos corruptos (`:28`, `:42`, `:85`, `:96-99`, `:112`): el aviso dice «Discrepancia en validaci?n de dep?sito».
- **Cambio exacto:**
  - Backend: clase pura `Wms.Application/ForeignTrade/Common/Services/DepositValidationMath.cs`: `RegisteredWeight(entradas)` = Σ neto físico de las entradas no anuladas; `Compare(plantilla, registrado, cantidadPlantilla, cantidadRegistrada)` con la tolerancia actual del 5 %. `ValidateDepositCommandHandler` incluye las entradas del depósito y, si ya fue validado, lanza `ConflictException("El depósito {número} ya fue validado el {dd/MM/yyyy HH:mm}.")` antes de avisar (el código ya define la validación como única); `ImportWarehouseStorage.MarkAsValidated(pesoPlantilla, cantidadPlantilla)` guarda la plantilla; la observación usa `ColombiaTime.Now`; se restauran los acentos. `GetDepositValidationHandler` usa el mismo cálculo y devuelve la plantilla guardada; `ValidationInfoDto` suma `TemplateQuantity`.
  - Frontend: `imports/[id]/index.vue:819` deja de pasar `registered-weight` y `registered-quantity` (el formulario usa `validation-info`); `IValidationInfoDto` suma `templateQuantity`.
  - No se toca: la tolerancia del 5 %.
- **Migración o script:** `AddValidationTemplateAndReceptionReceiver` (de la fase): `import_warehouse_storages.template_weight` y `template_quantity` (`numeric(18,4)`, nulas, sin valor por defecto). Sin saneamiento (los validados antes quedan con plantilla nula).
- **Pruebas automatizadas nuevas:** `Wms.Tests/ForeignTrade/DepositValidationMathTests.cs`: `RegisteredWeight_TwoTrucks_SumsAll` (20.000 + 18.000 = 38.000), `RegisteredWeight_IgnoresVoidedEntries`, `RegisteredWeight_NullNetWeight_CountsZero`, `Compare_TemplateEqualsRegistered_NoDifference`, `Compare_AboveFivePercent_FlagsDifference` (38.000 frente a 18.000), `Compare_ExactlyFivePercent_NoDifference` (18.900 frente a 18.000); `Wms.Tests/Domain/ForeignTrade/ImportWarehouseStorageValidationTests.cs`: `MarkAsValidated_StoresTemplate`, `MarkAsValidated_Twice_ThrowsConflict`.
- **Criterios de aceptación:**
  - Dado un depósito con dos camiones (20.000 y 18.000 kg), cuando CE valida con una plantilla de 38.000, entonces no hay diferencia y el depósito queda validado con su plantilla.
  - Dado el mismo depósito validado, cuando CE intenta validar de nuevo, entonces responde 409 «El depósito 2026BA00012 ya fue validado el 02/10/2026 10:15.» y no llega otro aviso al Admin.
- **Re-test QA:** F5-VAL-001, F5-VAL-003; REG F11-REG-017.
- **Riesgo de regresión:** bajo.
- **Tamaño:** M. **Dependencias:** CHG-69.

#### CHG-71 — Los filtros de órdenes de cargue buscan en los depósitos de la orden

- **Cierra:** DEF-F5-009 (MINOR).
- **Causa raíz:** `GetLoadingOrdersHandler.cs:50-62` filtra el documento comercial y el manifiesto DIAN por `lo.ServiceRecord`, que nunca se asigna (`LoadingOrder.cs:122` lo deja nulo y `ExecuteLoadingOrderCommandHandler.cs:143` llama `StartLoading()` sin argumento), y el importador por el cliente de la orden (`:50-51`), no por el importador del depósito. El selector de depósitos (`GetLoadingOrderDepositsHandler.cs:69-80`) tiene las ramas cruzadas: «Manifiesto DIAN» busca la carta porte y «Documento comercial» los documentos adicionales.
- **Cambio exacto:**
  - Backend: búsqueda compartida `Wms.Application/ForeignTrade/Common/Queries/LoadingOrderStorageSearch.ApplyStorageSearch(depósitos, campo, valor)`: «Importador» = importador del depósito (rol IMPORTER) o cliente de la orden; «Documento comercial» = carta porte (`CargoManifestNumber`) o documentos del servicio; «Manifiesto DIAN» = `ImportWarehouseStorage.ManifestNumber`. El listado de órdenes filtra las que tienen ítems en esos depósitos y el selector de depósitos usa la misma búsqueda.
  - Frontend: ninguno.
  - No se toca: los filtros por número de orden, placa, depósito, fecha, producto y transportadora.
- **Migración o script:** ninguno.
- **Pruebas automatizadas nuevas:** `Wms.IntegrationTests/ForeignTrade/LoadingOrderSearchTests.cs`: `Search_CommercialDoc_QA_CP_0401_ReturnsOrdersOfThatDeposit` (2026OC00011 y 2026OC00014), `Search_Importer_Andina_ReturnsOrdersOfThatDeposit`, `Search_DianManifest_QA_DIAN_002_ReturnsOrdersOfThatDeposit`, `Search_PendingOrderWithoutServiceRecord_StillMatches`.
- **Criterios de aceptación:**
  - Dado las órdenes de 2026BA00004, cuando CE filtra por documento comercial «QA-CP-0401», entonces aparecen 2026OC00011 y 2026OC00014.
  - Dado el filtro de importador «Andina», cuando CE busca, entonces aparecen las órdenes de los depósitos de QA Importación Andina Ltda.
- **Re-test QA:** F5-OC-019; REG F11-REG-019.
- **Riesgo de regresión:** bajo.
- **Tamaño:** M. **Dependencias:** CHG-32.

#### CHG-72 — El responsable de la recepción es quien recibió en Bodega

- **Cierra:** DEF-F5-012 (MINOR).
- **Causa raíz:** `GetImportDepositDetailHandler.cs:222` toma como responsable a `EntryLog.EntryAuthorizedBy` (Vigilancia) porque `ReceptionLog` no guarda quién recibió. Las cantidades del bloque (`:215-224`) suman lo declarado de todos los productos y camiones contra la última recepción, con unidades mezcladas (19 − 2 = −17).
- **Cambio exacto:**
  - Backend: `ReceptionLog.ReceivedById` (nulo, FK a `users`, `Restrict`) y `Complete(receivedById, …)`; lo asignan `CompleteReceptionCommandHandler.cs:184` y `CreateReceptionCommandHandler.cs:273` con el usuario autenticado y `CreateReceptionWithoutWeighbridgeCommandHandler.cs:283` con su autor. `GetImportDepositDetailHandler.cs:219-224` toma el nombre de ese usuario y arma las cantidades con `ReceptionDeclaredDifference.ForTruck` de la última recepción: `DepositWarehouseReceptionDto` suma `Lines` (producto, unidad, amparada, recibida, diferencia) y conserva los totales solo con una unidad.
  - Frontend: `DepositDetailWarehouseReceptionCard.vue` e `IDepositWarehouseReceptionDto` muestran una fila por línea con su unidad.
  - No se toca: `EntryLog.EntryAuthorizedBy` (sigue siendo el responsable del ingreso en «Transporte»).
- **Migración o script:** `AddValidationTemplateAndReceptionReceiver` (de la fase): `reception_logs.received_by_id uuid` nulo, FK a `users(id)` `ON DELETE RESTRICT` e índice. `fase-10-receptor.sql`, después de la migración: detección de recepciones completadas sin receptor y relleno desde `audit_logs` (último usuario que completó la descarga de cada recepción); en producción, solo con aprobación del usuario.
- **Pruebas automatizadas nuevas:** `Wms.Tests/Domain/Warehouse/ReceptionLogTests.cs`: `Complete_SetsReceivedBy`; en `ReceptionDeclaredDifferenceTests`: `ForTruck_TwoUnits_KeepsLinesSeparate`; `Wms.IntegrationTests/ForeignTrade/GetImportDepositDetailHandlerTests.cs`: `Handle_CompletedReception_ReturnsBodegaUser_NotVigilancia`.
- **Criterios de aceptación:**
  - Dado una recepción completada por el usuario de Bodega, cuando CE abre el detalle del depósito, entonces «Responsable» muestra a ese usuario, no al de Vigilancia.
  - Dado un camión con 12 bultos y 7 litros, cuando CE ve el bloque de recepción, entonces ve una línea por producto con su unidad y su diferencia.
- **Re-test QA:** F5-CNF-001 (detalle); REG F11-REG-014.
- **Riesgo de regresión:** bajo.
- **Tamaño:** M. **Dependencias:** CHG-70, CHG-56.

#### CHG-73 — Guía, factura y etiqueta muestran el producto, la agencia y la transportadora correctos

- **Cierra:** DEF-F5-010 (MINOR).
- **Causa raíz:** `DispatchGuidePdfService.cs:477-481` usa `wsp.ProductDescription ?? wsp.Product?.Name`, pero `LoadGuideContextAsync` (`:91-143`) no incluye `Product`: al reimprimir sale «N/A» (53 de 57 descripciones son nulas); igual en `GetPendingImportLoadingOrdersHandler.cs:70-71`, `GetPendingGuidesQuery.cs:74` y `LoadingOrderPdfService.cs:142`. La firma impresa cae al cliente (`:582`). `StorageBillingService.cs:25,774` busca la agencia por el nombre «Agencia de Aduanas» y el catálogo dice «Agencia de aduanas» (`SeedDataExtensions.cs:140`): «AGENCIA:N/A» en 33 facturas. `LabelGenerationService.cs:67-70` y `:292-295` toman como intermediario el primer tercero que no es importador ni transportadora y entra el cliente. La transportadora vacía (`DispatchGuidePdfService.cs:263-271,407-408`) es de datos: QAE002 y QAE017 no tienen transportadora.
- **Cambio exacto:**
  - Backend: `DispatchGuidePdfService` incluye `Items → WarehouseStorageProduct → Product` junto a `:132-136` e imprime `SignerName` sin respaldo al cliente (`:582`); el mismo `Include` en `GetPendingImportLoadingOrdersHandler`, `GetPendingGuidesQuery` y `LoadingOrderPdfService`. Clase pura `CustomsAgencyResolver` (cascada CUSTOMS_AGENCY → INTERMEDIARY → IMPORT_AGENCY → la heurística actual de `DispatchGuidePdfService.cs:647-661`, desempate por fecha), usada por las tres etiquetas, la guía y `DepositPdfService.cs:95-103`. `StorageBillingService.cs:774` filtra por `RoleType.Code == "CUSTOMS_AGENCY"` y se borra la constante de nombre. Clase pura `GuideCarrierText`: transportadora del vehículo de la orden, luego la de los vehículos de los ingresos y luego el rol TRANSPORT_COMPANY; sin ninguna imprime «—».
  - Frontend: ninguno.
  - No se toca: `DocumentProductLine` ni las reglas de firmante de CHG-34.
- **Migración o script:** sin migración. `fase-10-terceros-documentos.sql`, en la base local y en staging: firmante = importador en las guías con un solo importador y firmante «Importador»; «AGENCIA:N/A» reemplazado por la agencia en las facturas en Borrador o Pendiente de aprobación no consolidadas. Las facturas emitidas se corrigen en SIIGO. Los vehículos QAE002 y QAE017 reciben su transportadora desde el catálogo.
- **Pruebas automatizadas nuevas:** `Wms.Tests/ForeignTrade/CustomsAgencyResolverTests.cs`: `Resolve_CustomerListedFirst_ReturnsCustomsAgency`, `Resolve_NoAgency_ReturnsNull`, `Resolve_IntermediaryFallback_WhenNoCustomsAgency`; `Wms.Tests/Billing/StorageInvoiceDetailFormatterTests.cs`: `Build_WithAgency_PrintsAgencyName` («AGENCIA:QA Agencia SIA Aduanas»), `Build_WithoutAgency_PrintsNA`; `Wms.Tests/ForeignTrade/GuideCarrierTextTests.cs`: `OrderVehicleCarrierFirst`, `NoCarrierAnywhere_PrintsDash`; `Wms.IntegrationTests/ForeignTrade/GuideReprintTests.cs`: `Reprint_ShowsProductNameNotNA`.
- **Criterios de aceptación:**
  - Dado la guía 2026S00007, cuando CE la reimprime, entonces el producto dice «QA Cebolla» y no «N/A».
  - Dado un depósito con agencia QA Agencia SIA Aduanas, cuando se abre su período de almacenamiento, entonces el detalle de la factura dice «AGENCIA:QA Agencia SIA Aduanas».
  - Dado 2026BA00004, cuando CE imprime la etiqueta, entonces «Intermediario» es la agencia, no el cliente.
- **Re-test QA:** F5-GUI-003, F5-INT-001; REG F11-REG-020.
- **Riesgo de regresión:** bajo.
- **Tamaño:** M. **Dependencias:** CHG-34, CHG-35, CHG-66.

#### CHG-74 — El inventario de Bodega muestra los Borradores con mercancía recibida

- **Cierra:** DEF-F4-018 (MINOR).
- **Causa raíz:** `WarehouseController.GetWarehouseDeposits` (`:1078-1099`) reutiliza `GetLoadingOrderDepositsQuery`, el listado de CE para órdenes de cargue, cuyo handler excluye Borrador y exige cliente (`GetLoadingOrderDepositsHandler.cs:30-35`); la pantalla busca el depósito en esa lista (`app/pages/warehouse/inventory/index.vue:46-70`).
- **Cambio exacto (aplica §10 · Inventario de Bodega con Borradores):**
  - Backend: `GetLoadingOrderDepositsQuery.IncludeReceivedDrafts`; con él, el handler incluye los Borradores activos con al menos una recepción activa Completed en una entrada no anulada (la noción de `GetImportDepositDetailHandler.cs:204-209`) y no exige cliente («Sin cliente» en la proyección, `:102-103`). `WarehouseController.cs:1088-1095` lo activa; `ForeignTradeController.cs:933` no (CE sigue sin ver Borradores para cargue).
  - Frontend: `inventory/index.vue` (cerca de `:352`) muestra la etiqueta «Borrador» y «Comercio Exterior aún no lo confirma.»; `WarehouseDepositSelect.vue:55-57` agrega « (Borrador)».
  - No se toca: `GET inventory/stock/{id}`.
- **Migración o script:** ninguno.
- **Pruebas automatizadas nuevas:** `Wms.IntegrationTests/Warehouse/WarehouseDepositsListTests.cs`: `GetWarehouseDeposits_DraftWithCompletedReception_IsListed`, `GetWarehouseDeposits_DraftWithInProgressReception_IsNotListed`, `GetWarehouseDeposits_DraftWithoutCustomer_ShowsSinCliente`, `GetWarehouseDeposits_CancelledWithCompletedReception_IsNotListed`, `GetLoadingOrderDeposits_DraftWithCompletedReception_IsNotListed`.
- **Criterios de aceptación:**
  - Dado 2026BA00008 en Borrador con su recepción completada, cuando Bodega abre el inventario, entonces lo encuentra con la etiqueta «Borrador» y su stock.
  - Dado el mismo depósito, cuando CE crea una orden de cargue, entonces no aparece en el selector.
- **Re-test QA:** F4-INV-001; REG F11-REG-014.
- **Riesgo de regresión:** bajo.
- **Tamaño:** M. **Dependencias:** CHG-08.

#### CHG-75 — Las tarjetas de pendientes muestran el pesaje real

- **Cierra:** DEF-F4-015 (MINOR).
- **Causa raíz:** `app/pages/warehouse/receptions/entry.vue:184-188` lee `firstWeight` y `firstWeightCapturedAt`, que declara `app/features/warehouse/types/reception.ts:274-276`, pero el API envía `entryWeight`, `entryWeightType` y `entryCapturedAt` (`PendingFromWeighbridgeDto.cs:25-27`): «kg (Invalid Date)». El mismo desajuste existe en la búsqueda por placa (`reception.ts:165-166` frente a `PlateSearchResultDto.cs:23-24`; `warehouse-service.ts:141,143`), que oculta el peso en `ReceptionStepCompletion.vue:362`.
- **Cambio exacto:**
  - Backend: ninguno.
  - Frontend: `reception.ts:274-276` → `entryWeight`, `entryWeightType`, `entryCapturedAt`; `entry.vue:185-187` y `PendingFromWeighbridgeList.vue:189-200` usan esos campos con `formatColombiaDateTime` (texto «Pesaje 12.345 kg (03/10/2026 08:15)») mediante `formatPendingWeighing` (`app/features/warehouse/utils/pending-weighing.ts`); `warehouse-service.ts:141,143` mapea `firstWeight: data.entryWeight ?? null` y `netWeight: data.physicalNetWeight ?? null`.
  - No se toca: los DTO del API.
- **Migración o script:** ninguno.
- **Pruebas automatizadas nuevas:** `test/unit/warehouse/pending-weighing.spec.ts`: `{ entryWeight: 12345, entryCapturedAt: "2026-10-03T13:15:00+00:00" }` → «12.345 kg (03/10/2026 08:15)»; sin pesaje (0 y `0001-01-01`) → «—».
- **Criterios de aceptación:**
  - Dado QAA101 pesado a las 08:15 con 12.345 kg, cuando Bodega abre «Ingresos», entonces la tarjeta dice «Pesaje 12.345 kg (03/10/2026 08:15)».
- **Re-test QA:** F4-REC-001; REG F11-REG-014.
- **Riesgo de regresión:** bajo.
- **Tamaño:** S. **Dependencias:** CHG-36.

### Fase 11 — MINOR de reportes, fechas y documentos impresos

- **Objetivo:** que el historial, el tablero y el reporte diario de báscula cuadren; que los filtros y las exportaciones usen el día y la hora de Colombia; que movimientos y kárdex se exporten completos; que los reportes de salidas, ingresos (§10 · Reporte de ingresos diarios) y estadísticas muestren lo que corresponde; que la trazabilidad filtre por el día de Colombia y por placa sin distinguir mayúsculas; y que los documentos impresos tengan detalle, contacto real y una sola fuente de datos de la empresa. Cierra DEF-F3-015, DEF-F8-009, DEF-F4-007, DEF-F4-008, DEF-F7-009, DEF-F7-003, DEF-F7-012, DEF-F7-010, DEF-F7-004, DEF-F7-006 y DEF-F7-011.
- **Criterio de entrada:** checkpoint de la Fase 10 aprobado.
- **Cambios:** CHG-76, CHG-77, CHG-78, CHG-79, CHG-80, CHG-81, CHG-82, CHG-83, CHG-84.
- **Orden interno:** CHG-76 → CHG-77 (el tablero de báscula ya no envía fechas) → CHG-78 → CHG-79 → CHG-80 → CHG-81 → CHG-82 → CHG-83 (después del kárdex, mismo `warehouse-movements.vue`) → CHG-84 (después de CHG-82, mismo `DailyIncomingGoodsPdfService.cs`).
- **Migración de la fase (la genera el implementador con `dotnet ef`):** `SeedCompanyParameters` (CHG-84).
- **Riesgos y mitigación:**
  - El enlazador de fechas cambia cómo se leen todas las fechas de consulta. Mitigación: pruebas del parser y re-test de los filtros de recepciones, montacargas, historial de báscula, depósitos y facturas.
  - CHG-84 toca ocho PDF. Mitigación: con los valores sembrados, los pies reproducen el texto actual; se comparan los PDF antes y después.
- **Saneamiento de datos:** `fase-11-parametros-empresa.sql` (solo detección, antes de la migración).
- **Criterio de salida:** compuertas comunes (regla 4.0.4) y en PASA: F3-HIS-001, F3-HIS-005, F3-DSH-001, E2E-20, F4-REC-015, F4-INV-003, F7-REP-012, F7-REP-013, F7-REP-003, F7-TRZ-006, F7-TRZ-002, F7-TRZ-003, F7-NOT-008, F7-REP-001, F7-REP-019, F7-PDF-001, F7-PDF-004, F7-PDF-007; REG F11-REG-006, F11-REG-009, F11-REG-012, F11-REG-014, F11-REG-017, F11-REG-020, F11-REG-028.
- **Checkpoint:** se entrega al usuario un juego de documentos impresos (factura, tiquete, guía y reportes diarios), los Excel exportados con horas de Colombia y el tablero de báscula frente al reporte diario. El Admin confirma en `admin/parameters` los datos oficiales de la empresa (sembrados con el pie del legacy).

#### CHG-76 — Historial, tablero y reporte diario de báscula cuadran entre sí

- **Cierra:** DEF-F3-015 (MINOR), DEF-F8-009 (MINOR).
- **Causa raíz:**
  - DEF-F3-015 (parcialmente; el contador «Entradas» del historial cuenta, por definición, solo ciclos terminales, `WeighbridgeHistoryFilters.cs:77-80`): `WeighingTotals.cs:15-16` devuelve todo nulo con menos de dos pesajes, así que una operación de un solo pesaje (INSP, perecedero, Solo báscula) muestra «—» y «Pendiente» (`GetWeighbridgeHistoryHandler.cs:166-188`, `GetWeighbridgeHistoryTotalsHandler.cs:45`, `WeighbridgeHistoryTable.vue:429-438`). El tablero (`useWeighbridgeDashboard.ts`) arma sus cifras con el historial terminal («Ciclos hoy» 8 frente a 11 del reporte; «En proceso» siempre 0) y con `GetPendingSecondWeightHandler.cs:37-38`, que excluye salidas y Solo báscula que la cola sí muestra.
  - DEF-F8-009: `GetDailyBillingReportHandler.cs:54-56` rotula «Solo Pesaje» todo `Input` con `SingleWeightOnly`, que también fijan INSP y perecederos; los conteos de `:93-96` y `:109-121` arrastran el error y la consulta no trae la modalidad (`:23-47`).
- **Cambio exacto:**
  - Backend: `WeighingTotals.From(pesajes, ciclo completo)`: con un solo pesaje y ciclo completo, bruto o tara según su tipo y neto = ese peso (la convención de `ModifyFirstWeightHandler.cs:70-72`); con dos o más, como hoy. La usan `GetWeighbridgeHistoryHandler` y `GetWeighbridgeHistoryTotalsHandler` (la sobrecarga actual se conserva para `GetCustomsAgencyEntryDetailHandler.cs:65`). Consulta nueva `GET weighbridge/dashboard` (`WeighbridgeController.cs`, junto a `queue`): ciclos de hoy y completados de hoy con la ventana del día de Colombia del reporte diario; «En proceso» y «Pendientes repesaje» agrupando la cola (`WeighbridgeDashboardCounts.FromQueue`). Clase pura `DailyBillingServiceKind.Resolve(tipo, modalidad)`: «Salida» para `OutputCargo`, «Solo Pesaje» para `Input` con modalidad `OTH*`, «Ingreso» para el resto; el reporte incluye la modalidad y deriva de ella los conteos (Ingreso + Salida + Solo Pesaje = total de ciclos).
  - Frontend: `weighbridge-service.ts` (`getWeighbridgeDashboard`) y `useWeighbridgeDashboard.ts` con una sola consulta (`["weighbridge","dashboard"]`, cada 30 s); `app/pages/operations/weighbridge/dashboard.vue:15-47` con las cuatro cifras y sus enlaces.
  - No se toca: el filtro terminal del historial, `GetPendingSecondWeightHandler` ni la etiqueta «Solo Pesaje».
- **Migración o script:** ninguno (se calcula en cada consulta).
- **Pruebas automatizadas nuevas:** en `Wms.Tests/Weighbridge/WeighingTotalsTests.cs`: `SingleWeighingComplete_Gross_ReportsGrossAndNet` (30.000 → bruto 30.000, neto 30.000), `SingleWeighingComplete_Tare_ReportsTareAndNet`, `SingleWeighingNotComplete_HasNoWeights`, `TwoWeighings_KeepCurrentBehavior`; `Wms.Tests/Weighbridge/WeighbridgeDashboardCountsTests.cs`: `FromQueue_CountsByState` (2 por repesar, 1 listo, 1 por cobrar, 1 sin iniciar → en proceso 3, por repesar 2), `FromQueue_Empty_IsZero`; `Wms.Tests/Weighbridge/DailyBillingServiceKindTests.cs`: `Resolve_InspectionDepositSingleWeight_IsIngreso`, `Resolve_WeighingOnlyModality_IsSoloPesaje`, `Resolve_ImportAndExport_AreIngreso`, `Resolve_Output_IsSalida`, `Resolve_NullModality_IsIngreso`.
- **Criterios de aceptación:**
  - Dado la inspección de pesaje único de QAC404 con 30.000 kg, cuando báscula abre el historial, entonces ve bruto 30.000 y neto 30.000.
  - Dado un día con 11 ciclos (8 terminados y 3 abiertos), cuando báscula abre el tablero, entonces «Ciclos hoy» dice 11 y «En proceso» y «Pendientes repesaje» coinciden con la cola.
  - Dado el reporte diario de ese día, cuando báscula lo abre, entonces la inspección figura como «Ingreso» y Ingreso + Salida + Solo Pesaje = 11.
- **Re-test QA:** F3-HIS-001, F3-HIS-005, F3-DSH-001, E2E-20; REG F11-REG-009, F11-REG-012.
- **Riesgo de regresión:** bajo.
- **Tamaño:** M. **Dependencias:** CHG-36, CHG-37.

#### CHG-77 — Los filtros por fecha usan el día de Colombia y no responden 500

- **Cierra:** DEF-F4-007 (MINOR).
- **Causa raíz:** el frontend envía los dos límites con `toISOString()` de la medianoche local (`app/features/warehouse/components/ReceptionList.vue:56-57`; igual en `ForkliftUseList.vue:92-93`, `WeighbridgeHistoryTable.vue:98-99`, `DepositFiltersPanel.vue:122-125`, `app/pages/foreign-trade/deposits/index.vue:41-42`), así que «desde» = «hasta» y no hay filas. El backend compara el `DateTimeOffset` tal como llega (`GetReceptionsHandler.cs:29-37` y otras 14 consultas); Npgsql solo acepta desfase 0, de ahí el 500 con `-05:00`. `UtcDateTimeOffsetNormalizer` (`AppDbContext.cs:127`) solo actúa al guardar.
- **Cambio exacto:**
  - Backend: `ColombiaTime.EndOfDayUtc(fecha)`; clase pura `Wms.Common/Time/QueryInstantParser.TryParse(texto, finDelDía, out utc)` (`yyyy-MM-dd` → inicio o fin del día de Colombia; fecha y hora sin zona → hora de Colombia; con zona → el mismo instante en UTC) e `IsUpperBoundName(nombre)` (`To`, `ToDate`, `DateTo`); nuevo `Wms.Api/Common/ModelBinding/ColombiaDateTimeOffsetModelBinder.cs` (con su proveedor, insertado primero en `Program.cs`) para todo `DateTimeOffset` de la query: vacío → `null`; inválido → `BadRequestException("La fecha «{campo}» no es válida. Use AAAA-MM-DD o AAAA-MM-DDThh:mm:ss-05:00.")`.
  - Frontend: `app/utils/colombia-date.ts` suma `toColombiaStartOfDayIso(fecha)` y `toColombiaEndOfDayIso(fecha)` (`…T00:00:00.000-05:00` y `…T23:59:59.999-05:00`), usados en los cinco puntos citados, en `buildDayRange` de `app/pages/billing/invoices/index.vue:49-59` y en `endOfDay` de `app/pages/reports/warehouse-movements.vue:78-87`.
  - No se toca: los endpoints con `DateOnly`, `GetInvoicesHandler`, `UtcDateTimeOffsetNormalizer` ni `useWeighbridgeDashboard.ts` (desde CHG-76 ya no envía fechas).
- **Migración o script:** ninguno.
- **Pruebas automatizadas nuevas:** `Wms.Tests/Common/QueryInstantParserTests.cs`: `TryParse_DateOnlyFrom_ReturnsColombiaMidnightInUtc` («2026-10-02» → `2026-10-02T05:00:00Z`), `TryParse_DateOnlyTo_ReturnsLastTickOfColombiaDay`, `TryParse_OffsetMinus5_NormalizesToUtc`, `TryParse_Zulu_KeepsInstant`, `TryParse_DateTimeWithoutZone_IsColombiaTime`, `TryParse_ToDateWithExplicitTime_IsNotExtended`, `TryParse_Invalid_ReturnsFalse`, `IsUpperBoundName_RecognizesUpperBounds`; `test/unit/utils/colombia-date.spec.ts`: inicio y fin del 03/10/2026, relleno de ceros y diferencia de 86.399.999 ms; `Wms.IntegrationTests/Warehouse/ReceptionDateFilterTests.cs`: `GetReceptions_SameDayWithColombiaOffset_Returns200AndThatDay`.
- **Criterios de aceptación:**
  - Dado recepciones del 02/10/2026, cuando Bodega filtra el historial desde el 02/10 hasta el 02/10, entonces aparecen las de ese día.
  - Dado `GET warehouse/receptions?fromDate=2026-10-02T00:00:00-05:00`, cuando se envía, entonces responde 200; con `fromDate=hoy`, responde 400 con el mensaje de formato.
- **Re-test QA:** F4-REC-015; REG F11-REG-014.
- **Riesgo de regresión:** medio (cambia cómo se leen todas las fechas de consulta). Lo mitigan las pruebas del parser y la integración.
- **Tamaño:** M. **Dependencias:** CHG-48, CHG-76.

#### CHG-78 — Movimientos y kárdex se exportan completos y se ven sin expandir

- **Cierra:** DEF-F4-008 (MINOR), DEF-F7-009 (MINOR).
- **Causa raíz:**
  - DEF-F4-008: `WarehouseController.cs:991-1018` (`GetInventoryMovements`) no declara `all`, así que el Excel recibe solo la primera página aunque el frontend envía `all=true` (`useWarehouseExports.ts:27`); la columna «Usuario» lee campos que el API no envía (`useWarehouseExports.ts:43,45`).
  - DEF-F7-009: `app/pages/reports/warehouse-movements.vue:154-215` (`onExportExcel`) solo arma las hojas Productos, Levantes y Despachos; en pantalla las líneas existen dentro de una fila expandible cerrada por defecto (`:129`, `:446-500`) y sin «Origen» ni «Usuario». El API ya devuelve los movimientos (`GetWarehouseStorageMovementsHandler.cs:77-91,194-246`).
- **Cambio exacto:**
  - Backend: `GetInventoryMovements` recibe `[FromQuery(Name = "all")] bool all = false` y asigna `All`.
  - Frontend: `useWarehouseExports.ts:43,45` usa `authorizedByUser` y `reason` (tipo `IInventoryMovement` ajustado; columnas extraídas a `app/features/warehouse/utils/inventory-export-columns.ts`); `app/features/reports/utils/kardex-movements.ts` (`buildKardexMovementRows`) aplana los movimientos con las etiquetas de `inventory-labels.ts` (CHG-39); `onExportExcel` agrega la hoja «Movimientos» (Producto, Fecha, Tipo, Origen, Cantidad, Stock anterior, Stock nuevo, Placa, Tiquete, Guía, Usuario, Motivo); la pantalla expande todas las filas al cargar y suma «Origen» y «Usuario».
  - No se toca: el PDF, los totales ni las hojas de levantes y despachos.
- **Migración o script:** ninguno.
- **Pruebas automatizadas nuevas:** `Wms.IntegrationTests/Warehouse/InventoryMovementsTests.cs`: `GetInventoryMovements_AllTrue_ReturnsAllRows` (30 movimientos → 30 filas), `GetInventoryMovements_WithoutAll_ReturnsPageSize20`; `test/unit/warehouse/inventory-export-columns.spec.ts`: «Usuario» usa `authorizedByUser`, «Motivo» usa `reason`; `test/unit/reports/kardex-movements.spec.ts`: BA00001 aplanado en orden con «Entrada», «Salida» e «Ingreso declarado», sin movimientos devuelve vacío, fecha con respaldo a `createdAt`.
- **Criterios de aceptación:**
  - Dado 30 movimientos, cuando Bodega exporta a Excel, entonces el archivo trae las 30 filas con el usuario y el motivo.
  - Dado el kárdex de 2026BA00001, cuando CE lo abre y lo exporta, entonces ve las líneas sin expandir (con origen y usuario) y el Excel trae la hoja «Movimientos».
- **Re-test QA:** F4-INV-003, F7-REP-012, F7-REP-013; REG F11-REG-014.
- **Riesgo de regresión:** bajo.
- **Tamaño:** M. **Dependencias:** CHG-39, CHG-77.

#### CHG-79 — El reporte de salidas diarias incluye los despachos sin guía

- **Cierra:** DEF-F7-003 (MINOR).
- **Causa raíz:** `GetDailyOutgoingGoodsReportHandler.cs:39,66-72` parte de `DispatchGuides` y exige guía vigente, y `:106` expande por guía: una orden despachada sin guía (las de inspección, que nunca la tienen, `GuideType.cs:18-21`, y las de importación históricas) no aparece. `FindWspId` (`:188`, `:257-272`) empareja por número de guía, depósito y nombre del producto, y falla con guía nula o con dos productos del mismo nombre.
- **Cambio exacto:**
  - Backend: el handler parte de `LoadingOrders` despachadas o completas, con fecha efectiva = salida de la orden, o salida de la guía vigente, o fin del cargue, dentro del rango; la guía de la fila es la vigente más reciente (puede faltar); orden por fecha, guía (sin guía al final) y orden; cada fila nace con su producto y se elimina `FindWspId`. `DailyOutgoingGoodsReportRowDto` hace `GuideNumber` anulable y suma `LoadingOrderNumber` y `HasGuide`; `DailyOutgoingGoodsPdfService.cs:175` imprime «Sin guía ({orden})». Reglas puras en `OutgoingGoodsRowRules` (`EffectiveDate`, `GuideLabel`).
  - Frontend: `app/features/reports/types/daily-outgoing-goods.ts` con los campos nuevos; `app/pages/reports/daily-outgoing-goods.vue:309-314` muestra el número o la etiqueta «Sin guía» con la orden.
  - No se toca: el cálculo de levantes (`:171-182`) ni `GetOperationalStatisticsHandler.cs:190-196`.
- **Migración o script:** ninguno.
- **Pruebas automatizadas nuevas:** `Wms.Tests/Reports/OutgoingGoodsRowRulesTests.cs`: `EffectiveDate_PrefersOrderDeparture`, `EffectiveDate_FallsBackToGuideThenLoadingEnd`, `GuideLabel_WithoutGuide_ReturnsSinGuiaWithOrderNumber` («Sin guía (2026OC00017)»); `Wms.IntegrationTests/Reports/DailyOutgoingGoodsTests.cs`: `Report_InspectionOrderWithoutGuide_IsIncluded`.
- **Criterios de aceptación:**
  - Dado la orden de inspección 2026OC00017 despachada el 02/10/2026, cuando CE abre el reporte de salidas de ese día, entonces aparece con «Sin guía (2026OC00017)» y su cantidad.
- **Re-test QA:** F7-REP-003; REG F11-REG-020.
- **Riesgo de regresión:** bajo.
- **Tamaño:** M. **Dependencias:** CHG-33, CHG-35.

#### CHG-80 — Las estadísticas de facturación solo llegan al Admin

- **Cierra:** DEF-F7-012 (MINOR).
- **Causa raíz:** `ReportController.cs:155-162` (`GetOperationalStatistics`, política de clase `ForeignTradeAccess`, `:21`) no pasa el rol y `GetOperationalStatisticsHandler.cs:20,27` calcula y devuelve siempre el bloque `Billing` (`OperationalStatisticsDto.cs:8`); `app/pages/reports/statistics.vue:239`, `:317-354` y `:356-375` lo muestran a CE (solo el tablero `/` lo oculta, `TraceabilityStats.vue:10-14`).
- **Cambio exacto:**
  - Backend: clase pura `Wms.Application/Reports/Common/StatisticsVisibility.IncludesBilling(roles)` = contiene Admin; `GetOperationalStatisticsQuery(Period, IncludeBilling)` desde `ReportController.cs:160`; el handler calcula `Billing` solo con `IncludeBilling` y `OperationalStatisticsDto.Billing` pasa a anulable sin valor por defecto.
  - Frontend: `app/features/reports/types/index.ts:4` → `billing: IBillingStatistics | null`; `statistics.vue` importa `usePermissions` y `ROLES`; el KPI «Facturado» y las secciones de facturación (`:232-242`, `:317-354`, `:356-375`) llevan `v-if="isAdmin && data.billing"`; los gráficos de facturación (`:111-122`, `:131-134`) devuelven `null` sin datos; la rejilla usa tres columnas sin Admin.
  - No se toca: `TraceabilityStats.vue` ni `billing/dashboard/summary` (`BillingAccess`).
- **Migración o script:** ninguno.
- **Pruebas automatizadas nuevas:** `Wms.Tests/Reports/StatisticsVisibilityTests.cs`: `IncludesBilling_Admin_ReturnsTrue`, `IncludesBilling_ForeignTradeOnly_ReturnsFalse`, `IncludesBilling_BillingAndForeignTrade_ReturnsFalse`, `IncludesBilling_AdminAndForeignTrade_ReturnsTrue`; `Wms.IntegrationTests/Reports/OperationalStatisticsTests.cs`: `ForeignTrade_ReceivesNullBilling`.
- **Criterios de aceptación:**
  - Dado `c_exterior`, cuando abre `/reports/statistics` o llama `GET reports/operational-statistics`, entonces `billing` es `null` y la página no muestra «Facturado» ni las secciones de facturación.
  - Dado el Admin, cuando abre la misma página, entonces ve las secciones de facturación.
- **Re-test QA:** F7-TRZ-006; REG F11-REG-028.
- **Riesgo de regresión:** bajo.
- **Tamaño:** S. **Dependencias:** CHG-03.

#### CHG-81 — Trazabilidad: «Hoy» de Colombia, placa sin distinguir mayúsculas y aviso en español

- **Cierra:** DEF-F7-010 (MINOR).
- **Causa raíz:** `GetTraceabilityDashboardHandler.cs:20-21` y `:192-203` calculan «hoy» como la medianoche UTC (19:00 del día anterior en Colombia); `:40-41` filtra la placa con `Contains`, que distingue mayúsculas en PostgreSQL («qaa10» → 0); la búsqueda de la barra superior (`app/components/layout/AppTopbar.vue:24-30`) abre el tablero con «Hoy» (`app/pages/index.vue:17`, `:23-28`) y no encuentra el camión de ayer; el título «TraceabilityUpdated» se repite en 17 métodos `NotifyTraceabilityUpdateAsync` (p. ej. `CreateEntryLogHandler.cs:154`, `RegisterDepartureHandler.cs:93`, `InitiateStorageWeighingHandler.cs:1316`) y el aviso lo muestra tal cual (`useNotifications.ts:72-76`).
- **Cambio exacto:**
  - Backend: clase pura `TraceabilityDateRange.For(filtro, hoy)`: `day` (el día de Colombia), `week` (desde el lunes), `month` (desde el día 1) y `all` (sin fecha); otro valor se toma como `day`. El handler la usa con `ColombiaTime.Today` y, con `all` sin placa, responde 400 «Para consultar todo el historial digite una placa.». La placa se filtra con `EF.Functions.ILike(placa sin guiones, PlateNormalizer.ToContainsPattern(texto))` (CHG-05). Nuevo `Wms.Application/Common/Notifications/TraceabilityNotification.cs` (`Create` y `PublishAsync`): título «Trazabilidad», mensaje «Camión {placa} cambió a estado: {etapa}», `RelatedEntityType = "TraceabilityUpdated"` y destino Admin y ForeignTrade; los 17 métodos privados pasan a usarlo.
  - Frontend: `DateFilterSelector.vue` agrega «Todo el historial», habilitado solo con placa; `app/pages/index.vue:17` y `:23-28` abren con «Todo el historial» cuando llega `?plate=` y vuelven a «Hoy» al borrar la placa; `useTraceabilityDashboard.ts:60-63` refresca solo por `relatedEntityType`.
  - No se toca: `AppTopbar.vue` (la ruta `/?plate=` sigue igual), `NotificationDto` ni `SignalRNotifier`.
- **Migración o script:** ninguno.
- **Pruebas automatizadas nuevas:** `Wms.Tests/Reports/TraceabilityDateRangeTests.cs` (hoy = 2026-10-03): `For_Day_UsesColombiaCalendarDay` (`2026-10-03T05:00:00Z` a `2026-10-04T05:00:00Z`), `For_Week_StartsOnMonday` (`2026-09-28T05:00:00Z`), `For_Month_StartsOnDayOne`, `For_All_HasNoLowerBound`, `For_Unknown_FallsBackToDay`, `Day_ExcludesPreviousEveningInColombia`; `Wms.Tests/Reports/TraceabilityNotificationTests.cs`: `Create_UsesSpanishTitleAndKeepsTechnicalType`; `test/unit/traceability/date-filter.spec.ts`: con placa se habilita «Todo el historial» y sin placa vuelve a «Hoy».
- **Criterios de aceptación:**
  - Dado las 20:00 del 03/10/2026 en Colombia, cuando el Admin abre la trazabilidad con «Hoy», entonces no aparecen los camiones de la noche del 02/10.
  - Dado QAA101 de ayer, cuando el Admin busca «qaa10» desde la barra superior, entonces el tablero abre con «Todo el historial» y muestra QAA101.
  - Dado un ingreso nuevo con el Admin conectado, cuando llega el aviso, entonces dice «Trazabilidad» y «Camión QAA101 cambió a estado: Ingreso registrado».
- **Re-test QA:** F7-TRZ-002, F7-TRZ-003, F7-NOT-008; REG F11-REG-006.
- **Riesgo de regresión:** bajo.
- **Tamaño:** M. **Dependencias:** CHG-42, CHG-05.

#### CHG-82 — El reporte de ingresos diarios muestra placa, tiquete y peso neto de cada depósito

- **Cierra:** DEF-F7-004 (MINOR).
- **Causa raíz:** `Wms.Application/Warehouse/Queries/GetDailyIncomingGoodsReport/GetDailyIncomingGoodsReportHandler.cs:115` toma `NetDeclaredWeight`, que la báscula ya no llena desde WMS-10 (`InitiateStorageWeighingHandler.cs:405-407`): siempre 0; el neto real está por camión en `WarehouseStorageEntry.PhysicalNetWeight`. Placa y transportadora salen del ciclo buscado por el servicio ancla (`:75-88,95-96,106,112`): los depósitos adicionales de un multidepósito y los confirmados antes de pesar quedan vacíos, aunque la entrada guarda la placa. El tiquete (`:108`) toma una entrada cualquiera, sin orden ni exclusión de anuladas. El filtro de estado (`:48-49`) ya cumple §10 · Reporte de ingresos diarios.
- **Cambio exacto:**
  - Backend: el handler incluye las entradas con su ingreso, vehículo y transportadora, filtra explícitamente Confirmado y Cerrado y arma las filas con la clase pura nueva `Wms.Application/Warehouse/Common/Services/DailyIncomingGoodsRowBuilder.cs`: camiones = entradas no anuladas en orden de creación; placa, tiquete y transportadora = valores distintos unidos con «, » (la placa de la entrada o, si falta, la del vehículo del ingreso); peso neto = Σ neto físico de los camiones, solo en la primera fila del depósito (nulo en las demás y cuando ningún camión tiene neto). Se borra la consulta de ciclos (`:69-88`); el total suma los netos. `DailyIncomingGoodsReportRowDto.NetWeightKg` pasa a anulable y `DailyIncomingGoodsPdfService.cs:170` imprime vacío cuando falta.
  - Frontend: `app/features/reports/types/daily-incoming-goods.ts:20` → `netWeightKg: number | null` (la página ya pinta «—», `daily-incoming-goods.vue:147-152`).
  - No se toca: la fecha del informe (`CreatedAt`, `:46-47`) ni `DailyOutgoingGoods*`.
- **Migración o script:** ninguno (se calcula al leer).
- **Pruebas automatizadas nuevas:** `Wms.Tests/Warehouse/DailyIncomingGoodsRowBuilderTests.cs`: `Build_TwoTrucks_JoinsTicketsPlatesAndSumsNet` (QAA101/2026T00001/20.000 y QAB201/2026T00003/18.000 → «QAA101, QAB201», «2026T00001, 2026T00003», 38.000), `Build_TwoProducts_NetOnlyOnFirstRow`, `Build_VoidedTruck_IsIgnored`, `Build_TruckWithoutWeighing_KeepsPlateWithoutTicketOrNet`, `Build_EmptyEntryPlate_UsesEntryLogVehiclePlate`, `Build_DepositWithoutTrucks_TruckFieldsAreNull`.
- **Criterios de aceptación:**
  - Dado 2026BA00001 confirmado con QAA101 (20.000 kg, 2026T00001) y QAB201 (18.000 kg, 2026T00003), cuando CE genera el reporte de ingresos de ese día, entonces la fila muestra «QAA101, QAB201», «2026T00001, 2026T00003» y 38.000 kg.
  - Dado un depósito confirmado antes del pesaje, cuando se genera el reporte, entonces muestra la placa y deja tiquete y neto vacíos.
- **Re-test QA:** F7-REP-001; REG F11-REG-017.
- **Riesgo de regresión:** bajo.
- **Tamaño:** M. **Dependencias:** CHG-76.

#### CHG-83 — Las exportaciones a Excel escriben las fechas en hora de Colombia

- **Cierra:** DEF-F7-006 (MINOR).
- **Causa raíz:** `app/utils/excel-export.ts:59-73` (`toCellValue`), la única utilidad que escribe fechas en Excel (usada por `app/composables/useExcelExport.ts:23`, `app/pages/reports/warehouse-movements.vue:159` y `app/pages/billing/reports/deposit-billing.vue:51`), convierte con `toColombiaPickerDate` (`app/utils/colombia-date.ts:60-65`), que devuelve un `Date` local; exceljs serializa el instante en UTC, así que en un navegador de Colombia la celda queda 5 horas adelante (21:00 en vez de 16:00). Una fecha sin hora (`yyyy-MM-dd`) se interpreta como medianoche UTC. El kárdex exporta «Fecha de salida» como fecha sin hora (`warehouse-movements.vue:198`) mientras la pantalla muestra la hora.
- **Cambio exacto:**
  - Frontend: `app/utils/colombia-date.ts` suma `toColombiaExcelDate(valor, soloFecha)`: `yyyy-MM-dd` → `Date.UTC(año, mes, día)` sin conversión; fecha inválida → `null`; en otro caso, los componentes de la hora de Bogotá (`dateTimeFormatter`, `:3-11`) llevados a `Date.UTC` (sin hora ni minuto cuando es solo fecha). `excel-export.ts` exporta `toCellValue` y la usa en `:62-65` y `:72`. `warehouse-movements.vue:198` → `format: "datetime"`.
  - Backend: ninguno (no hay Excel generado en el servidor).
  - No se toca: `dateSuffix`, `downloadBuffer`, los formatos numéricos ni los PDF.
- **Migración o script:** ninguno.
- **Pruebas automatizadas nuevas:** `test/unit/utils/colombia-date.spec.ts` (ejecutadas con `TZ` UTC, America/Bogota y Asia/Tokyo): `2026-10-02T21:00:00Z` → `2026-10-02T16:00:00.000Z`; `2026-10-03T02:30:00Z` → `2026-10-02T21:30:00.000Z` y, solo fecha, `2026-10-02T00:00:00.000Z`; `2026-10-02` → `2026-10-02T00:00:00.000Z`; valor inválido → `null`; `test/unit/utils/excel-export.spec.ts`: una celda «datetime» escrita y releída con exceljs para `2026-10-02T21:00:00Z` tiene hora 16; una celda «date» descarta la hora.
- **Criterios de aceptación:**
  - Dado un movimiento registrado el 02/10/2026 a las 16:00 (hora de Colombia), cuando Bodega exporta el inventario general a Excel, entonces la celda muestra 02/10/2026 16:00.
  - Dado un levante con fecha 02/10/2026, cuando se exporta, entonces la celda muestra 02/10/2026.
- **Re-test QA:** F7-REP-019; REG F11-REG-014.
- **Riesgo de regresión:** bajo.
- **Tamaño:** S. **Dependencias:** CHG-77, CHG-78.

#### CHG-84 — Documentos impresos con detalle, contacto real y una sola fuente de datos de la empresa

- **Cierra:** DEF-F7-011 (MINOR).
- **Causa raíz (se reproducen tres de los cuatro síntomas; «Recibido» con pago verificado no se reproduce: `InvoicePdfService.cs:336-343` imprime el estado guardado):**
  - Detalle ausente: `Wms.Application/Billing/Common/Services/InvoicePdfService.cs:145-147` no imprime `invoice.Detail` (lo llena `StorageBillingService.BuildDepositDetail`, `:769`); solo las notas (`:154-159`).
  - Teléfono 0: `WeighbridgeTicketPdfService.cs:203-206` toma el contacto del cliente de la factura y `:208-211` el nombre y NIT del cliente del depósito; los contactos del cliente del depósito no se cargan (`:90`, `:135`), así que imprime «Dirección: N/A» y «Teléfono: 0» (`:206`, `:270-271`); `FirstOrDefault()` no ordena ni filtra activos (`:204`; igual en `InvoicePdfService.cs:38,44`).
  - Datos de empresa: los parámetros `COMPANY_*` no existen (solo se siembra `INVENTORY_ADJUSTMENT_ADMIN_EMAIL`, `SeedDataExtensions.cs:239-249`) y cada PDF usa sus literales: un juego en `InvoicePdfService.cs:14-19,75-79`, `WeighbridgeTicketPdfService.cs:20-25,46-62,241-246`, `DailyBillingPdfService.cs:13-35,58-61`, `DailyIncomingGoodsPdfService.cs:19-41,79-82` y `DailyOutgoingGoodsPdfService.cs:19-40,79-82`, y otro en los pies de `DispatchGuidePdfService.cs:616,619`, `DepositPdfService.cs:465,468` y `WarehouseMovementsPdfService.cs:218,221` (el del legacy, `bodegas-legacy/reportes/encabezado.php:38-42`).
  - Mismo origen en las fechas impresas (hallazgo de la verificación): `InvoicePdfService.cs:86,90,139,282` y `WeighbridgeTicketPdfService.cs:251` formatean sin `ColombiaTime.ToColombia` (la factura de BA00002 creada la noche del 02/10 dice 03/10).
- **Cambio exacto:**
  - Backend:
    - Una sola fuente: parámetros del sistema `COMPANY_NAME`, `COMPANY_NIT`, `COMPANY_ADDRESS`, `COMPANY_PHONE`, `COMPANY_EMAIL` y `COMPANY_CITY` sembrados en `SeedDataExtensions.cs` con los datos del pie legacy (el único origen documentado) y editables en `admin/parameters`. `Wms.Application/Common/Models/CompanyInfo.cs` (con `FooterAddressLine` y `FooterEmailLine`), la clase pura `CompanyInfoResolver.Resolve(parámetros)` (valor ausente o en blanco → el sembrado) e `ICompanyInfoProvider`/`CompanyInfoProvider` (lee los activos), registrado en `Wms.Application/DependencyInjection.cs`. Los ocho PDF citados usan el proveedor y se borran sus literales.
    - `InvoicePdfService.ComposeContent` imprime, después de `:145`, el bloque «DETALLE:» con las líneas de `InvoiceDetailText.Lines(invoice.Detail)` (clase pura nueva).
    - Clase pura `StakeholderContactPicker` (`Phone`, `Address`): primer valor no vacío de los contactos activos por fecha de creación. `WeighbridgeTicketPdfService` usa el cliente de la factura o, si falta, el del depósito, carga sus contactos (después de `:90` y `:135`) e imprime «N/A» cuando no hay dato, nunca «0»; `InvoicePdfService.cs:38,44,59` usa el mismo selector.
    - Las fechas de `InvoicePdfService.cs:86,90,139,282` y `WeighbridgeTicketPdfService.cs:251` pasan por `ColombiaTime.ToColombia`.
  - Frontend: ninguno.
  - No se toca: `LoadingOrderPdfService`, `WarehouseNoveltyPdfService` ni `TranslatePaymentStatus`.
- **Migración o script:** `SeedCompanyParameters` (la genera el implementador con `dotnet ef`; seis filas nuevas en `system_parameters`, sin columnas). `fase-11-parametros-empresa.sql` (solo detección, antes de la migración): `SELECT id, code, value FROM system_parameters WHERE code LIKE 'COMPANY\_%';` debe devolver 0 filas; si hay filas, se borran antes de aplicar la migración (índice único `idx_param_code`) y sus valores se vuelven a digitar en `admin/parameters`.
- **Pruebas automatizadas nuevas:** `Wms.Tests/Common/CompanyInfoResolverTests.cs`: `Resolve_WithoutParameters_UsesSeededValues`, `Resolve_EmailWithValue_Prevails`, `Resolve_BlankValue_UsesDefault`, `FooterAddressLine_SeededValues_ReproducesCurrentFooter`; `Wms.Tests/Common/StakeholderContactPickerTests.cs`: `Phone_FirstContactWithoutPhone_ReturnsSecondActive`, `Phone_OnlyInactiveContacts_ReturnsNull`, `Address_WithoutAddress_ReturnsNull`; `Wms.Tests/Billing/InvoiceDetailTextTests.cs`: `Lines_DetailWithLineBreaks_OneLinePerBlock`, `Lines_Null_ReturnsEmpty`.
- **Criterios de aceptación:**
  - Dado la factura de almacenamiento de 2026BA00002, cuando Facturación la imprime, entonces aparece el bloque «DETALLE:» con «ALMACENAMIENTO DE: …» y la fecha en hora de Colombia.
  - Dado el tiquete 2026T00001 cobrado a consumidor final, cuando báscula lo imprime, entonces el contacto sale del cliente del depósito o «N/A», nunca «Teléfono: 0».
  - Dado el Admin, cuando cambia `COMPANY_EMAIL` en `admin/parameters`, entonces la factura, el tiquete, la guía y los reportes diarios imprimen el correo nuevo sin desplegar.
- **Re-test QA:** F7-PDF-001, F7-PDF-004, F7-PDF-007; REG F11-REG-012, F11-REG-020.
- **Riesgo de regresión:** medio (toca los ocho PDF). Lo mitiga que, con los valores sembrados, los pies reproducen el texto actual.
- **Tamaño:** L. **Dependencias:** CHG-66, CHG-73, CHG-82.

### Fase 12 — MINOR y TRIVIAL de interfaz, avisos, formatos y textos

- **Objetivo:** que todos los componentes estén importados y no quede la página duplicada de recepción directa; que cada error se avise una sola vez, sin código HTTP, y que la aplicación se recupere sola cuando el API vuelve; que no haya callejones sin salida (inicio por rol, página de error en español, detalle inexistente claro); que números, montos y fechas tengan un solo formato es-CO; que botones y campos tengan nombre accesible y el foco vaya al primer error; y que los textos visibles estén en español y sin términos técnicos. Cierra DEF-F0-001, DEF-F0-002, DEF-F10-003, DEF-F10-004, DEF-F10-005, DEF-F0-003, DEF-F10-006, DEF-F10-008, DEF-F1-008, DEF-F10-007, DEF-F5-013 y DEF-F6-020.
- **Criterio de entrada:** checkpoint de la Fase 11 aprobado.
- **Cambios:** CHG-85, CHG-86, CHG-87, CHG-88, CHG-89, CHG-90.
- **Orden interno:** CHG-85 (retira archivos que los demás ya no tocan) → CHG-86 → CHG-87 (usa `ApiError` y `describePageError`) → CHG-88 → CHG-89 → CHG-90 (los tres últimos comparten `history.vue`, `WeighbridgeHistoryTable.vue` y `PaymentDialog.vue`).
- **Migración de la fase:** ninguna.
- **Riesgos y mitigación:**
  - CHG-86 cambia el manejo de errores de toda la aplicación. Mitigación: `ApiError` conserva las lecturas actuales (`message`, `description`, `response`) y el re-test recorre los avisos de cada módulo.
  - CHG-88 toca unos 100 archivos. Mitigación: las pruebas guardianas fallan ante cualquier formato suelto y el lint no puede subir (regla 4.0.4).
- **Saneamiento de datos:** ninguno.
- **Criterio de salida:** compuertas comunes (regla 4.0.4) y en PASA: F0-NAV-003, F10-ERR-001, F10-ERR-003, F10-ERR-005, F10-ERR-006, F0-NAV-004, F0-NAV-005, F0-LOG-007, F10-UX-010, F10-UI-005, F10-UI-008, F10-ACC-001, F10-UX-004, F1-TER-001, F1-TER-005, F10-UI-006, F10-UX-012, F10-ERR-010, F10-ERR-013, F5-CNF-009, F5-COR-003, F5-GUI-008, F6-ACC-008, F6-REF-003; REG F11-REG-001, F11-REG-002, F11-REG-003, F11-REG-009, F11-REG-012, F11-REG-017, F11-REG-022, F11-REG-028.
- **Checkpoint:** se entrega al usuario un recorrido con el API detenido y reiniciado, la página de error y el inicio por rol de los seis roles, capturas con el navegador en inglés (formatos es-CO) y el resultado de las pruebas guardianas. El usuario aprueba el cierre del plan y la entrada a la fase 11 de QA (§7.2).

#### CHG-85 — Componentes importados y sin la página duplicada de recepción directa

- **Cierra:** DEF-F0-001 (MINOR), DEF-F0-002 (MINOR).
- **Causa raíz:**
  - DEF-F0-001: diez componentes usan `<LabelBase>` sin importarlo (de 80 usos, 70 sí lo importan) y Nuxt solo registra `BaseLabelBase` (`.nuxt/components.d.ts:22`): la etiqueta sale como un elemento desconocido, sin estilo y sin `for`. Son `QuickCreatePackagingTypeDialog.vue`, `AssignDepositCustomerDialog.vue`, `DepositDetailDocumentStakeholdersSection.vue`, `DepositDetailGeneralInfoCard.vue`, `AdjustInventoryDialog.vue`, `ReceptionStepSearch.vue`, `ModifyWeighingDateDialog.vue`, `ModifyWeighingDialog.vue`, `QuickCreateStakeholderDialog.vue` y `ServiceRecordDocumentsManager.vue`.
  - DEF-F0-002: `app/pages/warehouse/receptions/create.vue:15-20` no importa `ReceptionStepManualInfo`, que usa en `:297-303` (`nuxt.config.ts:203-207` solo resuelve PrimeVue). Ningún enlace ni menú lleva a esa página (`AppMenu.vue:243-261`); la recepción directa real está en `/warehouse/receptions` → «Recepción Directa» (`index.vue:232-237`, `:346-358`). La página duplicada además pierde `receivedCargoUnitIds` (`:163-169`) y usa el indicador de envío equivocado (`:300`).
- **Cambio exacto:**
  - Frontend: `import LabelBase from "~/components/base/LabelBase.vue";` en los nueve componentes que se conservan, respetando el estilo de comillas de cada archivo. Se retiran `app/pages/warehouse/receptions/create.vue`, `ReceptionStepSearch.vue` y `ReceptionStepRegisterArrival.vue` (solo los usaba esa página) y sus exportaciones (`app/features/warehouse/components/index.ts:15-16`); se actualizan `app/features/warehouse/README.md` (`:51`, `:299`, `:564`, `:655`) y `app/features/warehouse/components/README.md` (`:33-60`, `:164-182`, `:262`); en la documentación de QA se retiran F4-REC-020 y R-BOD-03 (`docs/qa/fase-04-bodega.md:16,78`, `docs/qa/00-plan-maestro.md:315`). El asterisco de obligatorio no forma parte de `LabelBase` en ninguno de sus usos: las diez etiquetas quedan iguales a las del resto de formularios.
  - Backend: ninguno (`GET warehouse/search/plate/{plate}` sigue en uso por `ForkliftUseDialog.vue`).
  - No se toca: `LabelBase.vue`, `nuxt.config.ts`, `index.vue`, `entry.vue`, `ReceptionStepCompletion.vue` ni `DirectReceptionList.vue`.
- **Migración o script:** ninguno.
- **Pruebas automatizadas nuevas:** `test/unit/guards/label-base-imports.spec.ts`: recorre `app/**/*.vue` y falla si un archivo usa `<LabelBase` sin importarlo (hoy lista 10; después, 0); `test/unit/guards/receptions-create-route.spec.ts`: ningún archivo de `app/` enlaza `/warehouse/receptions/create`.
- **Criterios de aceptación:**
  - Dado el Admin en `/admin/products/create`, cuando abre «Nuevo embalaje», entonces la consola no muestra `Failed to resolve component: LabelBase` y la etiqueta está asociada a su campo.
  - Dado Bodega en `/warehouse/receptions`, cuando pulsa «Recepción Directa», entonces abre el formulario sin avisos en la consola; la URL `/warehouse/receptions/create` ya no muestra un formulario.
- **Re-test QA:** F0-NAV-003; REG F11-REG-002.
- **Riesgo de regresión:** bajo.
- **Tamaño:** S. **Dependencias:** CHG-01.

#### CHG-86 — Un solo dueño de los avisos de error y recuperación cuando el API se cae

- **Cierra:** DEF-F10-003 (MINOR), DEF-F10-004 (MINOR).
- **Causa raíz:**
  - DEF-F10-003: el mismo error sale por tres emisores: el aviso global (`app/app.vue:53-69`, titulado `Error ${status}`, alimentado por `app/plugins/api-client.ts:141-147` y `stores/api-errors.ts`), el `onError` de los hooks (`useAssignInvoiceNumber.ts:23-28`, `useRecordPayment.ts:23-28`, `useVerifyPayment.ts:18,39`) y el texto en línea (`InvoiceActionsDialog.vue:100-110`). No hay dueño único (162 llamadas a `showError` en 75 archivos; 21 archivos muestran el 409 en línea y también reciben el global). El interceptor rechaza con el cuerpo de la respuesta y no con un error (`api-client.ts:147`), así que 29 archivos que leen `error.message` o `error.response` muestran además un texto genérico; y `api-client.ts:143` rotula «Error interno del servidor» cualquier estado sin cuerpo.
  - DEF-F10-004: `api-client.ts:90-97` rotula todo error sin respuesta como «500 / Error de conexión con el servidor»; TanStack reintenta 3 veces por defecto (`app/plugins/vue-query.ts:18` no lo configura) en cada consulta activa y las que tienen `refetchInterval` (p. ej. `useWeighbridgeQueue.ts:13`, `useForeignTradeDashboard.ts:27-65`, `usePendingGuides.ts:10`) repiten el aviso mientras dure la caída; al volver el API nada refresca la pantalla (el evento `online` del navegador no ocurre); y `auth.global.ts:29-31` y `auth-init.client.ts:26-28` cierran la sesión ante cualquier error de `getCurrentUser`, también de red.
- **Cambio exacto:**
  - Frontend:
    - `app/utils/api-error.ts`: `ApiError` (`status`, `description` nunca vacía, `message` igual a la descripción, `errors`, `traceId`, `isNetwork` y `response = { status, data }` para que sigan funcionando las lecturas actuales); `normalizeApiError(status, cuerpo)` con textos sin cuerpo: 400 «La solicitud no es válida.», 401 «Su sesión venció. Inicie sesión de nuevo.», 403 «No tiene permiso para realizar esta acción.», 404 «No se encontró el recurso solicitado.», 409 «La operación entra en conflicto con el estado actual.», 5xx «Ocurrió un error en el servidor. Intente de nuevo.», sin respuesta «Sin conexión con el servidor.»; `buildApiErrorNotice(error)` con títulos sin código HTTP (400 «No se pudo completar la acción», 401 «Sesión vencida», 403 «Sin permiso», 404 «No encontrado», 409 «Conflicto», ≥ 500 «Error del servidor») y un solo aviso «Datos no válidos» cuando llegan varios errores de validación.
    - Regla única: el interceptor es el dueño del aviso de error del API (`app/utils/api-error-notifier.ts`: aviso 100 ms después del error, una vez por estado y texto en 5 s). Un componente que ya muestra el error en su lugar lo reclama (`meta: { handlesErrors: true | [códigos] }` en el hook, o `claimApiError(error)` en un `catch`) y el global no sale; un toast propio con el mismo texto lo descarta `app/utils/toast-dedupe.ts` (usado por `useWmsToast.ts:44-56`). `api-client.ts:84-148` rechaza con `ApiError` y notifica por el nuevo canal (el 503 de la DIAN con el título «TRM no disponible»); `app/app.vue:27-69` deja de vigilar `stores/api-errors.ts`, que se borra; `vue-query.ts` reclama según `meta` en `queryCache.onError` y `mutationCache.onError`. `useAssignInvoiceNumber.ts` declara `handlesErrors` y borra su `onError`; las ramas 409 que muestran el error en línea llaman `claimApiError` (`PackingListUploadDialog.vue:68`, `DepositDetailGeneralInfoCard.vue:149`, `WithdrawReleaseDialog.vue:69`, `useQuickCreateStakeholder.ts:33`, `NoveltyFormDialog.vue:243`, `ProductPlacementsDialog.vue:174`, `ServicePricingRuleFormDialog.vue:477`, `ReleaseForm.vue:360`, `app/pages/admin/crews/index.vue:120`, `app/pages/admin/cities/index.vue:183`, `app/pages/operations/weighbridge/history.vue:178`, `index.vue:653,872`, `cycles/[id].vue:107`, `app/pages/foreign-trade/loading-orders/[id]/index.vue:136,164`, `dispatch-guides/index.vue:73`, `imports/[id]/index.vue:230`, `exports/[id]/index.vue:194`, `inspections/[id]/index.vue:194`, `app/pages/warehouse/loading-orders/[id].vue:118`, `app/pages/warehouse/novelties/index.vue:179`); se borran los avisos de texto fijo de `AgreementDetailDialog.vue:292,305,317,329,338`, `app/pages/admin/stakeholders/[id].vue:276,300` y `app/pages/admin/parameters/index.vue:198`.
    - Caída del API: `app/utils/query-retry.ts` (`shouldRetryQuery`: reintenta solo 502, 503 y 504, hasta 2 veces; red y 4xx no reintentan) en `vue-query.ts` junto con `mutations.networkMode = 'always'` (una acción del usuario nunca queda en cola para reenviarse sola). Sin respuesta, `api-client.ts:90-97` marca la conexión caída: `app/composables/useApiConnection.ts` pone `onlineManager` fuera de línea (se pausan consultas y sondeos) y prueba cada 5 s `GET administration/system-roles` (catálogo anónimo, §10 · Catálogos sin autenticación aceptados); con cualquier respuesta vuelve a línea y TanStack refresca las consultas activas. `app/components/app/AppConnectionBanner.vue` (en `app.vue`, `role="alert"`): «Sin conexión con el servidor. Reintentando…» con «Reintentar ahora». Las lecturas fallidas no muestran toast; una acción sin conexión muestra uno: «Sin conexión con el servidor» / «La acción no se realizó. Verifique la red e intente de nuevo.». `auth.global.ts:29` y `auth-init.client.ts:26` cierran la sesión solo con 401 o 403.
  - Backend: ninguno.
  - No se toca: la renovación del token ante 401, los `refetchInterval` de cada hook ni `ReasonDialog`.
- **Migración o script:** ninguno.
- **Pruebas automatizadas nuevas:** `test/unit/utils/api-error.spec.ts`: 403 sin cuerpo → «No tiene permiso para realizar esta acción.»; 404 sin cuerpo nunca dice «Error interno»; con `description`, `message` es igual; tres errores de validación → un aviso; 409 → título «Conflicto»; `test/unit/utils/api-error-notifier.spec.ts` (tiempo simulado): misma clave en 5 s → un aviso; un componente que muestra el mismo detalle antes de 100 ms suprime el global; un reclamo antes de 100 ms → sin aviso; `test/unit/utils/toast-dedupe.spec.ts`; `test/unit/utils/query-retry.spec.ts`: 404 → no; 503 primera falla → sí; 503 tercera falla → no; red → no; `test/unit/composables/api-connection.spec.ts`: la primera falla de red pone fuera de línea e inicia la prueba; una segunda falla no inicia otra; la respuesta vuelve a línea; `test/components/app/AppConnectionBanner.spec.ts`: con la conexión caída muestra el texto.
- **Criterios de aceptación:**
  - Dado una factura con N.º SIIGO repetido, cuando Facturación lo asigna, entonces el error aparece una sola vez, bajo el campo.
  - Dado el API detenido con el tablero de báscula abierto, cuando pasan 60 s, entonces se ve solo la franja «Sin conexión con el servidor. Reintentando…», sin avisos apilados y sin cerrar la sesión; al iniciar el API, la franja desaparece y los datos se actualizan sin recargar.
  - Dado un 403 de cualquier pantalla, cuando aparece el aviso, entonces dice «Sin permiso» / «No tiene permiso para realizar esta acción.» y nunca «Error interno del servidor».
- **Re-test QA:** F10-ERR-001, F10-ERR-003, F10-ERR-005, F10-ERR-006; REG F11-REG-001, F11-REG-002.
- **Riesgo de regresión:** medio (cambia el manejo de errores de toda la aplicación). Lo mitigan los getters compatibles de `ApiError` y las pruebas del notificador.
- **Tamaño:** L. **Dependencias:** CHG-48, CHG-18.

#### CHG-87 — Sin callejones sin salida: inicio por rol, página de error en español y detalle inexistente claro

- **Cierra:** DEF-F10-005 (MINOR), DEF-F0-003 (MINOR).
- **Causa raíz:**
  - DEF-F10-005 (parcialmente; el spinner de la factura inexistente no es infinito, son 4 intentos de unos 7 s): la tarjeta de error de `app/pages/billing/invoices/[id].vue:255-266` lee `error.message` y queda en blanco, y el título dice «Factura pendiente de número» sin factura (`:201`); un ID mal formado choca con la restricción `{id:guid}` (`BillingController.cs:117`), el API responde 404 sin cuerpo y el interceptor lo rotula «Error interno del servidor» (`api-client.ts:143`); no existe `app/error.vue` y una ruta inexistente muestra la página por defecto de Nuxt en inglés.
  - DEF-F0-003: el logo enlaza `/` en `app/components/layout/AppTopbar.vue:39` y `AppSidebar.vue:34` (este con `<a href>`, que recarga), y `/` solo admite Admin y ForeignTrade (`app/pages/index.vue:11`): los otros roles caen en «Acceso Denegado» (`app/middleware/auth.global.ts:63-69`), que solo ofrece «Cerrar sesión» (`app/pages/access-denied.vue:28-35`).
- **Cambio exacto:**
  - Frontend:
    - `app/utils/role-routes.ts`: `resolveDeniedRedirect(ruta, roles)` → el inicio del rol cuando se pide `/` sin acceso, y `/access-denied` en los demás casos; `auth.global.ts:67` la usa. `AppTopbar.vue:39` y `AppSidebar.vue:34` (`NuxtLink`) enlazan `getDefaultRouteForRoles(roles)`; `access-denied.vue` suma el botón principal «Ir a mi inicio».
    - `app/utils/guid.ts` (`isGuid`) y `app/middleware/valid-route-id.global.ts`: un `id` de ruta que no es GUID produce un 404 de la aplicación sin llamar al API (cubre las 15 rutas `[id]`).
    - `app/error.vue` en español (diseño de `access-denied.vue`) con `describePageError(código)` de `api-error.ts`: 404 «Página no encontrada» / «La dirección que abrió no existe o ya no está disponible.»; 403 «Sin permiso»; otros «Ocurrió un error inesperado» / «Intente de nuevo. Si continúa, avise a soporte.». Botones «Volver» e «Ir a mi inicio» (`clearError({ redirect: getDefaultRouteForRoles(roles) })`).
    - `invoices/[id].vue`: el título solo dice «Factura {número o pendiente de número}» con factura cargada; con 404, «La factura no existe o fue eliminada.» con «Volver» e «Ir a Facturas»; otros errores muestran la descripción. `useInvoiceDetail.ts` declara `handlesErrors: [404]`.
  - Backend: ninguno.
  - No se toca: la tarjeta de error de CE (`app/pages/foreign-trade/imports/[id]/index.vue:520-525`) ni la búsqueda de placa de la barra superior (`AppTopbar.vue:27`).
- **Migración o script:** ninguno.
- **Pruebas automatizadas nuevas:** `test/unit/utils/role-routes.spec.ts`: inicio por rol (Billing `/billing`, Scale `/operations/weighbridge`, Receiving `/operations/entries`, Warehouse `/warehouse`, Admin y ForeignTrade `/`, sin rol `/`), `resolveDeniedRedirect("/", ["Billing"])` → `/billing`, `resolveDeniedRedirect("/admin/users", ["Billing"])` → `/access-denied`, `resolveDeniedRedirect("/", [])` → `/access-denied`; `test/unit/utils/guid.spec.ts`; en `api-error.spec.ts`: `describePageError(404)` en español; `test/components/app/ErrorPage.spec.ts`: el 404 muestra «Página no encontrada» y dos botones; `test/components/app/AccessDenied.spec.ts`: con rol Billing, «Ir a mi inicio» navega a `/billing`.
- **Criterios de aceptación:**
  - Dado `facturacion`, cuando pulsa el logo, entonces llega a `/billing`; dado `bodega`, cuando abre `/` por URL, entonces llega a `/warehouse`.
  - Dado `/billing/invoices/no-es-un-id`, cuando se abre, entonces aparece «Página no encontrada» en español con «Volver» e «Ir a mi inicio», sin llamar al API.
  - Dado el GUID de una factura que no existe, cuando Facturación lo abre, entonces ve «La factura no existe o fue eliminada.» con «Ir a Facturas».
- **Re-test QA:** F0-NAV-004, F0-NAV-005, F0-LOG-007, F10-ERR-005, F10-UX-010; REG F11-REG-001, F11-REG-002, F11-REG-028.
- **Riesgo de regresión:** bajo.
- **Tamaño:** M. **Dependencias:** CHG-86, CHG-03.

#### CHG-88 — Un solo formato de números, montos y fechas en toda la interfaz

- **Cierra:** DEF-F10-006 (MINOR).
- **Causa raíz:** cada pantalla formatea a su manera con el idioma del navegador: 63 `toLocaleString()` sin locale (60 de números) en 22 archivos y 4 `toLocaleTimeString()`; 59 de 75 `<InputNumber>` sin `locale="es-CO"`; 6 montos armados a mano con `$`; 25 `formatCurrency` locales y 29 `Intl.NumberFormat` sueltos; 93 formatos de fecha distintos en 71 archivos (26 con `es-ES`, 24 «3 oct 2026», 14 «3/10/26, 7:16 a. m.»), todos con la zona del navegador. Con un navegador en inglés se ve «12,000 kg» y «$28,560». Las utilidades correctas ya existen (`app/utils/colombia-date.ts`, `app/shared/utils/format.ts`, `useQuantityFormatter`). Pantallas de la ficha: `app/pages/operations/weighbridge/cycles/[id].vue:201,502,512,524,550`, `WeighbridgeCycleTimeline.vue:48,59,261`, `WeighbridgeCycleTickets.vue:172`, `history.vue:352,361,478,507,671,692,715,719,750,753`, `WeighbridgeHistoryTable.vue:138,147,428,431,436`, `app/pages/warehouse/inventory/index.vue:277,390-434,530,560-571`, `app/pages/billing/invoices/[id].vue:117-137`, `invoices/index.vue:123-127` y `app/pages/billing/index.vue:53-62`.
- **Cambio exacto:**
  - Frontend: formato único es-CO: números con punto de miles y coma decimal (máximo 2 decimales), pesos «12.000 kg», COP «$ 1.234.567», USD «US$ 1.234,56», fecha `dd/MM/yyyy` y fecha y hora `dd/MM/yyyy HH:mm` (24 h, `America/Bogota`). `format.ts` suma `formatNumber` y `formatKg` y conserva `formatCurrency`; se borran `formatDate` y `DateFormatPreset` y sus tres consumidores (`DepositInvoiceHistoryTable.vue:3`, `DepositSummaryDialog.vue:6`, `app/pages/billing/pending-deposits/index.vue:8`) pasan a `formatColombiaDate`; `useQuantityFormatter.ts:9-20` delega en `formatNumber` y `formatKg`; `colombia-date.ts` suma `formatColombiaTime` (`HH:mm`). Se reemplazan los `toLocaleString`, `toLocaleTimeString`, formatos de fecha, `formatCurrency` locales e `Intl.NumberFormat` sueltos por las utilidades compartidas; los montos manuales (`cycles/[id].vue:502`, `WeighbridgeCycleTickets.vue:172`, `useCreateDispatchGuide.ts:14,16`, `FinancialStatusAlert.vue:55`, `useForkliftMutations.ts:85`, `app/pages/warehouse/forklift/index.vue:48`) usan `formatCurrency(valor, 'COP')`; los 59 `<InputNumber>` declaran `locale="es-CO"`.
  - Backend: ninguno.
  - No se toca: `app/utils/excel-export.ts` (CHG-83), el formato global del `DatePicker` (`dd/mm/yy`) ni los PDF que replican el legacy (`DepositPdfService`, `DispatchGuidePdfService`, `LabelGenerationService`), que conservan su formato por el plan de paridad.
- **Migración o script:** ninguno.
- **Pruebas automatizadas nuevas:** `test/unit/utils/format.spec.ts`: `formatNumber(12000)` → «12.000», `formatNumber(1234.5)` → «1.234,5», `formatKg(303000)` → «303.000 kg», `formatCurrency(28560, 'COP')` → «$ 28.560», `formatCurrency(1234.5, 'USD')` → «US$ 1.234,50» (normalizando el espacio duro); en `colombia-date.spec.ts`: `2026-10-03T12:16:00Z` → «03/10/2026 07:16», `2026-10-03T03:30:00Z` → «02/10/2026», hora «07:16»; `test/unit/guards/source-guards.spec.ts`: ningún `toLocale*` sin locale, ningún `es-ES` y todo `<InputNumber>` con `locale="es-CO"` (hoy 67, 26 y 59).
- **Criterios de aceptación:**
  - Dado un navegador en inglés, cuando báscula abre el detalle de un ciclo, entonces ve «12.000 kg» y «$ 28.560».
  - Dado el historial de báscula, el inventario y las facturas, cuando se abren, entonces todas las fechas se leen «03/10/2026 07:16» o «03/10/2026».
- **Re-test QA:** F10-UI-005; REG F11-REG-009, F11-REG-012.
- **Riesgo de regresión:** medio (cambio mecánico en unos 100 archivos). Lo mitigan las pruebas guardianas, que fallan ante cualquier formato suelto.
- **Tamaño:** L. **Dependencias:** CHG-85, CHG-44, CHG-83.

#### CHG-89 — Botones y campos con nombre accesible y foco en el primer error

- **Cierra:** DEF-F10-008 (MINOR).
- **Causa raíz:** `app/components/app/AppTable.vue:635-669` pinta «Ver», «Editar» y «Eliminar» como íconos sin `aria-label` ni tooltip (en PrimeVue 4 un botón sin `label` no tiene nombre accesible), y sus filtros (`:456`, `:565-600`) solo tienen `placeholder`; hay 34 botones de solo ícono sin nombre en 20 archivos, 158 de 604 controles sin `id`, `input-id` ni `aria-label` y 165 etiquetas sin `for`; ninguno de los 25 formularios mueve el foco al primer error (p. ej. `StakeholderForm.vue:100` solo mira `formState.valid`). PrimeVue 4.5.5 ya marca `aria-invalid="true"` en los campos inválidos.
- **Cambio exacto:**
  - Frontend: `AppTable.vue:635-669` con `aria-label` y `v-tooltip.top` «Ver detalle», «Editar» y «Eliminar»; `:456` `aria-label="Buscar en la tabla"`; filtros (`:565-600`) con `aria-label` igual al placeholder o al encabezado. `aria-label` y `v-tooltip` en los botones de ícono de `WeighbridgeHistoryTable.vue:207,474`, `PendingEntryList.vue:163`, `ServiceRecordDocumentsManager.vue:146`, `TruckGrid.vue:235,254`, `LoadingOrderForm.vue:658,921`, `BankAccountsList.vue:22,23`, `ContactsList.vue:18,19`, `ForkliftUseDialog.vue:335`, `PhotoUploader.vue:146`, `ServicePricesList.vue:26`, `AppBreadcrumb.vue:74` («Cerrar sesión»), `AppTopbar.vue:67` («Cerrar búsqueda»), `app/pages/admin/locations/index.vue:325,333`, `app/pages/operations/weighbridge/recover.vue:277` y `reports.vue:108,121`; en Bodega, que usa tableta (§10 · Bodega usa tableta), «Buscar» lleva texto visible en `DirectReceptionList.vue:68,74,82`, `PendingFromWeighbridgeList.vue:83,89,97` y `app/pages/warehouse/receptions/entry.vue:78,84`. `for`/`input-id` o `aria-label` en los controles de `PaymentDialog.vue` y en los filtros de `app/pages/billing/invoices/index.vue:200-219`, `payments/index.vue:187-221,327`, `PendingDepositsFilters.vue:54,63`, `ReceptionList.vue:147-196`, `app/pages/foreign-trade/deposits/index.vue:181-221`, `loading-orders/index.vue:196-224`, `app/pages/reports/daily-outgoing-goods.vue:178-218`, `warehouse-movements.vue:274-296`, `WeighbridgeHistoryTable.vue:190-197` e `inventory/index.vue:337,500`. Foco: `app/utils/focus-first-invalid.ts` (busca el primer `[aria-invalid="true"]` en orden del documento, lo enfoca y lo centra; reintenta hasta 5 veces cada 80 ms porque la validación es asíncrona) y `app/plugins/focus-first-invalid.client.ts` (escucha `submit` en captura): cubre los 25 formularios sin editarlos.
  - Backend: ninguno.
  - No se toca: los componentes de PrimeVue ni el modo oscuro (§10 · el modo oscuro se mantiene).
- **Migración o script:** ninguno.
- **Pruebas automatizadas nuevas:** `test/components/app/AppTable.spec.ts`: las acciones de fila tienen «Ver detalle», «Editar» y «Eliminar» y los filtros tienen `aria-label`; `test/unit/utils/focus-first-invalid.spec.ts`: con dos campos inválidos enfoca el primero del documento; sin inválidos no hace nada; en `source-guards.spec.ts`: ningún botón de solo ícono sin nombre accesible (hoy 34).
- **Criterios de aceptación:**
  - Dado la lista de terceros con un lector de pantalla, cuando se recorren las acciones de una fila, entonces se anuncian «Ver detalle», «Editar» y «Eliminar».
  - Dado el alta de un tercero con dos campos obligatorios vacíos, cuando se pulsa «Crear Tercero», entonces el foco queda en el primero.
  - Dado la tableta de Bodega, cuando se abre «Ingresos», entonces «Buscar» muestra su texto.
- **Re-test QA:** F10-UI-008, F10-ACC-001, F10-UX-004; REG F11-REG-002.
- **Riesgo de regresión:** bajo.
- **Tamaño:** M. **Dependencias:** CHG-88.

#### CHG-90 — Textos visibles en español y sin términos técnicos

- **Cierra:** DEF-F1-008 (MINOR), DEF-F10-007 (MINOR), DEF-F5-013 (TRIVIAL), DEF-F6-020 (TRIVIAL).
- **Causa raíz:**
  - DEF-F1-008: «Stakeholder» quedó en textos de interfaz (`StakeholderForm.vue:315`, `useStakeholderCreate.ts:14-15`, `useStakeholderUpdate.ts:20`, `QuickCreateStakeholderDialog.vue:66,67,76,84,100,190,203`, `ReceptionStepManualInfo.vue:345`, `app/pages/billing/pending-deposits/index.vue:224`, `app/pages/admin/stakeholders/[id].vue:47`) y en mensajes del backend (`UpdateStakeholderHandler.cs:18`, `GetStakeholderByIdHandler.cs:21`, `AssignBusinessRoleHandler.cs:19`, `RemoveBusinessRoleHandler.cs:19`, `UpdateBankAccountHandler.cs:23`, los validadores de terceros y cuentas, los handlers y validadores de `Wms.Application/Agreements/`, `StartForkliftUseCommandValidator.cs:14`, `StartForkliftUseCommandHandler.cs:35` y `BillingService.cs:150`); `QuickCreateStakeholderDialog.vue:76,84` imprimen el código del rol.
  - DEF-F5-013: los mensajes interpolan el estado en inglés (`WarehouseStorage.cs:278,290,402`, `UpdateDraftDepositHandler.cs:40`, `UpdateDepositStakeholdersHandler.cs:43`, `CompleteReceptionCommandHandler.cs:68,76`, `InitiateOutputWeighingHandler.cs:92`, `EndForkliftUseCommandHandler.cs:44`), y `CreateDispatchGuideCommandHandler.cs:107-112` y `CreateExportDispatchGuideCommandHandler.cs:73-76` tratan una orden de inspección como de exportación.
  - DEF-F6-020: `UpdateInvoiceValidator.cs:9` usa la plantilla de FluentValidation con el nombre técnico («'Detail' debe ser menor o igual que 1000 caracteres…»); `ReissueInvoiceCommandHandler.cs:43` arma «La factura sin número ya fue refacturada como sin número.» (también `Invoice.cs:248,287`); `CalculateBillingPreviewValidator.cs:9` muestra `ServiceId`.
  - DEF-F10-007: faltan claves del idioma de PrimeVue en `nuxt.config.ts:47-215` (quedan en inglés las de `@primevue/core/config/index.mjs:36-100`); los mensajes de validación de `FileUpload` son propiedades del componente y nadie las define; «vehiculo» sin tilde en `app/pages/operations/entries/index.vue:140,189`; la auditoría muestra el nombre de la clase (`app/pages/admin/audit/index.vue:84-88`); el historial muestra «Pesaje #0 (Gross)» (`history.vue:650`); y los mensajes de báscula, recepción, montacargas y factura interpolan estados en inglés (`WeighbridgeCycle.cs:78,89,100,113`, `CompleteCycleHandler.cs:49`, `RecordWeighingHandler.cs:77,115,122,386,401,457`, `GenerateGlobalDispatchGuideHandler.cs:88,93`, `InitiateStorageWeighingHandler.cs:965`, `Invoice.cs:76,93,339,494`, `UpdateInvoiceRecipientHandler.cs:24`).
- **Cambio exacto:**
  - Backend:
    - Rótulos de estado como funciones puras: `WeighbridgeCycle.StatusLabel` (Pendiente de pago, Listo para pesar, Primer peso capturado, En proceso, Completo, Cancelado), rótulos de tipo de peso (Bruto, Tara, Intermedio), `ReceptionLog.StatusLabel` (En progreso, Descargada, Completada, Anulada) y `ForkliftUse.StatusLabel` (En progreso, Finalizado, Completado); se reutilizan `WarehouseStorage.StatusLabel` (CHG-31), `LoadingOrder.StatusLabel` e `Invoice.StatusLabel` (`Invoice.cs:295`).
    - Mensajes finales (ejemplos): «Solo se puede confirmar un depósito en estado Borrador. Estado actual: {estado}.»; «Solo se puede devolver para corrección un depósito en estado Confirmado. Estado actual: {estado}.»; «Solo se puede editar un depósito en estado Borrador. Estado actual: {estado}.»; «El ciclo no puede cerrarse en estado {estado}.»; «El primer pesaje requiere que el ciclo esté en estado Listo para pesar.»; «El primer pesaje debe ser {Bruto o Tara} según la configuración del servicio.»; «El segundo pesaje requiere que el ciclo esté en estado Primer peso capturado.»; «Solo se puede reasignar el destinatario de una factura en borrador.»; «Solo se pueden aprobar facturas en borrador o pendientes de aprobación.»; «Solo se puede actualizar el detalle de una factura en borrador.». Las órdenes de inspección se rechazan con «Las órdenes de cargue de inspección no generan guía de salida.» en `CreateDispatchGuideCommandHandler` y `CreateExportDispatchGuideCommandHandler.cs:73-76`.
    - «stakeholder» → «tercero» en los mensajes citados (p. ej. «El tercero no existe.», «No existe el tercero con el id {id}», «El Id del tercero no puede estar vacío.»).
    - Facturación: `UpdateInvoiceValidator.cs:9` → «El detalle no puede superar los 1000 caracteres.»; clase pura `Wms.Application/Billing/Common/Services/ReissueMessages.AlreadyReissued(original, nueva)`: «La factura FV-100 ya fue refacturada como la factura FV-101.», «La factura FV-100 ya fue refacturada; la nueva factura está en Borrador y aún no tiene número SIIGO.», «La factura anulada sin número ya fue refacturada como la factura FV-101.» y «La factura anulada sin número ya fue refacturada; la nueva factura está en Borrador y aún no tiene número SIIGO.»; `Invoice.cs:248,287` → «La factura {FV-100 o anulada sin número} ya fue refacturada.»; `CalculateBillingPreviewValidator.cs:9` → «Indique el servicio.».
  - Frontend:
    - «Tercero» en lugar de «Stakeholder» en los textos citados («Crear Tercero», «Tercero creado.», «El tercero {nombre} se creó con éxito.», «Tercero actualizado correctamente.», «Usar este tercero», cabecera «Terceros», «Solo terceros con rol de Cliente»); `QuickCreateStakeholderDialog.vue:76,84` muestran la etiqueta del rol (Cliente, Importador, Agencia de aduanas (SIA), Exportador).
    - `nuxt.config.ts`: las claves faltantes del idioma de PrimeVue (`completed`, `pending`, `fileChosenMessage`, `noFileChosenMessage`, horas y minutos anterior y siguiente, `am`, `pm`, `aria.listLabel`) en español; `app/utils/file-upload-messages.ts` con los mensajes de tamaño, tipo y cantidad de archivos («{0}: el archivo supera el tamaño máximo de {1}.», «{0}: tipo de archivo no permitido. Se aceptan: {1}.», «Se superó el máximo de {0} archivos.»), aplicado en `PaymentDialog.vue`, `LoadingOrderForm.vue:645`, `PackingListUploadDialog.vue:228`, `CityImportDialog.vue:103` y `PhotoUploader.vue:161`.
    - `app/pages/operations/entries/index.vue:140,189` → «Este vehículo ya tiene un ingreso abierto.».
    - Auditoría: `app/features/audit/utils/entity-labels.ts` con la etiqueta de las 44 entidades auditables (p. ej. `Stakeholder` → «Tercero»); `admin/audit/index.vue:84-88` muestra la etiqueta y filtra con una lista.
    - Pesajes: `app/features/weighbridge/utils/weighing-labels.ts` (`weighingNumber(secuencia)` = secuencia + 1 y `weightTypeLabel`), usado en `history.vue:650,901`, `cycles/[id].vue:402`, `ModifyWeighingDialog.vue:67,152`, `WeighbridgeCycleTimeline.vue:228`, `WeightCapture.vue:341` e `index.vue:1126`: «Pesaje 1 (Bruto)».
  - No se toca: rutas, clases, claves de consulta y nombres de variables (solo textos visibles); el término «Facturación por CPI» del menú (vocabulario del negocio heredado del legacy); `Invoice.cs:242,444` ni `OverrideBillingAmountHandler.cs:26` (ya en español).
- **Migración o script:** ninguno (`audit_logs.affected_table` conserva el nombre de la clase; solo cambia cómo se muestra).
- **Pruebas automatizadas nuevas:** `Wms.Tests/Domain/Warehouse/WarehouseStorageStatusLabelTests.cs`: `Confirm_WhenConfirmed_MessageUsesSpanishState` («…en estado Borrador. Estado actual: Confirmado.»), `MarkForCorrection_WhenDraft_MessageUsesSpanishState`, `UpdateDraftInfo_WhenConfirmed_MessageUsesSpanishState`; `Wms.Tests/ForeignTrade/DispatchGuideRulesTests.cs`: `Inspection_Throws_NoGuideMessage`; `Wms.Tests/Domain/Weighbridge/WeighbridgeCycleTests.cs`: `StatusLabel_EachStatus_ReturnsSpanishLabel`, `MarkAsReadyForWeighing_FromComplete_MessageHasNoEnglishStatus`; `Wms.Tests/Domain/Billing/InvoiceActionRulesTests.cs`: `Approve_FromPaid_MessageHasNoEnglishStatus`; `Wms.Tests/Weighbridge/WeighingTypeLabelsTests.cs`: Bruto, Tara e Intermedio; `Wms.Tests/Billing/ReissueMessagesTests.cs`: los cuatro textos exactos; `Wms.Tests/Billing/Validators/UpdateInvoiceValidatorTests.cs`: 1.001 caracteres → «El detalle no puede superar los 1000 caracteres.», 1.000 → válido; `test/unit/audit/entity-labels.spec.ts`: `Stakeholder` → «Tercero», clase desconocida → su nombre, todas las entidades auditables con etiqueta; `test/unit/weighbridge/weighing-labels.spec.ts`: secuencia 0 → 1, `Gross` → «Bruto»; en `source-guards.spec.ts`: ningún texto visible con «Stakeholder» y todo `FileUpload` con los mensajes en español.
- **Criterios de aceptación:**
  - Dado el Admin en el alta de terceros, cuando crea uno, entonces el botón dice «Crear Tercero» y el aviso «Tercero creado.».
  - Dado un depósito Confirmado, cuando CE intenta confirmarlo de nuevo, entonces ve «Solo se puede confirmar un depósito en estado Borrador. Estado actual: Confirmado.».
  - Dado una orden de inspección, cuando CE intenta emitirle guía, entonces ve «Las órdenes de cargue de inspección no generan guía de salida.».
  - Dado una factura anulada sin número y refacturada sin número, cuando se intenta refacturar otra vez, entonces el mensaje es «La factura anulada sin número ya fue refacturada; la nueva factura está en Borrador y aún no tiene número SIIGO.».
  - Dado el detalle de un ciclo en el historial, cuando báscula lo abre, entonces lee «Pesaje 1 (Bruto)»; dado un archivo de 6 MB en las fotos, el aviso está en español.
- **Re-test QA:** F1-TER-001, F1-TER-005, F10-UI-006, F10-UX-012, F10-ERR-010, F10-ERR-013, F5-CNF-009, F5-COR-003, F5-GUI-008, F6-ACC-008, F6-REF-003; REG F11-REG-003, F11-REG-017, F11-REG-022.
- **Riesgo de regresión:** bajo; solo cambian textos y rótulos.
- **Tamaño:** L. **Dependencias:** CHG-49, CHG-31, CHG-33, CHG-28, CHG-89.

## 5. Decisiones requeridas

No queda ninguna decisión pendiente. El usuario resolvió D-1 y D-2 el 3 de octubre de 2026 aceptando la recomendación; se conservan abajo como registro. Los dos pendientes que no son código (PRF-002 y la base de la fase 11 de QA) están en §7.3.

### D-1 — Consolidación de los cobros «por facturar» de báscula y montacargas (DEF-F6-017)

- **Pregunta:** para un cliente con preferencia «Consolidada», ¿los cobros «por facturar» de báscula y de montacargas se agrupan en una sola factura por ventana (semanal, quincenal o mensual según el ciclo), y se conserva la opción «Por ciclo de báscula»?
- **Recomendación:** no. «Consolidada» queda para almacenamiento y guías de salida a crédito, donde ya funciona (F6-ALM-007); se corrige el texto de la configuración, se retira «Por ciclo de báscula» (no tiene código) y el job pasa a ser la conciliación diaria de pagos. Motivos: el legacy no consolida; cada tiquete se imprime con su propia factura; es el mismo criterio de §10 · OnDemand se retira (una opción que no hace nada se retira). Tamaño S.
- **Alternativa:** consolidar al crear la factura: los cuatro handlers de cobro «por facturar» (`StartWeighingOnlyPendingBillingHandler.cs:89`, `StartStoragePendingBillingHandler.cs:115`, `StartOutputPendingBillingHandler.cs:95`, `EndForkliftUseCommandHandler.cs:130`) usan `BillingService.GetOrCreateConsolidatedInvoiceAsync`, como la guía a crédito (`CreateDispatchGuideCommandHandler.cs:244-249`). Implica que el ciclo, la entrada y el uso de montacargas apunten a la factura consolidada, un solo N.º SIIGO para cobros de días distintos, tiquetes impresos con una factura todavía abierta y definir qué hace «Por ciclo de báscula». Tamaño L.
- **Resolución (3-oct-2026):** se acepta la recomendación. La implementa CHG-63 (Fase 9).

### D-2 — Cambio del modo de pago de una operación de báscula ya cobrada (DEF-F3-013, primera parte)

- **Pregunta:** ¿báscula debe poder cambiar, desde el historial, el modo de pago de una operación ya cobrada (de «Por facturar» a «Pago inmediato» o al revés)? La ficha lo espera; el endpoint se retiró del backend en mayo de 2026 (`a088674`) y la pantalla quedó con la acción sin efecto.
- **Recomendación:** no. Todo cobro crea su factura en el mismo instante y el estado lo lleva la factura: un cobro «por facturar» se paga en Facturación → Pagos. Se retira la acción del historial. Tamaño S.
- **Alternativa:** restaurar `PATCH weighbridge/{id}/payment-mode` (política `ScaleAccess`) con reglas para la factura emitida, acordadas antes con Facturación: de «Por facturar» a «Pago inmediato» registra el pago en la factura existente; de «Pago inmediato» a «Por facturar» revierte un pago todavía no verificado. Tamaño M.
- **Resolución (3-oct-2026):** se acepta la recomendación. La implementa CHG-47 (Fase 7).

### 5.1 Criterios adoptados por el plan sin consulta

Las demás preguntas que surgieron en la verificación se resolvieron con el §10, con una regla ya escrita en el código o en el plan de paridad, o con la opción que cumple el resultado esperado de la ficha. Quedan a la vista para que el usuario los revise al aprobar el plan:

| Tema | Criterio adoptado | Fundamento | Cambio |
|---|---|---|---|
| Destino de las salidas de importación sin guía | Báscula no cierra la salida sin guía; la orden espera la guía si se carga después; Vigilancia no registra la salida | §10 · Ninguna mercancía de importación sale sin guía | CHG-33 |
| Firmante de una guía con varios clientes | El conductor | Es el único firmante común; así lo hacía el legacy | CHG-34 |
| Levante impreso en la guía | El más reciente del producto al emitir, guardado en la línea | La guía congela sus saldos (§10 · Guía con saldos congelados) | CHG-35 |
| Tara igual al bruto | Se acepta (neto 0) | Solo la tara mayor que el bruto es imposible | CHG-37 |
| Neto de una operación de un solo pesaje | El peso registrado | Convención ya usada en `ModifyFirstWeightHandler.cs:70-72` | CHG-76 |
| Efectivo y cambio ya guardados | Las columnas se conservan con su historia; el API deja de recibirlos y de mostrarlos | §10 · Efectivo y cambio fuera de la UI y del API, sin pérdida de datos | CHG-53 |
| Usuario inactivo con la contraseña correcta | Ve «Usuario inactivo. Comuníquese con el administrador.» | Solo lo ve quien conoce la contraseña | CHG-51 |
| Novedad con desglose que no cuadra | Advertencia en el API y confirmación en la pantalla, sin rechazo | El plan de paridad dejó las novedades «sin regla de suma, como el legacy»; la ficha acepta advertencia | CHG-57 |
| Ajuste CE-7 y corrección de productos | Registran movimiento en el kárdex | La ficha lo espera y `ReconcileDeposits` supone Σ movimientos = stock | CHG-39 |
| Validar de nuevo un depósito | No se permite (409) | El código ya define la validación como única | CHG-70 |
| Depósitos anulados en la lista de importaciones | No se listan; siguen en la columna «Anulado» del Kanban | Igual que exportaciones e inspecciones | CHG-43 |
| Órdenes de inspección | No generan guía | `GuideType.Inspection` lo documenta | CHG-33, CHG-90 |
| Búsqueda de placa desde la barra superior | Abre la trazabilidad con «Todo el historial» | La ficha exige que la búsqueda encuentre la placa | CHG-81 |
| Datos de la empresa en los documentos | Parámetros del sistema sembrados con el pie del legacy, editables por el Admin | Único origen documentado; se corrigen sin desplegar | CHG-84 |
| Ciclo OnDemand de configuraciones existentes | El valor se conserva para leer filas antiguas y no se ofrece ni se acepta | §10 · OnDemand se retira, sin migración de datos | CHG-60 |
| Alta de vehículos y conductores | Vigilancia, Báscula, Admin y Comercio Exterior (desde la orden de cargue) | §10 · Permisos de catálogos sin retroceso (regla 4.0.10): Comercio Exterior ya crea vehículos y conductores en su flujo | CHG-03 |
| Corrección de pesos por Facturación | Desde el detalle del ciclo, no desde el historial | La matriz de páginas de la fase 9 de QA no da a Facturación el historial de báscula | CHG-47 |
| Rechazo de un pago | Confirmación con monto, referencia y factura, sin motivo obligatorio | El API no exige motivo (`RejectPaymentRequest(string? Reason)`, `BillingController.cs:739`) y la ficha pide confirmación | CHG-18 |
| Fechas de los PDF que replican el legacy | Conservan su formato (`yyyy-MM-dd HH:mm:ss`) | Son réplicas del legacy del plan de paridad; la ficha trata las pantallas | CHG-88 |
| «Facturación por CPI» en el menú | Se conserva | Vocabulario del negocio heredado del legacy; ninguna ficha lo pide | CHG-90 |
| Fecha del reporte de ingresos diarios | Se conserva la fecha de creación del depósito | La ficha trata placa, tiquete y peso, no la fecha | CHG-82 |
| Asterisco de obligatorio en las etiquetas | No se agrega | `LabelBase` no lo dibuja en ninguno de sus usos; las diez etiquetas quedan como las demás | CHG-85 |

## 6. Observaciones no incluidas

Una observación (OBS) entra al plan solo si una decisión del usuario la convirtió en requisito; eso ocurrió con dos, que hoy son fichas. Las demás quedan fuera como requisito. Algunas se corrigen igual porque comparten causa con un defecto del plan; en ese caso la columna «Destino» dice qué cambio las cubre, y su verificación es la del caso detector de ese cambio.

| OBS | Destino | Justificación |
|---|---|---|
| OBS-F0-001 | No incluida | El comportamiento es el correcto (vuelve al login); el mensaje solo aparece en la consola. |
| OBS-F0-002 | Cubierta por CHG-86 | El título del aviso global deja de ser «Error 400» (misma causa que DEF-F10-003). |
| OBS-F0-003 | No incluida | No se reprodujo aislada; F0-LOG se repite en la fase 11 de QA con CHG-87 y CHG-86 aplicados. |
| OBS-F0-004 | Cubierta por CHG-87 | Es el 404 en inglés de DEF-F10-005. |
| OBS-F0-005 | Cubierta por CHG-89 | Son los botones de solo ícono de DEF-F10-008. |
| OBS-F0-006 | Cubierta por CHG-16 | Es el token vigente después de cerrar sesión de DEF-F1-009. |
| OBS-F0-007 | No incluida | Advertencias de Vue del modo desarrollo, sin efecto funcional; el build de producción no las emite. |
| OBS-F0-008 | Cerrada por §10 | §10 · Sin menú directo a Convenios. |
| OBS-F1-001 | No incluida | Mensaje genérico sin pérdida de datos; ninguna decisión lo convirtió en requisito. |
| OBS-F1-002 | No incluida | Bloqueo por intentos fallidos es una política de seguridad nueva que requiere decisión del usuario. |
| OBS-F1-003 | Cubierta en parte por CHG-84 | Los parámetros `COMPANY_*` se siembran; el alta de parámetros y la validación de correo no tienen ficha. |
| OBS-F1-004 | No incluida | El código de la unidad es inmutable por diseño; el aviso sería una mejora de interfaz. |
| OBS-F1-005 | No incluida | Activar y desactivar embalajes es funcionalidad nueva sin decisión. |
| OBS-F1-006 | No incluida | Mejora de búsqueda sin ficha; la búsqueda global ya ignora tildes. |
| OBS-F1-007 | No incluida | Cambio de contraseña voluntario y recuperación para todos son funcionalidad nueva sin decisión. |
| OBS-F1-008 | No incluida | Texto genérico correcto, sin impacto. |
| OBS-F1-009 | No incluida | Comportamiento documentado del motor de tarifas (MAF-08). |
| OBS-F1-010 | No incluida | El catálogo de fórmulas sigue el diseño vigente del motor de tarifas. |
| OBS-F1-011 | Cubierta por CHG-48 | Mensajes genéricos fuera de Development y Azure en Production. |
| OBS-F2-001 | No incluida | Texto y manual desactualizados; se corrige en la documentación de usuario, sin ficha. |
| OBS-F2-002 | No incluida | CHG-05 conserva a propósito el ingreso de un vehículo inactivo (`CreateEntryLogHandler.cs:66`). |
| OBS-F2-003 | Cubierta por CHG-86 | Es la duplicación de avisos de DEF-F10-003. |
| OBS-F2-004 | No incluida | El detalle de cada campo viaja en la lista de errores de la respuesta y la pantalla lo muestra. |
| OBS-F2-005 | Cubierta por CHG-52 | Ya no se aceptan fechas de ingreso futuras. |
| OBS-F3-001 | No incluida | Atribuida a la automatización; se confirma con teclado real al cronometrar PRF-002 (§7.3). |
| OBS-F3-002 | Cubierta por CHG-88 | Es el separador de miles de DEF-F10-006. |
| OBS-F3-003 | No incluida | El texto legal y el desglose del tiquete requieren decisión del usuario; ninguna ficha lo pide. |
| OBS-F3-004 | Cubierta por CHG-17 | La violación de `idx_weighbridge_weighing_cycle_sequence` responde «Este pesaje ya fue registrado. Actualice la pantalla.». |
| OBS-F3-005 | Cubierta en parte por CHG-90 | «Pesaje #0 (Gross)» pasa a «Pesaje 1 (Bruto)»; el rótulo «80 unidades» del resumen de la orden no tiene ficha. |
| OBS-F3-006 | No incluida | Dato secundario del conductor sin efecto en cobros ni documentos. |
| OBS-F3-007 | No incluida | Por diseño la fecha del depósito es la del primer camión (decisión de la Ola 1). |
| OBS-F3-008 | Cubierta por CHG-09 | Es la escalera que deja pasar reglas de otra modalidad (DEF-F6-001). |
| OBS-F4-001 | Convertida en DEF-F4-018 | Decisión del usuario del 2-oct (§10 · Inventario de Bodega con Borradores); la corrige CHG-74. |
| OBS-F4-002 | Cubierta en parte por CHG-78 y CHG-88 | El Excel trae usuario y motivo y la fecha sale en formato es-CO; la placa y la guía en las salidas no tienen ficha. |
| OBS-F4-003 | No incluida | Mejora de navegación; el botón existe en la tarjeta del listado. |
| OBS-F4-004 | No incluida | Textos de ayuda menores sin ficha. |
| OBS-F4-005 | No incluida | Una inspección de un solo pesaje no tiene neto físico de camión por diseño. |
| OBS-F4-006 | No incluida | Limitación del ambiente local; el correo se verifica en staging (bloque STG). |
| OBS-F4-007 | No incluida | Diferencia de centavos solo por API con valores no enteros; la pantalla coincide con la factura. |
| OBS-F5-001 | Convertida en DEF-F5-014 | Decisión del usuario del 2-oct (§10 · Ninguna mercancía de importación sale sin guía); la corrige CHG-33. |
| OBS-F5-002 | Cerrada por §10 | §10 · Una OC puede llevar parte de una unidad de carga. |
| OBS-F5-003 | No incluida | El vencimiento se calcula por diseño con los días de tránsito de la ciudad; CHG-34 corrige el texto de la pantalla. |
| OBS-F5-004 | No incluida | Definir los terceros de la etiqueta de inspección requiere decisión del usuario; ninguna ficha lo pide. |
| OBS-F5-005 | Cubierta por CHG-70 | La plantilla se guarda y la validación es única (DEF-F5-008). |
| OBS-F5-006 | No incluida | Decisión de la Ola 1: la TRM manual solo aplica cuando la DIAN no responde (§10 · TRM pendiente con mínimo y TRM manual). |
| OBS-F5-007 | No incluida | Mejora de presentación sin ficha. |
| OBS-F5-008 | Cubierta por CHG-34 | La lista de órdenes pendientes muestra todos los clientes dueños. |
| OBS-F6-001 | No incluida | Qué cuentan los indicadores del tablero de Facturación requiere decisión del usuario. |
| OBS-F6-002 | No incluida | La pantalla ordena las notificaciones; sin impacto. |
| OBS-F6-003 | Cubierta por CHG-73 | Es la agencia «N/A» de DEF-F5-010. |
| OBS-F6-004 | No incluida | Duplicados por reimportar listas de empaque, sin ficha; requiere decidir si la lista reutiliza productos existentes. |
| OBS-F6-005 | No incluida | Confirmar cómo se combina el mínimo de modalidad con una tarifa base requiere decisión del usuario. |
| OBS-F6-006 | No incluida | Es configuración del ambiente (correos de administradores), no un defecto de código. |
| OBS-F6-007 | Cubierta por CHG-33 | Son salidas de importación sin guía (DEF-F5-014). |
| OBS-F7-001 | Cerrada por §10 | §10 · Reporte de ingresos diarios: solo Confirmados y Cerrados. |
| OBS-F7-002 | Cerrada por §10 | §10 · Facturación accede al inventario general. |
| OBS-F7-003 | No incluida | Qué cuenta la facturación anual requiere decisión del usuario (igual que OBS-F6-001). |
| OBS-F7-004 | No incluida | Funcionalidad pendiente del plan de paridad (§G.13), fuera del alcance de las fichas. |
| OBS-F7-005 | No incluida | Nota sobre datos de prueba; no hay cambio de código. |
| OBS-F7-006 | Cubierta por CHG-59 | Es el PATCH de unidad de medida que desactiva lo que no se envía. |
| OBS-F8-001 | Cerrada por §10 | §10 · Mora bloquea el cierre del montacargas, no su inicio. |
| OBS-F8-002 | No incluida | Las fechas retroactivas son una premisa del negocio (fechas editables); CHG-52 solo impide las futuras. |
| OBS-F8-003 | No incluida | La factura conserva el destinatario con que se emitió; cambiarlo requiere decisión del usuario. |
| OBS-F8-004 | No incluida | Qué cuenta la cartera del tablero requiere decisión del usuario (igual que OBS-F6-001). |
| OBS-F8-005 | Cubierta por CHG-13 | El log informa solo transiciones reales. |
| OBS-F8-006 | Cerrada por §10 | §10 · Anular pesaje cobrado: la factura sigue pagada. |
| OBS-F9-001 | Cerrada por §10 | §10 · Catálogos sin autenticación aceptados. |
| OBS-F9-002 | No incluida | Mover los tokens fuera de `localStorage` es un endurecimiento que requiere decisión; CHG-16 ya revoca los tokens al cerrar sesión o desactivar. |
| OBS-F9-003 | Cerrada en parte por §10 | §10 · Permisos (convenios y tarifas: Admin y Facturación); que los roles operativos creen embalajes no tiene ficha. |
| OBS-F9-004 | No incluida | Sin ficha y sin efecto funcional observado. |
| OBS-F9-005 | No incluida | Endpoint de administración sin ficha. |
| OBS-F10-001 | No incluida | Texto de ayuda de la búsqueda de conductor, sin ficha. |
| OBS-F10-002 | No incluida | Mejora del texto «Falta 1 dato», sin ficha. |
| OBS-F10-003 | No incluida | El control de concurrencia optimista es funcionalidad nueva sin decisión. |
| OBS-F10-004 | Cubierta por CHG-86 | Los 404 dejan de reintentarse. |
| OBS-F10-005 | Cubierta por CHG-86 | Al volver el API, las consultas se refrescan solas. |
| OBS-F10-006 | No incluida | Presentación a 1024 px; las «6611 h» vienen de un camión de prueba con fecha de 2025. |
| OBS-F10-007 | No incluida | Datos de QA; desaparecen al recrear la base (§7.3). |
| OBS-F10-008 | No incluida | Atribuida a la automatización; se confirma con teclado real al cronometrar PRF-002 (§7.3). |
| OBS-F10-009 | Pendiente PRF-002 | Es la medición con el operario de §7.3. |

**Hallazgos de la verificación sin ficha.** El plan corrige tres porque comparten causa con un defecto: los PATCH de cinco catálogos que desactivan o borran lo que no se envía (CHG-59); la corrección de primer y segundo peso invertida en `ModifyWeighingDialog.vue:57` (dentro de CHG-37); y las fechas de la factura y del tiquete impresas sin la hora de Colombia (dentro de CHG-84). Queda fuera uno sin síntoma reportado: el detalle de depósitos de exportación e inspección busca el ciclo por el servicio ancla (`GetExportDepositDetailHandler.cs:111`, `GetInspectionDepositDetailHandler.cs:80`), la misma suposición que CHG-82 corrige en el reporte. Los cuatro pueden registrarse como fichas nuevas para su seguimiento.

## 7. Plan de re-test y cierre

### 7.1 Re-test al cerrar cada fase

1. El implementador termina los cambios en el «Orden interno» y deja las compuertas comunes en verde (regla 4.0.4). El usuario revisa el checkpoint y hace los commits.
2. Después del commit, el implementador actualiza cada ficha cerrada: «Estado» = «Corregido» y una fila de historial «Corregido · commits FE/BE · CHG-NN».
3. QA ejecuta en la base local, para cada defecto de la fase: el caso detector y los casos de la columna «Re-test QA» del cambio (paso 1 del bloque RET de la fase 11 de QA), los P0 del mismo bloque (paso 2) y los casos REG indicados. Marca cada ficha «Verificado» o «Reabierto» con evidencia (paso 3).
4. Los casos que necesitan vencer fechas (mora, vencimientos y renovaciones: F6-CAR-*, F6-JOB-*, F6-ALM-008, E2E-12, E2E-13) usan las palancas de tiempo `resultados/f6_palanca1.sql`, `resultados/f6_palanca2.sql` y `resultados/f8_palanca_mora.sql` **solo en la base local**.
5. Un defecto reabierto vuelve a su cambio dentro de la misma fase; la fase siguiente no empieza mientras haya reabiertos CRITICAL o MAJOR de la fase.

### 7.2 Cierre: fase 11 de QA

- **Entrada:** las 12 fases cerradas; las 126 fichas en «Corregido» o «Verificado», salvo DEF-F8-001, que se cierra con DEF-F3-002; decisión de la base tomada (§7.3).
- **Ejecución:** `docs/qa/fase-11-regresion-cierre.md` completa: RET de las 126 fichas por severidad (primero los 13 CRITICAL de las Fases 1 a 3), suite REG F11-REG-001 a F11-REG-031, regresión dirigida (DIR) con el `git log` de cada módulo, pruebas automatizadas F11-AUT-001 a F11-AUT-003 (ahora con `Wms.IntegrationTests` y `yarn test`) y STG en staging cuando el usuario despliegue el build candidato con `scripts/deploy-staging.sh`.
- **Salida:** la de la fase 11 de QA: REG 100 % ejecutada sin FALLA en P0, cero CRITICAL abiertos e informe final con la recomendación go/no-go.
- **Producción:** ningún script de saneamiento, migración ni cambio de infraestructura de este plan se aplica en producción sin la aprobación escrita del usuario.

### 7.3 Pendientes que no son código (no bloquean fases)

| Pendiente | Responsable y momento | Recomendación |
|---|---|---|
| PRF-002: cronometrar con el operario de báscula el registro de un camión hasta el primer peso (meta de unos 30 s, DF2; con un conductor nuevo la ficha pide 11 datos y con uno conocido se precargan 4) | El usuario, en el checkpoint de la Fase 4 (después de los bloqueos de CHG-17) y otra vez en la fase 11 de QA | Anotar el tiempo de tres camiones en el informe final; si la mediana supera 30 s, abrir una ficha nueva con el paso más lento. |
| Base de datos para la fase 11 de QA: recrearla con el dataset maestro o conservar la base de QA | El usuario, antes de iniciar la fase 11 de QA | Recrearla: la base de QA arrastra duplicados, estados forzados y datos de prueba que los scripts solo detectan; con la base nueva el bloque de corrección de cada script se omite y su detección queda como verificación (regla 4.0.3). Alternativa: conservar la base de QA y aplicar en orden los bloques de corrección de los scripts de las 12 fases. |

## Autocontrol

- [x] **Cobertura:** los 126 IDs de `INDICE.md` aparecen una sola vez en la matriz (§3): 125 en un cambio y DEF-F8-001 como duplicado de DEF-F3-002. El conteo por destino suma 126.
- [x] **Orden por severidad:** los 13 CRITICAL están en las Fases 1 a 3; los MAJOR, en las Fases 4 a 7; los MINOR y TRIVIAL, en las Fases 8 a 12, salvo los que cierra el mismo cambio que un defecto de mayor severidad (regla 4.0.5).
- [x] **Sin palabras prohibidas** en todo el documento.
- [x] **Sin dependencias hacia adelante:** cada dependencia de un cambio está en una fase anterior o antes en el orden interno de su fase.
- [x] **Tarjetas completas:** todo cambio tiene causa raíz con `archivo:línea`, cambio exacto, migración o script, pruebas automatizadas, criterios Dado/Cuando/Entonces con valores concretos, re-test QA (caso detector y REG), riesgo, tamaño y dependencias.
- [x] **Tamaño de las fases:** ninguna pasa de 12 cambios.
- [x] **Sin retrocesos:** ningún rol pierde una función que usa hoy en sus pantallas (regla 4.0.10; verificado en CHG-03 contra las pantallas que llaman cada endpoint restringido).
- [x] **§10:** ningún cambio lo contradice; cada aplicación se cita como «§10 · tema» y las observaciones que el §10 cierra están en §6.
- [x] **Credenciales:** no se copió ninguna contraseña, token ni clave del README ni de los ambientes.
