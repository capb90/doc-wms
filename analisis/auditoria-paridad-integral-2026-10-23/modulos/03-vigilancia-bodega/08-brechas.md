# 03 · Vigilancia y Bodega — Registro de brechas

> 11 brechas: 0 CRÍTICA, 0 ALTA, 2 MEDIA, 9 BAJA. Antes de registrar cada una se buscó en `docs/qa/resultados/defectos/` (153 fichas e `INDICE.md`), en `docs/planes/migracion-staging/resultados/defectos/` y en `docs/contexto/estado.md` §4 (términos: `PATCH entry-logs`, `UpdateEntryLog`, `warehouse/loading-orders`, `departure-authorizations`, `autorización de salida`, `redonde`, `auditor` + `montacarg`): ninguna está ya registrada. Las fichas relacionadas que existen se citan en cada brecha. `BE` = `Backend/wms-api/`, `FE` = `Frontend/wms/app/`.

## Búsquedas de ausencia (para las afirmaciones «no existe»)

| Afirmación | Términos | Carpetas |
| --- | --- | --- |
| No hay consumidor de `PATCH entry-logs/{id}` | `updateEntryLog`, `useUpdateEntryLog`, `entry-logs/${` | `FE/` (`*.ts`, `*.vue`) |
| No hay consumidor de `POST warehouse/loading-orders` | `useLoadingOrderCreate`, `createLoadingOrder`, `"/warehouse/loading-orders"` | `FE/` |
| Los diálogos de autorización y manifiesto no se abren | `openDepartureAuthDialog`, `openManifestDialog`, `showDepartureAuthDialog = true`, `showManifestDialog = true` | `FE/pages/operations/entries/history.vue` y `FE/` |
| La importación no trae posiciones | `ubic`, `location`, `placement`, `seccion` | `BE/Wms.Application/Administration/LegacyImport/Importers/DepositsImporter.cs`, `Common/LegacyDepositRowParser.cs` |
| `ForkliftUse` no es auditable | `IAuditable` | `BE/Wms.Domain/Entities/Warehouse/ForkliftUse.cs` |

---

### BR-03-001 — `PATCH entry-logs/{id}` cambia el motivo del ingreso sin la guarda de la corrección

- **ID funcional:** CF-V031 (corrección de ingresos), CF-V030.a.
- **Descripción:** el endpoint de actualización de ingresos, sin consumidor en el frontend, permite cambiar conductor, motivo y observaciones, y vincular el ingreso a cualquier servicio, sin las reglas de la corrección WMS-5.
- **Esperado:** el motivo de un ingreso con operación de báscula o de bodega no cambia (WMS-5 D07, `EntryLog.CorrectEntryReason`, `BE/Wms.Domain/Entities/Logistics/EntryLog.cs:126-138`) y toda corrección lleva motivo y queda marcada «Corregido» (`CorrectEntryLogCommandHandler.cs:97-101`).
- **Actual:** `PATCH entry-logs/{id}` (`BE/Wms.Api/Controllers/v1/EntryLogController.cs:63-72`, `GateAccess`: Admin y Receiving) llama a `UpdateEntryLogHandler`, que usa `AssignEntryReason` sin comprobar operación (`BE/Wms.Application/Logistics/EntryLogs/Commands/UpdateEntryLog/UpdateEntryLogHandler.cs:80-83`), agrega un enlace `ServiceRecordEntryLog` a un servicio cuya existencia no valida (`:66-73,85-96`) y reevalúa el estado (`:103`). Sin motivo ni marca de corrección. En el frontend, `updateEntryLog` (`FE/features/entries/services/entry-service.ts:34-40`) no tiene llamadas.
- **Capa / categoría:** Backend · `SEGURIDAD` (regla saltable por API).
- **Evidencia:** citada arriba. Riesgo conocido de la corrección: R-VIG-02 / DEF-F11-016 (verificado), que corrigió el camino de la corrección, no este endpoint.
- **Impacto:** un usuario de Vigilancia con un cliente HTTP puede sacar un camión de la cola de báscula o reasignarlo a otro servicio sin dejar motivo.
- **Criticidad:** MEDIA — escenario por API, no por la interfaz; compromete la consistencia ingreso–servicio en casos concretos.
- **Dependencias:** cola de báscula (módulo 02).
- **Acción recomendada:** retirar el endpoint (no lo usa ninguna pantalla; DEC-005 no se afecta) o aplicarle las mismas guardas que la corrección.
- **Criterio de resolución:** `PATCH entry-logs/{id}` con un ingreso que tiene ciclo de báscula y un `entryReasonId` distinto responde 404/405 o 409 con el mensaje de D07; prueba en `Wms.Tests` o `Wms.IntegrationTests`.

