# 05 — Resultado del agente AG-05 (Comercio Exterior: levantes, órdenes de cargue, salidas y guías)

> Auditoría estática del 2026-10-23. No se ejecutaron builds, pruebas, APIs ni consultas a bases de datos, ni comandos Git. Código según `docs/contexto/estado.md`: BE `35a61b2` / FE `c924a8b` (código en disco ese día). El commit `2eeaaad` está en disco y, según `estado.md` §3, no en staging.
> **Prefijos:** `L/` = `bodegas-legacy/`, `B/` = `Backend/wms-api/`, `F/` = `Frontend/wms/app/`, `FT/` = `Backend/wms-api/Wms.Application/ForeignTrade/`.

## 1. Cobertura

| Concepto | Cantidad |
| --- | ---: |
| Capacidades legacy asignadas (`CF-L143…167`, `CF-L238`, `CF-L239`, `CF-L261`) | 28 |
| Capacidades legacy no catalogadas (`CF-LX05-01` bloqueo manual de salidas, `CF-LX05-02` guía solo con cargue completo) | 2 |
| Filas de desglose (`CF-L159.a/.b`, `CF-L163.a/.b`) | 4 |
| Candidatas V2 asignadas (`CF-V050…053`) | 4 |
| Capacidades V2 nuevas (`CF-V054…058`) | 5 |
| Filas de la matriz | 43 |

Las 30 capacidades legacy y las 9 V2 tienen sus cinco dimensiones evaluadas con evidencia de código. Excluidas por decisión (Colmotores): `CF-L148`, `CF-L157`, `CF-L161` → `NO_APLICA`, sin restos en V2 (grep `vin`, `vines`, `Colmotores` en `FT/`, entidades de orden y guía, `F/features/foreign-trade`, `F/pages/foreign-trade`).

## 2. Paridad integral (30 capacidades legacy, filas padre)

| Estado | N.º | Capacidades |
| --- | ---: | --- |
| COMPLETO_CODIGO | 6 | CF-L147, CF-L149, CF-L156, CF-L165, CF-L238, CF-L261 |
| DIFERENCIA_INTENCIONAL | 6 | CF-L150, CF-L167 (GAP-012); CF-L153, CF-L166 (P16); CF-L162 (§B.4.6, P15); CF-L164 (DEC-016) |
| PARCIAL | 13 | CF-L143, CF-L144, CF-L145, CF-L146, CF-L151, CF-L152, CF-L154, CF-L155, CF-L158, CF-L159, CF-L160, CF-L163, CF-L239 |
| NO_IMPLEMENTADO | 2 | CF-LX05-01, CF-LX05-02 |
| NO_APLICA | 3 | CF-L148, CF-L157, CF-L161 |

Desglose: CF-L159.a PARCIAL, CF-L159.b DIFERENCIA_INTENCIONAL (§B.4.6), CF-L163.a PARCIAL, CF-L163.b PARCIAL.

### Por dimensión (30 legacy)

| Dimensión | Estados |
| --- | --- |
| Frontend | COMPLETO_CODIGO 15 · PARCIAL 7 · NO_IMPLEMENTADO 2 · NO_APLICA 6 |
| Backend | COMPLETO_CODIGO 18 · PARCIAL 5 · NO_IMPLEMENTADO 2 · NO_APLICA 5 |
| Integración | CONECTADO_CODIGO 21 · PARCIAL 1 · SIN_INTEGRACION 1 · NO_APLICA 7 |
| Reglas de negocio | COMPLETO_CODIGO 14 · PARCIAL 9 · NO_IMPLEMENTADO 2 · NO_APLICA 5 |

**Validación por ejecución:** 22 de las 30 filas citan casos de QA ejecutados (`docs/qa/resultados/F5-informe-2026-10-02.md`, re-tests en `F11-informe-S2-2026-10-05.md` y `F11-informe-S3-2026-10-06.md`); CF-L143 solo parcialmente (F5-REL-001 probó el filtro por levante, no las fechas). Sin ejecución: las 3 excluidas, CF-L150, CF-L167, CF-L165 (cubierta por QA de báscula, módulo 02), CF-L261 y CF-LX05-01. Ningún caso de QA cubre cancelar una orden con guía vigente ni operaciones simultáneas.

## 3. Brechas

| Criticidad | N.º | IDs |
| --- | ---: | --- |
| CRÍTICA | 0 | — |
| ALTA | 0 | — |
| MEDIA | 7 | BR-05-001 … BR-05-007 |
| BAJA | 6 | BR-05-008 … BR-05-013 |

Las más relevantes:

