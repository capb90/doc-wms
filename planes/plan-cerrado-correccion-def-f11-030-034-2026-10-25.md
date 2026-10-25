# Plan cerrado — Corrección de DEF-F11-030 y DEF-F11-034 antes de la fase 13

> **Fecha:** 25 de octubre de 2026. **Estado:** Aprobado por el usuario el 2026-10-25 (respuestas en §2).
> **Base:** BE `develop` `57c94dd` · FE `develop` `cb2a4f7`, los dos limpios. Es el build de la ronda QA de preproducción.
> **Origen:** `qa/resultados/PRE-informe-2026-10-25.md` (veredicto «GO con condiciones») y las fichas `qa/resultados/defectos/DEF-F11-030.md` y `DEF-F11-034.md`.
> **Rutas:** `B/` = `Backend/wms-api/`, `F/` = `Frontend/wms/`, `D/` = `docs/`.

---

## 0. Instrucciones para el agente ejecutor

1. Lee primero `B/AGENTS.md` y lo que cita, este plan completo y las dos fichas.
2. Trabaja en `develop`, sin ramas ni commits: el usuario commitea cada fase (`DEC-003`).
3. Una fase por sesión; al terminar, detente con el resumen de §7.
4. **Sin migraciones.** Si `dotnet ef migrations has-pending-model-changes` deja de salir limpio, detente.
5. Si el código contradice este plan, no improvises: detente y junta las dudas en un solo mensaje. Si un caso borde choca con una decisión `Dn`, gana la decisión (`DEC-002`).
6. Las reglas nuevas van en clases o funciones puras, con pruebas en `B/Wms.Tests` o Vitest; lo que depende de EF, en `B/Wms.IntegrationTests`.

---

## 1. Objetivo y alcance

### 1.1 DEF-F11-030 (CRITICAL) — la factura no se recalcula al corregir el depósito

**Hoy:**

- CE devuelve un depósito confirmado a Borrador, corrige y reconfirma.
- La reconfirmación llama a `OpenPeriodWithInvoiceAsync`, que no hace nada si ya hay un período abierto (`B/Wms.Application/Billing/Common/Services/StorageBillingService.cs:428-436`, D13). Está bien que no duplique la factura.
- La edición de productos sí recalcula en el acto, aun en Borrador (`B/Wms.Application/ForeignTrade/Common/Services/DepositProductEditing.cs:80-97`).
- **Correcciones que no recalculan:**
  - **Valor de la mercancía y moneda** (`B/Wms.Application/ForeignTrade/Commands/UpdateDraftDeposit/UpdateDraftDepositHandler.cs:45-48`). Son la base de `PERCENTAGE_OF_VALUE` (T1).
  - **Agencia de aduanas** (`…/UpdateDraftDepositHandler.cs:122-157`). Su nombre va en el detalle de la factura.
  - **Fecha de ingreso en Borrador.** El handler solo recalcula con el depósito `Confirmed` (`…/CorrectDepositEntryDate/CorrectDepositEntryDateCommandHandler.cs:46-53`), y `HandleEntryDateChangedAsync` sale si no lo está (`B/Wms.Application/Billing/Common/Services/StorageRecalculationTrigger.cs:166-167`).
  - **Cliente.** `UpdateDraftDepositHandler:77-120` y `AssignDepositCustomerHandler` (`PATCH foreign-trade/warehouse-storages/{id}/customer`, en `Draft` y `Confirmed`) solo pasan el cliente a las facturas y períodos **huérfanos**. Un depósito que ya tiene factura sigue facturando al cliente anterior y con su convenio, porque el recálculo usa el cliente del período (`RecalculateOpenPeriodAsync`, `stakeholderId = openPeriods[0].StakeholderId`). Esto se leyó en el código; la fase 1 lo confirma con una prueba que hoy falla.
- **La fecha del documento no interviene en la facturación.** En `B/Wms.Application/Billing` solo la usa la lista de pendientes (`GetPendingDepositsHandler.cs:205`). No se toca.

### 1.2 DEF-F11-034 (MAJOR) — mercancía de importación sale sin guía

**Hoy:**