### BR-03-002 — Bodega puede crear órdenes de cargue por API

- **ID funcional:** CF-V038 (superficie de órdenes de cargue de Bodega); flujo de órdenes del módulo 05.
- **Descripción:** existe `POST warehouse/loading-orders` con `WarehouseAccess` (Admin y Warehouse), además del endpoint de Comercio Exterior.
- **Esperado:** crear la orden de cargue es de Comercio Exterior (`POST foreign-trade/loading-orders`, `BE/Wms.Api/Controllers/v1/ForeignTradeController.cs:64,1005`, `ForeignTradeAccess`); en el legacy la autorización del cargue era de Salidas (LEGACY-FUNC-164).
- **Actual:** `BE/Wms.Api/Controllers/v1/WarehouseController.cs:791-826` envía el mismo `CreateLoadingOrderCommand` con la política de Bodega. El frontend tiene `useLoadingOrderCreate` (`FE/features/warehouse/composables/useLoadingOrderMutations.ts:25-33`) sin uso; la pantalla de creación usa el composable de Comercio Exterior (`FE/pages/foreign-trade/loading-orders/create.vue`).
- **Capa / categoría:** Backend · `SEGURIDAD`.
- **Evidencia:** citada.
- **Impacto:** separación de funciones: el operario de Bodega podría crear y reservar una orden sin pasar por CE (las validaciones de stock, mora y nacionalizado son las mismas del comando).
- **Criticidad:** MEDIA — solo por API; no hay pantalla.
- **Dependencias:** módulo 05 (órdenes de cargue).
- **Acción recomendada:** retirar el endpoint o pasarlo a `ForeignTradeAccess` (ningún rol pierde una función usada: DEC-005).
- **Criterio de resolución:** `POST warehouse/loading-orders` con el rol Warehouse responde 403 o 404; una prueba de superficie de controlador lo asegura.

### BR-03-003 — Autorizaciones de salida y manifiestos de Vigilancia sin interfaz alcanzable

- **ID funcional:** CF-V036.
- **Descripción:** el historial de Vigilancia tiene los diálogos «Autorización de Salida» y «Crear Manifiesto», pero nada los abre; los endpoints quedan sin consumidor.
- **Esperado:** o se exponen con una acción visible, o se retiran (código y endpoints) para no dejar flujos a medias.
- **Actual:** `FE/pages/operations/entries/history.vue:150-223` define los diálogos; `openDepartureAuthDialog` (`:156`) y `openManifestDialog` (`:193`) no se llaman y `AppTable` solo emite `view` y `edit` (`:264-278`). `useUpdateDepartureAuthorization` no tiene uso. Endpoints: `POST entry-logs/{id}/departure-authorizations`, `POST entry-logs/{id}/manifests` (`EntryLogController.cs:88-116`), `PATCH departure-authorizations/{id}` (`DepartureAuthorizationController.cs:12-30`). Además, `ICreateManifestRequest` declara `manifestPackaging`, `manifestAmount` y `unitMeasure` (`FE/features/entries/types/entry-log.ts:119-125`) que `CreateManifestRequest(ManifestNumber, ManifestWeight)` no recibe (`EntryLogController.cs:131-133`).
- **Capa / categoría:** Frontend + contrato · `INTEGRACION`.
- **Impacto:** ninguno en la operación actual; confusión al mantener y riesgo de reactivar un formulario cuyo contrato no coincide.
- **Criticidad:** BAJA.
- **Acción recomendada:** decidir con el negocio; si no se usan, retirar diálogos, composables y endpoints.
- **Criterio de resolución:** no quedan funciones ni endpoints sin consumidor para estas operaciones, o hay un botón visible y el TS coincide con el request.

### BR-03-004 — Sin vista global de la mercancía pendiente por ubicar

- **ID funcional:** CF-L168.
- **Descripción:** el legacy listaba en una sola pantalla todos los lotes con saldo y su cantidad «A Ubicar»; V2 lo muestra producto por producto dentro de cada depósito.
- **Esperado (legacy):** `bodegas-legacy/modulos/mod_bodegas/asignarbodegaproducto.php:35,129-166`.
- **Actual:** «Por ubicar» solo en el diálogo `ProductPlacementsDialog.vue`, abierto desde «Consultar Stock» de un depósito (`FE/pages/warehouse/inventory/index.vue`); no hay consulta del backend que liste pendientes de varios depósitos (`GET warehouse/storage-products/{id}/placements` es por producto).
- **Capa / categoría:** Frontend + backend · `REGLAS_NEGOCIO` (diferencia sin decisión).
- **Impacto:** tras el corte (BR-03-006) o una liberación, el operario no ve qué falta ubicar sin recorrer depósito por depósito. En la operación diaria la recepción ya ubica lo descargado.
- **Criticidad:** BAJA.
- **Dependencias:** BR-03-006.
- **Acción recomendada:** confirmar con el negocio; si se necesita, un filtro «pendiente por ubicar» en el inventario.
- **Criterio de resolución:** decisión registrada o una lista de productos con `pendingToPlace > 0` de todos los depósitos.