1. **BR-05-001 (MEDIA)** — Cancelar o modificar una orden con guía vigente no anula ni ajusta la guía ni su factura (pagada si fue de contado), mientras revertir sí exige anularla.
2. **BR-05-002 (MEDIA)** — Reservas y topes de nacionalización sin bloqueo de filas ni token de concurrencia: dos órdenes simultáneas pueden sobre-reservar y despachar más de lo nacionalizado.
3. **BR-05-003 (MEDIA)** — Los levantes de un depósito anulado bloquean su número y aceptación en otros depósitos y no se pueden retirar.
4. **BR-05-006 (MEDIA)** — La guía se emite antes del cargue sin el control del legacy (cargue completo o permiso `crearguiasinautorizacion`).
5. **BR-05-004 / BR-05-005 / BR-05-007 (MEDIA)** — Sin bloqueo manual de salidas por cliente (`sinsalidas`); la cabecera de la orden no se corrige; el filtro de fechas de «Levantes» se ignora (`DateOnly` ← ISO).

Se citan sin duplicar: BR-02-001 (báscula exige orden previa), BR-03-002 y BR-03-003, DEF-F10-001 y DEF-F3-002 (doble envío e idempotencia, verificados).

## 4. SOLO_V2

| ID | Resultado |
| --- | --- |
| CF-V050 Autorización de salida | Es la misma capacidad que **CF-V036** (módulo 03): autorización de salida del vehículo en Vigilancia, no de cargue. UI inalcanzable (BR-03-003). |
| CF-V051 Correcciones de orden de cargue | **Reasignada** a CF-L158, CF-L159.a/.b, CF-L162, CF-L163.a. |
| CF-V052 Guías pendientes | Confirmada. |
| CF-V053 Salida de la orden con tiquete | **Reasignada** a CF-L166 (F4-08, P16). |
| CF-V054 Vista previa y cobro de la guía por cliente dueño | Nueva, confirmada; criterio por depósito pendiente de validar (BR-05-011). |
| CF-V055 Cambiar el modo de pago de la guía | Nueva, confirmada (DEC-019; 2eeaaad, no en staging). |
| CF-V056 ZIP por depósito con registro de impresión | Nueva, confirmada. |
| CF-V057 Orden de cargue externa | Nueva, confirmada (DEC-016). |
| CF-V058 Salida de importación solo con guía y regularización | Nueva, confirmada (QA §10, CHG-33). |

## 5. Contraste con el análisis anterior

### 5.1 Estados de `bodegas-legacy/docs/legacy_analysis/MIGRATION_MATRIX.md` (28 filas, `:147-219`, `:238-240`)

| Clasificación | N.º | Detalle |
| --- | ---: | --- |
| CONFIRMADA_EN_CODIGO | 14 | L147 (por producto), L148, L157, L161 (excluidas), L150 (no se construye), L153 (tipo de guía del depósito), L155 (guía EXP automática), L156 (multi-cliente CE-12), L164 (orden con orden externa), L165, L167 (un soporte de orden externa), L238, L239, L261 (la orden exige ítems) |
| OBSOLETA | 11 | L143 («sin listado propio»: existe F5-03), L144 (ya valida duplicado y registra FOB/tasa), L145 («peso documental»: retirado en F2-01), L146 y L149 (retiro F2-04), L154 y L160 («no limita a lo nacionalizado»: F2-02), L158 y L162 (modificación F3-03), L159 (cancelación, reversión y anulación de guía: F3-02/04/07), L166 (salida con tiquete F4-08 construida) |
| INCOMPLETA | 3 | L151 y L152 («=»: faltan búsqueda por tiquete y fecha, BR-05-008), L163 («no libera ubicaciones»: hoy las libera el cargue; omite el conteo de impresiones y el control del legacy para emitir, BR-05-006, BR-05-010) |
| CONTRADICHA_POR_CODIGO | 0 | — |

### 5.2 Afirmaciones de planes y decisiones