- Bodega ejecuta el cargue de una orden de importación sin guía de salida (`B/Wms.Application/Warehouse/Commands/LoadingOrder/ExecuteLoadingOrderCommandHandler.cs`). La guía puede emitirse antes o después del cargue (`DEC-052`).
- Si el camión no pasó por báscula, la guarda de Vigilancia no ve la orden (`B/Wms.Application/ForeignTrade/Common/Services/LoadingOrderGuideReader.cs:57-76`) y el camión sale sin guía.

**Decisión del usuario:** el control pasa a **Bodega, en el momento del cargue**.

- El conductor solicita la guía en Comercio Exterior antes del cargue.
- El operario de bodega la valida y, sin guía vigente, no carga.
- Vigilancia y Báscula no cambian. Hay una sola salida y un operario para entradas y salidas, así que no se les agrega trabajo y su operación sigue igual de rápida.

### 1.3 Fuera de alcance

- Los MINOR y el TRIVIAL de la ronda (DEF-F11-029, 031, 032 y 033).
- Exportación e inspección: su cargue no cambia. La guía de exportación es automática al cargar y la inspección no lleva guía.
- La guarda de salida de Vigilancia: queda como está, sin búsqueda por vehículo (P2).
- Báscula: no se exige la salida en báscula antes del cargue (P2). Si un camión se salta la báscula, sale con su guía pero sin pesaje de salida y la orden queda `Loaded`. Es el riesgo residual que acepta la operación (§8).
- Datos de staging: sin backfill (`DEC-006`).

---

## 2. Respuestas del usuario (2026-10-25)

| # | Pregunta | Respuesta |
| --- | --- | --- |
| P1 | Cambio de cliente de un depósito con factura de almacenamiento | **(a):** con la factura en Borrador y no consolidada, se reasignan la factura y los períodos al cliente nuevo y se recalcula con su tarifa; en otro estado o consolidada, 409 para que Facturación la anule antes |
| P2 | Cómo cerrar DEF-F11-034 | Ni la guarda por vehículo en Vigilancia ni el requisito de báscula antes del cargue. **Bodega valida la guía al cargar**: una orden de importación sin guía vigente no se carga, y el conductor la solicita en CE en ese momento |

---

## 3. Decisiones