### BR-03-005 — El «Reporte de mercancías» no imprime CPI, número de salida ni tipo de novedad

- **ID funcional:** CF-L177.
- **Descripción:** el PDF V2 difiere del legacy en tres datos.
- **Esperado (legacy):** «No. CPI-Factura» = tipo y número del documento comercial (`bodegas-legacy/modulos/mod_bodegas/imprimirobservacion.php:109-110`); «Salida» = número de la salida del lote (`:134-141`); «Orden de» muestra el tipo de observación (`:105-106`).
- **Actual:** «Factura / CPI» y «Depósito» imprimen los dos el número de depósito; no hay número de salida ni tipo de novedad (`BE/Wms.Application/Warehouse/Novelties/Services/WarehouseNoveltyPdfService.cs:83-92`). El plan F4-04 definió «factura o CPI, que es el número del depósito», pero el plan no es fuente de decisión (§5 de las instrucciones).
- **Capa / categoría:** Backend · `REGLAS_NEGOCIO`.
- **Impacto:** el documento de soporte de reclamaciones pierde la referencia al documento de transporte y a la salida.
- **Criticidad:** BAJA.
- **Acción recomendada:** confirmar con el negocio qué va en «Factura / CPI» y si se imprimen el tipo y la salida.
- **Criterio de resolución:** decisión registrada o PDF con esos campos; `WarehouseNoveltyPdfServiceTests` lo cubre.

### BR-03-006 — Las posiciones de bodega del legacy no se migran

- **ID funcional:** CF-L168, CF-L169.
- **Descripción:** la migración crea las ubicaciones, pero no lo que hay en cada una.
- **Esperado:** los saldos vivos llegan con su posición, o hay una decisión que acepte reubicarlos.
- **Actual:** `LocationsImporter` crea ubicaciones desde `bodega`/`seccion` (`BE/Wms.Application/Administration/LegacyImport/Importers/LocationsImporter.cs:118-123`); `DepositsImporter` no carga `productodetalle_x_seccion` ni placements (búsqueda arriba). El plan F4-01 lo deja como «riesgo» con datos iniciales opcionales, no como decisión (`docs/planes/paridad-legacy/plan-backend-paridad-legacy.md`, F4-01 «Esquema» y «Riesgo»).
- **Capa / categoría:** Backend · `PERSISTENCIA`.
- **Impacto:** tras el corte real (`estado.md` §4.7) todo el stock migrado queda «por ubicar». El legacy tenía 6 secciones en 9 bodegas (`docs/planes/migracion-staging/plan-migracion-legacy-staging.md:65`): uso bajo.
- **Criticidad:** BAJA.
- **Dependencias:** BR-03-004; corte real.
- **Acción recomendada:** confirmar con el negocio si se reubica a mano o se agrega la exportación de posiciones activas al CSV de depósitos.
- **Criterio de resolución:** decisión en `docs/contexto/decisiones.md` o importación probada en local.

### BR-03-007 — Estadísticas de inventario y de ubicaciones en stubs; sin vista de ocupación por bodega

- **ID funcional:** CF-V035, CF-L171.a.
- **Descripción:** el servicio del frontend tiene funciones que devuelven datos vacíos fijos y la pantalla las consulta.
- **Actual:** `FE/features/warehouse/services/warehouse-service.ts:570-596` (`getInventoryStatistics` → `null`, `getStockAlerts` → `[]`, `getStockHistorySummary` → `[]`) y `:690-712` (`getLocationOccupancySummary`, `getLocationStatistics`, `getLocationHierarchy`), con el comentario «stubs - backend not implemented yet». `FE/pages/warehouse/inventory/index.vue:167-169` los consulta; la tarjeta queda oculta (`:262`). No hay resumen de ocupación ni vista por bodega (el legacy pintaba la cuadrícula, `registrarbodegacantidad.php:182-256`).
- **Capa / categoría:** Frontend · `FRONTEND`.
- **Impacto:** ninguno visible; código que aparenta funciones inexistentes.
- **Criticidad:** BAJA.
- **Acción recomendada:** retirar los stubs y sus composables, o implementarlos si el negocio quiere el resumen.
- **Criterio de resolución:** no quedan funciones con datos fijos en el servicio de Bodega.

### BR-03-008 — Eliminar una ubicación con mercancía da un error genérico