| Afirmación | Clasificación | Evidencia |
| --- | --- | --- |
| Plan backend F2-01 (topes de levante por producto) | CONFIRMADA_EN_CODIGO | `FT/Common/Services/NationalizationBalance.cs:33-34,91-97`; `RegisterImportReleaseCommandHandler.cs:47-55`; `UpdateImportReleaseCommandHandler.cs:57-73` |
| F2-02 (tope de despacho por lo nacionalizado, con reservas) | CONFIRMADA_EN_CODIGO, con salvedad de concurrencia | `CreateLoadingOrderCommandHandler.cs:168-198`; `LoadingOrderReservationService.cs:178-205`; salvedad BR-05-002 |
| F2-03 (levante repetido) | CONFIRMADA_EN_CODIGO | `ReleaseDuplicateLookup.cs:24-38`; el plan no previó los depósitos anulados (BR-05-003) |
| F2-04 (retirar levante) | CONFIRMADA_EN_CODIGO | `WithdrawImportReleaseCommandHandler.cs:43-87` |
| F2-05 (FOB y tasa congelados) | CONFIRMADA_EN_CODIGO | `ReleaseFobService.cs:17,68-79`; `UpdateImportReleaseCommandHandler.cs:91-93` |
| F2-07 (destino por catálogo y vencimiento con días de la ciudad) | CONFIRMADA_EN_CODIGO | `CreateLoadingOrderCommandHandler.cs:254-265,331`; `GuideExpirationCalculator.cs:23-45` |
| F3-01 (cargue parcial, reserva liberada) | NO_VERIFICADA (módulo 03) | Solo se leyó el consumo: la guía congela `LoadedQuantity ?? Quantity` (`DispatchGuideBalanceService.cs:15-21`) |
| F3-02 (cancelar solo antes del cargue, motivo, aviso) | CONFIRMADA_EN_CODIGO | `LoadingOrder.cs:309-330`; `CancelLoadingOrderHandler.cs`; el plan no trató la guía emitida antes (BR-05-001) |
| F3-03 (modificar la orden antes del cargue) | CONFIRMADA_EN_CODIGO | `UpdateLoadingOrderItemsCommandHandler.cs:44-146`; `LoadingOrderEditPlan.cs` |
| F3-04 (anular la guía) | CONFIRMADA_EN_CODIGO | `CancelDispatchGuideCommandHandler.cs:24-67`; `InvoiceCancellationPolicy.cs:21-77`; PDF «ANULADA» `DispatchGuidePdfService.cs:366-372` |
| F3-07 (revertir la salida) | CONFIRMADA_EN_CODIGO | `RevertLoadingOrderCommandHandler.cs:41-164` |
| F4-07 (pesaje compartido) | NO_VERIFICADA (módulo 02) | — |
| F4-08 (salida con tiquete de ingreso, también desde CE) | CONFIRMADA_EN_CODIGO | `LoadingOrderExitController.cs:30-39`; `ExitWithEntryTicketCommandHandler.cs:28-110` |
| F4-10 (cuadrilla en la guía) | CONFIRMADA_EN_CODIGO | `CreateDispatchGuideCommandHandler.cs:62,240`; `DispatchGuidePdfService.cs:599` |
| P16 (sin salida global en lote; una guía por camión) | CONFIRMADA_EN_CODIGO | No existe selección de varios tiquetes; `ExitWithEntryTicketDialog.vue` opera una orden por vez |
| DF4 (FOB una vez por levante) | CONFIRMADA_EN_CODIGO | `ReleaseForm.vue:322-330,446-452` |
| DF18 (salida con tiquete desde el detalle del depósito) | CONFIRMADA_EN_CODIGO | `imports/[id]/index.vue:778,880`; `exports/[id]/index.vue:497,555` |
| GAP-012 (soportes no se construyen) | CONFIRMADA_EN_CODIGO | Sin archivos en levantes ni salidas; solo el soporte de la orden externa |
| DEC-012 (series `2026S` única y `2026OC`, año de emisión) | CONFIRMADA_EN_CODIGO | `DocumentNumberFormat.cs:13-24`; `DocumentNumberGenerator.cs:17`; `ForeignTradeService.cs:78-79` |
| DEC-016 (la orden se conserva, sin PDF al crear, con orden externa; orden y guía separadas) | CONFIRMADA_EN_CODIGO | `CreateLoadingOrderCommandHandler.cs:267-356`; páginas separadas `loading-orders/*` y `dispatch-guides/*` |
| DEC-019 (el modo de pago de la guía sí se cambia) | CONFIRMADA_EN_CODIGO (en disco; no en staging) | `ChangeDispatchGuidePaymentModeCommandHandler.cs`; `dispatch-guides/index.vue` |
| DEC-041 T4 (guía $15.000) | NO_VERIFICADA | El precio es configuración (`ForeignTradeService.cs:22-57`), no código |
| `estado.md` §1 «toda la funcionalidad planeada está implementada» (para este módulo) | CONFIRMADA_EN_CODIGO | Todos los ítems del plan del módulo existen; las brechas son casos no previstos por el plan |

## 6. Incertidumbres

- BR-05-007 se dedujo del contrato (`DateOnly` no admite hora y el filtro de `ModelState` está suprimido); falta ejecutar la llamada.
- BR-05-002 es un análisis de concurrencia; requiere prueba de integración con dos peticiones paralelas.
- No se pudo saber qué caminos de salida usaban realmente los operarios en el legacy, ni si `cliente.sinsalidas` estaba en uso (los datos están fuera del alcance: `db_legacy/`).
- No se determinó si la salida de exportación del legacy exigía levante (`registrarsalidaexp.php:239` copia el aviso de importación).

## 7. Lo que quedó sin analizar y por qué

- **Cargue en Bodega** (`ExecuteLoadingOrderCommandHandler`, F3-01, F4-02) y **pesaje de salida** (F4-07, `RecordWeighing`, repesaje con 409, DEC-019): se leyeron solo los puntos de contacto; los auditan los módulos 03 y 02.
- **Motor de facturación de la guía** (aprobación, N.º SIIGO, consolidadas, pagos): módulo 06.
- **Datos de staging** (precio T4, guías migradas): fuera del alcance estático.
- Los HTML/PDF generados en `L/reportes/salidas/` y `L/reportes/ordenes/` no se abrieron (pueden tener datos de personas).