| # | Decisión | Fuente |
| --- | --- | --- |
| **DEF-F11-030** | | |
| D1 | El recálculo corre **en el momento de la corrección**, después del commit, con `StorageRecalculationTrigger`, igual que la edición de productos. La reconfirmación no recalcula: `OpenPeriodWithInvoiceAsync` sigue idempotente (D13). | `DepositProductEditing.cs:80-97`; `DEC-022` |
| D2 | Solo si el depósito tiene **un período `Open`**. Un Borrador que nunca se confirmó no tiene período. | `StorageRecalculationTrigger.RunAsync` |
| D3 | Disparadores en `PATCH foreign-trade/warehouse-storages/{id}/draft`: cambia el **valor**, la **moneda** o la **agencia** respecto de lo que había antes de guardar. El cliente sigue D9. La fecha del documento y las observaciones no disparan nada. | §1.1 |
| D4 | **Regla pura nueva** `DraftCorrectionBillingRules` en `B/Wms.Application/ForeignTrade/Common/Services/DraftCorrectionBillingRules.cs`:<br>• `ChangedBillingFields(previousValue, newValue, previousCurrency, newCurrency, previousAgencyId, newAgencyId)` devuelve, en este orden, los nombres de lo que cambió: «valor de la mercancía», «moneda», «agencia de aduanas». La moneda se compara sin distinguir mayúsculas; un valor `null` en la petición significa «sin cambio».<br>• `Reason(depositNumber, fields)` devuelve «corrección de {campos unidos con ", " y " y "} del depósito {número}». | `B/AGENTS.md` |
| D5 | **TRM al cambiar la moneda:** antes de recalcular, si `storage.IsTrmPending` (pasó a USD sin TRM), se llama `IStorageBillingService.TryAssignDianTrmAsync`, con su espera máxima de siempre. Si la DIAN no responde, queda «TRM pendiente» y el recálculo cae al mínimo con sus avisos (`DEC-020`, `DEC-023`). La TRM existente no se borra: depende solo de la fecha de ingreso, y la única moneda extranjera admitida es USD (`UpdateDraftDepositCommandValidator`, «COP o USD»). | `StorageBillingService.cs:836-856`; `HandleEntryDateChangedAsync:178-179` |
| D6 | **Fecha de ingreso en Borrador:** `CorrectDepositEntryDateCommandHandler` llama a `HandleEntryDateChangedAsync` si el depósito está `Confirmed` **o** está en `Draft` con algún período (`Open` o `Closed`). `HandleEntryDateChangedAsync` acepta `Draft` en ese caso; el resto de su lógica no cambia. El resultado `billingNotified` queda `true` cuando se llamó. | §1.1 |
| D7 | Avisos y auditoría: los de `RunAsync`, sin cambios.<br>• Factura en Borrador: sin aviso, salvo una sobrescritura descartada (F6-REC-003).<br>• Aprobada, enviada o con pagos: conserva el número y avisa con el total anterior y el nuevo (F6-REC-004/005).<br>• Anulada: no se toca y avisa «Cambio de depósito sin facturar» (F6-REC-006).<br>• La descripción de auditoría lleva el motivo de D4. | `DEC-022`; `StorageRecalculationTrigger.cs:260-291` |
| D8 | Un fallo del recálculo **nunca** revierte la corrección: se registra con `LogError` y se avisa a Facturación, como en `DepositProductEditing.AfterCommitAsync`. | `DEC-013` |
| D9 | **Cambio de cliente (P1 a).** **Regla pura** `CustomerChangeBillingRules.Decide(InvoiceStatus? openInvoiceStatus, bool isConsolidated)` en `B/Wms.Application/Billing/Common/Services/CustomerChangeBillingRules.cs`. Devuelve:<br>• `Reassign`: la factura del período abierto está en `Draft` y no es consolidada;<br>• `Block`: la factura está en otro estado distinto de `Cancelled`, o es consolidada;<br>• `PeriodsOnly`: no hay período abierto o su factura está anulada; solo se reasignan los períodos por refacturar. | P1 |
| D10 | Uso de D9 en `UpdateDraftDepositHandler` (cuando `CustomerId` trae un cliente distinto del actual) y en `AssignDepositCustomerHandler`, **antes** de guardar:<br>• `Block` → `ConflictException`: «La factura de almacenamiento {N.º o "sin número"} del depósito {número} está {estado en español}: Facturación debe anularla antes de cambiar el cliente.». No se guarda nada.<br>• `Reassign` → `invoice.AssignCustomer(nuevo)`, que ya admite `Draft`; `period.AssignStakeholder(nuevo)` en los períodos `Open` y en los `Closed` cuya factura está anulada sin refacturar. Después del commit, `RecalculateAsync` con «cambio de cliente del depósito {número}» (D8).<br>• `PeriodsOnly` → `AssignStakeholder` en los períodos `Closed` de factura anulada sin refacturar (la refacturación sale al cliente nuevo); sin recálculo.<br>El estado en español sale de la etiqueta que ya usa el backend para las facturas; si no existe, se agrega en la misma regla pura. | P1; `Invoice.AssignCustomer` (`B/Wms.Domain/Entities/Billing/Invoice.cs:80-95`) |
| D11 | Sin cambios en el contrato del API ni en el frontend para DEF-F11-030. | §1.3 |
| **DEF-F11-034** | | |
| D12 | **Guía antes del cargue de importación.** Regla pura nueva en `ImportGuideRules`: `EnsureLoadingHasGuide(string orderNumber, bool requiresGuide, bool hasActiveGuide)`. Con `requiresGuide && !hasActiveGuide` lanza `ConflictException`: «No se puede cargar la orden {OC}: es de importación y no tiene guía de salida vigente. El conductor debe solicitar la guía en Comercio Exterior antes del cargue.». | P2; `ImportGuideRules.cs` |
| D13 | `ExecuteLoadingOrderCommandHandler` lee `LoadingOrderGuideReader.ReadAsync` (`RequiresGuide`, `HasActiveGuide`) y llama a D12 **antes** de mover stock, junto a sus demás validaciones. Sin cambios para exportación e inspección (`RequiresGuide` es falso). | `LoadingOrderGuideReader.cs:18-28` |
| D14 | La guía que difiere de lo cargado sigue como hoy (`DEC-052`): el cargue parcial con guía vigente se permite y avisa a CE para que la anule y la emita de nuevo. | `DEC-052`; F5-GUI-018 |
| D15 | El aviso «Guía de salida requerida» y la lógica `AwaitsGuide` del cargue no se quitan: siguen sirviendo para órdenes `Loaded` sin guía de antes del despliegue. Con D12 ya no se generan casos nuevos. | `ExecuteLoadingOrderCommandHandler.cs:360, 441` |
| D16 | **Bodega ve la guía antes de cargar.** `GET warehouse/loading-orders/pending` (`B/Wms.Application/Warehouse/Queries/GetPendingLoadingOrders/GetPendingLoadingOrdersHandler.cs`) llena en cada `LoadingOrderDto`:<br>• `ActiveDispatchGuideNumber`: la guía vigente, el campo que ya existe;<br>• `RequiresDispatchGuide` (bool, **nuevo** en `LoadingOrderDto`): si algún ítem es de un depósito `IMP*`, con `ImportGuideRules.RequiresGuide`.<br>Las dos con consultas por lote para toda la página, sin una consulta por orden. | P2 («el operario de bodega puede validar la guía») |
| D17 | **Frontend: función pura nueva** `F/app/features/warehouse/utils/loading-guide-gate.ts`, `loadingGuideGate(requiresGuide, guideNumber)`, que devuelve `{ canLoad, severity, message }`:<br>• exige guía y la tiene → `canLoad: true`, `success`, «Guía de salida {N.º} vigente. Verifíquela con el conductor.»;<br>• exige guía y no la tiene → `canLoad: false`, `warn`, «Esta orden es de importación y no tiene guía de salida vigente. El conductor debe solicitarla en Comercio Exterior antes del cargue.»;<br>• no exige guía → `canLoad: true`, sin mensaje (`message: null`). | P2 |
| D18 | `F/app/features/warehouse/components/LoadingOrderExecutionDialog.vue` muestra el mensaje de D17 (`Message`, sin cerrar) arriba de los datos del cargue, y suma `gate.canLoad` a `canSubmit`. Sin guía, «Ejecutar Cargue» queda deshabilitado. El 409 de D12 es la defensa del backend (otra pestaña o la guía anulada en el intermedio). Tipo: `requiresDispatchGuide?: boolean` en `F/app/features/warehouse/types/loading-order.ts`. | P2 |
| D19 | **Decisión nueva para `D/contexto/decisiones.md`** (fase 4): **DEC-056 — Guía antes del cargue de importación** (2026-10-25). «Bodega no ejecuta el cargue de una orden de importación sin guía de salida vigente; el conductor la solicita en Comercio Exterior antes del cargue y el operario de bodega la valida en la pantalla del cargue. Vigilancia y Báscula no agregan controles: una sola salida y un operario. Precisa `DEC-052`: la guía ya no puede emitirse después del cargue. Exportación e inspección no cambian.» Se anota también el cambio de cliente de D9/D10 en la misma entrada. | P1, P2 |