- **ID funcional:** catálogo de ubicaciones (CF-L092 «Eliminar bodegas», módulo 01); se reporta aquí porque nace de las ubicaciones por cantidad (F4-01).
- **Descripción:** la baja de una ubicación no revisa si tiene mercancía ubicada.
- **Actual:** `DeleteWarehouseLocationHandler.cs:20-24` solo revisa la colección `WarehouseStorages`; las ubicaciones por cantidad tienen FK `Restrict` (`BE/Wms.Infrastructure/Persistence/Configurations/Warehouse/WarehouseStorageProductPlacementConfiguration.cs:36-39`), así que el `SaveChanges` falla y el manejador global responde 409 con el texto genérico de base de datos (`BE/Wms.Api/Common/Exception/GlobalExceptionHandler.cs:120-128`). La ubicación principal del producto pasa a nulo (`WarehouseStorageProductConfiguration.cs:67-70`, `SetNull`) si no hay placements.
- **Capa / categoría:** Backend · `BACKEND`.
- **Impacto:** el Admin no entiende por qué no puede borrar; no hay pérdida de datos.
- **Criticidad:** BAJA.
- **Acción recomendada:** validar placements antes de borrar con `ConflictException` «La ubicación tiene mercancía ubicada; libérela o desactívela.».
- **Criterio de resolución:** `DELETE warehouse/locations/{id}` con mercancía ubicada responde 409 con mensaje de negocio.
- **Confianza:** MEDIA (no se verificó el mapeo de `WarehouseLocation.WarehouseStorages`).

### BR-03-009 — IVA del montacargas: redondeo distinto en la interfaz y en el API

- **ID funcional:** CF-V033.b.
- **Descripción:** la vista previa del cobro redondea el IVA a pesos enteros; el backend, a 2 decimales.
- **Actual:** `FE/features/billing/components/BillingCollectForm.vue:231` (`Math.round(total × tasa / 100)`) vs `BE/Wms.Application/Warehouse/Common/Services/ForkliftVatCalculator.cs:14-17` (`Math.Round(…, 2)`). Observado en QA como OBS-F4-007 (`docs/qa/resultados/F4-informe-2026-10-02.md:90,169`), sin ficha DEF.
- **Capa / categoría:** Integración · `REGLAS_NEGOCIO`.
- **Impacto:** con valores con centavos, el total mostrado al operario difiere del facturado (p. ej. 100.001 + IVA).
- **Criticidad:** BAJA.
- **Dependencias:** módulo 06 (política de redondeo de facturas).
- **Acción recomendada:** usar la misma regla de redondeo en ambos lados (la del módulo de facturación).
- **Criterio de resolución:** con base 100.001 la UI y la factura muestran el mismo IVA.

### BR-03-010 — Anular una novedad exige motivo; el legacy no

- **ID funcional:** CF-L174.b.
- **Descripción:** diferencia de regla sin decisión escrita.
- **Esperado (legacy):** `eliminarobservacion.php:44-52` marca `eliminado` sin motivo.
- **Actual:** `POST warehouse/novelties/{id}/void` exige motivo de 10 a 500 caracteres (`BE/Wms.Api/Controllers/v1/WarehouseNoveltiesController.cs:117-130`; mensaje en `docs/planes/paridad-legacy/plan-backend-paridad-legacy.md` F4-03 regla 4).
- **Capa / categoría:** Backend · `REGLAS_NEGOCIO`.
- **Impacto:** positivo para la trazabilidad; un paso más para el operario.
- **Criticidad:** BAJA.
- **Acción recomendada:** confirmar con el negocio y registrar la decisión (DEC-nnn).
- **Criterio de resolución:** decisión registrada.

### BR-03-011 — El uso de montacargas no queda en la auditoría genérica

- **ID funcional:** CF-V033.a.
- **Descripción:** `ForkliftUse` no implementa `IAuditable`.
- **Esperado:** convención del proyecto: la auditoría es genérica (`IAuditable` → `audit_logs`, `Backend/wms-api/AGENTS.md`, «Convenciones»).
- **Actual:** `BE/Wms.Domain/Entities/Warehouse/ForkliftUse.cs:11` (`public class ForkliftUse`); el inicio, el fin, los horómetros, el modo de pago y el IVA no dejan registro de cambios. La factura sí es auditable (`Invoice : IAuditable`).
- **Capa / categoría:** Backend · `PERSISTENCIA`.
- **Impacto:** sin historial de quién cambió el horómetro o el modo de pago.
- **Criticidad:** BAJA.
- **Acción recomendada:** marcar la entidad `IAuditable` (cambio de modelo con su migración, `dotnet ef`).
- **Criterio de resolución:** iniciar y finalizar un uso deja filas en `audit_logs`.
