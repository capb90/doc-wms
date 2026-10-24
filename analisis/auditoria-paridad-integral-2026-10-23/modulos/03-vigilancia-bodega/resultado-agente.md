# 03 · Vigilancia y Bodega — Resultado del agente AG-03

> Auditoría estática del 2026-10-23. Sin Git, sin builds, sin pruebas, sin APIs ni bases de datos. Código en disco, que según `docs/contexto/estado.md` corresponde a BE `35a61b2` / FE `c924a8b`; el commit `83de58a` (montacargas con camión, recepción con todos los camiones) está en disco pero no en staging.

## 1. Cobertura

- **Legacy asignado:** 16 capacidades (CF-L168…180, CF-L230, CF-L236, CF-L254), auditadas las 16. Desglosadas en 22 filas (CF-L169.a/b, CF-L171.a/b, CF-L172.a/b/c, CF-L173.a/b, CF-L174.a/b).
- **Legacy no catalogado:** 3 (CF-LX03-01 liberar posiciones con la guía; CF-LX03-02 eliminar registro de portería, enlace roto; CF-LX03-03 plantilla de autorización sin uso).
- **Búsqueda de Vigilancia fuera de esas rutas:** el legacy **no tenía registro de ingreso de vehículos** por Vigilancia; `entrada.php` es solo el *frameset* posterior al login y el ingreso lo registraba Báscula. Tampoco había montacargas ni trazabilidad (términos y carpetas en `01-inventario-legacy.md` §1).
- **V2:** 6 candidatas SOLO_V2 (CF-V030…035) confirmadas y 4 nuevas (CF-V036…039), en 13 filas.
- **Archivos legacy leídos:** los 58 de `modulos/mod_bodegas/` en sus partes funcionales (SQL, permisos, formularios), `mod_observaciones/`, `salidapuerta/index.php`, `menus/menuizquierda.php`, `aut_verifica.inc.php`, `entrada.php`, `verificapermisos.php`, `mod_salidas/verguia.php` (tramos de liberación) y `bodegas_schema.sql` (tablas del módulo). Las variantes Colmotores se identificaron por menú e invocadores sin leerse a fondo.

## 2. Conteos (filas de la matriz)

**Paridad integral (25 filas legacy):** COMPLETO_CODIGO 10 · PARCIAL 4 · DIFERENCIA_INTENCIONAL 3 · NO_VERIFICADO 1 · NO_APLICA 7 · NO_IMPLEMENTADO 0. Las 13 filas V2 son `NO_APLICA` (origen SOLO_V2).

**Por capacidad (16 asignadas + 3 nuevas):** COMPLETO_CODIGO 5 (CF-L169, 173, 179, 180, 254) · PARCIAL 4 (CF-L168, 171, 174, 177) · DIFERENCIA_INTENCIONAL 3 (CF-L178, 230, LX03-01) · NO_VERIFICADO 1 (CF-L172, por su reporte general, que audita el módulo 07) · NO_APLICA 6 (CF-L170, 175, 176, 236 por Colmotores; LX03-02 y LX03-03 por no existir funcionalidad).

| Dimensión | Legacy (25) | V2 (13) |
| --- | --- | --- |
| Frontend | COMPLETO 15 · PARCIAL 2 · NO_VERIFICADO 1 · NO_APLICA 7 | COMPLETO 11 · PARCIAL 1 · SOLO_MAQUETADO 1 |
| Backend | COMPLETO 16 · PARCIAL 1 · NO_VERIFICADO 1 · NO_APLICA 7 | COMPLETO 11 · PARCIAL 2 |
| Integración | CONECTADO 17 · NO_VERIFICADO 1 · NO_APLICA 7 | CONECTADO 12 · SIN_INTEGRACION 1 |
| Reglas | COMPLETO 15 · PARCIAL 2 · NO_VERIFICADO 1 · NO_APLICA 7 | COMPLETO 10 · PARCIAL 3 |

**Validación por ejecución:** 25 de 38 filas citan una ejecución previa de QA (`docs/qa/resultados/F2-informe-2026-10-02.md`, `F4-informe-2026-10-02.md` o re-tests F11 en `defectos/INDICE.md`); las demás, «No ejecutada en esta auditoría». Los cambios de `83de58a` no tienen ejecución registrada.

## 3. Brechas (11)

| Criticidad | Cantidad | IDs |
| --- | ---: | --- |
| CRÍTICA | 0 | — |
| ALTA | 0 | — |
| MEDIA | 2 | BR-03-001, BR-03-002 |
| BAJA | 9 | BR-03-003 … BR-03-011 |

