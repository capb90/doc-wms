# 05 · Registro de brechas

> Auditoría estática del 2026-10-23 (AG-05). **Prefijos:** `L/` = `bodegas-legacy/`, `B/` = `Backend/wms-api/`, `F/` = `Frontend/wms/app/`, `FT/` = `Backend/wms-api/Wms.Application/ForeignTrade/`.
> Antes de registrar cada brecha se revisaron `docs/qa/resultados/defectos/INDICE.md` (fichas DEF-F5-*, DEF-F8-*, DEF-F10-001, DEF-F11-*), `docs/planes/migracion-staging/resultados/defectos/` y `docs/contexto/estado.md` §4. Donde hay antecedente se cita. No se registran como brecha las diferencias con decisión (van como `DIFERENCIA_INTENCIONAL` en la matriz) ni las ya registradas por otros módulos: BR-02-001 (la salida de báscula exige una orden previa), BR-03-002 (`POST warehouse/loading-orders` sin consumidor) y BR-03-003 (autorizaciones de salida inalcanzables).

## Resumen

| ID | Capacidad | Título | Categoría | Criticidad |
| --- | --- | --- | --- | --- |
| BR-05-001 | CF-L159.a, CF-L158, CF-L163.a | Cancelar o modificar una orden con guía vigente no anula ni ajusta la guía ni su factura | REGLAS_NEGOCIO | MEDIA |
| BR-05-002 | CF-L154, CF-L160, CF-L145, CF-L146 | Reservas y topes de nacionalización sin bloqueo ni control de concurrencia | PERSISTENCIA | MEDIA |
| BR-05-003 | CF-L144, CF-L146 | Los levantes de un depósito anulado bloquean su número y aceptación y no se pueden retirar | REGLAS_NEGOCIO | MEDIA |
| BR-05-004 | CF-LX05-01, CF-L154 | No existe el bloqueo manual de salidas por cliente (`cliente.sinsalidas`) | REGLAS_NEGOCIO | MEDIA |
| BR-05-005 | CF-L158 | La cabecera de la orden (vehículo, conductor, ciudad, fecha, observaciones, orden externa) no se corrige | BACKEND / FRONTEND | MEDIA |
| BR-05-006 | CF-LX05-02, CF-L163.a | La guía se emite antes del cargue sin el control del legacy | REGLAS_NEGOCIO | MEDIA |
| BR-05-007 | CF-L143 | El filtro de fechas del listado de levantes se ignora | CONTRATOS_API | MEDIA |
| BR-05-008 | CF-L151, CF-L152, CF-L239 | Listados de salidas sin búsqueda por tiquete ni por fecha de salida; selector de la guía con tope de 50 | FRONTEND | BAJA |
| BR-05-009 | CF-L155 | Guía de exportación automática: sin reintento si falla y con un modo de pago sin efecto | BACKEND | BAJA |
| BR-05-010 | CF-L163.b | El conteo de impresiones de la guía no se muestra y la descarga del PDF no lo registra | REGLAS_NEGOCIO | BAJA |
| BR-05-011 | CF-L163.a, CF-V054 | Cobro de la guía por depósito del cliente dueño, pendiente de validar | VALIDACION_PENDIENTE | BAJA |
| BR-05-012 | CF-L144, CF-L145 | Diferencias menores del levante sin decisión en §A | REGLAS_NEGOCIO | BAJA |
| BR-05-013 | CF-L154, CF-L163, CF-V052 | Contratos TS y estados residuales | CONTRATOS_API | BAJA |

Por criticidad: CRÍTICA 0 · ALTA 0 · MEDIA 7 · BAJA 6.

## Búsquedas de ausencia