---

## 4. Archivos

### 4.1 Fase 1 — DEF-F11-030 (backend)

| Archivo | Cambio |
| --- | --- |
| **Nuevo** `B/Wms.Application/ForeignTrade/Common/Services/DraftCorrectionBillingRules.cs` | D4 |
| **Nuevo** `B/Wms.Application/Billing/Common/Services/CustomerChangeBillingRules.cs` | D9 |
| `B/Wms.Application/ForeignTrade/Commands/UpdateDraftDeposit/UpdateDraftDepositHandler.cs` | Toma valor, moneda, agencia y cliente previos. Antes de guardar: D10 si cambia el cliente. Después de guardar: si hay campos de D4 y un período `Open` (D2), D5 y `RecalculateAsync(storageId, Reason, ct)`; si D10 dio `Reassign`, el recálculo de D10. Un solo recálculo si se cumplen los dos, con los motivos unidos por « y ». Todo con `try/catch` (D8) |
| `B/Wms.Application/ForeignTrade/Commands/AssignDepositCustomer/AssignDepositCustomerHandler.cs` | D10 |
| `B/Wms.Application/ForeignTrade/Commands/CorrectDepositEntryDate/CorrectDepositEntryDateCommandHandler.cs` | D6 (condición de llamada) |
| `B/Wms.Application/Billing/Common/Services/StorageRecalculationTrigger.cs` | D6 (`HandleEntryDateChangedAsync` acepta `Draft` con período) |