Las más relevantes:
1. **BR-03-001 (MEDIA):** `PATCH entry-logs/{id}`, sin consumidor, cambia el motivo del ingreso y lo vincula a cualquier servicio sin la guarda D07 ni motivo.
2. **BR-03-002 (MEDIA):** `POST warehouse/loading-orders` deja a Bodega crear órdenes de cargue por API (función de CE), sin consumidor.
3. **BR-03-005 (BAJA):** el «Reporte de mercancías» imprime el depósito como CPI y omite número de salida y tipo de novedad.
4. **BR-03-006 (BAJA):** las posiciones del legacy no se migran; tras el corte todo queda «por ubicar».
5. **BR-03-009 (BAJA):** IVA del montacargas redondeado distinto en la UI y en el API (OBS-F4-007 sin ficha).

Ninguna duplica una ficha `DEF-*` (búsqueda en `08-brechas.md`).

## 4. SOLO_V2 confirmadas

CF-V030 (ingreso y salida de Vigilancia), CF-V031 (corrección de ingresos), CF-V032 (recepción informativa), CF-V033 (montacargas: uso, cobro con IVA opcional y tarifas base), CF-V034 (trazabilidad por placa), CF-V035 (inventario de Bodega, con stubs), y nuevas CF-V036 (autorizaciones de salida y manifiestos: API sin UI alcanzable), CF-V037 (recepción directa sin báscula), CF-V038 (cancelar orden de cargue desde Bodega), CF-V039 (orden de trabajo de cargue en PDF).

## 5. Contraste con el análisis anterior

### 5.1 Estados de `MIGRATION_MATRIX.md` (16 capacidades)

| Capacidad | Estado previo | Clasificación | Motivo |
| --- | --- | --- | --- |
| CF-L168 | COMPORTAMIENTO DIFERENTE («una ubicación por producto») | OBSOLETA | Hay ubicaciones por cantidad (F4-01) |
| CF-L169 | COMPORTAMIENTO DIFERENTE | OBSOLETA | Ubicar, mover y liberar implementados |
| CF-L170 | EXCLUIDA | CONFIRMADA_EN_CODIGO | Sin restos de VIN/Colmotores |
| CF-L171 | PARCIAL («la recepción no valida `IsAvailable`») | OBSOLETA | La recepción valida la ubicación (`PlaceUpToPendingAsync`) |
| CF-L172 | PARCIAL («sin ocupación», «no libera al despachar») | OBSOLETA | Contenido por ubicación y liberación LIFO al cargar |
| CF-L173 | PARCIAL | OBSOLETA | Novedades con desglose (F4-03) |
| CF-L174 | NO ENCONTRADA | OBSOLETA | Editar y anular implementados |
| CF-L175 | EXCLUIDA | CONFIRMADA_EN_CODIGO | Colmotores |
| CF-L176 | EXCLUIDA | CONFIRMADA_EN_CODIGO | Colmotores |
| CF-L177 | NO ENCONTRADA | OBSOLETA | PDF implementado (con diferencias, BR-03-005) |
| CF-L178 | PARCIAL («fotos por recepción, sin borrado») | CONFIRMADA_EN_CODIGO | Sigue así; hoy respaldado por §B.4.8 |
| CF-L179 | CUBIERTA | CONFIRMADA_EN_CODIGO | — |
| CF-L180 | CUBIERTA | CONFIRMADA_EN_CODIGO | Ahora además con cantidades cargadas y LIFO |
| CF-L230 | COMPORTAMIENTO DIFERENTE («sin comprobar guía ni ciclo completo») | CONTRADICHA_POR_CODIGO | La salida se bloquea con pesaje abierto (CHG-30) y con orden de importación sin guía (CHG-33) |
| CF-L236 | EXCLUIDA | CONFIRMADA_EN_CODIGO | Colmotores |
| CF-L254 | CUBIERTA | CONFIRMADA_EN_CODIGO | — |

**Totales:** OBSOLETA 7 · CONFIRMADA_EN_CODIGO 8 · CONTRADICHA_POR_CODIGO 1 · INCOMPLETA 0 · NO_VERIFICADA 0.

### 5.2 Afirmaciones de los planes y documentos