| Afirmación | Términos | Carpetas |
| --- | --- | --- |
| No hay bloqueo manual de salidas (BR-05-004) | `sinsalidas`, `BlockedExits`, `ExitsBlocked`, `BlockDispatch`, `DispatchBlocked`, `IsBlocked`, `UpdateFinancialStatus(` | `B/Wms.Domain`, `B/Wms.Application`, `F/pages/admin/stakeholders`, `F/features/stakeholders` |
| No se edita la cabecera de la orden (BR-05-005) | `UpdateExternalOrder(`, `UpdateDestination(`, `UpdateObservations(`, `AssignCrew(`, `SetDestination(`, `ChangeVehicle`, `ChangeDriver`, `HttpPatch("loading-orders`, `HttpPut("loading-orders` | `B/Wms.Application`, `B/Wms.Api/Controllers/v1` |
| No hay bloqueo de concurrencia (BR-05-002) | `IsConcurrencyToken`, `IsRowVersion`, `xmin`, `RowVersion`, `ConcurrencyCheck`, `FOR UPDATE`, `IsolationLevel`, `HasCheckConstraint` | `B/Wms.Infrastructure`, `B/Wms.Application`, `B/Wms.Domain`, `B/Wms.Api` (sin `Migrations/`) |
| `LoadingOrder.Complete()` no tiene llamadores (BR-05-013) | `.Complete();`, `order.Complete()` | `B/Wms.Application` |
| El conteo de impresiones de la guía no se muestra (BR-05-010) | `DispatchGuidePrintLogs`, `printCount`, `impresiones` | `B/Wms.Application`, `F/features/foreign-trade`, `F/pages/foreign-trade/dispatch-guides` |

---

### BR-05-001 — Cancelar o modificar una orden con guía vigente no anula ni ajusta la guía ni su factura

- **ID funcional:** CF-L159.a (anular antes del cargue), CF-L158 (modificar), CF-L163.a (guía). Relacionada con BR-05-006.
- **Descripción:** la guía de importación se puede emitir con la orden en `Pending` o `InProgress`. Después, «Cancelar orden» y «Modificar ítems» siguen disponibles y no miran la guía: la cancelación deja la guía **vigente**, con su factura (pagada si fue de contado) y sin aviso a Facturación; la modificación de cantidades deja la guía con las cantidades anteriores. En cambio, «Revertir salida» sí exige anular antes la guía.
- **Comportamiento esperado:** coherente con §B.4.4/§B.4.6: una orden con guía vigente no se cancela ni cambia cantidades sin anular primero la guía (409 «Anule primero la guía …»), o la cancelación anula la guía aplicando `InvoiceCancellationPolicy` y avisando a Facturación.
- **Comportamiento actual:** `LoadingOrder.Cancel` solo rechaza estados cargados, cancelados o revertidos (`B/Wms.Domain/Entities/Warehouse/LoadingOrder.cs:309-330`); `CancelLoadingOrderHandler.cs:38-49` libera reservas y guarda. `UpdateLoadingOrderItemsCommandHandler.cs:44-121` solo bloquea **retirar** un ítem que figura en una guía (`FT/Common/Services/LoadingOrderReservationService.cs:135-143`), no cambiar su cantidad. Pantalla: `F/pages/foreign-trade/loading-orders/[id]/index.vue:44-46` muestra «Cancelar Orden» y «Modificar ítems» sin mirar guías. La guía de una orden cancelada deja de contar en saldos (`DispatchGuideBalanceService.cs:39-44`), pero sigue en el historial como vigente.
- **Capa:** backend y frontend. **Categoría:** REGLAS_NEGOCIO.
- **Evidencia adicional:** QA F5-GUI-007 PASA («Guía para OC14 Pending: 201 (cantidad pedida)», `docs/qa/resultados/F5-informe-2026-10-02.md:150`); no hay caso de cancelar con guía. El legacy tampoco anulaba la guía al eliminar la salida (`L/modulos/mod_salidas/eliminarsalida.php:87-124`), pero en el legacy la guía casi siempre se creaba con el cargue completo (CF-LX05-02). Sin ficha DEF.
- **Impacto:** guía impresa y cobrada para mercancía que no sale; cobro de $15.000 (T4) sin servicio; un PDF de guía con cantidades distintas a las de la orden.
- **Criticidad:** MEDIA — escenario específico (guía antes del cargue), con efecto en documentos y facturación.
- **Dependencias:** módulo 06 (factura de la guía).
- **Acción recomendada:** en `Cancel` y en `UpdateLoadingOrderItems` (cambio de cantidad), 409 si hay guía vigente; ocultar los botones en ese caso o mostrar «Anule primero la guía».
- **Criterio de resolución:** con una guía vigente sobre una orden `Pending`, `PATCH …/cancel` y `PUT …/items` con otra cantidad responden 409 con el número de la guía; prueba de dominio en `Wms.Tests` (`LoadingOrderTransitionsTests`) y caso QA nuevo.

### BR-05-002 — Reservas y topes de nacionalización sin bloqueo ni control de concurrencia