### 4.2 Fase 2 — DEF-F11-034 (backend)

| Archivo | Cambio |
| --- | --- |
| `B/Wms.Application/ForeignTrade/Common/Services/ImportGuideRules.cs` | D12 |
| `B/Wms.Application/Warehouse/Commands/LoadingOrder/ExecuteLoadingOrderCommandHandler.cs` | D13 |
| `B/Wms.Application/Warehouse/Common/DTOs/LoadingOrderDto.cs` | `RequiresDispatchGuide` (D16) |
| `B/Wms.Application/Warehouse/Queries/GetPendingLoadingOrders/GetPendingLoadingOrdersHandler.cs` | D16 |
| `B/Wms.IntegrationTests/ForeignTrade/ImportExitScenario.cs` | `ExecuteLoadingAsync` gana `bool ensureGuide = true`: si la orden es de importación y no tiene guía vigente, la emite con `CreateGuideOkAsync` antes de cargar. La prueba negativa pasa `ensureGuide: false`. Las pruebas que emitían la guía **después** del cargue quitan esa llamada (ya la emitió el ayudante); si una aserción dependía del orden, se ajusta y se anota en el resumen |
| Pruebas cuyo punto de partida es «orden de importación cargada sin guía» (`ImportExitRequiresGuideTests`: `CloseExitWeighing_ImportOrderWithoutGuide_Returns409`, `RegisterDeparture_ImportOrderLoadedWithoutGuide_Returns409`, `LoadedImportOrder_WithEntryTicketAndNoGuide_AwaitsGuide`, `PendingGuideOrders_IncludeDispatchedWithoutGuide`) | Siembran ese estado en la base (`ExecuteUpdateAsync` sobre la orden, el stock y el kárdex, como las órdenes `Loaded` de antes del despliegue) en lugar de cargar por el API. Sus aserciones no cambian: prueban las guardas que siguen vigentes (D15) |
| `ImportExitRequiresGuideTests.LoadAfterEntryTicketExit_WithoutGuide_StaysLoaded_ThenGuideDispatches` | Se reemplaza por `LoadAfterEntryTicketExit_WithGuide_Dispatches`: guía, tiquete de ingreso y cargue → `Dispatched` al cargar |

### 4.3 Fase 3 — DEF-F11-034 (frontend)

| Archivo | Cambio |
| --- | --- |
| **Nuevo** `F/app/features/warehouse/utils/loading-guide-gate.ts` | D17 |
| `F/app/features/warehouse/types/loading-order.ts` | `requiresDispatchGuide?: boolean` |
| `F/app/features/warehouse/components/LoadingOrderExecutionDialog.vue` | D18 |
| **Nuevo** `F/test/unit/warehouse/loading-guide-gate.spec.ts` | Los tres casos de D17 y un `guideNumber` con espacios (se recorta, como en `orderActionsWithGuide`) |

---

## 5. Pruebas

### 5.1 `Wms.Tests`

- **Nuevo** `B/Wms.Tests/ForeignTrade/DraftCorrectionBillingRulesTests.cs`:
  - solo valor;
  - valor y moneda;
  - moneda igual con otra capitalización: sin cambio;
  - campos `null`: sin cambio;
  - solo agencia;
  - texto exacto de `Reason` con uno, dos y tres campos.
- **Nuevo** `B/Wms.Tests/Billing/CustomerChangeBillingRulesTests.cs`:
  - `Draft` → `Reassign`;
  - consolidada → `Block`;
  - `PendingApproval`, `Approved`, `Sent`, `PartiallyPaid`, `Paid`, `Overdue` → `Block`;
  - anulada o sin factura → `PeriodsOnly`.
- `B/Wms.Tests/ForeignTrade/ImportGuideRulesTests.cs` (existe) suma `EnsureLoadingHasGuide`:
  - importación sin guía → 409 con el texto de D12;
  - importación con guía, exportación e inspección → no lanza.

### 5.2 `Wms.IntegrationTests`