| Afirmación | Fuente | Clasificación | Evidencia |
| --- | --- | --- | --- |
| F4-01 ubicaciones por cantidad (ubicar, mover, liberar) implementado | `plan-backend-paridad-legacy.md` §C.4 | CONFIRMADA_EN_CODIGO | `WarehousePlacementService.cs`, `WarehousePlacementsController.cs`, `PlacementPlannerTests.cs` |
| F4-02 liberar al cargar y cuadrar con el stock | ídem | CONFIRMADA_EN_CODIGO | `ExecuteLoadingOrderCommandHandler.cs:195`; `TrimToStockAsync` en 4 handlers |
| F4-03 novedades con desglose | ídem | CONFIRMADA_EN_CODIGO | `Novelties/*`; más advertencia CHG-57 |
| F4-04 impresión «Reporte de mercancías» | ídem | INCOMPLETA | PDF existe; CPI = depósito, sin salida ni tipo (BR-03-005) |
| F3-01 cargue: liberar reserva no cargada | ídem §C.3 | CONFIRMADA_EN_CODIGO | `ExecuteLoadingOrderCommandHandler.cs:116,200,219-220`; `LoadingExecutionMathTests.cs` |
| Plan frontend fase 4 (F4-02, F4-03) completada | `plan-frontend-paridad-legacy.md` §C.4 | CONFIRMADA_EN_CODIGO | `ProductPlacementsDialog.vue`, `LocationContentPanel.vue`, `novelties/index.vue`, `DepositNoveltiesSection.vue` |
| Novedades con `requiredRoles` Admin, Warehouse, Receiving | plan frontend F4-03 «Roles y menú» | OBSOLETA | Hoy `["Admin","Warehouse"]` (DEF-F9-002, §10 Vigilancia) |
| DF17: camión entre las recepciones del depósito | plan frontend §A.4 | CONFIRMADA_EN_CODIGO | `NoveltyFormDialog.vue:80-99` |
| GAP-004 aceptado (portería sin guía) | `FUNCTIONAL_GAPS.md`; `DECISIONES_REVISION.md` §2.C.10 | CONFIRMADA_EN_CODIGO | No se lee la guía en portería |
| GAP-004: «un camión con mercancía puede salir sin guía»; `ApplyApproval` solo verifica `DateTimeDeparture` | `FUNCTIONAL_GAPS.md` GAP-004 | CONTRADICHA_POR_CODIGO | `EntryLogDepartureGuard.cs:20-40`, también en la aprobación (`UpdateDepartureAuthorizationHandler.cs:85`) |
| GAP-014 y GAP-015 «construir» | `FUNCTIONAL_GAPS.md` | CONFIRMADA_EN_CODIGO | Ver F4-01…04 |
| Ronda de cierre 1: báscula con rol de Vigilancia «abre Bodega completa» | `DECISIONES_REVISION.md` §3.1; `BASCULA_PARITY.md` §6 | OBSOLETA | `WarehouseAccess` = Admin, Warehouse (`WmsPolicyRoles.cs:33-34`); páginas `/warehouse/*` sin Receiving. Conserva la corrección de ingresos |
| «`POST entry-logs` exige `WarehouseAccess`» | `BASCULA_PARITY.md` §6 | CONTRADICHA_POR_CODIGO | `EntryLogController.cs:20` (`GateAccess`) |
| DEC-010 (Bodega solo informa; unidad de carga completa) | `docs/contexto/decisiones.md` | CONFIRMADA_EN_CODIGO | `CreateReceptionCommandHandler.cs:165-181,261-264` |
| DEC-018 (montacargas con IVA opcional) | ídem | CONFIRMADA_EN_CODIGO (con BR-03-009) | `AssignServiceTaxHandler.cs:24-26`; `EndForkliftUseCommandHandler.cs:94-111` |
| DEC-019 (CE-7 no es de Bodega; descartado = «Cancelado») | ídem | CONFIRMADA_EN_CODIGO | `InventoryAdjustmentController.cs:20-21`; `TruckStageResolver.cs:24-26` |
| README y guía del módulo Warehouse: «la recepción actualiza el stock» | `Backend/wms-api/Wms.Application/Warehouse/README.md:134`, `GUIA_USUARIO.md:224`, `Commands/Reception/README.md` | CONTRADICHA_POR_CODIGO | La recepción no mueve stock (DEC-010) |
| «Toda la funcionalidad planeada está implementada» (para este módulo) | `docs/contexto/estado.md` §1 | CONFIRMADA_EN_CODIGO, con las diferencias de §3 | — |

## 6. Incertidumbres

- El uso real de secciones en el legacy parece bajo (6 secciones en 9 bodegas); condiciona BR-03-004 y BR-03-006.
- `WarehouseLocation.WarehouseStorages` (guarda de la baja de ubicaciones) no se rastreó hasta su mapeo EF (BR-03-008, confianza MEDIA).
- Las columnas de la relación de mercancía de la orden en Bodega (`loading-orders/[id].vue`) no se compararon una a una con las del legacy (entrada, saldo anterior, saldo nuevo); confianza MEDIA en CF-L179.

## 7. Lo que quedó sin analizar

- **CF-L172.c (reportes de Bodega):** el inventario general (`GetGeneralInventoryHandler`) es del módulo 07; aquí solo se verificó el filtro por ubicación.
- **Variantes Colmotores:** no se leyeron a fondo (excluidas por decisión); se confirmó la ausencia de restos en V2.
- **Detalle de la factura del montacargas** (numeración, IVA en el documento, aprobación): módulo 06.
- **Pantallas de recepción** (`ReceptionStepCompletion.vue`, `ReceptionStepManualInfo.vue`): se trazaron sus llamadas, no cada validación de formulario.
- Nada se ejecutó: los estados son de código, no de funcionamiento.