- **ID funcional:** CF-L154, CF-L160 (tope GAP-002, RN-034), CF-L145, CF-L146 (guarda de «usado» al editar o retirar levantes).
- **Descripción:** crear y modificar órdenes, cancelar, ejecutar el cargue y editar o retirar levantes leen `CurrentStock`/`ReservedStock` sin bloqueo y escriben el valor absoluto. No hay token de concurrencia ni `CHECK` en `warehouse_storage_products`.
- **Comportamiento esperado:** el tope «no despachar más de lo nacionalizado considerando las reservas de órdenes abiertas» se cumple también con dos operaciones simultáneas sobre el mismo producto.
- **Comportamiento actual:** `CreateLoadingOrderCommandHandler.cs:79-198` valida stock y nacionalizado **antes** de abrir la transacción (`:309`); la reserva se aplica en memoria (`WarehouseStorageProduct.cs:239-249`) y EF la escribe como valor. El bloqueo del consecutivo `OC` (`DocumentNumberGenerator.cs:30-37`) serializa la creación, pero la segunda transacción usa la entidad leída antes y sobrescribe el reservado de la primera. `UpdateLoadingOrderItemsCommandHandler.cs`, `CancelLoadingOrderHandler.cs`, `ExecuteLoadingOrderCommandHandler.cs:134`, `WithdrawImportReleaseCommandHandler.cs` y `UpdateImportReleaseCommandHandler.cs` no bloquean. Solo la guía bloquea productos (`DispatchGuideBalanceService.cs:28-30`).
- **Capa:** backend. **Categoría:** PERSISTENCIA.
- **Evidencia adicional:** DEF-F10-001 (Verificado) protegió el doble clic en «Crear OC» y «Emitir guía» desde el frontend; DEF-F3-002 (Verificado) resolvió la idempotencia solo en báscula (`EntryLogLock`). `docs/qa/00-plan-maestro.md` §10 descarta la concurrencia entre operarios **de báscula**, no de Comercio Exterior ni de Bodega.
- **Impacto:** reservado subestimado: otra orden puede reservar el mismo stock o despachar sobre lo nacionalizado; un levante podría reducirse por debajo de lo ya reservado.
- **Criticidad:** MEDIA — requiere simultaneidad real, pero compromete el control aduanero si ocurre.
- **Dependencias:** módulo 03 (cargue).
- **Acción recomendada:** `SELECT … FOR UPDATE` de los `warehouse_storage_products` afectados (y de la orden) al inicio de la transacción, releyendo después del bloqueo, como `DispatchGuideBalanceService`; o token de concurrencia (`xmin`) con 409 al chocar.
- **Criterio de resolución:** prueba de integración (`Wms.IntegrationTests`) con dos `CreateLoadingOrder` paralelos por el total disponible del mismo producto: uno 201 y otro 400; `ReservedStock` final = una sola reserva.

### BR-05-003 — Los levantes de un depósito anulado bloquean su número y aceptación y no se pueden retirar

- **ID funcional:** CF-L144 (RN-026), CF-L146.
- **Descripción:** al anular un depósito sus levantes quedan «como historia» (F3-08, punto 7). La búsqueda de duplicados no filtra por estado del depósito y el retiro está prohibido en depósitos anulados, así que el número de levante y de aceptación quedan inutilizables.
- **Comportamiento esperado:** si un depósito se anula (p. ej. se creó mal y se rehízo), su levante DIAN se puede registrar en el depósito correcto.
- **Comportamiento actual:** `FT/Common/Services/ReleaseDuplicateLookup.cs:24-35` consulta todos los `ImportReleases`; `WithdrawImportReleaseCommandHandler.cs:43-44` responde 400 «No se pueden retirar levantes de un depósito anulado.». La anulación no toca los levantes (sin referencias a `ImportReleases` en `CancelWarehouseStorageHandler.cs` ni en `WarehouseStorageCancellationService.cs`).
- **Capa:** backend. **Categoría:** REGLAS_NEGOCIO.
- **Evidencia adicional:** QA F5-LEV-004 (duplicado en otro depósito, PASA) y DEF-F5-005 (levantes en anulados, Verificado) no cubren este caso.
- **Impacto:** el operario no puede nacionalizar la mercancía del depósito rehecho con su levante real; la salida queda bloqueada (F2-02).
- **Criticidad:** MEDIA — escenario específico que bloquea la salida.
- **Acción recomendada:** confirmar con el negocio y excluir de `ReleaseDuplicateLookup` los levantes de depósitos `Cancelled` (conservándolos como historia).
- **Criterio de resolución:** con `QA-LEV-X` en un depósito anulado, registrarlo en otro depósito responde 200; prueba en `ReleaseDuplicateRulesTests`.