- **Nuevo** `B/Wms.IntegrationTests/ForeignTrade/DraftCorrectionRecalculationTests.cs`, con `BillingScenario`, la tarifa base `PERCENTAGE_OF_VALUE` y `FakeDianTrmService` (`B/Wms.IntegrationTests/Infrastructure/TestDoubles.cs`):
  1. Confirmar con USD 10.000, devolver a Borrador, `PATCH …/draft` con 20.000 → la factura del período sube al doble, sigue siendo una sola y en Borrador. **Hoy falla** (reproduce DEF-F11-030).
  2. Confirmar en COP, devolver, cambiar a USD → TRM de la DIAN asignada y factura recalculada con ella.
  3. Lo mismo con la fecha de ingreso en `FakeDianTrmService.UnavailableDates` → «TRM pendiente», factura al mínimo, aviso.
  4. Factura aprobada con N.º: devolver, corregir el valor → misma factura y número, total nuevo, aviso con el anterior y el nuevo.
  5. `PATCH …/draft` en un depósito que nunca se confirmó → sin períodos y sin facturación.
  6. Corregir la fecha de ingreso con el depósito devuelto a Borrador → período rebasado (D6).
  7. Cambio de cliente con la factura en Borrador → factura y períodos al cliente nuevo, con su convenio. **Hoy falla.**
  8. Cambio de cliente con la factura aprobada → 409 con el texto de D10 y nada cambia, por `PATCH …/draft` y por `PATCH …/customer` (en `Confirmed`).
  9. Cambio de cliente con la factura anulada sin refacturar → al refacturar, la factura sale al cliente nuevo.
- **Nuevo** `B/Wms.IntegrationTests/ForeignTrade/LoadingRequiresGuideTests.cs` (D12, D13, D16):
  - importación sin guía → 409, sin movimiento de stock ni reserva liberada;
  - con guía → 200;
  - con guía anulada → 409;
  - exportación e inspección sin guía → 200;
  - `GET warehouse/loading-orders/pending` trae `requiresDispatchGuide` y `activeDispatchGuideNumber` correctos para una orden de importación con y sin guía y para una de exportación.
- Siguen en verde, con los ajustes de §4.2:
  - `ImportExitRequiresGuideTests`, `ExportAndInspectionExitTests`, `GuideLoadMismatchNoticeTests`;
  - `LoadingOrderConcurrencyTests`, `DailyOutgoingGoodsTests`, `StakeholderExitBlockTests`;
  - `ExitReweighRequiresLoadingTests`, `HistoryTicketFilterTests`, `DepartureGuardTests`;
  - `StorageRecalculationDispatchTests`, `StorageRenewalAtPeriodStartTests`, `DepletedInGraceRenewalTests`.

### 5.3 QA (fase 4)

- **`D/qa/fase-05-comercio-exterior.md`:**
  - F5-COR-002 pasa a «la factura del período se recalcula con lo corregido (valor, moneda, agencia, cliente o productos), sin duplicarse»;
  - **nuevos** F5-COR-007 «Corregir valor o moneda en Borrador recalcula la factura» y F5-COR-008 «Cambiar el cliente con factura de almacenamiento»;
  - F5-GUI: la guía de importación se emite antes del cargue.
- **`D/qa/fase-04-bodega.md`:**
  - **nuevo** F4-CAR-016 «Cargue de importación sin guía: el diálogo lo avisa y no deja ejecutar; por API, 409»;
  - **nuevo** F4-CAR-017 «Cargue con guía: el diálogo muestra el número vigente»;
  - F4-CAR-001/002: la guía es previa al cargue (DEC-056).
- **`D/qa/fase-08-e2e.md`:** E2E-01 (pasos 11 y 12), E2E-02, E2E-10 y E2E-11 emiten la guía antes del cargue.
- **Re-test local** sobre `wms_qa_preprod`, la copia de la ronda que se conserva:
  - E2E-11 paso 3, F5-COR-002, F5-COR-007/008;
  - F4-CAR-016/017 en la pantalla de Bodega;
  - PRE-B2-SAL-01 (el cargue sin guía ya no ocurre);
  - E2E-01 y E2E-17 completos con el orden nuevo.
- El re-test se anota como anexo de `D/qa/resultados/PRE-informe-2026-10-25.md`.

---

## 6. Fases