### BR-05-004 — No existe el bloqueo manual de salidas por cliente (`cliente.sinsalidas`)

- **ID funcional:** CF-LX05-01, CF-L154.
- **Descripción:** en el legacy, Comercio Exterior o la administración marcaban un cliente con «sin salidas» y la salida quedaba «Bloqueado», independientemente de la mora. En V2 el único bloqueo es `FinancialStatus.Blocked`, que calcula el job de mora.
- **Comportamiento esperado:** poder bloquear las salidas de un cliente por decisión comercial, o decisión documentada de no hacerlo.
- **Comportamiento actual:** `BillingService.ValidateFinancialStatusAsync` (`B/Wms.Application/Billing/Common/Services/BillingService.cs:106-119`) solo mira `FinancialStatus`; su único escritor es el job (`B/Wms.Application/Billing/Jobs/BillingJobService.cs:83`) y el recálculo (`BillingService.cs:194`). Legacy: `L/modulos/mod_salidas/registrarsalida.php:546-549,1225-1227`; `L/modulos/mod_clientes/modificarcliente.php:80,94,480`.
- **Capa:** backend y frontend. **Categoría:** REGLAS_NEGOCIO.
- **Evidencia adicional:** sin ficha DEF; no aparece en `FUNCTIONAL_GAPS.md`, `DECISIONES_REVISION.md` ni en el plan de paridad. BR-01-004 (módulo 01) agrupa los datos de las fichas legacy sin destino; no nombra `sinsalidas`.
- **Impacto:** un cliente con salidas retenidas por razones no financieras (disputas, orden de la DIAN, garantía) puede retirar mercancía.
- **Criticidad:** MEDIA — control comercial sin sustituto.
- **Dependencias:** módulo 01 (ficha del tercero), módulo 06 (estado financiero).
- **Acción recomendada:** confirmar con el negocio si se usaba; si sí, marca en el tercero (Admin/Facturación) que bloquee crear orden y emitir guía, con el mismo mensaje del bloqueo por mora.
- **Criterio de resolución:** decisión registrada en `docs/contexto/decisiones.md`, o un tercero marcado responde 400 en `POST foreign-trade/loading-orders` y `POST foreign-trade/dispatch-guides`.

### BR-05-005 — La cabecera de la orden no se corrige

- **ID funcional:** CF-L158.
- **Descripción:** F3-03 permite cambiar los ítems antes del cargue, pero ningún endpoint corrige vehículo, conductor, ciudad de destino, dirección, fecha programada, observaciones, cuadrilla (salvo en el cargue) ni la orden externa. El legacy cambiaba fecha, cliente, transportadora, SIA, destino, cuadrilla y observaciones (`L/modulos/mod_salidas/modificarsalida.php:126-140`) y la hora de la orden (`modificarorden.php`).
- **Comportamiento esperado:** corregir la cabecera mientras la orden no esté cargada, o decisión documentada de «cancelar y crear otra».
- **Comportamiento actual:** los métodos `LoadingOrder.UpdateExternalOrder`, `UpdateObservations`, `UpdateDestination` existen (`LoadingOrder.cs:150-170,444-470`) pero no tienen llamadores; `AssignCrew` solo en crear y ejecutar (`CreateLoadingOrderCommandHandler.cs:332`; `ExecuteLoadingOrderCommandHandler.cs:125`). El detalle de la orden es de solo lectura (`F/pages/foreign-trade/loading-orders/[id]/index.vue:220-338`).
- **Capa:** backend y frontend. **Categoría:** BACKEND / FRONTEND.
- **Evidencia adicional:** sin ficha DEF. §B.4.6 decide solo sobre ítems y cancelación.
- **Impacto:** si llega otro camión o conductor, la báscula no encuentra la orden del vehículo (la orden es por placa) y hay que cancelar y recrear (nueva reserva, nuevo consecutivo, nueva orden externa); una ciudad mal elegida cambia el vencimiento de la guía.
- **Criticidad:** MEDIA — flujo frecuente con alternativa costosa.
- **Acción recomendada:** confirmar con el negocio; `PATCH foreign-trade/loading-orders/{id}` para `Pending`/`InProgress` (vehículo y conductor solo sin salida activa en báscula), con motivo y `Describe`.
- **Criterio de resolución:** decisión registrada, o una orden `Pending` cambia vehículo y ciudad y la báscula la encuentra con la placa nueva.

### BR-05-006 — La guía se emite antes del cargue sin el control del legacy

- **ID funcional:** CF-LX05-02, CF-L163.a.
- **Descripción:** en el legacy «Crear Guía» solo aparecía con el cargue completo, salvo para usuarios con el permiso `crearguiasinautorizacion` (`L/modulos/mod_salidas/listarsalidas.php:688-705`). En V2 cualquier usuario con `ForeignTradeAccess` emite la guía de una orden `Pending` o `InProgress`.
- **Comportamiento esperado:** decisión documentada sobre cuándo se puede emitir la guía; si se mantiene antes del cargue, que el cargue parcial o la modificación avisen que la guía quedó desactualizada.
- **Comportamiento actual:** `LoadingOrder.EnsureGuidable` (`LoadingOrder.cs:390-398`); `GetPendingImportLoadingOrdersHandler.cs:34-38`. La guía congela lo pedido si no hay cargue (`DispatchGuideBalanceService.cs:15-21`); el plan lo acepta como riesgo de F3-01 («se corrige anulándola»), pero no hay decisión en §A ni §B.4.
- **Capa:** backend. **Categoría:** REGLAS_NEGOCIO.
- **Evidencia adicional:** QA F5-GUI-007 «Se permite (anotar)»; la báscula exige la guía antes de cerrar el pesaje de salida (`ImportGuideRules.EnsureScaleCanClose`), lo que empuja a emitirla temprano.
- **Impacto:** guías con cantidades distintas a lo cargado; base de BR-05-001.
- **Criticidad:** MEDIA — documento aduanero con cantidades que pueden no coincidir.
- **Acción recomendada:** confirmar con el negocio: (a) solo con la orden `Loaded`, (b) antes del cargue con aviso a Comercio Exterior si el cargue difiere, o (c) mantener y documentar.
- **Criterio de resolución:** decisión en `docs/contexto/decisiones.md` y código que la cumpla (prueba de dominio de `EnsureGuidable` o del aviso).

### BR-05-007 — El filtro de fechas del listado de levantes se ignora

- **ID funcional:** CF-L143.
- **Descripción:** la página envía las fechas como instante ISO y el API las espera como `DateOnly`.
- **Comportamiento esperado:** filtrar por la fecha del levante (días de Colombia, inclusivos) en pantalla y en el Excel.
- **Comportamiento actual:** `F/pages/foreign-trade/releases/index.vue:49-50` → `fromDate=2026-10-01T05:00:00.000Z`; `FT/Queries/GetReleases/GetReleasesQuery.cs:19-20` (`DateOnly?`). `DateOnly` rechaza textos con hora y el filtro automático de `ModelState` está suprimido (`B/Wms.Api/Program.cs:69`); el binder de Colombia solo cubre `DateTimeOffset` (`B/Wms.Api/Common/ModelBinding/ColombiaDateTimeOffsetModelBinder.cs:55-63`). Resultado esperado del análisis: `FromDate`/`ToDate` nulos y la lista completa. **No ejecutado.**
- **Capa:** integración. **Categoría:** CONTRATOS_API.
- **Evidencia adicional:** QA F5-REL-001 PASA solo con el filtro por levante (`F5-informe-2026-10-02.md:167`). Sin ficha DEF.
- **Impacto:** consultas y Excel por fecha devuelven todos los levantes sin que el operario lo note.
- **Criticidad:** MEDIA — función de consulta secundaria con resultado engañoso.
- **Acción recomendada:** enviar `yyyy-MM-dd` en hora de Colombia (como otros filtros de fecha) o aceptar `DateTimeOffset` en el query.
- **Criterio de resolución:** `GET foreign-trade/releases?fromDate=…&toDate=…` desde la pantalla devuelve solo levantes de ese rango; caso QA F5-REL-001 con fechas.

### BR-05-008 — Listados de salidas sin búsqueda por tiquete ni por fecha de salida; selector de la guía con tope de 50