| Fase | Contenido | Criterio de salida |
| --- | --- | --- |
| 1 | DEF-F11-030: D1–D11 (backend) | Compuertas de backend; pruebas 1 y 7 de §5.2 en verde (antes fallaban); ficha DEF-F11-030 en «Corregido» |
| 2 | DEF-F11-034 backend: D12–D16 y el ajuste de las pruebas de §4.2 | Compuertas de backend; las pruebas que cargan siguen en verde; ficha DEF-F11-034 en «Corregido» (parte backend) |
| 3 | DEF-F11-034 frontend: D17–D18 | Compuertas de frontend; diálogo verificado en local con una orden de importación con y sin guía |
| 4 | QA y documentación: §5.3, DEC-056 (D19) en `D/contexto/decisiones.md`, fichas en «Verificado» si pasan, `D/qa/resultados/defectos/INDICE.md`, `D/planes/registro-ejecucion-brechas-p1-2026-10-24.md` y el estado de este plan | Casos en PASA; anexo del informe con veredicto |

Después sigue la fase 13 del plan P1, con la aprobación del usuario paso a paso. Este plan no agrega migraciones a esa lista. **Aviso para la fase 13:** desde el despliegue, CE debe emitir la guía de importación antes de que Bodega cargue. Conviene comunicarlo a los operarios de CE y Bodega y al de Vigilancia (el conductor pide la guía antes de cargar).

---

## 7. Compuertas y entrega de cada fase

- **Backend (fases 1 y 2):**
  - `dotnet build Wms.sln` sin errores;
  - `dotnet test Wms.Tests` y `dotnet test Wms.IntegrationTests` (con Docker) en verde. En la suite completa siguen fallando solo las 2 de la línea base: `InitiateCustomerIdTests.Queue_PendingService_ReturnsCustomerId` y `DiscardOperationTests.Discard_ReleasesTruckToNotStarted`;
  - `dotnet ef migrations has-pending-model-changes` limpio.
- **Frontend (fase 3):**
  - `yarn build` con código 0;
  - `yarn test` en verde;
  - `yarn lint` con igual o menos errores que al empezar y ninguno en archivos nuevos.
- **Entrega:** conteos antes y después, archivos tocados, desviaciones y el mensaje de commit propuesto por repo.

---

## 8. Riesgos

| Riesgo | Mitigación |
| --- | --- |
| La operación cargaba antes de emitir la guía de importación | Es la decisión del usuario (P2, DEC-056). El diálogo de Bodega lo explica antes de intentar, y el 409 dice qué hacer. Aviso a los operarios en la fase 13 (§6) |
| Cargue parcial con la guía emitida por lo pedido | Sigue `DEC-052`: aviso a CE para anular y reemitir (D14) |
| Un camión que se salta la báscula sale con guía pero sin pesaje ni cobro de báscula, y la orden queda `Loaded` | Riesgo residual aceptado: Vigilancia y Báscula no agregan controles (P2). Queda anotado en DEC-056 |
| Ajustar ~17 pruebas que cargan | Ayudante `ExecuteLoadingAsync(ensureGuide: true)` y siembra directa para las que prueban guardas de órdenes sin guía (§4.2) |
| El recálculo en Borrador avisa de más | En Borrador no avisa (D7) |
| La consulta de la TRM demora el `PATCH` | Misma espera máxima de `EnsureTrmAsync`, solo cuando la moneda pasa a USD sin TRM (D5) |
| P1 cambia el destinatario de una factura | Solo en `Draft` no consolidada; en los demás casos, 409 y Facturación decide (D9, D10) |

---

## 9. Estado de las fases

| Fase | Estado | Notas |
| --- | --- | --- |
| 1 | Hecha el 2026-10-25: BE `b8c600e`; el cambio de agencia, sin commit | Wms.Tests 1981 → 2004; Wms.IntegrationTests 415/417 → 425/427 (las 2 de la línea base); modelo sin cambios. Agregado a pedido del usuario: el cambio de agencia por `PUT …/stakeholders` (el que usa la pantalla de CE) también recalcula (`UpdateDepositStakeholdersHandler`). Desviación por D10: `ReissueInvoiceCommandHandler` toma el cliente de los períodos (`CustomerChangeBillingRules.ReissueCustomer`) para que la refacturación salga al cliente nuevo; los períodos `Open` con la factura anulada también pasan al cliente nuevo |
| 2 | Pendiente | — |
| 3 | Pendiente | — |
| 4 | Pendiente | — |