- **ID funcional:** CF-L151, CF-L152, CF-L239.
- **Descripción:** el legacy buscaba salidas por depósito, guía, fecha de salida, tiquete, transportadora, importador y placa (`listarsalidas.php:327-333`, `listarsalidasexp.php:317-323`). V2 cubre depósito, importador, transportadora y placa en órdenes, y guía en el historial, pero no tiquete ni fecha de salida en pantalla (el API de órdenes acepta `fromDate`/`toDate` sobre `CreatedAt`). El selector de órdenes de la guía pide 50 filas (`DispatchGuideForm.vue:29-34`), contra la convención `all=true`.
- **Comportamiento actual:** `F/pages/foreign-trade/loading-orders/index.vue:29-53`; `FT/Queries/GetLoadingOrders/LoadingOrderSearchField.cs`; `FT/Queries/GetDispatchGuides/GetDispatchGuidesHandler.cs:22-40`.
- **Capa:** frontend. **Categoría:** FRONTEND.
- **Evidencia adicional:** DEF-F5-009 (filtros de órdenes, Verificado) no cubre estos criterios.
- **Impacto:** búsquedas más lentas; con más de 50 órdenes pendientes, «Generar Guía» desde «Pendientes» puede abrir el formulario sin la orden.
- **Criticidad:** BAJA.
- **Acción recomendada:** filtro de fechas en órdenes y guías; búsqueda por tiquete; selector con `all=true` o búsqueda por id.
- **Criterio de resolución:** filtros visibles y funcionando; con 60 órdenes pendientes, la 60 se preselecciona.

### BR-05-009 — Guía de exportación automática: sin reintento si falla y con un modo de pago sin efecto

- **ID funcional:** CF-L155.
- **Descripción:** la guía EXP se crea al final del cargue, fuera de su transacción; si falla, solo queda en el log y no hay ruta para emitirla. Nace con `PaymentMode = Immediate` sin factura, y el historial ofrece «Cambiar modo de pago», que no tiene efecto (QA F5-GUI-014 «EXP: cambio aplicado»). La guía automática no tiene decisión documentada en §A (el legacy la creaba a mano con «Crear Guía», `listarsalidasexp.php:718`).
- **Comportamiento actual:** `ExecuteLoadingOrderCommandHandler.cs:352-366`; `CreateExportDispatchGuideCommand.cs:11-15`; `CreateDispatchGuideCommandHandler.cs:125-130` (rechaza exportación).
- **Capa:** backend. **Categoría:** BACKEND.
- **Impacto:** una orden EXP cargada podría quedar sin guía; acción de pantalla sin sentido.
- **Criticidad:** BAJA — fallo poco probable; no hay cobro.
- **Acción recomendada:** confirmar con el negocio la guía automática; permitir regenerarla (o reintentar desde «Pendientes»); no ofrecer el cambio de modo en guías sin factura.
- **Criterio de resolución:** una orden EXP `Loaded` sin guía aparece con acción para emitirla; `canChangePaymentMode` = false sin facturas.

### BR-05-010 — El conteo de impresiones de la guía no se muestra y la descarga del PDF no lo registra

- **ID funcional:** CF-L163.b.
- **Descripción:** el legacy sumaba cada impresión y avisaba «La guía se ha impreso en N ocasión(es)» (`contarimpresiones.php:40-50`; `verguia.php:224-243`). V2 registra `DispatchGuidePrintLog` solo al bajar el ZIP por depósito y no lo muestra en ninguna pantalla; `GET dispatch-guides/{id}/pdf` no registra.
- **Comportamiento actual:** `GetDispatchGuidePerDepositZipHandler.cs:68-71`; sin consumidores de `DispatchGuidePrintLogs` fuera de ese handler (grep).
- **Capa:** backend y frontend. **Categoría:** REGLAS_NEGOCIO.
- **Evidencia adicional:** GAP-024 (a) se cerró solo para etiquetas (F4-09/F7-01).
- **Impacto:** se pierde el control de reimpresiones de un documento aduanero.
- **Criticidad:** BAJA.
- **Acción recomendada:** confirmar con el negocio; registrar también la descarga del PDF y mostrar el conteo en el historial, como `LabelPrintsBadge`.
- **Criterio de resolución:** dos descargas del PDF muestran «Impresa 2 veces» en el historial.

### BR-05-011 — Cobro de la guía por depósito del cliente dueño, pendiente de validar

- **ID funcional:** CF-L163.a, CF-V054.
- **Descripción:** V2 cobra la guía (el legacy no la cobraba, DEC-041 T4) como tarifa × número de depósitos de cada cliente dueño + IVA (`DispatchGuideBillingPlan.cs`); P16 dice «se cobra una guía por camión». `docs/qa/00-plan-maestro.md` §10 dejó «Guía de orden multi-cliente … validar contra el legacy». El valor T4 ($15.000) es configuración (`ServicePrice`/convenio, `ForeignTradeService.cs:22-57`), no verificable en código.
- **Capa:** backend. **Categoría:** VALIDACION_PENDIENTE.
- **Impacto:** una guía de un camión con dos depósitos del mismo cliente cobra dos veces la tarifa (QA F5-GUI-012: 60.000 = 30.000 × 2).
- **Criticidad:** BAJA — importe pequeño, pero repetido en cada salida multi-depósito.
- **Dependencias:** módulo 06.
- **Acción recomendada:** confirmar con el negocio «por guía» o «por depósito» y registrar la decisión; verificar la tarifa T4 en staging.
- **Criterio de resolución:** decisión en `docs/contexto/decisiones.md` y prueba de `DispatchGuideBillingPlan` acorde.

### BR-05-012 — Diferencias menores del levante sin decisión en §A

- **ID funcional:** CF-L144, CF-L145.
- **Descripción:** (a) el importador del levante es siempre el del depósito (el legacy lo guardaba por levante, `levante.id_importador`); (b) el número y la fecha del manifiesto DIAN se llevan en el depósito (módulo 04), no en el levante (`modificarlevante.php:88`); (c) el peso se registra por fila de producto, no por levante (`levante.peso_bruto`); (d) no hay registro de varios productos en un solo envío (DF4 lo cubre con «Registrar otro producto»). Solo (d) tiene decisión; (a)–(c) están en el texto de F2-05 o son efecto del modelo, no en §A/§B.4.
- **Capa:** backend. **Categoría:** REGLAS_NEGOCIO.
- **Impacto:** bajo; informes de pólizas por levante podrían sumar pesos por fila.
- **Criticidad:** BAJA.
- **Acción recomendada:** confirmar con el negocio y registrar la decisión.
- **Criterio de resolución:** decisión registrada (o ajuste del modelo).

### BR-05-013 — Contratos TS y estados residuales

- **ID funcional:** CF-L154, CF-L163, CF-V052.
- **Descripción:** (a) `ICreateLoadingOrderItemRequest` no declara `warehouseStorageCargoUnitId` (`F/features/foreign-trade/types/loading-order.ts:74-77`), que el formulario envía (`LoadingOrderForm.vue:471-476`); (b) `IDispatchGuideDto` declara `signerType` y `signerName` (`types/dispatch-guide.ts:73-74`), que `DispatchGuideDto` no tiene; (c) el estado `Complete` de la orden no tiene transición que lo asigne (`LoadingOrder.Complete()`, `LoadingOrder.cs:294-302`, sin llamadores) y aparece en filtros y guardas; (d) «Guías pendientes» suma la cantidad **pedida**, no la cargada (`GetPendingGuidesQuery.cs:54`); (e) `dispatch_guides.loading_order_id` no tiene índice único filtrado por `cancelled_at IS NULL` (`DispatchGuideConfiguration.cs:38`).
- **Capa:** contratos. **Categoría:** CONTRATOS_API.
- **Impacto:** bajo; tipos que no reflejan el contrato y una garantía de unicidad solo en código.
- **Criticidad:** BAJA.
- **Acción recomendada:** alinear los tipos; retirar `Complete` o asignarlo; usar `LoadedQuantity ?? Quantity` en pendientes; índice único parcial (migración con `dotnet ef`).
- **Criterio de resolución:** `vue-tsc` sin campos inexistentes; búsqueda de `Complete` con uso o retirado; índice presente en el snapshot.


---

## Decisiones posteriores (2026-10-23)

> Nota del orquestador. Después de esta auditoría, el usuario respondió las preguntas al negocio (`docs/contexto/decisiones.md`, DEC-050…054; `06-brechas-priorizadas.md` §3.1). El registro de arriba es la foto previa y no se reescribe. El estado vigente está en `06-brechas-priorizadas.md` y `04-matriz-global.csv`.

| Brecha | Estado | Decisión |
| --- | --- | --- |
| BR-05-004 | Abierta: se construye (requiere plan cerrado) | DEC-052 |
| BR-05-006 | Abierta: se construye (requiere plan cerrado) | DEC-052 |
